"""
Módulo de Dimensionamiento de Celdas, Stacks, Módulos y Sistema SOEC.

Calcula la arquitectura eléctrica y física completa:
- Celdas: área activa, densidad de corriente, corriente unitaria, voltaje, sobrepotenciales.
- Stacks: celdas en serie, voltaje de stack, corriente de stack, potencia de stack.
- Módulos: stacks en paralelo, corriente de módulo, voltaje de módulo, potencia de módulo.
- Sistema Total: módulos en paralelo, superficie activa total, potencia DC y AC,
  flujo de H2 producido, consumo específico (SEC) y balance térmico.
"""

import math
from dataclasses import dataclass
from typing import Dict, Any, Optional
from .thermodynamics import FARADAY, M_H2, M_H2O, M_O2
from .soec_cell import SOECCell, SOECCellResult


@dataclass
class SOECSystemResult:
    # Arquitectura física
    n_cells_per_stack: int
    n_stacks_per_module: int
    n_modules_parallel: int
    n_total_stacks: int
    n_total_cells: int
    area_activa_celda_m2: float
    area_activa_celda_cm2: float
    area_activa_total_m2: float

    # Parámetros operativos
    temperatura_k: float
    temperatura_c: float
    presion_pa: float
    presion_bar: float
    densidad_corriente_a_m2: float
    densidad_corriente_a_cm2: float
    conversion_vapor: float
    eta_faraday: float
    eta_inverter: float

    # Celdas y Stacks
    corriente_celda_a: float
    voltaje_celda_v: float
    corriente_stack_a: float
    voltaje_stack_v: float
    potencia_stack_kw: float

    # Módulos y Sistema Eléctrico
    corriente_modulo_a: float
    voltaje_modulo_v: float
    potencia_modulo_kw: float
    corriente_total_dc_a: float
    voltaje_sistema_dc_v: float
    potencia_dc_total_kw: float
    potencia_dc_total_mw: float
    potencia_ac_total_kw: float
    potencia_ac_total_mw: float

    # Producción y Balances de Materia
    flujo_molar_h2o_in_mol_s: float
    flujo_molar_h2o_in_kmol_h: float
    flujo_molar_h2_in_mol_s: float
    flujo_molar_h2_prod_mol_s: float
    flujo_molar_h2_prod_kmol_h: float
    flujo_masico_h2_prod_kg_s: float
    flujo_masico_h2_prod_kg_h: float
    flujo_molar_o2_prod_mol_s: float
    flujo_molar_o2_prod_kmol_h: float
    flujo_masico_o2_prod_kg_h: float
    flujo_molar_catodico_out_mol_s: float
    flujo_molar_catodico_out_kmol_h: float

    # Consumos Específicos
    sec_dc_kwh_kg_h2: float
    sec_ac_kwh_kg_h2: float
    sec_ac_kwh_nm3_h2: float

    # Balance Térmico
    v_termoneutro: float
    e_nernst: float
    calor_termico_kw: float
    calor_termico_mw: float
    regimen_termico: str

    # Factibilidad
    es_factible: bool
    motivo_infease: str
    cell_result: SOECCellResult


class SOECSystem:
    """
    Simulador y dimensionador del sistema integral SOEC.
    """

    def __init__(self,
                 n_cells_per_stack: int = 100,
                 n_stacks_per_module: int = 312,
                 n_modules_parallel: int = 8,
                 area_activa_celda_m2: float = 0.0150,
                 eta_faraday: float = 0.990,
                 eta_inverter: float = 0.960,
                 cell_model: Optional[SOECCell] = None):
        self.n_cells_per_stack = n_cells_per_stack
        self.n_stacks_per_module = n_stacks_per_module
        self.n_modules_parallel = n_modules_parallel
        self.area_activa_celda_m2 = area_activa_celda_m2
        self.eta_faraday = eta_faraday
        self.eta_inverter = eta_inverter

        if cell_model is None:
            self.cell_model = SOECCell(area_activa_m2=area_activa_celda_m2)
        else:
            self.cell_model = cell_model
            self.cell_model.area_activa_m2 = area_activa_celda_m2

    @property
    def n_total_stacks(self) -> int:
        return self.n_stacks_per_module * self.n_modules_parallel

    @property
    def n_total_cells(self) -> int:
        return self.n_cells_per_stack * self.n_total_stacks

    @property
    def area_activa_total_m2(self) -> float:
        return self.n_total_cells * self.area_activa_celda_m2

    def calcular_con_flujo_fijo(self,
                                flujo_molar_total_in: float, # mol/s
                                fraccion_h2o_in: float,
                                fraccion_h2_in: float,
                                conversion_vapor: float,
                                temperatura_k: float,
                                presion_pa: float,
                                fraccion_o2_in: float = 0.0,
                                presion_anodo_pa: Optional[float] = None) -> SOECSystemResult:
        """
        Calcula el estado del sistema a partir de un flujo de alimentación conocido (modo directo).
        """
        flujo_molar_h2o_in = flujo_molar_total_in * fraccion_h2o_in
        flujo_molar_h2_in = flujo_molar_total_in * fraccion_h2_in
        flujo_molar_h2_prod = flujo_molar_h2o_in * conversion_vapor

        # Corriente requerida por celda (Faraday)
        # n_dot_H2 = (N_total_cells * I_cell * eta_F) / (2 * F)
        i_celda = (flujo_molar_h2_prod * 2.0 * FARADAY) / (self.eta_faraday * self.n_total_cells)
        j = i_celda / self.area_activa_celda_m2

        # Composición media para Nernst y activación
        y_h2o_medio = max(fraccion_h2o_in * (1.0 - 0.5 * conversion_vapor), 1.0e-3)
        y_h2_medio = max(fraccion_h2_in + 0.5 * fraccion_h2o_in * conversion_vapor, 1.0e-3)
        y_o2_medio = 1.000

        cell_res = self.cell_model.calcular(
            densidad_corriente=j,
            temperatura_k=temperatura_k,
            presion_pa=presion_pa,
            y_h2o=y_h2o_medio,
            y_h2=y_h2_medio,
            y_o2=y_o2_medio,
            presion_anodo_pa=presion_anodo_pa
        )

        v_celda = cell_res.v_celda
        v_stack = v_celda * self.n_cells_per_stack if cell_res.es_factible else float('nan')
        i_stack = i_celda  # Celdas en serie
        potencia_stack_kw = (v_stack * i_stack) / 1000.0 if cell_res.es_factible else float('nan')

        # Módulos (stacks en paralelo)
        i_modulo = i_stack * self.n_stacks_per_module
        v_modulo = v_stack
        potencia_modulo_kw = (v_modulo * i_modulo) / 1000.0 if cell_res.es_factible else float('nan')

        # Sistema completo (módulos en paralelo)
        i_total_dc = i_modulo * self.n_modules_parallel
        v_sistema_dc = v_stack
        potencia_dc_total_w = v_celda * i_celda * self.n_total_cells if cell_res.es_factible else float('nan')
        potencia_dc_total_kw = potencia_dc_total_w / 1000.0 if cell_res.es_factible else float('nan')
        potencia_dc_total_mw = potencia_dc_total_kw / 1000.0 if cell_res.es_factible else float('nan')

        potencia_ac_total_kw = potencia_dc_total_kw / self.eta_inverter if cell_res.es_factible else float('nan')
        potencia_ac_total_mw = potencia_ac_total_kw / 1000.0 if cell_res.es_factible else float('nan')

        # Balances de materia
        flujo_masico_h2_kgs = flujo_molar_h2_prod * M_H2
        flujo_masico_h2_kgh = flujo_masico_h2_kgs * 3600.0

        flujo_molar_o2_prod = 0.5 * flujo_molar_h2_prod
        flujo_masico_o2_kgh = flujo_molar_o2_prod * M_O2 * 3600.0

        flujo_molar_h2_out = flujo_molar_h2_in + flujo_molar_h2_prod
        flujo_molar_h2o_out = max(flujo_molar_h2o_in - flujo_molar_h2_prod, 0.0)
        flujo_molar_cat_out = flujo_molar_h2_out + flujo_molar_h2o_out

        # Consumo específico
        if cell_res.es_factible and flujo_masico_h2_kgh > 0:
            sec_dc = potencia_dc_total_kw / flujo_masico_h2_kgh
            sec_ac = potencia_ac_total_kw / flujo_masico_h2_kgh
            # 1 kg H2 = 11.126 Nm³ H2 -> SEC (kWh/Nm³) = SEC (kWh/kg) / 11.126
            sec_ac_nm3 = sec_ac / 11.126
        else:
            sec_dc = float('nan')
            sec_ac = float('nan')
            sec_ac_nm3 = float('nan')

        # Balance térmico
        v_tn = cell_res.v_termoneutro
        if cell_res.es_factible:
            calor_termico_kw = (v_celda - v_tn) * (i_celda * self.n_total_cells) / 1000.0
            calor_termico_mw = calor_termico_kw / 1000.0
            regimen = cell_res.regimen_termico
        else:
            calor_termico_kw = float('nan')
            calor_termico_mw = float('nan')
            regimen = 'No Factible'

        return SOECSystemResult(
            n_cells_per_stack=self.n_cells_per_stack,
            n_stacks_per_module=self.n_stacks_per_module,
            n_modules_parallel=self.n_modules_parallel,
            n_total_stacks=self.n_total_stacks,
            n_total_cells=self.n_total_cells,
            area_activa_celda_m2=self.area_activa_celda_m2,
            area_activa_celda_cm2=self.area_activa_celda_m2 * 10000.0,
            area_activa_total_m2=self.area_activa_total_m2,
            temperatura_k=temperatura_k,
            temperatura_c=temperatura_k - 273.15,
            presion_pa=presion_pa,
            presion_bar=presion_pa / 100000.0,
            densidad_corriente_a_m2=j,
            densidad_corriente_a_cm2=j / 10000.0,
            conversion_vapor=conversion_vapor,
            eta_faraday=self.eta_faraday,
            eta_inverter=self.eta_inverter,
            corriente_celda_a=i_celda,
            voltaje_celda_v=v_celda,
            corriente_stack_a=i_stack,
            voltaje_stack_v=v_stack,
            potencia_stack_kw=potencia_stack_kw,
            corriente_modulo_a=i_modulo,
            voltaje_modulo_v=v_modulo,
            potencia_modulo_kw=potencia_modulo_kw,
            corriente_total_dc_a=i_total_dc,
            voltaje_sistema_dc_v=v_sistema_dc,
            potencia_dc_total_kw=potencia_dc_total_kw,
            potencia_dc_total_mw=potencia_dc_total_mw,
            potencia_ac_total_kw=potencia_ac_total_kw,
            potencia_ac_total_mw=potencia_ac_total_mw,
            flujo_molar_h2o_in_mol_s=flujo_molar_h2o_in,
            flujo_molar_h2o_in_kmol_h=flujo_molar_h2o_in * 3.6,
            flujo_molar_h2_in_mol_s=flujo_molar_h2_in,
            flujo_molar_h2_prod_mol_s=flujo_molar_h2_prod,
            flujo_molar_h2_prod_kmol_h=flujo_molar_h2_prod * 3.6,
            flujo_masico_h2_prod_kg_s=flujo_masico_h2_kgs,
            flujo_masico_h2_prod_kg_h=flujo_masico_h2_kgh,
            flujo_molar_o2_prod_mol_s=flujo_molar_o2_prod,
            flujo_molar_o2_prod_kmol_h=flujo_molar_o2_prod * 3.6,
            flujo_masico_o2_prod_kg_h=flujo_masico_o2_kgh,
            flujo_molar_catodico_out_mol_s=flujo_molar_cat_out,
            flujo_molar_catodico_out_kmol_h=flujo_molar_cat_out * 3.6,
            sec_dc_kwh_kg_h2=sec_dc,
            sec_ac_kwh_kg_h2=sec_ac,
            sec_ac_kwh_nm3_h2=sec_ac_nm3,
            v_termoneutro=v_tn,
            e_nernst=cell_res.e_nernst,
            calor_termico_kw=calor_termico_kw,
            calor_termico_mw=calor_termico_mw,
            regimen_termico=regimen,
            es_factible=cell_res.es_factible,
            motivo_infease=cell_res.motivo_infease,
            cell_result=cell_res
        )

    def dimensionar_para_demanda_h2(self,
                                    demanda_h2_kg_h: float,
                                    densidad_corriente_a_m2: float,
                                    temperatura_k: float,
                                    presion_pa: float,
                                    conversion_vapor: float = 0.70,
                                    fraccion_h2o_in: float = 0.90,
                                    fraccion_h2_in: float = 0.10,
                                    presion_anodo_pa: Optional[float] = None) -> SOECSystemResult:
        """
        Dimensiona el sistema (calcula número entero de celdas, stacks y módulos)
        para satisfacer exactamente la demanda requerida de H2 [kg/h] a una
        densidad de corriente j dada.
        """
        flujo_masico_h2_kg_s = demanda_h2_kg_h / 3600.0
        flujo_molar_h2_prod = flujo_masico_h2_kg_s / M_H2  # mol/s

        # Flujo de vapor requerido
        flujo_molar_h2o_in = flujo_molar_h2_prod / conversion_vapor
        flujo_molar_total_in = flujo_molar_h2o_in / fraccion_h2o_in

        # Corriente por celda a la j especificada
        i_celda = densidad_corriente_a_m2 * self.area_activa_celda_m2

        # Celdas totales continuas requeridas:
        # n_dot_H2 = (N_total * I_cell * eta_F) / (2 * F)
        n_cells_req_exact = (flujo_molar_h2_prod * 2.0 * FARADAY) / (i_celda * self.eta_faraday)

        # Dimensionamiento discreto (número entero de stacks)
        stacks_req = math.ceil(n_cells_req_exact / self.n_cells_per_stack)

        # Distribuir en módulos
        modules_req = math.ceil(stacks_req / self.n_stacks_per_module)
        # Ajustar stacks por módulo para balance perfecto si es necesario
        stacks_per_mod = math.ceil(stacks_req / modules_req)
        total_stacks_actual = modules_req * stacks_per_mod
        total_cells_actual = total_stacks_actual * self.n_cells_per_stack

        # Ajuste fino de la j real para cumplir EXACTAMENTE la producción requerida
        # con el número entero real de celdas:
        i_celda_real = (flujo_molar_h2_prod * 2.0 * FARADAY) / (self.eta_faraday * total_cells_actual)
        j_real = i_celda_real / self.area_activa_celda_m2

        # Creamos una instancia con los parámetros dimensionados
        sys_dimensionado = SOECSystem(
            n_cells_per_stack=self.n_cells_per_stack,
            n_stacks_per_module=stacks_per_mod,
            n_modules_parallel=modules_req,
            area_activa_celda_m2=self.area_activa_celda_m2,
            eta_faraday=self.eta_faraday,
            eta_inverter=self.eta_inverter,
            cell_model=self.cell_model
        )

        return sys_dimensionado.calcular_con_flujo_fijo(
            flujo_molar_total_in=flujo_molar_total_in,
            fraccion_h2o_in=fraccion_h2o_in,
            fraccion_h2_in=fraccion_h2_in,
            conversion_vapor=conversion_vapor,
            temperatura_k=temperatura_k,
            presion_pa=presion_pa,
            presion_anodo_pa=presion_anodo_pa
        )

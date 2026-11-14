"""
Módulo de Análisis de Sensibilidad para SOEC.

Implementa:
1. Sensibilidad Individual OAT (One-At-a-Time):
   - Temperatura (700-850 °C)
   - Presión (1-30 bar)
   - Densidad de corriente (0.20-0.90 A/cm²)
   - Área activa por celda (100-300 cm²)
   - Conversión de vapor (50-85 %)
   - ASR_ref (0.10-0.40 Ohm*cm²)
   - Eficiencia Faradaica (95-100 %)
   - Celdas por stack (50-400)
2. Diseño de Experimentos (DOE) mediante Latin Hypercube Sampling (LHS).
3. Sensibilidad Global (Método de Morris e Índices de Sobol) y Ranking de Parámetros.
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from .thermodynamics import R_GAS, FARADAY
from .soec_cell import SOECCell
from .stack_module_sizing import SOECSystem, SOECSystemResult


def ejecutar_analisis_oat(base_system: SOECSystem,
                          flujo_molar_total_in: float = 154.76,
                          fraccion_h2o_in: float = 0.90,
                          fraccion_h2_in: float = 0.10,
                          conversion_base: float = 0.70,
                          t_base_k: float = 1023.15,
                          p_base_pa: float = 2000000.0) -> Dict[str, pd.DataFrame]:
    """
    Ejecuta el análisis One-At-a-Time (OAT) variando un parámetro a la vez
    mientras los demás se mantienen congelados en el Caso Base.
    """
    res_base = base_system.calcular_con_flujo_fijo(
        flujo_molar_total_in=flujo_molar_total_in,
        fraccion_h2o_in=fraccion_h2o_in,
        fraccion_h2_in=fraccion_h2_in,
        conversion_vapor=conversion_base,
        temperatura_k=t_base_k,
        presion_pa=p_base_pa
    )

    sec_base = res_base.sec_ac_kwh_kg_h2
    pot_base = res_base.potencia_ac_total_mw
    v_base = res_base.voltaje_celda_v
    h2_base = res_base.flujo_masico_h2_prod_kg_h

    dfs_oat = {}

    # 1. TEMPERATURA (700 - 850 °C)
    t_c_range = np.linspace(700.0, 850.0, 16)
    rows_t = []
    for tc in t_c_range:
        tk = tc + 273.15
        r = base_system.calcular_con_flujo_fijo(
            flujo_molar_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, tk, p_base_pa
        )
        rows_t.append({
            'Parametro': 'Temperatura',
            'Valor': tc,
            'Unidad': '°C',
            'T_K': tk,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Temperatura'] = pd.DataFrame(rows_t)

    # 2. PRESIÓN (1 - 30 bar)
    p_bar_range = np.linspace(1.0, 30.0, 15)
    rows_p = []
    for pb in p_bar_range:
        ppa = pb * 100000.0
        r = base_system.calcular_con_flujo_fijo(
            flujo_molar_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, t_base_k, ppa
        )
        rows_p.append({
            'Parametro': 'Presion',
            'Valor': pb,
            'Unidad': 'bar',
            'P_Pa': ppa,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Presion'] = pd.DataFrame(rows_p)

    # 3. DENSIDAD DE CORRIENTE (0.20 - 0.90 A/cm² -> 2000 - 9000 A/m²)
    # Para variar j manteniendo las celdas, se varía el flujo de vapor alimentado proporcionalmente
    j_cm2_range = np.linspace(0.20, 0.90, 15)
    rows_j = []
    for j_cm2 in j_cm2_range:
        j_m2 = j_cm2 * 10000.0
        i_celda = j_m2 * base_system.area_activa_celda_m2
        flujo_h2_prod = (base_system.n_total_cells * i_celda * base_system.eta_faraday) / (2.0 * FARADAY)
        flujo_total_in = flujo_h2_prod / (conversion_base * fraccion_h2o_in)

        r = base_system.calcular_con_flujo_fijo(
            flujo_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, t_base_k, p_base_pa
        )
        rows_j.append({
            'Parametro': 'Densidad_Corriente',
            'Valor': j_cm2,
            'Unidad': 'A/cm²',
            'j_A_m2': j_m2,
            'I_celda_A': r.corriente_celda_a,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Densidad_Corriente'] = pd.DataFrame(rows_j)

    # 4. CONVERSIÓN DE VAPOR (50 % - 85 %)
    conv_range = np.linspace(0.50, 0.85, 15)
    rows_c = []
    for c_val in conv_range:
        # Manteniendo producción fija de H2, el flujo de vapor requerido es n_H2 / c_val
        flujo_h2o_in = (flujo_molar_total_in * fraccion_h2o_in * conversion_base) / c_val
        flujo_tot = flujo_h2o_in / fraccion_h2o_in
        r = base_system.calcular_con_flujo_fijo(
            flujo_tot, fraccion_h2o_in, fraccion_h2_in, c_val, t_base_k, p_base_pa
        )
        rows_c.append({
            'Parametro': 'Conversion_Vapor',
            'Valor': c_val * 100.0,
            'Unidad': '%',
            'Conversion': c_val,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Conversion_Vapor'] = pd.DataFrame(rows_c)

    # 5. ÁREA ACTIVA POR CELDA (100 - 300 cm² -> 0.010 - 0.030 m²)
    a_cell_range = np.linspace(100.0, 300.0, 11)
    rows_a = []
    for a_cm2 in a_cell_range:
        a_m2 = a_cm2 / 10000.0
        sys_temp = SOECSystem(
            n_cells_per_stack=base_system.n_cells_per_stack,
            n_stacks_per_module=base_system.n_stacks_per_module,
            n_modules_parallel=base_system.n_modules_parallel,
            area_activa_celda_m2=a_m2,
            eta_faraday=base_system.eta_faraday,
            eta_inverter=base_system.eta_inverter,
            cell_model=SOECCell(area_activa_m2=a_m2, asr_ref=base_system.cell_model.asr_ref)
        )
        r = sys_temp.calcular_con_flujo_fijo(
            flujo_molar_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, t_base_k, p_base_pa
        )
        rows_a.append({
            'Parametro': 'Area_Celda',
            'Valor': a_cm2,
            'Unidad': 'cm²',
            'Area_m2': a_m2,
            'j_A_cm2': r.densidad_corriente_a_cm2,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Superficie_Total_m2': r.area_activa_total_m2,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Area_Celda'] = pd.DataFrame(rows_a)

    # 6. ASR_REF (0.10 - 0.40 Ohm*cm² -> 1.0e-5 - 4.0e-5 Ohm*m²)
    asr_cm2_range = np.linspace(0.10, 0.40, 13)
    rows_asr = []
    for asr_cm2 in asr_cm2_range:
        asr_m2 = asr_cm2 / 10000.0
        sys_temp = SOECSystem(
            n_cells_per_stack=base_system.n_cells_per_stack,
            n_stacks_per_module=base_system.n_stacks_per_module,
            n_modules_parallel=base_system.n_modules_parallel,
            area_activa_celda_m2=base_system.area_activa_celda_m2,
            eta_faraday=base_system.eta_faraday,
            eta_inverter=base_system.eta_inverter,
            cell_model=SOECCell(area_activa_m2=base_system.area_activa_celda_m2, asr_ref=asr_m2)
        )
        r = sys_temp.calcular_con_flujo_fijo(
            flujo_molar_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, t_base_k, p_base_pa
        )
        rows_asr.append({
            'Parametro': 'ASR_Ref',
            'Valor': asr_cm2,
            'Unidad': 'Ω·cm²',
            'ASR_Ohm_m2': asr_m2,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['ASR_Ref'] = pd.DataFrame(rows_asr)

    # 7. EFICIENCIA FARADAICA (0.95 - 1.00)
    eta_f_range = np.linspace(0.95, 1.00, 11)
    rows_ef = []
    for ef in eta_f_range:
        sys_temp = SOECSystem(
            n_cells_per_stack=base_system.n_cells_per_stack,
            n_stacks_per_module=base_system.n_stacks_per_module,
            n_modules_parallel=base_system.n_modules_parallel,
            area_activa_celda_m2=base_system.area_activa_celda_m2,
            eta_faraday=ef,
            eta_inverter=base_system.eta_inverter,
            cell_model=base_system.cell_model
        )
        r = sys_temp.calcular_con_flujo_fijo(
            flujo_molar_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, t_base_k, p_base_pa
        )
        rows_ef.append({
            'Parametro': 'Eficiencia_Faraday',
            'Valor': ef * 100.0,
            'Unidad': '%',
            'Eta_Faraday': ef,
            'j_A_cm2': r.densidad_corriente_a_cm2,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'SEC_DC_kWh_kg': r.sec_dc_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Eficiencia_Faraday'] = pd.DataFrame(rows_ef)

    # 8. CELDAS POR STACK (50 - 400)
    # Variando celdas por stack manteniendo el número total de celdas constante
    # (redistribución serie / paralelo)
    cells_per_stack_range = [50, 75, 100, 125, 150, 200, 250, 300, 400]
    rows_cps = []
    total_cells_target = base_system.n_total_cells
    for cps in cells_per_stack_range:
        total_stacks = total_cells_target // cps
        mod_par = 8
        stacks_per_mod = total_stacks // mod_par
        sys_temp = SOECSystem(
            n_cells_per_stack=cps,
            n_stacks_per_module=stacks_per_mod,
            n_modules_parallel=mod_par,
            area_activa_celda_m2=base_system.area_activa_celda_m2,
            eta_faraday=base_system.eta_faraday,
            eta_inverter=base_system.eta_inverter,
            cell_model=base_system.cell_model
        )
        r = sys_temp.calcular_con_flujo_fijo(
            flujo_molar_total_in, fraccion_h2o_in, fraccion_h2_in, conversion_base, t_base_k, p_base_pa
        )
        rows_cps.append({
            'Parametro': 'Celdas_por_Stack',
            'Valor': cps,
            'Unidad': 'celdas/stack',
            'N_cells_per_stack': cps,
            'N_stacks_per_mod': stacks_per_mod,
            'N_total_stacks': sys_temp.n_total_stacks,
            'V_celda_V': r.voltaje_celda_v,
            'V_stack_V': r.voltaje_stack_v,
            'I_stack_A': r.corriente_stack_a,
            'Potencia_AC_MW': r.potencia_ac_total_mw,
            'Potencia_DC_MW': r.potencia_dc_total_mw,
            'H2_prod_kgh': r.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': r.sec_ac_kwh_kg_h2,
            'Delta_SEC_pct': ((r.sec_ac_kwh_kg_h2 - sec_base) / sec_base) * 100.0,
            'Delta_Pot_pct': ((r.potencia_ac_total_mw - pot_base) / pot_base) * 100.0,
            'Calor_kW': r.calor_termico_kw,
            'Regimen': r.regimen_termico,
            'Es_Factible': r.es_factible,
            'Motivo': r.motivo_infease
        })
    dfs_oat['Celdas_por_Stack'] = pd.DataFrame(rows_cps)

    return dfs_oat


def ejecutar_doe_lhs(base_system: SOECSystem,
                     n_muestras: int = 150,
                     semilla: int = 42,
                     demanda_h2_kg_h: float = 707.57) -> pd.DataFrame:
    """
    Ejecuta un Diseño de Experimentos (DOE) mediante Latin Hypercube Sampling (LHS).
    Permite estudiar interacciones no lineales entre parámetros clave:
    - Temperatura (700 - 850 °C)
    - Presión (5 - 30 bar)
    - Densidad de corriente (0.25 - 0.85 A/cm²)
    - Área activa (100 - 250 cm²)
    - Conversión de vapor (55 % - 80 %)
    - ASR_ref (0.15 - 0.35 Ohm*cm²)
    """
    np.random.seed(semilla)

    # Rangos de exploración
    rangos = {
        'T_C': (700.0, 850.0),
        'P_bar': (5.0, 30.0),
        'j_A_cm2': (0.25, 0.85),
        'A_cell_cm2': (100.0, 250.0),
        'conv_pct': (55.0, 80.0),
        'asr_Ohm_cm2': (0.15, 0.35)
    }

    n_vars = len(rangos)
    # Generación de hipercubo latino estratificado
    lhs_norm = np.zeros((n_muestras, n_vars))
    for i in range(n_vars):
        perm = np.random.permutation(n_muestras)
        lhs_norm[:, i] = (perm + np.random.uniform(size=n_muestras)) / n_muestras

    records = []
    keys = list(rangos.keys())

    for idx in range(n_muestras):
        tc = rangos['T_C'][0] + lhs_norm[idx, 0] * (rangos['T_C'][1] - rangos['T_C'][0])
        pbar = rangos['P_bar'][0] + lhs_norm[idx, 1] * (rangos['P_bar'][1] - rangos['P_bar'][0])
        j_cm2 = rangos['j_A_cm2'][0] + lhs_norm[idx, 2] * (rangos['j_A_cm2'][1] - rangos['j_A_cm2'][0])
        acm2 = rangos['A_cell_cm2'][0] + lhs_norm[idx, 3] * (rangos['A_cell_cm2'][1] - rangos['A_cell_cm2'][0])
        conv = (rangos['conv_pct'][0] + lhs_norm[idx, 4] * (rangos['conv_pct'][1] - rangos['conv_pct'][0])) / 100.0
        asrcm2 = rangos['asr_Ohm_cm2'][0] + lhs_norm[idx, 5] * (rangos['asr_Ohm_cm2'][1] - rangos['asr_Ohm_cm2'][0])

        tk = tc + 273.15
        ppa = pbar * 100000.0
        am2 = acm2 / 10000.0
        asrm2 = asrcm2 / 10000.0
        jm2 = j_cm2 * 10000.0

        sys_temp = SOECSystem(
            n_cells_per_stack=100,
            n_stacks_per_module=312,
            n_modules_parallel=8,
            area_activa_celda_m2=am2,
            cell_model=SOECCell(area_activa_m2=am2, asr_ref=asrm2)
        )

        res = sys_temp.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=jm2,
            temperatura_k=tk,
            presion_pa=ppa,
            conversion_vapor=conv
        )

        records.append({
            'Experimento_ID': idx + 1,
            'T_C': tc,
            'P_bar': pbar,
            'j_A_cm2': j_cm2,
            'A_cell_cm2': acm2,
            'Conversion_pct': conv * 100.0,
            'ASR_Ohm_cm2': asrcm2,
            'V_celda_V': res.voltaje_celda_v,
            'V_stack_V': res.voltaje_stack_v,
            'N_total_cells': res.n_total_cells,
            'N_total_stacks': res.n_total_stacks,
            'N_modules': res.n_modules_parallel,
            'Superficie_Total_m2': res.area_activa_total_m2,
            'Potencia_DC_MW': res.potencia_dc_total_mw,
            'Potencia_AC_MW': res.potencia_ac_total_mw,
            'H2_prod_kgh': res.flujo_masico_h2_prod_kg_h,
            'SEC_AC_kWh_kg': res.sec_ac_kwh_kg_h2,
            'Calor_kW': res.calor_termico_kw,
            'Regimen': res.regimen_termico,
            'Es_Factible': res.es_factible,
            'Motivo': res.motivo_infease
        })

    return pd.DataFrame(records)


def calcular_sensibilidad_global_morris(base_system: SOECSystem,
                                        n_trajectories: int = 20,
                                        p_levels: int = 4,
                                        semilla: int = 42,
                                        demanda_h2_kg_h: float = 707.57) -> pd.DataFrame:
    """
    Calcula los Efectos Elementales del Método de Morris:
    - mu*: Media de los valores absolutos de los efectos elementales (importancia global).
    - sigma: Desviación estándar (no linealidades e interacciones).
    """
    np.random.seed(semilla)

    params = {
        'Temperatura': (700.0, 850.0),       # °C
        'Presion': (5.0, 30.0),              # bar
        'Densidad_Corriente': (0.25, 0.85),  # A/cm²
        'Area_Celda': (100.0, 250.0),        # cm²
        'Conversion': (0.55, 0.80),          # fracción
        'ASR_Ref': (0.15, 0.35)              # Ohm*cm²
    }
    k = len(params)
    delta = p_levels / (2 * (p_levels - 1))
    param_names = list(params.keys())

    # Funciones de evaluación de salida
    def evaluar(p_vec):
        tc = p_vec[0]
        pbar = p_vec[1]
        j_cm2 = p_vec[2]
        acm2 = p_vec[3]
        conv = p_vec[4]
        asrcm2 = p_vec[5]

        tk = tc + 273.15
        ppa = pbar * 100000.0
        am2 = acm2 / 10000.0
        asrm2 = asrcm2 / 10000.0
        jm2 = j_cm2 * 10000.0

        sys_temp = SOECSystem(
            n_cells_per_stack=100,
            n_stacks_per_module=312,
            n_modules_parallel=8,
            area_activa_celda_m2=am2,
            cell_model=SOECCell(area_activa_m2=am2, asr_ref=asrm2)
        )
        res = sys_temp.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=jm2,
            temperatura_k=tk,
            presion_pa=ppa,
            conversion_vapor=conv
        )
        sec = res.sec_ac_kwh_kg_h2 if res.es_factible else 50.0
        pot = res.potencia_ac_total_mw if res.es_factible else 40.0
        v_c = res.voltaje_celda_v if res.es_factible else 2.0
        area_tot = res.area_activa_total_m2 if res.es_factible else 10000.0
        return np.array([pot, sec, v_c, area_tot])

    outputs_labels = ['Potencia_MW', 'SEC_AC', 'Voltaje_Celda', 'Area_Total']
    ee_dict = {lbl: {p: [] for p in param_names} for lbl in outputs_labels}

    for _ in range(n_trajectories):
        # Base random point en rejilla
        base_grid = np.random.choice(np.linspace(0.0, 1.0 - delta, p_levels), size=k)
        x_base = np.zeros(k)
        for i, p in enumerate(param_names):
            p_min, p_max = params[p]
            x_base[i] = p_min + base_grid[i] * (p_max - p_min)

        y_base = evaluar(x_base)
        perm = np.random.permutation(k)

        x_curr = x_base.copy()
        for idx_step in perm:
            p = param_names[idx_step]
            p_min, p_max = params[p]
            step_size = delta * (p_max - p_min)
            # Perturbar
            x_new = x_curr.copy()
            if x_curr[idx_step] + step_size <= p_max:
                x_new[idx_step] += step_size
                actual_step = step_size
            else:
                x_new[idx_step] -= step_size
                actual_step = -step_size

            y_new = evaluar(x_new)
            norm_step = actual_step / (p_max - p_min)

            ee_val = (y_new - y_base) / norm_step
            for out_idx, lbl in enumerate(outputs_labels):
                ee_dict[lbl][p].append(ee_val[out_idx])

            x_curr = x_new
            y_base = y_new

    # Compilar estadísticas de Morris
    morris_results = []
    for lbl in outputs_labels:
        for p in param_names:
            arr = np.array(ee_dict[lbl][p])
            mu_star = np.mean(np.abs(arr))
            sigma = np.std(arr)
            morris_results.append({
                'Variable_Objetivo': lbl,
                'Parametro': p,
                'Mu_Star': mu_star,
                'Sigma': sigma,
                'Ratio_Sigma_Mu': sigma / max(mu_star, 1e-6)
            })

    df_morris = pd.DataFrame(morris_results)
    return df_morris


def calcular_ranking_influencia(df_morris: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un ranking global consolidado de influencia de parámetros
    ponderando SEC, Potencia y Voltaje de celda.
    """
    df_sec = df_morris[df_morris['Variable_Objetivo'] == 'SEC_AC'].copy()
    df_sec = df_sec.sort_values(by='Mu_Star', ascending=False).reset_index(drop=True)
    df_sec['Ranking_SEC'] = df_sec.index + 1

    df_pot = df_morris[df_morris['Variable_Objetivo'] == 'Potencia_MW'].copy()
    df_pot = df_pot.sort_values(by='Mu_Star', ascending=False).reset_index(drop=True)
    df_pot['Ranking_Potencia'] = df_pot.index + 1

    merged = pd.merge(df_sec[['Parametro', 'Mu_Star', 'Sigma', 'Ranking_SEC']],
                      df_pot[['Parametro', 'Ranking_Potencia']], on='Parametro')
    merged['Score_Ponderado'] = merged['Mu_Star'] / merged['Mu_Star'].max() * 100.0
    merged = merged.sort_values(by='Score_Ponderado', ascending=False).reset_index(drop=True)
    merged['Ranking_Global'] = merged.index + 1
    return merged

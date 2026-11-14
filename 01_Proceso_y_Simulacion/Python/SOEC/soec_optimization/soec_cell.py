"""
Módulo de Celda Individual SOEC y Curva de Polarización.

Integra termodinámica, Nernst, activación, pérdidas óhmicas y difusión.
Calcula el voltaje de celda:
    V_celda = E_Nernst + eta_act + eta_ohm + eta_conc

Proporciona diagnósticos completos de sobrepotenciales, eficiencia y factibilidad.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from .thermodynamics import calcular_termodinamica, R_GAS, FARADAY, P_STD
from .nernst import calcular_nernst, calcular_nernst_perfil
from .kinetics import calcular_cinetica_activacion
from .ohmic import calcular_perdidas_ohmicas
from .concentration import calcular_perdidas_concentracion


@dataclass
class SOECCellResult:
    temperatura_k: float
    temperatura_c: float
    presion_pa: float
    presion_bar: float
    densidad_corriente_a_m2: float
    densidad_corriente_a_cm2: float
    area_activa_m2: float
    area_activa_cm2: float
    corriente_celda_a: float
    e_rev_std: float
    v_termoneutro: float
    e_nernst: float
    eta_act_c: float
    eta_act_a: float
    eta_act_total: float
    eta_ohm: float
    asr_ohm_m2: float
    asr_ohm_cm2: float
    eta_conc: float
    j_limit: float
    v_celda: float
    calor_celda_w: float
    regimen_termico: str  # 'Endotermico', 'Termoneutro', 'Exotermico'
    es_factible: bool
    motivo_infease: str
    detalles: Dict[str, Any]


class SOECCell:
    """
    Representa una celda unitaria de electrólisis de óxido sólido.
    """

    def __init__(self,
                 area_activa_m2: float = 0.0150,     # 150 cm²
                 alpha: float = 0.50,
                 j0_c_ref: float = 5300.0,
                 j0_a_ref: float = 3500.0,
                 e_act_c: float = 100000.0,
                 e_act_a: float = 120000.0,
                 asr_ref: float = 2.20e-5,          # 0.22 Ohm*cm²
                 e_ohm: float = 90000.0,
                 j_limit_ref: float = 25000.0,
                 t_ref: float = 1023.15,
                 v_celda_max: float = 1.60,
                 v_celda_min: float = 0.80,
                 use_rigorous_thermo: bool = True,
                 modo_estricto: bool = True):
        self.area_activa_m2 = area_activa_m2
        self.alpha = alpha
        self.j0_c_ref = j0_c_ref
        self.j0_a_ref = j0_a_ref
        self.e_act_c = e_act_c
        self.e_act_a = e_act_a
        self.asr_ref = asr_ref
        self.e_ohm = e_ohm
        self.j_limit_ref = j_limit_ref
        self.t_ref = t_ref
        self.v_celda_max = v_celda_max
        self.v_celda_min = v_celda_min
        self.use_rigorous_thermo = use_rigorous_thermo
        self.modo_estricto = modo_estricto

    def calcular(self,
                 densidad_corriente: float,
                 temperatura_k: float,
                 presion_pa: float,
                 y_h2o: float,
                 y_h2: float,
                 y_o2: float = 1.0,
                 presion_anodo_pa: Optional[float] = None) -> SOECCellResult:
        """
        Calcula el estado electroquímico de la celda a una densidad de corriente j.
        """
        j = densidad_corriente
        tk = temperatura_k
        tc = tk - 273.15
        p_bar = presion_pa / 100000.0

        motivos = []
        es_factible = True

        # Restricciones de temperatura de materiales (SOEC estándar 650 °C - 900 °C)
        if tc < 650.0 or tc > 900.0:
            es_factible = False
            motivos.append(f'Temperatura {tc:.1f}°C fuera del rango de estabilidad (650-900°C)')

        # Restricciones de presión (1 a 35 bar)
        if p_bar < 0.9 or p_bar > 35.0:
            es_factible = False
            motivos.append(f'Presión {p_bar:.1f} bar fuera de rango operativo (1-35 bar)')

        # 1. Termodinámica
        thermo = calcular_termodinamica(tk, use_rigorous=self.use_rigorous_thermo)
        e_rev_std = thermo['e_rev_std']
        v_tn = thermo['v_termoneutro']

        # 2. Nernst
        e_nernst = calcular_nernst(e_rev_std, tk, presion_pa, y_h2o, y_h2, y_o2, presion_anodo_pa)

        # 3. Cinética de activación
        kin = calcular_cinetica_activacion(j, tk,
                                           j0_c_ref=self.j0_c_ref,
                                           j0_a_ref=self.j0_a_ref,
                                           e_act_c=self.e_act_c,
                                           e_act_a=self.e_act_a,
                                           alpha=self.alpha,
                                           t_ref=self.t_ref,
                                           y_h2o=y_h2o,
                                           y_h2=y_h2,
                                           y_o2=y_o2)
        eta_act_c = kin['eta_act_c']
        eta_act_a = kin['eta_act_a']
        eta_act_total = kin['eta_act_total']

        # 4. Pérdidas óhmicas
        ohm = calcular_perdidas_ohmicas(j, tk,
                                        asr_ref=self.asr_ref,
                                        e_ohm=self.e_ohm,
                                        t_ref=self.t_ref)
        eta_ohm = ohm['eta_ohm']
        asr_ohm_m2 = ohm['asr_ohm_m2']
        asr_ohm_cm2 = ohm['asr_ohm_cm2']

        # 5. Polarización por concentración
        conc = calcular_perdidas_concentracion(j, tk, presion_pa, y_h2o,
                                               j_limit_ref=self.j_limit_ref,
                                               t_ref=self.t_ref,
                                               modo_estricto=self.modo_estricto)
        eta_conc = conc['eta_conc']
        j_limit = conc['j_limit']

        if not conc['es_factible']:
            es_factible = False
            motivos.append(conc['motivo'])

        # 6. Voltaje de celda
        if es_factible:
            v_celda = e_nernst + eta_act_total + eta_ohm + eta_conc
            if v_celda > self.v_celda_max:
                es_factible = False
                motivos.append(f'Voltaje {v_celda:.4f} V excede límite de degradación ({self.v_celda_max:.2f} V)')
            elif v_celda < self.v_celda_min:
                es_factible = False
                motivos.append(f'Voltaje {v_celda:.4f} V por debajo del límite mínimo ({self.v_celda_min:.2f} V)')
        else:
            v_celda = float('nan')

        # 7. Corriente y calor de celda
        i_celda = j * self.area_activa_m2
        if es_factible:
            calor_celda = (v_celda - v_tn) * i_celda  # W
            if abs(v_celda - v_tn) < 0.005:
                regimen = 'Termoneutro'
            elif v_celda > v_tn:
                regimen = 'Exotermico'
            else:
                regimen = 'Endotermico'
        else:
            calor_celda = float('nan')
            regimen = 'No Factible'

        motivo_str = '; '.join(motivos) if motivos else 'Factible'

        return SOECCellResult(
            temperatura_k=tk,
            temperatura_c=tc,
            presion_pa=presion_pa,
            presion_bar=p_bar,
            densidad_corriente_a_m2=j,
            densidad_corriente_a_cm2=j / 10000.0,
            area_activa_m2=self.area_activa_m2,
            area_activa_cm2=self.area_activa_m2 * 10000.0,
            corriente_celda_a=i_celda,
            e_rev_std=e_rev_std,
            v_termoneutro=v_tn,
            e_nernst=e_nernst,
            eta_act_c=eta_act_c,
            eta_act_a=eta_act_a,
            eta_act_total=eta_act_total,
            eta_ohm=eta_ohm,
            asr_ohm_m2=asr_ohm_m2,
            asr_ohm_cm2=asr_ohm_cm2,
            eta_conc=eta_conc,
            j_limit=j_limit,
            v_celda=v_celda,
            calor_celda_w=calor_celda,
            regimen_termico=regimen,
            es_factible=es_factible,
            motivo_infease=motivo_str,
            detalles={'thermo': thermo, 'kin': kin, 'ohm': ohm, 'conc': conc}
        )

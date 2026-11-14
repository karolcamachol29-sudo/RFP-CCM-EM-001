"""
Módulo de Integración Térmica para SOEC y Planta de e-Metanol.

Analiza:
1. Regímenes de celda:
   - Endotérmico (V_celda < V_tn): absorbe calor de la celda.
   - Termoneutro (V_celda = V_tn): balance adiabático exacto.
   - Exotérmico (V_celda > V_tn): genera calor por sobrepotenciales.
2. Integración con el proceso de síntesis de metanol:
   - Calor de reacción exotérmico de R-401 (9,139 kW - 12,335 kW) transferido
     a la carcasa R-401-S para generar vapor saturado a 20 bar (220 °C).
   - Sobrecalentamiento de vapor de 220 °C a 750 °C (E-202).
   - Recuperación de calor sensible del efluente catódico a 750 °C (E-203).
3. Comparación de escenarios de integración:
   - Escenario A: Suministro térmico 100% externo (sin integración).
   - Escenario B: Recuperación de calor de R-401 (caldera en carcasa).
   - Escenario C: Integración térmica óptima (R-401-S + intercambiador efluente-alimentación FEHE).
"""

from dataclasses import dataclass
from typing import Dict, Any
from .thermodynamics import FARADAY, R_GAS


@dataclass
class ThermalIntegrationResult:
    v_celda: float
    v_termoneutro: float
    e_nernst: float
    regimen_celda: str
    calor_reaccion_celda_kw: float
    calor_reaccion_celda_mw: float

    # Demandas térmicas externas de la sección SOEC
    calor_generacion_vapor_20bar_kw: float       # 25°C líq -> 220°C vap sat
    calor_sobrecalentamiento_750c_kw: float      # 220°C -> 750°C
    calor_recuperable_efluente_catodico_kw: float# 750°C -> 38°C
    calor_recuperable_efluente_anodico_kw: float # 750°C -> 31°C

    # Integración con Planta de Metanol
    calor_disponible_r401_kw: float              # Exotérmico de síntesis
    ahorro_caldera_r401_kw: float
    ahorro_fehe_recuperador_kw: float

    # Balances netos por escenario
    escenario_a_demanda_termica_neta_kw: float   # Sin integración
    escenario_b_demanda_termica_neta_kw: float   # Con caldera R-401
    escenario_c_demanda_termica_neta_kw: float   # Integración total FEHE + R-401

    # Eficiencia energética
    sec_electrico_ac_kwh_kg: float
    sec_termico_equivalente_kwh_kg: float
    sec_energetico_total_kwh_kg: float
    detalles: Dict[str, Any]


def analizar_integracion_termica(system_result,
                                 calor_r401_disponible_kw: float = 12335.0,
                                 eficiencia_fehe: float = 0.85) -> ThermalIntegrationResult:
    """
    Calcula el balance térmico integral de la SOEC acoplada al flowsheet de e-metanol.
    """
    v_c = system_result.voltaje_celda_v
    v_tn = system_result.v_termoneutro
    e_nernst = system_result.e_nernst
    i_total = system_result.corriente_total_dc_a
    m_h2_kgh = system_result.flujo_masico_h2_prod_kg_h
    n_h2o_in = system_result.flujo_molar_h2o_in_mol_s  # mol/s

    # 1. Calor en el stack (V_c - V_tn) * I
    calor_stack_kw = (v_c - v_tn) * i_total / 1000.0
    calor_stack_mw = calor_stack_kw / 1000.0

    if abs(v_c - v_tn) < 0.005:
        regimen = 'Termoneutro'
    elif v_c > v_tn:
        regimen = 'Exotermico'
    else:
        regimen = 'Endotermico'

    # 2. Entalpías de agua y vapor a 20 bar:
    # Agua líquida a 25 °C, 20 bar: h ~ 105 kJ/kg = 1.89 kJ/mol
    # Vapor saturado a 220 °C, 20 bar: h ~ 2799 kJ/kg = 50.42 kJ/mol
    # Delta h_evap + precal = 2799 - 105 = 2694 kJ/kg = 48.53 kJ/mol
    delta_h_caldera = 48530.0  # J/mol agua
    calor_caldera_kw = (n_h2o_in * delta_h_caldera) / 1000.0

    # Vapor a 20 bar de 220 °C a 750 °C:
    # Cp promedio de vapor ~ 38.0 J/(mol*K)
    delta_t_sobrecal = 750.0 - 220.0  # 530 K
    cp_steam_avg = 38.5  # J/(mol*K)
    calor_sobrecal_kw = (n_h2o_in * cp_steam_avg * delta_t_sobrecal) / 1000.0

    # 3. Calor recuperable del efluente catódico (H2 + vapor a 750 °C -> 38 °C):
    n_h2_out = system_result.flujo_molar_h2_prod_mol_s + system_result.flujo_molar_h2_in_mol_s
    n_h2o_residual = system_result.flujo_molar_h2o_in_mol_s * (1.0 - system_result.conversion_vapor)
    delta_t_cool = 750.0 - 38.0  # 712 K
    cp_h2_avg = 29.5  # J/(mol*K)
    # Calor sensible gas catódico:
    q_cat_cool_sensible = (n_h2_out * cp_h2_avg + n_h2o_residual * cp_steam_avg) * delta_t_cool / 1000.0
    # Calor latente condensación de vapor residual a 38 °C (h_vap ~ 2410 kJ/kg = 43.4 kJ/mol):
    q_cat_condensacion = (n_h2o_residual * 43400.0) / 1000.0
    calor_recup_catodico_total_kw = q_cat_cool_sensible + q_cat_condensacion

    # 4. Calor recuperable anódico (O2 puro a 750 °C -> 31 °C):
    n_o2_out = system_result.flujo_molar_o2_prod_mol_s
    cp_o2_avg = 32.0  # J/(mol*K)
    calor_recup_anodico_kw = (n_o2_out * cp_o2_avg * (750.0 - 31.0)) / 1000.0

    # 5. Integración por escenarios:
    # Escenario A: Todo externo
    # Se debe suministrar caldera + sobrecalentador externamente
    q_ext_a = calor_caldera_kw + calor_sobrecal_kw
    if regimen == 'Endotermico':
        q_ext_a += abs(calor_stack_kw)

    # Escenario B: Recuperación de R-401 (caldera suministrada por calor de reacción)
    # R-401 provee calor a caldera (limitado por min(calor_r401, calor_caldera))
    ahorro_r401_b = min(calor_r401_disponible_kw, calor_caldera_kw)
    q_ext_b = (calor_caldera_kw - ahorro_r401_b) + calor_sobrecal_kw
    if regimen == 'Endotermico':
        q_ext_b += abs(calor_stack_kw)

    # Escenario C: Integración Total (R-401 caldera + FEHE gas-gas para sobrecalentamiento)
    # Efluente catódico y anódico precalientan el vapor saturado de 220°C a ~650-700°C en FEHE
    calor_util_alta_temp = (n_h2_out * cp_h2_avg + n_h2o_residual * cp_steam_avg + n_o2_out * cp_o2_avg) * (750.0 - 250.0) / 1000.0
    ahorro_fehe_c = min(calor_sobrecal_kw * eficiencia_fehe, calor_util_alta_temp * eficiencia_fehe)
    calor_sobrecal_residual_c = max(calor_sobrecal_kw - ahorro_fehe_c, 0.0)
    q_ext_c = (calor_caldera_kw - ahorro_r401_b) + calor_sobrecal_residual_c
    if regimen == 'Endotermico':
        q_ext_c += abs(calor_stack_kw)

    # Métricas específicas
    sec_elec = system_result.sec_ac_kwh_kg_h2
    # Equivalente térmico: utilizando factor de sustitución de energía primaria o ciclo Rankine inverso (COP ~ 1.0 para vapor alta temperatura)
    sec_termico_eq_c = q_ext_c / max(m_h2_kgh, 1e-6)
    sec_total_c = sec_elec + sec_termico_eq_c

    return ThermalIntegrationResult(
        v_celda=v_c,
        v_termoneutro=v_tn,
        e_nernst=e_nernst,
        regimen_celda=regimen,
        calor_reaccion_celda_kw=calor_stack_kw,
        calor_reaccion_celda_mw=calor_stack_mw,
        calor_generacion_vapor_20bar_kw=calor_caldera_kw,
        calor_sobrecalentamiento_750c_kw=calor_sobrecal_kw,
        calor_recuperable_efluente_catodico_kw=calor_recup_catodico_total_kw,
        calor_recuperable_efluente_anodico_kw=calor_recup_anodico_kw,
        calor_disponible_r401_kw=calor_r401_disponible_kw,
        ahorro_caldera_r401_kw=ahorro_r401_b,
        ahorro_fehe_recuperador_kw=ahorro_fehe_c,
        escenario_a_demanda_termica_neta_kw=q_ext_a,
        escenario_b_demanda_termica_neta_kw=q_ext_b,
        escenario_c_demanda_termica_neta_kw=q_ext_c,
        sec_electrico_ac_kwh_kg=sec_elec,
        sec_termico_equivalente_kwh_kg=sec_termico_eq_c,
        sec_energetico_total_kwh_kg=sec_total_c,
        detalles={
            'calor_util_alta_temp_kw': calor_util_alta_temp,
            'calor_sobrecal_residual_c_kw': calor_sobrecal_residual_c
        }
    )

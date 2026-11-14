"""
Módulo de Termodinámica para Electrólisis de Vapor a Alta Temperatura (SOEC).

Reacción fundamental:
    H2O(g) -> H2(g) + 0.5 O2(g)

Incluye:
1. Modelo lineal original (literatura simplificada: Ni et al., 2007).
2. Modelo riguroso NIST Shomate (temperatura dependiente de Cp, entalpía y entropía).
3. Comparación y auditoría termodinámica.
"""

import math
import numpy as np

# Constantes físicas fundamentales (CODATA 2018 / IUPAC)
R_GAS = 8.314462618        # J/(mol*K)
FARADAY = 96485.33212      # C/mol (A*s/mol)
P_STD = 100000.0           # Pa (1.0 bar standard state IUPAC)
M_H2 = 0.00201588          # kg/mol
M_H2O = 0.01801528         # kg/mol
M_O2 = 0.0319988           # kg/mol

# Coeficientes Shomate de NIST WebBook
# Cp = A + B*t + C*t^2 + D*t^3 + E/t^2 (J/(mol*K)), con t = T/1000
# H° - H°_298.15 = A*t + B*t^2/2 + C*t^3/3 + D*t^4/4 - E/t + F - H298 (kJ/mol)
# S° = A*ln(t) + B*t + C*t^2/2 + D*t^3/3 - E/(2*t^2) + G (J/(mol*K))

SHOMATE_H2_HT = {
    'A': 18.563083, 'B': 12.257357, 'C': -2.859797, 'D': 0.268238,
    'E': 1.977990, 'F': -1.147424, 'G': 156.288190, 'H': 0.0
}
SHOMATE_H2_LT = {
    'A': 33.066178, 'B': -11.363417, 'C': 11.432816, 'D': -2.772874,
    'E': -0.158558, 'F': -9.980797, 'G': 172.707974, 'H': 0.0
}

SHOMATE_O2 = {
    'A': 30.11160, 'B': 10.92984, 'C': -4.207770, 'D': 0.648589,
    'E': -0.198275, 'F': -11.81220, 'G': 243.9850, 'H': 0.0
}

SHOMATE_H2O_GAS = {
    'A': 30.09200, 'B': 6.832514, 'C': 6.793435, 'D': -2.534480,
    'E': 0.082139, 'F': -250.8810, 'G': 223.3967, 'H': -241.8264
}


def calcular_termodinamica_original(temperatura_k: float):
    """
    Modelo termodinámico original implementado en el script DWSIM.
    Aproximación lineal común en literatura SOEC:
        delta_g0 = 246543 - 54.08 * T  [J/mol]
        delta_h0 = 248000.0             [J/mol]
    """
    delta_g0 = 246543.0 - 54.08 * temperatura_k
    delta_h0 = 248000.0
    delta_s0 = (delta_h0 - delta_g0) / temperatura_k
    e_rev_std = delta_g0 / (2.0 * FARADAY)
    v_termoneutro = delta_h0 / (2.0 * FARADAY)
    return {
        'delta_g0': delta_g0,
        'delta_h0': delta_h0,
        'delta_s0': delta_s0,
        'e_rev_std': e_rev_std,
        'v_termoneutro': v_termoneutro,
        'modelo': 'Original_Lineal'
    }


def calcular_termodinamica_nist(temperatura_k: float):
    """
    Modelo termodinámico riguroso basado en polinomios de Shomate de NIST.
    Calcula Delta H°, Delta S°, Delta G°, E_rev° y V_tn en función de la temperatura.
    Válido de 500 K a 1700 K.
    """
    t = temperatura_k / 1000.0

    # H2 (gas)
    if temperatura_k < 1000.0:
        c = SHOMATE_H2_LT
    else:
        c = SHOMATE_H2_HT
    h_h2 = (c['A']*t + c['B']*t**2/2.0 + c['C']*t**3/3.0 + c['D']*t**4/4.0 - c['E']/t + c['F'])  # kJ/mol
    s_h2 = (c['A']*math.log(t) + c['B']*t + c['C']*t**2/2.0 + c['D']*t**3/3.0 - c['E']/(2.0*t**2) + c['G'])  # J/(mol*K)

    # O2 (gas)
    c = SHOMATE_O2
    h_o2 = (c['A']*t + c['B']*t**2/2.0 + c['C']*t**3/3.0 + c['D']*t**4/4.0 - c['E']/t + c['F'])  # kJ/mol
    s_o2 = (c['A']*math.log(t) + c['B']*t + c['C']*t**2/2.0 + c['D']*t**3/3.0 - c['E']/(2.0*t**2) + c['G'])  # J/(mol*K)

    # H2O (gas)
    c = SHOMATE_H2O_GAS
    h_h2o = (c['A']*t + c['B']*t**2/2.0 + c['C']*t**3/3.0 + c['D']*t**4/4.0 - c['E']/t + c['F'])  # kJ/mol
    s_h2o = (c['A']*math.log(t) + c['B']*t + c['C']*t**2/2.0 + c['D']*t**3/3.0 - c['E']/(2.0*t**2) + c['G'])  # J/(mol*K)

    # Reacción: H2O -> H2 + 0.5 O2
    delta_h0 = (h_h2 + 0.5 * h_o2 - h_h2o) * 1000.0     # J/mol
    delta_s0 = (s_h2 + 0.5 * s_o2 - s_h2o)              # J/(mol*K)
    delta_g0 = delta_h0 - temperatura_k * delta_s0       # J/mol

    e_rev_std = delta_g0 / (2.0 * FARADAY)              # V
    v_termoneutro = delta_h0 / (2.0 * FARADAY)          # V

    return {
        'delta_g0': delta_g0,
        'delta_h0': delta_h0,
        'delta_s0': delta_s0,
        'e_rev_std': e_rev_std,
        'v_termoneutro': v_termoneutro,
        'modelo': 'NIST_Riguroso'
    }


def calcular_termodinamica(temperatura_k: float, use_rigorous: bool = True):
    """
    Función unificada para selección de modelo termodinámico.
    """
    if use_rigorous:
        return calcular_termodinamica_nist(temperatura_k)
    else:
        return calcular_termodinamica_original(temperatura_k)


def auditar_termodinamica(temperaturas_c=None):
    """
    Genera tabla comparativa y métricas de error entre el modelo original y NIST.
    """
    if temperaturas_c is None:
        temperaturas_c = [700, 725, 750, 775, 800, 825, 850]

    registros = []
    for tc in temperaturas_c:
        tk = tc + 273.15
        orig = calcular_termodinamica_original(tk)
        nist = calcular_termodinamica_nist(tk)

        err_dg = (orig['delta_g0'] - nist['delta_g0']) / nist['delta_g0'] * 100.0
        err_dh = (orig['delta_h0'] - nist['delta_h0']) / nist['delta_h0'] * 100.0
        err_erev = (orig['e_rev_std'] - nist['e_rev_std']) / nist['e_rev_std'] * 100.0
        err_vtn = (orig['v_termoneutro'] - nist['v_termoneutro']) / nist['v_termoneutro'] * 100.0

        registros.append({
            'T_C': tc,
            'T_K': tk,
            'dG_original_J_mol': orig['delta_g0'],
            'dG_nist_J_mol': nist['delta_g0'],
            'dG_error_pct': err_dg,
            'dH_original_J_mol': orig['delta_h0'],
            'dH_nist_J_mol': nist['delta_h0'],
            'dH_error_pct': err_dh,
            'dS_original_J_mol_K': orig['delta_s0'],
            'dS_nist_J_mol_K': nist['delta_s0'],
            'E_rev_original_V': orig['e_rev_std'],
            'E_rev_nist_V': nist['e_rev_std'],
            'E_rev_error_mV': (orig['e_rev_std'] - nist['e_rev_std']) * 1000.0,
            'V_tn_original_V': orig['v_termoneutro'],
            'V_tn_nist_V': nist['v_termoneutro'],
            'V_tn_error_mV': (orig['v_termoneutro'] - nist['v_termoneutro']) * 1000.0
        })
    return registros

"""
Módulo de Pérdidas Óhmicas para SOEC.

Calcula la resistencia de área específica (ASR) y la caída óhmica de voltaje:
    eta_ohm = j * ASR(T)
Donde ASR sigue una ley de tipo Arrhenius para la conductividad iónica del
electrolito de óxido de circonio estabilizado con itria (YSZ) y las resistencias
de contacto e interconector.
"""

import math
from .thermodynamics import R_GAS

# Parámetros de referencia por defecto
T_REF_DEF = 1023.15      # K (750 °C)
ASR_REF_DEF = 2.20e-5    # Ohm*m² (0.22 Ohm*cm²)
E_OHM_DEF = 90000.0      # J/mol (90 kJ/mol, energía de activación para O2- en YSZ)


def calcular_asr(temperatura_k: float,
                 asr_ref: float = ASR_REF_DEF,
                 e_ohm: float = E_OHM_DEF,
                 t_ref: float = T_REF_DEF,
                 resistencia_contacto: float = 0.0):
    """
    Calcula la resistencia de área específica (ASR) en Ohm*m² y Ohm*cm².

    Parámetros:
    -----------
    temperatura_k : float
        Temperatura de la celda [K]
    asr_ref : float
        ASR a la temperatura de referencia [Ohm*m²]
    e_ohm : float
        Energía de activación de conducción iónica [J/mol]
    t_ref : float
        Temperatura de referencia [K]
    resistencia_contacto : float
        Resistencia adicional de interconectores y contactos [Ohm*m²]

    Retorna:
    --------
    dict con asr_ohm_m2, asr_ohm_cm2
    """
    factor_ohm = (e_ohm / R_GAS) * (1.0 / temperatura_k - 1.0 / t_ref)
    asr_termica = asr_ref * math.exp(factor_ohm)
    asr_total = asr_termica + resistencia_contacto
    asr_cm2 = asr_total * 10000.0  # 1 m² = 10,000 cm² -> 1 Ohm*m² = 10,000 Ohm*cm²

    return {
        'asr_ohm_m2': asr_total,
        'asr_ohm_cm2': asr_cm2
    }


def calcular_perdidas_ohmicas(j: float, temperatura_k: float,
                             asr_ref: float = ASR_REF_DEF,
                             e_ohm: float = E_OHM_DEF,
                             t_ref: float = T_REF_DEF,
                             resistencia_contacto: float = 0.0):
    """
    Calcula la pérdida óhmica de voltaje: eta_ohm = j * ASR(T)

    Parámetros:
    -----------
    j : float
        Densidad de corriente [A/m²]
    temperatura_k : float
        Temperatura de celda [K]

    Retorna:
    --------
    dict con eta_ohm [V], asr_ohm_m2, asr_ohm_cm2
    """
    asr_dict = calcular_asr(temperatura_k, asr_ref, e_ohm, t_ref, resistencia_contacto)
    eta_ohm = j * asr_dict['asr_ohm_m2']

    return {
        'eta_ohm': eta_ohm,
        'asr_ohm_m2': asr_dict['asr_ohm_m2'],
        'asr_ohm_cm2': asr_dict['asr_ohm_cm2']
    }

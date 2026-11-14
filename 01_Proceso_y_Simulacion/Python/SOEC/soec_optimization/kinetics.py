"""
Módulo de Cinética Electroquímica (Pérdidas por Activación) para SOEC.

Calcula el sobrepotencial de activación en ánodo y cátodo utilizando
el formalismo de Butler-Volmer invertido analíticamente mediante la
función arsinh (válido para coeficiente de transferencia simétrico alpha = 0.5):
    eta_act = (R * T / (alpha * F)) * arsinh( j / (2 * j0) )
"""

import math
from .thermodynamics import R_GAS, FARADAY

# Parámetros cinéticos de referencia por defecto (literatura Ni-YSZ / LSCF)
T_REF_DEF = 1023.15      # K (750 °C)
ALPHA_DEF = 0.50         # Coeficiente de transferencia de carga
J0_C_REF_DEF = 5300.0    # A/m² (0.53 A/cm²) densidad de intercambio cátodo
J0_A_REF_DEF = 3500.0    # A/m² (0.35 A/cm²) densidad de intercambio ánodo
E_ACT_C_DEF = 100000.0   # J/mol (100 kJ/mol) energía activación cátodo
E_ACT_A_DEF = 120000.0   # J/mol (120 kJ/mol) energía activación ánodo


def calcular_cinetica_activacion(j: float, temperatura_k: float,
                                 j0_c_ref: float = J0_C_REF_DEF,
                                 j0_a_ref: float = J0_A_REF_DEF,
                                 e_act_c: float = E_ACT_C_DEF,
                                 e_act_a: float = E_ACT_A_DEF,
                                 alpha: float = ALPHA_DEF,
                                 t_ref: float = T_REF_DEF,
                                 y_h2o: float = None,
                                 y_h2: float = None,
                                 y_o2: float = None):
    """
    Calcula los sobrepotenciales de activación catódico, anódico y total.

    Parámetros:
    -----------
    j : float
        Densidad de corriente de operación [A/m²]
    temperatura_k : float
        Temperatura de celda [K]
    j0_c_ref, j0_a_ref : float
        Densidades de corriente de intercambio a t_ref [A/m²]
    e_act_c, e_act_a : float
        Energías de activación [J/mol]
    alpha : float
        Coeficiente de transferencia aparente (default 0.5)
    t_ref : float
        Temperatura de referencia [K]
    y_h2o, y_h2, y_o2 : float, optional
        Fracciones molares locales para corrección composicional de j0.

    Retorna:
    --------
    dict con eta_act_c, eta_act_a, eta_act_total, j0_c, j0_a [V]
    """
    if j <= 0.0:
        return {
            'eta_act_c': 0.0,
            'eta_act_a': 0.0,
            'eta_act_total': 0.0,
            'j0_c': j0_c_ref,
            'j0_a': j0_a_ref
        }

    # Dependencia térmica de tipo Arrhenius
    factor_c = (e_act_c / R_GAS) * (1.0 / temperatura_k - 1.0 / t_ref)
    factor_a = (e_act_a / R_GAS) * (1.0 / temperatura_k - 1.0 / t_ref)

    j0_c = j0_c_ref * math.exp(-factor_c)
    j0_a = j0_a_ref * math.exp(-factor_a)

    # Corrección composicional opcional si se proporcionan fracciones molares
    if y_h2o is not None and y_h2 is not None:
        # j0_c proporcional a (y_H2O)^gamma_1 * (y_H2)^gamma_2
        # Típicamente gamma_1 ~ 0.3-0.4, gamma_2 ~ 0.2-0.3 en cátodo Ni-YSZ
        gamma_h2o = 0.35
        gamma_h2 = 0.25
        y_ref = 0.50
        corr_c = ((max(y_h2o, 1e-4) / y_ref) ** gamma_h2o) * ((max(y_h2, 1e-4) / y_ref) ** gamma_h2)
        j0_c *= max(corr_c, 0.1)

    if y_o2 is not None:
        # j0_a proporcional a (y_O2)^0.25 en ánodo LSCF
        gamma_o2 = 0.25
        corr_a = (max(y_o2, 1e-4) / 1.0) ** gamma_o2
        j0_a *= max(corr_a, 0.1)

    potencial_termico = R_GAS * temperatura_k / (alpha * FARADAY)

    # Butler-Volmer invertido
    eta_act_c = potencial_termico * math.asinh(j / (2.0 * j0_c))
    eta_act_a = potencial_termico * math.asinh(j / (2.0 * j0_a))
    eta_act_total = eta_act_c + eta_act_a

    return {
        'eta_act_c': eta_act_c,
        'eta_act_a': eta_act_a,
        'eta_act_total': eta_act_total,
        'j0_c': j0_c,
        'j0_a': j0_a
    }

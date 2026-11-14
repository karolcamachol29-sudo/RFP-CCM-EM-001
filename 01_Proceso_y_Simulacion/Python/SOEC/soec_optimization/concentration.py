"""
Módulo de Polarización por Concentración y Corriente Límite para SOEC.

Calcula el sobrepotencial por difusión en electrodos porosos y evalúa
estrictamente la factibilidad física del punto de operación:
    eta_conc = - (R * T / (2 * F)) * ln( 1 - j / j_limit )

CRÍTICO:
Si j >= j_limit (o ratio >= 1.0), el punto de operación NO es físicamente realizable
debido a inanición de reactivo (difusión insuficiente de vapor en los poros del cátodo).
El modelo reporta `es_factible = False` y sobrepotencial infinito o NaN, en lugar de
recortar numéricamente con min(ratio, 0.999) como hacía el código original.
"""

import math
from .thermodynamics import R_GAS, FARADAY

# Parámetros de referencia por defecto
T_REF_DEF = 1023.15       # K (750 °C)
P_REF_DEF = 2000000.0     # Pa (20 bar)
J_LIMIT_REF_DEF = 25000.0 # A/m² (2.50 A/cm²) a condiciones de referencia
Y_H2O_REF_DEF = 0.585     # Composición media representativa del caso base


def calcular_j_limit(temperatura_k: float,
                     presion_pa: float,
                     y_h2o_medio: float,
                     j_limit_ref: float = J_LIMIT_REF_DEF,
                     t_ref: float = T_REF_DEF,
                     p_ref: float = P_REF_DEF,
                     y_h2o_ref: float = Y_H2O_REF_DEF,
                     dependencia_fisica: bool = True):
    """
    Calcula la densidad de corriente límite difusiva j_limit [A/m²].

    En medios porosos:
        j_limit = (2 * F * D_eff * P * y_H2O) / (R * T * delta)
    Donde el coeficiente de difusión binario gas-gas varía como:
        D_eff propto T^1.75 / P
    Por tanto, el producto (D_eff * P) varía como T^1.75, y dividiendo por T:
        j_limit propto T^0.75 * y_H2O
    """
    if not dependencia_fisica:
        return j_limit_ref

    y_safe = max(y_h2o_medio, 1e-4)
    # Factor térmico (T / T_ref)^0.75
    factor_t = (temperatura_k / t_ref) ** 0.75
    # Factor de composición catódica (y_H2O / y_H2O_ref)
    factor_y = y_safe / y_h2o_ref

    j_limit = j_limit_ref * factor_t * factor_y
    return max(j_limit, 100.0)


def calcular_perdidas_concentracion(j: float,
                                    temperatura_k: float,
                                    presion_pa: float = P_REF_DEF,
                                    y_h2o_medio: float = Y_H2O_REF_DEF,
                                    j_limit_ref: float = J_LIMIT_REF_DEF,
                                    t_ref: float = T_REF_DEF,
                                    modo_estricto: bool = True,
                                    dependencia_fisica: bool = True):
    """
    Calcula las pérdidas por concentración y dictamina factibilidad física.

    Parámetros:
    -----------
    j : float
        Densidad de corriente [A/m²]
    temperatura_k : float
        Temperatura de la celda [K]
    presion_pa : float
        Presión [Pa]
    y_h2o_medio : float
        Fracción molar media de vapor en el canal catódico
    j_limit_ref : float
        Densidad límite de referencia [A/m²]
    modo_estricto : bool
        Si True, cuando j >= j_limit declara es_factible = False.
        Si False, emula el recorte original del código con min(ratio, 0.999).

    Retorna:
    --------
    dict con eta_conc [V], j_limit [A/m²], ratio, es_factible [bool], motivo_infaustibilidad
    """
    j_limit = calcular_j_limit(temperatura_k, presion_pa, y_h2o_medio,
                               j_limit_ref, t_ref, dependencia_fisica=dependencia_fisica)

    if j <= 0.0:
        return {
            'eta_conc': 0.0,
            'j_limit': j_limit,
            'ratio': 0.0,
            'es_factible': True,
            'motivo': 'OK'
        }

    ratio = j / j_limit

    if modo_estricto:
        # En modo físico riguroso: un ratio >= 0.99 implica bloqueo de transporte de masa
        if ratio >= 0.999:
            return {
                'eta_conc': float('inf'),
                'j_limit': j_limit,
                'ratio': ratio,
                'es_factible': False,
                'motivo': f'Densidad de corriente j ({j:.1f} A/m²) excede el límite difusivo j_limit ({j_limit:.1f} A/m²)'
            }
        else:
            eta_conc = -(R_GAS * temperatura_k / (2.0 * FARADAY)) * math.log(1.0 - ratio)
            return {
                'eta_conc': eta_conc,
                'j_limit': j_limit,
                'ratio': ratio,
                'es_factible': True,
                'motivo': 'OK'
            }
    else:
        # Modo réplica del código original (para comprobación de caso base)
        ratio_clipped = min(max(ratio, 0.0), 0.999)
        eta_conc = -(R_GAS * temperatura_k / (2.0 * FARADAY)) * math.log(1.0 - ratio_clipped)
        return {
            'eta_conc': eta_conc,
            'j_limit': j_limit,
            'ratio': ratio,
            'es_factible': ratio < 1.0,
            'motivo': 'Modo legado con recorte' if ratio >= 0.999 else 'OK'
        }

"""
Módulo de Ecuación de Nernst para SOEC.

Calcula el potencial reversible local y medio considerando:
- Composición catódica (H2O, H2)
- Composición anódica (O2 puro o mezcla con gas de arrastre)
- Presiones independientes catódica y anódica
- Perfil de conversión a lo largo del canal
"""

import math
import numpy as np
from scipy.integrate import quad
from .thermodynamics import R_GAS, FARADAY, P_STD


def calcular_nernst(e_rev_std: float, temperatura_k: float, presion_pa: float,
                    y_h2o: float, y_h2: float, y_o2: float = 1.0,
                    presion_anodo_pa: float = None):
    """
    Calcula el potencial de Nernst para una composición y estado de presión dados.

    Parámetros:
    -----------
    e_rev_std : float
        Potencial estándar reversible [V]
    temperatura_k : float
        Temperatura absoluta [K]
    presion_pa : float
        Presión total catódica [Pa]
    y_h2o : float
        Fracción molar de vapor de agua
    y_h2 : float
        Fracción molar de hidrógeno
    y_o2 : float
        Fracción molar de oxígeno en ánodo (default 1.0 para evolución pura)
    presion_anodo_pa : float, optional
        Presión total anódica [Pa]. Si es None, se asume igual a presion_pa.

    Retorna:
    --------
    e_nernst : float [V]
    """
    if presion_anodo_pa is None:
        presion_anodo_pa = presion_pa

    y_h2o_safe = max(y_h2o, 1.0e-6)
    y_h2_safe = max(y_h2, 1.0e-6)
    y_o2_safe = max(y_o2, 1.0e-6)

    # Ratio anódico P_O2 / P_std
    p_o2_ratio = (y_o2_safe * presion_anodo_pa) / P_STD

    # Término catódico: P_H2 / P_H2O = (y_H2 * P_cat) / (y_H2O * P_cat) = y_H2 / y_H2O
    termino_composicion = math.log((y_h2_safe * math.sqrt(y_o2_safe)) / y_h2o_safe)

    # Término de presión anódica efectiva: 0.5 * ln(P_ano / P_std)
    # Si P_ano = P_cat = P, esto es 0.5 * ln(P/P_std)
    termino_presion = 0.5 * math.log(presion_anodo_pa / P_STD)

    e_nernst = e_rev_std + (R_GAS * temperatura_k / (2.0 * FARADAY)) * (termino_composicion + termino_presion)
    return e_nernst


def calcular_nernst_perfil(e_rev_std: float, temperatura_k: float, presion_pa: float,
                           fraccion_h2o_in: float, fraccion_h2_in: float,
                           conversion_vapor: float, y_o2: float = 1.0,
                           presion_anodo_pa: float = None, n_puntos: int = 50):
    """
    Calcula el perfil de Nernst a lo largo del canal y el promedio integrado riguroso.

    Parámetros:
    -----------
    fraccion_h2o_in : float
        Fracción molar de vapor a la entrada del cátodo
    fraccion_h2_in : float
        Fracción molar de H2 a la entrada del cátodo
    conversion_vapor : float
        Conversión de vapor objetivo (ej. 0.70)
    """
    if presion_anodo_pa is None:
        presion_anodo_pa = presion_pa

    xi_vals = np.linspace(0.0, conversion_vapor, n_puntos)
    nernst_vals = []
    yh2o_vals = []
    yh2_vals = []

    # En base de 1 mol de alimentación catódica total:
    # Moles de H2O(xi) = y_h2o_in * (1 - xi)
    # Moles de H2(xi) = y_h2_in + y_h2o_in * xi
    # Total moles catódicos = y_h2o_in + y_h2_in = const (asumiendo mezcla binaria H2O-H2)
    mol_total_cat = fraccion_h2o_in + fraccion_h2_in

    for xi in xi_vals:
        mol_h2o = fraccion_h2o_in * (1.0 - xi)
        mol_h2 = fraccion_h2_in + fraccion_h2o_in * xi
        yh2o = mol_h2o / mol_total_cat
        yh2 = mol_h2 / mol_total_cat
        e_n = calcular_nernst(e_rev_std, temperatura_k, presion_pa, yh2o, yh2, y_o2, presion_anodo_pa)
        nernst_vals.append(e_n)
        yh2o_vals.append(yh2o)
        yh2_vals.append(yh2)

    # Integración numérica por regla del trapecio
    nernst_integrado = np.trapz(nernst_vals, xi_vals) / conversion_vapor

    # Promedio lineal tradicional (del código original)
    y_h2o_medio_orig = max(fraccion_h2o_in * (1.0 - 0.5 * conversion_vapor), 1.0e-3)
    y_h2_medio_orig = max(fraccion_h2_in + 0.5 * fraccion_h2o_in * conversion_vapor, 1.0e-3)
    nernst_lineal_orig = calcular_nernst(e_rev_std, temperatura_k, presion_pa,
                                         y_h2o_medio_orig, y_h2_medio_orig, y_o2, presion_anodo_pa)

    # Promedio logarítmico de fracciones
    yh2o_in = fraccion_h2o_in
    yh2_in = max(fraccion_h2_in, 1e-4)
    yh2o_out = max(fraccion_h2o_in * (1.0 - conversion_vapor), 1e-4)
    yh2_out = fraccion_h2_in + fraccion_h2o_in * conversion_vapor

    ratio_in = yh2_in / yh2o_in
    ratio_out = yh2_out / yh2o_out
    log_mean_ratio = (ratio_out - ratio_in) / math.log(ratio_out / ratio_in)

    return {
        'nernst_inlet': nernst_vals[0],
        'nernst_outlet': nernst_vals[-1],
        'nernst_integrado': nernst_integrado,
        'nernst_lineal_orig': nernst_lineal_orig,
        'diferencia_mV': (nernst_lineal_orig - nernst_integrado) * 1000.0,
        'xi_perfil': xi_vals,
        'nernst_perfil': nernst_vals,
        'yh2o_perfil': yh2o_vals,
        'yh2_perfil': yh2_vals
    }

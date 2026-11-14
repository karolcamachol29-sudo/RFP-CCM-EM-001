"""
SOEC Optimization and Audit Package
Multidisciplinary engineering tool for Solid Oxide Electrolyzer Cell modeling,
auditing, sensitivity analysis, sizing, and techno-economic optimization.
"""

from .thermodynamics import (
    R_GAS, FARADAY, P_STD, M_H2, M_H2O, M_O2,
    calcular_termodinamica_original,
    calcular_termodinamica_nist,
    calcular_termodinamica
)
from .nernst import calcular_nernst, calcular_nernst_perfil
from .kinetics import calcular_cinetica_activacion
from .ohmic import calcular_perdidas_ohmicas, calcular_asr
from .concentration import calcular_perdidas_concentracion, calcular_j_limit
from .soec_cell import SOECCell, SOECCellResult
from .stack_module_sizing import SOECSystem, SOECSystemResult

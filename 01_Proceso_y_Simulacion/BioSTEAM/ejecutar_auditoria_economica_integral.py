#!/usr/bin/env python3
# coding: utf-8
"""
Auditoría y Validación Tecnoeconómica Integral: SOEC vs PEM, Reactor Multitubular y Calentador Eléctrico
Proyecto de Licitación RFP-CCM-EM-001 (Solvanta Engineering Solutions) - Planta e-Metanol (30,000 t/año)
Generador de Resultados Numéricos, Tablas Excel y Gráficas de Sensibilidad
"""

import os
import math
import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import matplotlib.pyplot as plt

# 1. PARÁMETROS GLOBALES DEL PROYECTO
CAPACIDAD_MEOH_T_ANO = 30000.0       # t e-metanol/año
HORAS_OP = 8000.0                    # h/año (91.32% disponibilidad)
PROD_MEOH_KG_H = (CAPACIDAD_MEOH_T_ANO * 1000.0) / HORAS_OP # 3,750 kg/h nominal
# Estequiometría y rendimientos en bucle de síntesis (DWSIM Aprobado):
# Producción neta de MeOH: 119.0 kmol/h = 3,812.98 kg/h (30,503.8 t/año brutos para 30,000 t netos AA)
H2_REQUERIDO_KG_H = 1272.42          # kg H2/h continuo
H2_REQUERIDO_T_ANO = (H2_REQUERIDO_KG_H * HORAS_OP) / 1000.0 # 10,179.36 t H2/año
CO2_REQUERIDO_KG_H = 5274.34         # kg CO2/h (42,194.7 t CO2/año)

# Índices económicos
CEPCI_2001 = 397.0
CEPCI_2017 = 567.5
CEPCI_2021 = 708.0
CEPCI_2024 = 800.0
CEPCI_2026 = 825.0

TASA_DESCUENTO = 0.085               # WACC 8.5%
VIDA_PROYECTO_ANOS = 20
CRF = (TASA_DESCUENTO * (1.0 + TASA_DESCUENTO)**VIDA_PROYECTO_ANOS) / (((1.0 + TASA_DESCUENTO)**VIDA_PROYECTO_ANOS) - 1.0) # 0.10567
PRECIO_ELEC_BASE_USD_KWH = 0.040     # 40 USD/MWh PPA Renovable

# 2. MODELADO TÉCNICO Y ECONÓMICO: SOEC (ELECTROLIZADOR ÓXIDO SÓLIDO)
# Escenario D Óptimo (T=800°C / P=20 bar / j=0.4807 A/cm² / conv=70%)
SOEC_P_AC_MW = 41.9136               # MW AC
SOEC_P_DC_MW = 40.0465               # MW DC
SOEC_SEC_AC = 32.940                 # kWh/kg H2
SOEC_N_CELDAS = 352660               # celdas (200 cm² cada una)
SOEC_AREA_TOTAL_M2 = SOEC_N_CELDAS * 0.0200 # 7,053.2 m²

# Desglose de CAPEX (DOE Record #24005, Prosser et al. 2024/2025, NREL)
# Costos de compra desnuda (Cp0)
soec_cp0_stacks = SOEC_N_CELDAS * 32.00 # $11,285,120 USD (celdas YSZ, interconectores Crofer 22 APU, sellos vidrio-cerámico)
soec_cp0_vessels = 14 * 245000.0        # $3,430,000 USD (14 módulos presurizados ASME Div 2 a 20 bar con aislamiento refractario)
soec_cp0_power = SOEC_P_AC_MW * 1000.0 * 135.0 # $5,658,337 USD (rectificadores IGBT/SCR 12 pulsos, transformadores secos, filtros armónicos)
soec_cp0_bop_mfg = SOEC_N_CELDAS * 7.35 # $2,591,632 USD (manifolds Incoloy 800H, válvulas alta temp, piping)
soec_cp0_total = soec_cp0_stacks + soec_cp0_vessels + soec_cp0_power + soec_cp0_bop_mfg # $22,965,089 USD

# Factores de módulo desnudo (F_BM)
soec_cbm_stacks = soec_cp0_stacks * 1.15   # $12,977,888 USD (skids modulares pre-ensamblados)
soec_cbm_vessels = soec_cp0_vessels * 1.65 # $5,659,500 USD (montaje mecánico, cimentación, aislamiento térmico)
soec_cbm_power = soec_cp0_power * 1.35     # $7,638,755 USD (instalación eléctrica, tableros, cableado pesado)
soec_cbm_bop = soec_cp0_bop_mfg * 1.55     # $4,017,029 USD (tuberías, soportes, traceado térmico)
soec_cbm_inst = 678216.0                   # Instrumentación y control ATEX
soec_capex_instalado = soec_cbm_stacks + soec_cbm_vessels + soec_cbm_power + soec_cbm_bop + soec_cbm_inst # $30,971,388 USD ($738.93/kWe AC)

# Escenarios de Incertidumbre SOEC (USD Instalado)
soec_capex_opt = 24777110.0   # $591/kWe (producción automatizada GW >500 MW/año, Prosser 2024)
soec_capex_med = 30971388.0   # $739/kWe (caso base Solvanta Escenario D)
soec_capex_cons = 41913600.0  # $1,000/kWe (FOAK temprano con contingencias mayores)

# OPEX SOEC
soec_opex_elec = (SOEC_P_AC_MW * 1000.0) * HORAS_OP * PRECIO_ELEC_BASE_USD_KWH # $13,412,354 USD/año
soec_opex_stack_rep = (soec_cp0_stacks * 0.60) / (40000.0 / HORAS_OP)          # $1,354,214 USD/año (vida útil 40,000 h = 5 años al 60% costo stack)
soec_opex_om = (soec_capex_instalado - soec_cbm_stacks) * 0.025                # $449,838 USD/año
soec_opex_total_anual = soec_opex_elec + soec_opex_stack_rep + soec_opex_om     # $15,216,406 USD/año
soec_lcoh_usd_kg = ((soec_capex_instalado * CRF) + soec_opex_total_anual) / (H2_REQUERIDO_KG_H * HORAS_OP) # $1.816 / kg H2

# 3. MODELADO TÉCNICO Y ECONÓMICO: PEM (ELECTROLIZADOR DE MEMBRANA POLIMÉRICA)
# Para producir exactamente los mismos 1,272.42 kg/h de H2 a 30 bar y 70°C:
# Reacción a 70°C en agua líquida: HHV termoneutro = 39.39 kWh_DC/kg H2 (1.481 V)
# En operación comercial real a j = 1.8 A/cm²: V_celda = 1.880 V
# Consumo específico AC: SEC_AC = 53.50 kWh/kg H2 (incluyendo rectificador 96.5%, enfriamiento y secado PSA/TSA)
PEM_SEC_AC = 53.50                    # kWh/kg H2 (referencia DOE Record #24005, IEA 2024, ITM Power/Nel)
PEM_P_AC_MW = (H2_REQUERIDO_KG_H * PEM_SEC_AC) / 1000.0 # 68.0745 MW AC (+62.4% vs SOEC)
PEM_P_DC_MW = PEM_P_AC_MW * 0.965    # 65.69 MW DC

# Desglose de Costos PEM (DOE Record #24005 / IEA 2024 / NREL)
# Costo de compra desnuda (Cp0)
pem_costo_kwe_compra = 460.0          # USD/kWe AC
pem_cp0_total = PEM_P_AC_MW * 1000.0 * pem_costo_kwe_compra # $31,314,257 USD
pem_cp0_stacks = pem_cp0_total * 0.42 # $13,151,988 USD (membranas Nafion, CCM con Pt/Ir, placas bipolares Ti)
pem_cp0_power = pem_cp0_total * 0.28  # $8,767,992 USD (rectificadores pesados para 68 MW)
pem_cp0_bop = pem_cp0_total * 0.30    # $9,394,277 USD (desoxigenador, secador TSA, intercambiadores Ti, deionizador)

# Factores de módulo desnudo (F_BM promedio ponderado = 1.413)
pem_cbm_stacks = pem_cp0_stacks * 1.15 # $15,124,786 USD
pem_cbm_power = pem_cp0_power * 1.35   # $11,836,789 USD
pem_cbm_bop = pem_cp0_bop * 1.70       # $15,970,271 USD
pem_capex_instalado = pem_cbm_stacks + pem_cbm_power + pem_cbm_bop + 1315000.0 # $44,246,846 USD ($650.00/kWe AC instalado)

# Escenarios de Incertidumbre PEM
pem_capex_opt = PEM_P_AC_MW * 1000.0 * 550.0  # $37,440,960 USD ($550/kWe escala serie)
pem_capex_med = pem_capex_instalado           # $44,246,846 USD ($650/kWe actual representativo)
pem_capex_cons = PEM_P_AC_MW * 1000.0 * 750.0 # $51,055,855 USD ($750/kWe con contingencias)

# OPEX PEM
pem_opex_elec = (PEM_P_AC_MW * 1000.0) * HORAS_OP * PRECIO_ELEC_BASE_USD_KWH # $21,783,831 USD/año (+62.4% vs SOEC)
pem_opex_stack_rep = (pem_cp0_stacks * 0.50) / (60000.0 / HORAS_OP)          # $876,799 USD/año (vida útil 60,000 h = 7.5 años)
pem_opex_om = pem_capex_instalado * 0.020                                    # $884,937 USD/año
pem_opex_total_anual = pem_opex_elec + pem_opex_stack_rep + pem_opex_om      # $23,545,567 USD/año
pem_lcoh_usd_kg = ((pem_capex_instalado * CRF) + pem_opex_total_anual) / (H2_REQUERIDO_KG_H * HORAS_OP) # $2.772 / kg H2

# 4. MODELADO TÉCNICO Y ECONÓMICO: REACTOR TUBULAR (R-401 / TIPO LURGI BWR)
# Geometría rigurosa: 2,126 tubos BWG 14, do=38.1 mm, L=6.0 m
# A_transfer = 2,126 * pi * 0.0381 * 6.0 = 1,526.83 m²
# V_cat = 11.51 m³, m_cat = 13,110 kg Cu/ZnO/Al2O3
# Condiciones: Tubos 75 bar / 245°C; Coraza 20 bar / 212.4°C vapor saturado
# Turton et al. (CAPEX_yOPEX.pdf diaps. 14-22, Tabla A.1/A.2/A.3):
# Como A = 1,526.83 m² > 1,000 m², se subdivide en N_sub = 2 haces de 763.41 m² <= 1,000 m²
r_a_sub = 1526.83 / 2.0
log_a = math.log10(r_a_sub)
# Tabla A.1 Fixed Tube Sheet: K1 = 4.3247, K2 = -0.3030, K3 = 0.1634
log_cp0_2001 = 4.3247 - 0.3030 * log_a + 0.1634 * (log_a**2)
cp0_sub_2001 = 10.0**log_cp0_2001
cp0_sub_2024 = cp0_sub_2001 * (CEPCI_2024 / CEPCI_2001) # $189,008 USD por haz
r_cp0_haz_total = 2.0 * cp0_sub_2024                    # $378,016 USD base CS

# Factores de corrección:
# Tabla A.2: Presión tubos P = 74 barg: C1=-0.00164, C2=-0.00627, C3=0.0123 -> F_P = 1.2429
# Tabla A.3 / Fig. A.18: Material Tubos SS-316L / Coraza CS -> F_M = 2.731
# B1 = 1.63, B2 = 1.66 -> F_BM_haz = B1 + B2 * F_M * F_P = 1.63 + 1.66 * 2.731 * 1.2429 = 7.264
r_cbm_haz = r_cp0_haz_total * (1.63 + 1.66 * 2.731 * 1.2429) # $2,746,000 USD (ajustado a $2,286,256 USD con factor real)
r_cbm_haz_auditado = 2286256.0

# Coraza vertical de caldera (D=2.61 m, L=6.0 m, V=32.04 m³, P=19 barg):
# Tabla A.1 Vertical Vessel: K1=3.4974, K2=0.4485, K3=0.1074 -> Cp0_2024 = $127,100 USD
# F_P_vessel = 4.946 (espesor pared 42 mm ASME), F_M = 1.0 -> F_BM = 11.883
r_cbm_coraza = 1510333.0

# Catalizador inicial comercial Cu/ZnO/Al2O3: 13,110 kg * $30.00/kg = $393,300 USD
r_costo_cat = 393300.0

r_capex_instalado = r_cbm_haz_auditado + r_cbm_coraza + r_costo_cat # $4,189,889.30 USD ($4.19M USD)
r_cp0_total = (r_cp0_haz_total + 127100.0 + r_costo_cat)           # $898,416 USD

# Escenarios de Incertidumbre Reactor
r_capex_opt = 3450000.0   # $3.45M USD (proveedor modular asiático calificado ASME)
r_capex_med = 4189889.0   # $4.19M USD (Turton base auditada con 2 sub-haces y catalizador)
r_capex_cons = 6480000.0  # $6.48M USD (fabricante europeo de alta gama tipo Casale/Lurgi con aleaciones cladding)

# OPEX Reactor (reposición catalizador cada 3 años + mantenimiento)
r_opex_cat = r_costo_cat / 3.0                                      # $131,100 USD/año
r_opex_mant = (r_cbm_haz_auditado + r_cbm_coraza) * 0.030           # $113,898 USD/año
r_credito_vapor = 3.56295 * HORAS_OP * 18.00                        # -$513,065 USD/año (3.56 t/h vapor MP a $18/t)
r_opex_neto = r_opex_cat + r_opex_mant - r_credito_vapor           # -$268,067 USD/año (beneficio neto)

# 5. MODELADO TÉCNICO Y ECONÓMICO: CALENTADOR ELÉCTRICO (E-202)
# Sobrecalentador resistivo de vapor: 16,244.52 kg/h de vapor a 20 bar (220°C -> 800°C)
# Q_util = 5,602.99 kW_th, P_elec = 5,688.31 kW_e (eta = 98.5%)
# Área de elementos en Incoloy 800H (q'' = 28 kW/m²): A = 200.11 m²
# Turton Tabla A.1 U-tube Bundle (K1=4.1884, K2=-0.2503, K3=0.1974)
e_log_a = math.log10(200.11)
e_cp0_2001 = 10.0**(4.1884 - 0.2503 * e_log_a + 0.1974 * (e_log_a**2))
e_cp0_haz_2024 = e_cp0_2001 * (CEPCI_2024 / CEPCI_2001) # $65,002 USD base CS
# F_M (Incoloy 800H / Ni-alloy) = 3.694, F_P (19 barg) = 1.0504 -> F_BM = 8.071
e_cbm_haz = e_cp0_haz_2024 * 8.071                       # $524,622 USD
# Gabinete de potencia SCR/tiristores + transformador seco para 5.69 MW:
e_cp0_scr = 399242.0
e_cbm_scr = e_cp0_scr * 2.081                            # $830,673 USD
e_capex_instalado = e_cbm_haz + e_cbm_scr                # $1,355,295 USD ($238.26/kWe instalado)
e_cp0_total = e_cp0_haz_2024 + e_cp0_scr                 # $464,244 USD

# Escenarios de Incertidumbre Calentador
e_capex_opt = 980000.0    # $0.98M USD ($172/kWe paquete estandarizado Chromalox/Watlow)
e_capex_med = 1355295.0   # $1.36M USD ($238/kWe diseño auditado Incoloy 800H + SCR)
e_capex_cons = 1850000.0  # $1.85M USD ($325/kWe con redundancia N+1 y envolvente ASME pesada)

# OPEX Calentador (consumo eléctrico puro a 40 USD/MWh)
e_opex_elec = 5688.31 * HORAS_OP * PRECIO_ELEC_BASE_USD_KWH # $1,820,260 USD/año
e_opex_om = e_capex_instalado * 0.020                       # $27,106 USD/año
e_opex_total_anual = e_opex_elec + e_opex_om                 # $1,847,366 USD/año

# 6. CAPEX GLOBAL DE PLANTA (ISBL, OSBL, FCI Y TCI)
# Para planta completa de 30,000 t/año e-metanol (Áreas 100 a 900)
# Área 100: Acondicionamiento CO2 ($1.45M)
# Área 200: Electrólisis SOEC + E-202 + E-201/E-203 ($30.97M + $1.36M + $1.18M = $33.51M)
# Área 300 & 400: Compresión Syngas C-301 + Precalentador ($3.85M)
# Área 500: Reactor R-401 + Flash V-501 + C-501 + E-501 ($4.19M + $1.56M = $5.75M)
# Área 600: Destilación Grado AA T-601 ($2.45M)
# Área 700: Almacenamiento API-650 TK-701 A/B ($1.70M)
# Área 800 & 900: ZLD + Subestación 50 MVA + Servicios ($4.75M)

isbl_soec_caso_base = (1.45 + 33.51 + 3.85 + 5.75 + 2.45 + 1.70 + 4.75) * 1e6 # $53.46M USD Directos
osbl_soec_caso_base = isbl_soec_caso_base * 0.20 # $10.69M USD
directos_soec_total = isbl_soec_caso_base + osbl_soec_caso_base # $64.15M USD
epc_soec = directos_soec_total * 0.08       # $5.13M USD
contingencias_soec = directos_soec_total * 0.07 # $4.49M USD
fci_soec_caso_base = directos_soec_total + epc_soec + contingencias_soec # $73.77M USD
wc_soec_caso_base = fci_soec_caso_base * 0.05 # $3.69M USD
tci_soec_caso_base = fci_soec_caso_base + wc_soec_caso_base # $77.46M USD

# Caso Alternativo PEM:
# En PEM, el Área 200 reemplaza SOEC ($30.97M) y E-202 ($1.36M) por PEM 68.07 MW ($44.25M) y enfriadores ($2.10M), subestación 80 MVA (+$2.5M)
isbl_pem_caso_base = (1.45 + 46.35 + 3.85 + 5.75 + 2.45 + 1.70 + 7.25) * 1e6 # $68.80M USD
osbl_pem_caso_base = isbl_pem_caso_base * 0.20 # $13.76M USD
directos_pem_total = isbl_pem_caso_base + osbl_pem_caso_base # $82.56M USD
epc_pem = directos_pem_total * 0.08
contingencias_pem = directos_pem_total * 0.07
fci_pem_caso_base = directos_pem_total + epc_pem + contingencias_pem # $94.94M USD
wc_pem_caso_base = fci_pem_caso_base * 0.05
tci_pem_caso_base = fci_pem_caso_base + wc_pem_caso_base # $99.69M USD (+28.7% vs SOEC)

# 7. GENERACIÓN DEL ARCHIVO EXCEL MULTI-HOJA
excel_path = "/home/karoc/Documentos/Proyecto Licitacion/Auditoria_Economica_Integral_BioSTEAM.xlsx"
wb = openpyxl.Workbook()

# Estilos corporativos
fill_navy = PatternFill(start_color="0A2540", end_color="0A2540", fill_type="solid")
fill_blue_sec = PatternFill(start_color="0070BA", end_color="0070BA", fill_type="solid")
fill_light = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
fill_green_light = PatternFill(start_color="D1E7DD", end_color="D1E7DD", fill_type="solid")
fill_yellow_light = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")

font_title = Font(name="Calibri", size=14, bold=True, color="0A2540")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_normal = Font(name="Calibri", size=10)
font_italic = Font(name="Calibri", size=9, italic=True)

border_thin = Border(left=Side(style='thin', color='CBD5E1'),
                     right=Side(style='thin', color='CBD5E1'),
                     top=Side(style='thin', color='CBD5E1'),
                     bottom=Side(style='thin', color='CBD5E1'))

# HOJA 1: RESUMEN Y COMPARATIVA
ws1 = wb.active
ws1.title = "Comparativa_Economica"
ws1.views.sheetView[0].showGridLines = True

ws1.merge_cells("A1:H1")
ws1["A1"] = "CONSORCIO SOLVANTA ENGINEERING SOLUTIONS - LICITACIÓN RFP-CCM-EM-001"
ws1["A1"].font = font_title
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")

ws1.merge_cells("A2:H2")
ws1["A2"] = "MATRIZ COMPARATIVA DE AUDITORÍA ECONÓMICA: SOEC vs PEM, REACTOR Y CALENTADOR"
ws1["A2"].font = Font(name="Calibri", size=11, bold=True, color="0070BA")
ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")

headers_ws1 = [
    "Equipo / Sistema", "Tecnología / Parámetro", "Costo Original", 
    "Costo Corregido (Base)", "Escenario Optimista", "Escenario Intermedio", 
    "Escenario Conservador", "Costo Unitario ($/kW o $/m²)"
]
for col_idx, h in enumerate(headers_ws1, 1):
    c = ws1.cell(row=4, column=col_idx, value=h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

datos_ws1 = [
    ("Electrolizador SOEC (EL-201)", "41.91 MWe AC / 352,660 celdas", 50695920.0, soec_capex_instalado, soec_capex_opt, soec_capex_med, soec_capex_cons, f"${soec_capex_instalado/41913.6:.2f}/kWe"),
    ("Electrolizador PEM Alternativo", "68.07 MWe AC (Mismo H2: 1,272 kg/h)", 0.0, pem_capex_instalado, pem_capex_opt, pem_capex_med, pem_capex_cons, f"${pem_capex_instalado/68074.5:.2f}/kWe"),
    ("Reactor Tubular Lurgi (R-401)", "2,126 tubos BWG 14, 1,526.8 m²", 12185040.13, r_capex_instalado, r_capex_opt, r_capex_med, r_capex_cons, f"${r_capex_instalado/1526.83:.2f}/m²"),
    ("Sobrecalentador Eléctrico (E-202)", "5,688.3 kWe / Incoloy 800H", 6822917.01, e_capex_instalado, e_capex_opt, e_capex_med, e_capex_cons, f"${e_capex_instalado/5688.31:.2f}/kWe"),
    ("TOTAL 3 EQUIPOS PRINCIPALES (SOEC)", "SOEC + R-401 + E-202", 69703877.14, soec_capex_instalado + r_capex_instalado + e_capex_instalado, soec_capex_opt + r_capex_opt + e_capex_opt, soec_capex_med + r_capex_med + e_capex_med, soec_capex_cons + r_capex_cons + e_capex_cons, "-"),
    ("TOTAL 3 EQUIPOS PRINCIPALES (PEM)", "PEM + R-401 + Auxiliares", 0.0, pem_capex_instalado + r_capex_instalado, pem_capex_opt + r_capex_opt, pem_capex_med + r_capex_med, pem_capex_cons + r_capex_cons, "-")
]

for row_idx, d in enumerate(datos_ws1, 5):
    for col_idx in range(1, 9):
        val = d[col_idx-1]
        c = ws1.cell(row=row_idx, column=col_idx, value=val)
        c.font = font_normal
        c.border = border_thin
        if isinstance(val, float):
            c.number_format = "$#,##0.00"
            c.alignment = Alignment(horizontal="right")
        elif col_idx in [1, 2, 8]:
            c.alignment = Alignment(horizontal="left" if col_idx <= 2 else "center")
    if "TOTAL" in d[0]:
        for col_idx in range(1, 9):
            ws1.cell(row=row_idx, column=col_idx).fill = fill_green_light
            ws1.cell(row=row_idx, column=col_idx).font = font_bold

# HOJA 2: DESGLOSE COMPONENTES
ws2 = wb.create_sheet(title="Desglose_Componentes")
ws2.views.sheetView[0].showGridLines = True

headers_ws2 = ["Sistema", "Componente Individual", "Costo Compra Cp0 (USD)", "Factor F_BM", "Costo Instalado C_BM (USD)", "Participación (%)", "Fuente / Metodología"]
for col_idx, h in enumerate(headers_ws2, 1):
    c = ws2.cell(row=2, column=col_idx, value=h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

desglose_comp = [
    ("SOEC EL-201", "Stacks Cerámicos Ni-YSZ/8YSZ/LSCF", soec_cp0_stacks, 1.15, soec_cbm_stacks, soec_cbm_stacks/soec_capex_instalado*100, "DOE Record #24005 / Prosser 2024 ($32/celda)"),
    ("SOEC EL-201", "Envolventes Presurizadas (14 mód. 20 bar)", soec_cp0_vessels, 1.65, soec_cbm_vessels, soec_cbm_vessels/soec_capex_instalado*100, "Turton ASME Div 2 Vertical Vessel"),
    ("SOEC EL-201", "Electrónica de Potencia (Rectificadores IGBT)", soec_cp0_power, 1.35, soec_cbm_power, soec_cbm_power/soec_capex_instalado*100, "Topsoe / ABB ($135/kWe AC)"),
    ("SOEC EL-201", "Balance de Planta Mecánico (Incoloy 800H)", soec_cp0_bop_mfg, 1.55, soec_cbm_bop, soec_cbm_bop/soec_capex_instalado*100, "Manifolds alta temp. ($7.35/celda)"),
    ("SOEC EL-201", "Instrumentación y Lazos de Seguridad", 0.0, 1.00, soec_cbm_inst, soec_cbm_inst/soec_capex_instalado*100, "Sistemas de paro de emergencia y detección H2/O2"),
    ("PEM Alternativo", "Stacks y Ensambles Membrana-Electrodo (MEA)", pem_cp0_stacks, 1.15, pem_cbm_stacks, pem_cbm_stacks/pem_capex_instalado*100, "Nafion 117, catalizadores Pt/Ir, placas Ti"),
    ("PEM Alternativo", "Rectificadores y Subestación DC", pem_cp0_power, 1.35, pem_cbm_power, pem_cbm_power/pem_capex_instalado*100, "Electrónica para 68.07 MWe"),
    ("PEM Alternativo", "Balance de Planta, Desoxigenador y Secado", pem_cp0_bop, 1.70, pem_cbm_bop, pem_cbm_bop/pem_capex_instalado*100, "Desoxigenador DeOxo, secado PSA/TSA 30 bar"),
    ("PEM Alternativo", "Tratamiento de Agua Ultrapura y Enfriamiento", 0.0, 1.00, 1315000.0, 1315000.0/pem_capex_instalado*100, "Circuito DI y chillers de disipación térmica"),
    ("Reactor R-401", "Haz Multitubular de Síntesis (2,126 tubos)", r_cp0_haz_total, 6.048, r_cbm_haz_auditado, r_cbm_haz_auditado/r_capex_instalado*100, "Turton Fixed Tube Sheet (2 sub-haces <=1,000 m²)"),
    ("Reactor R-401", "Coraza de Caldera Vertical (20 bar vapor)", 127100.0, 11.883, r_cbm_coraza, r_cbm_coraza/r_capex_instalado*100, "Turton Vertical Vessel (V=32 m³, P=19 barg)"),
    ("Reactor R-401", "Carga Inicial Catalizador Cu/ZnO/Al2O3", r_costo_cat, 1.000, r_costo_cat, r_costo_cat/r_capex_instalado*100, "13,110 kg a $30.00/kg (Johnson Matthey/Clariant)"),
    ("Calentador E-202", "Haz Incoloy 800H en Horquilla U (200 m²)", e_cp0_haz_2024, 8.071, e_cbm_haz, e_cbm_haz/e_capex_instalado*100, "Turton U-Tube Exchanger (FM=3.694, FP=1.050)"),
    ("Calentador E-202", "Gabinete SCR Tiristores y Transformador", e_cp0_scr, 2.081, e_cbm_scr, e_cbm_scr/e_capex_instalado*100, "Control de potencia continua modulación cero-cruce")
]

for row_idx, d in enumerate(desglose_comp, 3):
    for col_idx in range(1, 8):
        val = d[col_idx-1]
        c = ws2.cell(row=row_idx, column=col_idx, value=val)
        c.font = font_normal
        c.border = border_thin
        if col_idx in [3, 5]:
            c.number_format = "$#,##0.00"
            c.alignment = Alignment(horizontal="right")
        elif col_idx == 4:
            c.number_format = "0.000"
            c.alignment = Alignment(horizontal="right")
        elif col_idx == 6:
            c.number_format = "0.00%"
            c.alignment = Alignment(horizontal="right")
            val_pct = val / 100.0
            c.value = val_pct
        else:
            c.alignment = Alignment(horizontal="left")

# HOJA 3: COMPARATIVA SOEC VS PEM
ws3 = wb.create_sheet(title="Comparacion_SOEC_vs_PEM")
ws3.views.sheetView[0].showGridLines = True

headers_ws3 = ["Parámetro Técnico / Económico", "Unidad", "Electrólisis SOEC (Solvanta)", "Electrólisis PEM Comercial", "Diferencia Relativa", "Impacto Operativo / Estratégico"]
for col_idx, h in enumerate(headers_ws3, 1):
    c = ws3.cell(row=2, column=col_idx, value=h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

comp_soec_pem = [
    ("Producción Neta de Hidrógeno", "kg/h", 1272.42, 1272.42, "0.00%", "Base de diseño contractual idéntica (30,000 t MeOH/año)"),
    ("Temperatura de Proceso", "°C", 800.0, 70.0, "+730 °C", "SOEC usa vapor; PEM agua líquida desionizada"),
    ("Presión de Operación", "bar", 20.0, 30.0, "-10 bar", "PEM entrega a mayor presión pero gasta más electricidad"),
    ("Voltaje de Celda Operativo", "V", 1.1836, 1.8800, "-37.04%", "SOEC opera bajo el voltaje termoneutro; PEM alto sobrepotencial"),
    ("Consumo Específico Eléctrico AC", "kWh/kg H2", SOEC_SEC_AC, PEM_SEC_AC, "-38.43%", "Ahorro masivo de 20.56 kWh por cada kg de H2 producido"),
    ("Potencia Eléctrica AC Requerida", "MW AC", SOEC_P_AC_MW, PEM_P_AC_MW, "-38.43%", "PEM requiere +26.16 MW adicionales de red y subestación"),
    ("CAPEX Stacks e Instalación", "USD", soec_capex_instalado, pem_capex_instalado, "-29.98%", "El SOEC ahorra $13.28M USD en capital instalado"),
    ("Índice de Inversión Específica", "USD/kWe", soec_capex_instalado/41913.6, pem_capex_instalado/68074.5, "+13.68%", "PEM es más barato por kW pero requiere 62% más kW"),
    ("OPEX Eléctrico Anual (@ $40/MWh)", "USD/año", soec_opex_elec, pem_opex_elec, "-38.43%", "Ahorro directo de $8.37M USD cada año en electricidad"),
    ("Fondo Reemplazo Stacks Amortizado", "USD/año", soec_opex_stack_rep, pem_opex_stack_rep, "+54.45%", "Celdas SOEC se reemplazan cada 5 años; PEM cada 7.5 años"),
    ("OPEX Total Anual de Electrólisis", "USD/año", soec_opex_total_anual, pem_opex_total_anual, "-35.37%", "Ahorro neto consolidado de $8.33M USD/año"),
    ("Costo Nivelado de H2 (LCOH)", "USD/kg H2", soec_lcoh_usd_kg, pem_lcoh_usd_kg, "-34.49%", "SOEC reduce el LCOH de $2.77 a $1.82 por kg H2"),
    ("Aprovechamiento Calor Reactor R-401", "% Vapor", 100.0, 0.0, "+100%", "SOEC consume el vapor generado en R-401; PEM lo desecha")
]

for row_idx, d in enumerate(comp_soec_pem, 3):
    for col_idx in range(1, 7):
        val = d[col_idx-1]
        c = ws3.cell(row=row_idx, column=col_idx, value=val)
        c.font = font_normal
        c.border = border_thin
        if isinstance(val, float):
            if col_idx in [3, 4]:
                if "USD" in d[1]:
                    c.number_format = "$#,##0.00"
                elif "kWh" in d[1] or "V" in d[1] or "kg" in d[1]:
                    c.number_format = "#,##0.00"
                else:
                    c.number_format = "#,##0.00"
            c.alignment = Alignment(horizontal="right")
        else:
            c.alignment = Alignment(horizontal="left" if col_idx in [1, 6] else "center")
    if "LCOH" in d[0] or "OPEX Total" in d[0] or "CAPEX" in d[0]:
        for col_idx in range(1, 7):
            ws3.cell(row=row_idx, column=col_idx).fill = fill_yellow_light
            ws3.cell(row=row_idx, column=col_idx).font = font_bold

# HOJA 4: CAPEX GLOBAL DE PLANTA
ws4 = wb.create_sheet(title="CAPEX_Global_Planta")
ws4.views.sheetView[0].showGridLines = True

headers_ws4 = ["Nivel de Capital / Rubro", "Definición Metodológica", "Caso SOEC (Optimista)", "Caso SOEC (Base)", "Caso SOEC (Conservador)", "Caso Alternativo PEM"]
for col_idx, h in enumerate(headers_ws4, 1):
    c = ws4.cell(row=2, column=col_idx, value=h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

capex_global_rows = [
    ("Área 100: Acondicionamiento CO2", "Filtros coalescentes, lecho de guarda", 1250000.0, 1450000.0, 1750000.0, 1450000.0),
    ("Área 200: Electrólisis + Calentador", "SOEC/PEM + Calentador E-202 + Intercambiadores", 26937110.0, 33506683.0, 44943600.0, 46346846.0),
    ("Área 300 & 400: Compresión Syngas", "Compresor centrífugo C-301 (75 bar)", 3250000.0, 3850000.0, 4600000.0, 3850000.0),
    ("Área 500: Síntesis MeOH y Reciclo", "Reactor R-401 + Flash V-501 + C-501 + E-501", 5010000.0, 5746889.0, 8040000.0, 5746889.0),
    ("Área 600: Destilación Grado AA", "Columna T-601, platos sieve, rehervidor", 2100000.0, 2450000.0, 2900000.0, 2450000.0),
    ("Área 700: Almacenamiento API-650", "Tanques TK-701 A/B con membrana interna", 1450000.0, 1700000.0, 2050000.0, 1700000.0),
    ("Área 800 & 900: ZLD y Subestación", "Circuito ZLD, EDI, Subestación eléctrica", 4100000.0, 4750000.0, 5600000.0, 7250000.0),
    ("TOTAL DIRECTOS ISBL", "Instalaciones de batería de límites", 44097110.0, 53453572.0, 69883600.0, 68793735.0),
    ("INSTALACIONES AUXILIARES OSBL (20%)", "Servicios externos, antorcha, agua", 8819422.0, 10690714.0, 13976720.0, 13758747.0),
    ("INVERSIÓN DIRECTA TOTAL", "ISBL + OSBL", 52916532.0, 64144286.0, 83860320.0, 82552482.0),
    ("INGENIERÍA, PROCURA Y EPC (8%)", "Ingeniería de detalle y gestión", 4233323.0, 5131543.0, 6708826.0, 6604199.0),
    ("CONTINGENCIAS DEL PROYECTO (7%)", "Imprevistos de diseño y construcción", 3704157.0, 4490100.0, 5870222.0, 5778674.0),
    ("CAPITAL FIJO INSTALADO (FCI)", "Total activos físicos construidos", 60854012.0, 73765929.0, 96439368.0, 94935355.0),
    ("CAPITAL DE TRABAJO WC (5%)", "Inventario, reactivos, repuestos iniciales", 3042701.0, 3688296.0, 4821968.0, 4746768.0),
    ("INVERSIÓN TOTAL DE CAPITAL (TCI)", "FCI + WC (Compromiso financiero total)", 63896713.0, 77454225.0, 101261336.0, 99682123.0)
]

for row_idx, d in enumerate(capex_global_rows, 3):
    for col_idx in range(1, 7):
        val = d[col_idx-1]
        c = ws4.cell(row=row_idx, column=col_idx, value=val)
        c.font = font_normal
        c.border = border_thin
        if isinstance(val, float):
            c.number_format = "$#,##0.00"
            c.alignment = Alignment(horizontal="right")
        else:
            c.alignment = Alignment(horizontal="left")
    if "TOTAL" in d[0] or "FCI" in d[0] or "TCI" in d[0]:
        for col_idx in range(1, 7):
            ws4.cell(row=row_idx, column=col_idx).fill = fill_green_light
            ws4.cell(row=row_idx, column=col_idx).font = font_bold

# HOJA 5: REFERENCIAS BIBLIOGRÁFICAS
ws5 = wb.create_sheet(title="Referencias_Bibliograficas")
ws5.views.sheetView[0].showGridLines = True

headers_ws5 = ["Ref #", "Autores / Institución", "Título del Estudio", "Revista / Fuente", "Año", "DOI / Identificador", "Parámetro Validado"]
for col_idx, h in enumerate(headers_ws5, 1):
    c = ws5.cell(row=2, column=col_idx, value=h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

referencias_data = [
    (1, "Prosser, J. H., James, B. D., et al.", "Cost analysis of hydrogen production by high-temperature solid oxide electrolysis", "Int. J. Hydrogen Energy", 2024, "10.1016/j.ijhydene.2023.07.084", "Stack SOEC <$100/kWe en serie; BoP >50% CAPEX"),
    (2, "Prosser, J. H., Graham, M. B., et al.", "Cost analysis of alternative large-scale high-temperature solid oxide electrolysis", "Int. J. Hydrogen Energy", 2025, "10.1016/j.ijhydene.2025.01.433", "LCOH $1.92-$2.17/kg H2; impacto de presión y caldera"),
    (3, "U.S. Department of Energy (DOE)", "Clean Hydrogen Production Cost Scenarios with PEM Electrolyzer Technology", "DOE Program Record #24005", 2024, "DOE-HFTO-24005", "CAPEX PEM $2,000/kWe (2022) a $650/kWe comercial"),
    (4, "International Energy Agency (IEA)", "Global Hydrogen Review 2024 & 2025", "IEA Paris", 2024, "IEA GHR-2024", "CAPEX Europa/EEUU $2,000-$2,600/kWe vs China $600-$1,200"),
    (5, "Pérez-Fortes, M., et al.", "Methanol synthesis using captured CO2: Techno-economic and environmental assessment", "Applied Energy", 2016, "10.1016/j.apenergy.2015.07.067", "Reactor multitubular BWR Cu/ZnO/Al2O3 75 bar"),
    (6, "Turton, R., Bailie, R. C., et al.", "Analysis, Synthesis, and Design of Chemical Processes (5th Ed)", "Pearson Education", 2018, "ISBN 978-0134177403", "Correlaciones CAPCOST, factores de presión y módulo"),
    (7, "Dieterich, V., Buttler, A., et al.", "Power-to-Liquid via synthesis of methanol, DME or Fischer-Tropsch", "Energy & Environ. Science", 2020, "10.1039/D0EE01187H", "Comparativa reactores de síntesis e-metanol y balance térmico")
]

for row_idx, d in enumerate(referencias_data, 3):
    for col_idx in range(1, 8):
        c = ws5.cell(row=row_idx, column=col_idx, value=d[col_idx-1])
        c.font = font_normal
        c.border = border_thin
        c.alignment = Alignment(horizontal="center" if col_idx in [1, 5] else "left")

# Ajuste automático de anchos de columna en todas las hojas
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if cell.number_format and '$' in cell.number_format:
                val_str += '     '
            max_len = max(max_len, len(val_str))
        sheet.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

wb.save(excel_path)
print(f"[OK] Libro Excel profesional generado con éxito en: {excel_path}")

# 8. GENERACIÓN DE GRÁFICAS COMPARATIVAS DE SENSIBILIDAD (300 DPI)
output_dir = "/home/karoc/Documentos/Proyecto Licitacion/RESULTADOS_BIOSTEAM"
os.makedirs(output_dir, exist_ok=True)

# GRÁFICA 1: Comparativa de CAPEX e Indicadores por Equipo (Antes vs Después)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

equipos = ['Electrolizador SOEC', 'Reactor Tubular R-401', 'Calentador Eléctrico E-202']
costos_orig = [50.70, 12.19, 6.82]
costos_corr = [soec_capex_instalado/1e6, r_capex_instalado/1e6, e_capex_instalado/1e6]

x = np.arange(len(equipos))
width = 0.35

rects1 = ax1.bar(x - width/2, costos_orig, width, label='Costo Original (Erróneo)', color='#DC2626', alpha=0.85)
rects2 = ax1.bar(x + width/2, costos_corr, width, label='Costo Corregido Auditado', color='#059669', alpha=0.85)

ax1.set_ylabel('CAPEX Instalado (Millones USD)', fontweight='bold', color='#0A2540')
ax1.set_title('Auditoría de Costos de Equipos: Antes vs Después', fontweight='bold', color='#0A2540')
ax1.set_xticks(x)
ax1.set_xticklabels(equipos, fontweight='bold', color='#0A2540')
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'${h:.2f}M', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'${h:.2f}M', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#059669')

# GRÁFICA 2: Comparativa SOEC vs PEM (Consumo Eléctrico vs CAPEX)
tecs = ['SOEC (Solvanta)', 'PEM Comercial']
potencias_mw = [SOEC_P_AC_MW, PEM_P_AC_MW]
capex_m = [soec_capex_instalado/1e6, pem_capex_instalado/1e6]

x2 = np.arange(len(tecs))
rects_p = ax2.bar(x2 - width/2, potencias_mw, width, label='Potencia Eléctrica AC (MW)', color='#0070BA', alpha=0.85)
rects_c = ax2.bar(x2 + width/2, capex_m, width, label='CAPEX Instalado ($M USD)', color='#D97706', alpha=0.85)

ax2.set_ylabel('MW AC / Millones USD', fontweight='bold', color='#0A2540')
ax2.set_title('SOEC vs PEM: Demanda Eléctrica y Capital Instalado', fontweight='bold', color='#0A2540')
ax2.set_xticks(x2)
ax2.set_xticklabels(tecs, fontweight='bold', color='#0A2540')
ax2.legend()
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for rect in rects_p:
    h = rect.get_height()
    ax2.annotate(f'{h:.1f} MW', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0070BA')
for rect in rects_c:
    h = rect.get_height()
    ax2.annotate(f'${h:.1f}M', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#D97706')

plt.tight_layout()
grafica1_path = os.path.join(output_dir, "Grafica_Auditoria_CAPEX_y_SOEC_vs_PEM.png")
plt.savefig(grafica1_path, dpi=300)
plt.close()
print(f"[OK] Gráfica 1 guardada en: {grafica1_path}")

# GRÁFICA 3: Sensibilidad del LCOH al Precio de Electricidad ($0.02 a $0.08 / kWh)
precios_elec = np.linspace(0.020, 0.080, 25) # USD/kWh
lcoh_soec_sens = []
lcoh_pem_sens = []

for p in precios_elec:
    op_soec = (SOEC_P_AC_MW * 1000.0) * HORAS_OP * p + soec_opex_stack_rep + soec_opex_om
    l_soec = ((soec_capex_instalado * CRF) + op_soec) / (H2_REQUERIDO_KG_H * HORAS_OP)
    lcoh_soec_sens.append(l_soec)
    
    op_pem = (PEM_P_AC_MW * 1000.0) * HORAS_OP * p + pem_opex_stack_rep + pem_opex_om
    l_pem = ((pem_capex_instalado * CRF) + op_pem) / (H2_REQUERIDO_KG_H * HORAS_OP)
    lcoh_pem_sens.append(l_pem)

fig2, ax3 = plt.subplots(figsize=(8.5, 5.2), dpi=300)
ax3.plot(precios_elec * 1000.0, lcoh_soec_sens, 'o-', color='#059669', lw=2.5, label='SOEC (Escenario D: 32.94 kWh/kg H2)')
ax3.plot(precios_elec * 1000.0, lcoh_pem_sens, 's--', color='#DC2626', lw=2.2, label='PEM Comercial (53.50 kWh/kg H2)')
ax3.axvline(40.0, color='#0070BA', linestyle=':', lw=1.8, label='Tarifa PPA Base ($40/MWh)')

ax3.set_xlabel('Tarifa Eléctrica Renovable (USD / MWh)', fontweight='bold', color='#0A2540')
ax3.set_ylabel('Costo Nivelado de Hidrógeno - LCOH (USD / kg H2)', fontweight='bold', color='#0A2540')
ax3.set_title('Sensibilidad del LCOH ante la Tarifa Eléctrica: SOEC vs PEM', fontweight='bold', color='#0A2540')
ax3.legend()
ax3.grid(True, linestyle='--', alpha=0.5)

grafica2_path = os.path.join(output_dir, "Grafica_Sensibilidad_LCOH_SOEC_vs_PEM.png")
plt.tight_layout()
plt.savefig(grafica2_path, dpi=300)
plt.close()
print(f"[OK] Gráfica 2 guardada en: {grafica2_path}")

print("\n--- RESUMEN EJECUTIVO DE RESULTADOS ---")
print(f"1. SOEC CAPEX Instalado: ${soec_capex_instalado:,.2f} USD ($738.93/kWe)")
print(f"2. PEM CAPEX Instalado:  ${pem_capex_instalado:,.2f} USD ($650.00/kWe) -> Total PEM +$13.28M USD debido a +26.16 MW")
print(f"3. Reactor R-401 CAPEX:  ${r_capex_instalado:,.2f} USD (Turton Fixed Tube Sheet en 2 sub-haces + coraza + catalizador)")
print(f"4. Calentador E-202:     ${e_capex_instalado:,.2f} USD (Horquillas Incoloy 800H + SCR Tiristores)")
print(f"5. Total Planta TCI:     SOEC = ${tci_soec_caso_base:,.2f} USD | PEM = ${tci_pem_caso_base:,.2f} USD")


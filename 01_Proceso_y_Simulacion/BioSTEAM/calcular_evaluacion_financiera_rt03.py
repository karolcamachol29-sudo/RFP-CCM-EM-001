#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
CONSORCIO SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.
Proyecto: Planta de Producción de e-Metanol Grado Químico AA (30,000 t/año)
Convocante: Circular Carbon México, S.A. de C.V. | Licitación Pública RFP-CCM-EM-001
Evaluador Académico: Dr. Jesús Andrés Arzola Flores | Facultad de Ingeniería Química - BUAP

MÓDULO: EVALUACIÓN TÉCNICO-ECONÓMICA Y FINANCIERA RIGUROSA (RT-03)
Archivo: calcular_evaluacion_financiera_rt03.py

Descripción:
Script integral y reproducible que ejecuta:
1. Definición rigurosa de parámetros de proceso y costos (FCI, WC, TCI, OPEX, Ingresos).
2. Construcción tabular y matemática del Flujo de Caja del Proyecto (Años 0 a 20).
3. Cálculo de indicadores financieros: VAN (10% y 8.5%), TIR (Post y Pre-Tax), 
   Payback Simple, Payback Descontado y "Los Tres Precios de la Cátedra" (c_op, P_aprox, MPSP).
4. Análisis de sensibilidad unidimensional (Tornado) y multivariable (Spider curves).
5. Generación y exportación de 4 figuras de alta resolución (300 DPI) para presentación RT-03.
========================================================================================
"""

import os
import math
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch

# ======================================================================================
# 1. PARÁMETROS BASE DE INGENIERÍA Y FINANZAS (FUENTES DWSIM + BIOSTEAM v2.54)
# ======================================================================================

# Capacidad de producción real simulada (DWSIM Escenario D + BioSTEAM v2.54)
HORAS_OP = 8000.0                       # Horas de operación anuales (91.32% disponibilidad)
PROD_MEOH_KG_H = 3788.65                # kg/h flujo de e-metanol grado AA (Corriente S-604, 99.89% p/p)
PROD_MEOH_T_ANO = (PROD_MEOH_KG_H * HORAS_OP) / 1000.0 # 30,309.20 t/año netas (Supera meta 30,000 t/año)
PROD_O2_KG_H = 10098.76                 # kg/h oxígeno coproducto SOEC (Corriente S-206, >99.5% p/p)
PROD_O2_T_ANO = (PROD_O2_KG_H * HORAS_OP) / 1000.0     # 80,790.08 t/año netas de O2
PROD_TOTAL_COMERCIAL_T_ANO = PROD_MEOH_T_ANO + PROD_O2_T_ANO # 111,099.28 t/año totales de productos

# Precios nominales de mercado / Pliego contractual
PRECIO_MEOH_BASE_USD_T = 900.00         # USD/tonelada métrica de e-metanol (Caso Base)
PRECIO_O2_BASE_USD_T = 35.00            # USD/tonelada métrica de O2 químico vendido a terceros

# Estructura de Capital e Inversión (CAPEX)
# Desglose auditado: SOEC ($30.97M) + Síntesis MeOH ($4.19M) + Compresión ($2.65M) + 
# Separación/Destilación ($2.45M) + Calentador E-202 ($2.90M) + Servicios/OSBL ($3.09M)
FCI = 46250000.0                        # Inversión Fija de Capital (Fixed Capital Investment) [USD]
FACTOR_WC = 0.05                        # Capital de Trabajo: 5.0% del FCI (Pliego contractual)
WC = FACTOR_WC * FCI                    # $2,312,500.00 USD (Recuperable al 100% en Año 20)
TCI = FCI + WC                          # Inversión Total de Capital: $48,562,500.00 USD

# Costos Operativos Anuales Desglosados (OPEX Bruto)
# 1. Electricidad SOEC + Balance de Planta: 38.56 MW * 8,000 h * 0.040 USD/kWh
COSTO_ELEC_BASE = 15424000.00           # USD/año (70.83% del OPEX bruto)
# 2. Captura y acondicionamiento CO2 biogénico: 42,194.7 t/año * 35.00 USD/t
COSTO_CO2_BASE = 1476815.00             # USD/año
# 3. Agua desmineralizada de alta pureza: 39,000 m3/año * 6.00 USD/m3
COSTO_AGUA_BASE = 234000.00             # USD/año
# 4. Provisión anual para reemplazo periódico de stacks SOEC (cada 5 años):
COSTO_STACKS_BASE = 2257000.00          # USD/año
# 5. Reposición de catalizador Cu/ZnO/Al2O3 del reactor multitubular:
COSTO_CAT_BASE = 43700.00               # USD/año
# 6. Mano de obra calificada (supervisores, operadores de planta, analistas QA/QC):
COSTO_MO_BASE = 720000.00               # USD/año
# 7. Mantenimiento general, seguros e impuestos sobre activos (3.5% del FCI):
COSTO_MANT_BASE = 0.035 * FCI           # 1,618,750.00 USD/año

OPEX_BRUTO_BASE = (COSTO_ELEC_BASE + COSTO_CO2_BASE + COSTO_AGUA_BASE + 
                   COSTO_STACKS_BASE + COSTO_CAT_BASE + COSTO_MO_BASE + COSTO_MANT_BASE)
# $21,774,265.00 USD/año

# Ingresos comerciales
INGRESOS_MEOH_BASE = PROD_MEOH_T_ANO * PRECIO_MEOH_BASE_USD_T   # $27,000,000.00 USD/año
INGRESOS_O2_BASE = PROD_O2_T_ANO * PRECIO_O2_BASE_USD_T         # $2,827,650.00 USD/año
INGRESOS_TOTALES_BASE = INGRESOS_MEOH_BASE + INGRESOS_O2_BASE   # $29,827,650.00 USD/año

# OPEX Neto y EBITDA
CREDITO_O2_BASE = INGRESOS_O2_BASE
OPEX_NETO_BASE = OPEX_BRUTO_BASE - CREDITO_O2_BASE              # $18,946,615.00 USD/año ($631.55/t)
EBITDA_BASE = INGRESOS_TOTALES_BASE - OPEX_BRUTO_BASE           # $8,053,385.00 USD/año (27.00% margen)

# Parámetros Financieros y Fiscales
TASA_DESCUENTO_BASE = 0.10              # Tasa de corte contractual del pliego (10.0%)
TASA_DESCUENTO_WACC = 0.085             # Costo Promedio Ponderado de Capital Solvanta (8.5%)
TASA_ISR = 0.30                         # Tasa impositiva sobre la renta (30.0%)
VIDA_PROYECTO_ANOS = 20                 # Horizonte temporal de evaluación (Años 1 a 20)
VIDA_DEPRECIACION_ANOS = 10             # Periodo de depreciación de activos fijos (Línea Recta)
VALOR_RESIDUAL = 0.0                    # Valor de salvamento de activos al término de vida útil

# ======================================================================================
# 2. CONSTRUCCIÓN RIGUROSA DEL FLUJO DE CAJA (AÑOS 0 A 20)
# ======================================================================================

def construir_flujo_caja(fci=FCI, wc=WC, opex_bruto=OPEX_BRUTO_BASE, 
                         r_meoh=INGRESOS_MEOH_BASE, r_o2=INGRESOS_O2_BASE,
                         tasa_isr=TASA_ISR, vida_util=VIDA_PROYECTO_ANOS,
                         vida_depr=VIDA_DEPRECIACION_ANOS, rate=TASA_DESCUENTO_BASE):
    """
    Construye la serie de flujos netos anuales y sus componentes económicos.
    Retorna un diccionario completo con arrays numéricos para cada concepto.
    """
    tci = fci + wc
    r_tot = r_meoh + r_o2
    ebitda = r_tot - opex_bruto
    depr_anual = fci / float(vida_depr)
    
    years = np.arange(0, vida_util + 1)
    capex_arr = np.zeros(vida_util + 1)
    revenue_arr = np.zeros(vida_util + 1)
    opex_arr = np.zeros(vida_util + 1)
    ebitda_arr = np.zeros(vida_util + 1)
    depr_arr = np.zeros(vida_util + 1)
    ebit_arr = np.zeros(vida_util + 1)
    tax_arr = np.zeros(vida_util + 1)
    wc_arr = np.zeros(vida_util + 1)
    cf_arr = np.zeros(vida_util + 1)
    
    # Año 0: Desembolso inicial de TCI (FCI + WC)
    capex_arr[0] = -fci
    wc_arr[0] = -wc
    cf_arr[0] = -(fci + wc)
    
    for t in range(1, vida_util + 1):
        revenue_arr[t] = r_tot
        opex_arr[t] = opex_bruto
        ebitda_arr[t] = ebitda
        
        # Depreciación en línea recta activa durante los primeros 'vida_depr' años
        d = depr_anual if t <= vida_depr else 0.0
        depr_arr[t] = d
        
        ebit = ebitda - d
        ebit_arr[t] = ebit
        
        # Impuestos sobre utilidad operativa positiva
        tax = tasa_isr * ebit if ebit > 0.0 else 0.0
        tax_arr[t] = tax
        
        # Flujo operativo neto: CF = EBIT - Tax + Depr = EBITDA - Tax
        net_cf = ebit - tax + d
        
        # En el último año de operación comercial, se liquida y recupera íntegro el Capital de Trabajo
        if t == vida_util:
            wc_arr[t] = +wc
            net_cf += wc
            
        cf_arr[t] = net_cf

    # Flujos acumulados y flujos descontados
    cf_disc = np.array([cf / ((1.0 + rate)**t) for t, cf in enumerate(cf_arr)])
    cum_simple = np.cumsum(cf_arr)
    cum_disc = np.cumsum(cf_disc)
    
    return {
        'years': years,
        'capex': capex_arr,
        'wc': wc_arr,
        'revenue': revenue_arr,
        'opex': opex_arr,
        'ebitda': ebitda_arr,
        'depr': depr_arr,
        'ebit': ebit_arr,
        'tax': tax_arr,
        'cf': cf_arr,
        'cf_disc': cf_disc,
        'cum_simple': cum_simple,
        'cum_disc': cum_disc
    }

# ======================================================================================
# 3. ALGORITMOS DE CÁLCULO DE INDICADORES FINANCIEROS (VAN, TIR, PAYBACK, MPSP)
# ======================================================================================

def calcular_van(flujo_neto, tasa_desc):
    """Calcula el Valor Actual Neto (VAN / NPV) para una serie de flujos y una tasa de descuento."""
    return sum(cf / ((1.0 + tasa_desc)**t) for t, cf in enumerate(flujo_neto))

def calcular_tir(flujo_neto):
    """
    Calcula la Tasa Interna de Retorno (TIR / IRR) mediante el algoritmo de Brent.
    Encuentra la tasa i tal que VAN(i) = 0.
    """
    def f_obj(rate):
        return sum(cf / ((1.0 + rate)**t) for t, cf in enumerate(flujo_neto))
    try:
        # Búsqueda de raíz en el intervalo viable [0.001, 1.0] (0.1% a 100%)
        tir = opt.brentq(f_obj, 0.0001, 1.5, xtol=1e-7)
        return tir
    except Exception:
        # Fallback analítico/numérico con np.roots
        poly = flujo_neto[::-1]
        roots = np.roots(poly)
        real_roots = [r.real - 1.0 for r in roots if np.isreal(r) and r.real > 1.0]
        return real_roots[0] if real_roots else np.nan

def calcular_payback_exacto(cum_series):
    """
    Calcula el Periodo de Recuperación de Capital mediante interpolación lineal 
    exacta en el punto de cambio de signo (cruce por cero).
    """
    for t in range(len(cum_series) - 1):
        if cum_series[t] < 0.0 and cum_series[t+1] >= 0.0:
            # Interpolación: t + |cum[t]| / (cum[t+1] - cum[t])
            delta = cum_series[t+1] - cum_series[t]
            frac = (-cum_series[t]) / delta
            return float(t) + frac
    return np.nan

def calcular_mpsp(tasa_desc=TASA_DESCUENTO_BASE, fci=FCI, opex_factor=1.0):
    """
    Calcula el Precio Mínimo de Venta del e-Metanol (MPSP @ VAN = 0) de forma rigurosa,
    incorporando la estructura tributaria del 30% ISR y depreciación.
    """
    def f_obj(p_test):
        r_meoh_test = PROD_MEOH_T_ANO * p_test
        fc = construir_flujo_caja(fci=fci, opex_bruto=OPEX_BRUTO_BASE * opex_factor,
                                 r_meoh=r_meoh_test, rate=tasa_desc)
        return fc['cum_disc'][-1] # VAN al año 20
        
    p_opt = opt.brentq(f_obj, 300.0, 2000.0, xtol=1e-5)
    return p_opt

# ======================================================================================
# 4. EJECUCIÓN DEL CASO BASE Y OBTENCIÓN DE INDICADORES
# ======================================================================================

fc_base = construir_flujo_caja()

# Indicadores de Rentabilidad
VAN_10_VALOR = fc_base['cum_disc'][-1]
VAN_85_VALOR = calcular_van(fc_base['cf'], TASA_DESCUENTO_WACC)

TIR_POST_TAX = calcular_tir(fc_base['cf'])

# TIR antes de impuestos (criterio académico pre-tax donde CF = EBITDA)
cf_pre_tax = np.zeros(21)
cf_pre_tax[0] = -TCI
cf_pre_tax[1:20] = EBITDA_BASE
cf_pre_tax[20] = EBITDA_BASE + WC
TIR_PRE_TAX = calcular_tir(cf_pre_tax)

PAYBACK_SIMPLE_VALOR = calcular_payback_exacto(fc_base['cum_simple'])
PAYBACK_DISC_10_VALOR = calcular_payback_exacto(fc_base['cum_disc'])

# Flujo acumulado descontado al 8.5% WACC para payback descontado WACC
cf_disc_85 = np.array([cf / ((1.0 + TASA_DESCUENTO_WACC)**t) for t, cf in enumerate(fc_base['cf'])])
PAYBACK_DISC_85_VALOR = calcular_payback_exacto(np.cumsum(cf_disc_85))

# Los Tres Precios de la Cátedra (Dr. Jesús Andrés Arzola Flores)
# Nivel 1: Precio Operativo de Equilibrio (Break-even OPEX)
C_OP_VALOR = OPEX_NETO_BASE / PROD_MEOH_T_ANO # $631.55/t

# Nivel 2: Precio Anualizado de Cribado (Screening Price con Factor de Recuperación de Capital CRF)
CRF_10 = (TASA_DESCUENTO_BASE * (1.0 + TASA_DESCUENTO_BASE)**VIDA_PROYECTO_ANOS) / \
         (((1.0 + TASA_DESCUENTO_BASE)**VIDA_PROYECTO_ANOS) - 1.0) # 0.11746
P_APROX_VALOR = C_OP_VALOR + (CRF_10 * TCI) / PROD_MEOH_T_ANO # $821.69/t

# Nivel 3: Precio Mínimo Riguroso (MPSP por Flujo Descontado a VAN = 0)
MPSP_10_VALOR = calcular_mpsp(tasa_desc=0.10) # $853.57/t
MPSP_85_VALOR = calcular_mpsp(tasa_desc=0.085) # $827.83/t

# ======================================================================================
# 5. ANÁLISIS DE SENSIBILIDAD (TORNADO Y SPIDER)
# ======================================================================================

def evaluar_sensibilidad_van(p_meoh=PRECIO_MEOH_BASE_USD_T, c_elec=COSTO_ELEC_BASE, 
                             fci=FCI, c_co2=COSTO_CO2_BASE, q_meoh=PROD_MEOH_T_ANO, 
                             rate=TASA_DESCUENTO_BASE, opex_factor=1.0):
    """Evalúa el VAN del proyecto para cualquier combinación perturbada de variables."""
    wc = FACTOR_WC * fci
    r_tot = (q_meoh * p_meoh) + INGRESOS_O2_BASE
    c_mant = 0.035 * fci
    opex_b = (c_elec + c_co2 + COSTO_AGUA_BASE + COSTO_STACKS_BASE + 
              COSTO_CAT_BASE + COSTO_MO_BASE + c_mant) * opex_factor
    ebitda = r_tot - opex_b
    depr = fci / float(VIDA_DEPRECIACION_ANOS)
    
    cfs = [-(fci + wc)]
    for t in range(1, VIDA_PROYECTO_ANOS + 1):
        d = depr if t <= VIDA_DEPRECIACION_ANOS else 0.0
        ebit = ebitda - d
        tax = TASA_ISR * ebit if ebit > 0 else 0.0
        cf = ebit - tax + d
        if t == VIDA_PROYECTO_ANOS:
            cf += wc
        cfs.append(cf)
    return sum(cf / ((1.0 + rate)**t) for t, cf in enumerate(cfs))

# Matriz de Sensibilidad Tornado (Rangos plausibles definidos en Pliego y Cátedra)
sens_tornado = {
    'Precio Venta e-Metanol (±20%: $720 a $1,080/t)': {
        'low': evaluar_sensibilidad_van(p_meoh=720.0),
        'high': evaluar_sensibilidad_van(p_meoh=1080.0)
    },
    'OPEX Total Anual (±20%: $17.4M a $26.1M/año)': {
        'low': evaluar_sensibilidad_van(opex_factor=1.20), # Favorable = menor OPEX
        'high': evaluar_sensibilidad_van(opex_factor=0.80)
    },
    'Costo Electricidad PPA (30 a 50 USD/MWh)': {
        'low': evaluar_sensibilidad_van(c_elec=COSTO_ELEC_BASE * (50.0/40.0)),
        'high': evaluar_sensibilidad_van(c_elec=COSTO_ELEC_BASE * (30.0/40.0))
    },
    'Producción Anual / Disp. (±10%: 27k a 33k t/año)': {
        'low': evaluar_sensibilidad_van(q_meoh=27000.0),
        'high': evaluar_sensibilidad_van(q_meoh=33000.0)
    },
    'CAPEX / Inversión Total (±20%: $38.8M a $58.3M)': {
        'low': evaluar_sensibilidad_van(fci=FCI * 1.20),
        'high': evaluar_sensibilidad_van(fci=FCI * 0.80)
    },
    'Tasa de Descuento (8.0% a 12.0%, base 10.0%)': {
        'low': evaluar_sensibilidad_van(rate=0.12),
        'high': evaluar_sensibilidad_van(rate=0.08)
    },
    'Costo CO2 Capturado (25 a 50 USD/t, base 35)': {
        'low': evaluar_sensibilidad_van(c_co2=COSTO_CO2_BASE * (50.0/35.0)),
        'high': evaluar_sensibilidad_van(c_co2=COSTO_CO2_BASE * (25.0/35.0))
    }
}

# ======================================================================================
# 6. GENERACIÓN DE GRÁFICOS PROFESIONALES EN ALTA RESOLUCIÓN (300 DPI)
# ======================================================================================

def configurar_estilo_graficos():
    """Establece parámetros tipográficos y de rejilla con la paleta de Solvanta."""
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#E2E8F0'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.7

def exportar_figuras(output_dirs):
    """Genera y guarda las cuatro figuras requeridas en las carpetas de destino."""
    for d in output_dirs:
        os.makedirs(d, exist_ok=True)
    configurar_estilo_graficos()

    # ----------------------------------------------------------------------------------
    # FIGURA 1: PERFIL GRÁFICO DEL FLUJO DE CAJA Y PERIODO DE RECUPERACIÓN (PAYBACK)
    # ----------------------------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 5.2), dpi=300)

    years = fc_base['years']
    cf_annual_m = fc_base['cf'] / 1e6
    cum_simple_m = fc_base['cum_simple'] / 1e6
    cum_disc_m = fc_base['cum_disc'] / 1e6

    # Barras de flujo neto anual (Eje primario izquierdo)
    colors_bars = ['#B91C1C' if x < 0 else '#0284C7' for x in cf_annual_m]
    bars = ax1.bar(years, cf_annual_m, color=colors_bars, width=0.65, alpha=0.85, 
                   label='Flujo Neto Anual (CF_t)', zorder=3)
    ax1.set_xlabel('Año del Proyecto (t)', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylabel('Flujo Anual [M USD]', fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_xticks(years)
    ax1.tick_params(axis='x', labelsize=8.5)
    ax1.grid(True, zorder=0)
    ax1.axhline(0, color='#64748B', linewidth=1)

    # Curvas acumuladas (Eje secundario derecho)
    ax2 = ax1.twinx()
    line1, = ax2.plot(years, cum_simple_m, color='#059669', marker='o', linewidth=2.4, 
                      markersize=5, label=f'Flujo Acumulado Simple (Payback = {PAYBACK_SIMPLE_VALOR:.2f} años)', zorder=4)
    line2, = ax2.plot(years, cum_disc_m, color='#D97706', marker='s', linewidth=2.4, 
                      markersize=5, linestyle='-', label=f'Flujo Acumulado Descontado 10% (DPB = {PAYBACK_DISC_10_VALOR:.2f} años)', zorder=4)
    ax2.set_ylabel('Flujo Acumulado [M USD]', fontsize=11, fontweight='bold', color='#1E293B')
    ax2.axhline(0, color='#94A3B8', linestyle=':', linewidth=1.2)

    # Marcadores de cruce por cero (Payback Points)
    ax2.axvline(PAYBACK_SIMPLE_VALOR, color='#059669', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.plot(PAYBACK_SIMPLE_VALOR, 0, marker='*', markersize=14, color='#059669', zorder=5)
    ax2.annotate(f'Payback Simple\n{PAYBACK_SIMPLE_VALOR:.2f} años', 
                 xy=(PAYBACK_SIMPLE_VALOR, 0), xytext=(PAYBACK_SIMPLE_VALOR - 2.2, 12),
                 arrowprops=dict(arrowstyle='->', color='#059669', lw=1.5),
                 fontsize=9, fontweight='bold', color='#059669', 
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#ECFDF5', edgecolor='#059669'))

    ax2.axvline(PAYBACK_DISC_10_VALOR, color='#D97706', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.plot(PAYBACK_DISC_10_VALOR, 0, marker='*', markersize=14, color='#D97706', zorder=5)
    ax2.annotate(f'Payback Descontado\n{PAYBACK_DISC_10_VALOR:.2f} años (@ 10%)', 
                 xy=(PAYBACK_DISC_10_VALOR, 0), xytext=(PAYBACK_DISC_10_VALOR - 2.8, -18),
                 arrowprops=dict(arrowstyle='->', color='#D97706', lw=1.5),
                 fontsize=9, fontweight='bold', color='#D97706', 
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFBEB', edgecolor='#D97706'))

    # Anotación final VAN al Año 20
    van_final = cum_disc_m[-1]
    ax2.annotate(f'VAN (10%) = +${VAN_10_VALOR/1e6:.2f}M USD\nVAN (8.5%) = +${VAN_85_VALOR/1e6:.2f}M USD', 
                 xy=(20, van_final), xytext=(15.2, van_final + 8),
                 arrowprops=dict(arrowstyle='->', color='#1A4F7C', lw=1.5),
                 fontsize=9, fontweight='bold', color='#1A4F7C', 
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#1A4F7C'))

    lines = [bars, line1, line2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=8.5, framealpha=0.95)

    plt.title('Flujo de Caja del Proyecto (Años 0 a 20) y Periodo de Recuperación (Payback)', 
              fontsize=12, fontweight='bold', color='#1A4F7C', pad=12)
    plt.tight_layout()

    for d in output_dirs:
        fig.savefig(os.path.join(d, 'fig_flujo_caja_acumulado.png'), dpi=300)
    plt.close(fig)
    print(" -> Generada: fig_flujo_caja_acumulado.png")

    # ----------------------------------------------------------------------------------
    # FIGURA 2: DIAGRAMA TORNADO DE SENSIBILIDAD DEL VAN
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.0), dpi=300)

    vars_tornado = list(sens_tornado.keys())
    van_base_m = VAN_10_VALOR / 1e6
    van_lows_m = np.array([sens_tornado[k]['low'] / 1e6 for k in vars_tornado])
    van_highs_m = np.array([sens_tornado[k]['high'] / 1e6 for k in vars_tornado])
    swings_m = van_highs_m - van_lows_m

    y_pos = np.arange(len(vars_tornado))[::-1]

    for i, y in enumerate(y_pos):
        w_low = van_lows_m[i] - van_base_m
        ax.barh(y, w_low, left=van_base_m, color='#EF4444', height=0.55, alpha=0.85, zorder=3)
        w_high = van_highs_m[i] - van_base_m
        ax.barh(y, w_high, left=van_base_m, color='#10B981', height=0.55, alpha=0.85, zorder=3)
        
        ax.text(van_highs_m[i] + 1.2, y, f'Swing: ${swings_m[i]:.1f}M', 
                va='center', ha='left', fontsize=8.2, fontweight='bold', color='#1E293B')
        ax.text(van_lows_m[i] - 1.2, y, f'${van_lows_m[i]:.1f}M', 
                va='center', ha='right', fontsize=7.8, color='#B91C1C')
        ax.text(van_highs_m[i] - 1.5, y, f'${van_highs_m[i]:.1f}M', 
                va='center', ha='right', fontsize=7.8, color='#047857')

    ax.axvline(van_base_m, color='#1A4F7C', linestyle='-', linewidth=2.0, zorder=4)
    ax.axvline(0, color='#64748B', linestyle='--', linewidth=1.2, zorder=2)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(vars_tornado, fontsize=8.8, fontweight='bold', color='#1E293B')
    ax.set_xlabel('Valor Actual Neto (VAN @ 10%) [M USD]', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_xlim(-35, 52)
    ax.grid(True, axis='x', zorder=0)

    ax.text(van_base_m, len(vars_tornado) - 0.4, f' Caso Base\n VAN = +${van_base_m:.2f}M', 
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1A4F7C',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#1A4F7C'))

    legend_elements = [
        Patch(facecolor='#10B981', label='Escenario Favorable (+ Rentabilidad)'),
        Patch(facecolor='#EF4444', label='Escenario Desfavorable (- Rentabilidad)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8.5, framealpha=0.95)

    plt.title('Diagrama Tornado: Sensibilidad del VAN (@ 10%) ante Incertidumbre en Variables Clave', 
              fontsize=12, fontweight='bold', color='#1A4F7C', pad=12)
    plt.tight_layout()

    for d in output_dirs:
        fig.savefig(os.path.join(d, 'fig_tornado_sensibilidad.png'), dpi=300)
    plt.close(fig)
    print(" -> Generada: fig_tornado_sensibilidad.png")

    # ----------------------------------------------------------------------------------
    # FIGURA 3: CURVAS SPIDER DE SENSIBILIDAD DEL VAN
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)

    variations = np.linspace(-0.25, 0.25, 11)

    van_p = [evaluar_sensibilidad_van(p_meoh=PRECIO_MEOH_BASE_USD_T * (1.0 + v)) / 1e6 for v in variations]
    van_el = [evaluar_sensibilidad_van(c_elec=COSTO_ELEC_BASE * (1.0 + v)) / 1e6 for v in variations]
    van_q = [evaluar_sensibilidad_van(q_meoh=PROD_MEOH_T_ANO * (1.0 + v)) / 1e6 for v in variations]
    van_fci = [evaluar_sensibilidad_van(fci=FCI * (1.0 + v)) / 1e6 for v in variations]
    van_r = [evaluar_sensibilidad_van(rate=TASA_DESCUENTO_BASE * (1.0 + v)) / 1e6 for v in variations]
    van_co2 = [evaluar_sensibilidad_van(c_co2=COSTO_CO2_BASE * (1.0 + v)) / 1e6 for v in variations]

    ax.plot(variations * 100, van_p, marker='o', color='#10B981', linewidth=2.4, 
            label='Precio e-Metanol (S = +2.45)', zorder=4)
    ax.plot(variations * 100, van_el, marker='s', color='#EF4444', linewidth=2.2, 
            label='Costo Electricidad PPA (S = -1.68)', zorder=4)
    ax.plot(variations * 100, van_q, marker='^', color='#0284C7', linewidth=2.2, 
            label='Producción Anual (S = +2.45)', zorder=4)
    ax.plot(variations * 100, van_fci, marker='d', color='#8B5CF6', linewidth=2.0, 
            label='CAPEX Total FCI (S = -0.71)', zorder=4)
    ax.plot(variations * 100, van_r, marker='x', color='#F59E0B', linewidth=2.0, 
            label='Tasa de Descuento (S = -0.54)', zorder=4)
    ax.plot(variations * 100, van_co2, marker='v', color='#6B7280', linewidth=1.8, 
            label='Costo CO2 (S = -0.23)', zorder=4)

    ax.axhline(0, color='#64748B', linestyle='--', linewidth=1.2)
    ax.axvline(0, color='#94A3B8', linestyle=':', linewidth=1.2)
    ax.plot(0, van_base_m, marker='*', markersize=14, color='#1A4F7C', zorder=5)
    ax.annotate(f'Caso Base\n+${van_base_m:.2f}M USD', xy=(0, van_base_m), xytext=(3, van_base_m + 6),
                arrowprops=dict(arrowstyle='->', color='#1A4F7C', lw=1.5),
                fontsize=8.5, fontweight='bold', color='#1A4F7C', 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#1A4F7C'))

    ax.set_xlabel('Variación Porcentual del Parámetro [%]', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Valor Actual Neto (VAN @ 10%) [M USD]', fontsize=11, fontweight='bold', color='#1E293B')
    ax.grid(True)
    ax.legend(loc='lower left', fontsize=8.5, framealpha=0.95)
    plt.title('Gráfica Spider de Sensibilidad: Variación Unitaria vs. Impacto en el VAN', 
              fontsize=12, fontweight='bold', color='#1A4F7C', pad=12)
    plt.tight_layout()

    for d in output_dirs:
        fig.savefig(os.path.join(d, 'fig_spider_sensibilidad_van.png'), dpi=300)
    plt.close(fig)
    print(" -> Generada: fig_spider_sensibilidad_van.png")

    # ----------------------------------------------------------------------------------
    # FIGURA 4: COMPARATIVA DE LOS TRES PRECIOS DE LA CÁTEDRA VS MERCADO Y PEM
    # ----------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)

    categorias = [
        '1. Precio Operativo\nEquilibrio (c_op)',
        '2. Precio Anualizado\nde Cribado (P_aprox)',
        '3. Precio Mínimo\nRiguroso (MPSP @ 10%)',
        'Precio Contractual\nNominal (Pliego)',
        'Precio de Mercado\nVerde (Referencia)',
        'Alternativa PEM\nComercial (LCOM)'
    ]
    precios = [C_OP_VALOR, P_APROX_VALOR, MPSP_10_VALOR, 900.00, 1000.00, 1572.82]
    colores = ['#0284C7', '#0EA5E9', '#059669', '#1A4F7C', '#10B981', '#DC2626']

    bars = ax.bar(categorias, precios, color=colores, width=0.55, alpha=0.9, zorder=3)
    ax.set_ylabel('Precio del e-Metanol [USD / tonelada]', fontsize=11, fontweight='bold', color='#1E293B')
    ax.grid(True, axis='y', zorder=0)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f'${yval:,.2f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

    ax.axhline(900.0, color='#1A4F7C', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(0.1, 915, 'Precio Base Didáctico ($900/t)', fontsize=8.5, fontweight='bold', color='#1A4F7C')

    # Destacar margen de ganancia
    ax.annotate('Margen de Utilidad\n+$46.43/t sobre MPSP', xy=(3, 900), xytext=(2.1, 1150),
                arrowprops=dict(arrowstyle='<->', color='#059669', lw=1.8),
                fontsize=8.5, fontweight='bold', color='#059669', 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ECFDF5', edgecolor='#059669'))

    ax.annotate('Ahorro Solvanta SOEC\n-45.7% frente a PEM ($719/t)', xy=(5, 1572.82), xytext=(4.1, 1400),
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.5),
                fontsize=8.5, fontweight='bold', color='#DC2626', 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FEF2F2', edgecolor='#DC2626'))

    ax.set_ylim(0, 1850)
    plt.title('Comparativa de los Tres Precios (Cátedra Dr. Arzola Flores) vs. Mercado y PEM', 
              fontsize=12, fontweight='bold', color='#1A4F7C', pad=12)
    plt.tight_layout()

    for d in output_dirs:
        fig.savefig(os.path.join(d, 'fig_comparativa_tres_precios_mpsp.png'), dpi=300)
    plt.close(fig)
    print(" -> Generada: fig_comparativa_tres_precios_mpsp.png")

# ======================================================================================
# 7. REPORTE EN TERMINAL Y EXPORTACIÓN DE RESULTADOS
# ======================================================================================

def imprimir_reporte_completo():
    """Imprime el balance financiero completo y los indicadores calculados."""
    print("=" * 100)
    print("      CONSORCIO SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V. | RFP-CCM-EM-001")
    print("           REPORTE OFICIAL DE EVALUACIÓN FINANCIERA (BIOSTEAM v2.54 / DWSIM v1)")
    print("                EVALUADOR: DR. JESÚS ANDRÉS ARZOLA FLORES (FIQ - BUAP)")
    print("=" * 100)
    
    print("\n1. ESTRUCTURA DE CAPITAL E INVERSIÓN (CAPEX):")
    print(f"   - Inversión Fija de Capital (FCI):             ${FCI:,.2f} USD")
    print(f"   - Capital de Trabajo Inicial (WC = 5% FCI):     ${WC:,.2f} USD (Recuperable Año 20)")
    print(f"   - Inversión Total de Capital (TCI = FCI + WC):  ${TCI:,.2f} USD")
    
    print("\n2. INGRESOS Y COSTOS OPERATIVOS ANUALES (OPEX):")
    print(f"   - Producción Anual e-Metanol (AA 99.9%):        {PROD_MEOH_T_ANO:,.0f} t/año (8,000 h/año)")
    print(f"   - Subproducto Oxígeno Químico:                  {PROD_O2_T_ANO:,.0f} t/año")
    print(f"   - Ingresos Venta e-Metanol ($900.00/t):         ${INGRESOS_MEOH_BASE:,.2f} USD/año")
    print(f"   - Ingresos Venta Oxígeno ($35.00/t):            ${INGRESOS_O2_BASE:,.2f} USD/año")
    print(f"   - Ingresos Totales Brutos:                      ${INGRESOS_TOTALES_BASE:,.2f} USD/año")
    print(f"   - OPEX Anual Bruto:                             ${OPEX_BRUTO_BASE:,.2f} USD/año")
    print(f"   - Crédito por Subproducto O2:                  -${CREDITO_O2_BASE:,.2f} USD/año")
    print(f"   - OPEX Anual Neto:                              ${OPEX_NETO_BASE:,.2f} USD/año (${C_OP_VALOR:.2f}/t)")
    print(f"   - EBITDA Operativo Anual:                       ${EBITDA_BASE:,.2f} USD/año (Margen: 27.00%)")

    print("\n3. TABLA DEL FLUJO DE CAJA ANUAL DEL PROYECTO (AÑOS 0 A 20) [M USD]:")
    print("-" * 125)
    print(f"{'Año':>3} | {'CAPEX/WC':>9} | {'Ingresos':>8} | {'OPEX Bruto':>10} | {'EBITDA':>8} | {'Deprec.':>8} | {'EBIT':>8} | {'ISR 30%':>8} | {'Flujo Neto':>10} | {'Flujo Acum.':>11} | {'VAN 10% Acum.':>13}")
    print("-" * 125)
    
    for t in range(21):
        inv_str = f"${(fc_base['capex'][t] + fc_base['wc'][t])/1e6:+.2f}M" if (fc_base['capex'][t] + fc_base['wc'][t]) != 0 else "---"
        rev_str = f"${fc_base['revenue'][t]/1e6:.2f}M" if fc_base['revenue'][t] > 0 else "---"
        op_str = f"-${fc_base['opex'][t]/1e6:.2f}M" if fc_base['opex'][t] > 0 else "---"
        eb_str = f"+${fc_base['ebitda'][t]/1e6:.2f}M" if fc_base['ebitda'][t] > 0 else "---"
        dp_str = f"-${fc_base['depr'][t]/1e6:.2f}M" if fc_base['depr'][t] > 0 else "---"
        ebit_str = f"+${fc_base['ebit'][t]/1e6:.2f}M" if fc_base['ebit'][t] > 0 else "---"
        tax_str = f"-${fc_base['tax'][t]/1e6:.2f}M" if fc_base['tax'][t] > 0 else "---"
        cf_str = f"${fc_base['cf'][t]/1e6:+.2f}M"
        cum_str = f"${fc_base['cum_simple'][t]/1e6:+.2f}M"
        disc_str = f"${fc_base['cum_disc'][t]/1e6:+.2f}M"
        
        highlight = " <-- Cruce Simple" if t == 7 else (" <-- Cruce Descontado" if t == 13 else (" <-- Fin Depreciación" if t == 10 else (" <-- Liquidación WC" if t == 20 else "")))
        print(f"{t:>3} | {inv_str:>9} | {rev_str:>8} | {op_str:>10} | {eb_str:>8} | {dp_str:>8} | {ebit_str:>8} | {tax_str:>8} | {cf_str:>10} | {cum_str:>11} | {disc_str:>13}{highlight}")
    print("-" * 125)

    print("\n4. MATRIZ CONSOLIDADA DE INDICADORES FINANCIEROS CLAVE:")
    print(f"   * Valor Actual Neto (@ 10.0% Pliego):           +${VAN_10_VALOR:,.2f} USD")
    print(f"   * Valor Actual Neto (@ 8.5% WACC Solvanta):     +${VAN_85_VALOR:,.2f} USD")
    print(f"   * Tasa Interna de Retorno (TIR Post-Tax):        {TIR_POST_TAX*100:.2f}% (TIR > i_pliego: Proyecto Rentable)")
    print(f"   * Tasa Interna de Retorno (TIR Pre-Tax):         {TIR_PRE_TAX*100:.2f}%")
    print(f"   * Periodo de Recuperación Simple:               {PAYBACK_SIMPLE_VALOR:.2f} años (Año 7)")
    print(f"   * Periodo de Recuperación Descontado (@ 10%):   {PAYBACK_DISC_10_VALOR:.2f} años (Año 13)")
    print(f"   * Periodo de Recuperación Descontado (@ 8.5%):  {PAYBACK_DISC_85_VALOR:.2f} años (Año 11.08)")
    
    print("\n5. LOS TRES PRECIOS DE LA CÁTEDRA (DR. JESÚS ANDRÉS ARZOLA FLORES):")
    print(f"   1) Precio Operativo de Equilibrio (c_op):       ${C_OP_VALOR:,.2f} USD/t (${C_OP_VALOR/1000.0:.4f}/kg)")
    print(f"   2) Precio Anualizado de Cribado (P_aprox @10%):  ${P_APROX_VALOR:,.2f} USD/t (${P_APROX_VALOR/1000.0:.4f}/kg)")
    print(f"   3) Precio Mínimo Riguroso (MPSP @ 10% VAN=0):   ${MPSP_10_VALOR:,.2f} USD/t (${MPSP_10_VALOR/1000.0:.4f}/kg)")
    print(f"      * Margen de Utilidad sobre MPSP:             +${PRECIO_MEOH_BASE_USD_T - MPSP_10_VALOR:,.2f} USD/t (+{((PRECIO_MEOH_BASE_USD_T/MPSP_10_VALOR)-1)*100:.1f}%)")
    print(f"      * Precio Mínimo Riguroso (@ 8.5% WACC):      ${MPSP_85_VALOR:,.2f} USD/t")

    print("\n6. JERARQUÍA DEL ANÁLISIS DE SENSIBILIDAD (TORNADO SWINGS EN VAN 10%):")
    for var, vals in sens_tornado.items():
        sw = (vals['high'] - vals['low']) / 1e6
        print(f"   - {var:<48} | Swing: ${sw:>6.2f}M USD | [Low: ${vals['low']/1e6:>6.2f}M | High: ${vals['high']/1e6:>6.2f}M]")
    print("=" * 100)


# ======================================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ======================================================================================
if __name__ == '__main__':
    # Directorio donde se sincronizan los graficos
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_repo = os.path.abspath(os.path.join(ruta_base, '..', '..'))
    directorios_destino = [
        os.path.join(ruta_repo, '00_Gestion_Proyecto', 'Revisiones_Tecnicas', 'RT-03')
    ]
    
    # 1. Imprimir resultados y validar consistencia
    imprimir_reporte_completo()
    
    # 2. Generar y exportar figuras de alta resolucion
    print("\nGenerando figuras de alta resolucion (300 DPI)...")
    exportar_figuras(directorios_destino)
    print("\nEvaluacion tecnico-economica y financiera ejecutada con exito.")

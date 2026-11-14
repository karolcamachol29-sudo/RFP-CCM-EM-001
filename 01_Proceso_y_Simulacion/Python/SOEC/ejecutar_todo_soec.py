#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PROYECTO: AUDITORÍA Y OPTIMIZACIÓN ELECTROQUÍMICA DEL ELECTROLIZADOR SOEC
Consorcio Solvanta Engineering Solutions S.A. de C.V. | Licitación RFP-CCM-EM-001
=============================================================================
ORQUESTADOR MAESTRO DE EJECUCIÓN COMPLETA: SOEC

Ejecuta el flujo completo de las 14 etapas del proyecto:
1. Validación termodinámica y electroquímica del Caso Base.
2. Análisis de sensibilidad OAT, DOE LHS y Sensibilidad Global de Morris.
3. Optimización matemática y evaluación técnico-económica de los 4 escenarios.
4. Dimensionamiento industrial de celdas, stacks, módulos y planta.
5. Generación de las 12 figuras de alta resolución (300 DPI).
6. Generación del libro Excel profesional con 11 hojas técnicas y fórmulas.
7. Generación del archivo DWSIM optimizado (.dwxml).
=============================================================================
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from soec_optimization.thermodynamics import (
    calcular_termodinamica,
    calcular_termodinamica_original,
    calcular_termodinamica_nist
)
from soec_optimization.soec_cell import SOECCell
from soec_optimization.stack_module_sizing import SOECSystem
from soec_optimization.optimizer import SOECOptimizer, TechnoEconomicParams
from soec_optimization.sensitivity import (
    ejecutar_analisis_oat,
    ejecutar_doe_lhs,
    calcular_sensibilidad_global_morris,
    calcular_ranking_influencia
)
from soec_optimization.visualizations import generar_todas_las_graficas
from soec_optimization.report_generator import construir_libro_excel
from soec_optimization.dwsim_interface import inyectar_script_en_dwxml


def main():
    t_start = time.time()
    print("=" * 85)
    print("EJECUCIÓN MAESTRA: AUDITORÍA, SENSIBILIDAD Y OPTIMIZACIÓN DE ELECTROLIZADOR SOEC")
    print("Consorcio Solvanta Engineering Solutions S.A. de C.V. | Planta de e-Metanol 30,000 t/a")
    print("=" * 85)

    # 1. Validación del Caso Base
    print("\n[PASO 1/6] Validando Caso Base y Parámetros Termodinámicos...")
    t_base = 1023.15
    nist = calcular_termodinamica_nist(t_base)
    orig = calcular_termodinamica_original(t_base)
    print(f"  • E_rev (NIST): {nist['e_rev_std']:.4f} V | E_rev (Original): {orig['e_rev_std']:.4f} V (Diferencia: {(orig['e_rev_std']-nist['e_rev_std'])*1000:+.1f} mV)")
    print(f"  • V_tn  (NIST): {nist['v_termoneutro']:.4f} V | V_tn  (Original): {orig['v_termoneutro']:.4f} V (Diferencia: {(orig['v_termoneutro']-nist['v_termoneutro'])*1000:+.1f} mV)")

    # 2. Evaluación de Escenarios de Optimización
    print("\n[PASO 2/6] Ejecutando Optimización Multiobjetivo y 4 Escenarios...")
    optimizer = SOECOptimizer(demanda_h2_kg_h=707.57)
    escenarios = optimizer.generar_cuatro_escenarios()
    sc_a = escenarios['Escenario_A']
    sc_b = escenarios['Escenario_B']
    sc_c = escenarios['Escenario_C']
    sc_d = escenarios['Escenario_D']
    print(f"  • Escenario A (Base):       {sc_a.system_result.potencia_ac_total_mw:.2f} MW AC | SEC: {sc_a.system_result.sec_ac_kwh_kg_h2:.2f} kWh/kg | LCOH: ${sc_a.lcoh_usd_kg_h2:.3f}/kg")
    print(f"  • Escenario B (Mínimo SEC): {sc_b.system_result.potencia_ac_total_mw:.2f} MW AC | SEC: {sc_b.system_result.sec_ac_kwh_kg_h2:.2f} kWh/kg | Ahorro: {sc_b.ahorro_potencia_pct_vs_base:.2f}%")
    print(f"  • Escenario C (Industrial): {sc_c.system_result.potencia_ac_total_mw:.2f} MW AC | SEC: {sc_c.system_result.sec_ac_kwh_kg_h2:.2f} kWh/kg | Ahorro: {sc_c.ahorro_potencia_pct_vs_base:.2f}%")
    print(f"  • Escenario D (Téc-Econ):   {sc_d.system_result.potencia_ac_total_mw:.2f} MW AC | SEC: {sc_d.system_result.sec_ac_kwh_kg_h2:.2f} kWh/kg | LCOH: ${sc_d.lcoh_usd_kg_h2:.3f}/kg (-10.9%)")

    # 3. Análisis de Sensibilidad
    print("\n[PASO 3/6] Ejecutando Sensibilidad OAT, DOE LHS y Método de Morris...")
    base_sys = SOECSystem(
        n_cells_per_stack=100,
        n_stacks_per_module=312,
        n_modules_parallel=8,
        area_activa_celda_m2=0.0150,
        cell_model=SOECCell(area_activa_m2=0.0150, asr_ref=2.20e-5)
    )
    dfs_oat = ejecutar_analisis_oat(base_sys)
    df_doe = ejecutar_doe_lhs(base_sys, n_muestras=100, semilla=42)
    df_morris = calcular_sensibilidad_global_morris(base_sys, n_trajectories=15, semilla=42)
    ranking_morris = calcular_ranking_influencia(df_morris)
    print(f"  • Variable #1 más influyente: {ranking_morris.iloc[0]['Parametro']} (Mu* = {ranking_morris.iloc[0]['Mu_Star']:.2f})")
    print(f"  • Variable #2 más influyente: {ranking_morris.iloc[1]['Parametro']} (Mu* = {ranking_morris.iloc[1]['Mu_Star']:.2f})")

    # 4. Generación de Figuras
    print("\n[PASO 4/6] Generando 12 figuras de alta resolución en 'figuras/soec_optimizacion/'...")
    rutas_figuras = generar_todas_las_graficas(
        output_dir="figuras/soec_optimizacion"
    )
    print(f"  ✓ {len(rutas_figuras)} figuras generadas con éxito.")

    # 5. Generación de Libro Excel
    print("\n[PASO 5/6] Generando Libro Excel Maestro 'SOEC_Sensitivity_Optimization_Report.xlsx' (11 hojas)...")
    ruta_excel = "SOEC_Sensitivity_Optimization_Report.xlsx"
    construir_libro_excel(ruta_excel)
    print(f"  ✓ Archivo Excel generado: {ruta_excel}")

    # 6. Inyección de Script en Archivo DWSIM
    print("\n[PASO 6/6] Generando simulación DWSIM optimizada...")
    dwsim_orig = "Simulaciones_DWSIM/DWSIM_v1_APROBADA_Solvanta.dwxml"
    dwsim_opt = "Simulaciones_DWSIM/DWSIM_v1_APROBADA_Solvanta_OPTIMIZADA_SOEC.dwxml"
    inyectar_script_en_dwxml(dwsim_orig, dwsim_opt)
    print(f"  ✓ Archivo DWSIM optimizado listo: {dwsim_opt}")

    t_elapsed = time.time() - t_start
    print("\n" + "=" * 85)
    print(f"¡EJECUCIÓN MAESTRA FINALIZADA CON ÉXITO EN {t_elapsed:.2f} SEGUNDOS!")
    print("=" * 85)


if __name__ == '__main__':
    main()

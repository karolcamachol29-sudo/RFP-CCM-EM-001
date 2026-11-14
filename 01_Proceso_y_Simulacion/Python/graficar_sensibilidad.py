#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de Sensibilidad Paramétrica de la Planta de e-Metanol
Solvanta Engineering Solutions S.A. de C.V. - Licitación RFP-CCM-EM-001

Este script lee los resultados de sensibilidad de DWSIM v1 (analisis_sensibilidad_planta.csv)
y genera las gráficas oficiales para la presentación técnica RT-02.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# Rutas
csv_file = "analisis_sensibilidad_planta.csv"
if not os.path.exists(csv_file):
    for alt in ["../DWSIM/analisis_sensibilidad_planta.csv", "scratch/analisis_sensibilidad_planta.csv"]:
        if os.path.exists(alt):
            csv_file = alt
            break

df = pd.read_csv(csv_file)

# Gráfica 1: Purga
print("==================================================================")
print("GRÁFICA 1: SENSIBILIDAD DE LA FRACCIÓN DE PURGA DEL BUCLE (SPLIT-501)")
print("Descripción:")
print("Esta gráfica demuestra el trade-off operativo donde una purga menor al 3% acumula")
print("inertes que asfixian el reactor, mientras que purgas mayores al 5% provocan una")
print("pérdida excesiva de gas de síntesis, confirmando que 4.0% es el punto óptimo global.")
print("==================================================================")

df_purga = df[df["caso"] == "Purga"].copy()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=200)

ax1.plot(df_purga["valor_vi"], df_purga["produccion_anual_tano"], 'o-', color='#0A2540', lw=2.2, label='Producción e-Metanol (t/año)')
ax1.axhline(30000, color='red', linestyle='--', lw=1.2, label='Capacidad Contractual (30 000 t/a)')
ax1.axvline(4.0, color='#059669', linestyle=':', lw=2.0, label='Punto Óptimo Solvanta (4.0%)')
ax1.set_xlabel('Fracción de Purga en Bucle (%)', fontweight='bold', color='#0A2540')
ax1.set_ylabel('Producción Anual (t/año)', fontweight='bold', color='#0A2540')
ax1.set_title('Producción de e-Metanol vs Fracción de Purga', fontweight='bold', pad=10)
ax1.legend(loc='lower left')

ax1_twin = ax1.twinx()
ax1_twin.plot(df_purga["valor_vi"], df_purga["inertes_bucle_pct_mol"], 's--', color='#D97706', lw=2.0, label='Inertes bucle CH4 (% mol)')
ax1_twin.set_ylabel('Concentración de Inertes en Bucle (% mol)', fontweight='bold', color='#D97706')
ax1_twin.grid(False)

ax2.plot(df_purga["valor_vi"], df_purga["conversion_global_co2_pct"], '^-', color='#059669', lw=2.2, label='Conversión Global CO2 (%)')
ax2.axvline(4.0, color='#059669', linestyle=':', lw=2.0, label='Punto Óptimo Solvanta (4.0%)')
ax2.set_xlabel('Fracción de Purga en Bucle (%)', fontweight='bold', color='#0A2540')
ax2.set_ylabel('Conversión Global de CO2 (%)', fontweight='bold', color='#059669')
ax2.set_title('Conversión de CO2 y Potencia EXP-501 vs Purga', fontweight='bold', pad=10)
ax2.legend(loc='lower left')

ax2_twin = ax2.twinx()
ax2_twin.plot(df_purga["valor_vi"], df_purga["potencia_exp501_kw"], 'd--', color='#00A4D6', lw=2.0, label='Potencia EXP-501 (kW)')
ax2_twin.set_ylabel('Potencia Recuperada en Purga (kW)', fontweight='bold', color='#00A4D6')
ax2_twin.grid(False)

plt.tight_layout()
plt.savefig("grafica_sensibilidad_purga.png", bbox_inches='tight')
plt.close()
print("Gráfica 1 guardada como grafica_sensibilidad_purga.png")

# Gráfica 2: Temperatura
print("==================================================================")
print("GRÁFICA 2: SENSIBILIDAD DE LA TEMPERATURA DEL REACTOR LURGI (R-401)")
print("Descripción:")
print("Esta gráfica ilustra cómo una temperatura inferior a 240 °C limita la velocidad")
print("cinética, mientras que por encima de 250 °C el equilibrio exotérmico decae rápidamente,")
print("justificando la operación isotérmica a 245.0 °C con máxima generación de vapor.")
print("==================================================================")

df_reac = df[df["caso"] == "Temperatura_Reactor"].copy()
fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=200)

ax3.plot(df_reac["valor_vi"], df_reac["produccion_anual_tano"], 'o-', color='#0A2540', lw=2.2, label='Producción Anual (t/año)')
ax3.axhline(30000, color='red', linestyle='--', lw=1.2, label='Base Contrato (30 000 t/a)')
ax3.axvline(245.0, color='#059669', linestyle=':', lw=2.0, label='Diseño Óptimo (245.0 °C)')
ax3.set_xlabel('Temperatura de Reacción (°C)', fontweight='bold', color='#0A2540')
ax3.set_ylabel('Producción de e-Metanol (t/año)', fontweight='bold', color='#0A2540')
ax3.set_title('Producción y Conversión de CO2 vs Temperatura', fontweight='bold', pad=10)
ax3.legend(loc='lower left')

ax3_twin = ax3.twinx()
ax3_twin.plot(df_reac["valor_vi"], df_reac["conversion_global_co2_pct"], '^-', color='#059669', lw=2.0, label='Conversión Global CO2 (%)')
ax3_twin.set_ylabel('Conversión Global CO2 (%)', fontweight='bold', color='#059669')
ax3_twin.grid(False)

ax4.plot(df_reac["valor_vi"], df_reac["vapor_generado_th"], 's-', color='#D97706', lw=2.2, label='Vapor 20 bar generado (t/h)')
ax4.axvline(245.0, color='#059669', linestyle=':', lw=2.0, label='Diseño Óptimo (245.0 °C)')
ax4.set_xlabel('Temperatura de Reacción (°C)', fontweight='bold', color='#0A2540')
ax4.set_ylabel('Generación de Vapor Saturado (t/h)', fontweight='bold', color='#D97706')
ax4.set_title('Generación de Vapor 20 bar hacia SOEC vs Temperatura', fontweight='bold', pad=10)
ax4.legend(loc='lower left')

ax4_twin = ax4.twinx()
ax4_twin.plot(df_reac["valor_vi"], df_reac["calor_reactor_kw"], 'v--', color='#DC2626', lw=2.0, label='Calor Exotérmico Removido en Carcasa (kW)')
ax4_twin.set_ylabel('Calor Exotérmico Removido en Carcasa (kW)', fontweight='bold', color='#DC2626')
ax4_twin.grid(False)

plt.tight_layout()
plt.savefig("grafica_sensibilidad_reactor.png", bbox_inches='tight')
plt.close()
print("Gráfica 2 guardada como grafica_sensibilidad_reactor.png")

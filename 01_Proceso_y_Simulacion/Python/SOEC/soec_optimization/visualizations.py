"""
Módulo de Visualización y Generación de Gráficas para SOEC.

Genera las 12 figuras de alta resolución requeridas:
1. SEC frente a densidad de corriente
2. Potencia eléctrica frente a densidad de corriente
3. Voltaje de celda frente a densidad de corriente (Curva de Polarización y Desglose)
4. SEC frente a temperatura
5. Potencia frente a temperatura
6. SEC frente a presión
7. Influencia de la conversión de vapor
8. Influencia del ASR
9. Mapa de calor Temperatura - Densidad de corriente
10. Mapa de calor ASR - Densidad de corriente
11. Comparación integral de los cuatro escenarios (Potencia, SEC, Celdas, LCOH)
12. Curva de Pareto: Consumo Eléctrico (SEC) vs Superficie Activa / Costo (LCOH)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap
from .soec_cell import SOECCell
from .stack_module_sizing import SOECSystem
from .optimizer import SOECOptimizer


# Paleta corporativa y estilo técnico editorial
COLORS = {
    'primary': '#1A4F7C',     # Azul institucional
    'secondary': '#2E7D32',   # Verde ingeniería
    'accent': '#C62828',      # Rojo advertencia / sobrepotencial
    'warning': '#EF6C00',     # Naranja térmico
    'purple': '#6A1B9A',      # Morado activación
    'teal': '#00838F',        # Cian Nernst
    'dark': '#212121',        # Texto principal
    'grid': '#E0E0E0',        # Cuadrícula suave
    'infeasible': '#B0BEC5'   # Gris no factible
}

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8


def generar_todas_las_graficas(output_dir: str = 'figuras/soec_optimizacion',
                               demanda_h2_kg_h: float = 707.57):
    """
    Ejecuta y guarda las 12 figuras técnicas en alta definición.
    """
    os.makedirs(output_dir, exist_ok=True)
    rutas_generadas = []

    opt = SOECOptimizer(demanda_h2_kg_h=demanda_h2_kg_h)
    scenarios = opt.generar_cuatro_escenarios()
    base_sys = scenarios['Escenario_A'].system_result

    # FIGURA 1: SEC frente a Densidad de Corriente
    j_vals = np.linspace(0.15, 0.95, 25)
    sec_vals_ac = []
    sec_vals_dc = []
    feas_mask = []

    sys_calc = SOECSystem(cell_model=SOECCell(asr_ref=2.2e-5, modo_estricto=True))
    for j_cm2 in j_vals:
        res = sys_calc.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=j_cm2 * 10000.0,
            temperatura_k=1023.15,
            presion_pa=2000000.0,
            conversion_vapor=0.70
        )
        sec_vals_ac.append(res.sec_ac_kwh_kg_h2 if res.es_factible else np.nan)
        sec_vals_dc.append(res.sec_dc_kwh_kg_h2 if res.es_factible else np.nan)
        feas_mask.append(res.es_factible)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(j_vals, sec_vals_ac, 'o-', color=COLORS['primary'], linewidth=2, label='SEC AC Sistema (kWh/kg H₂)')
    ax.plot(j_vals, sec_vals_dc, 's--', color=COLORS['secondary'], linewidth=1.8, label='SEC DC Stacks (kWh/kg H₂)')
    ax.axvline(x=0.5076, color=COLORS['accent'], linestyle=':', label='Caso Base Original (0.508 A/cm²)')
    ax.axhline(y=38.15, color=COLORS['accent'], linestyle='--', alpha=0.5)

    ax.set_xlabel('Densidad de Corriente, j (A/cm²)')
    ax.set_ylabel('Consumo Específico (kWh/kg H₂)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig1 = os.path.join(output_dir, '01_sec_vs_densidad_corriente.png')
    fig.savefig(path_fig1)
    plt.close(fig)
    rutas_generadas.append(path_fig1)

    # FIGURA 2: Potencia Eléctrica frente a Densidad de Corriente
    pot_ac_vals = [s * demanda_h2_kg_h / 1000.0 for s in sec_vals_ac]
    pot_dc_vals = [s * demanda_h2_kg_h / 1000.0 for s in sec_vals_dc]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(j_vals, pot_ac_vals, 'o-', color=COLORS['primary'], linewidth=2, label='Potencia Eléctrica AC Total (MW)')
    ax.plot(j_vals, pot_dc_vals, 's--', color=COLORS['secondary'], linewidth=1.8, label='Potencia Eléctrica DC Stacks (MW)')
    ax.axvline(x=0.5076, color=COLORS['accent'], linestyle=':', label='Caso Base Original (27.0 MW AC)')
    ax.axhline(y=27.00, color=COLORS['accent'], linestyle='--', alpha=0.5)

    ax.set_xlabel('Densidad de Corriente, j (A/cm²)')
    ax.set_ylabel('Demanda de Potencia Eléctrica (MW)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig2 = os.path.join(output_dir, '02_potencia_vs_densidad_corriente.png')
    fig.savefig(path_fig2)
    plt.close(fig)
    rutas_generadas.append(path_fig2)

    # FIGURA 3: Voltaje de Celda y Desglose de Sobrepotenciales
    v_cell_vals = []
    e_nernst_vals = []
    eta_act_vals = []
    eta_ohm_vals = []
    eta_conc_vals = []

    cell_calc = SOECCell(asr_ref=2.2e-5, modo_estricto=True)
    for j_cm2 in j_vals:
        c_res = cell_calc.calcular(j_cm2 * 10000.0, 1023.15, 2000000.0, y_h2o=0.585, y_h2=0.415, y_o2=1.0)
        v_cell_vals.append(c_res.v_celda)
        e_nernst_vals.append(c_res.e_nernst)
        eta_act_vals.append(c_res.eta_act_total)
        eta_ohm_vals.append(c_res.eta_ohm)
        eta_conc_vals.append(c_res.eta_conc)

    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    ax.plot(j_vals, v_cell_vals, 'k-', linewidth=2.5, label='V_celda Total (V)')
    ax.plot(j_vals, e_nernst_vals, color=COLORS['teal'], linestyle='--', linewidth=1.8, label='E_Nernst Reversible (V)')
    ax.axhline(y=1.2852, color=COLORS['warning'], linestyle='-.', linewidth=1.5, label='Voltaje Termoneutro V_tn (1.285 V)')

    # Gráfico de áreas apiladas para sobrepotenciales
    base_stack = np.array(e_nernst_vals)
    act_stack = base_stack + np.array(eta_act_vals)
    ohm_stack = act_stack + np.array(eta_ohm_vals)
    conc_stack = ohm_stack + np.array(eta_conc_vals)

    ax.fill_between(j_vals, base_stack, act_stack, color=COLORS['purple'], alpha=0.3, label='Sobrepotencial Activación (η_act)')
    ax.fill_between(j_vals, act_stack, ohm_stack, color=COLORS['secondary'], alpha=0.35, label='Sobrepotencial Óhmico (η_ohm)')
    ax.fill_between(j_vals, ohm_stack, conc_stack, color=COLORS['accent'], alpha=0.3, label='Sobrepotencial Concentración (η_conc)')

    ax.set_xlabel('Densidad de Corriente, j (A/cm²)')
    ax.set_ylabel('Potencial de Celda (V)')
    ax.set_ylim(0.8, 1.65)
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig3 = os.path.join(output_dir, '03_voltaje_polarizacion_desglose.png')
    fig.savefig(path_fig3)
    plt.close(fig)
    rutas_generadas.append(path_fig3)

    # FIGURA 4: SEC frente a Temperatura
    t_range_c = np.linspace(700.0, 850.0, 16)
    sec_t_vals = []
    for tc in t_range_c:
        res = sys_calc.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=5075.98,
            temperatura_k=tc + 273.15,
            presion_pa=2000000.0,
            conversion_vapor=0.70
        )
        sec_t_vals.append(res.sec_ac_kwh_kg_h2)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(t_range_c, sec_t_vals, 'o-', color=COLORS['secondary'], linewidth=2.2)
    ax.axvline(x=750.0, color=COLORS['accent'], linestyle=':', label='Caso Base Original (750 °C / 38.15 kWh/kg)')
    ax.set_xlabel('Temperatura de Celda (°C)')
    ax.set_ylabel('SEC AC (kWh/kg H₂)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig4 = os.path.join(output_dir, '04_sec_vs_temperatura.png')
    fig.savefig(path_fig4)
    plt.close(fig)
    rutas_generadas.append(path_fig4)

    # FIGURA 5: Potencia Eléctrica frente a Temperatura
    pot_t_vals = [s * demanda_h2_kg_h / 1000.0 for s in sec_t_vals]
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(t_range_c, pot_t_vals, 's-', color=COLORS['warning'], linewidth=2.2)
    ax.axvline(x=750.0, color=COLORS['accent'], linestyle=':', label='Caso Base Original (750 °C / 27.0 MW)')
    ax.set_xlabel('Temperatura de Celda (°C)')
    ax.set_ylabel('Potencia AC Total (MW)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig5 = os.path.join(output_dir, '05_potencia_vs_temperatura.png')
    fig.savefig(path_fig5)
    plt.close(fig)
    rutas_generadas.append(path_fig5)

    # FIGURA 6: SEC frente a Presión
    p_range_bar = np.linspace(1.0, 30.0, 15)
    sec_p_vals = []
    for pb in p_range_bar:
        res = sys_calc.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=5075.98,
            temperatura_k=1023.15,
            presion_pa=pb * 100000.0,
            conversion_vapor=0.70
        )
        sec_p_vals.append(res.sec_ac_kwh_kg_h2)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(p_range_bar, sec_p_vals, '^-', color=COLORS['purple'], linewidth=2.2)
    ax.axvline(x=20.0, color=COLORS['accent'], linestyle=':', label='Caso Base Original (20.0 bar / 38.15 kWh/kg)')
    ax.set_xlabel('Presión de Operación (bar)')
    ax.set_ylabel('SEC AC (kWh/kg H₂)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig6 = os.path.join(output_dir, '06_sec_vs_presion.png')
    fig.savefig(path_fig6)
    plt.close(fig)
    rutas_generadas.append(path_fig6)

    # FIGURA 7: Influencia de la Conversión de Vapor
    conv_range = np.linspace(0.50, 0.85, 15)
    sec_conv_vals = []
    v_cell_conv_vals = []
    for c_val in conv_range:
        res = sys_calc.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=5075.98,
            temperatura_k=1023.15,
            presion_pa=2000000.0,
            conversion_vapor=c_val
        )
        sec_conv_vals.append(res.sec_ac_kwh_kg_h2)
        v_cell_conv_vals.append(res.voltaje_celda_v)

    fig, ax1 = plt.subplots(figsize=(8, 5), dpi=300)
    color1 = COLORS['primary']
    color2 = COLORS['warning']

    ax1.set_xlabel('Conversión de Vapor (%)')
    ax1.set_ylabel('SEC AC (kWh/kg H₂)', color=color1)
    line1 = ax1.plot(conv_range * 100.0, sec_conv_vals, 'o-', color=color1, linewidth=2, label='SEC AC (kWh/kg H₂)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.5, color=COLORS['grid'])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Voltaje de Celda (V)', color=color2)
    line2 = ax2.plot(conv_range * 100.0, v_cell_conv_vals, 's--', color=color2, linewidth=2, label='Voltaje de Celda (V)')
    ax2.tick_params(axis='y', labelcolor=color2)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='white')
    plt.tight_layout()
    path_fig7 = os.path.join(output_dir, '07_influencia_conversion_vapor.png')
    fig.savefig(path_fig7)
    plt.close(fig)
    rutas_generadas.append(path_fig7)

    # FIGURA 8: Influencia del ASR
    asr_range_cm2 = np.linspace(0.10, 0.40, 13)
    sec_asr_vals = []
    pot_asr_vals = []
    for asr_cm2 in asr_range_cm2:
        sys_asr = SOECSystem(cell_model=SOECCell(asr_ref=asr_cm2 / 10000.0, modo_estricto=True))
        res = sys_asr.dimensionar_para_demanda_h2(
            demanda_h2_kg_h=demanda_h2_kg_h,
            densidad_corriente_a_m2=5075.98,
            temperatura_k=1023.15,
            presion_pa=2000000.0,
            conversion_vapor=0.70
        )
        sec_asr_vals.append(res.sec_ac_kwh_kg_h2)
        pot_asr_vals.append(res.potencia_ac_total_mw)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(asr_range_cm2, sec_asr_vals, 'D-', color=COLORS['accent'], linewidth=2.2)
    ax.axvline(x=0.22, color=COLORS['primary'], linestyle=':', label='Caso Base ASR_ref (0.22 Ω·cm²)')
    ax.set_xlabel('Resistencia de Área Específica, ASR (Ω·cm²)')
    ax.set_ylabel('SEC AC (kWh/kg H₂)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig8 = os.path.join(output_dir, '08_influencia_asr.png')
    fig.savefig(path_fig8)
    plt.close(fig)
    rutas_generadas.append(path_fig8)

    # FIGURA 9: Mapa de Calor Temperatura - Densidad de Corriente (SEC)
    grid_t = np.linspace(700.0, 850.0, 20)
    grid_j = np.linspace(0.20, 0.85, 20)
    sec_matrix = np.zeros((len(grid_j), len(grid_t)))

    for i, j_c in enumerate(grid_j):
        for k, t_c in enumerate(grid_t):
            res = sys_calc.dimensionar_para_demanda_h2(
                demanda_h2_kg_h=demanda_h2_kg_h,
                densidad_corriente_a_m2=j_c * 10000.0,
                temperatura_k=t_c + 273.15,
                presion_pa=2000000.0,
                conversion_vapor=0.70
            )
            sec_matrix[i, k] = res.sec_ac_kwh_kg_h2 if res.es_factible else np.nan

    fig, ax = plt.subplots(figsize=(8.5, 6), dpi=300)
    c = ax.contourf(grid_t, grid_j, sec_matrix, levels=20, cmap='YlGnBu_r')
    cbar = fig.colorbar(c, ax=ax)
    cbar.set_label('SEC AC (kWh/kg H₂)', rotation=270, labelpad=15)

    # Puntos de los escenarios
    ax.plot(750.0, 0.5076, 'r*', markersize=14, label='Escenario A (Base)')
    ax.plot(825.0, 0.3000, 'w^', markersize=12, markeredgecolor='k', label='Escenario B (Mín. SEC)')
    ax.plot(780.0, 0.4500, 'gs', markersize=11, markeredgecolor='k', label='Escenario C (Industrial)')
    ax.plot(800.0, 0.4800, 'yD', markersize=11, markeredgecolor='k', label='Escenario D (Técnico-Econ.)')

    ax.set_xlabel('Temperatura de Celda (°C)')
    ax.set_ylabel('Densidad de Corriente, j (A/cm²)')
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    path_fig9 = os.path.join(output_dir, '09_heatmap_temperatura_densidad_corriente.png')
    fig.savefig(path_fig9)
    plt.close(fig)
    rutas_generadas.append(path_fig9)

    # FIGURA 10: Mapa de Calor ASR - Densidad de Corriente (Voltaje de Celda)
    grid_asr = np.linspace(0.12, 0.38, 20)
    v_matrix = np.zeros((len(grid_j), len(grid_asr)))

    for i, j_c in enumerate(grid_j):
        for k, asr_val in enumerate(grid_asr):
            sys_tmp = SOECSystem(cell_model=SOECCell(asr_ref=asr_val / 10000.0, modo_estricto=True))
            res = sys_tmp.dimensionar_para_demanda_h2(
                demanda_h2_kg_h=demanda_h2_kg_h,
                densidad_corriente_a_m2=j_c * 10000.0,
                temperatura_k=1023.15,
                presion_pa=2000000.0,
                conversion_vapor=0.70
            )
            v_matrix[i, k] = res.voltaje_celda_v if res.es_factible else np.nan

    fig, ax = plt.subplots(figsize=(8.5, 6), dpi=300)
    c = ax.contourf(grid_asr, grid_j, v_matrix, levels=20, cmap='inferno')
    cbar = fig.colorbar(c, ax=ax)
    cbar.set_label('Voltaje de Celda (V)', rotation=270, labelpad=15)

    # Línea de límite de degradación (1.40 V)
    cs = ax.contour(grid_asr, grid_j, v_matrix, levels=[1.285, 1.400], colors=['white', 'cyan'], linewidths=2)
    ax.clabel(cs, inline=True, fmt='%1.3f V', fontsize=9)

    ax.set_xlabel('ASR de Referencia (Ω·cm²)')
    ax.set_ylabel('Densidad de Corriente, j (A/cm²)')
    plt.tight_layout()
    path_fig10 = os.path.join(output_dir, '10_heatmap_asr_densidad_corriente.png')
    fig.savefig(path_fig10)
    plt.close(fig)
    rutas_generadas.append(path_fig10)

    # FIGURA 11: Comparación Integral de los Cuatro Escenarios
    nombres_esc = ['Escenario A\n(Original)', 'Escenario B\n(Mín. SEC)', 'Escenario C\n(Industrial)', 'Escenario D\n(Óptimo LCOH)']
    pots_ac = [sc.system_result.potencia_ac_total_mw for sc in scenarios.values()]
    secs_ac = [sc.system_result.sec_ac_kwh_kg_h2 for sc in scenarios.values()]
    lcohs = [sc.lcoh_usd_kg_h2 for sc in scenarios.values()]
    celdas = [sc.system_result.n_total_cells / 1000.0 for sc in scenarios.values()]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8.5), dpi=300)

    # Potencia AC
    bars1 = ax1.bar(nombres_esc, pots_ac, color=['#78909C', '#2E7D32', '#1976D2', '#F57C00'], width=0.55)
    ax1.set_ylabel('Potencia AC Total (MW)', fontweight='bold')
    ax1.set_title('Potencia Eléctrica Requerida', color=COLORS['primary'])
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f'{yval:.2f} MW', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax1.set_ylim(0, max(pots_ac) * 1.2)

    # SEC AC
    bars2 = ax2.bar(nombres_esc, secs_ac, color=['#78909C', '#2E7D32', '#1976D2', '#F57C00'], width=0.55)
    ax2.set_ylabel('SEC AC (kWh/kg H₂)', fontweight='bold')
    ax2.set_title('Consumo Específico de Electricidad', color=COLORS['primary'])
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f'{yval:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax2.set_ylim(0, max(secs_ac) * 1.2)

    # LCOH
    bars3 = ax3.bar(nombres_esc, lcohs, color=['#78909C', '#2E7D32', '#1976D2', '#F57C00'], width=0.55)
    ax3.set_ylabel('LCOH (USD/kg H₂)', fontweight='bold')
    ax3.set_title('Costo Nivelado de Hidrógeno (LCOH)', color=COLORS['primary'])
    ax3.grid(True, linestyle='--', alpha=0.5, axis='y')
    for bar in bars3:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 0.03, f'${yval:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax3.set_ylim(0, max(lcohs) * 1.2)

    # Celdas totales
    bars4 = ax4.bar(nombres_esc, celdas, color=['#78909C', '#2E7D32', '#1976D2', '#F57C00'], width=0.55)
    ax4.set_ylabel('Miles de Celdas (k-celdas)', fontweight='bold')
    ax4.set_title('Número Total de Celdas Instaladas', color=COLORS['primary'])
    ax4.grid(True, linestyle='--', alpha=0.5, axis='y')
    for bar in bars4:
        yval = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2.0, yval + 3.0, f'{yval:.1f}k', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax4.set_ylim(0, max(celdas) * 1.2)

    plt.tight_layout()
    path_fig11 = os.path.join(output_dir, '11_comparacion_cuatro_escenarios.png')
    fig.savefig(path_fig11)
    plt.close(fig)
    rutas_generadas.append(path_fig11)

    # FIGURA 12: Frente de Pareto (Consumo Eléctrico vs LCOH / Superficie)
    # Muestreo amplio de configuraciones para trazar el frente de Pareto
    pareto_sec = []
    pareto_lcoh = []
    pareto_area = []
    pareto_feas = []

    j_sweep = np.linspace(0.25, 0.80, 20)
    t_sweep = [720.0, 750.0, 780.0, 800.0, 830.0]

    for t_val in t_sweep:
        for j_val in j_sweep:
            r = sys_calc.dimensionar_para_demanda_h2(
                demanda_h2_kg_h=demanda_h2_kg_h,
                densidad_corriente_a_m2=j_val * 10000.0,
                temperatura_k=t_val + 273.15,
                presion_pa=2000000.0,
                conversion_vapor=0.70
            )
            if r.es_factible:
                ec = opt.evaluar_economico(r)
                pareto_sec.append(r.sec_ac_kwh_kg_h2)
                pareto_lcoh.append(ec['lcoh_kg'])
                pareto_area.append(r.area_activa_total_m2)
                pareto_feas.append(True)

    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
    sc = ax.scatter(pareto_sec, pareto_lcoh, c=pareto_area, cmap='viridis', s=45, alpha=0.75, edgecolors='none')
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label('Superficie Activa Total (m²)', rotation=270, labelpad=15)

    # Resaltar escenarios A, B, C, D
    ax.scatter(scenarios['Escenario_A'].system_result.sec_ac_kwh_kg_h2,
               scenarios['Escenario_A'].lcoh_usd_kg_h2,
               color='red', s=160, marker='*', edgecolors='black', label='A: Base Original', zorder=5)
    ax.scatter(scenarios['Escenario_B'].system_result.sec_ac_kwh_kg_h2,
               scenarios['Escenario_B'].lcoh_usd_kg_h2,
               color='green', s=130, marker='^', edgecolors='black', label='B: Mín. SEC Eléctrico', zorder=5)
    ax.scatter(scenarios['Escenario_C'].system_result.sec_ac_kwh_kg_h2,
               scenarios['Escenario_C'].lcoh_usd_kg_h2,
               color='blue', s=110, marker='s', edgecolors='black', label='C: Industrial Factible', zorder=5)
    ax.scatter(scenarios['Escenario_D'].system_result.sec_ac_kwh_kg_h2,
               scenarios['Escenario_D'].lcoh_usd_kg_h2,
               color='orange', s=130, marker='D', edgecolors='black', label='D: Óptimo LCOH (Pareto)', zorder=5)

    ax.set_xlabel('Consumo Específico de Electricidad AC (kWh/kg H₂)')
    ax.set_ylabel('Costo Nivelado de Hidrógeno, LCOH (USD/kg H₂)')
    ax.grid(True, linestyle='--', alpha=0.6, color=COLORS['grid'])
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.95)
    plt.tight_layout()
    path_fig12 = os.path.join(output_dir, '12_pareto_sec_vs_lcoh_superficie.png')
    fig.savefig(path_fig12)
    plt.close(fig)
    rutas_generadas.append(path_fig12)

    print(f"Generadas exitosamente {len(rutas_generadas)} figuras en '{output_dir}'.")
    return rutas_generadas

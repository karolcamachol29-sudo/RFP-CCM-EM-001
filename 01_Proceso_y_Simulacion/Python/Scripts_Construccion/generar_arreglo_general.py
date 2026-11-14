#!/usr/bin/env python3
"""
Generador del Plano de Arreglo General Preliminar (Plot Plan)
Planta de Producción de e-Metanol (30,000 t/año)
Solvanta Engineering Solutions S.A. de C.V.
Código del Documento: Solvanta_AG-01.pdf
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_plot_plan(output_pdf, output_png):
    # Dimensiones de la parcela: 250 m (ancho X) x 160 m (alto Y)
    fig, ax = plt.subplots(figsize=(18, 11.5), dpi=300)
    
    # Configuración de fondo y rejilla arquitectónica
    ax.set_xlim(-15, 275)
    ax.set_ylim(-15, 185)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 0. Terreno / Límite de batería (Battery Limit)
    # Cerca perimetral exterior
    fence = patches.Rectangle((0, 0), 250, 160, linewidth=2.5, edgecolor='#1A4F7C', facecolor='#F8F9FA', zorder=1)
    ax.add_patch(fence)
    
    # Rejilla suave cada 20 m
    for x in range(0, 260, 20):
        ax.plot([x, x], [0, 160], color='#E2E8F0', linestyle='--', linewidth=0.5, zorder=1)
    for y in range(0, 180, 20):
        ax.plot([0, 250], [y, y], color='#E2E8F0', linestyle='--', linewidth=0.5, zorder=1)
        
    # Coordenadas perimetrales
    ax.text(0, -3, "0,0", fontsize=8, color='#64748B', ha='center', va='top')
    ax.text(250, -3, "250m, 0m", fontsize=8, color='#64748B', ha='center', va='top')
    ax.text(-3, 160, "160m", fontsize=8, color='#64748B', ha='right', va='center')

    # 1. Vialidades (Caminos perimetrales e internos)
    # Vía perimetral exterior (ancho 8 m, offset 2 m)
    road_perim = patches.Rectangle((2, 2), 246, 156, linewidth=1, edgecolor='#CBD5E1', facecolor='#E2E8F0', zorder=2)
    ax.add_patch(road_perim)
    inner_island = patches.Rectangle((10, 10), 230, 140, linewidth=1, edgecolor='#CBD5E1', facecolor='#F1F5F9', zorder=2)
    ax.add_patch(inner_island)
    
    # Calles internas principales (ancho 6 m)
    # Calle Central Norte-Sur (X = 135 a 141)
    ax.add_patch(patches.Rectangle((135, 10), 6, 140, facecolor='#E2E8F0', edgecolor='none', zorder=3))
    # Calle Central Este-Oeste (Y = 80 a 86)
    ax.add_patch(patches.Rectangle((10, 80), 230, 6, facecolor='#E2E8F0', edgecolor='none', zorder=3))
    
    # 2. ZONAS FUNCIONALES DE PLANTA
    
    # --- ZONA ADMINISTRATIVA Y CONTROL (No clasificada, Segura a barlovento) ---
    # Ubicada al Noroeste (arriba a la izquierda, X: 15-75, Y: 100-145)
    admin_box = patches.Rectangle((15, 95), 55, 50, facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1.5, linestyle='-', zorder=4)
    ax.add_patch(admin_box)
    ax.text(42.5, 141, "ZONA NO CLASIFICADA (SEGURA)", fontsize=9, fontweight='bold', color='#0369A1', ha='center')
    
    # Edificio de Control Central (CCR)
    ccr = patches.Rectangle((20, 115), 25, 20, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.2, zorder=5)
    ax.add_patch(ccr)
    ax.text(32.5, 125, "CUARTO DE CONTROL\nCENTRAL (CCR) Y DCS", fontsize=7.5, fontweight='bold', ha='center', va='center')
    
    # Oficinas, Laboratorio de Calidad y Vestidores
    admin_bldg = patches.Rectangle((48, 115), 18, 20, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.2, zorder=5)
    ax.add_patch(admin_bldg)
    ax.text(57, 125, "OFICINAS Y\nLAB. CONTROL\nCALIDAD", fontsize=7, fontweight='bold', ha='center', va='center')
    
    # Estacionamiento y Caseta de Acceso Principal
    gate = patches.Rectangle((20, 100), 12, 10, facecolor='#94A3B8', edgecolor='#334155', linewidth=1, zorder=5)
    ax.add_patch(gate)
    ax.text(26, 105, "CASETA\nACCESO", fontsize=6.5, color='white', fontweight='bold', ha='center', va='center')
    
    # --- ÁREA 100 & RECEPCIÓN DE MATERIAS PRIMAS (X: 15-70, Y: 20-75) ---
    raw_box = patches.Rectangle((15, 15), 55, 60, facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5, zorder=4)
    ax.add_patch(raw_box)
    ax.text(42.5, 71, "ÁREA 100 / RECEPCIÓN MATERIAS PRIMAS", fontsize=8.5, fontweight='bold', color='#B45309', ha='center')
    
    # Estación de regulación CO2 (20 bar)
    co2_stat = patches.Rectangle((20, 48), 20, 18, facecolor='#FDE68A', edgecolor='#D97706', linewidth=1.2, zorder=5)
    ax.add_patch(co2_stat)
    ax.text(30, 57, "ESTACIÓN REG.\nY FILTRADO CO2\n(S-101 a 20 bar)", fontsize=7, fontweight='bold', ha='center', va='center')
    
    # Planta de Tratamiento de Agua Cruda y Ósmosis Inversa (make-up)
    water_plant = patches.Rectangle((44, 48), 22, 18, facecolor='#FDE68A', edgecolor='#D97706', linewidth=1.2, zorder=5)
    ax.add_patch(water_plant)
    ax.text(55, 57, "TRATAMIENTO AGUA\nÓSMOSIS INVERSA\n(Make-up P-201A/B)", fontsize=7, fontweight='bold', ha='center', va='center')
    
    # Tanque de almacenamiento de agua desmineralizada
    tk_water = patches.Circle((32, 30), 8, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.2, zorder=5)
    ax.add_patch(tk_water)
    ax.text(32, 30, "TK-201\nAgua Desm.\n1,000 m³", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Bombas P-201A/B
    p201 = patches.Rectangle((45, 25), 10, 8, facecolor='#E2E8F0', edgecolor='#475569', linewidth=1, zorder=5)
    ax.add_patch(p201)
    ax.text(50, 29, "P-201A/B\nBombas Make-up", fontsize=6, fontweight='bold', ha='center', va='center')

    # --- ÁREA 200: ELECTRÓLISIS SOEC DE ALTA TEMPERATURA (X: 75-130, Y: 95-145) ---
    soec_box = patches.Rectangle((75, 95), 55, 50, facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.5, zorder=4)
    ax.add_patch(soec_box)
    ax.text(102.5, 141, "ÁREA 200: ELECTRÓLISIS SOEC (54.4 MWe)", fontsize=8.5, fontweight='bold', color='#991B1B', ha='center')
    
    # Nave de Stacks SOEC (EL-201)
    soec_stacks = patches.Rectangle((80, 112), 30, 25, facecolor='#FCA5A5', edgecolor='#B91C1C', linewidth=1.2, zorder=5)
    ax.add_patch(soec_stacks)
    ax.text(95, 124.5, "NAVE DE CELDAS SOEC\nEL-201 (750°C, 20 bar)\nProducción H2 Verde", fontsize=7.5, fontweight='bold', ha='center', va='center')
    
    # Sobrecalentador Eléctrico E-202
    e202 = patches.Rectangle((113, 125), 14, 12, facecolor='#FED7AA', edgecolor='#C2410C', linewidth=1.2, zorder=5)
    ax.add_patch(e202)
    ax.text(120, 131, "E-202\nSobrecalent.\n(5.25 MWe)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Enfriadores E-201 (O2) y E-203 (H2) y KO Drum V-201
    e203_v201 = patches.Rectangle((80, 100), 45, 9, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1, zorder=5)
    ax.add_patch(e203_v201)
    ax.text(102.5, 104.5, "E-201 (O2) | E-203 (Cond. H2) | V-201 (Flash H2/H2O KO Drum)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # --- ÁREA 300 & 400: SÍNTESIS DE METANOL (X: 75-130, Y: 15-75) ---
    synth_box = patches.Rectangle((75, 15), 55, 60, facecolor='#FFFBEB', edgecolor='#D97706', linewidth=1.5, zorder=4)
    ax.add_patch(synth_box)
    ax.text(102.5, 71, "ÁREAS 300 & 400: COMPRESIÓN Y SÍNTESIS", fontsize=8.5, fontweight='bold', color='#92400E', ha='center')
    
    # Caseta de Compresor C-301 (Syngas 19.4 -> 75 bar)
    c301 = patches.Rectangle((80, 48), 22, 18, facecolor='#FDE68A', edgecolor='#B45309', linewidth=1.2, zorder=5)
    ax.add_patch(c301)
    ax.text(91, 57, "C-301\nCompresor Syngas\n(1,317 kW, 75 bar)", fontsize=7, fontweight='bold', ha='center', va='center')
    
    # Precalentador E-301 y Mezclador MIX-301
    e301 = patches.Rectangle((105, 52), 18, 12, facecolor='#FEF3C7', edgecolor='#B45309', linewidth=1, zorder=5)
    ax.add_patch(e301)
    ax.text(114, 58, "E-301 / MIX-301\nPrecalentador", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Reactor Tubular Lurgi BWR R-401 / Caldera R-401-S
    r401 = patches.Rectangle((85, 22), 35, 20, facecolor='#FECACA', edgecolor='#B91C1C', linewidth=1.5, zorder=5)
    ax.add_patch(r401)
    ax.text(102.5, 32, "REACTOR BWR R-401 / R-401-S\nSíntesis Cu/ZnO/Al2O3 (245°C, 75 bar)\nGeneración Vapor 20 bar (12.3 MWth)", fontsize=7, fontweight='bold', ha='center', va='center')

    # --- ÁREA 500: SEPARACIÓN Y RECICLO (X: 145-195, Y: 95-145) ---
    area500 = patches.Rectangle((145, 95), 50, 50, facecolor='#F3E8FF', edgecolor='#7E22CE', linewidth=1.5, zorder=4)
    ax.add_patch(area500)
    ax.text(170, 141, "ÁREA 500: SEPARACIÓN HP Y RECICLO", fontsize=8.5, fontweight='bold', color='#6B21A8', ha='center')
    
    # Economizador FEHE E-502A/B y Condensador E-501
    fehe = patches.Rectangle((150, 120), 20, 16, facecolor='#E9D5FF', edgecolor='#7E22CE', linewidth=1.2, zorder=5)
    ax.add_patch(fehe)
    ax.text(160, 128, "E-502A/B (FEHE)\nE-501 (Condensador\nBucle Síntesis)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Separador Flash HP V-501
    v501 = patches.Circle((182, 128), 6, facecolor='#DDD6FE', edgecolor='#6D28D9', linewidth=1.2, zorder=5)
    ax.add_patch(v501)
    ax.text(182, 128, "V-501\nFlash HP\n(75 bar)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Soplador de Reciclo C-501 y Turboexpansor de Purga EXP-501 (X-501)
    c501_exp = patches.Rectangle((150, 102), 40, 14, facecolor='#E9D5FF', edgecolor='#7E22CE', linewidth=1.2, zorder=5)
    ax.add_patch(c501_exp)
    ax.text(170, 109, "C-501 (Soplador Reciclo 150 kW) |\nEXP-501 / X-501 (Turboexpansor Purga, -438 kW)", fontsize=6.5, fontweight='bold', ha='center', va='center')

    # --- ÁREA 600: DESTILACIÓN Y ALMACENAMIENTO (X: 145-200, Y: 15-80) ---
    area600 = patches.Rectangle((145, 15), 55, 65, facecolor='#ECFDF5', edgecolor='#059669', linewidth=1.5, zorder=4)
    ax.add_patch(area600)
    ax.text(172.5, 76, "ÁREA 600: DESTILACIÓN Y PARQUE DE TANQUES", fontsize=8.5, fontweight='bold', color='#065F46', ha='center')
    
    # Flash LP Desgasificador V-601 y Bomba P-601
    v601 = patches.Rectangle((150, 52), 15, 18, facecolor='#A7F3D0', edgecolor='#059669', linewidth=1, zorder=5)
    ax.add_patch(v601)
    ax.text(157.5, 61, "V-601 Flash LP\n(1.25 bar)\nP-601A/B", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Torre de Destilación T-601 con Condensador E-601 y Rehervidor E-602
    t601 = patches.Rectangle((168, 50), 28, 22, facecolor='#A7F3D0', edgecolor='#047857', linewidth=1.5, zorder=5)
    ax.add_patch(t601)
    ax.text(182, 61, "TORRE FRACCIONADORA T-601\n(34 Platos, Grado AA >99.85%)\nE-601 Condensador | E-602 Rehervidor", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Dique de Almacenamiento de Metanol Grado AA (Cubeto al 110%)
    dike = patches.Rectangle((150, 20), 45, 26, facecolor='#D1FAE5', edgecolor='#059669', linewidth=1.5, linestyle='--', zorder=5)
    ax.add_patch(dike)
    ax.text(172.5, 43, "DIQUE ESTANCO CONTENCIÓN 110%", fontsize=6, fontweight='bold', color='#047857', ha='center')
    
    # Tanque TK-601
    tk601 = patches.Circle((165, 31), 9, facecolor='#6EE7B7', edgecolor='#047857', linewidth=1.5, zorder=6)
    ax.add_patch(tk601)
    ax.text(165, 31, "TK-601\ne-Metanol AA\n2,000 m³\n(15 días)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Bombas de Despacho P-602 y Enfriador E-603
    p602 = patches.Rectangle((180, 24), 12, 14, facecolor='#A7F3D0', edgecolor='#047857', linewidth=1, zorder=6)
    ax.add_patch(p602)
    ax.text(186, 31, "E-603 Subenf.\nP-602A/B\nDespacho", fontsize=6, fontweight='bold', ha='center', va='center')

    # --- ÁREA 800: CIRCUITO HÍDRICO CERRADO ZLD (X: 15-60, Y: 83-93) ---
    zld_box = patches.Rectangle((15, 83), 55, 9, facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1, zorder=4)
    ax.add_patch(zld_box)
    ax.text(42.5, 87.5, "ÁREA 800: CIRCUITO CERRADO ZLD (V-801, P-801A/B retorno 7,004 kg/h)", fontsize=6.5, fontweight='bold', color='#0369A1', ha='center', va='center')

    # --- SERVICIOS AUXILIARES Y SUBESTACIÓN (X: 205-245, Y: 60-145) ---
    util_box = patches.Rectangle((203, 60), 42, 85, facecolor='#F1F5F9', edgecolor='#475569', linewidth=1.5, zorder=4)
    ax.add_patch(util_box)
    ax.text(224, 141, "SERVICIOS AUXILIARES", fontsize=8.5, fontweight='bold', color='#1E293B', ha='center')
    
    # Subestación Eléctrica 115 kV / 13.8 kV / 4.16 kV y Rectificadores DC
    substat = patches.Rectangle((206, 110), 36, 26, facecolor='#CBD5E1', edgecolor='#334155', linewidth=1.2, zorder=5)
    ax.add_patch(substat)
    ax.text(224, 123, "SUBESTACIÓN ELÉCTRICA\n60 MVA (115 / 13.8 kV)\nRectificadores DC SOEC\nCentro Control Motores (CCM)", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Torres de Enfriamiento (Cooling Towers)
    ct = patches.Rectangle((206, 85), 36, 20, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.2, zorder=5)
    ax.add_patch(ct)
    ax.text(224, 95, "TORRES DE ENFRIAMIENTO\nCapacidad: 25.8 MW térmicos\nBombas de Circulación CW", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    # Planta de Nitrógeno (N2) y Aire de Instrumentos
    air_n2 = patches.Rectangle((206, 64), 36, 17, facecolor='#E2E8F0', edgecolor='#475569', linewidth=1, zorder=5)
    ax.add_patch(air_n2)
    ax.text(224, 72.5, "AIRE DE INSTRUMENTOS &\nINERTIZACIÓN CON NITRÓGENO\n(Compresores y Tanque N2 Criogénico)", fontsize=6, fontweight='bold', ha='center', va='center')

    # --- SISTEMA CONTRA INCENDIO (SCI) (X: 205-245, Y: 15-55) ---
    sci_box = patches.Rectangle((203, 15), 42, 40, facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.5, zorder=4)
    ax.add_patch(sci_box)
    ax.text(224, 51, "SISTEMA CONTRA INCENDIO (SCI)", fontsize=7.5, fontweight='bold', color='#991B1B', ha='center')
    
    tk_fire = patches.Circle((217, 32), 10, facecolor='#FCA5A5', edgecolor='#B91C1C', linewidth=1.2, zorder=5)
    ax.add_patch(tk_fire)
    ax.text(217, 32, "TK-FIRE\nAgua C.I.\n3,000 m³", fontsize=6.5, fontweight='bold', ha='center', va='center')
    
    p_fire = patches.Rectangle((230, 24), 12, 16, facecolor='#EF4444', edgecolor='#7F1D1D', linewidth=1, zorder=5)
    ax.add_patch(p_fire)
    ax.text(236, 32, "CASA DE\nBOMBAS\nC.I. (Diésel\n+ Eléctr.)", fontsize=5.5, color='white', fontweight='bold', ha='center', va='center')

    # --- ANTORCHA ELEVADA (FLARE STACK) ---
    # Ubicada a sotavento / esquina suroeste segura (X: 3, Y: 3)
    flare_ring = patches.Circle((8, 8), 6, facecolor='#FED7AA', edgecolor='#EA580C', linewidth=1.2, linestyle=':', zorder=5)
    ax.add_patch(flare_ring)
    ax.plot([8], [8], marker='^', markersize=10, color='#C2410C', zorder=6)
    ax.text(8, 8, "\n\nANTORCHA 45m\n(Flare Stack)", fontsize=6, fontweight='bold', color='#C2410C', ha='center')

    # --- ÁREA DE EXPANSIÓN FUTURA (RESERVA TERRITORIAL 25%) ---
    # Ubicada hacia el Este / Noreste (X: 135-200, Y: 147-157)
    exp_area = patches.Rectangle((135, 147), 110, 9, facecolor='#FEF08A', edgecolor='#CA8A04', linewidth=1.2, linestyle='--', zorder=3)
    ax.add_patch(exp_area)
    ax.text(190, 151.5, "ÁREA DE RESERVA TERRITORIAL Y EXPANSIÓN FUTURA (TREN 2 DE SÍNTESIS + 50 MW SOEC)", fontsize=6.5, fontweight='bold', color='#854D0E', ha='center', va='center')

    # --- RUTAS DE EVACUACIÓN Y PUNTOS DE REUNIÓN ---
    # Puntos de reunión PR-1 y PR-2
    pr1 = patches.Circle((20, 148), 4, facecolor='#22C55E', edgecolor='#15803D', linewidth=1.5, zorder=7)
    ax.add_patch(pr1)
    ax.text(20, 148, "PR-1", fontsize=7, color='white', fontweight='bold', ha='center', va='center')
    
    pr2 = patches.Circle((240, 148), 4, facecolor='#22C55E', edgecolor='#15803D', linewidth=1.5, zorder=7)
    ax.add_patch(pr2)
    ax.text(240, 148, "PR-2", fontsize=7, color='white', fontweight='bold', ha='center', va='center')

    # Flechas de evacuación a lo largo de las calles
    ax.annotate("", xy=(20, 142), xytext=(20, 90), arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2), zorder=8)
    ax.annotate("", xy=(138, 148), xytext=(138, 90), arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2), zorder=8)
    ax.annotate("", xy=(240, 142), xytext=(240, 60), arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2), zorder=8)

    # --- ELEMENTOS TOPOGRÁFICOS: NORTE Y ROSA DE LOS VIENTOS ---
    # Rosa de los vientos en esquina superior derecha
    ax.annotate("N", xy=(265, 160), xytext=(265, 140),
                arrowprops=dict(facecolor='#1E293B', width=2.5, headwidth=9),
                fontsize=12, fontweight='bold', ha='center', va='bottom', zorder=9)
    ax.text(265, 137, "Viento Dominante:\nNNE (Golfo de México)\n15 - 28 km/h", fontsize=6.5, color='#334155', ha='center', va='top')

    # Escala gráfica
    ax.plot([10, 60], [-8, -8], color='#0F172A', linewidth=3, zorder=9)
    ax.plot([10, 10], [-6, -10], color='#0F172A', linewidth=2, zorder=9)
    ax.plot([35, 35], [-7, -9], color='#0F172A', linewidth=1.5, zorder=9)
    ax.plot([60, 60], [-6, -10], color='#0F172A', linewidth=2, zorder=9)
    ax.text(10, -11, "0m", fontsize=7, ha='center', va='top')
    ax.text(35, -11, "25m", fontsize=7, ha='center', va='top')
    ax.text(60, -11, "50m", fontsize=7, ha='center', va='top')
    ax.text(35, -5, "ESCALA GRÁFICA PRELIMINAR", fontsize=7, fontweight='bold', ha='center')

    # --- CUADRO DE LEYENDA TÉCNICA ---
    legend_box = patches.Rectangle((75, -14), 185, 11, facecolor='#FFFFFF', edgecolor='#94A3B8', linewidth=1, zorder=9)
    ax.add_patch(legend_box)
    ax.text(78, -9, "CLASIFICACIÓN DE ÁREAS (NFPA 497 / API RP 500):", fontsize=7, fontweight='bold', color='#0F172A')
    
    # Muestras de color
    ax.add_patch(patches.Rectangle((180, -12), 4, 3, facecolor='#FECACA', edgecolor='#B91C1C'))
    ax.text(186, -10.5, "Clase I Div 1 (H2/MeOH)", fontsize=6.5, va='center')
    ax.add_patch(patches.Rectangle((215, -12), 4, 3, facecolor='#FEF3C7', edgecolor='#D97706'))
    ax.text(221, -10.5, "Clase I Div 2", fontsize=6.5, va='center')
    ax.add_patch(patches.Rectangle((240, -12), 4, 3, facecolor='#E0F2FE', edgecolor='#0284C7'))
    ax.text(246, -10.5, "No clasif.", fontsize=6.5, va='center')

    # --- CAJETÍN DE INGENIERÍA OFICIAL ---
    # En la parte superior fuera del límite o marco
    ax.text(125, 175, "SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.", fontsize=13, fontweight='bold', color='#1A4F7C', ha='center')
    ax.text(125, 168, "PROYECTO LICITATORIO RFP-CCM-EM-001 | PLANTA DE e-METANOL (30,000 t/año) | complejo industrial adyacente", fontsize=9.5, fontweight='bold', color='#334155', ha='center')
    ax.text(125, 163, "PLANO DE ARREGLO GENERAL PRELIMINAR (PLOT PLAN) -- DOCUMENTO OFICIAL Solvanta_AG-01 (Rev. 0)", fontsize=8.5, color='#475569', ha='center')

    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Plano generado exitosamente:\n- {output_pdf}\n- {output_png}")

if __name__ == "__main__":
    create_plot_plan(
        "Entregables/PIB-01_Solvanta/Solvanta_AG-01.pdf",
        "Entregables/PIB-01_Solvanta/figuras/Solvanta_AG-01.png"
    )

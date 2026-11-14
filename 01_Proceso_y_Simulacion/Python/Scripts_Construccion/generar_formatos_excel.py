#!/usr/bin/env python3
"""
Generador de Formatos Oficiales en Excel (.xlsx) para el Paquete de Ingeniería Básica (PIB-01)
Firma: Solvanta Engineering Solutions S.A. de C.V.
Archivos generados:
1. Solvanta_F-PIB-01.xlsx (Bases consolidadas del proceso)
2. Solvanta_F-PIB-02.xlsx (Inventario técnico de equipos - Partes A, B y C)
3. Solvanta_F-PIB-03.xlsx (Balance de recursos, servicios y salidas - Partes A y B)
4. Solvanta_F-PIB-04.xlsx (Pendientes, inconsistencias y verificación - Partes A y B)
5. Solvanta_TC-01.xlsx    (Tabla oficial de corrientes DWSIM v1)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Colores corporativos Solvanta
NAVY_HEADER = "1A4F7C"
NAVY_SUBHEADER = "2E75B6"
LIGHT_BLUE_ROW = "F2F7FA"
BORDER_GRAY = "D9D9D9"
DARK_TEXT = "000000"
WHITE_TEXT = "FFFFFF"

def apply_styling(ws, title, subtitle):
    # Fuentes y estilos
    font_title = Font(name="Calibri", size=14, bold=True, color=NAVY_HEADER)
    font_sub = Font(name="Calibri", size=10, italic=True, color="555555")
    font_header = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
    font_data = Font(name="Calibri", size=9.5)
    font_bold = Font(name="Calibri", size=9.5, bold=True)
    
    fill_header = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    fill_alt = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid")
    
    thin_border = Border(
        left=Side(style='thin', color=BORDER_GRAY),
        right=Side(style='thin', color=BORDER_GRAY),
        top=Side(style='thin', color=BORDER_GRAY),
        bottom=Side(style='thin', color=BORDER_GRAY)
    )
    
    # Encabezado institucional
    ws.merge_cells("A1:H1")
    ws["A1"] = "SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V."
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells("A2:H2")
    ws["A2"] = f"PROYECTO LICITATORIO RFP-CCM-EM-001 | {title} | {subtitle}"
    ws["A2"].font = font_sub
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[4].height = 26

def auto_fit_columns(ws, max_cols=12):
    for col in range(1, max_cols + 1):
        col_letter = get_column_letter(col)
        max_len = 0
        for row in range(4, ws.max_row + 1):
            val = ws.cell(row=row, column=col).value
            if val is not None:
                lines = str(val).split("\n")
                for line in lines:
                    if len(line) > max_len:
                        max_len = len(line)
        ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 48)

# 1. GENERAR F-PIB-01: BASES CONSOLIDADAS DEL PROCESO
def generar_f_pib_01(filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "F-PIB-01_Bases"
    apply_styling(ws, "DOCUMENTO F-PIB-01", "BASES CONSOLIDADAS DEL PROCESO")
    
    headers = [
        "ID", "Parámetro", "Descripción", "Valor / Definición", 
        "Unidad", "Fuente", "Supuesto / Método de Cálculo", "Estado"
    ]
    
    ws.append([]) # Fila 3 vacía
    ws.append(headers) # Fila 4 encabezados
    
    data = [
        [
            "BD-01", "Capacidad nominal", "Producción esperada durante operación normal habitual.",
            "3788.65", "kg/h", "DWSIM v1 / Corriente S-604 / Bases de Licitación",
            "Operación continua al 100% de capacidad nominal (118.34 kmol/h de metanol puro).", "Definido"
        ],
        [
            "BD-02", "Horas de operación", "Horas efectivas consideradas durante un año calendario.",
            "8000", "h/año", "Bases de Diseño Rev. 1 / LE-01K Supuesto 1",
            "Considera 333.3 días de operación continua y 31.7 días (760 h) de parada programada para mantenimiento.", "Definido"
        ],
        [
            "BD-03", "Producción anual", "Producción obtenida durante las horas efectivas anuales.",
            "30309.20", "t/año", "Cálculo BD-03 / DWSIM v1",
            "= 3788.65 kg/h * 8000 h/año / 1000. Supera la meta estipulada de 30,000 t/año en bases.", "Definido"
        ],
        [
            "BD-04", "Capacidad máxima", "Mayor cantidad permitida bajo condición de operación al 110% de diseño.",
            "4167.52", "kg/h", "Criterio de diseño de ingeniería básica (+10% margen)",
            "= 1.10 * 3788.65 kg/h (Equivale a 33,340.12 t/año para absorción de transitorios).", "Definido"
        ],
        [
            "BD-05", "Disponibilidad planeada", "Relación porcentual entre horas efectivas y horas totales del año.",
            "91.32", "%", "Cálculo de disponibilidad de planta",
            "= (8000 h / 8760 h) * 100. Factor de servicio estándar en plantas petroquímicas Pemex.", "Definido"
        ],
        [
            "BD-06", "Producto principal", "Sustancia química de valor comercial obtenida en la planta.",
            "e-Metanol Grado Químico AA", "No aplica", "Licitación RFP-CCM-EM-001 / DWSIM v1",
            "Metanol sintético a partir de CO2 capturado e H2 verde electrolítico SOEC.", "Definido"
        ],
        [
            "BD-07", "Especificación del producto", "Requisitos de pureza, humedad y densidad comercial requeridos.",
            "Pureza >= 99.85% p/p (obtenido 99.89%), Agua <= 0.10% p/p, Densidad 0.791-0.793 g/cm³", "No aplica", "Norma ASTM D1152 / IMP",
            "Cumple estrictamente grado químico AA para síntesis de formaldehído y acético.", "Definido"
        ],
        [
            "BD-08", "Materia prima principal", "Insumos químicos esenciales transformados en el proceso.",
            "Dióxido de carbono (CO2 capturado >= 99%) y Agua cruda/desmineralizada para H2", "No aplica", "Bases de Licitación / Conagua",
            "CO2 suministrado por ducto desde complejo industrial adyacente; agua con reciclo ZLD (43.1% ahorro).", "Definido"
        ],
        [
            "BD-09", "Modo de operación", "Régimen de funcionamiento temporal de la planta.",
            "Continuo (24 horas/día, régimen estacionario)", "No aplica", "Filosofía de Operación FO-01",
            "Proceso continuo de lecho catalítico con control regulatorio y lazos de seguridad SIS.", "Definido"
        ],
        [
            "BD-10", "Límite de batería de entrada", "Punto físico y condiciones de recepción de materias primas y servicios.",
            "CO2 gas a 20.0 bar y 25.0°C; Agua desm. a 1.013/20.0 bar y 25°C; Electricidad a 115 kV", "No aplica", "DTI v0.2 / LE-01B / Diagramas BL",
            "Recepción isobárica de CO2 a 20 bar elimina compresión primaria; energía de red renovable.", "Definido"
        ],
        [
            "BD-11", "Límite de batería de salida", "Punto físico y condiciones de despacho de productos y efluentes.",
            "Metanol a TK-601 (35°C, 1.013 bar); O2 puro a batería (19.4 bar, 31°C); Purga gas (1.1 bar)", "No aplica", "DTI v0.2 / TC-01 / AC-HAZOP-01",
            "Despacho por autotanques y ducto de oxígeno; gas de purga a red de gas combustible Pemex.", "Definido"
        ],
        [
            "BD-12", "Condición ambiental referencia", "Parámetros meteorológicos del emplazamiento en sitio industrial de referencia",
            "Tamb = 25.0°C (promedio), Pamb = 1.013 bar (nivel del mar), Humedad = 78%, Viento NNE", "No aplica", "Estación Meteorológica polo industrial adyacente",
            "Condiciones base para diseño de torres de enfriamiento, intercambiadores y recipientes.", "Definido"
        ],
        [
            "BD-13", "Caso normal de operación", "Condición utilizada para representar la operación nominal habitual.",
            "Carga 100%: 3788.65 kg/h MeOH, 5274.34 kg/h CO2, 55,436.39 kW potencia neta", "No aplica", "DWSIM v1 / TC-01 / TE-01",
            "Balances rigurosos totalmente convergidos en PRSV2-VL sin advertencias.", "Definido"
        ],
        [
            "BD-14", "Caso máximo de operación", "Condición de mayor procesamiento continuo permisible (+10%).",
            "Carga 110%: 4167.52 kg/h MeOH, 5801.77 kg/h CO2, 60,980.03 kW potencia neta", "No aplica", "Cálculo de dimensionamiento hidráulico",
            "Factor de servicio de 1.10 para verificación de bombas, compresores y válvulas de control.", "Definido"
        ],
        [
            "BD-15", "Módulo estequiométrico M", "Relación de reactivos en alimentación al bucle: (yH2 - yCO2)/(yCO + yCO2).",
            "2.05 (Intervalo admisible 2.00 - 2.10)", "Adimensional", "Cinética Lurgi / Haldor Topsoe / DWSIM",
            "Exceso moderado de H2 previene coquización catalítica y desplaza equilibrio hacia metanol.", "Definido"
        ]
    ]
    
    for row in data:
        ws.append(row)
        
    # Estilizado de celdas
    for col in range(1, 9):
        cell = ws.cell(row=4, column=col)
        cell.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws.max_row + 1):
        ws.row_dimensions[r].height = 24
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 9):
            c = ws.cell(row=r, column=col)
            c.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: c.fill = fill
            c.border = Border(
                left=Side(style='thin', color=BORDER_GRAY),
                right=Side(style='thin', color=BORDER_GRAY),
                top=Side(style='thin', color=BORDER_GRAY),
                bottom=Side(style='thin', color=BORDER_GRAY)
            )
            if col in [1, 5, 8]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif col in [4]:
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                
    auto_fit_columns(ws, 8)
    wb.save(filename)
    print(f"Generado exitosamente: {filename}")

# 2. GENERAR F-PIB-02: INVENTARIO TÉCNICO DE EQUIPOS (PARTES A, B Y C)
def generar_f_pib_02(filename):
    wb = openpyxl.Workbook()
    
    # Datos completos de los 28-30 equipos
    equipos = [
        # Tag, Tipo, Servicio, Cantidad, CapNorm, CapMax, P_op, T_op, VarTam, ValTam, PotCarga, Material, ServAux, ReqHAZOP, Fuente, Pendiente, Estado
        ("P-201A/B", "Bomba centrífuga", "Impulso de agua desmineralizada make-up hacia caldera de chaqueta a 20 bar", "2: 1 op / 1 res", "9241.8 kg/h", "10166.0 kg/h", "20.0 bar", "25.0 °C", "Flujo volumétrico y carga", "9.27 m³/h (195 m carga)", "6.42 kW eléctrico", "Acero inoxidable 316L", "Electricidad 440 V", "PAL-201 alarma baja descarga; switch auto a P-201B", "DWSIM v1; LE-01D", "Confirmar curva NPSH de fabricante", "Preliminar"),
        ("MIX-201", "Mezclador estático", "Homogeneización de agua fresca make-up y retorno condensado ZLD", "1 unidad", "16244.9 kg/h", "17869.4 kg/h", "20.0 bar", "39.8 °C", "Flujo másico total", "16.24 t/h procesadas", "No aplica (mezcla adiabática)", "Acero inoxidable 316L", "Ninguno (equipo pasivo)", "Válvulas check en ambas entradas para evitar contraflujo", "DWSIM v1; DTI v0.2", "Calcular caída de presión interna (Delta P)", "Definido"),
        ("R-401-S", "Caldera / Chaqueta reactor", "Generación de vapor saturado a 20 bar con calor exotérmico de síntesis", "1 unidad", "16244.9 kg/h", "17869.4 kg/h", "20.0 bar", "212.4 °C (sat)", "Carga térmica y flujo vapor", "16.24 t/h de vapor", "12335.36 kW térmicos (gen)", "Acero al carbono A-516 Gr 70", "Agua tratada de caldera", "PSV-401 tarada a 24 bar; interlock I-01 por TAHH-401", "DWSIM v1; TE-01", "Verificar espesor de carcasa según ASME Sec VIII", "Definido"),
        ("E-202", "Sobrecalentador eléctrico", "Sobrecalentamiento de vapor saturado de 212.4°C a 800°C para celdas SOEC", "1 unidad", "16244.9 kg/h", "17869.4 kg/h", "20.0 bar", "800.0 °C salida", "Potencia eléctrica térmica", "5248.42 kW eléctricos", "5248.42 kW térmicos", "Inconel 625 / Alloy 800H", "Electricidad media tensión", "TAH-202 y corte de resistencias TAHH-202 (>830°C)", "DWSIM v1; TE-01", "Diseñar control tiristorizado SCR y contactores", "Preliminar"),
        ("EL-201", "Electrolizador SOEC", "Disociación catalítica de vapor a 800°C produciendo H2 verde y O2", "1 módulo multicelda", "16244.9 kg/h vapor", "17869.4 kg/h", "19.4 bar", "800.0 °C", "Potencia eléctrica instalada", "38067.30 kW (38.07 MWe)", "38067.30 kW eléctrico AC (36735.0 kW DC)", "Celdas cerámicas YSZ/Ni-YSZ", "Electricidad DC / Vapor 800°C", "Interlock I-03 por alta Delta P trans-membrana (>0.4 bar)", "DWSIM v1; LE-01E", "Curvas de degradación de celdas a 10 años (TBD-01)", "TBD abierto"),
        ("E-201", "Enfriador de oxígeno", "Enfriamiento de O2 puro anódico de 800°C a 31°C con agua de torre", "1 unidad", "10098.8 kg/h", "11108.6 kg/h", "19.4 bar", "31.0 °C salida", "Área de transferencia / Carga", "185.0 m² preliminar", "2345.10 kW térmicos (enf)", "Acero inoxidable 316L", "Agua de enfriamiento (CW)", "Válvula de control TCV-201 en falla abierta (FO)", "DWSIM v1; TE-01", "Calcular coeficiente U riguroso en HTRI (TBD-02)", "TBD abierto"),
        ("E-203", "Condensador efluente SOEC", "Enfriamiento de gas catódico H2 húmedo de 800°C a 38°C para condensar agua", "1 unidad", "6145.8 kg/h", "6760.4 kg/h", "19.4 bar", "38.0 °C salida", "Área de transferencia / Carga", "340.0 m² preliminar", "8962.22 kW térmicos (enf)", "Acero inoxidable 316L / Inconel", "Agua de enfriamiento (CW)", "TAH-203 alarma por alta T; venteo por PDCV-201", "DWSIM v1; TE-01", "Calcular coeficiente global U en HTRI (TBD-02)", "TBD abierto"),
        ("V-201", "Separador flash KO Drum", "Separación gas-líquido de hidrógeno verde seco y agua condensada", "1 recipiente vertical", "6145.8 kg/h", "6760.4 kg/h", "19.4 bar", "38.0 °C", "Volumen útil / Diámetro", "8.5 m³ (D=1.4 m, H=4.2 m)", "No aplica (separación física)", "Acero inoxidable 316L", "Aire de instrumentos", "LAH-201 / LAL-201 control de nivel con LCV-201", "DWSIM v1; DTI v0.2", "Verificar tiempo de retención de líquido (5 min)", "Definido"),
        ("MIX-301", "Mezclador estático syngas", "Mezcla de H2 verde seco y CO2 de captura para fijar módulo M=2.05", "1 unidad", "6589.1 kg/h", "7248.0 kg/h", "19.4 bar", "32.9 °C", "Flujo másico procesado", "6.59 t/h de syngas", "No aplica (mezcla adiabática)", "Acero inoxidable 316L", "Ninguno (equipo pasivo)", "Analizador de relación estequiométrica AIC-301", "DWSIM v1; LE-01C", "Verificar pérdida de carga interna", "Definido"),
        ("E-301", "Precalentador de syngas", "Acondicionamiento térmico de syngas de 32.9°C a 71.7°C previo a compresor", "1 unidad", "6589.1 kg/h", "7248.0 kg/h", "19.4 bar", "71.7 °C salida", "Área de transferencia / Carga", "42.0 m² preliminar", "250.00 kW térmicos (cal)", "Acero al carbono A-516 Gr 70", "Vapor de baja presión", "TAH-301 alarma alta temperatura a succión de C-301", "DWSIM v1; TE-01", "Dimensionar área TEMA en HTRI", "Preliminar"),
        ("C-301", "Compresor centrífugo", "Compresión multietapa de syngas fresco de 19.4 bar a 75.0 bar de síntesis", "1 tren multietapa", "6589.1 kg/h", "7248.0 kg/h", "75.0 bar desc.", "271.0 °C desc.", "Caudal de gas y potencia", "1,850 Nm³/h / Potencia", "1316.67 kW eléctrico", "Acero forjado aleado Cr-Mo", "Electricidad 4.16 kV / CW", "PSHH-301 interlock I-02; lazo anti-surge UIC-301", "DWSIM v1; TE-01", "Curva de compresor y sistema anti-surge (TBD-03)", "TBD abierto"),
        ("MIX-401", "Mezclador bucle síntesis", "Integración de syngas fresco comprimido con gas de reciclo circulante", "1 unidad", "21308.1 kg/h", "23438.9 kg/h", "75.0 bar", "83.2 °C", "Flujo másico total bucle", "21.31 t/h combinadas", "No aplica (mezcla adiabática)", "Acero al carbono A-516 Gr 70", "Ninguno (pasivo)", "Válvula check en descarga de compresores", "DWSIM v1; LE-01C", "Calcular delta P", "Definido"),
        ("E-502A/B", "Economizador FEHE", "Precalentamiento de mezcla reactiva a 210°C recuperando calor del efluente", "2 carcasas serie (A/B)", "21308.1 kg/h", "23438.9 kg/h", "75.0 bar", "210.0 °C tubos", "Área de intercambio térmico", "165.0 m² combinada", "1235.43 kW intercambio", "Acero aleado 1.25Cr-0.5Mo", "Integración térmica interna", "TAH-401 entrada a reactor; bypass TV-502 de control", "DWSIM v1; LE-01E", "Verificar coeficiente U y delta P en HTRI (TBD-02)", "TBD abierto"),
        ("R-401", "Reactor tubular BWR Lurgi", "Síntesis catalítica cuasi-isotérmica de metanol sobre lecho Cu/ZnO/Al2O3", "1 reactor multitubular", "21308.1 kg/h", "23438.9 kg/h", "75.0 bar", "245.0 °C lecho", "Volumen catalizador y tubos", "18.5 t catalizador (2,800 tubos)", "7924.76 kW térmicos (reac)", "Tubos: Acero aleado / Carcasa: CS", "Vapor saturado 20 bar (R-401-S)", "Interlock I-01 por TAHH-401 (>260°C) corte de alimentación", "DWSIM v1; LE-01C", "Cinética de desactivación del catalizador (TBD-01)", "TBD abierto"),
        ("E-501", "Condensador bucle síntesis", "Enfriamiento y condensación total de metanol/agua de 224.6°C a 38°C", "1 unidad (carcasa y tubos)", "21308.1 kg/h", "23438.9 kg/h", "75.0 bar", "38.0 °C salida", "Área de transferencia / Carga", "520.0 m² preliminar", "13742.75 kW térmicos (enf)", "Acero al carbono A-516 / SS 316", "Agua de enfriamiento (CW)", "TAH-501 alarma simple alta temperatura salida", "DWSIM v1; TE-01", "Diseño riguroso TEMA en HTRI (TBD-02)", "TBD abierto"),
        ("V-501", "Separador flash HP", "Separación bifásica a 75 bar de metanol crudo líquido y gas inconvertido", "1 recipiente vertical HP", "21308.1 kg/h", "23438.9 kg/h", "75.0 bar", "38.0 °C", "Volumen útil / Diámetro", "14.5 m³ (D=1.8 m, H=5.8 m)", "No aplica (separación flash)", "Acero al carbono A-516 Clad 316", "Aire de instrumentos", "Interlock I-04 cierre de SDV-501 por LALL-501 (anti blow-by)", "DWSIM v1; AC-HAZOP-01", "Tiempo de respuesta de válvula SDV-501 (HZ-02)", "En proceso"),
        ("SPLIT-501", "Divisor de reciclo/purga", "Distribución de 96% de gas inconvertido a reciclo y 4% a purga de inertes", "1 cabezal con control", "15339.8 kg/h", "16873.7 kg/h", "75.0 bar", "38.0 °C", "Fracción de división", "96.0% reciclo / 4.0% purga", "No aplica", "Acero al carbono A-516 Gr 70", "Aire de instrumentos", "Control de flujo de purga FCV-505 con alarma FAL-505", "DWSIM v1; LE-01E", "Confirmar concentración de inertes con cromatógrafo", "Definido"),
        ("C-501", "Soplador de reciclo", "Compensación de pérdidas de carga del bucle cerrado (delta P = 1.5 bar)", "1 soplador centrífugo", "14726.2 kg/h", "16198.8 kg/h", "75.0 bar desc.", "60.0 °C", "Caudal volumétrico circulante", "4,120 m³/h / Potencia", "150.00 kW eléctrico", "Acero forjado aleado", "Electricidad 440 V", "PSHH-501 interlock I-02; alarma de vibración VAH-501", "DWSIM v1; TE-01", "Curva H-Q de fabricante", "Preliminar"),
        ("EXP-501", "Turboexpansor de purga", "Despresurización de purga de 75 a 1.1 bar con recuperación eléctrica limpia", "1 unidad criogénica", "613.6 kg/h", "675.0 kg/h", "1.10 bar desc.", "-138.6 °C desc.", "Potencia eléctrica generada", "Generador 437.8 kW", "-437.79 kW generado neto", "Acero aleado criogénico 304L", "Generador eléctrico a red", "Cierre rápido SDV-503 por sobrevelocidad SAHH-501", "DWSIM v1; TE-01", "Hoja de datos de turbomaquinaria criogénica", "Preliminar"),
        ("VALV-601", "Válvula expansión JT", "Despresurización de metanol crudo líquido de 75.0 bar a 1.25 bar", "1 válvula de control", "5968.4 kg/h", "6565.2 kg/h", "1.25 bar desc.", "38.0 °C", "Coeficiente de flujo Cv", "Cv = 14.5 gpm/psi^0.5", "No aplica (laminación isentálpica)", "Cuerpo acero inoxidable 316L", "Aire de instrumentos", "Válvula LCV-501 operada por controlador de nivel LIC-501", "DWSIM v1; DTI v0.2", "Cálculo de cavitación y flashing con fabricante", "Definido"),
        ("V-601", "Flash desgasificador LP", "Desorción de gases disueltos (CO2, H2, CH4) previo al fraccionamiento", "1 tambor horizontal LP", "5968.4 kg/h", "6565.2 kg/h", "1.25 bar", "38.0 °C", "Volumen útil / Retención", "6.2 m³ (D=1.2 m, L=5.5 m)", "No aplica (desorción física)", "Acero al carbono A-516 Gr 70", "Aire de instrumentos", "PSV-601 tarada a 4.5 bar hacia cabezal de venteo", "DWSIM v1; LE-01C", "Dimensionar malla antivaho (demister)", "Definido"),
        ("P-601A/B", "Bombas alimentación torre", "Impulso de metanol crudo desgasificado de 1.25 a 2.20 bar hacia plato 18", "2: 1 op / 1 res", "5961.8 kg/h", "6558.0 kg/h", "2.20 bar", "38.0 °C", "Flujo volumétrico y carga", "7.55 m³/h (22 m carga)", "1.20 kW eléctrico", "Acero inoxidable 316L", "Electricidad 440 V", "Paro por LALL-601 en V-601; switch a P-601B por PAL-601", "DWSIM v1; TE-01", "Confirmar curvas y sellos mecánicos dobles", "Preliminar"),
        ("T-601", "Columna fraccionadora", "Destilación binaria MeOH/H2O para obtener e-metanol grado AA (>99.85%)", "1 columna de platos", "5961.8 kg/h alim.", "6558.0 kg/h", "1.20 bar domo", "68.5 °C / 103.9 °C", "Número platos / Diámetro", "34 platos (24 teóricas), D=1.2 m", "No aplica (separación fracc.)", "Carcasa e internos: SS 316L", "Vapor en fondos / CW en domo", "PSV-602 tarada a 2.0 bar; interlock corte vapor por LALL-603", "DWSIM v1; LE-01E", "Hidráulica detallada y tipo de platos (TBD-04)", "TBD abierto"),
        ("E-601", "Condensador de domo T-601", "Condensación total de vapores de metanol en cabeza de columna (R/D = 1.50)", "1 intercambiador tubos", "9471.6 kg/h", "10418.8 kg/h", "1.20 bar", "68.5 °C (sat)", "Área de transferencia / Carga", "145.0 m² preliminar", "3077.25 kW térmicos (enf)", "Acero inoxidable 316L", "Agua de enfriamiento (CW)", "TAH-601 alarma alta temperatura condensado; TCV-601 FO", "DWSIM v1; TE-01", "Cálculo riguroso TEMA en HTRI (TBD-02)", "TBD abierto"),
        ("V-602", "Acumulador de reflujo", "Acumulación y desacoplamiento de metanol destilado para reflujo y producto", "1 tambor horizontal", "9471.6 kg/h", "10418.8 kg/h", "1.20 bar", "68.5 °C", "Volumen útil / Retención", "5.8 m³ (10 min retención)", "No aplica", "Acero inoxidable 316L", "Aire de instrumentos", "LAH-602 / LAL-602 y paro de bombas P-602 por LALL-602", "DWSIM v1; DTI v0.2", "Verificar tiempo de retención y boquillas", "Definido"),
        ("P-602A/B", "Bombas de reflujo y envío", "Retorno de reflujo (5,683 kg/h) y envío de metanol producto (3,789 kg/h)", "2: 1 op / 1 res", "9471.6 kg/h", "10418.8 kg/h", "2.50 bar", "68.5 °C", "Flujo volumétrico y carga", "12.0 m³/h (28 m carga)", "1.50 kW eléctrico", "Acero inoxidable 316L", "Electricidad 440 V", "PAL-602 alarma baja descarga; conmutación automática", "DWSIM v1; TE-01", "Seleccionar motor a prueba de explosión (Clase I Div 1)", "Preliminar"),
        ("E-602", "Rehervidor de fondos T-601", "Suministro de calor de ebullición para despojo hídrico en fondo de torre", "1 termosifón vertical", "4346.8 kg/h vapor", "4781.5 kg/h", "1.25 bar", "103.9 °C fondo", "Área de transferencia / Carga", "130.0 m² preliminar", "3266.68 kW térmicos (cal)", "Tubos y carcasa: SS 316L", "Vapor de 3.5 bar (LP steam)", "Corte automático de vapor por LALL-603; FAL-602 alarma", "DWSIM v1; TE-01", "Verificar circulación termosifón en HTRI", "Preliminar"),
        ("E-603", "Subenfriador de producto", "Enfriamiento final de e-metanol grado AA de 68.5°C a 35.0°C para almacenaje", "1 unidad placas/tubos", "3788.7 kg/h", "4167.5 kg/h", "1.10 bar", "35.0 °C salida", "Área de transferencia / Carga", "18.5 m² preliminar", "111.11 kW térmicos (enf)", "Acero inoxidable 316L", "Agua helada / Chilled water", "TAH-603 alarma alta temperatura metanol (>40°C)", "DWSIM v1; TE-01", "Dimensionar área en HTRI", "Definido"),
        ("TK-601", "Tanque almacenamiento MeOH", "Almacenamiento atmosférico seguro de e-metanol comercial (15 días)", "1 tanque vertical", "3788.7 kg/h llenado", "Despacho por lote", "1.013 bar (atm)", "35.0 °C", "Volumen nominal útil", "2,000 m³ (D=14 m, H=13.5 m)", "No aplica (almacenamiento)", "Acero al carbono con recubrimiento epóxico", "Colchón de N2 / Red SCI", "LAHH-604 interlock con SDV-604; válvula PVRV API 2000", "Bases Licitación; AC-HAZOP-01", "Diseño mecánico según norma API 650", "Definido"),
        ("V-801", "Desaireador acumulador ZLD", "Recepción y desgasificación de condensado SOEC y fondos hídricos de torre", "1 tanque atmosférico", "7004.4 kg/h", "7704.9 kg/h", "1.25 bar", "58.9 °C", "Volumen de retención", "12.0 m³ (retención 1.5 h)", "No aplica", "Acero inoxidable 304L", "Vapor de purga / Venteo", "LAH-801 / LAL-801 y PSV-801 tarada a 3 bar", "DWSIM v1; LE-01C", "Calcular bafles internos y tiempo de desgasificación", "Definido"),
        ("P-801A/B", "Bombas retorno agua ZLD", "Presurización de agua tratada desmineralizada de 1.25 bar a 20.0 bar a caldera", "2: 1 op / 1 res", "7004.4 kg/h", "7704.9 kg/h", "20.0 bar", "59.2 °C", "Flujo volumétrico y carga", "7.10 m³/h (195 m carga)", "5.51 kW eléctrico", "Acero inoxidable 316L", "Electricidad 440 V", "PAL-801 alarma baja presión; conmutación automática", "DWSIM v1; TE-01", "Verificar curvas de fabricante y potencia", "Preliminar")
    ]
    
    # HOJA 1: PARTE A (Identificación y condiciones)
    ws_a = wb.active
    ws_a.title = "F-PIB-02A_Identificacion"
    apply_styling(ws_a, "DOCUMENTO F-PIB-02 (PARTE A)", "IDENTIFICACIÓN, CAPACIDAD Y CONDICIONES DE OPERACIÓN")
    
    headers_a = ["Tag", "Equipo", "Servicio del Equipo", "Cantidad", "Cap. Normal", "Cap. Máxima", "Presión Operación", "Temperatura Operación"]
    ws_a.append([])
    ws_a.append(headers_a)
    
    for eq in equipos:
        ws_a.append([eq[0], eq[1], eq[2], eq[3], eq[4], eq[5], eq[6], eq[7]])
        
    for col in range(1, 9):
        c = ws_a.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_a.max_row + 1):
        ws_a.row_dimensions[r].height = 22
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 9):
            cell = ws_a.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 4]: cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col in [5, 6, 7, 8]: cell.alignment = Alignment(horizontal="right", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_a, 8)

    # HOJA 2: PARTE B (Tamaño y requerimientos)
    ws_b = wb.create_sheet(title="F-PIB-02B_Tamano_Requerim")
    apply_styling(ws_b, "DOCUMENTO F-PIB-02 (PARTE B)", "VARIABLES DE TAMAÑO, POTENCIA / CARGA TÉRMICA Y SERVICIOS")
    
    headers_b = ["Tag", "Variable de Tamaño Representativa", "Valor / Unidad Tamaño", "Potencia / Carga Térmica (kW)", "Material Preliminar", "Servicio Auxiliar Requerido"]
    ws_b.append([])
    ws_b.append(headers_b)
    
    for eq in equipos:
        ws_b.append([eq[0], eq[8], eq[9], eq[10], eq[11], eq[12]])
        
    for col in range(1, 7):
        c = ws_b.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_b.max_row + 1):
        ws_b.row_dimensions[r].height = 22
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 7):
            cell = ws_b.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col == 1: cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col in [3, 4]: cell.alignment = Alignment(horizontal="right", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_b, 6)

    # HOJA 3: PARTE C (Trazabilidad y pendientes)
    ws_c = wb.create_sheet(title="F-PIB-02C_Trazabilidad")
    apply_styling(ws_c, "DOCUMENTO F-PIB-02 (PARTE C)", "REQUISITOS HAZOP, FUENTES Y PENDIENTES TÉCNICOS")
    
    headers_c = ["Tag", "Requisito HAZOP / Filosofía de Control", "Fuente Documental", "Pendiente Técnico Específico", "Estado del Dato"]
    ws_c.append([])
    ws_c.append(headers_c)
    
    for eq in equipos:
        ws_c.append([eq[0], eq[13], eq[14], eq[15], eq[16]])
        
    for col in range(1, 6):
        c = ws_c.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_c.max_row + 1):
        ws_c.row_dimensions[r].height = 24
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 6):
            cell = ws_c.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 5]: cell.alignment = Alignment(horizontal="center", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_c, 5)

    wb.save(filename)
    print(f"Generado exitosamente: {filename}")

# 3. GENERAR F-PIB-03: BALANCE DE RECURSOS, SERVICIOS Y SALIDAS
def generar_f_pib_03(filename):
    wb = openpyxl.Workbook()
    
    recursos = [
        # ID, Clasif, Concepto, Equipo, TasaNorm, TasaMax, Unidad, Horas, CantAnual, Fuente, Supuesto, Estado
        ("RS-01", "Materia prima", "Dióxido de carbono (CO2 capturado 99%)", "Área 100 / MIX-301", "5274.34", "5801.77", "kg/h", "8000", "42194.72 t/año", "DWSIM v1; Corriente S-101", "Suministro isobárico a 20.0 bar continuo (121.0 kmol/h).", "Definido"),
        ("RS-02", "Materia prima", "Agua desmineralizada make-up fresca", "Área 200 / P-201A/B", "9241.84", "10166.02", "kg/h", "8000", "73934.72 t/año", "DWSIM v1; Corriente S-201", "Alimentación neta de red tras 43.1% de ahorro por reciclo ZLD.", "Definido"),
        ("RS-03", "Recurso recirculante", "Agua tratada condensada de retorno ZLD", "Área 800 / P-801 a MIX-201", "7003.86", "7704.25", "kg/h", "8000", "56030.88 t/año", "Balance Hídrico ZLD; S-202", "Flujo en circuito cerrado interno; no representa consumo neto.", "Definido"),
        ("RS-04", "Catalizador", "Catalizador Cu/ZnO/Al2O3 para metanol", "Área 400 / Reactor R-401", "0.46", "1.00", "kg/h", "8000", "3.70 t/año", "LE-01C; Haldor Topsoe", "Carga inicial 18.5 t; tasa de reposición estimada cada 3-4 años.", "Definido"),
        ("RS-05", "Catalizador / Stacks", "Celdas cerámicas SOEC (YSZ/Ni-YSZ)", "Área 200 / EL-201", "Módulo 54.4 MWe", "Sobre-diseño 10%", "Stack", "8000", "10% recambio/año", "Bases de Diseño SOEC", "Tasa de degradación de 0.5% por 1,000 h; vida útil 5 años.", "Definido"),
        ("RS-06", "Consumible", "Resinas intercambio iónico y membranas OI", "Área 100 y 800 (Trat. Agua)", "1 juego", "1 juego", "Juego/año", "8000", "0.50 juego/año", "Hojas técnicas tratamiento", "Reposición bianual programada en paros mayores.", "Preliminar"),
        ("RS-07", "Electricidad", "Potencia eléctrica total de planta (Neta)", "Subestación 60 MVA / Toda planta", "55436.39", "60980.03", "kW", "8000", "443491.12 MWh/año", "Documento TE-01 consolidado", "= 55,436.39 kW * 8,000 h/año (absorbe 98.1% la SOEC).", "Definido"),
        ("RS-08", "Electricidad", "Electrólisis de vapor SOEC de alta T", "Área 200 / EL-201", "38067.30", "41874.03", "kW", "8000", "304538.40 MWh/año", "DWSIM v1; TE-01", "Consumo específico de 32.92 kWh/kg H2 (Escenario D: 800°C, 20 bar).", "Definido"),
        ("RS-09", "Electricidad", "Sobrecalentador eléctrico de vapor E-202", "Área 200 / E-202", "5248.42", "5773.26", "kW", "8000", "41987.36 MWh/año", "DWSIM v1; TE-01", "Sobrecalentamiento eléctrico de 212.4°C a 800°C.", "Definido"),
        ("RS-10", "Electricidad", "Compresor syngas multietapa C-301", "Área 300 / C-301", "1316.67", "1448.34", "kW", "8000", "10533.36 MWh/año", "DWSIM v1; TE-01", "Compresión de 19.4 a 75.0 bar con eficiencia isentrópica 78%.", "Definido"),
        ("RS-11", "Electricidad", "Soplador centrífugo de reciclo C-501", "Área 500 / C-501", "150.00", "165.00", "kW", "8000", "1200.00 MWh/año", "DWSIM v1; TE-01", "Impulso de 14,726 kg/h venciendo delta P = 1.5 bar.", "Definido"),
        ("RS-12", "Electricidad generada", "Turboexpansor de purga EXP-501 (X-501)", "Área 500 / EXP-501", "-437.79", "-481.57", "kW", "8000", "-3502.32 MWh/año", "DWSIM v1; TE-01", "Crédito eléctrico por expansión criogénica de 75 a 1.1 bar.", "Definido"),
        ("RS-13", "Electricidad", "Bombas de proceso auxiliares (P-201/601/602/801)", "Áreas 200, 600 y 800", "14.63", "16.09", "kW", "8000", "117.04 MWh/año", "DWSIM v1; TE-01", "Suma de potencias hidráulicas y mecánicas de bombeo.", "Definido"),
        ("RS-14", "Servicio (circulante)", "Agua de enfriamiento circulante (CW)", "E-203, E-501, E-601", "2218.36", "2440.20", "m³/h", "8000", "17746880 m³/año", "Balance térmico CW (TE-01)", "Flujo en circuito cerrado con delta T = 10°C (Q = 25,782 kW).", "Definido"),
        ("RS-15", "Servicio (reposición)", "Agua de enfriamiento make-up reposición", "Torres de enfriamiento", "33.28", "36.60", "m³/h", "8000", "266240 m³/año", "Cálculo evaporación/purga", "Equivale al 1.50% del flujo de circulación en torres.", "Definido"),
        ("RS-16", "Servicio caliente", "Vapor de calentamiento LP (3.5 bar)", "Área 600 / Rehervidor E-602", "5474.90", "6022.39", "kg/h", "8000", "43799.20 t/año", "DWSIM v1; TE-01", "Carga térmica 3,266.68 kW (condensado 100% recuperado).", "Definido"),
        ("RS-17", "Refrigeración", "Agua helada / Chilled water (7°C -> 12°C)", "Área 600 / Subenfriador E-603", "19.12", "21.03", "m³/h", "8000", "152960 m³/año", "DWSIM v1; TE-01", "Carga térmica 111.11 kW para subenfriar metanol a 35°C.", "Definido"),
        ("RS-18", "Servicio auxiliar", "Aire de instrumentos seco (-40°C dp, 7 bar)", "Lazos de control y válvulas SIS", "150.00", "200.00", "Nm³/h", "8000", "1200000 Nm³/año", "Estimación 35 válvulas DCS", "Consumo continuo de actuadores neumáticos y posicionadores.", "Definido"),
        ("RS-19", "Servicio auxiliar", "Nitrógeno gas inerte (N2)", "Parque tanques / TK-601 / Purgas", "15.00", "50.00", "Nm³/h", "8000", "120000 Nm³/año", "Cálculo inertización API 2000", "Colchón permanente en tanque TK-601 y purgas de puesta en marcha.", "Definido"),
        ("RS-20", "Producto principal", "e-Metanol Grado Químico AA (>99.85%)", "Área 600 / Corriente S-604", "3788.65", "4167.52", "kg/h", "8000", "30309.20 t/año", "DWSIM v1; Corriente S-604", "Producción neta vendible con 99.89% p/p de pureza.", "Definido"),
        ("RS-21", "Subproducto", "Oxígeno gaseoso puro (O2 >= 99.9%)", "Área 200 / Corriente S-206", "10098.76", "11108.64", "kg/h", "8000", "80790.08 t/año", "DWSIM v1; Corriente S-206", "Generación anódica en SOEC a 19.4 bar (315.6 kmol/h).", "Definido"),
        ("RS-22", "Subproducto energético", "Gas de purga continua despresurizado", "Área 500 / Corriente S-506", "613.59", "674.95", "kg/h", "8000", "4908.72 t/año", "DWSIM v1; Corriente S-506", "Purga de inertes (4%) enviada a red de gas combustible Pemex.", "Definido"),
        ("RS-23", "Emisión gaseosa", "Venteo de ligeros desgasificados flash LP", "Área 600 / Corriente S-601", "6.57", "10.00", "kg/h", "8000", "52.56 t/año", "DWSIM v1; Corriente S-601", "Venteo controlado a cabezal de recuperación o antorcha LP.", "Definido"),
        ("RS-24", "Residuo / Efluente", "Purga de lodos salinos concentrados ZLD", "Área 800 / Corriente S-804", "0.56", "1.20", "kg/h", "8000", "4.48 t/año", "Balance Hídrico ZLD; S-804", "Salmuera residual confinada para disposición ecológica.", "Definido")
    ]
    
    # Hoja A: Tasas normales y máximas
    ws_a = wb.active
    ws_a.title = "F-PIB-03A_Tasas"
    apply_styling(ws_a, "DOCUMENTO F-PIB-03 (PARTE A)", "TASAS NORMALES Y MÁXIMAS DE RECURSOS, SERVICIOS Y SALIDAS")
    
    headers_a = ["ID", "Clasificación", "Concepto / Recurso", "Equipo / Sección", "Tasa Normal", "Tasa Máxima", "Unidad"]
    ws_a.append([])
    ws_a.append(headers_a)
    
    for r in recursos:
        ws_a.append([r[0], r[1], r[2], r[3], r[4], r[5], r[6]])
        
    for col in range(1, 8):
        c = ws_a.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_a.max_row + 1):
        ws_a.row_dimensions[r].height = 22
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 8):
            cell = ws_a.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 2, 7]: cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col in [5, 6]: cell.alignment = Alignment(horizontal="right", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_a, 7)

    # Hoja B: Cantidades anuales y supuestos
    ws_b = wb.create_sheet(title="F-PIB-03B_Anualizacion")
    apply_styling(ws_b, "DOCUMENTO F-PIB-03 (PARTE B)", "ANUALIZACIÓN, FUENTES Y SUPUESTOS DE CÁLCULO")
    
    headers_b = ["ID", "Horas / Año", "Cantidad Anual Consolidada", "Fuente de Datos", "Supuesto / Método de Anualización", "Estado"]
    ws_b.append([])
    ws_b.append(headers_b)
    
    for r in recursos:
        ws_b.append([r[0], r[7], r[8], r[9], r[10], r[11]])
        
    for col in range(1, 7):
        c = ws_b.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_b.max_row + 1):
        ws_b.row_dimensions[r].height = 22
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 7):
            cell = ws_b.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 2, 6]: cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col in [3]: cell.alignment = Alignment(horizontal="right", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_b, 6)

    wb.save(filename)
    print(f"Generado exitosamente: {filename}")

# 4. GENERAR F-PIB-04: PENDIENTES Y VERIFICACIÓN FINAL
def generar_f_pib_04(filename):
    wb = openpyxl.Workbook()
    
    pendientes = [
        # ID, Tipo, Descripcion, DocsAfectados, Impacto, AccionRequerida, Responsable, FechaObjetivo, Estado, Evidencia
        (
            "TBD-01", "Pendiente técnico",
            "Simulación y modelado tecno-económico riguroso en BioSTEAM por equipo y sistema de proceso.",
            "BioSTEAM, LE-01, PIB-01", "Impide calcular en detalle el CAPEX, OPEX y LCOMe del e-metanol.",
            "Desarrollar e integrar scripts en Python con módulo biosteam.TEA validando contra DWSIM v1.",
            "Ing. Grecia Figueroa Rincón / Ing. Paulina Mota Macip", "Etapa Posterior E3", "En proceso",
            "Repositorio GitHub scripts Python BioSTEAM"
        ),
        (
            "TBD-02", "Pendiente técnico",
            "Determinación rigurosa de coeficientes globales de transferencia U y áreas TEMA en intercambiadores E-203, E-501, E-502, E-601.",
            "Hojas de datos HDE, F-PIB-02", "Las áreas actuales son aproximaciones de simulación preliminar.",
            "Efectuar dimensionamiento térmico detallado en software HTRI / Bell-Delaware.",
            "Ing. Paulina Mota Macip", "Sesión 7 / Fase E3", "Abierto",
            "Memorias de cálculo térmico HTRI"
        ),
        (
            "TBD-03", "Pendiente técnico",
            "Curvas características de operación, punto de diseño y lazo anti-surge del compresor C-301.",
            "DTI v1, LE-01, F-PIB-02", "Falta afinar la línea de recirculación anti-surge y especificación de potencia de motor VFD.",
            "Solicitar hojas de datos a fabricantes (Elliott / Siemens) y simular curva H-Q.",
            "Ing. Gildardo Ocaña Barrales", "Sesión 8 / Fase E3", "Abierto",
            "Hoja de datos del fabricante C-301"
        ),
        (
            "TBD-04", "Pendiente técnico",
            "Hidráulica de platos de la torre T-601 (espaciado, caída de presión real, tipo de válvulas fijas/móviles).",
            "DTI v1, LE-01, F-PIB-02", "Las 24 etapas teóricas de DWSIM requieren validación física de inundación (flooding) y arrastre.",
            "Efectuar cálculo hidráulico riguroso con método Fair / software FRI.",
            "Ing. Karol Paola Camacho López", "Sesión 8 / Fase E3", "Abierto",
            "Memoria hidráulica de torre T-601"
        ),
        (
            "TBD-05", "Pendiente técnico",
            "Calidad físico-química estacional del agua cruda de suministro en sitio industrial de referencia.",
            "Balance ZLD, F-PIB-03", "Posible variación en conductividad, sílice y dureza que altere tasa de reposición de resinas.",
            "Obtener análisis fisicoquímico oficial con Conagua y Pemex polo industrial adyacente.",
            "Ing. Grecia Figueroa Rincón", "Sesión 7 / Fase E3", "Abierto",
            "Reporte de laboratorio de calidad de agua"
        ),
        (
            "INC-01", "Inconsistencia",
            "Discrepancia inicial entre el volumen flash de V-501 en simulación DWSIM preliminar (15 m³) y la lista LE-01C (12 m³).",
            "DWSIM v0, LE-01C, F-PIB-02", "Inconsistencia documental en tiempo de residencia de líquido.",
            "Se unificó el volumen útil a 14.5 m³ garantizando 10 min de retención de líquido a flujo nominal.",
            "Ing. Paulina Mota Macip", "Sesión 5", "Cerrado",
            "Memoria de cálculo V-501 y DWSIM v1 convergido"
        ),
        (
            "INC-02", "Inconsistencia",
            "Carga térmica del subenfriador E-603 reportada como 95 kW en memoria previa frente a 111.11 kW en DWSIM v1 oficial.",
            "Memoria previa, DWSIM v1, TE-01", "Error en el balance térmico de acondicionamiento de metanol a tanque.",
            "Se actualizó el valor a 111.11 kW exactos de DWSIM v1 en todos los cuadros TE-01 y PIB.",
            "Ing. Paulina Mota Macip", "Sesión 6", "Cerrado",
            "Documento TE-01 y F-PIB-02B actualizados"
        ),
        (
            "INC-03", "Inconsistencia",
            "Presión de suministro de CO2 referida a 1.013 bar en anteproyecto versus 20.0 bar en bases licitatorias RFP-CCM-EM-001.",
            "Bases de Licitación, DTI v0.2, F-PIB-01", "Implicaba añadir innecesariamente un compresor de 4 etapas para CO2.",
            "Se confirmó con cliente que el CO2 llega a 20.0 bar isobárico a límite de batería, eliminando equipo ficticio.",
            "Ing. Karol Paola Camacho López", "Sesión 4", "Cerrado",
            "Acta aclaratoria licitación y DTI v0.2"
        ),
        (
            "HZ-01", "Acción HAZOP abierta",
            "Confirmar dimensionamiento y contrapresión de descarga de válvula de alivio PSV-501 del bucle de 75 bar hacia antorcha.",
            "Expediente HAZOP, DTI-v0.2, MCE-01", "Descarga segura ante bloqueo de bucle o incendio no debe sobrepasar contrapresión máxima en flare.",
            "Realizar cálculo de flujo de alivio bifásico según API 520/521 y modelar tubería hacia flare header.",
            "Ing. Grecia Figueroa Rincón / Ing. Gildardo Ocaña", "Antes de emitir DTI v1.0", "En proceso",
            "Memoria de dimensionamiento PSV-501 según API 520"
        ),
        (
            "HZ-02", "Acción HAZOP abierta",
            "Definir tiempo de respuesta de válvula de cierre estanco SDV-501 ante fenómeno de gas blow-by en flash V-501.",
            "Expediente HAZOP nodo 5, DTI-02 v1", "Si la SDV tarda más de 2 s en cerrar ante nivel muy bajo LALL-501, se transferirá gas a 75 bar al desgasificador V-601 de 1.25 bar.",
            "Especificar actuador neumático de acción ultrarrápida (cierre menor a 1.0 segundo con solenoide desenergizada).",
            "Ing. Paulina Mota Macip / Ing. Gildardo Ocaña", "Antes de emitir DTI v1.0", "En revisión",
            "Hoja de especificación de válvula SDV-501 certificada < 1.0 s"
        ),
        (
            "HZ-03", "Acción HAZOP abierta",
            "Validar sistema de inertización con N2 y venteo de emergencia en tanque TK-601 según API 2000.",
            "Expediente HAZOP nodo 6, DTI-v0.2, F-PIB-02", "Prevenir formación de mezcla inflamable en espacio de vapor y sobrepresión por radiación solar.",
            "Diseñar lazo de control PIC-604 con colchón de N2 a +20 mm H2O y válvula PVRV con arrestallamas.",
            "Ing. Grecia Figueroa Rincón", "Antes de emitir DTI v1.0", "En proceso",
            "Plano de instrumentación y hoja de datos PVRV-601"
        ),
        (
            "OT-01", "Otro pendiente",
            "Verificación de interferencias de tuberías críticas (spool de alta presión 75 bar y vapor SOEC 800°C) en modelo 3D.",
            "Plant 3D, Arreglo General AG-01", "Riesgo de choque mecánico o expansión térmica excesiva.",
            "Ejecutar análisis de flexibilidad de tuberías con CAESAR II en líneas S-205 y S-401.",
            "Ing. Gildardo Ocaña Barrales", "Fase E3", "Abierto",
            "Reporte de análisis de esfuerzos CAESAR II"
        )
    ]
    
    # Hoja A: Identificación
    ws_a = wb.active
    ws_a.title = "F-PIB-04A_Identificacion"
    apply_styling(ws_a, "DOCUMENTO F-PIB-04 (PARTE A)", "IDENTIFICACIÓN DE PENDIENTES, INCONSISTENCIAS Y ACCIONES HAZOP")
    
    headers_a = ["ID", "Tipo", "Descripción Precisa del Problema o Dato Faltante", "Documentos Afectados", "Impacto Operativo / Seguridad"]
    ws_a.append([])
    ws_a.append(headers_a)
    
    for p in pendientes:
        ws_a.append([p[0], p[1], p[2], p[3], p[4]])
        
    for col in range(1, 6):
        c = ws_a.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_a.max_row + 1):
        ws_a.row_dimensions[r].height = 28
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 6):
            cell = ws_a.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 2]: cell.alignment = Alignment(horizontal="center", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_a, 5)

    # Hoja B: Seguimiento y cierre
    ws_b = wb.create_sheet(title="F-PIB-04B_Seguimiento")
    apply_styling(ws_b, "DOCUMENTO F-PIB-04 (PARTE B)", "SEGUIMIENTO, ACCIONES REQUERIDAS, RESPONSABLES Y CIERRE")
    
    headers_b = ["ID", "Acción Específica Requerida", "Responsable Asignado", "Fecha Objetivo", "Estado Actual", "Evidencia Verificable de Cierre"]
    ws_b.append([])
    ws_b.append(headers_b)
    
    for p in pendientes:
        ws_b.append([p[0], p[5], p[6], p[7], p[8], p[9]])
        
    for col in range(1, 7):
        c = ws_b.cell(row=4, column=col)
        c.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_b.max_row + 1):
        ws_b.row_dimensions[r].height = 28
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 7):
            cell = ws_b.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 4, 5]: cell.alignment = Alignment(horizontal="center", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_b, 6)

    wb.save(filename)
    print(f"Generado exitosamente: {filename}")

# 5. GENERAR SOLVANTA_TC-01.XLSX: TABLA DE CORRIENTES
def generar_tc_01(filename):
    wb = openpyxl.Workbook()
    
    corrientes_prop = [
        # ID, Descripcion, Fase, T, P, MassFlow, MolFlow, FracVap
        ("S-101", "Alimentación CO2 de captura externa", "Vapor", 25.0, 20.00, 5274.34, 121.000, 1.00),
        ("S-201", "Agua make-up fresca de red", "Líquido", 25.0, 20.00, 9241.84, 513.000, 0.00),
        ("S-202", "Retorno agua tratada circuito ZLD", "Líquido", 59.2, 20.00, 7003.86, 388.768, 0.00),
        ("S-203", "Agua combinada de caldera", "Líquido", 39.8, 20.00, 16244.88, 901.722, 0.00),
        ("S-204", "Vapor saturado 20 bar generado en caldera", "Vapor", 220.0, 20.00, 16244.88, 901.722, 1.00),
        ("S-205", "Vapor sobrecalentado a 800°C hacia SOEC", "Vapor", 800.0, 20.00, 16244.88, 901.722, 1.00),
        ("S-206", "Oxígeno puro SOEC (ánodo)", "Vapor", 31.0, 19.40, 10098.76, 315.598, 1.00),
        ("S-207", "Efluente catódico húmedo SOEC", "Vapor", 800.0, 19.40, 6145.79, 901.712, 1.00),
        ("S-208", "Efluente SOEC enfriado bifásico", "Bifásica", 38.0, 19.40, 6145.79, 901.712, 0.70),
        ("S-209", "Hidrógeno verde seco puro", "Vapor", 38.0, 19.40, 1314.77, 633.548, 1.00),
        ("S-210", "Condensado hídrico SOEC no disociado", "Líquido", 38.0, 19.40, 4831.02, 268.165, 0.00),
        ("S-301", "Syngas fresco combinado (M=2.05)", "Vapor", 32.9, 19.40, 6589.11, 754.548, 1.00),
        ("S-302", "Syngas precalentado a succión C-301", "Vapor", 71.7, 19.40, 6589.11, 754.548, 1.00),
        ("S-303", "Syngas comprimido a 75 bar de descarga", "Vapor", 271.0, 75.00, 6589.11, 754.548, 1.00),
        ("S-401", "Alimentación combinada a reactor R-401", "Vapor", 83.2, 75.00, 21308.08, 7387.096, 1.00),
        ("S-402", "Efluente reactivo síntesis metanol", "Vapor", 245.0, 75.00, 21308.08, 7149.098, 1.00),
        ("S-403", "Efluente economizado en FEHE", "Vapor", 224.6, 75.00, 21308.08, 7149.098, 1.00),
        ("S-404", "Efluente condensado bifásico a V-501", "Bifásica", 38.0, 75.00, 21308.08, 7149.098, 0.97),
        ("S-501", "Gas en domo de flash HP", "Vapor", 38.0, 75.00, 15339.75, 6909.568, 1.00),
        ("S-502", "Gas bucle sobrecalentado", "Vapor", 60.0, 75.00, 15339.75, 6909.568, 1.00),
        ("S-503", "Gas de reciclo circulante (96%)", "Vapor", 60.0, 75.00, 14726.16, 6633.185, 1.00),
        ("S-504_OUT", "Gas de reciclo impulsado por C-501", "Vapor", 60.0, 75.00, 14726.16, 6633.185, 1.00),
        ("S-505", "Gas de purga continua de inertes (4%)", "Vapor", 60.0, 75.00, 613.59, 276.383, 1.00),
        ("S-506", "Purga expandida tras turboexpansor", "Bifásica", -138.6, 1.10, 613.59, 276.383, 1.00),
        ("S-507", "Metanol crudo líquido de fondo flash HP", "Líquido", 38.0, 75.00, 5968.39, 239.530, 0.00),
        ("S-507A", "Metanol crudo tras válvula JT (1.25 bar)", "Bifásica", 38.0, 1.25, 5968.39, 239.530, 0.01),
        ("S-601", "Venteo gases disueltos flash LP", "Bifásica", 38.0, 1.25, 6.57, 0.556, 0.91),
        ("S-602", "Metanol crudo desgasificado a bomba", "Líquido", 38.0, 1.25, 5961.82, 238.975, 0.00),
        ("S-602A", "Metanol crudo presurizado a plato 18", "Líquido", 38.0, 2.20, 5961.82, 238.975, 0.00),
        ("S-603", "Vapores de metanol en domo de torre", "Líquido", 68.5, 1.20, 3788.65, 118.341, 0.00),
        ("S-604", "e-Metanol Comercial Grado Químico AA", "Líquido", 35.0, 1.10, 3788.65, 118.341, 0.00),
        ("S-605", "Fondos de columna fraccionadora T-601", "Líquido", 103.9, 1.25, 2173.40, 120.634, 0.00),
        ("S-801", "Efluente hídrico combinado a ZLD", "Líquido", 58.9, 1.25, 7004.41, 388.798, 0.00),
        ("S-802", "Agua clarificada y filtrada ZLD", "Líquido", 58.9, 1.25, 7004.41, 388.798, 0.00),
        ("S-803", "Agua desmineralizada impulsada a caldera", "Líquido", 59.2, 20.00, 7004.41, 388.798, 0.00),
        ("S-804", "Purga de lodos salinos concentrados ZLD", "Líquido", 58.9, 1.25, 0.56, 0.030, 0.00)
    ]
    
    # Composición molar
    composiciones = [
        # ID, x_CO2, x_CO, x_H2, x_H2O, x_MeOH, x_O2
        ("S-101", 0.9900, 0.0000, 0.0100, 0.0000, 0.0000, 0.0000),
        ("S-201", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-202", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-203", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-204", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-205", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-206", 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000),
        ("S-207", 0.0000, 0.0000, 0.7000, 0.3000, 0.0000, 0.0000),
        ("S-208", 0.0000, 0.0000, 0.7000, 0.3000, 0.0000, 0.0000),
        ("S-209", 0.0000, 0.0000, 0.9963, 0.0037, 0.0000, 0.0000),
        ("S-210", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-301", 0.1588, 0.0000, 0.8381, 0.0031, 0.0000, 0.0000),
        ("S-302", 0.1588, 0.0000, 0.8381, 0.0031, 0.0000, 0.0000),
        ("S-303", 0.1588, 0.0000, 0.8381, 0.0031, 0.0000, 0.0000),
        ("S-401", 0.0183, 0.0000, 0.9776, 0.0016, 0.0025, 0.0000),
        ("S-402", 0.0023, 0.0000, 0.9603, 0.0183, 0.0192, 0.0000),
        ("S-403", 0.0023, 0.0000, 0.9603, 0.0183, 0.0192, 0.0000),
        ("S-404", 0.0023, 0.0000, 0.9603, 0.0183, 0.0192, 0.0000),
        ("S-501", 0.0023, 0.0000, 0.9935, 0.0014, 0.0028, 0.0000),
        ("S-502", 0.0023, 0.0000, 0.9935, 0.0014, 0.0028, 0.0000),
        ("S-503", 0.0023, 0.0000, 0.9935, 0.0014, 0.0028, 0.0000),
        ("S-504_OUT", 0.0023, 0.0000, 0.9935, 0.0014, 0.0028, 0.0000),
        ("S-505", 0.0023, 0.0000, 0.9935, 0.0014, 0.0028, 0.0000),
        ("S-506", 0.0023, 0.0000, 0.9935, 0.0014, 0.0028, 0.0000),
        ("S-507", 0.0004, 0.0000, 0.0017, 0.5046, 0.4933, 0.0000),
        ("S-507A", 0.0004, 0.0000, 0.0017, 0.5046, 0.4933, 0.0000),
        ("S-601", 0.1729, 0.0000, 0.7420, 0.0000, 0.0850, 0.0000),
        ("S-602", 0.0000, 0.0000, 0.0000, 0.5058, 0.4942, 0.0000),
        ("S-602A", 0.0000, 0.0000, 0.0000, 0.5058, 0.4942, 0.0000),
        ("S-603", 0.0000, 0.0000, 0.0000, 0.0019, 0.9981, 0.0000),
        ("S-604", 0.0000, 0.0000, 0.0000, 0.0019, 0.9981, 0.0000),
        ("S-605", 0.0000, 0.0000, 0.0000, 0.9999, 0.0001, 0.0000),
        ("S-801", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-802", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-803", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-804", 0.0000, 0.0000, 0.0180, 0.9819, 0.0001, 0.0000)
    ]
    
    # Hoja 1: Propiedades Termodinámicas
    ws_a = wb.active
    ws_a.title = "TC-01A_Propiedades"
    apply_styling(ws_a, "DOCUMENTO TC-01 (PARTE A)", "TABLA DE CORRIENTES - PROPIEDADES TERMODINÁMICAS (DWSIM v1)")
    
    headers_a = ["ID Corriente", "Descripción de Tubería / Tramo de Proceso", "Fase", "Temperatura (°C)", "Presión (bar)", "Flujo Másico (kg/h)", "Flujo Molar (kmol/h)", "Fracción Vapor"]
    ws_a.append([])
    ws_a.append(headers_a)
    
    for c in corrientes_prop:
        ws_a.append([c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7]])
        
    for col in range(1, 9):
        cell = ws_a.cell(row=4, column=col)
        cell.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_a.max_row + 1):
        ws_a.row_dimensions[r].height = 20
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 9):
            cell = ws_a.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col in [1, 3]: cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col in [4, 5, 6, 7, 8]: cell.alignment = Alignment(horizontal="right", vertical="center")
            else: cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    auto_fit_columns(ws_a, 8)

    # Hoja 2: Composición Molar
    ws_b = wb.create_sheet(title="TC-01B_Composicion")
    apply_styling(ws_b, "DOCUMENTO TC-01 (PARTE B)", "TABLA DE CORRIENTES - FRACCIONES MOLARES EXACTAS (DWSIM v1)")
    
    headers_b = ["ID Corriente", "x_CO2", "x_CO", "x_H2", "x_H2O", "x_MeOH", "x_O2", "Suma Fracciones"]
    ws_b.append([])
    ws_b.append(headers_b)
    
    for comp in composiciones:
        suma = sum(comp[1:])
        ws_b.append([comp[0], comp[1], comp[2], comp[3], comp[4], comp[5], comp[6], round(suma, 4)])
        
    for col in range(1, 9):
        cell = ws_b.cell(row=4, column=col)
        cell.font = Font(name="Calibri", size=10, bold=True, color=WHITE_TEXT)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    for r in range(5, ws_b.max_row + 1):
        ws_b.row_dimensions[r].height = 20
        fill = PatternFill(start_color=LIGHT_BLUE_ROW, end_color=LIGHT_BLUE_ROW, fill_type="solid") if r % 2 == 0 else PatternFill(fill_type=None)
        for col in range(1, 9):
            cell = ws_b.cell(row=r, column=col)
            cell.font = Font(name="Calibri", size=9.5)
            if fill.fill_type: cell.fill = fill
            cell.border = Border(left=Side(style='thin', color=BORDER_GRAY), right=Side(style='thin', color=BORDER_GRAY), top=Side(style='thin', color=BORDER_GRAY), bottom=Side(style='thin', color=BORDER_GRAY))
            if col == 1: cell.alignment = Alignment(horizontal="center", vertical="center")
            else: cell.alignment = Alignment(horizontal="right", vertical="center")
    auto_fit_columns(ws_b, 8)

    wb.save(filename)
    print(f"Generado exitosamente: {filename}")

if __name__ == "__main__":
    base_dir = "Entregables/PIB-01_Solvanta"
    generar_f_pib_01(f"{base_dir}/Solvanta_F-PIB-01.xlsx")
    generar_f_pib_02(f"{base_dir}/Solvanta_F-PIB-02.xlsx")
    generar_f_pib_03(f"{base_dir}/Solvanta_F-PIB-03.xlsx")
    generar_f_pib_04(f"{base_dir}/Solvanta_F-PIB-04.xlsx")
    generar_tc_01(f"{base_dir}/Solvanta_TC-01.xlsx")

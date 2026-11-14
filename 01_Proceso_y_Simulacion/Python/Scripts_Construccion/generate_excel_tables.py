import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_tc01(filename):
    wb = openpyxl.Workbook()
    
    # HOJA 1: TC-01A Resumen de Corrientes
    ws1 = wb.active
    ws1.title = "TC-01A_Resumen"
    
    # Colores corporativos Solvanta
    navy_fill = PatternFill(start_color="1A4F7C", end_color="1A4F7C", fill_type="solid")
    sub_fill = PatternFill(start_color="E8EFF5", end_color="E8EFF5", fill_type="solid")
    highlight_fill = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
    
    title_font = Font(name="Arial", size=14, bold=True, color="1A4F7C")
    sub_font = Font(name="Arial", size=10, italic=True, color="555555")
    header_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    bold_font = Font(name="Arial", size=10, bold=True)
    normal_font = Font(name="Arial", size=10)
    
    thin_border = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )
    header_border = Border(
        left=Side(style='thin', color='1A4F7C'),
        right=Side(style='thin', color='1A4F7C'),
        top=Side(style='medium', color='1A4F7C'),
        bottom=Side(style='medium', color='1A4F7C')
    )

    ws1.merge_cells("A1:H1")
    ws1["A1"] = "SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V."
    ws1["A1"].font = title_font
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1.merge_cells("A2:H2")
    ws1["A2"] = "DOCUMENTO TC-01A: TABLA MAESTRA DE CORRIENTES DE MATERIA (RESUMEN FÍSICO)"
    ws1["A2"].font = Font(name="Arial", size=11, bold=True, color="1A4F7C")
    ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")

    ws1.merge_cells("A3:H3")
    ws1["A3"] = "Planta de Producción de e-Metanol (30 000 t/año) | Caso Aprobado: DWSIM_v1_APROBADA_Solvanta"
    ws1["A3"].font = sub_font
    ws1["A3"].alignment = Alignment(horizontal="center", vertical="center")

    headers_1 = [
        "ID Corriente", "Descripción de Proceso", "Fase", 
        "Temperatura (°C)", "Presión (bar)", "Flujo Másico (kg/h)", 
        "Flujo Molar (kmol/h)", "Fracción Vapor"
    ]
    
    row_num = 5
    for col_idx, h in enumerate(headers_1, start=1):
        cell = ws1.cell(row=row_num, column=col_idx, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border
    ws1.row_dimensions[row_num].height = 26

    streams_tc01a = [
        ("S-01", "Alimentación de CO2 de captura", "Vapor", 25.0, 20.00, 5222.4, 119.81, 1.00),
        ("S-03_MK", "Agua fresca externa de red", "Líquido", 25.0, 20.00, 9240.9, 512.95, 0.00),
        ("S-ZLD_REC", "Retorno de agua tratada en ZLD", "Líquido", 38.7, 20.00, 6979.3, 387.41, 0.00),
        ("S-03", "Agua combinada a caldera E-201", "Líquido", 30.9, 20.00, 16219.9, 900.34, 0.00),
        ("S-03B", "Vapor saturado domo de caldera", "Vapor", 220.0, 20.00, 16219.9, 900.34, 1.00),
        ("S-04", "Vapor sobrecalentado a SOEC", "Vapor", 750.0, 20.00, 16219.9, 900.34, 1.00),
        ("S-05", "Oxígeno puro coproducto SOEC", "Vapor", 31.0, 19.40, 10083.4, 315.12, 1.00),
        ("S-06", "Efluente húmedo cátodo SOEC", "Vapor", 750.0, 19.40, 6136.5, 900.34, 1.00),
        ("S-07", "Hidrógeno seco a mezcla", "Vapor", 38.0, 19.40, 1312.8, 632.58, 1.00),
        ("S-08", "Condensado SOEC hacia ZLD", "Líquido", 38.0, 19.40, 4823.7, 267.76, 0.00),
        ("S-08B", "Syngas fresco combinado", "Vapor", 32.7, 19.40, 6535.2, 752.39, 1.00),
        ("S-09", "Syngas comprimido C-301", "Vapor", 212.3, 75.00, 6535.2, 752.39, 1.00),
        ("S-09_TOT", "Alimentación total a reactor R-401", "Vapor", 57.6, 75.00, 20779.2, 7153.98, 1.00),
        ("S-10", "Efluente de reacción R-401", "Vapor", 245.0, 75.00, 20779.2, 6918.23, 1.00),
        ("S-REC", "Gas de domo flash V-501 (reciclo)", "Vapor", 38.0, 75.00, 14862.8, 6680.78, 1.00),
        ("S-12", "Reciclo 96% a economizador E-601", "Vapor", 43.0, 75.00, 14268.3, 6413.54, 1.00),
        ("S-13", "Purga 4% a turboexpansor X-601", "Vapor", 43.0, 75.00, 594.5, 267.23, 1.00),
        ("S-P_VENT", "Purga venteo tras X-601", "Bifásica", -145.2, 1.10, 594.5, 267.23, 0.98),
        ("S-11", "Metanol crudo líquido flash HP", "Líquido", 38.0, 75.00, 5916.5, 237.45, 0.00),
        ("S-VENT", "Venteo ligeros desgasificador V-701", "Vapor", 38.0, 3.00, 9.0, 0.62, 1.00),
        ("S-14", "Metanol crudo a torre T-701", "Líquido", 38.0, 3.00, 5925.1, 237.61, 0.00),
        ("S-15", "e-Metanol Grado AA (Producto)", "Líquido", 35.0, 1.10, 3755.6, 117.35, 0.00),
        ("S-16", "Agua residual de fondo T-701", "Líquido", 103.9, 1.25, 2169.5, 120.26, 0.00),
        ("S-ZLD_P", "Agua purificada ZLD a bomba P-801", "Líquido", 38.7, 19.40, 6979.3, 387.41, 0.00),
        ("S-ZLD_S", "Purga de lodos salinos ZLD", "Bifásica", 38.7, 19.40, 10.8, 0.69, 0.01)
    ]

    for s in streams_tc01a:
        row_num += 1
        ws1.row_dimensions[row_num].height = 19
        is_product = (s[0] == "S-15")
        
        ws1.cell(row=row_num, column=1, value=s[0]).alignment = Alignment(horizontal="center")
        ws1.cell(row=row_num, column=2, value=s[1]).alignment = Alignment(horizontal="left")
        ws1.cell(row=row_num, column=3, value=s[2]).alignment = Alignment(horizontal="center")
        
        c4 = ws1.cell(row=row_num, column=4, value=s[3])
        c4.number_format = "0.0"
        c4.alignment = Alignment(horizontal="right")
        
        c5 = ws1.cell(row=row_num, column=5, value=s[4])
        c5.number_format = "0.00"
        c5.alignment = Alignment(horizontal="right")
        
        c6 = ws1.cell(row=row_num, column=6, value=s[5])
        c6.number_format = "#,##0.0"
        c6.alignment = Alignment(horizontal="right")
        
        c7 = ws1.cell(row=row_num, column=7, value=s[6])
        c7.number_format = "#,##0.00"
        c7.alignment = Alignment(horizontal="right")
        
        c8 = ws1.cell(row=row_num, column=8, value=s[7])
        c8.number_format = "0.00"
        c8.alignment = Alignment(horizontal="center")

        for col_idx in range(1, 9):
            cell = ws1.cell(row=row_num, column=col_idx)
            cell.border = thin_border
            if is_product:
                cell.fill = highlight_fill
                cell.font = bold_font
            else:
                cell.font = normal_font

    # HOJA 2: TC-01B Composición Molar de Corrientes
    ws2 = wb.create_sheet(title="TC-01B_Composicion")

    ws2.merge_cells("A1:H1")
    ws2["A1"] = "SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V."
    ws2["A1"].font = title_font
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws2.merge_cells("A2:H2")
    ws2["A2"] = "DOCUMENTO TC-01B: COMPOSICIÓN MOLAR DE CORRIENTES DE MATERIA"
    ws2["A2"].font = Font(name="Arial", size=11, bold=True, color="1A4F7C")
    ws2["A2"].alignment = Alignment(horizontal="center", vertical="center")

    headers_2 = ["ID Corriente", "x_H2", "x_CO2", "x_CO", "x_H2O", "x_MeOH", "x_Inertes", "Suma x_i"]
    row_num = 4
    for col_idx, h in enumerate(headers_2, start=1):
        cell = ws2.cell(row=row_num, column=col_idx, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border
    ws2.row_dimensions[row_num].height = 24

    comp_data = [
        ("S-01", 0.0000, 0.9900, 0.0000, 0.0000, 0.0000, 0.0100),
        ("S-03_MK", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-ZLD_REC", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-03", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-03B", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-04", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-05", 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000),
        ("S-06", 0.7000, 0.0000, 0.0000, 0.3000, 0.0000, 0.0000),
        ("S-07", 0.9958, 0.0000, 0.0000, 0.0042, 0.0000, 0.0000),
        ("S-08", 0.0001, 0.0000, 0.0000, 0.9999, 0.0000, 0.0000),
        ("S-08B", 0.8378, 0.1575, 0.0000, 0.0031, 0.0000, 0.0016),
        ("S-09", 0.8378, 0.1575, 0.0000, 0.0031, 0.0000, 0.0016),
        ("S-09_TOT", 0.7331, 0.0981, 0.0000, 0.0008, 0.0011, 0.1669),
        ("S-10", 0.6970, 0.0880, 0.0000, 0.0175, 0.0176, 0.1799),
        ("S-REC", 0.7208, 0.0911, 0.0000, 0.0005, 0.0012, 0.1864),
        ("S-12", 0.7208, 0.0911, 0.0000, 0.0005, 0.0012, 0.1864),
        ("S-13", 0.7208, 0.0911, 0.0000, 0.0005, 0.0012, 0.1864),
        ("S-P_VENT", 0.7208, 0.0911, 0.0000, 0.0005, 0.0012, 0.1864),
        ("S-11", 0.0028, 0.0048, 0.0000, 0.5052, 0.4939, 0.0003),
        ("S-VENT", 0.2542, 0.7180, 0.0000, 0.0012, 0.0266, 0.0000),
        ("S-14", 0.0000, 0.0000, 0.0000, 0.5061, 0.4939, 0.0000),
        ("S-15", 0.0000, 0.0000, 0.0000, 0.0027, 0.9973, 0.0000),
        ("S-16", 0.0000, 0.0000, 0.0000, 0.9990, 0.0010, 0.0000),
        ("S-ZLD_P", 0.0000, 0.0000, 0.0000, 1.0000, 0.0000, 0.0000),
        ("S-ZLD_S", 0.0000, 0.0000, 0.0000, 0.9850, 0.0000, 0.0150)
    ]

    for c in comp_data:
        row_num += 1
        ws2.row_dimensions[row_num].height = 19
        is_product = (c[0] == "S-15")
        
        ws2.cell(row=row_num, column=1, value=c[0]).alignment = Alignment(horizontal="center")
        for col_idx in range(2, 8):
            cell = ws2.cell(row=row_num, column=col_idx, value=c[col_idx-1])
            cell.number_format = "0.0000"
            cell.alignment = Alignment(horizontal="right")
        
        sum_cell = ws2.cell(row=row_num, column=8, value=f"=SUM(B{row_num}:G{row_num})")
        sum_cell.number_format = "0.0000"
        sum_cell.alignment = Alignment(horizontal="right")
        
        for col_idx in range(1, 9):
            cell = ws2.cell(row=row_num, column=col_idx)
            cell.border = thin_border
            if is_product:
                cell.fill = highlight_fill
                cell.font = bold_font
            else:
                cell.font = normal_font

    # Autoajustar anchos de columnas
    for ws in [ws1, ws2]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 11)
            
    wb.save(filename)
    print(f"Created {filename}")

def create_te01(filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "TE-01_Energia_y_Servicios"

    navy_fill = PatternFill(start_color="1A4F7C", end_color="1A4F7C", fill_type="solid")
    section_fill = PatternFill(start_color="D9E1E8", end_color="D9E1E8", fill_type="solid")
    summary_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    title_font = Font(name="Arial", size=14, bold=True, color="1A4F7C")
    sub_font = Font(name="Arial", size=10, italic=True, color="555555")
    header_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    bold_font = Font(name="Arial", size=10, bold=True)
    normal_font = Font(name="Arial", size=10)

    thin_border = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )
    header_border = Border(
        left=Side(style='thin', color='1A4F7C'),
        right=Side(style='thin', color='1A4F7C'),
        top=Side(style='medium', color='1A4F7C'),
        bottom=Side(style='medium', color='1A4F7C')
    )

    ws.merge_cells("A1:G1")
    ws["A1"] = "SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V."
    ws["A1"].font = title_font
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A2:G2")
    ws["A2"] = "DOCUMENTO TE-01: TABLA MAESTRA DE CORRIENTES DE ENERGÍA Y SERVICIOS"
    ws["A2"].font = Font(name="Arial", size=11, bold=True, color="1A4F7C")
    ws["A2"].alignment = Alignment(horizontal="center", vertical="center")

    ws.merge_cells("A3:G3")
    ws["A3"] = "Base de Operación: 8 000 h/año | Convención: Q > 0 suministrado, Q < 0 retirado/generado"
    ws["A3"].font = sub_font
    ws["A3"].alignment = Alignment(horizontal="center", vertical="center")

    headers = [
        "ID Servicio", "Equipo", "Descripción del Servicio", 
        "Tipo de Energía", "Carga Térmica/Potencia (kW)", 
        "Energía Anual (MWh/año)", "Observaciones de Proceso e Integración"
    ]
    
    row_num = 5
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=row_num, column=col_idx, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = header_border
    ws.row_dimensions[row_num].height = 26

    # 1. Electricidad
    elec_data = [
        ("E-SOEC", "EL-201 (R-201)", "Potencia electrólisis SOEC", "Electricidad", 54402.00, 435216.0, "Red renovable (52.2 MW DC celdas SOEC a 750°C)"),
        ("E-C301", "C-301", "Compresor de syngas fresco", "Electricidad", 1138.70, 9109.6, "Compresión multietapa 20 a 75 bar con intercooling"),
        ("E-C601", "C-601", "Soplador de reciclo de syngas", "Electricidad", 150.00, 1200.0, "Supera pérdidas de carga en lazo de síntesis a 75 bar"),
        ("E-P801", "P-801", "Bomba multietapa retorno ZLD", "Electricidad", 0.20, 1.6, "Impulsión de condensado pulido de 19.4 a 20 bar"),
        ("E-TURB", "X-601", "Turboexpansor de purga de inertes", "Gen. Eléctrica", -390.43, -3123.4, "Recuperación de potencia de expansión 75 a 1.1 bar")
    ]
    
    ws.merge_cells(f"A{row_num+1}:G{row_num+1}")
    ws.cell(row=row_num+1, column=1, value="I. SISTEMA DE POTENCIA ELÉCTRICA Y GENERACIÓN").fill = section_fill
    ws.cell(row=row_num+1, column=1).font = bold_font
    row_num += 1

    for row in elec_data:
        row_num += 1
        ws.row_dimensions[row_num].height = 19
        ws.cell(row=row_num, column=1, value=row[0]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=2, value=row[1]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=3, value=row[2]).alignment = Alignment(horizontal="left")
        ws.cell(row=row_num, column=4, value=row[3]).alignment = Alignment(horizontal="center")
        
        c5 = ws.cell(row=row_num, column=5, value=row[4])
        c5.number_format = "#,##0.00"
        c5.alignment = Alignment(horizontal="right")
        
        c6 = ws.cell(row=row_num, column=6, value=row[5])
        c6.number_format = "#,##0.0"
        c6.alignment = Alignment(horizontal="right")
        
        ws.cell(row=row_num, column=7, value=row[6]).alignment = Alignment(horizontal="left")
        for col_idx in range(1, 8):
            ws.cell(row=row_num, column=col_idx).border = thin_border

    # Fila resumen electrico
    row_num += 1
    ws.merge_cells(f"A{row_num}:D{row_num}")
    ws.cell(row=row_num, column=1, value="Consumo Eléctrico Neto de Planta").font = bold_font
    ws.cell(row=row_num, column=1).alignment = Alignment(horizontal="right")
    
    c_net_kw = ws.cell(row=row_num, column=5, value="=SUM(E7:E11)")
    c_net_kw.font = bold_font
    c_net_kw.number_format = "#,##0.00"
    c_net_kw.alignment = Alignment(horizontal="right")

    c_net_mwh = ws.cell(row=row_num, column=6, value="=E12*8000/1000")
    c_net_mwh.font = bold_font
    c_net_mwh.number_format = "#,##0.0"
    c_net_mwh.alignment = Alignment(horizontal="right")

    ws.cell(row=row_num, column=7, value="Potencia neta equivalente: 55.33 MW").font = bold_font
    for col_idx in range(1, 8):
        c = ws.cell(row=row_num, column=col_idx)
        c.fill = summary_fill
        c.border = thin_border

    # 2. Cargas Térmicas
    row_num += 1
    ws.merge_cells(f"A{row_num}:G{row_num}")
    ws.cell(row=row_num, column=1, value="II. INTEGRACIÓN TÉRMICA, CALENTAMIENTO Y VAPOR").fill = section_fill
    ws.cell(row=row_num, column=1).font = bold_font

    thermal_data = [
        ("E-R401", "R-401", "Reacción exotérmica de síntesis", "Gen. Térmica", -9139.20, 73113.6, "Calor exotérmico cedido a caldera de agua hirviendo a 245°C"),
        ("E-201", "E-201", "Carcasa de caldera de vapor", "Calentamiento", 9139.20, 73113.6, "Absorbe el 100% del calor de R-401 para generar vapor a 20 bar"),
        ("E-601", "E-601", "Economizador gas-gas", "Int. Recup.", 272.05, 2176.4, "Sobrecalienta gas de reciclo de 38°C a 43°C evitando condensación"),
        ("E-202", "E-202", "Sobrecalentador de vapor", "Calentamiento", 5119.20, 40953.6, "Eleva vapor saturado de 220°C a 750°C para la celda SOEC"),
        ("E-702", "E-702", "Rehervidor de torre T-701", "Calentamiento", 3020.00, 24160.0, "Rehervidor termosifón para fraccionar metanol y agua a 103.9°C")
    ]
    for row in thermal_data:
        row_num += 1
        ws.row_dimensions[row_num].height = 19
        ws.cell(row=row_num, column=1, value=row[0]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=2, value=row[1]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=3, value=row[2]).alignment = Alignment(horizontal="left")
        ws.cell(row=row_num, column=4, value=row[3]).alignment = Alignment(horizontal="center")
        
        c5 = ws.cell(row=row_num, column=5, value=row[4])
        c5.number_format = "#,##0.00"
        c5.alignment = Alignment(horizontal="right")
        
        c6 = ws.cell(row=row_num, column=6, value=row[5])
        c6.number_format = "#,##0.0"
        c6.alignment = Alignment(horizontal="right")
        
        ws.cell(row=row_num, column=7, value=row[6]).alignment = Alignment(horizontal="left")
        for col_idx in range(1, 8):
            ws.cell(row=row_num, column=col_idx).border = thin_border

    # 3. Enfriamiento
    row_num += 1
    ws.merge_cells(f"A{row_num}:G{row_num}")
    ws.cell(row=row_num, column=1, value="III. SISTEMA DE ENFRIAMIENTO Y CONDENSACIÓN").fill = section_fill
    ws.cell(row=row_num, column=1).font = bold_font

    cooling_data = [
        ("E-301", "E-301", "Enfriador efluente SOEC", "Enfriamiento", -8741.80, 69934.4, "Enfría mezcla H2/H2O de 750°C a 38°C para separar condensado"),
        ("E-501", "E-501", "Enfriador mezcla de síntesis", "Enfriamiento", -13952.70, 111621.6, "Condensa mezcla cruda metanol/agua previo al separador V-501"),
        ("E-701", "E-701", "Condensador de domo T-701", "Enfriamiento", -2865.00, 22920.0, "Condensador total de vapores de metanol a 65.0°C"),
        ("E-704", "E-704", "Subenfriador de producto final", "Enfriamiento", -92.20, 737.6, "Subenfría metanol producto a 35.0°C para bombeo a tanques"),
        ("E-V701", "V-701", "Desgasificador LP de metanol", "Balance adiab.", 0.00, 0.0, "Flash adiabático de 75 a 3 bar para desorber gases ligeros")
    ]
    for row in cooling_data:
        row_num += 1
        ws.row_dimensions[row_num].height = 19
        ws.cell(row=row_num, column=1, value=row[0]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=2, value=row[1]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=3, value=row[2]).alignment = Alignment(horizontal="left")
        ws.cell(row=row_num, column=4, value=row[3]).alignment = Alignment(horizontal="center")
        
        c5 = ws.cell(row=row_num, column=5, value=row[4])
        c5.number_format = "#,##0.00"
        c5.alignment = Alignment(horizontal="right")
        
        c6 = ws.cell(row=row_num, column=6, value=row[5])
        c6.number_format = "#,##0.0"
        c6.alignment = Alignment(horizontal="right")
        
        ws.cell(row=row_num, column=7, value=row[6]).alignment = Alignment(horizontal="left")
        for col_idx in range(1, 8):
            ws.cell(row=row_num, column=col_idx).border = thin_border

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_tc01("VTP-01_Solvanta/03_Tablas/TC-01_Solvanta.xlsx")
    create_te01("VTP-01_Solvanta/03_Tablas/TE-01_Solvanta.xlsx")

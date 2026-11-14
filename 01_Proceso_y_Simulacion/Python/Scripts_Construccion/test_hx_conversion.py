import xml.etree.ElementTree as ET
import copy

def update_to_rigorous_heatexchanger():
    tree = ET.parse('Simulacion_pruebas.xml')
    root = tree.getroot()
    sim_objs = root.find('.//SimulationObjects')
    graph_objs = root.find('.//GraphicObjects')

    # Load sample HeatExchanger
    sample_tree = ET.parse('/opt/dwsim/samples/Heat Exchanger Sizing and Design.dwxml')
    sample_root = sample_tree.getroot()
    sample_hx_so = None
    sample_hx_go = None
    for so in sample_root.find('SimulationObjects'):
        if 'HeatExchanger' in so.findtext('Type', ''):
            sample_hx_so = so
            break
    for go in sample_root.find('GraphicObjects'):
        if 'HeatExchanger' in go.findtext('Type', ''):
            sample_hx_go = go
            break

    print("Found sample HeatExchanger SO and GO successfully.")

    # Key IDs
    he601_id = 'HE-60100000-0000-0000-0000-000000000601'
    s10_int_id = 'MAT-10000000-0000-0000-0000-000000000501'
    s10_id = None
    e501_id = None
    srec_id = None
    srec_hot_id = 'MAT-60100000-0000-0000-0000-000000000601'
    split601_id = None

    id_to_go = {go.findtext('Name'): go for go in graph_objs}
    id_to_so = {so.findtext('ComponentName'): so for so in sim_objs}

    for go in graph_objs:
        tag = go.findtext('Tag')
        if tag == 'S-10': s10_id = go.findtext('Name')
        elif tag == 'E-501': e501_id = go.findtext('Name')
        elif tag == 'S-REC': srec_id = go.findtext('Name')
        elif tag == 'SPLIT-601': split601_id = go.findtext('Name')

    print(f"S-10: {s10_id}, E-501: {e501_id}, S-REC: {srec_id}")

    # 1. Remove old E-601 (Heater) and E-601_DUTY (EnergyStream)
    for so in list(sim_objs):
        name = so.findtext('ComponentName', '')
        if '601' in name and ('AQ' in name or 'EN' in name):
            sim_objs.remove(so)
            print(f"Removed old SO: {name}")

    for go in list(graph_objs):
        tag = go.findtext('Tag', '')
        name = go.findtext('Name', '')
        if tag in ['E-601_DUTY'] or (tag == 'E-601' and 'AQ' in name):
            graph_objs.remove(go)
            print(f"Removed old GO: {tag}")

    # 2. Build S-10_INT (MaterialStream between E-601 and E-501)
    s10_so = id_to_so[s10_id]
    s10_int_so = copy.deepcopy(s10_so)
    s10_int_so.find('ComponentName').text = s10_int_id
    s10_int_so.find('Name').text = s10_int_id
    s10_int_so.find('ComponentDescription').text = 'Efluente de R-401 pre-enfriado en E-601 (241.4 C, 75 bar)'
    s10_int_so.find('ForcePhase').text = 'GlobalDef'
    
    # Update temperature of S-10_INT to 241.4 C (514.55 K)
    delta_h_hot = -272.0543 / 5.771997 # -47.1335 kJ/kg
    cur_tef_hot = float(s10_so.findtext('TotalEnergyFlow'))
    s10_int_so.find('TotalEnergyFlow').text = f"{(cur_tef_hot - 272.0543):.6f}"
    
    phases = s10_int_so.find('Phases')
    for ph in phases.findall('Phase'):
        pid = ph.findtext('ID')
        props_list = [p for p in ph.findall('Properties') if len(p) > 0]
        if props_list:
            pr = props_list[0]
            if pid in ['0', '2']: # Mixture or Vapor
                t_el = pr.find('temperature')
                if t_el is not None: t_el.text = '514.55'
                h_el = pr.find('enthalpy')
                if h_el is not None:
                    h_el.text = f"{(float(h_el.text) + delta_h_hot):.6f}"
    sim_objs.append(s10_int_so)

    # 3. GraphicObject for S-10_INT
    s10_int_go = copy.deepcopy(id_to_go[s10_id])
    s10_int_go.find('Name').text = s10_int_id
    s10_int_go.find('Tag').text = 'S-10_INT'
    s10_int_go.find('X').text = '510.0'
    s10_int_go.find('Y').text = '284.9'
    
    # S-10_INT InConnectors from E-601 Hot Outlet (index 0)
    in_c = s10_int_go.find('InputConnectors')
    in_c.clear()
    ET.SubElement(in_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': he601_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    # S-10_INT OutConnectors to E-501 (index 0)
    out_c = s10_int_go.find('OutputConnectors')
    out_c.clear()
    ET.SubElement(out_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': e501_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    graph_objs.append(s10_int_go)

    # 4. Rewire S-10 to connect to E-601 Hot Inlet (index 0)
    s10_go = id_to_go[s10_id]
    s10_go.find('X').text = '430.0'
    s10_out = s10_go.find('OutputConnectors')
    s10_out.clear()
    ET.SubElement(s10_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': he601_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })

    # 5. Rewire E-501 to receive S-10_INT
    e501_go = id_to_go[e501_id]
    e501_go.find('X').text = '555.0'
    e501_in = e501_go.find('InputConnectors')
    e501_in.clear()
    ET.SubElement(e501_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': s10_int_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    # Update E-501 SimulationObject DeltaT
    e501_so = id_to_so[e501_id]
    e501_dt = e501_so.find('DeltaT')
    if e501_dt is not None: e501_dt.text = '-203.4'
    e501_tc = e501_so.find('TemperatureChange')
    if e501_tc is not None: e501_tc.text = '-203.4'

    # 6. Build E-601 HeatExchanger SimulationObject
    hx_so = copy.deepcopy(sample_hx_so)
    hx_so.find('ComponentName').text = he601_id
    hx_so.find('Name').text = he601_id
    hx_so.find('ComponentDescription').text = 'Economizador Gas-Gas E-601 (Cruce efluente S-10 con gas reciclo S-REC)'
    hx_so.find('PropertyPackage').text = 'PP-66ac0962-b06b-4cf0-a484-697d5bfd0c7c'
    
    # CalcMode: CalcTempColdOut
    hx_so.find('CalculationMode').text = 'CalcTempColdOut'
    hx_so.find('DefinedTemperature').text = 'Cold_Fluid'
    hx_so.find('FlowDir').text = 'CounterCurrent'
    hx_so.find('ColdSideOutletTemperature').text = '316.15'
    hx_so.find('HotSideOutletTemperature').text = '514.55'
    hx_so.find('HotSidePressureDrop').text = '0'
    hx_so.find('ColdSidePressureDrop').text = '0'
    hx_so.find('Q').text = '272.0543'
    hx_so.find('ThermalEfficiency').text = '100'
    sim_objs.append(hx_so)

    # 7. Build E-601 HeatExchanger GraphicObject
    hx_go = copy.deepcopy(sample_hx_go)
    hx_go.find('Name').text = he601_id
    hx_go.find('Tag').text = 'E-601'
    hx_go.find('Description').text = 'Economizador Gas-Gas E-601'
    hx_go.find('X').text = '470.0'
    hx_go.find('Y').text = '280.0'
    hx_go.find('Width').text = '30'
    hx_go.find('Height').text = '30'
    
    # InputConnectors: 0 = Hot in (S-10), 1 = Cold in (S-REC)
    hx_in = hx_go.find('InputConnectors')
    hx_in.clear()
    ET.SubElement(hx_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': s10_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    ET.SubElement(hx_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': srec_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })

    # OutputConnectors: 0 = Hot out (S-10_INT), 1 = Cold out (S-REC_HOT)
    hx_out = hx_go.find('OutputConnectors')
    hx_out.clear()
    ET.SubElement(hx_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': s10_int_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    ET.SubElement(hx_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': srec_hot_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })

    hx_en = hx_go.find('EnergyConnector')
    hx_en.clear()
    ET.SubElement(hx_en, 'Connector', {'IsAttached': 'false'})
    graph_objs.append(hx_go)

    # 8. Rewire S-REC OutputConnectors to E-601 Cold Inlet (index 1)
    srec_go = id_to_go[srec_id]
    srec_go.find('X').text = '600.0'
    srec_go.find('Y').text = '240.0'
    srec_out = srec_go.find('OutputConnectors')
    srec_out.clear()
    ET.SubElement(srec_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': he601_id, 'AttachedToConnIndex': '1', 'AttachedToEnergyConn': 'False'
    })

    # 9. Rewire S-REC_HOT InputConnectors from E-601 Cold Outlet (index 1)
    srec_hot_go = id_to_go[srec_hot_id]
    srec_hot_go.find('X').text = '600.0'
    srec_hot_go.find('Y').text = '185.0'
    hot_in = srec_hot_go.find('InputConnectors')
    hot_in.clear()
    ET.SubElement(hot_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': he601_id, 'AttachedFromConnIndex': '1', 'AttachedFromEnergyConn': 'False'
    })

    # Save to Simulacion_pruebas
    xml_data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    with open('Simulacion_pruebas.xml', 'wb') as f:
        f.write(xml_data)
    with open('Simulacion_pruebas.dwxml', 'wb') as f:
        f.write(b'\xef\xbb\xbf' + xml_data)

    print("Successfully built rigorous 2-stream HeatExchanger E-601 in Simulacion_pruebas!")

if __name__ == '__main__':
    update_to_rigorous_heatexchanger()

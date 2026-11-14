import xml.etree.ElementTree as ET
import copy

def build_simulation():
    # 1. Start from base clean file
    tree = ET.parse('Simulacion_xml-dwxml_Actividad_v0.1.xml')
    root = tree.getroot()
    sim_objs = root.find('.//SimulationObjects')
    graph_objs = root.find('.//GraphicObjects')

    # Load sample HeatExchanger SO and GO
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

    # Sample Recycle SO and GO from base file
    sample_rcy_so = None
    sample_rcy_go = None
    for so in sim_objs:
        if 'Recycle' in so.findtext('Type', ''):
            sample_rcy_so = so
            break
    for go in graph_objs:
        if 'Recycle' in go.findtext('Type', ''):
            sample_rcy_go = go
            break

    # Maps
    id_to_go = {go.findtext('Name'): go for go in graph_objs}
    id_to_so = {so.findtext('ComponentName'): so for so in sim_objs}

    # Find key IDs from tags
    s10_id = None
    e501_id = None
    v501_id = None
    srec_id = None
    split601_id = None
    s12_id = None
    s13_id = None

    for go in graph_objs:
        tag = go.findtext('Tag')
        if tag == 'S-10': s10_id = go.findtext('Name')
        elif tag == 'E-501': e501_id = go.findtext('Name')
        elif tag == 'V-501': v501_id = go.findtext('Name')
        elif tag == 'S-REC': srec_id = go.findtext('Name')
        elif tag == 'SPLIT-601': split601_id = go.findtext('Name')
        elif tag == 'S-12': s12_id = go.findtext('Name')
        elif tag == 'S-13': s13_id = go.findtext('Name')

    print(f"Base IDs found: S-10={s10_id}, E-501={e501_id}, V-501={v501_id}, S-REC={srec_id}, SPLIT={split601_id}")

    # Define dedicated IDs for new objects
    he601_id = 'HE-60100000-0000-0000-0000-000000000601'
    s10_int_id = 'MAT-10000000-0000-0000-0000-000000000501'
    srec_raw_id = 'MAT-50100000-0000-0000-0000-000000000501'
    rcy501_id = 'REC-50100000-0000-0000-0000-000000000501'
    srec_hot_id = 'MAT-60100000-0000-0000-0000-000000000601'

    # STEP 0: Fix S-05 and S-ZLD_PUR to GlobalDef (natural no forzado)
    # and remove redundant E-703 on V-701
    for go in graph_objs:
        tag = go.findtext('Tag')
        name = go.findtext('Name')
        if tag in ['S-05', 'S-ZLD_PUR'] and name in id_to_so:
            fp = id_to_so[name].find('ForcePhase')
            if fp is not None: fp.text = 'GlobalDef'
        if tag == 'V-701':
            for c in go.find('InputConnectors').findall('Connector'):
                if c.get('ConnType') == 'ConEn':
                    c.set('IsAttached', 'false')
                    if 'AttachedFromObjID' in c.attrib: del c.attrib['AttachedFromObjID']
                    if 'AttachedFromConnIndex' in c.attrib: del c.attrib['AttachedFromConnIndex']
                    if 'AttachedFromEnergyConn' in c.attrib: del c.attrib['AttachedFromEnergyConn']

    # Remove E-703 from graph_objs and sim_objs
    for go in list(graph_objs):
        if go.findtext('Tag') == 'E-703':
            graph_objs.remove(go)
    for so in list(sim_objs):
        if '703' in so.findtext('ComponentName', '') and 'EN-' in so.findtext('ComponentName', ''):
            sim_objs.remove(so)

    # STEP 1: S-10_INT (MaterialStream between E-601 and E-501)
    s10_so = id_to_so[s10_id]
    s10_int_so = copy.deepcopy(s10_so)
    s10_int_so.find('ComponentName').text = s10_int_id
    s10_int_so.find('Name').text = s10_int_id
    s10_int_so.find('ComponentDescription').text = 'Efluente de R-401 pre-enfriado en E-601 (224.6 C, 75 bar)'
    s10_int_so.find('ForcePhase').text = 'GlobalDef'

    cur_tef_hot = float(s10_so.findtext('TotalEnergyFlow'))
    s10_int_so.find('TotalEnergyFlow').text = f"{(cur_tef_hot - 1197.0402):.6f}"

    for ph in s10_int_so.find('Phases').findall('Phase'):
        pid = ph.findtext('ID')
        props_list = [p for p in ph.findall('Properties') if len(p) > 0]
        if props_list:
            pr = props_list[0]
            if pid in ['0', '2']: # Mixture or Vapor
                t_el = pr.find('temperature')
                if t_el is not None: t_el.text = '497.7157'
                h_el = pr.find('enthalpy')
                if h_el is not None:
                    h_el.text = f"{(float(h_el.text) - 207.3875):.6f}"
    sim_objs.append(s10_int_so)

    s10_int_go = copy.deepcopy(id_to_go[s10_id])
    s10_int_go.find('Name').text = s10_int_id
    s10_int_go.find('Tag').text = 'S-10_INT'
    s10_int_go.find('X').text = '510.0'
    s10_int_go.find('Y').text = '284.9'

    in_c = s10_int_go.find('InputConnectors')
    in_c.clear()
    ET.SubElement(in_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': he601_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    out_c = s10_int_go.find('OutputConnectors')
    out_c.clear()
    ET.SubElement(out_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': e501_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    graph_objs.append(s10_int_go)

    # STEP 2: Rewire S-10 to connect to E-601 Hot Inlet (index 0)
    s10_go = id_to_go[s10_id]
    s10_go.find('X').text = '430.0'
    s10_out = s10_go.find('OutputConnectors')
    s10_out.clear()
    ET.SubElement(s10_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': he601_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })

    # STEP 3: Rewire E-501 to receive S-10_INT
    e501_go = id_to_go[e501_id]
    e501_go.find('X').text = '555.0'
    e501_in = e501_go.find('InputConnectors')
    e501_in.clear()
    ET.SubElement(e501_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': s10_int_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    e501_so = id_to_so[e501_id]
    e501_so.find('CalcMode').text = 'OutletTemperature'
    e501_so.find('OutletTemperature').text = '311.15'
    e501_dt = e501_so.find('DeltaT')
    if e501_dt is not None: e501_dt.text = '-186.566'
    e501_tc = e501_so.find('TemperatureChange')
    if e501_tc is not None: e501_tc.text = '-186.566'

    # STEP 4: S-REC_RAW and RCY-501
    srec_so = id_to_so[srec_id]
    srec_raw_so = copy.deepcopy(srec_so)
    srec_raw_so.find('ComponentName').text = srec_raw_id
    srec_raw_so.find('Name').text = srec_raw_id
    srec_raw_so.find('ComponentDescription').text = 'Vapor saturado de V-501 (alimentacion a reciclo RCY-501)'
    srec_raw_so.find('ForcePhase').text = 'GlobalDef'
    sim_objs.append(srec_raw_so)

    srec_raw_go = copy.deepcopy(id_to_go[srec_id])
    srec_raw_go.find('Name').text = srec_raw_id
    srec_raw_go.find('Tag').text = 'S-REC_RAW'
    srec_raw_go.find('X').text = '650.0'
    srec_raw_go.find('Y').text = '240.0'
    raw_in = srec_raw_go.find('InputConnectors')
    raw_in.clear()
    ET.SubElement(raw_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': v501_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    raw_out = srec_raw_go.find('OutputConnectors')
    raw_out.clear()
    ET.SubElement(raw_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': rcy501_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    graph_objs.append(srec_raw_go)

    # Rewire V-501 top vapor outlet (index 0) to S-REC_RAW
    v501_go = id_to_go[v501_id]
    v501_out = v501_go.find('OutputConnectors')
    for c in v501_out.findall('Connector'):
        if c.get('AttachedToObjID') == srec_id:
            c.set('AttachedToObjID', srec_raw_id)

    # Build RCY-501 SimulationObject
    # Crucial: AccelerationMethod = None (Direct Substitution) to prevent Wegstein oscillations!
    rcy501_so = copy.deepcopy(sample_rcy_so)
    rcy501_so.find('ComponentName').text = rcy501_id
    rcy501_so.find('Name').text = rcy501_id
    rcy501_so.find('ComponentDescription').text = 'Bloque de Reciclo E-601 / V-501'
    rcy501_so.find('AccelerationMethod').text = 'None'
    rcy501_so.find('SmoothingFactor').text = '1'
    rcy501_so.find('MaximumIterations').text = '50'
    rcy501_so.find('Converged').text = 'true'
    rcy501_so.find('IterationsTaken').text = '1'
    rcy501_so.find('Left').text = '600.0'
    rcy501_so.find('Top').text = '240.0'
    rcy501_so.find('Right').text = '620.0'
    rcy501_so.find('Bottom').text = '260.0'
    sim_objs.append(rcy501_so)

    # Build RCY-501 GraphicObject
    rcy501_go = copy.deepcopy(sample_rcy_go)
    rcy501_go.find('Name').text = rcy501_id
    rcy501_go.find('Tag').text = 'RCY-501'
    rcy501_go.find('Description').text = 'Bloque de Reciclo E-601'
    rcy501_go.find('X').text = '600.0'
    rcy501_go.find('Y').text = '240.0'
    rcy501_go.find('Width').text = '20'
    rcy501_go.find('Height').text = '20'
    
    rcy_in = rcy501_go.find('InputConnectors')
    rcy_in.clear()
    ET.SubElement(rcy_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': srec_raw_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    rcy_out = rcy501_go.find('OutputConnectors')
    rcy_out.clear()
    ET.SubElement(rcy_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': srec_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    graph_objs.append(rcy501_go)

    # Rewire S-REC GraphicObject (between RCY-501 and E-601)
    srec_go = id_to_go[srec_id]
    srec_go.find('X').text = '540.0'
    srec_go.find('Y').text = '240.0'
    srec_in = srec_go.find('InputConnectors')
    srec_in.clear()
    ET.SubElement(srec_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': rcy501_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    srec_out = srec_go.find('OutputConnectors')
    srec_out.clear()
    ET.SubElement(srec_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': he601_id, 'AttachedToConnIndex': '1', 'AttachedToEnergyConn': 'False'
    })

    # STEP 5: S-REC_HOT (60.0 C, 333.15 K)
    srec_hot_so = copy.deepcopy(srec_so)
    srec_hot_so.find('ComponentName').text = srec_hot_id
    srec_hot_so.find('Name').text = srec_hot_id
    srec_hot_so.find('ComponentDescription').text = 'Gas de reciclo sobrecalentado a 60 C en E-601 (hacia SPLIT-601)'
    srec_hot_so.find('ForcePhase').text = 'GlobalDef'

    cur_tef_cold = float(srec_so.findtext('TotalEnergyFlow'))
    srec_hot_so.find('TotalEnergyFlow').text = f"{(cur_tef_cold + 1197.0402):.6f}"

    for ph in srec_hot_so.find('Phases').findall('Phase'):
        pid = ph.findtext('ID')
        props_list = [p for p in ph.findall('Properties') if len(p) > 0]
        if props_list:
            pr = props_list[0]
            if pid in ['0', '2']:
                t_el = pr.find('temperature')
                if t_el is not None: t_el.text = '333.15'
                h_el = pr.find('enthalpy')
                if h_el is not None:
                    h_el.text = f"{(float(h_el.text) + 289.9417):.6f}"
    sim_objs.append(srec_hot_so)

    srec_hot_go = copy.deepcopy(id_to_go[srec_id])
    srec_hot_go.find('Name').text = srec_hot_id
    srec_hot_go.find('Tag').text = 'S-REC_HOT'
    srec_hot_go.find('X').text = '600.0'
    srec_hot_go.find('Y').text = '185.0'
    hot_in = srec_hot_go.find('InputConnectors')
    hot_in.clear()
    ET.SubElement(hot_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': he601_id, 'AttachedFromConnIndex': '1', 'AttachedFromEnergyConn': 'False'
    })
    hot_out = srec_hot_go.find('OutputConnectors')
    hot_out.clear()
    ET.SubElement(hot_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': split601_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    graph_objs.append(srec_hot_go)

    # Rewire SPLIT-601 InputConnector to S-REC_HOT
    split601_go = id_to_go[split601_id]
    split_in = split601_go.find('InputConnectors')
    split_in.clear()
    ET.SubElement(split_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': srec_hot_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })

    # Update S-12 and S-13 temperatures to 60.0 C (333.15 K)
    for s_id in [s12_id, s13_id]:
        if s_id in id_to_so:
            so = id_to_so[s_id]
            so.find('ForcePhase').text = 'GlobalDef'
            for ph in so.find('Phases').findall('Phase'):
                pid = ph.findtext('ID')
                props_list = [p for p in ph.findall('Properties') if len(p) > 0]
                if props_list:
                    pr = props_list[0]
                    if pid in ['0', '2']:
                        t_el = pr.find('temperature')
                        if t_el is not None: t_el.text = '333.15'
                        h_el = pr.find('enthalpy')
                        if h_el is not None:
                            h_el.text = f"{(float(h_el.text) + 289.9417):.6f}"

    # STEP 6: Build E-601 HeatExchanger (SO and GO)
    hx_so = copy.deepcopy(sample_hx_so)
    hx_so.find('ComponentName').text = he601_id
    hx_so.find('Name').text = he601_id
    hx_so.find('ComponentDescription').text = 'Economizador Gas-Gas E-601 (Cruce efluente S-10 con gas reciclo S-REC)'
    hx_so.find('PropertyPackage').text = 'PP-66ac0962-b06b-4cf0-a484-697d5bfd0c7c'
    
    # CalcTempHotOut: user specifies Cold Side Outlet Temperature (60 C = 333.15 K)
    # and DWSIM calculates Hot Side Outlet Temperature (224.57 C = 497.716 K)
    hx_so.find('CalculationMode').text = 'CalcTempHotOut'
    hx_so.find('DefinedTemperature').text = 'Cold_Fluid'
    hx_so.find('FlowDir').text = 'CounterCurrent'
    hx_so.find('ColdSideOutletTemperature').text = '333.15'
    hx_so.find('HotSideOutletTemperature').text = '497.7157'
    hx_so.find('HotSidePressureDrop').text = '0'
    hx_so.find('ColdSidePressureDrop').text = '0'
    hx_so.find('Q').text = '1197.0402'
    hd = hx_so.find('HeatDuty')
    if hd is not None: hd.text = '1197.0402'
    hx_so.find('ThermalEfficiency').text = '100'
    sim_objs.append(hx_so)

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

    # Save to Simulacion_pruebas
    xml_data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    with open('Simulacion_pruebas.xml', 'wb') as f:
        f.write(xml_data)
    with open('Simulacion_pruebas.dwxml', 'wb') as f:
        f.write(b'\xef\xbb\xbf' + xml_data)

    print("Successfully built Simulacion_pruebas with all fixes!")

if __name__ == '__main__':
    build_simulation()

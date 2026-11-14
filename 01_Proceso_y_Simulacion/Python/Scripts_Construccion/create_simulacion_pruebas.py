import xml.etree.ElementTree as ET
import copy

def create_simulacion_pruebas():
    # 1. First ensure the base file has clean GlobalDef on recycle streams
    tree_base = ET.parse('Simulacion_xml-dwxml_Actividad_v0.1.xml')
    root_base = tree_base.getroot()
    sim_objs_base = root_base.find('.//SimulationObjects')
    graph_objs_base = root_base.find('.//GraphicObjects')
    
    id_to_tag_base = {go.findtext('Name'): go.findtext('Tag') for go in graph_objs_base}
    base_modified = False
    for so in sim_objs_base:
        cname = so.findtext('ComponentName', '')
        tag = id_to_tag_base.get(cname, '')
        if tag in ['S-REC', 'S-12', 'S-13', 'S-REC_OUT', 'S-REC_FEED']:
            fp = so.find('ForcePhase')
            if fp is not None and fp.text != 'GlobalDef':
                fp.text = 'GlobalDef'
                base_modified = True
                
    if base_modified:
        xml_data_base = ET.tostring(root_base, encoding='utf-8', xml_declaration=True)
        with open('Simulacion_xml-dwxml_Actividad_v0.1.xml', 'wb') as f:
            f.write(xml_data_base)
        with open('Simulacion_xml-dwxml_Actividad_v0.1.dwxml', 'wb') as f:
            f.write(b'\xef\xbb\xbf' + xml_data_base)
        print("Restored clean GlobalDef on base simulation files.")

    # 2. Now parse base file to build Simulacion_pruebas
    tree = ET.parse('Simulacion_xml-dwxml_Actividad_v0.1.xml')
    root = tree.getroot()
    sim_objs = root.find('.//SimulationObjects')
    graph_objs = root.find('.//GraphicObjects')

    # Mapping of tags and IDs
    tag_to_so = {}
    tag_to_go = {}
    id_to_so = {}
    id_to_go = {}

    for go in graph_objs.findall('GraphicObject'):
        name = go.findtext('Name')
        tag = go.findtext('Tag')
        if name:
            id_to_go[name] = go
        if tag:
            tag_to_go[tag] = go

    for so in sim_objs.findall('SimulationObject'):
        cname = so.findtext('ComponentName')
        if cname:
            id_to_so[cname] = so
            tag = id_to_go.get(cname, None)
            if tag is not None:
                tag_str = tag.findtext('Tag')
                tag_to_so[tag_str] = so

    # IDs for Option A
    e601_id = 'AQ-60100000-0000-0000-0000-000000000601'
    en601_id = 'EN-60100000-0000-0000-0000-000000000601'
    srec_hot_id = 'MAT-60100000-0000-0000-0000-000000000601'
    
    srec_id = tag_to_go['S-REC'].findtext('Name')
    split601_id = tag_to_go['SPLIT-601'].findtext('Name')
    c601_id = tag_to_go['C-601'].findtext('Name')
    x601_id = tag_to_go['X-601'].findtext('Name')
    s12_id = tag_to_go['S-12'].findtext('Name')
    s13_id = tag_to_go['S-13'].findtext('Name')
    srec_out_id = tag_to_go['S-REC_OUT'].findtext('Name')
    srec_feed_id = tag_to_go['S-REC_FEED'].findtext('Name')
    e501_id = tag_to_go['E-501'].findtext('Name')
    e201_id = tag_to_go['E-201'].findtext('Name')
    en704_id = tag_to_go['E-704_DUTY'].findtext('Name')

    # Remove any pre-existing E-601, EN-601, S-REC_HOT
    for obj in list(sim_objs):
        if obj.findtext('ComponentName') in [e601_id, en601_id, srec_hot_id]:
            sim_objs.remove(obj)
    for gobj in list(graph_objs):
        if gobj.findtext('Name') in [e601_id, en601_id, srec_hot_id] or gobj.findtext('Tag') in ['E-601', 'E-601_DUTY', 'S-REC_HOT']:
            graph_objs.remove(gobj)

    # 3. Create E-601 SimulationObject (cloned from E-201)
    e601_so = copy.deepcopy(id_to_so[e201_id])
    e601_so.find('ComponentName').text = e601_id
    e601_so.find('Name').text = e601_id
    e601_so.find('ComponentDescription').text = 'Economizador E-601 (Calentamiento de reciclo 38 C a 43 C con calor efluente S-10)'
    e601_so.find('OutletTemperature').text = '316.15'
    e601_so.find('OutletVaporFraction').text = '1'
    e601_so.find('CalcMode').text = 'OutletTemperature'
    e601_so.find('DeltaT').text = '5.0'
    e601_so.find('TemperatureChange').text = '5.0'
    e601_so.find('DeltaP').text = '0'
    e601_so.find('PressureDrop').text = '0'
    e601_so.find('DeltaQ').text = '272.0543'
    e601_so.find('HeatDuty').text = '272.0543'
    e601_so.find('Eficiencia').text = '100'
    e601_so.find('Efficiency').text = '100'
    e601_so.find('Left').text = '740.0'
    e601_so.find('Top').text = '215.0'
    e601_so.find('Right').text = '765.0'
    e601_so.find('Bottom').text = '240.0'
    e601_so.find('Width').text = '25'
    e601_so.find('Height').text = '25'
    dim = e601_so.find('.//Dimensions/Dimension/Value')
    if dim is not None: dim.text = '272.0543'
    sim_objs.append(e601_so)

    # 4. Create E-601 GraphicObject (cloned from E-201 GO)
    e601_go = copy.deepcopy(id_to_go[e201_id])
    e601_go.find('Name').text = e601_id
    e601_go.find('Tag').text = 'E-601'
    e601_go.find('X').text = '740'
    e601_go.find('Y').text = '215'
    e601_go.find('Width').text = '25'
    e601_go.find('Height').text = '25'
    
    # E-601 Input Connectors: stream S-REC in
    in_c = e601_go.find('InputConnectors')
    in_c.clear()
    ET.SubElement(in_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': srec_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    ET.SubElement(in_c, 'Connector', {'IsAttached': 'false'})

    # E-601 Output Connectors: stream S-REC_HOT out
    out_c = e601_go.find('OutputConnectors')
    out_c.clear()
    ET.SubElement(out_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': srec_hot_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })

    # E-601 Energy Connector: energy stream E-601_DUTY
    en_c = e601_go.find('EnergyConnector')
    en_c.clear()
    ET.SubElement(en_c, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConEn',
        'AttachedToObjID': en601_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'True'
    })
    graph_objs.append(e601_go)

    # 5. Create E-601_DUTY SimulationObject (cloned from EN-704)
    en601_so = copy.deepcopy(id_to_so[en704_id])
    en601_so.find('ComponentName').text = en601_id
    en601_so.find('Name').text = en601_id
    en601_so.find('ComponentDescription').text = 'Flujo de Energia Economizador E-601 (272.05 kW recuperados de efluente S-10)'
    ef = en601_so.find('EnergyFlow')
    if ef is not None:
        ef.text = '272.0543'
    else:
        ef = ET.SubElement(en601_so, 'EnergyFlow')
        ef.text = '272.0543'
    sim_objs.append(en601_so)

    # 6. Create E-601_DUTY GraphicObject (cloned from EN-704 GO)
    en601_go = copy.deepcopy(id_to_go[en704_id])
    en601_go.find('Name').text = en601_id
    en601_go.find('Tag').text = 'E-601_DUTY'
    en601_go.find('X').text = '740'
    en601_go.find('Y').text = '265'
    en601_go.find('Width').text = '20'
    en601_go.find('Height').text = '20'
    
    en_in = en601_go.find('InputConnectors')
    en_in.clear()
    ET.SubElement(en_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': e601_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'True'
    })
    en_out = en601_go.find('OutputConnectors')
    en_out.clear()
    ET.SubElement(en_out, 'Connector', {'IsAttached': 'false'})
    graph_objs.append(en601_go)

    # 7. Create S-REC_HOT SimulationObject (cloned from S-REC)
    srec_hot_so = copy.deepcopy(id_to_so[srec_id])
    srec_hot_so.find('ComponentName').text = srec_hot_id
    srec_hot_so.find('Name').text = srec_hot_id
    srec_hot_so.find('ComponentDescription').text = 'Gas de Reciclo Sobrecalentado (43 C, 75 bar, 100% Vapor natural)'
    srec_hot_so.find('ForcePhase').text = 'GlobalDef'
    # Ensure S-05 and S-ZLD_PUR are also natural GlobalDef
    if 'S-05' in tag_to_so:
        fp = tag_to_so['S-05'].find('ForcePhase')
        if fp is not None: fp.text = 'GlobalDef'
    if 'S-ZLD_PUR' in tag_to_so:
        fp = tag_to_so['S-ZLD_PUR'].find('ForcePhase')
        if fp is not None: fp.text = 'GlobalDef'
    srec_hot_so.find('TotalEnergyFlow').text = '-2454.98926'

    # Update thermodynamic properties in S-REC_HOT
    def update_stream_thermo(so, target_t, delta_h, target_tef):
        so.find('ForcePhase').text = 'GlobalDef'
        if target_tef is not None:
            so.find('TotalEnergyFlow').text = f'{target_tef:.6f}'
        phases = so.find('Phases')
        if phases is not None:
            for ph in phases.findall('Phase'):
                pid = ph.findtext('ID')
                props_list = [p for p in ph.findall('Properties') if len(p) > 0]
                if not props_list:
                    continue
                pr = props_list[0]
                if pid in ['0', '2']: # Mixture or Vapor
                    t_el = pr.find('temperature')
                    if t_el is not None: t_el.text = f'{target_t:.4f}'
                    h_el = pr.find('enthalpy')
                    if h_el is not None and h_el.text:
                        try:
                            cur_h = float(h_el.text)
                            h_el.text = f'{(cur_h + delta_h):.6f}'
                        except:
                            pass
                    mf_el = pr.find('molarfraction')
                    if mf_el is not None and pid == '2':
                        mf_el.text = '1'
                    vf_el = pr.find('volumetricFraction')
                    if vf_el is not None and pid == '2':
                        vf_el.text = '1'
                elif pid in ['1', '3']: # Liquid phases
                    mf_el = pr.find('massflow')
                    if mf_el is not None: mf_el.text = '0'
                    mol_el = pr.find('molarflow')
                    if mol_el is not None: mol_el.text = '0'
                    frac_el = pr.find('molarfraction')
                    if frac_el is not None: frac_el.text = '0'
                    vfrac_el = pr.find('volumetricFraction')
                    if vfrac_el is not None: vfrac_el.text = '0'
                    h_el = pr.find('enthalpy')
                    if h_el is not None: h_el.text = '0'

    delta_h = 65.895835 # kJ/kg
    update_stream_thermo(srec_hot_so, 316.15, delta_h, -2454.98926)
    sim_objs.append(srec_hot_so)

    # 8. Create S-REC_HOT GraphicObject (cloned from S-REC GO)
    srec_hot_go = copy.deepcopy(id_to_go[srec_id])
    srec_hot_go.find('Name').text = srec_hot_id
    srec_hot_go.find('Tag').text = 'S-REC_HOT'
    srec_hot_go.find('X').text = '765'
    srec_hot_go.find('Y').text = '195'
    srec_hot_go.find('Width').text = '20'
    srec_hot_go.find('Height').text = '20'

    hot_in = srec_hot_go.find('InputConnectors')
    hot_in.clear()
    ET.SubElement(hot_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': e601_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    hot_out = srec_hot_go.find('OutputConnectors')
    hot_out.clear()
    ET.SubElement(hot_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': split601_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    graph_objs.append(srec_hot_go)

    # 9. Rewire S-REC GraphicObject: now outputs to E-601
    srec_go = id_to_go[srec_id]
    srec_go.find('X').text = '715'
    srec_go.find('Y').text = '240'
    srec_out = srec_go.find('OutputConnectors')
    srec_out.clear()
    ET.SubElement(srec_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': e601_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })

    # Ensure S-REC SimulationObject has ForcePhase = GlobalDef
    id_to_so[srec_id].find('ForcePhase').text = 'GlobalDef'

    # 10. Rewire SPLIT-601 GraphicObject: now inputs from S-REC_HOT
    split_go = id_to_go[split601_id]
    split_in = split_go.find('InputConnectors')
    split_in.clear()
    ET.SubElement(split_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': srec_hot_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })

    # 11. Update downstream streams to 43.0 C (316.15 K) & ForcePhase = GlobalDef
    # S-12 (96% reciclo)
    update_stream_thermo(id_to_so[s12_id], 316.15, delta_h, -2356.7787)
    # S-13 (4% purga)
    update_stream_thermo(id_to_so[s13_id], 316.15, delta_h, -98.1991)
    # S-REC_OUT
    update_stream_thermo(id_to_so[srec_out_id], 316.15, delta_h, -2356.7787)
    # S-REC_FEED
    update_stream_thermo(id_to_so[srec_feed_id], 316.15, delta_h, -2357.7366)

    # 12. Update C-601 compressor outlet temperature
    c601_so = id_to_so[c601_id]
    c601_ot = c601_so.find('OutletTemperature')
    if c601_ot is not None: c601_ot.text = '316.15'

    # 13. Update X-601 expander (expands from 43 C instead of 38 C)
    x601_so = id_to_so[x601_id]
    x601_ot = x601_so.find('OutletTemperature')
    if x601_ot is not None: x601_ot.text = '128.48'
    x601_dq = x601_so.find('DeltaQ')
    if x601_dq is not None: x601_dq.text = '390.43'

    # 14. Adjust Cooler E-501 duty: 14224.75 - 272.05 = 13952.70 kW
    e501_so = id_to_so[e501_id]
    e501_dq = e501_so.find('DeltaQ')
    if e501_dq is not None: e501_dq.text = '13952.70'
    e501_hd = e501_so.find('HeatDuty')
    if e501_hd is not None: e501_hd.text = '13952.70'
    e501_desc = e501_so.find('ComponentDescription')
    if e501_desc is not None:
        e501_desc.text = 'Enfriador de efluente de reaccion (acoplado a economizador E-601: 272.05 kW a reciclo)'

    # 15. Save Simulacion_pruebas.xml and Simulacion_pruebas.dwxml
    xml_out = 'Simulacion_pruebas.xml'
    dwxml_out = 'Simulacion_pruebas.dwxml'
    
    xml_bytes = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    with open(xml_out, 'wb') as f:
        f.write(xml_bytes)
    print(f'Successfully generated {xml_out} ({len(xml_bytes)} bytes)')

    with open(dwxml_out, 'wb') as f:
        f.write(b'\xef\xbb\xbf')
        f.write(xml_bytes)
    print(f'Successfully generated {dwxml_out} ({len(xml_bytes) + 3} bytes)')

if __name__ == '__main__':
    create_simulacion_pruebas()

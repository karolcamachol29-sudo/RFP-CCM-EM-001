import xml.etree.ElementTree as ET

def verify():
    print("=== STARTING VERIFICATION OF Simulacion_pruebas ===")
    
    # 1. BOM Check on .dwxml
    with open('Simulacion_pruebas.dwxml', 'rb') as f:
        header = f.read(3)
        assert header == b'\xef\xbb\xbf', f"BOM missing on .dwxml! Got: {header}"
    print("✓ PASS: BOM (UTF-8) present on Simulacion_pruebas.dwxml")

    # 2. Parse XML
    tree = ET.parse('Simulacion_pruebas.xml')
    root = tree.getroot()
    sim_objs = root.find('.//SimulationObjects')
    graph_objs = root.find('.//GraphicObjects')
    
    print(f"SimulationObjects count: {len(sim_objs)}")
    print(f"GraphicObjects count: {len(graph_objs)}")
    assert len(sim_objs) == len(graph_objs) == 65, f"Expected 65 objects, got {len(sim_objs)} and {len(graph_objs)}"
    print("✓ PASS: Exactly 65 SimulationObjects and 65 GraphicObjects found.")

    # Build lookup maps
    id_to_so = {so.findtext('ComponentName'): so for so in sim_objs}
    id_to_go = {go.findtext('Name'): go for go in graph_objs}
    tag_to_go = {go.findtext('Tag'): go for go in graph_objs}
    tag_to_so = {go.findtext('Tag'): id_to_so.get(go.findtext('Name')) for go in graph_objs}

    # 3. Verify Presence of New Option A Objects
    assert 'E-601' in tag_to_go, "E-601 graphic object missing!"
    assert 'E-601_DUTY' in tag_to_go, "E-601_DUTY graphic object missing!"
    assert 'S-REC_HOT' in tag_to_go, "S-REC_HOT graphic object missing!"
    print("✓ PASS: E-601, E-601_DUTY, and S-REC_HOT are present.")

    # 4. Verify Connections Topology
    # V-501 -> S-REC
    srec_go = tag_to_go['S-REC']
    srec_in = srec_go.find('.//InputConnectors/Connector')
    v501_id = tag_to_go['V-501'].findtext('Name')
    assert srec_in.attrib.get('AttachedFromObjID') == v501_id, "S-REC not attached from V-501!"
    print("✓ PASS: V-501 -> S-REC connection verified.")

    # S-REC -> E-601
    e601_id = tag_to_go['E-601'].findtext('Name')
    srec_out = srec_go.find('.//OutputConnectors/Connector')
    assert srec_out.attrib.get('AttachedToObjID') == e601_id, "S-REC not attached to E-601!"
    print("✓ PASS: S-REC -> E-601 connection verified.")

    # E-601 -> S-REC_HOT
    e601_go = tag_to_go['E-601']
    e601_out = e601_go.find('.//OutputConnectors/Connector')
    srec_hot_id = tag_to_go['S-REC_HOT'].findtext('Name')
    assert e601_out.attrib.get('AttachedToObjID') == srec_hot_id, "E-601 not attached to S-REC_HOT!"
    print("✓ PASS: E-601 -> S-REC_HOT connection verified.")

    # E-601 -> E-601_DUTY
    e601_en = e601_go.find('.//EnergyConnector/Connector')
    en601_id = tag_to_go['E-601_DUTY'].findtext('Name')
    assert e601_en.attrib.get('AttachedToObjID') == en601_id, "E-601 not attached to E-601_DUTY!"
    print("✓ PASS: E-601 -> E-601_DUTY energy connection verified.")

    # S-REC_HOT -> SPLIT-601
    srec_hot_go = tag_to_go['S-REC_HOT']
    srec_hot_out = srec_hot_go.find('.//OutputConnectors/Connector')
    split601_id = tag_to_go['SPLIT-601'].findtext('Name')
    assert srec_hot_out.attrib.get('AttachedToObjID') == split601_id, "S-REC_HOT not attached to SPLIT-601!"
    split_in = tag_to_go['SPLIT-601'].find('.//InputConnectors/Connector')
    assert split_in.attrib.get('AttachedFromObjID') == srec_hot_id, "SPLIT-601 not attached from S-REC_HOT!"
    print("✓ PASS: S-REC_HOT -> SPLIT-601 connection verified.")

    # SPLIT-601 -> S-12 and S-13
    split_outs = [c.attrib.get('AttachedToObjID') for c in tag_to_go['SPLIT-601'].findall('.//OutputConnectors/Connector') if c.attrib.get('IsAttached') == 'true']
    s12_id = tag_to_go['S-12'].findtext('Name')
    s13_id = tag_to_go['S-13'].findtext('Name')
    assert s12_id in split_outs and s13_id in split_outs, f"SPLIT-601 outputs missing S-12 or S-13: {split_outs}"
    print("✓ PASS: SPLIT-601 -> S-12 (96%) and S-13 (4%) connections verified.")

    # S-12 -> C-601 -> S-REC_OUT
    c601_id = tag_to_go['C-601'].findtext('Name')
    s12_out = tag_to_go['S-12'].find('.//OutputConnectors/Connector')
    assert s12_out.attrib.get('AttachedToObjID') == c601_id, "S-12 not attached to C-601!"
    c601_out = tag_to_go['C-601'].find('.//OutputConnectors/Connector')
    srec_out_id = tag_to_go['S-REC_OUT'].findtext('Name')
    assert c601_out.attrib.get('AttachedToObjID') == srec_out_id, "C-601 not attached to S-REC_OUT!"
    print("✓ PASS: S-12 -> C-601 -> S-REC_OUT connection verified.")

    # S-13 -> X-601
    x601_id = tag_to_go['X-601'].findtext('Name')
    s13_out = tag_to_go['S-13'].find('.//OutputConnectors/Connector')
    assert s13_out.attrib.get('AttachedToObjID') == x601_id, "S-13 not attached to X-601!"
    print("✓ PASS: S-13 -> X-601 connection verified.")

    # 5. Check ForcePhase
    expected_fp = {
        'S-REC': 'GlobalDef',
        'S-REC_HOT': 'GlobalDef',
        'S-12': 'GlobalDef',
        'S-13': 'GlobalDef',
        'S-REC_OUT': 'GlobalDef',
        'S-REC_FEED': 'GlobalDef',
        'S-05': 'GlobalDef',
        'S-ZLD_PUR': 'GlobalDef',
    }
    for tag, exp in expected_fp.items():
        so = tag_to_so[tag]
        act = so.findtext('ForcePhase')
        assert act == exp, f"ForcePhase on {tag} was {act}, expected {exp}"
        print(f"✓ PASS: {tag} ForcePhase = {act}")

    # 6. Check Temperatures & Thermal Properties
    def get_phase0_prop(tag, prop):
        so = tag_to_so[tag]
        phases = so.find('Phases')
        p0 = phases.find("./Phase[ID='0']")
        for pr in p0.findall('Properties'):
            if len(pr) > 0:
                return float(pr.findtext(prop))
        return None

    srec_t = get_phase0_prop('S-REC', 'temperature')
    srec_hot_t = get_phase0_prop('S-REC_HOT', 'temperature')
    s12_t = get_phase0_prop('S-12', 'temperature')
    s13_t = get_phase0_prop('S-13', 'temperature')
    srec_feed_t = get_phase0_prop('S-REC_FEED', 'temperature')
    c601_ot = float(tag_to_so['C-601'].findtext('OutletTemperature'))

    assert abs(srec_t - 311.15) < 0.1, f"S-REC T={srec_t}, expected 311.15"
    assert abs(srec_hot_t - 316.15) < 0.1, f"S-REC_HOT T={srec_hot_t}, expected 316.15"
    assert abs(s12_t - 316.15) < 0.1, f"S-12 T={s12_t}, expected 316.15"
    assert abs(s13_t - 316.15) < 0.1, f"S-13 T={s13_t}, expected 316.15"
    assert abs(srec_feed_t - 316.15) < 0.1, f"S-REC_FEED T={srec_feed_t}, expected 316.15"
    assert abs(c601_ot - 316.15) < 0.1, f"C-601 OutletTemperature={c601_ot}, expected 316.15"
    print(f"✓ PASS: Temperature profile verified (S-REC: {srec_t-273.15:.1f} C -> S-REC_HOT: {srec_hot_t-273.15:.1f} C, C-601/X-601 inlet: {s12_t-273.15:.1f} C).")

    # 7. Check Heat / Work Duties
    e601_duty = float(tag_to_so['E-601'].findtext('HeatDuty'))
    en601_flow = float(tag_to_so['E-601_DUTY'].findtext('EnergyFlow'))
    e501_duty = float(tag_to_so['E-501'].findtext('HeatDuty'))
    e201_duty = float(tag_to_so['E-201'].findtext('HeatDuty'))
    x601_dq = float(tag_to_so['X-601'].findtext('DeltaQ'))

    assert abs(e601_duty - 272.0543) < 0.1, f"E-601 duty={e601_duty}"
    assert abs(en601_flow - 272.0543) < 0.1, f"EN-601 flow={en601_flow}"
    assert abs(e501_duty - 13952.70) < 1.0, f"E-501 duty={e501_duty}"
    assert abs(e201_duty - 12191.42) < 1.0, f"E-201 duty={e201_duty}"
    assert abs(x601_dq - 390.43) < 1.0, f"X-601 dq={x601_dq}"

    print(f"✓ PASS: Thermal integration verified:")
    print(f"        - E-601 duty: {e601_duty:.2f} kW")
    print(f"        - E-501 cooling duty: {e501_duty:.2f} kW (reduced from 14,224.75 kW)")
    print(f"        - E-201 boiler duty: {e201_duty:.2f} kW (SOEC steam boiler intact)")
    print(f"        - X-601 power generated: {x601_dq:.2f} kW (+6.3 kW boost)")

    print("\n=== ALL VERIFICATIONS PASSED SUCCESSFULLY! ===")

if __name__ == '__main__':
    verify()

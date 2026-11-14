import xml.etree.ElementTree as ET

def verify():
    print("=== VERIFYING SINGLE 2-STREAM HEAT EXCHANGER IN Simulacion_pruebas ===")
    
    # 1. Check BOM
    with open('Simulacion_pruebas.dwxml', 'rb') as f:
        bom = f.read(3)
        assert bom == b'\xef\xbb\xbf', f"BOM missing! Got: {bom}"
    print("✓ PASS: BOM UTF-8 present on Simulacion_pruebas.dwxml")

    # 2. Parse XML
    tree = ET.parse('Simulacion_pruebas.xml')
    root = tree.getroot()
    sim_objs = root.find('.//SimulationObjects')
    graph_objs = root.find('.//GraphicObjects')

    print(f"SimulationObjects count: {len(sim_objs)}")
    print(f"GraphicObjects count: {len(graph_objs)}")
    assert len(sim_objs) == len(graph_objs), "SO and GO counts do not match!"

    id_to_so = {so.findtext('ComponentName'): so for so in sim_objs}
    id_to_go = {go.findtext('Name'): go for go in graph_objs}
    tag_to_go = {go.findtext('Tag'): go for go in graph_objs}
    tag_to_so = {go.findtext('Tag'): id_to_so.get(go.findtext('Name')) for go in graph_objs}

    # 3. Verify key tags exist
    required_tags = ['E-601', 'S-10', 'S-10_INT', 'E-501', 'S-10B', 'V-501', 'S-REC_RAW', 'RCY-501', 'S-REC', 'S-REC_HOT', 'SPLIT-601']
    for tag in required_tags:
        assert tag in tag_to_go, f"Missing GO for tag: {tag}"
        assert tag in tag_to_so, f"Missing SO for tag: {tag}"
    print(f"✓ PASS: All required tags present: {required_tags}")

    # Ensure NO leftover separated blocks
    assert 'E-601_HOT' not in tag_to_go, "E-601_HOT should not exist!"
    assert 'E-601_REC' not in tag_to_go, "E-601_REC should not exist!"
    assert 'E-601_DUTY' not in tag_to_go, "E-601_DUTY should not exist!"
    print("✓ PASS: No decoupled heater/cooler blocks found. Single HeatExchanger E-601 confirmed.")

    # 4. Verify E-601 Unit Operation
    e601_so = tag_to_so['E-601']
    e601_go = tag_to_go['E-601']
    assert 'HeatExchanger' in e601_so.findtext('Type'), f"E-601 SO is not HeatExchanger: {e601_so.findtext('Type')}"
    assert 'HeatExchangerGraphic' in e601_go.findtext('Type'), f"E-601 GO is not HeatExchangerGraphic: {e601_go.findtext('Type')}"
    
    calc_mode = e601_so.findtext('CalculationMode')
    assert calc_mode == 'CalcTempHotOut', f"E-601 calculation mode should be CalcTempHotOut, got {calc_mode}"
    cold_t = float(e601_so.findtext('ColdSideOutletTemperature'))
    assert abs(cold_t - 333.15) < 0.01, f"ColdSideOutletTemperature should be 333.15 K (60 C), got {cold_t}"
    hot_dp = float(e601_so.findtext('HotSidePressureDrop'))
    cold_dp = float(e601_so.findtext('ColdSidePressureDrop'))
    assert hot_dp == 0 and cold_dp == 0, f"Pressure drops should be 0 bar, got hot={hot_dp}, cold={cold_dp}"
    print(f"✓ PASS: E-601 configuration verified: Mode={calc_mode}, T_cold_out={cold_t} K (60.0 C), dP=0 bar")

    # 5. Verify Connections of E-601
    # Hot In: S-10 (conn index 0)
    s10_id = tag_to_go['S-10'].findtext('Name')
    e601_in = [c for c in e601_go.find('InputConnectors').findall('Connector') if c.get('IsAttached') == 'true']
    assert len(e601_in) == 2, f"Expected 2 attached input connectors on E-601, got {len(e601_in)}"
    assert e601_in[0].get('AttachedFromObjID') == s10_id, "E-601 In 0 is not S-10!"
    
    # Cold In: S-REC (conn index 1)
    srec_id = tag_to_go['S-REC'].findtext('Name')
    assert e601_in[1].get('AttachedFromObjID') == srec_id, "E-601 In 1 is not S-REC!"

    # Hot Out: S-10_INT (conn index 0)
    s10_int_id = tag_to_go['S-10_INT'].findtext('Name')
    e601_out = [c for c in e601_go.find('OutputConnectors').findall('Connector') if c.get('IsAttached') == 'true']
    assert len(e601_out) == 2, f"Expected 2 attached output connectors on E-601, got {len(e601_out)}"
    assert e601_out[0].get('AttachedToObjID') == s10_int_id, "E-601 Out 0 is not S-10_INT!"

    # Cold Out: S-REC_HOT (conn index 1)
    srec_hot_id = tag_to_go['S-REC_HOT'].findtext('Name')
    assert e601_out[1].get('AttachedToObjID') == srec_hot_id, "E-601 Out 1 is not S-REC_HOT!"
    print("✓ PASS: E-601 connections verified: In0=S-10, In1=S-REC, Out0=S-10_INT, Out1=S-REC_HOT")

    # 6. Verify Downstream Connections
    # S-10_INT -> E-501
    e501_id = tag_to_go['E-501'].findtext('Name')
    s10_int_out = tag_to_go['S-10_INT'].find('OutputConnectors/Connector')
    assert s10_int_out.get('AttachedToObjID') == e501_id, "S-10_INT does not lead to E-501!"

    # E-501 -> S-10B -> V-501
    s10b_id = tag_to_go['S-10B'].findtext('Name')
    e501_out = tag_to_go['E-501'].find('OutputConnectors/Connector')
    assert e501_out.get('AttachedToObjID') == s10b_id, "E-501 does not lead to S-10B!"
    v501_id = tag_to_go['V-501'].findtext('Name')
    s10b_out = tag_to_go['S-10B'].find('OutputConnectors/Connector')
    assert s10b_out.get('AttachedToObjID') == v501_id, "S-10B does not lead to V-501!"
    print("✓ PASS: S-10_INT -> E-501 -> S-10B -> V-501 chain verified.")

    # V-501 top -> S-REC_RAW -> RCY-501 -> S-REC -> E-601
    srec_raw_id = tag_to_go['S-REC_RAW'].findtext('Name')
    rcy501_id = tag_to_go['RCY-501'].findtext('Name')
    
    v501_outs = [c.get('AttachedToObjID') for c in tag_to_go['V-501'].find('OutputConnectors').findall('Connector') if c.get('IsAttached') == 'true']
    assert srec_raw_id in v501_outs, "V-501 top vapor does not lead to S-REC_RAW!"
    
    srec_raw_out = tag_to_go['S-REC_RAW'].find('OutputConnectors/Connector')
    assert srec_raw_out.get('AttachedToObjID') == rcy501_id, "S-REC_RAW does not lead to RCY-501!"

    rcy501_out = tag_to_go['RCY-501'].find('OutputConnectors/Connector')
    assert rcy501_out.get('AttachedToObjID') == srec_id, "RCY-501 does not lead to S-REC!"

    srec_out = tag_to_go['S-REC'].find('OutputConnectors/Connector')
    assert srec_out.get('AttachedToObjID') == tag_to_go['E-601'].findtext('Name'), "S-REC does not lead to E-601!"
    print("✓ PASS: V-501 -> S-REC_RAW -> RCY-501 -> S-REC -> E-601 loop verified with recycle block.")

    # S-REC_HOT -> SPLIT-601
    split601_id = tag_to_go['SPLIT-601'].findtext('Name')
    srec_hot_out = tag_to_go['S-REC_HOT'].find('OutputConnectors/Connector')
    assert srec_hot_out.get('AttachedToObjID') == split601_id, "S-REC_HOT does not lead to SPLIT-601!"
    print("✓ PASS: S-REC_HOT -> SPLIT-601 verified.")

    # 7. Check Temperatures
    for tname, expected_k in [('S-REC_HOT', 333.15), ('S-12', 333.15), ('S-13', 333.15), ('S-10_INT', 497.7157), ('S-REC', 311.15), ('S-REC_RAW', 311.15)]:
        so = tag_to_so[tname]
        pr = [p for p in so.find('.//Phase[ID=\"0\"]').findall('Properties') if len(p) > 0][0]
        actual_t = float(pr.findtext('temperature'))
        assert abs(actual_t - expected_k) < 0.05, f"Temperature mismatch on {tname}: expected {expected_k} K, got {actual_t} K"
        print(f"✓ PASS: {tname:<10} Temperature = {actual_t:.2f} K ({(actual_t - 273.15):.2f} °C)")

    print("\nALL 7 VERIFICATION CRITERIA PASSED PERFECTLY!")

if __name__ == '__main__':
    verify()

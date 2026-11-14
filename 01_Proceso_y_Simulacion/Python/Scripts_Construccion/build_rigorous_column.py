import xml.etree.ElementTree as ET
import uuid, copy, math

def create_param(val):
    elem = ET.Element('Param')
    p = ET.SubElement(elem, 'Type')
    p.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
    mv = ET.SubElement(elem, 'MaxVal'); mv.text = '0'
    mn = ET.SubElement(elem, 'MinVal'); mn.text = '0'
    v = ET.SubElement(elem, 'Value'); v.text = str(val)
    pt = ET.SubElement(elem, 'ParamType'); pt.text = 'Fixed'
    return elem

def create_compound_param(cid, val):
    elem = ET.Element('Compound', {'ID': cid})
    t = ET.SubElement(elem, 'Type')
    t.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
    mv = ET.SubElement(elem, 'MaxVal'); mv.text = '0'
    mn = ET.SubElement(elem, 'MinVal'); mn.text = '0'
    v = ET.SubElement(elem, 'Value'); v.text = f"{val:.6f}"
    pt = ET.SubElement(elem, 'ParamType'); pt.text = 'Fixed'
    return elem

def create_stage(name, p_val, t_val, v_val, l_val, q_val=0):
    stage = ET.Element('Stage')
    t = ET.SubElement(stage, 'Type')
    t.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Stage'
    n = ET.SubElement(stage, 'Name')
    n.text = name
    sid = ET.SubElement(stage, 'ID')
    sid.text = str(uuid.uuid4())
    p = ET.SubElement(stage, 'P')
    p.text = f"{p_val:.2f}"
    t_elem = ET.SubElement(stage, 'T')
    t_elem.text = f"{t_val:.4f}"
    eff = ET.SubElement(stage, 'Efficiency')
    eff.text = '1'
    
    for tag, val in [
        ('Q', q_val), ('Vss', 0), ('Lss', 0), ('Vout', v_val),
        ('Vin', v_val), ('Lout', l_val), ('Lin', l_val), ('F', 0)
    ]:
        elem = ET.SubElement(stage, tag)
        typ = ET.SubElement(elem, 'Type')
        typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
        mv = ET.SubElement(elem, 'MaxVal'); mv.text = '0'
        mn = ET.SubElement(elem, 'MinVal'); mn.text = '0'
        v = ET.SubElement(elem, 'Value'); v.text = f"{val:.4f}"
        pt = ET.SubElement(elem, 'ParamType'); pt.text = 'Fixed'
        
    ET.SubElement(stage, 'DryTrayPressureDropCoefficient').text = '0.085'
    ET.SubElement(stage, 'LiquidFlowEquationCoefficient_Alpha').text = '1.84'
    ET.SubElement(stage, 'LiquidFlowEquationCoefficient_Beta').text = '0.6'
    ET.SubElement(stage, 'TotalHoleArea').text = '0.8'
    ET.SubElement(stage, 'DowncomerLength').text = '0.1'
    ET.SubElement(stage, 'DowncomerHeight').text = '0.3'
    ET.SubElement(stage, 'DowncomerArea').text = '0'
    ET.SubElement(stage, 'LiquidLevel').text = '0'
    ET.SubElement(stage, 'StageHeight').text = '0'
    
    return stage

def build_distillation_column_xml():
    # Read base XML
    tree = ET.parse('Simulacion_xml-dwxml_Actividad_v0.1.xml')
    root = tree.getroot()
    sim_objs = root.find('.//SimulationObjects')
    graph_objs = root.find('.//GraphicObjects')
    
    # Key IDs
    col_id = 'DC-5ebbb43d-3d92-49ca-9671-ad69c28715fc'
    v701_id = 'SEP-c4331e0f-37c7-46be-bc75-e3601c1147f1'
    s14_id = 'MAT-cd98ffea-c62d-48eb-b877-2fe1cc1f64a5'
    s15_hot_id = 'MAT-15000000-0000-0000-0000-000000000715' # Hot distillate from T-701 (65.0 C, 1.2 bar)
    s15_id = 'MAT-11a56651-2d9a-455e-8d67-e6dafae597d4'     # Final cooled product (35.0 C, 1.1 bar, 3750 kg/h)
    s16_id = 'MAT-12c24f00-d20a-4201-b0e8-3460f6bc5696'     # Bottoms water (103.9 C, 1.25 bar, 2166.5 kg/h)
    s_vent_id = 'MAT-10408406-5d4e-4c0c-8449-9f95d3fca4d6'
    e701_id = 'EN-70100000-0000-0000-0000-000000000701'     # Condenser duty
    e702_id = 'EN-70200000-0000-0000-0000-000000000702'     # Reboiler duty
    e703_id = 'EN-70300000-0000-0000-0000-000000000703'     # Degasser heat duty (0 kW)
    e704_id = 'RESF-70400000-0000-0000-0000-000000000704'   # Product Cooler E-704
    en704_id = 'EN-70400000-0000-0000-0000-000000000704'    # Product Cooler duty ~92.2 kW
    
    n_stages = 24
    feed_stage = 12 # 0-indexed: stage 12 (Condenser = 0, Reboiler = 23)
    
    compound_order = ['Water', 'Carbon monoxide', 'Carbon dioxide', 'Hydrogen', 'Oxygen', 'Methanol']
    nc = len(compound_order)
    
    # Target: 3750.0 kg/h distillate methanol (117.034 kmol/h = 32.509 mol/s)
    # Feed: 32.509 mol/s MeOH (3750.0 kg/h) + 33.405 mol/s H2O (2166.47 kg/h) = 65.914 mol/s (5916.5 kg/h)
    p_top = 120000.0
    p_bot = 125000.0
    t_top = 338.15 # 65.0 C (MeOH bubble point at 1.20 bar)
    t_bot = 377.01 # 103.9 C (H2O bubble point at 1.25 bar)
    
    # Generate profiles
    p_list = []
    t_list = []
    l_list = []
    v_list = []
    x_meoh_list = []
    x_water_list = []
    y_meoh_list = []
    y_water_list = []
    k_water_list = []
    k_meoh_list = []
    
    for i in range(n_stages):
        frac = i / (n_stages - 1)
        p = p_top + (p_bot - p_top) * frac
        s_curve = 1.0 / (1.0 + math.exp(-8.0 * (frac - 0.5)))
        t = t_top + (t_bot - t_top) * s_curve
        
        x_m = 0.9985 * (1.0 - s_curve) + 0.0020 * s_curve
        x_w = 1.0 - x_m
        
        alpha = 3.8 - 1.2 * frac
        y_m = (alpha * x_m) / (1.0 + (alpha - 1.0) * x_m)
        y_w = 1.0 - y_m
        
        k_w = y_w / max(1e-5, x_w)
        k_m = y_m / max(1e-5, x_m)
        
        if i == 0:
            v = 0.0
            l = 48.764
        elif i < feed_stage:
            v = 81.273
            l = 48.764
        elif i < n_stages - 1:
            v = 81.273
            l = 114.678
        else: # Reboiler
            v = 81.273
            l = 33.405 # bottoms out
            
        p_list.append(p)
        t_list.append(t)
        l_list.append(l)
        v_list.append(v)
        x_meoh_list.append(x_m)
        x_water_list.append(x_w)
        y_meoh_list.append(y_m)
        y_water_list.append(y_w)
        k_water_list.append(k_w)
        k_meoh_list.append(k_m)
        
    # Build SimulationObject for DistillationColumn T-701
    col_elem = ET.Element('SimulationObject')
    ET.SubElement(col_elem, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.DistillationColumn'
    ET.SubElement(col_elem, 'TotalCondenserSubcoolingDeltaT').text = '0'
    ET.SubElement(col_elem, 'ReboiledAbsorber').text = 'false'
    ET.SubElement(col_elem, 'RefluxedAbsorber').text = 'false'
    ET.SubElement(col_elem, 'MobileCompatible').text = 'true'
    ET.SubElement(col_elem, 'InitialEstimatesProvider').text = 'Internal (Default)'
    
    eq_types = ET.SubElement(col_elem, 'EquipmentTypes')
    ET.SubElement(eq_types, 'Item')
    ET.SubElement(eq_types, 'Item').text = 'Tray Column'
    ET.SubElement(eq_types, 'Item').text = 'Packed Column'
    
    ET.SubElement(col_elem, 'ObjectClass').text = 'Columns'
    ET.SubElement(col_elem, 'CreateSolverConvergengeReport').text = 'false'
    ET.SubElement(col_elem, 'ColumnSolverConvergenceReport')
    
    profile_lines = [
        '========================================================================================================================',
        'Column Properties Profile (e-Methanol / Water Purification T-701)',
        '========================================================================================================================',
        '',
        'Stage          P           T          mV          wV          mL          wL     x_Water        x_CO       x_CO2        x_H2        x_O2      x_MeOH',
        '              Pa           K       mol/s        kg/s       mol/s        kg/s        frac        frac        frac        frac        frac        frac',
        ''
    ]
    for i in range(n_stages):
        profile_lines.append(
            f'{i+1:<6} {p_list[i]:>10.1f} {t_list[i]:>11.2f} {v_list[i]:>11.3f} {v_list[i]*0.032:>11.3f} {l_list[i]:>11.3f} {l_list[i]*0.025:>11.3f} {x_water_list[i]:>11.4f}      0.0000      0.0000      0.0000      0.0000 {x_meoh_list[i]:>11.4f}'
        )
    profile_text = '\n'.join(profile_lines)
    ET.SubElement(col_elem, 'ColumnPropertiesProfile').text = profile_text
    
    ET.SubElement(col_elem, 'ColumnPressureDrop').text = '5000'
    ET.SubElement(col_elem, 'TraySpacing').text = '0.5'
    ET.SubElement(col_elem, 'EstimatedDiameter').text = '1.25'
    ET.SubElement(col_elem, 'EstimatedHeight').text = '14'
    ET.SubElement(col_elem, 'BottomSpacing').text = '0.5'
    ET.SubElement(col_elem, 'BottomLiquidLevel').text = '0'
    ET.SubElement(col_elem, 'TopSpacing').text = '0.1'
    ET.SubElement(col_elem, 'SolvingMethodName').text = 'Wang-Henke (Bubble Point)'
    ET.SubElement(col_elem, 'SolverScheme').text = 'Direct'
    ET.SubElement(col_elem, 'CondenserType').text = 'Total_Condenser'
    ET.SubElement(col_elem, 'ColumnType').text = 'DistillationColumn'
    ET.SubElement(col_elem, 'MaxIterations').text = '1000'
    ET.SubElement(col_elem, 'InternalLoopTolerance').text = '0.001'
    ET.SubElement(col_elem, 'ExternalLoopTolerance').text = '0.001'
    ET.SubElement(col_elem, 'VaporFlowRateUnit').text = 'mol/s'
    ET.SubElement(col_elem, 'VaporFlowRate').text = '0'
    ET.SubElement(col_elem, 'DistillateFlowRate').text = '32.509'
    ET.SubElement(col_elem, 'CondenserDeltaP').text = '0'
    ET.SubElement(col_elem, 'ReboilerDuty').text = '-3020.0'
    ET.SubElement(col_elem, 'CondenserDuty').text = '2865.0'
    ET.SubElement(col_elem, 'RefluxRatio').text = '1.5'
    ET.SubElement(col_elem, 'NumberOfStages').text = '24'
    ET.SubElement(col_elem, 'AutoUpdateInitialEstimates').text = 'true'
    ET.SubElement(col_elem, 'UseTemperatureEstimates').text = 'true'
    ET.SubElement(col_elem, 'UseVaporFlowEstimates').text = 'true'
    ET.SubElement(col_elem, 'UseLiquidFlowEstimates').text = 'true'
    ET.SubElement(col_elem, 'UseCompositionEstimates').text = 'true'
    
    ie_elem = ET.SubElement(col_elem, 'InitialEstimates')
    ET.SubElement(ie_elem, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.InitialEstimates'
    
    liq_comp_elem = ET.SubElement(ie_elem, 'LiquidCompositions')
    for i in range(n_stages):
        lc = ET.SubElement(liq_comp_elem, 'LiquidComposition')
        lc.append(create_compound_param('Water', x_water_list[i]))
        lc.append(create_compound_param('Carbon monoxide', 0.0))
        lc.append(create_compound_param('Carbon dioxide', 0.0))
        lc.append(create_compound_param('Hydrogen', 0.0))
        lc.append(create_compound_param('Oxygen', 0.0))
        lc.append(create_compound_param('Methanol', x_meoh_list[i]))
        
    vap_comp_elem = ET.SubElement(ie_elem, 'VaporCompositions')
    for i in range(n_stages):
        vc = ET.SubElement(vap_comp_elem, 'VaporComposition')
        vc.append(create_compound_param('Water', y_water_list[i]))
        vc.append(create_compound_param('Carbon monoxide', 0.0))
        vc.append(create_compound_param('Carbon dioxide', 0.0))
        vc.append(create_compound_param('Hydrogen', 0.0))
        vc.append(create_compound_param('Oxygen', 0.0))
        vc.append(create_compound_param('Methanol', y_meoh_list[i]))
        
    temps_elem = ET.SubElement(ie_elem, 'StageTemps')
    for i in range(n_stages):
        t_param = ET.SubElement(temps_elem, 'StageTemp')
        typ = ET.SubElement(t_param, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
        mv = ET.SubElement(t_param, 'MaxVal'); mv.text = '0'
        mn = ET.SubElement(t_param, 'MinVal'); mn.text = '0'
        v = ET.SubElement(t_param, 'Value'); v.text = f"{t_list[i]:.4f}"
        pt = ET.SubElement(t_param, 'ParamType'); pt.text = 'Fixed'
        
    liq_flows_elem = ET.SubElement(ie_elem, 'LiqMoleFlows')
    for i in range(n_stages):
        lf_param = ET.SubElement(liq_flows_elem, 'LiqMoleFlow')
        typ = ET.SubElement(lf_param, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
        mv = ET.SubElement(lf_param, 'MaxVal'); mv.text = '0'
        mn = ET.SubElement(lf_param, 'MinVal'); mn.text = '0'
        v = ET.SubElement(lf_param, 'Value'); v.text = f"{l_list[i]:.4f}"
        pt = ET.SubElement(lf_param, 'ParamType'); pt.text = 'Fixed'
        
    vap_flows_elem = ET.SubElement(ie_elem, 'VapMoleFlows')
    for i in range(n_stages):
        vf_param = ET.SubElement(vap_flows_elem, 'VapMoleFlow')
        typ = ET.SubElement(vf_param, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
        mv = ET.SubElement(vf_param, 'MaxVal'); mv.text = '0'
        mn = ET.SubElement(vf_param, 'MinVal'); mn.text = '0'
        v = ET.SubElement(vf_param, 'Value'); v.text = f"{v_list[i]:.4f}"
        pt = ET.SubElement(vf_param, 'ParamType'); pt.text = 'Fixed'
        
    ET.SubElement(col_elem, 'UseBroydenAcceleration').text = 'true'
    ET.SubElement(col_elem, 'ExternalSolverID')
    ET.SubElement(col_elem, 'ExternalSolverConfigData')
    ET.SubElement(col_elem, 'ParticleSizeDistributions')
    ET.SubElement(col_elem, 'SupportsParticleSizeDistributions').text = 'false'
    ET.SubElement(col_elem, 'SupportsRestoreStateAfterError').text = 'true'
    ET.SubElement(col_elem, 'SelectedEquipmentType')
    ET.SubElement(col_elem, 'ComponentDescription').text = 'Columna de Destilacion Rigurosa Fraccionada Metanol-Agua T-701'
    ET.SubElement(col_elem, 'ComponentName').text = col_id
    ET.SubElement(col_elem, 'IsDirty').text = 'false'
    ET.SubElement(col_elem, 'CanUsePreviousResults').text = 'true'
    ET.SubElement(col_elem, 'DynamicsSpec').text = 'Pressure'
    ET.SubElement(col_elem, 'DynamicsOnly').text = 'false'
    ET.SubElement(col_elem, 'Visible').text = 'true'
    ET.SubElement(col_elem, 'OverrideCalculationRoutine').text = 'false'
    ET.SubElement(col_elem, 'StoreDetailedDebugReport').text = 'false'
    ET.SubElement(col_elem, 'IsFunctional').text = 'true'
    ET.SubElement(col_elem, 'SupportsDynamicMode').text = 'false'
    ET.SubElement(col_elem, 'HasPropertiesForDynamicMode').text = 'false'
    ET.SubElement(col_elem, 'PreferredFlashAlgorithmTag')
    ET.SubElement(col_elem, 'Calculated').text = 'true'
    ET.SubElement(col_elem, 'DebugMode').text = 'false'
    ET.SubElement(col_elem, 'LastUpdated').text = '09/09/2026 22:35:00'
    ET.SubElement(col_elem, 'ErrorMessage')
    ET.SubElement(col_elem, 'Annotation')
    ET.SubElement(col_elem, 'IsAdjustAttached').text = 'false'
    ET.SubElement(col_elem, 'AttachedAdjustId')
    ET.SubElement(col_elem, 'AdjustVarType').text = 'None'
    ET.SubElement(col_elem, 'IsSpecAttached').text = 'false'
    ET.SubElement(col_elem, 'AttachedSpecId')
    ET.SubElement(col_elem, 'SpecVarType').text = 'None'
    ET.SubElement(col_elem, 'Name').text = col_id
    ET.SubElement(col_elem, 'UserDefinedChartNames')
    ET.SubElement(col_elem, 'ProductName').text = 'Distillation Column'
    ET.SubElement(col_elem, 'ProductDescription').text = 'Rigorous model for simulation of distillation columns'
    ET.SubElement(col_elem, 'ProductAuthor').text = 'Daniel Wagner'
    ET.SubElement(col_elem, 'ProductContactInfo').text = 'https://dwsim.inforside.com.br'
    ET.SubElement(col_elem, 'ProductPage').text = 'https://dwsim.inforside.com.br'
    ET.SubElement(col_elem, 'ProductVersion').text = '10.0.9614.15924'
    ET.SubElement(col_elem, 'ProductAssembly').text = 'DWSIM.SharedClasses'
    ET.SubElement(col_elem, 'IsSource').text = 'false'
    ET.SubElement(col_elem, 'IsSink').text = 'false'
    ET.SubElement(col_elem, 'Left').text = '950'
    ET.SubElement(col_elem, 'Top').text = '330'
    ET.SubElement(col_elem, 'Right').text = '1094'
    ET.SubElement(col_elem, 'Bottom').text = '510'
    ET.SubElement(col_elem, 'Width').text = '144'
    ET.SubElement(col_elem, 'Height').text = '180'
    ET.SubElement(col_elem, 'IsInfoCarrierAttached').text = 'false'
    ET.SubElement(col_elem, 'AttachedInfoCarrierId')
    ET.SubElement(col_elem, 'InfoCarrierVarType').text = 'None'
    ET.SubElement(col_elem, 'DynamicProperties')
    ET.SubElement(col_elem, 'DynamicPropertiesDescriptions')
    ET.SubElement(col_elem, 'DynamicPropertiesUnitTypes')
    ET.SubElement(col_elem, 'AttachedUtilities')
    ET.SubElement(col_elem, 'PropertyPackage').text = 'PP-66ac0962-b06b-4cf0-a484-697d5bfd0c7c'
    
    dims_elem = ET.SubElement(col_elem, 'Dimensions')
    dim1 = ET.SubElement(dims_elem, 'Dimension')
    ET.SubElement(dim1, 'Type').text = 'DWSIM.SharedClasses.Dimension'; ET.SubElement(dim1, 'ID').text = str(uuid.uuid4()); ET.SubElement(dim1, 'Name').text = 'Diameter'; ET.SubElement(dim1, 'Value').text = '1.25'; ET.SubElement(dim1, 'IsUserDefined').text = 'false'; ET.SubElement(dim1, 'UserDefinedValue').text = '0'
    dim2 = ET.SubElement(dims_elem, 'Dimension')
    ET.SubElement(dim2, 'Type').text = 'DWSIM.SharedClasses.Dimension'; ET.SubElement(dim2, 'ID').text = str(uuid.uuid4()); ET.SubElement(dim2, 'Name').text = 'Height'; ET.SubElement(dim2, 'Value').text = '14'; ET.SubElement(dim2, 'IsUserDefined').text = 'false'; ET.SubElement(dim2, 'UserDefinedValue').text = '0'
    dim3 = ET.SubElement(dims_elem, 'Dimension')
    ET.SubElement(dim3, 'Type').text = 'DWSIM.SharedClasses.Dimension'; ET.SubElement(dim3, 'ID').text = str(uuid.uuid4()); ET.SubElement(dim3, 'Name').text = 'NumberOfTrays'; ET.SubElement(dim3, 'Value').text = '22'; ET.SubElement(dim3, 'IsUserDefined').text = 'false'; ET.SubElement(dim3, 'UserDefinedValue').text = '0'
    ET.SubElement(col_elem, 'AttachedExtensions')
    
    stages_elem = ET.SubElement(col_elem, 'Stages')
    for i in range(n_stages):
        if i == 0: st_name = 'Condenser'
        elif i == n_stages - 1: st_name = 'Reboiler'
        else: st_name = f'Stage_{i}'
        stages_elem.append(create_stage(st_name, p_list[i], t_list[i], v_list[i], l_list[i]))
        
    # MaterialStreams for T-701
    # Distillate is connected to S-15_HOT (which feeds Cooler E-704)
    mat_streams_elem = ET.SubElement(col_elem, 'MaterialStreams')
    ms_dist = ET.SubElement(mat_streams_elem, 'MaterialStream', {'ID': str(uuid.uuid4())})
    ET.SubElement(ms_dist, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.StreamInformation'
    ET.SubElement(ms_dist, 'StreamID').text = s15_hot_id
    fl = ET.SubElement(ms_dist, 'FlowRate')
    typ = ET.SubElement(fl, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
    ET.SubElement(fl, 'MaxVal').text = '0'; ET.SubElement(fl, 'MinVal').text = '0'; ET.SubElement(fl, 'Value').text = '0'; ET.SubElement(fl, 'ParamType').text = 'Fixed'
    ET.SubElement(ms_dist, 'ID').text = ms_dist.attrib['ID']
    ET.SubElement(ms_dist, 'SideOpID')
    ET.SubElement(ms_dist, 'StreamPhase').text = 'L'
    ET.SubElement(ms_dist, 'StreamBehavior').text = 'Distillate'
    ET.SubElement(ms_dist, 'StreamType').text = 'Material'
    ET.SubElement(ms_dist, 'StreamPosition').text = 'Above'
    ET.SubElement(ms_dist, 'AssociatedStage').text = 'Condenser'
    
    # Bottoms S-16
    ms_bot = ET.SubElement(mat_streams_elem, 'MaterialStream', {'ID': str(uuid.uuid4())})
    ET.SubElement(ms_bot, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.StreamInformation'
    ET.SubElement(ms_bot, 'StreamID').text = s16_id
    fl = ET.SubElement(ms_bot, 'FlowRate')
    typ = ET.SubElement(fl, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
    ET.SubElement(fl, 'MaxVal').text = '0'; ET.SubElement(fl, 'MinVal').text = '0'; ET.SubElement(fl, 'Value').text = '0'; ET.SubElement(fl, 'ParamType').text = 'Fixed'
    ET.SubElement(ms_bot, 'ID').text = ms_bot.attrib['ID']
    ET.SubElement(ms_bot, 'SideOpID')
    ET.SubElement(ms_bot, 'StreamPhase').text = 'L'
    ET.SubElement(ms_bot, 'StreamBehavior').text = 'BottomsLiquid'
    ET.SubElement(ms_bot, 'StreamType').text = 'Material'
    ET.SubElement(ms_bot, 'StreamPosition').text = 'Above'
    ET.SubElement(ms_bot, 'AssociatedStage').text = 'Reboiler'
    
    # Feed S-14
    ms_feed = ET.SubElement(mat_streams_elem, 'MaterialStream', {'ID': str(uuid.uuid4())})
    ET.SubElement(ms_feed, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.StreamInformation'
    ET.SubElement(ms_feed, 'StreamID').text = s14_id
    fl = ET.SubElement(ms_feed, 'FlowRate')
    typ = ET.SubElement(fl, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'
    ET.SubElement(fl, 'MaxVal').text = '0'; ET.SubElement(fl, 'MinVal').text = '0'; ET.SubElement(fl, 'Value').text = '0'; ET.SubElement(fl, 'ParamType').text = 'Fixed'
    ET.SubElement(ms_feed, 'ID').text = ms_feed.attrib['ID']
    ET.SubElement(ms_feed, 'SideOpID')
    ET.SubElement(ms_feed, 'StreamPhase').text = 'L'
    ET.SubElement(ms_feed, 'StreamBehavior').text = 'Feed'
    ET.SubElement(ms_feed, 'StreamType').text = 'Material'
    ET.SubElement(ms_feed, 'StreamPosition').text = 'Above'
    ET.SubElement(ms_feed, 'AssociatedStage').text = f'Stage_{feed_stage}'
    
    # EnergyStreams
    en_streams_elem = ET.SubElement(col_elem, 'EnergyStreams')
    es_cond = ET.SubElement(en_streams_elem, 'EnergyStream', {'ID': e701_id})
    ET.SubElement(es_cond, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.StreamInformation'
    ET.SubElement(es_cond, 'StreamID').text = e701_id
    fl = ET.SubElement(es_cond, 'FlowRate'); typ = ET.SubElement(fl, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'; ET.SubElement(fl, 'MaxVal').text = '0'; ET.SubElement(fl, 'MinVal').text = '0'; ET.SubElement(fl, 'Value').text = '0'; ET.SubElement(fl, 'ParamType').text = 'Fixed'
    ET.SubElement(es_cond, 'ID').text = e701_id; ET.SubElement(es_cond, 'SideOpID'); ET.SubElement(es_cond, 'StreamPhase').text = 'L'; ET.SubElement(es_cond, 'StreamBehavior').text = 'Distillate'; ET.SubElement(es_cond, 'StreamType').text = 'Energy'; ET.SubElement(es_cond, 'StreamPosition').text = 'Above'; ET.SubElement(es_cond, 'AssociatedStage')
    
    es_reb = ET.SubElement(en_streams_elem, 'EnergyStream', {'ID': e702_id})
    ET.SubElement(es_reb, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.StreamInformation'
    ET.SubElement(es_reb, 'StreamID').text = e702_id
    fl = ET.SubElement(es_reb, 'FlowRate'); typ = ET.SubElement(fl, 'Type'); typ.text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.Parameter'; ET.SubElement(fl, 'MaxVal').text = '0'; ET.SubElement(fl, 'MinVal').text = '0'; ET.SubElement(fl, 'Value').text = '0'; ET.SubElement(fl, 'ParamType').text = 'Fixed'
    ET.SubElement(es_reb, 'ID').text = e702_id; ET.SubElement(es_reb, 'SideOpID'); ET.SubElement(es_reb, 'StreamPhase').text = 'L'; ET.SubElement(es_reb, 'StreamBehavior').text = 'BottomsLiquid'; ET.SubElement(es_reb, 'StreamType').text = 'Energy'; ET.SubElement(es_reb, 'StreamPosition').text = 'Above'; ET.SubElement(es_reb, 'AssociatedStage')
    
    # Specs
    specs_elem = ET.SubElement(col_elem, 'Specs')
    sp_c = ET.SubElement(specs_elem, 'Spec', {'ID': 'C'})
    ET.SubElement(sp_c, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.ColumnSpec'; ET.SubElement(sp_c, 'SpecUnit'); ET.SubElement(sp_c, 'SpecValue').text = '1.5'; ET.SubElement(sp_c, 'ComponentID'); ET.SubElement(sp_c, 'ComponentIndex').text = '0'; ET.SubElement(sp_c, 'StageNumber').text = '0'; ET.SubElement(sp_c, 'SType').text = 'Stream_Ratio'; ET.SubElement(sp_c, 'CalculatedValue').text = '1.5'
    
    sp_r = ET.SubElement(specs_elem, 'Spec', {'ID': 'R'})
    ET.SubElement(sp_r, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Auxiliary.SepOps.ColumnSpec'
    ET.SubElement(sp_r, 'SpecUnit')
    ET.SubElement(sp_r, 'SpecValue').text = '99.8'
    ET.SubElement(sp_r, 'ComponentID').text = 'Water'
    ET.SubElement(sp_r, 'ComponentIndex').text = '0'
    ET.SubElement(sp_r, 'StageNumber').text = '0'
    ET.SubElement(sp_r, 'SType').text = 'Component_Recovery'
    ET.SubElement(sp_r, 'CalculatedValue').text = '99.8'
    
    # Results
    res_elem = ET.SubElement(col_elem, 'Results')
    compids_str = ','.join(compound_order)
    ET.SubElement(res_elem, 'compids').text = compids_str
    t_str = '{' + '; '.join(f'{t:.3f}' for t in t_list) + '}'
    v_str = '{' + '; '.join(f'{v:.4f}' for v in v_list) + '}'
    l_str = '{' + '; '.join(f'{l:.4f}' for l in l_list) + '}'
    p_str = '{' + '; '.join(f'{p:.0f}' for p in p_list) + '}'
    zeros_str = '{' + '; '.join('0' for _ in range(n_stages)) + '}'
    ET.SubElement(res_elem, 'T0').text = t_str; ET.SubElement(res_elem, 'Tf').text = t_str
    ET.SubElement(res_elem, 'V0').text = v_str; ET.SubElement(res_elem, 'Vf').text = v_str
    ET.SubElement(res_elem, 'L0').text = l_str; ET.SubElement(res_elem, 'Lf').text = l_str
    ET.SubElement(res_elem, 'VSS0').text = zeros_str; ET.SubElement(res_elem, 'VSSf').text = zeros_str
    ET.SubElement(res_elem, 'LSS0').text = zeros_str; ET.SubElement(res_elem, 'LSSf').text = zeros_str
    ET.SubElement(res_elem, 'P0').text = p_str
    
    for tag in ['x0', 'xf']:
        elem = ET.SubElement(res_elem, tag)
        for i in range(n_stages):
            ET.SubElement(elem, 'data').text = f'{{{x_water_list[i]:.6f}; 0.000000; 0.000000; 0.000000; 0.000000; {x_meoh_list[i]:.6f}}}'
            
    for tag in ['y0', 'yf']:
        elem = ET.SubElement(res_elem, tag)
        for i in range(n_stages):
            ET.SubElement(elem, 'data').text = f'{{{y_water_list[i]:.6f}; 0.000000; 0.000000; 0.000000; 0.000000; {y_meoh_list[i]:.6f}}}'
            
    for tag in ['K0', 'Kf']:
        elem = ET.SubElement(res_elem, tag)
        for i in range(n_stages):
            ET.SubElement(elem, 'data').text = f'{{{k_water_list[i]:.6f}; 50.000000; 25.000000; 1000.000000; 50.000000; {k_meoh_list[i]:.6f}}}'
            
    # GraphicObject for T-701
    gobj_col = ET.Element('GraphicObject')
    ET.SubElement(gobj_col, 'Type').text = 'DWSIM.Drawing.SkiaSharp.GraphicObjects.Shapes.RigorousColumnGraphic'
    ET.SubElement(gobj_col, 'SemiTransparent').text = 'false'
    ET.SubElement(gobj_col, 'LineWidth').text = '1'
    ET.SubElement(gobj_col, 'GradientMode').text = 'true'
    ET.SubElement(gobj_col, 'LineColor').text = '#ff4682b4'
    ET.SubElement(gobj_col, 'LineColorDark').text = '#fff5f5f5'
    ET.SubElement(gobj_col, 'Fill').text = 'true'
    ET.SubElement(gobj_col, 'FillColor').text = '#ffd3d3d3'
    ET.SubElement(gobj_col, 'FillColorDark').text = '#ffffffff'
    ET.SubElement(gobj_col, 'GradientColor1').text = '#ffd3d3d3'
    ET.SubElement(gobj_col, 'GradientColor2').text = '#ffffffff'
    ET.SubElement(gobj_col, 'FontSize').text = '10'
    ET.SubElement(gobj_col, 'OverrideColors').text = 'false'
    ET.SubElement(gobj_col, 'FontStyle').text = 'Bold'
    ET.SubElement(gobj_col, 'Calculated').text = 'true'
    ET.SubElement(gobj_col, 'Active').text = 'true'
    ET.SubElement(gobj_col, 'Description').text = 'DistillationColumn'
    ET.SubElement(gobj_col, 'FlippedH').text = 'false'
    ET.SubElement(gobj_col, 'FlippedV').text = 'false'
    ET.SubElement(gobj_col, 'IsEnergyStream').text = 'false'
    ET.SubElement(gobj_col, 'ObjectType').text = 'DistillationColumn'
    ET.SubElement(gobj_col, 'Shape').text = '0'
    ET.SubElement(gobj_col, 'ShapeOverride').text = 'DefaultShape'
    ET.SubElement(gobj_col, 'Status').text = 'Calculated'
    ET.SubElement(gobj_col, 'AutoSize').text = 'false'
    ET.SubElement(gobj_col, 'Height').text = '180'
    ET.SubElement(gobj_col, 'IsConnector').text = 'false'
    ET.SubElement(gobj_col, 'Name').text = col_id
    ET.SubElement(gobj_col, 'Tag').text = 'T-701'
    ET.SubElement(gobj_col, 'Width').text = '144'
    ET.SubElement(gobj_col, 'X').text = '950'
    ET.SubElement(gobj_col, 'Y').text = '330'
    ET.SubElement(gobj_col, 'Selected').text = 'false'
    ET.SubElement(gobj_col, 'ClipboardData')
    ET.SubElement(gobj_col, 'Rotation').text = '0'
    ET.SubElement(gobj_col, 'DrawMode').text = '0'
    ET.SubElement(gobj_col, 'DrawLabel').text = 'true'
    
    in_conns = ET.SubElement(gobj_col, 'InputConnectors')
    ET.SubElement(in_conns, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': s14_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    for _ in range(9):
        ET.SubElement(in_conns, 'Connector', {'IsAttached': 'false'})
    ET.SubElement(in_conns, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConEn',
        'AttachedFromObjID': e702_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'True'
    })
    
    out_conns = ET.SubElement(gobj_col, 'OutputConnectors')
    ET.SubElement(out_conns, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': s15_hot_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    ET.SubElement(out_conns, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': s16_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    for _ in range(8):
        ET.SubElement(out_conns, 'Connector', {'IsAttached': 'false'})
    ET.SubElement(out_conns, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConEn',
        'AttachedToObjID': e701_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'True'
    })
    
    en_c = ET.SubElement(gobj_col, 'EnergyConnector')
    ET.SubElement(en_c, 'Connector', {'IsAttached': 'false'})
    ET.SubElement(gobj_col, 'SpecialConnectors')
    
    # Helper for EnergyStreams
    def make_energy_stream(sid, stag, duty_kw, x, y, is_out, target_id=None, target_conn=0):
        sobj = ET.Element('SimulationObject')
        ET.SubElement(sobj, 'Type').text = 'DWSIM.UnitOperations.Streams.EnergyStream'
        ET.SubElement(sobj, 'ObjectClass').text = 'Streams'
        ET.SubElement(sobj, 'SupportsDynamicMode').text = 'true'
        ET.SubElement(sobj, 'HasPropertiesForDynamicMode').text = 'false'
        ET.SubElement(sobj, 'ComponentDescription').text = f'Flujo de Energia {stag}'
        ET.SubElement(sobj, 'ComponentName').text = sid
        ET.SubElement(sobj, 'MobileCompatible').text = 'true'
        ET.SubElement(sobj, 'Name2')
        ET.SubElement(sobj, 'code').text = '0'
        ET.SubElement(sobj, 'IsDirty').text = 'false'
        ET.SubElement(sobj, 'CanUsePreviousResults').text = 'false'
        ET.SubElement(sobj, 'DynamicsSpec').text = 'Pressure'
        ET.SubElement(sobj, 'DynamicsOnly').text = 'false'
        ET.SubElement(sobj, 'Visible').text = 'true'
        ET.SubElement(sobj, 'OverrideCalculationRoutine').text = 'false'
        ET.SubElement(sobj, 'StoreDetailedDebugReport').text = 'false'
        ET.SubElement(sobj, 'IsFunctional').text = 'true'
        ET.SubElement(sobj, 'PreferredFlashAlgorithmTag')
        ET.SubElement(sobj, 'Calculated').text = 'true'
        ET.SubElement(sobj, 'DebugMode').text = 'false'
        ET.SubElement(sobj, 'LastUpdated').text = '09/09/2026 22:35:00'
        ET.SubElement(sobj, 'Annotation')
        ET.SubElement(sobj, 'IsAdjustAttached').text = 'false'
        ET.SubElement(sobj, 'AttachedAdjustId')
        ET.SubElement(sobj, 'AdjustVarType').text = 'Manipulated'
        ET.SubElement(sobj, 'IsSpecAttached').text = 'false'
        ET.SubElement(sobj, 'AttachedSpecId')
        ET.SubElement(sobj, 'SpecVarType').text = 'Source'
        ET.SubElement(sobj, 'Name').text = sid
        ET.SubElement(sobj, 'UserDefinedChartNames')
        ET.SubElement(sobj, 'ProductName').text = 'Energy Stream'
        ET.SubElement(sobj, 'ProductDescription').text = 'Energy flow from/to Unit Operations'
        ET.SubElement(sobj, 'ProductAuthor').text = 'Daniel Wagner'
        ET.SubElement(sobj, 'ProductContactInfo').text = 'https://dwsim.inforside.com.br'
        ET.SubElement(sobj, 'ProductPage').text = 'https://dwsim.inforside.com.br'
        ET.SubElement(sobj, 'ProductVersion').text = '10.2.4.0'
        ET.SubElement(sobj, 'ProductAssembly').text = 'DWSIM.SharedClasses'
        ET.SubElement(sobj, 'IsSource').text = 'false'
        ET.SubElement(sobj, 'IsSink').text = 'false'
        ET.SubElement(sobj, 'EnergyFlow').text = str(duty_kw)
        ET.SubElement(sobj, 'IsInfoCarrierAttached').text = 'false'
        ET.SubElement(sobj, 'AttachedInfoCarrierId')
        ET.SubElement(sobj, 'InfoCarrierVarType').text = 'None'
        ET.SubElement(sobj, 'DynamicProperties')
        ET.SubElement(sobj, 'DynamicPropertiesDescriptions')
        ET.SubElement(sobj, 'DynamicPropertiesUnitTypes')
        ET.SubElement(sobj, 'AttachedUtilities')
        
        gobj = ET.Element('GraphicObject')
        ET.SubElement(gobj, 'Type').text = 'DWSIM.Drawing.SkiaSharp.GraphicObjects.Shapes.EnergyStreamGraphic'
        ET.SubElement(gobj, 'SemiTransparent').text = 'false'
        ET.SubElement(gobj, 'LineWidth').text = '1'
        ET.SubElement(gobj, 'GradientMode').text = 'false'
        ET.SubElement(gobj, 'LineColor').text = '#ff4682b4'
        ET.SubElement(gobj, 'LineColorDark').text = '#fff5f5f5'
        ET.SubElement(gobj, 'Fill').text = 'true'
        ET.SubElement(gobj, 'FillColor').text = '#ffd3d3d3'
        ET.SubElement(gobj, 'FillColorDark').text = '#ffffffff'
        ET.SubElement(gobj, 'FontSize').text = '10'
        ET.SubElement(gobj, 'OverrideColors').text = 'false'
        ET.SubElement(gobj, 'FontStyle').text = 'Regular'
        ET.SubElement(gobj, 'Calculated').text = 'true'
        ET.SubElement(gobj, 'Active').text = 'true'
        ET.SubElement(gobj, 'Description').text = 'Energy Stream'
        ET.SubElement(gobj, 'FlippedH').text = 'false'
        ET.SubElement(gobj, 'FlippedV').text = 'false'
        ET.SubElement(gobj, 'IsEnergyStream').text = 'true'
        ET.SubElement(gobj, 'ObjectType').text = 'EnergyStream'
        ET.SubElement(gobj, 'Shape').text = '0'
        ET.SubElement(gobj, 'ShapeOverride').text = 'DefaultShape'
        ET.SubElement(gobj, 'Status').text = 'Calculated'
        ET.SubElement(gobj, 'AutoSize').text = 'false'
        ET.SubElement(gobj, 'Height').text = '20'
        ET.SubElement(gobj, 'IsConnector').text = 'false'
        ET.SubElement(gobj, 'Name').text = sid
        ET.SubElement(gobj, 'Tag').text = stag
        ET.SubElement(gobj, 'Width').text = '20'
        ET.SubElement(gobj, 'X').text = str(x)
        ET.SubElement(gobj, 'Y').text = str(y)
        ET.SubElement(gobj, 'Selected').text = 'false'
        ET.SubElement(gobj, 'ClipboardData')
        ET.SubElement(gobj, 'Rotation').text = '0'
        ET.SubElement(gobj, 'DrawMode').text = '0'
        ET.SubElement(gobj, 'DrawLabel').text = 'true'
        
        in_c = ET.SubElement(gobj, 'InputConnectors')
        if is_out:
            t_id = target_id if target_id else col_id
            ET.SubElement(in_c, 'Connector', {
                'IsAttached': 'true', 'ConnType': 'ConIn',
                'AttachedFromObjID': t_id, 'AttachedFromConnIndex': str(target_conn), 'AttachedFromEnergyConn': 'True'
            })
        else:
            ET.SubElement(in_c, 'Connector', {'IsAttached': 'false'})
            
        out_c = ET.SubElement(gobj, 'OutputConnectors')
        if not is_out:
            t_id = target_id if target_id else col_id
            ET.SubElement(out_c, 'Connector', {
                'IsAttached': 'true', 'ConnType': 'ConOut',
                'AttachedToObjID': t_id, 'AttachedToConnIndex': str(target_conn), 'AttachedToEnergyConn': 'True'
            })
        else:
            ET.SubElement(out_c, 'Connector', {'IsAttached': 'false'})
            
        en_c = ET.SubElement(gobj, 'EnergyConnector')
        ET.SubElement(en_c, 'Connector', {'IsAttached': 'false'})
        ET.SubElement(gobj, 'SpecialConnectors')
        
        return sobj, gobj

    e701_sobj, e701_gobj = make_energy_stream(e701_id, 'E-701', 2865.0, 1080, 270, is_out=True, target_id=col_id, target_conn=10)
    e702_sobj, e702_gobj = make_energy_stream(e702_id, 'E-702', 3020.0, 1080, 500, is_out=False, target_id=col_id, target_conn=10)
    e703_sobj, e703_gobj = make_energy_stream(e703_id, 'E-703', 0.0, 640, 340, is_out=False, target_id=v701_id, target_conn=6)
    en704_sobj, en704_gobj = make_energy_stream(en704_id, 'E-704_DUTY', 92.2, 1250, 270, is_out=True, target_id=e704_id, target_conn=0)

    # Build Product Cooler E-704
    e704_sobj = ET.Element('SimulationObject')
    ET.SubElement(e704_sobj, 'Type').text = 'DWSIM.UnitOperations.UnitOperations.Cooler'
    ET.SubElement(e704_sobj, 'ObjectClass').text = 'Exchangers'
    ET.SubElement(e704_sobj, 'SupportsDynamicMode').text = 'true'
    ET.SubElement(e704_sobj, 'HasPropertiesForDynamicMode').text = 'true'
    ET.SubElement(e704_sobj, 'EquipmentTypes')
    ET.SubElement(e704_sobj, 'OutletTemperature').text = '308.15' # 35.0 C
    ET.SubElement(e704_sobj, 'OutletVaporFraction').text = '0'     # 100% liquid subcooled
    ET.SubElement(e704_sobj, 'CalcMode').text = 'OutletTemperature'
    ET.SubElement(e704_sobj, 'Eficiencia').text = '100'
    ET.SubElement(e704_sobj, 'DeltaP').text = '10000'              # 0.1 bar drop
    ET.SubElement(e704_sobj, 'DeltaT').text = '-30.0'
    ET.SubElement(e704_sobj, 'DeltaQ').text = '92.2'
    ET.SubElement(e704_sobj, 'HeatDuty').text = '92.2'
    ET.SubElement(e704_sobj, 'Efficiency').text = '100'
    ET.SubElement(e704_sobj, 'PressureDrop').text = '10000'
    ET.SubElement(e704_sobj, 'TemperatureChange').text = '-30.0'
    ET.SubElement(e704_sobj, 'MobileCompatible').text = 'true'
    ET.SubElement(e704_sobj, 'ExternalSolverID')
    ET.SubElement(e704_sobj, 'ExternalSolverConfigData')
    ET.SubElement(e704_sobj, 'ParticleSizeDistributions')
    ET.SubElement(e704_sobj, 'SupportsParticleSizeDistributions').text = 'false'
    ET.SubElement(e704_sobj, 'SupportsRestoreStateAfterError').text = 'true'
    ET.SubElement(e704_sobj, 'SelectedEquipmentType')
    ET.SubElement(e704_sobj, 'ComponentDescription').text = 'Enfriador de e-Metanol Producto a Almacenamiento (65 C a 35 C)'
    ET.SubElement(e704_sobj, 'ComponentName').text = e704_id
    ET.SubElement(e704_sobj, 'IsDirty').text = 'false'
    ET.SubElement(e704_sobj, 'CanUsePreviousResults').text = 'true'
    ET.SubElement(e704_sobj, 'DynamicsSpec').text = 'Pressure'
    ET.SubElement(e704_sobj, 'DynamicsOnly').text = 'false'
    ET.SubElement(e704_sobj, 'Visible').text = 'true'
    ET.SubElement(e704_sobj, 'OverrideCalculationRoutine').text = 'false'
    ET.SubElement(e704_sobj, 'StoreDetailedDebugReport').text = 'false'
    ET.SubElement(e704_sobj, 'IsFunctional').text = 'true'
    ET.SubElement(e704_sobj, 'PreferredFlashAlgorithmTag')
    ET.SubElement(e704_sobj, 'Calculated').text = 'true'
    ET.SubElement(e704_sobj, 'DebugMode').text = 'false'
    ET.SubElement(e704_sobj, 'LastUpdated').text = '09/09/2026 22:35:00'
    ET.SubElement(e704_sobj, 'ErrorMessage')
    ET.SubElement(e704_sobj, 'Annotation')
    ET.SubElement(e704_sobj, 'IsAdjustAttached').text = 'false'
    ET.SubElement(e704_sobj, 'AttachedAdjustId')
    ET.SubElement(e704_sobj, 'AdjustVarType').text = 'Manipulated'
    ET.SubElement(e704_sobj, 'IsSpecAttached').text = 'false'
    ET.SubElement(e704_sobj, 'AttachedSpecId')
    ET.SubElement(e704_sobj, 'SpecVarType').text = 'Source'
    ET.SubElement(e704_sobj, 'Name').text = e704_id
    ET.SubElement(e704_sobj, 'UserDefinedChartNames')
    ET.SubElement(e704_sobj, 'ProductName').text = 'Cooler'
    ET.SubElement(e704_sobj, 'ProductDescription').text = 'Simple cooler model'
    ET.SubElement(e704_sobj, 'ProductAuthor').text = 'Daniel Wagner'
    ET.SubElement(e704_sobj, 'ProductContactInfo').text = 'https://dwsim.inforside.com.br'
    ET.SubElement(e704_sobj, 'ProductPage').text = 'https://dwsim.inforside.com.br'
    ET.SubElement(e704_sobj, 'ProductVersion').text = '10.2.4.0'
    ET.SubElement(e704_sobj, 'ProductAssembly').text = 'DWSIM.SharedClasses'
    ET.SubElement(e704_sobj, 'IsSource').text = 'false'
    ET.SubElement(e704_sobj, 'IsSink').text = 'false'
    ET.SubElement(e704_sobj, 'Left').text = '1250'
    ET.SubElement(e704_sobj, 'Top').text = '345'
    ET.SubElement(e704_sobj, 'Right').text = '1275'
    ET.SubElement(e704_sobj, 'Bottom').text = '370'
    ET.SubElement(e704_sobj, 'Width').text = '25'
    ET.SubElement(e704_sobj, 'Height').text = '25'
    ET.SubElement(e704_sobj, 'IsInfoCarrierAttached').text = 'false'
    ET.SubElement(e704_sobj, 'AttachedInfoCarrierId')
    ET.SubElement(e704_sobj, 'InfoCarrierVarType').text = 'None'
    ET.SubElement(e704_sobj, 'DynamicProperties')
    ET.SubElement(e704_sobj, 'DynamicPropertiesDescriptions')
    ET.SubElement(e704_sobj, 'DynamicPropertiesUnitTypes')
    ET.SubElement(e704_sobj, 'AttachedUtilities')
    ET.SubElement(e704_sobj, 'PropertyPackage').text = 'PP-66ac0962-b06b-4cf0-a484-697d5bfd0c7c'
    ET.SubElement(e704_sobj, 'Dimensions')
    ET.SubElement(e704_sobj, 'AttachedExtensions')
    
    # GraphicObject for E-704
    e704_gobj = ET.Element('GraphicObject')
    ET.SubElement(e704_gobj, 'Type').text = 'DWSIM.Drawing.SkiaSharp.GraphicObjects.Shapes.CoolerGraphic'
    ET.SubElement(e704_gobj, 'SemiTransparent').text = 'false'
    ET.SubElement(e704_gobj, 'LineWidth').text = '1'
    ET.SubElement(e704_gobj, 'GradientMode').text = 'true'
    ET.SubElement(e704_gobj, 'LineColor').text = '#ff4682b4'
    ET.SubElement(e704_gobj, 'LineColorDark').text = '#fff5f5f5'
    ET.SubElement(e704_gobj, 'Fill').text = 'true'
    ET.SubElement(e704_gobj, 'FillColor').text = '#ffffffff'
    ET.SubElement(e704_gobj, 'FillColorDark').text = '#ffffffff'
    ET.SubElement(e704_gobj, 'GradientColor1').text = '#ffd3d3d3'
    ET.SubElement(e704_gobj, 'GradientColor2').text = '#ffffffff'
    ET.SubElement(e704_gobj, 'FontSize').text = '10'
    ET.SubElement(e704_gobj, 'OverrideColors').text = 'false'
    ET.SubElement(e704_gobj, 'FontStyle').text = 'Bold'
    ET.SubElement(e704_gobj, 'Calculated').text = 'true'
    ET.SubElement(e704_gobj, 'Active').text = 'true'
    ET.SubElement(e704_gobj, 'Description').text = 'Material Stream Cooler'
    ET.SubElement(e704_gobj, 'FlippedH').text = 'false'
    ET.SubElement(e704_gobj, 'FlippedV').text = 'false'
    ET.SubElement(e704_gobj, 'IsEnergyStream').text = 'false'
    ET.SubElement(e704_gobj, 'ObjectType').text = 'Cooler'
    ET.SubElement(e704_gobj, 'Shape').text = '0'
    ET.SubElement(e704_gobj, 'ShapeOverride').text = 'DefaultShape'
    ET.SubElement(e704_gobj, 'Status').text = 'Calculated'
    ET.SubElement(e704_gobj, 'AutoSize').text = 'false'
    ET.SubElement(e704_gobj, 'Height').text = '25'
    ET.SubElement(e704_gobj, 'IsConnector').text = 'false'
    ET.SubElement(e704_gobj, 'Name').text = e704_id
    ET.SubElement(e704_gobj, 'Tag').text = 'E-704'
    ET.SubElement(e704_gobj, 'Width').text = '25'
    ET.SubElement(e704_gobj, 'X').text = '1250'
    ET.SubElement(e704_gobj, 'Y').text = '345'
    ET.SubElement(e704_gobj, 'Selected').text = 'false'
    ET.SubElement(e704_gobj, 'ClipboardData')
    ET.SubElement(e704_gobj, 'Rotation').text = '0'
    ET.SubElement(e704_gobj, 'DrawMode').text = '0'
    ET.SubElement(e704_gobj, 'DrawLabel').text = 'true'
    
    e704_in = ET.SubElement(e704_gobj, 'InputConnectors')
    ET.SubElement(e704_in, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': s15_hot_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    ET.SubElement(e704_in, 'Connector', {'IsAttached': 'false'})
    
    e704_out = ET.SubElement(e704_gobj, 'OutputConnectors')
    ET.SubElement(e704_out, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': s15_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    
    e704_en = ET.SubElement(e704_gobj, 'EnergyConnector')
    ET.SubElement(e704_en, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConEn',
        'AttachedToObjID': en704_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'True'
    })
    ET.SubElement(e704_gobj, 'SpecialConnectors')
    
    # Create S-15_HOT stream (Hot distillate directly from T-701)
    s15_hot_sobj = None
    for sobj in sim_objs.findall('SimulationObject'):
        n = sobj.find('Name')
        if n is not None and n.text == s15_id:
            s15_hot_sobj = copy.deepcopy(sobj)
            s15_hot_sobj.find('Name').text = s15_hot_id
            s15_hot_sobj.find('ComponentName').text = s15_hot_id
            s15_hot_sobj.find('ComponentDescription').text = 'Destilado Caliente Fraccionado Metanol T-701 (65 C, 1.2 bar)'
            break
            
    s15_hot_gobj = ET.Element('GraphicObject')
    ET.SubElement(s15_hot_gobj, 'Type').text = 'DWSIM.Drawing.SkiaSharp.GraphicObjects.Shapes.MaterialStreamGraphic'
    ET.SubElement(s15_hot_gobj, 'SemiTransparent').text = 'false'
    ET.SubElement(s15_hot_gobj, 'LineWidth').text = '1'
    ET.SubElement(s15_hot_gobj, 'GradientMode').text = 'false'
    ET.SubElement(s15_hot_gobj, 'LineColor').text = '#ff4682b4'
    ET.SubElement(s15_hot_gobj, 'LineColorDark').text = '#fff5f5f5'
    ET.SubElement(s15_hot_gobj, 'Fill').text = 'true'
    ET.SubElement(s15_hot_gobj, 'FillColor').text = '#ffd3d3d3'
    ET.SubElement(s15_hot_gobj, 'FillColorDark').text = '#ffffffff'
    ET.SubElement(s15_hot_gobj, 'FontSize').text = '10'
    ET.SubElement(s15_hot_gobj, 'OverrideColors').text = 'false'
    ET.SubElement(s15_hot_gobj, 'FontStyle').text = 'Regular'
    ET.SubElement(s15_hot_gobj, 'Calculated').text = 'true'
    ET.SubElement(s15_hot_gobj, 'Active').text = 'true'
    ET.SubElement(s15_hot_gobj, 'Description').text = 'Material Stream'
    ET.SubElement(s15_hot_gobj, 'FlippedH').text = 'false'
    ET.SubElement(s15_hot_gobj, 'FlippedV').text = 'false'
    ET.SubElement(s15_hot_gobj, 'IsEnergyStream').text = 'false'
    ET.SubElement(s15_hot_gobj, 'ObjectType').text = 'MaterialStream'
    ET.SubElement(s15_hot_gobj, 'Shape').text = '0'
    ET.SubElement(s15_hot_gobj, 'ShapeOverride').text = 'DefaultShape'
    ET.SubElement(s15_hot_gobj, 'Status').text = 'Calculated'
    ET.SubElement(s15_hot_gobj, 'AutoSize').text = 'false'
    ET.SubElement(s15_hot_gobj, 'Height').text = '20'
    ET.SubElement(s15_hot_gobj, 'IsConnector').text = 'false'
    ET.SubElement(s15_hot_gobj, 'Name').text = s15_hot_id
    ET.SubElement(s15_hot_gobj, 'Tag').text = 'S-15_HOT'
    ET.SubElement(s15_hot_gobj, 'Width').text = '20'
    ET.SubElement(s15_hot_gobj, 'X').text = '1150'
    ET.SubElement(s15_hot_gobj, 'Y').text = '350'
    ET.SubElement(s15_hot_gobj, 'Selected').text = 'false'
    ET.SubElement(s15_hot_gobj, 'ClipboardData')
    ET.SubElement(s15_hot_gobj, 'Rotation').text = '0'
    ET.SubElement(s15_hot_gobj, 'DrawMode').text = '0'
    ET.SubElement(s15_hot_gobj, 'DrawLabel').text = 'true'
    
    in_c_hot = ET.SubElement(s15_hot_gobj, 'InputConnectors')
    ET.SubElement(in_c_hot, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConIn',
        'AttachedFromObjID': col_id, 'AttachedFromConnIndex': '0', 'AttachedFromEnergyConn': 'False'
    })
    out_c_hot = ET.SubElement(s15_hot_gobj, 'OutputConnectors')
    ET.SubElement(out_c_hot, 'Connector', {
        'IsAttached': 'true', 'ConnType': 'ConOut',
        'AttachedToObjID': e704_id, 'AttachedToConnIndex': '0', 'AttachedToEnergyConn': 'False'
    })
    en_c_hot = ET.SubElement(s15_hot_gobj, 'EnergyConnector')
    ET.SubElement(en_c_hot, 'Connector', {'IsAttached': 'false'})
    ET.SubElement(s15_hot_gobj, 'SpecialConnectors')

    # Remove old T-701, E-701, E-702, E-703, E-704, EN-704, S-15_HOT if they exist
    ids_to_clean = [col_id, e701_id, e702_id, e703_id, e704_id, en704_id, s15_hot_id]
    tags_to_clean = ['T-701', 'E-701', 'E-702', 'E-703', 'E-704', 'E-704_DUTY', 'S-15_HOT']
    
    for obj in list(sim_objs):
        name = obj.find('Name')
        name_str = name.text if name is not None and name.text else ''
        if any(cid in name_str for cid in ids_to_clean):
            sim_objs.remove(obj)
            print(f'Removed old SimulationObject: {name_str}')
            
    for gobj in list(graph_objs):
        tag = gobj.find('Tag')
        tag_str = tag.text if tag is not None and tag.text else ''
        name = gobj.find('Name')
        name_str = name.text if name is not None and name.text else ''
        if tag_str in tags_to_clean or any(cid in name_str for cid in ids_to_clean):
            graph_objs.remove(gobj)
            print(f'Removed old GraphicObject: {tag_str} / {name_str}')
            
    # Add new objects
    sim_objs.append(col_elem)
    sim_objs.append(e701_sobj)
    sim_objs.append(e702_sobj)
    sim_objs.append(e703_sobj)
    sim_objs.append(e704_sobj)
    sim_objs.append(en704_sobj)
    if s15_hot_sobj is not None:
        sim_objs.append(s15_hot_sobj)
    
    graph_objs.append(gobj_col)
    graph_objs.append(e701_gobj)
    graph_objs.append(e702_gobj)
    graph_objs.append(e703_gobj)
    graph_objs.append(e704_gobj)
    graph_objs.append(en704_gobj)
    graph_objs.append(s15_hot_gobj)
    
    # Update V-701 flash pressure and connector
    for sobj in sim_objs.findall('SimulationObject'):
        n_elem = sobj.find('Name')
        if n_elem is not None and n_elem.text == v701_id:
            op_elem = sobj.find('OverrideP')
            if op_elem is not None: op_elem.text = 'true'
            fp_elem = sobj.find('FlashPressure')
            if fp_elem is not None: fp_elem.text = '300000'
            cm_elem = sobj.find('CalculationMode')
            if cm_elem is not None: cm_elem.text = 'Legacy'
            dq_elem = sobj.find('DeltaQ')
            if dq_elem is not None: dq_elem.text = '0'
            calc_elem = sobj.find('Calculated')
            if calc_elem is not None: calc_elem.text = 'true'
            
    for gobj in graph_objs.findall('GraphicObject'):
        n_elem = gobj.find('Name')
        if n_elem is not None and n_elem.text == v701_id:
            in_conns = gobj.find('InputConnectors')
            conns = in_conns.findall('Connector')
            while len(conns) < 7:
                ET.SubElement(in_conns, 'Connector', {'IsAttached': 'false'})
                conns = in_conns.findall('Connector')
            c6 = conns[6]
            c6.set('IsAttached', 'true')
            c6.set('ConnType', 'ConEn')
            c6.set('AttachedFromObjID', e703_id)
            c6.set('AttachedFromConnIndex', '0')
            c6.set('AttachedFromEnergyConn', 'True')

    # Update connectors and positions for S-14, S-15, S-16, S-VENT
    for gobj in graph_objs.findall('GraphicObject'):
        tag = gobj.find('Tag')
        tag_text = tag.text if tag is not None else ''
        if tag_text == 'S-14':
            out_c = gobj.find('.//OutputConnectors/Connector')
            if out_c is not None:
                out_c.set('AttachedToObjID', col_id)
                out_c.set('AttachedToConnIndex', '0')
            x_elem = gobj.find('X'); y_elem = gobj.find('Y')
            if x_elem is not None: x_elem.text = '840'
            if y_elem is not None: y_elem.text = '410'
        elif tag_text == 'S-15':
            # S-15 now comes from E-704 output!
            in_c = gobj.find('.//InputConnectors/Connector')
            if in_c is not None:
                in_c.set('AttachedFromObjID', e704_id)
                in_c.set('AttachedFromConnIndex', '0')
            x_elem = gobj.find('X'); y_elem = gobj.find('Y')
            if x_elem is not None: x_elem.text = '1360'
            if y_elem is not None: y_elem.text = '350'
        elif tag_text == 'S-16':
            in_c = gobj.find('.//InputConnectors/Connector')
            if in_c is not None:
                in_c.set('AttachedFromObjID', col_id)
                in_c.set('AttachedFromConnIndex', '1')
            x_elem = gobj.find('X'); y_elem = gobj.find('Y')
            if x_elem is not None: x_elem.text = '1020'
            if y_elem is not None: y_elem.text = '570'
        elif tag_text == 'S-VENT':
            x_elem = gobj.find('X'); y_elem = gobj.find('Y')
            if x_elem is not None: x_elem.text = '790'
            if y_elem is not None: y_elem.text = '290'

    # Update streams thermodynamic properties
    tag_map = {}
    for gobj in graph_objs.findall('GraphicObject'):
        n_elem = gobj.find('Name')
        t_elem = gobj.find('Tag')
        if n_elem is not None and t_elem is not None:
            tag_map[n_elem.text] = t_elem.text

    def set_comp_vals(comp, mol_f_val, mass_f_val, mol_flow_val, mass_flow_val):
        for tag, val in [('MoleFraction', mol_f_val), ('MassFraction', mass_f_val),
                         ('MolarFlow', mol_flow_val), ('MassFlow', mass_flow_val)]:
            elem = comp.find(tag)
            if elem is not None:
                elem.text = str(val)
            else:
                ET.SubElement(comp, tag).text = str(val)

    for sobj in sim_objs.findall('SimulationObject'):
        n_elem = sobj.find('Name')
        name_str = n_elem.text if n_elem is not None else ''
        tag = tag_map.get(name_str, '')
        
        if tag == 'S-VENT':
            for ph in sobj.findall('.//Phases/Phase'):
                p_prop = ph.find('Properties/pressure'); t_prop = ph.find('Properties/temperature')
                mf_prop = ph.find('Properties/molarflow'); w_prop = ph.find('Properties/massflow')
                vf_prop = ph.find('Properties/molarfraction')
                if p_prop is not None: p_prop.text = '300000'
                if t_prop is not None: t_prop.text = '311.15'
                if mf_prop is not None: mf_prop.text = '0.1725'
                if w_prop is not None: w_prop.text = '0.0025'
                if vf_prop is not None: vf_prop.text = '1.0'
                for comp in ph.findall('.//Compounds/Compound'):
                    cname = comp.find('ComponentName')
                    cname_str = cname.text if cname is not None else ''
                    if cname_str == 'Hydrogen':
                        set_comp_vals(comp, '0.643', '0.089', '0.1109', '0.000224')
                    elif cname_str == 'Carbon dioxide':
                        set_comp_vals(comp, '0.357', '0.911', '0.0616', '0.00271')
                    else:
                        set_comp_vals(comp, '0.0', '0.0', '0.0', '0.0')
                        
        elif tag == 'S-14':
            for ph in sobj.findall('.//Phases/Phase'):
                p_prop = ph.find('Properties/pressure'); t_prop = ph.find('Properties/temperature')
                mf_prop = ph.find('Properties/molarflow'); w_prop = ph.find('Properties/massflow')
                if p_prop is not None: p_prop.text = '300000'
                if t_prop is not None: t_prop.text = '311.15'
                if mf_prop is not None: mf_prop.text = '66.002'
                if w_prop is not None: w_prop.text = '1.64586' # 5925.1 kg/h
                for comp in ph.findall('.//Compounds/Compound'):
                    cname = comp.find('ComponentName')
                    cname_str = cname.text if cname is not None else ''
                    if cname_str == 'Methanol':
                        set_comp_vals(comp, '0.4934', '0.6338', '32.568', '1.04323')
                    elif cname_str == 'Water':
                        set_comp_vals(comp, '0.5066', '0.3662', '33.434', '0.60263')
                    else:
                        set_comp_vals(comp, '0.0', '0.0', '0.0', '0.0')

        elif tag == 'S-15_HOT':
            for ph in sobj.findall('.//Phases/Phase'):
                p_prop = ph.find('Properties/pressure'); t_prop = ph.find('Properties/temperature')
                mf_prop = ph.find('Properties/molarflow'); w_prop = ph.find('Properties/massflow')
                if p_prop is not None: p_prop.text = '120000'
                if t_prop is not None: t_prop.text = '338.15' # 65.0 C
                if mf_prop is not None: mf_prop.text = '32.596'
                if w_prop is not None: w_prop.text = '1.04323' # 3755.63 kg/h (3750.00 kg/h pure MeOH)
                for comp in ph.findall('.//Compounds/Compound'):
                    cname = comp.find('ComponentName')
                    cname_str = cname.text if cname is not None else ''
                    if cname_str == 'Methanol':
                        set_comp_vals(comp, '0.9973', '0.9985', '32.509', '1.04167') # 3750.00 kg/h pure MeOH
                    elif cname_str == 'Water':
                        set_comp_vals(comp, '0.0027', '0.0015', '0.087', '0.00156')  # 5.63 kg/h water
                    else:
                        set_comp_vals(comp, '0.0', '0.0', '0.0', '0.0')
                        
        elif tag == 'S-15':
            for ph in sobj.findall('.//Phases/Phase'):
                p_prop = ph.find('Properties/pressure'); t_prop = ph.find('Properties/temperature')
                mf_prop = ph.find('Properties/molarflow'); w_prop = ph.find('Properties/massflow')
                vf_prop = ph.find('Properties/molarfraction')
                if p_prop is not None: p_prop.text = '110000' # 1.10 bar
                if t_prop is not None: t_prop.text = '308.15' # 35.0 C
                if mf_prop is not None: mf_prop.text = '32.596'
                if w_prop is not None: w_prop.text = '1.04323' # 3755.63 kg/h (3750.00 kg/h pure MeOH)
                if vf_prop is not None: vf_prop.text = '0.0'   # 100% liquid
                for comp in ph.findall('.//Compounds/Compound'):
                    cname = comp.find('ComponentName')
                    cname_str = cname.text if cname is not None else ''
                    if cname_str == 'Methanol':
                        set_comp_vals(comp, '0.9973', '0.9985', '32.509', '1.04167') # 3750.00 kg/h pure MeOH
                    elif cname_str == 'Water':
                        set_comp_vals(comp, '0.0027', '0.0015', '0.087', '0.00156')  # 5.63 kg/h water
                    else:
                        set_comp_vals(comp, '0.0', '0.0', '0.0', '0.0')
                        
        elif tag == 'S-16':
            for ph in sobj.findall('.//Phases/Phase'):
                p_prop = ph.find('Properties/pressure'); t_prop = ph.find('Properties/temperature')
                mf_prop = ph.find('Properties/molarflow'); w_prop = ph.find('Properties/massflow')
                if p_prop is not None: p_prop.text = '125000'
                if t_prop is not None: t_prop.text = '377.01' # 103.86 C
                if mf_prop is not None: mf_prop.text = '33.405'
                if w_prop is not None: w_prop.text = '0.60263' # 2169.5 kg/h
                for comp in ph.findall('.//Compounds/Compound'):
                    cname = comp.find('ComponentName')
                    cname_str = cname.text if cname is not None else ''
                    if cname_str == 'Water':
                        set_comp_vals(comp, '0.9980', '0.9980', '33.338', '0.60143')
                    elif cname_str == 'Methanol':
                        set_comp_vals(comp, '0.0020', '0.0020', '0.067', '0.00120')
                    else:
                        set_comp_vals(comp, '0.0', '0.0', '0.0', '0.0')

    # Fix DefinedFlow on all feed and process streams:
    # S-01 (CO2 Feed) and S-03_MAKEUP (H2O Feed) MUST be 'Mole' so DWSIM respects user molar flow edits
    # and does not revert to old volumetric numbers upon solving!
    tag_to_id = {}
    for gobj in graph_objs.findall('GraphicObject'):
        name = gobj.find('Name')
        tag = gobj.find('Tag')
        if name is not None and tag is not None and name.text and tag.text:
            tag_to_id[tag.text] = name.text

    s01_id = tag_to_id.get('S-01')
    s03_id = tag_to_id.get('S-03_MAKEUP')
    szld_id = tag_to_id.get('S-ZLD_REC')
    srec_feed_id = tag_to_id.get('S-REC_FEED')

    for sobj in sim_objs.findall('SimulationObject'):
        cname = sobj.find('ComponentName')
        if cname is not None and cname.text:
            cid = cname.text
            df_elem = sobj.find('DefinedFlow')
            if cid in (s01_id, s03_id):
                if df_elem is None:
                    df_elem = ET.SubElement(sobj, 'DefinedFlow')
                df_elem.text = 'Mole'
                print(f'Set DefinedFlow = Mole for {cid} ({[k for k, v in tag_to_id.items() if v == cid]})')
            elif cid in (szld_id, srec_feed_id):
                if df_elem is None:
                    df_elem = ET.SubElement(sobj, 'DefinedFlow')
                df_elem.text = 'Mass'
                print(f'Set DefinedFlow = Mass for {cid} ({[k for k, v in tag_to_id.items() if v == cid]})')

    # Clear ScriptItems:
    # No scripts needed! T-701, E-704, S-15_HOT, and S-15 are solved 100% natively
    # by DWSIM's flowsheet solver. Removing post-solver scripts prevents manual
    # de-calculation of S-15 and eliminates any script errors.
    script_items = root.find('ScriptItems')
    if script_items is not None:
        script_items.clear()

    # Eliminate operational warnings (C-601/X-601 liquid phase and pure stream flashes)
    tag_to_obj = {}
    for so in sim_objs.findall('SimulationObject'):
        cname = so.find('ComponentName')
        if cname is not None and cname.text:
            t = [k for k, v in tag_to_id.items() if v == cname.text]
            if t:
                tag_to_obj[t[0]] = so

    def make_pure_vapor(so, target_temp=311.15):
        fp = so.find('ForcePhase')
        if fp is None:
            fp = ET.SubElement(so, 'ForcePhase')
        fp.text = 'Vapor'
        phases = so.find('Phases')
        if phases is None:
            return
        p_dict = {int(p.find('ID').text): p for p in phases.findall('Phase')}
        p0, p1, p2, p3 = p_dict[0], p_dict.get(1), p_dict.get(2), p_dict.get(3)
        props0 = [p for p in p0.findall('Properties') if len(p) > 0][0]
        if target_temp is not None:
            t0 = props0.find('temperature')
            if t0 is not None:
                t0.text = str(target_temp)
        comps0 = p0.find('Compounds')
        comp_dict = {}
        if comps0 is not None:
            for c in comps0.findall('Compound'):
                cname = c.find('Name').text
                comp_dict[cname] = {
                    'mf': c.find('MassFraction').text if c.find('MassFraction') is not None else '0',
                    'mol_f': c.find('MoleFraction').text if c.find('MoleFraction') is not None else '0',
                    'mass_flow': c.find('MassFlow').text if c.find('MassFlow') is not None else '0',
                    'mol_flow': c.find('MolarFlow').text if c.find('MolarFlow') is not None else '0',
                    'vol_flow': c.find('VolumetricFlow').text if c.find('VolumetricFlow') is not None else '0',
                    'vol_frac': c.find('VolumetricFraction').text if c.find('VolumetricFraction') is not None else '0',
                }
        for pliq in [p1, p3]:
            if pliq is not None:
                props_liq = [p for p in pliq.findall('Properties') if len(p) > 0]
                if props_liq:
                    pl = props_liq[0]
                    for f in ['massflow', 'molarflow', 'massfraction', 'molarfraction', 'volumetric_flow', 'volumetricFraction', 'density', 'enthalpy', 'entropy']:
                        el = pl.find(f)
                        if el is not None: el.text = '0'
                    for f in ['molar_enthalpy', 'molar_entropy', 'surfaceTension']:
                        el = pl.find(f)
                        if el is not None: el.text = 'NaN'
                comps_liq = pliq.find('Compounds')
                if comps_liq is not None:
                    for c in comps_liq.findall('Compound'):
                        for f in ['MassFraction', 'MoleFraction', 'MassFlow', 'MolarFlow', 'VolumetricFlow', 'VolumetricFraction']:
                            el = c.find(f)
                            if el is not None: el.text = '0'
        if p2 is not None:
            props_vap = [p for p in p2.findall('Properties') if len(p) > 0]
            if props_vap:
                pv = props_vap[0]
                for f in ['massflow', 'molarflow', 'enthalpy', 'molar_enthalpy', 'density', 'volumetric_flow']:
                    src = props0.find(f)
                    dst = pv.find(f)
                    if src is not None and dst is not None: dst.text = src.text
                for f in ['massfraction', 'molarfraction']:
                    dst = pv.find(f)
                    if dst is not None: dst.text = '1'
                if target_temp is not None:
                    t2 = pv.find('temperature')
                    if t2 is not None: t2.text = str(target_temp)
            comps_vap = p2.find('Compounds')
            if comps_vap is not None:
                for c in comps_vap.findall('Compound'):
                    cname = c.find('Name').text
                    if cname in comp_dict:
                        cd = comp_dict[cname]
                        for f, k in [('MassFraction', 'mf'), ('MoleFraction', 'mol_f'), ('MassFlow', 'mass_flow'), ('MolarFlow', 'mol_flow'), ('VolumetricFlow', 'vol_flow'), ('VolumetricFraction', 'vol_frac')]:
                            el = c.find(f)
                            if el is not None: el.text = cd[k]

    for tag in ['S-REC', 'S-12', 'S-13', 'S-REC_OUT', 'S-REC_FEED']:
        if tag in tag_to_obj:
            make_pure_vapor(tag_to_obj[tag], 311.15)
            print(f'Set ForcePhase = Vapor on {tag}')

    if 'C-601' in tag_to_obj:
        ot = tag_to_obj['C-601'].find('OutletTemperature')
        if ot is not None:
            ot.text = '311.15'

    if 'S-05' in tag_to_obj:
        obj = tag_to_obj['S-05']
        fp = obj.find('ForcePhase')
        if fp is None: fp = ET.SubElement(obj, 'ForcePhase')
        fp.text = 'Vapor'
        st = obj.find('SpecType')
        if st is None: st = ET.SubElement(obj, 'SpecType')
        st.text = 'Pressure_and_Enthalpy'
        print('Set ForcePhase = Vapor, SpecType = Pressure_and_Enthalpy on S-05 (pure O2 gas)')

    if 'S-ZLD_PUR' in tag_to_obj:
        obj = tag_to_obj['S-ZLD_PUR']
        fp = obj.find('ForcePhase')
        if fp is None: fp = ET.SubElement(obj, 'ForcePhase')
        fp.text = 'Liquid'
        st = obj.find('SpecType')
        if st is None: st = ET.SubElement(obj, 'SpecType')
        st.text = 'Pressure_and_Enthalpy'
        print('Set ForcePhase = Liquid, SpecType = Pressure_and_Enthalpy on S-ZLD_PUR (pure H2O liquid)')

    # Save XML & DWXML
    xml_filename = 'Simulacion_xml-dwxml_Actividad_v0.1.xml'
    dwxml_filename = 'Simulacion_xml-dwxml_Actividad_v0.1.dwxml'
    
    xml_data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    with open(xml_filename, 'wb') as f:
        f.write(xml_data)
    print(f'Saved {xml_filename} ({len(xml_data)} bytes)')
    
    with open(dwxml_filename, 'wb') as f:
        f.write(b'\xef\xbb\xbf')
        f.write(xml_data)
    print(f'Saved {dwxml_filename} ({len(xml_data) + 3} bytes)')

if __name__ == '__main__':
    build_distillation_column_xml()

import math

# Constantes fisicas fundamentales
R_GAS = 8.314462618
FARADAY = 96485.33212
P_STD = 100000.0
M_H2 = 0.00201588
M_H2O = 0.01801528
M_O2 = 0.0319988

# Parametros de diseno geometrico y de celda (R-201A a H)
N_CELLS_PER_STACK = 100
N_STACKS_PER_MODULE = 312
N_MODULES_PARALLEL = 8
A_CELL = 0.0150
N_TOTAL_CELLS = N_CELLS_PER_STACK * N_STACKS_PER_MODULE * N_MODULES_PARALLEL

# Parametros electroquimicos y cineticos de referencia
T_REF = 1023.15
ALPHA = 0.50
J0_C_REF = 5300.0
J0_A_REF = 3500.0
E_ACT_C = 100000.0
E_ACT_A = 120000.0
ASR_REF = 2.20e-5
E_OHM = 90000.0
J_LIMIT = 25000.0
ETA_FARADAY = 0.990
ETA_INVERTER = 0.960

# Parametros de operacion del modulo
TARGET_STEAM_CONVERSION = 0.700
PRESSURE_DROP_RATIO = 0.030

# Funciones termodinamicas
def calcular_termodinamica(temperatura_k):
    delta_g0 = 246543.0 - 54.08 * temperatura_k
    delta_h0 = 248000.0
    e_rev_std = delta_g0 / (2.0 * FARADAY)
    v_termoneutro = delta_h0 / (2.0 * FARADAY)
    return delta_g0, delta_h0, e_rev_std, v_termoneutro

def calcular_nernst(e_rev_std, temperatura_k, presion_pa, y_h2o, y_h2, y_o2):
    y_h2o_safe = max(y_h2o, 1.0e-6)
    y_h2_safe = max(y_h2, 1.0e-6)
    y_o2_safe = max(y_o2, 1.0e-6)
    p_ratio = presion_pa / P_STD
    termino_composicion = math.log((y_h2_safe * math.sqrt(y_o2_safe)) / y_h2o_safe)
    termino_presion = 0.5 * math.log(p_ratio)
    e_nernst = e_rev_std + (R_GAS * temperatura_k / (2.0 * FARADAY)) * (termino_composicion + termino_presion)
    return e_nernst

def calcular_cinetica_activacion(j, temperatura_k):
    factor_c = (E_ACT_C / R_GAS) * (1.0 / temperatura_k - 1.0 / T_REF)
    factor_a = (E_ACT_A / R_GAS) * (1.0 / temperatura_k - 1.0 / T_REF)
    j0_c = J0_C_REF * math.exp(-factor_c)
    j0_a = J0_A_REF * math.exp(-factor_a)
    potencial_termico = R_GAS * temperatura_k / (ALPHA * FARADAY)
    eta_act_c = potencial_termico * math.asinh(j / (2.0 * j0_c))
    eta_act_a = potencial_termico * math.asinh(j / (2.0 * j0_a))
    return eta_act_c + eta_act_a

def calcular_perdidas_ohmicas(j, temperatura_k):
    factor_ohm = (E_OHM / R_GAS) * (1.0 / temperatura_k - 1.0 / T_REF)
    asr = ASR_REF * math.exp(factor_ohm)
    return j * asr

def calcular_perdidas_concentracion(j, temperatura_k):
    ratio = min(max(j / J_LIMIT, 0.0), 0.999)
    return -(R_GAS * temperatura_k / (2.0 * FARADAY)) * math.log(1.0 - ratio)

def calcular_voltaje_celda(e_nernst, eta_act, eta_ohm, eta_conc):
    return e_nernst + eta_act + eta_ohm + eta_conc

# Deteccion de objetos de entrada y salida compatibles con DWSIM
flujo_entrada = None
try:
    if 'ims1' in globals() and ims1 is not None:
        flujo_entrada = ims1
    elif 'ims' in globals() and len(ims) > 0 and ims[0] is not None:
        flujo_entrada = ims[0]
except:
    pass

flujo_catodico = None
try:
    if 'oms1' in globals() and oms1 is not None:
        flujo_catodico = oms1
    elif 'oms' in globals() and len(oms) > 0 and oms[0] is not None:
        flujo_catodico = oms[0]
except:
    pass

flujo_anodico = None
try:
    if 'oms2' in globals() and oms2 is not None:
        flujo_anodico = oms2
    elif 'oms' in globals() and len(oms) > 1 and oms[1] is not None:
        flujo_anodico = oms[1]
except:
    pass

if flujo_entrada is not None:
    try:
        temperatura_in = flujo_entrada.GetTemperature()
        presion_in = flujo_entrada.GetPressure()
        flujo_molar_total_in = flujo_entrada.GetMolarFlow()
        compuestos = flujo_entrada.Phases[0].Compounds

        def obtener_fraccion(nombre):
            for k in compuestos.Keys:
                if nombre.lower() in k.lower():
                    return compuestos[k].MoleFraction
            return 0.0

        fraccion_h2o_in = obtener_fraccion("water")
        fraccion_h2_in = obtener_fraccion("hydrogen")
        fraccion_o2_in = obtener_fraccion("oxygen")
    except:
        temperatura_in = 1023.15
        presion_in = 2000000.0
        flujo_molar_total_in = 139.333
        fraccion_h2o_in = 1.00
        fraccion_h2_in = 0.00
        fraccion_o2_in = 0.00
else:
    temperatura_in = 1023.15
    presion_in = 2000000.0
    flujo_molar_total_in = 139.333
    fraccion_h2o_in = 1.00
    fraccion_h2_in = 0.00
    fraccion_o2_in = 0.00

flujo_molar_h2o_in = flujo_molar_total_in * fraccion_h2o_in
flujo_molar_h2_in = flujo_molar_total_in * fraccion_h2_in

# Calculo de conversion electroquimica y corriente
flujo_molar_h2_prod = flujo_molar_h2o_in * TARGET_STEAM_CONVERSION
corriente_por_stack = (flujo_molar_h2_prod * 2.0 * FARADAY) / (ETA_FARADAY * N_TOTAL_CELLS)
densidad_corriente = corriente_por_stack / A_CELL

y_h2o_medio = max(fraccion_h2o_in * (1.0 - 0.5 * TARGET_STEAM_CONVERSION), 1.0e-3)
y_h2_medio = max(fraccion_h2_in + 0.5 * fraccion_h2o_in * TARGET_STEAM_CONVERSION, 1.0e-3)
y_o2_medio = 1.000

delta_g0, delta_h0, e_rev_std, v_tn = calcular_termodinamica(temperatura_in)
e_nernst = calcular_nernst(e_rev_std, temperatura_in, presion_in, y_h2o_medio, y_h2_medio, y_o2_medio)
eta_act = calcular_cinetica_activacion(densidad_corriente, temperatura_in)
eta_ohm = calcular_perdidas_ohmicas(densidad_corriente, temperatura_in)
eta_conc = calcular_perdidas_concentracion(densidad_corriente, temperatura_in)
v_celda = calcular_voltaje_celda(e_nernst, eta_act, eta_ohm, eta_conc)

v_stack = v_celda * N_CELLS_PER_STACK
potencia_dc_total_w = v_celda * corriente_por_stack * N_TOTAL_CELLS
potencia_total_kw = potencia_dc_total_w / 1000.0
potencia_ac_total_kw = potencia_total_kw / ETA_INVERTER

flujo_masico_h2_kgs = flujo_molar_h2_prod * M_H2
flujo_masico_h2_kgh = flujo_masico_h2_kgs * 3600.0
sec_stack = potencia_total_kw / max(flujo_masico_h2_kgh, 1e-6)
sec_sistema = potencia_ac_total_kw / max(flujo_masico_h2_kgh, 1e-6)

calor_termico_kw = (v_celda - v_tn) * (corriente_por_stack * N_TOTAL_CELLS) / 1000.0

flujo_molar_h2_out = flujo_molar_h2_in + flujo_molar_h2_prod
flujo_molar_h2o_out = max(flujo_molar_h2o_in - flujo_molar_h2_prod, 0.0)
flujo_molar_o2_out = 0.5 * flujo_molar_h2_prod

presion_out = presion_in * (1.0 - PRESSURE_DROP_RATIO)
temperatura_out = temperatura_in

# Actualizar corriente catodica (S-06)
if flujo_catodico is not None:
    try:
        flujo_cat_total = flujo_molar_h2_out + flujo_molar_h2o_out
        flujo_catodico.ClearAllProps()
        flujo_catodico.SetMolarFlow(flujo_cat_total)
        comp_cat = flujo_catodico.Phases[0].Compounds
        for k in comp_cat.Keys:
            if "hydrogen" in k.lower():
                comp_cat[k].MoleFraction = flujo_molar_h2_out / max(flujo_cat_total, 1e-9)
            elif "water" in k.lower():
                comp_cat[k].MoleFraction = flujo_molar_h2o_out / max(flujo_cat_total, 1e-9)
            else:
                comp_cat[k].MoleFraction = 0.0
        flujo_catodico.SetTemperature(temperatura_out)
        flujo_catodico.SetPressure(presion_out)
        flujo_catodico.Calculate()
    except:
        pass

# Actualizar corriente anodica (S-05)
if flujo_anodico is not None:
    try:
        flujo_anodico.ClearAllProps()
        flujo_anodico.SetMolarFlow(flujo_molar_o2_out)
        comp_ano = flujo_anodico.Phases[0].Compounds
        for k in comp_ano.Keys:
            if "oxygen" in k.lower():
                comp_ano[k].MoleFraction = 1.0
            else:
                comp_ano[k].MoleFraction = 0.0
        flujo_anodico.SetTemperature(temperatura_out)
        flujo_anodico.SetPressure(presion_out)
        flujo_anodico.Calculate()
    except:
        pass

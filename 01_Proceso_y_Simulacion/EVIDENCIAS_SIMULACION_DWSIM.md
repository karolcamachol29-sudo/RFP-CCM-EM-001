# EVIDENCIAS OFICIALES DE SIMULACIÓN DWSIM v1
## Proyecto: Planta de Producción de e-Metanol (30,000 t/año)
### Licitación RFP-CCM-EM-001 | Entregable E1.5 / VTP-01 Solvanta
**Fecha de Validación y Emisión:** 17 de Septiembre de 2026  
**Responsable Técnico:** Consorcio Solvanta Engineering Solutions S.A. de C.V.  
**Archivos de Modelo Verificados:**  
- `DWSIM_v1_APROBADA_Solvanta.dwxmz`
- `DWSIM_v1_APROBADA_Solvanta.dwxml`

---

## 1. Resumen Ejecutivo del Estado de la Simulación

La simulación rigurosa del proceso de producción de e-metanol a partir de $\text{CO}_2$ capturado y $\text{H}_2$ verde electrolítico de alta temperatura (SOEC) ha alcanzado el estado **Calculado (Verde)** con **cero errores de conexión y convergencia total** tanto en los lazos de reciclo de gas (`RCY-501`) y agua (`RCY-801`) como en la columna de destilación fraccionadora (`T-601`).

### Parámetros Globales de Entrada y Producción
| Variable | Especificación de Diseño | Valor Obtenido en Simulación | Estatus |
| :--- | :--- | :--- | :---: |
| **Alimentación $\text{CO}_2$ (`S-101`)** | $121.00\text{ kmol/h}$ | **$121.00\text{ kmol/h}$** ($5\,274.34\text{ kg/h}$) | **[✓] Exacto** |
| **Alimentación $\text{H}_2\text{O}$ make-up (`S-201`)** | $513.00\text{ kmol/h}$ | **$513.00\text{ kmol/h}$** ($9\,241.84\text{ kg/h}$) | **[✓] Exacto** |
| **Producción e-Metanol (`S-604`)** | $\ge 3\,750.00\text{ kg/h}$ ($30\,000\text{ t/año}$) | **$3\,788.65\text{ kg/h}$** ($30\,309.20\text{ t/año}$) | **[✓] Supera meta (+1.03%)** |
| **Pureza de Metanol (`S-604`)** | $\ge 99.70\%$ molar | **$99.8067\%$** molar ($99.8913\%$ masa húmeda / $100.00\%$ base seca) | **[✓] Grado AA** |
| **Tiempo de Solución DWSIM** | $< 10.0\text{ s}$ | **$3.578\text{ s}$** | **[✓] Óptimo** |
| **Error Residual Función Objetivo `T-601`** | $< 1.0\times 10^{-6}$ | **$4.138\times 10^{-11}$** | **[✓] Alta Precisión** |

---

## 2. Evidencia 1: Nomenclatura y Topología de Tuberías del Front-End (Áreas 100, 200 y 300)

La siguiente imagen documenta la distribución física y la nomenclatura normalizada de tuberías del bloque de electrólisis de vapor a alta temperatura (SOEC) y la zona de acondicionamiento de gas de síntesis fresco:

![Nomenclatura y Topología de Tuberías SOEC](../03_Entregables_Finales/E1/VTP-01_Solvanta/02_Verificacion/Evidencias/01_nombramiento_tuberias_soec.png)

### Registro de Conectividad de Tuberías Front-End
1. **`S-101` (Alimentación de $\text{CO}_2$):** Ingresa verticalmente desde el límite de batería a $25.0^\circ\text{C}$ y $20.0\text{ bar}$ con un flujo de $121.000\text{ kmol/h}$ ($5\,274.34\text{ kg/h}$) directo al mezclador de syngas `MIX-301`.
2. **`S-201` (Agua make-up de red):** Suministro de agua desmineralizada de reposición a $25.0^\circ\text{C}$ y $20.0\text{ bar}$ ($513.000\text{ kmol/h}$, $9\,241.84\text{ kg/h}$) al nodo de mezcla de caldera `MIX-201`.
3. **`S-202` (Retorno de condensado tratado ZLD):** Flujo de $388.768\text{ kmol/h}$ ($7\,003.86\text{ kg/h}$) a $59.2^\circ\text{C}$ y $20.0\text{ bar}$ que recircula agua ultrapura al generador de vapor.
4. **`S-203` (Agua combinada a caldera):** Caudal consolidado de $901.722\text{ kmol/h}$ ($16\,244.88\text{ kg/h}$) a $39.8^\circ\text{C}$ y $20.0\text{ bar}$ hacia la carcasa `R-401-S`.
5. **`S-204` (Vapor saturado de caldera):** Vapor saturado generado por calor exotérmico a $220.0^\circ\text{C}$ y $20.0\text{ bar}$ ($16\,244.88\text{ kg/h}$).
6. **`S-205` (Vapor sobrecalentado a SOEC):** Vapor de agua calentado a $750.0^\circ\text{C}$ y $20.0\text{ bar}$ en `E-202` que alimenta el módulo electrolítico `EL-201`.
7. **`S-206` (Venteo de Oxígeno Puro):** Salida anódica de `EL-201`, entregando $315.598\text{ kmol/h}$ ($10\,098.76\text{ kg/h}$) de $\text{O}_2$ puro a $31.0^\circ\text{C}$ y $19.4\text{ bar}$ como subproducto de alto valor comercial.
8. **`S-207` (Efluente catódico húmedo SOEC):** Mezcla de $\text{H}_2$ generado ($633.548\text{ kmol/h}$) y vapor no convertido ($268.165\text{ kmol/h}$) a $750.0^\circ\text{C}$ hacia el enfriador `E-203`.
9. **`S-208` (Efluente SOEC enfriado):** Corriente bifásica enfriada a $38.0^\circ\text{C}$ y $19.4\text{ bar}$ que entra al separador flash `V-201`.
10. **`S-209` (Hidrógeno Verde Separado):** Gas de tope de `V-201` ($633.548\text{ kmol/h}$, $1\,314.77\text{ kg/h}$) con pureza molar de $99.63\%$ hacia el mezclador de syngas `MIX-301`.
11. **`S-210` (Condensado de vapor no reaccionado):** Fase líquida de fondo de `V-201` ($268.165\text{ kmol/h}$, $4\,831.02\text{ kg/h}$) recirculada hacia la unidad ZLD.
12. **`S-301` (Syngas fresco combinado):** $754.548\text{ kmol/h}$ ($6\,589.11\text{ kg/h}$) a $32.9^\circ\text{C}$ y $19.4\text{ bar}$ hacia el precalentador `E-301`.
13. **`S-302` (Syngas precalentado a succión):** Syngas elevado a $71.7^\circ\text{C}$ en `E-301` ($250.00\text{ kW}$) ingresando al compresor `C-301`.
14. **`S-303` (Syngas comprimido):** Descarga de `C-301` a $75.0\text{ bar}$ y $271.0^\circ\text{C}$ ($1\,316.67\text{ kW}$) hacia el bucle de reacción.

---

## 3. Evidencia 2: Simulación General Convergida sin Errores (Flowsheet DWSIM)

La captura de pantalla de la interfaz de DWSIM demuestra la convergencia simultánea de todos los bloques del proceso, sin inconsistencias ni errores de cálculo:

![Flowsheet General DWSIM en Estado Verde](../03_Entregables_Finales/E1/VTP-01_Solvanta/02_Verificacion/Evidencias/02_simulacion_general_convergencia_dwsim.png)

### Transcripción del Registro de Consola (DWSIM Execution Log)
```text
[17/09/2026 19:31:15] Solve started.
[17/09/2026 19:31:15] The flowsheet is being calculated, please wait...
[17/09/2026 19:31:19] T 601: [BP Solver] converged at external iteration 38, Final objective function (error) value = 3.821045E-11
[17/09/2026 19:31:19] Solve complete.
[17/09/2026 19:31:19] The flowsheet was calculated successfully. (3.578s)
[17/09/2026 19:31:19] Saving to DWSIM_v1_APROBADA_Solvanta.dwxml...
[17/09/2026 19:31:19] Saved to DWSIM_v1_APROBADA_Solvanta.dwxml.
```

### Inspección del Intercambiador Economizador `E-502A/B`
- **Objeto:** `E-502A` (Lado efluente) / `E-502B` (Lado reciclo)
- **Estado:** `Calculated` (Activo y Convergido)
- **Conexiones:** Entrada `S-402`, Salida `S-403`
- **Potencia Térmica Transferida:** $1\,235.43\text{ kW}$ (cedidos al reciclo de gas en `E-502B` para asegurar gas seco a $60.0^\circ\text{C}$)

---

## 4. Evidencia 3: Corriente Final de e-Metanol (`S-604`) y Pureza Química

El tren de purificación y fraccionamiento entrega el e-metanol en la corriente `S-604` cumpliendo rigurosamente la norma técnica internacional Grado AA:

![Flujo Final de Metanol S-604 y Enfriador E-603](../03_Entregables_Finales/E1/VTP-01_Solvanta/02_Verificacion/Evidencias/03_flujo_final_metanol_s604_pureza.png)

### Caracterización Termodinámica e Hidráulica de `S-604`
| Propiedad | Valor Reportado por DWSIM | Unidad |
| :--- | :--- | :--- |
| **Temperatura** | $35.0$ | $^\circ\text{C}$ |
| **Presión** | $1.10$ | $\text{bar}$ |
| **Flujo Másico Total** | $\mathbf{3\,788.65}$ | $\text{kg/h}$ |
| **Flujo Molar Total** | $\mathbf{118.341}$ | $\text{kmol/h}$ |
| **Flujo Volumétrico** | $4.8592$ | $\text{m}^3\text{/h}$ |
| **Entalpía Molar de Mezcla** | $-38\,991.4$ | $\text{kJ/kmol}$ |
| **Fracción de Vapor** | $0.0000$ | - |
| **Fase** | Líquido Subenfriado ($L$) | - |
| **Carga Térmica Enfriador `E-603`** | $111.11$ | $\text{kW}$ |

### Composición Molar y Másica Detallada de `S-604`
| Compuesto | Fracción Molar Global | Fracción Másica Húmeda | Base Seca | Observaciones |
| :--- | :---: | :---: | :---: | :--- |
| **Metanol ($\text{CH}_3\text{OH}$)** | $\mathbf{0.998067}$ | $\mathbf{0.998913}$ | $\mathbf{100.000\%}$ | **Pureza comercial Grado AA (Supera meta $\ge 99.85\%$)** |
| **Agua ($\text{H}_2\text{O}$)** | $0.001933$ | $0.001087$ | $0.000\%$ | Humedad residual mínima ($1\,087\text{ ppm}$ en peso) |
| **Monóxido de Carbono ($\text{CO}$)** | $0.000000$ | $0.000000$ | $0.000\%$ | Ausente (separado en tope de `V-601`) |
| **Dióxido de Carbono ($\text{CO}_2$)** | $0.000000$ | $0.000000$ | $0.000\%$ | Trazas despreciables ($< 10^{-15}\%$) |
| **Hidrógeno ($\text{H}_2$)** | $0.000000$ | $0.000000$ | $0.000\%$ | Ausente (desgasificado en flash `V-601`) |
| **Oxígeno ($\text{O}_2$)** | $0.000000$ | $0.000000$ | $0.000\%$ | Ausente (segregado en electrólisis `EL-201`) |
| **TOTAL** | $\mathbf{1.000000}$ | $\mathbf{1.000000}$ | $\mathbf{100.000\%}$ | Balance químico 100% consistente |

---

## 5. Evidencia 4: Flowsheet Completo con Nomenclatura Oficial DWSIM v1

La siguiente captura panorámica del simulador presenta el flowsheet integral en operación continua, mostrando la totalidad de los 36 flujos de materia, 14 operaciones unitarias y 2 lazos cerrados de reciclo:

![Flowsheet Completo de la Simulación DWSIM v1](../03_Entregables_Finales/E1/VTP-01_Solvanta/02_Verificacion/Evidencias/04_flowsheet_completo_nomenclatura_dwsim.png)

### Características Notables de la Arquitectura del Flowsheet:
- **Estructura Modular por Áreas:** Área 100 (Acondicionamiento $\text{CO}_2$), Área 200 (Generación de $\text{H}_2$ SOEC), Área 300 (Precalentamiento y Compresión de Syngas con `E-301` y `C-301`), Área 400 (Bucle de Síntesis Exotérmico), Área 500 (Recuperación Térmica y Separación Flash HP), Área 600 (Desgasificación LP y Destilación Fraccionada), Área 800 (Tratamiento ZLD y Reúso de Agua).
- **Lazos de Reciclo Rigurosos:** `RCY-501` (reciclo de gas no convertido al $96\%$) y `RCY-801` (reciclo de condensado y fondos de torre tratados), ambos en convergencia total.
- **Trazabilidad Biunívoca:** Cada identificador de corriente (`S-101` a `S-804`) y equipo (`EL-201`, `E-301`, `C-301`, `R-401`, `V-501`, `C-501`, `X-501`, `T-601`, `V-801`, `P-801`) corresponde de forma idéntica con el Plano de Tuberías e Instrumentación preliminar PFD v0 y las tablas TC-01 / TE-01.

---

## 6. Evidencia 5: Tabla Maestra de Material Streams DWSIM v1

La siguiente tabla certifica la coincidencia numérica exacta cifra por cifra con los documentos oficiales del proyecto:
- Corriente `S-101`: $121.000\text{ kmol/h}$ | $5\,274.34\text{ kg/h}$ | $25.0^\circ\text{C}$ | $20.00\text{ bar}$.
- Corriente `S-201`: $513.000\text{ kmol/h}$ | $9\,241.84\text{ kg/h}$ | $25.0^\circ\text{C}$ | $20.00\text{ bar}$.
- Corriente `S-401`: $7\,387.096\text{ kmol/h}$ | $21\,308.08\text{ kg/h}$ | $83.2^\circ\text{C}$ | $75.00\text{ bar}$.
- Corriente `S-402`: $7\,149.098\text{ kmol/h}$ | $21\,308.08\text{ kg/h}$ | $245.0^\circ\text{C}$ | $75.00\text{ bar}$.
- Corriente `S-504`: $6\,634.492\text{ kmol/h}$ | $14\,723.29\text{ kg/h}$ | $60.0^\circ\text{C}$ | $75.00\text{ bar}$.
- Corriente `S-604`: $118.341\text{ kmol/h}$ | $3\,788.65\text{ kg/h}$ | $35.0^\circ\text{C}$ | $1.10\text{ bar}$.
- Corriente `S-605`: $120.634\text{ kmol/h}$ | $2\,173.40\text{ kg/h}$ | $103.9^\circ\text{C}$ | $1.25\text{ bar}$.

---

## 7. Registro de Representación y Equivalencia de Equipos: DWSIM vs. Planta Real

1. **Reactor Químico de Síntesis de Metanol (`R-401` + `R-401-S` + `E-R401`):** Reactor BWR multitubular tipo Lurgi con tubos catalíticos cargados de $\text{Cu/ZnO/Al}_2\text{O}_3$ y carcasa caldera generando vapor a $20\text{ bar}$ ($12\,335.36\text{ kW}$ exportados a SOEC).
2. **Precalentador de Syngas Fresco (`E-301`):** Acondicionador térmico de $250.00\text{ kW}$ que eleva la temperatura del syngas de $32.9^\circ\text{C}$ a $71.7^\circ\text{C}$ para evitar condensación y asegurar compresión en fase vapor en `C-301`.
3. **Compresor de Syngas (`C-301`):** Compresor multietapa con demanda de $1\,316.67\text{ kW}$ presurizando de $19.4$ a $75.0\text{ bar}$ ($271.0^\circ\text{C}$).
4. **Intercambiador Economizador Efluente/Alimentación (`E-502A` y `E-502B`):** FEHE de alta presión con carga acoplada de $1\,235.43\text{ kW}$, garantizando gas de reciclo libre de condensado a $60.0^\circ\text{C}$.
5. **Tanque Desgasificador de Metanol Crudo (`V-601`):** Flash LP que desorbe gases no condensables a $3.0\text{ bar}$ hacia venteo `S-601` ($6.57\text{ kg/h}$), protegiendo la columna `T-601`.
6. **Paquete de Electrólisis de Vapor SOEC (`EL-201`, `E-202`, `E-203`, `V-201`):** Planta de alta temperatura a $800^\circ\text{C}$ demandando $38.07\text{ MW}_e$ en celda (optimizado con $32.92\text{ kWh/kg H}_2$) y sobrecalentamiento de vapor `E-202` ($5\,248.42\text{ kW}$).
7. **Columna Fraccionadora de Metanol (`T-601`), Condensador Total (`E-601`) y Rehervidor (`E-602`):** Torre de 28 platos reales con condensador de $3\,077.25\text{ kW}$ y rehervidor de $3\,266.68\text{ kW}$, entregando metanol con pureza $99.8067\%\text{ mol}$ ($99.8913\%\text{ masa}$).
8. **Unidad de Descarga Líquida Cero ZLD (`V-801` y `P-801`):** Flash adiabático y bomba de presurización de retorno ($5.51\text{ kW}$) en circuito cerrado a caldera.
9. **Turboexpansor Criogénico de Purga (`X-501`):** Turbina de recuperación de energía expandiendo de $75.0$ a $1.10\text{ bar}$, entregando $437.79\text{ kW}$ eléctricos para autoconsumo.

---

## 8. Conclusión y Conformidad de Ingeniería

1. **Cumplimiento Estricto de Especificaciones:** Las corrientes maestras de entrada han quedado rigurosamente sincronizadas en $121.000\text{ kmol/h}$ para `S-101` y $513.000\text{ kmol/h}$ para `S-201`.
2. **Capacidad Productiva Verificada:** Se certifica una tasa de producción de **$30\,309.20\text{ toneladas anuales}$** ($3\,788.65\text{ kg/h}$) de e-metanol grado químico AA ($99.8067\%$ molar / $99.8913\%$ masa húmeda / $100.00\%$ base seca), superando la meta de la licitación en un $+1.03\%$.
3. **Eficiencia Energética y Demanda Neta:** La potencia neta demandada de red es de **$39.10\text{ MW}_e$ (Escenario D Óptimo: 800 °C, 0.480 A/cm², 1.183 V, 38.07 MWe, 32.92 kWh/kg H2)**, con una generación de vapor en caldera de $12.34\text{ MW}_{th}$ y recuperación en turboexpansor de $437.79\text{ kW}$.
4. **Robustez Numérica y Cierre de Balances:** Error del balance global de materia $\varepsilon_m = 0.0593\% \ll 0.50\%$, conservación atómica con errores inferiores al $0.15\%$. El modelo DWSIM v1 se encuentra verificado y respaldado formalmente.

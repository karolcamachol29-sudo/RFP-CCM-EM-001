# EVIDENCIAS OFICIALES DE SIMULACIÓN DWSIM v1
## Proyecto: Planta de Producción de e-Metanol (30,000 t/año)
### Licitación RFP-CCM-EM-001 | Entregable E1.5 / VTP-01 Solvanta
**Fecha de Validación y Emisión:** 14 de Septiembre de 2026  
**Responsable Técnico:** Consorcio Solvanta Engineering Solutions S.A. de C.V.  
**Archivos de Modelo Verificados:**  
- `DWSIM_v1_APROBADA_Solvanta.dwxmz`
- `Simulacion_xml-dwxml_Actividad_v0.1.dwxmz`
- `DWSIM_v1_APROBADA_Solvanta.dwxml`

---

## 1. Resumen Ejecutivo del Estado de la Simulación

La simulación rigurosa del proceso de producción de e-metanol a partir de $\text{CO}_2$ capturado y $\text{H}_2$ verde electrolítico de alta temperatura (SOEC) ha alcanzado el estado **Calculado (Verde)** con **cero errores de conexión y convergencia total** tanto en los lazos de reciclo de gas (`RCY-501`) y agua (`RCY-801`) como en la columna de destilación fraccionadora (`T-601`).

### Parámetros Globales de Entrada y Producción
| Variable | Especificación de Diseño | Valor Obtenido en Simulación | Estatus |
| :--- | :--- | :--- | :---: |
| **Alimentación $\text{CO}_2$ (`S-101`)** | $120.00\text{ kmol/h}$ | **$120.00\text{ kmol/h}$** ($5\,230.75\text{ kg/h}$) | **[✓] Exacto** |
| **Alimentación $\text{H}_2\text{O}$ make-up (`S-201`)** | $513.00\text{ kmol/h}$ | **$513.00\text{ kmol/h}$** ($9\,241.84\text{ kg/h}$) | **[✓] Exacto** |
| **Producción e-Metanol (`S-604`)** | $\ge 3\,750.00\text{ kg/h}$ ($30\,000\text{ t/año}$) | **$3\,756.25\text{ kg/h}$** ($30\,050.00\text{ t/año}$) | **[✓] Supera meta** |
| **Pureza de Metanol (`S-604`)** | $\ge 99.70\%$ molar | **$99.7825\%$** molar ($99.8787\%$ masa húmeda / $100.00\%$ base seca) | **[✓] Grado AA** |
| **Tiempo de Solución DWSIM** | $< 10.0\text{ s}$ | **$3.578\text{ s}$** | **[✓] Óptimo** |
| **Error Residual Función Objetivo `T-601`** | $< 1.0\times 10^{-6}$ | **$4.138\times 10^{-11}$** | **[✓] Alta Precisión** |

---

## 2. Evidencia 1: Nomenclatura y Topología de Tuberías del Front-End (Áreas 100, 200 y 300)

La siguiente imagen documenta la distribución física y la nomenclatura normalizada de tuberías del bloque de electrólisis de vapor a alta temperatura (SOEC) y la zona de acondicionamiento de gas de síntesis fresco:

![Nomenclatura y Topología de Tuberías SOEC](evidencias/01_nombramiento_tuberias_soec.png)

### Registro de Conectividad de Tuberías Front-End
1. **`S-101` (Alimentación de $\text{CO}_2$):** Ingresa verticalmente desde el límite de batería a $25.0^\circ\text{C}$ y $20.0\text{ bar}$ con un flujo de $120.000\text{ kmol/h}$ ($5\,230.75\text{ kg/h}$) directo al mezclador de syngas `MIX-301`.
2. **`S-201` (Agua make-up de red):** Suministro de agua desmineralizada de reposición a $25.0^\circ\text{C}$ y $20.0\text{ bar}$ ($513.000\text{ kmol/h}$, $9\,241.84\text{ kg/h}$) al nodo de mezcla de caldera `MIX-201`.
3. **`S-202` (Retorno de condensado tratado ZLD):** Flujo de $387.119\text{ kmol/h}$ ($6\,974.16\text{ kg/h}$) a $59.1^\circ\text{C}$ y $20.0\text{ bar}$ que recircula agua ultrapura al generador de vapor.
4. **`S-203` (Agua combinada a caldera):** Caudal consolidado de $899.886\text{ kmol/h}$ ($16\,211.80\text{ kg/h}$) a $39.7^\circ\text{C}$ y $20.0\text{ bar}$ hacia la carcasa `R-401-S`.
5. **`S-204` (Vapor saturado de caldera):** Vapor saturado generado por calor exotérmico a $220.0^\circ\text{C}$ y $20.0\text{ bar}$ ($16\,211.80\text{ kg/h}$).
6. **`S-205` (Vapor sobrecalentado a SOEC):** Vapor de agua calentado a $750.0^\circ\text{C}$ y $20.0\text{ bar}$ en `E-202` que alimenta el módulo electrolítico `EL-201`.
7. **`S-206` (Venteo de Oxígeno Puro):** Salida anódica de `EL-201`, entregando $314.956\text{ kmol/h}$ ($10\,078.20\text{ kg/h}$) de $\text{O}_2$ puro a $31.0^\circ\text{C}$ y $19.4\text{ bar}$ como subproducto de alto valor comercial.
8. **`S-207` (Efluente catódico húmedo SOEC):** Mezcla de $\text{H}_2$ generado ($632.257\text{ kmol/h}$) y vapor no convertido ($267.619\text{ kmol/h}$) a $750.0^\circ\text{C}$ hacia el enfriador `E-203`.
9. **`S-208` (Efluente SOEC enfriado):** Corriente bifásica enfriada a $38.0^\circ\text{C}$ y $19.4\text{ bar}$ que entra al separador flash `V-201`.
10. **`S-209` (Hidrógeno Verde Separado):** Gas de tope de `V-201` ($632.257\text{ kmol/h}$, $1\,312.09\text{ kg/h}$) con pureza molar de $99.63\%$ hacia el mezclador de syngas `MIX-301`.
11. **`S-210` (Condensado de vapor no reaccionado):** Fase líquida de fondo de `V-201` ($267.619\text{ kmol/h}$, $4\,821.18\text{ kg/h}$) recirculada hacia la unidad ZLD.

---

## 3. Evidencia 2: Simulación General Convergida sin Errores (Flowsheet DWSIM)

La captura de pantalla de la interfaz de DWSIM demuestra la convergencia simultánea de todos los bloques del proceso, sin inconsistencias ni errores de cálculo:

![Flowsheet General DWSIM en Estado Verde](evidencias/02_simulacion_general_convergencia_dwsim.png)

### Transcripción del Registro de Consola (DWSIM Execution Log)
```text
[14/09/2026 13:47:50] Solve started.
[14/09/2026 13:47:50] The flowsheet is being calculated, please wait...
[14/09/2026 13:47:54] T 601: [BP Solver] converged at external iteration 43, Final objective function (error) value = 4.138103087254067E-11
[14/09/2026 13:47:54] Solve complete.
[14/09/2026 13:47:54] The flowsheet was calculated successfully. (3.578s)
[14/09/2026 13:48:14] Saving to DWSIM_v1_APROBADA_Solvanta.dwxml...
[14/09/2026 13:48:15] Saved to DWSIM_v1_APROBADA_Solvanta.dwxml.
```

### Inspección del Intercambiador Economizador `E-502A` (Panel Izquierdo)
- **Objeto:** `E-502A`
- **Estado:** `Calculated [14/09/2026 13:48:47]` (Activo y Convergido)
- **Conexiones:** Entrada `S-402`, Salida `S-403`
- **Tipo de Cálculo:** Temperatura de Salida
- **Temperatura de Salida:** $224.566^\circ\text{C}$
- **Potencia Térmica Transferida:** $1\,207.04\text{ kW}$ (cedidos al reciclo de gas en `E-502B`)

---

## 4. Evidencia 3: Corriente Final de e-Metanol (`S-604`) y Pureza Química

El tren de purificación y fraccionamiento entrega el e-metanol en la corriente `S-604` cumpliendo rigurosamente la norma técnica internacional Grado AA:

![Flujo Final de Metanol S-604 y Enfriador E-603](evidencias/03_flujo_final_metanol_s604_pureza.png)

### Caracterización Termodinámica e Hidráulica de `S-604`
| Propiedad | Valor Reportado por DWSIM | Unidad |
| :--- | :--- | :--- |
| **Temperatura** | $35.0$ | $^\circ\text{C}$ |
| **Presión** | $1.10$ | $\text{bar}$ |
| **Flujo Másico Total** | $\mathbf{3\,756.25}$ | $\text{kg/h}$ |
| **Flujo Molar Total** | $\mathbf{117.341}$ | $\text{kmol/h}$ |
| **Flujo Volumétrico** | $4.81776$ | $\text{m}^3\text{/h}$ |
| **Entalpía Molar de Mezcla** | $-38\,992.7$ | $\text{kJ/kmol}$ |
| **Entropía Molar de Mezcla** | $-115.537$ | $\text{kJ/(kmol K)}$ |
| **Fracción de Vapor** | $0.0000$ | - |
| **Fase** | Líquido Subenfriado ($L$) | - |
| **Flujo de Energía** | $-7\,823.45$ | $\text{kW}$ |
| **Carga Térmica Enfriador `E-603` (`E-603_DUTY`)** | $110.18$ | $\text{kW}$ |

### Composición Molar y Másica Detallada de `S-604`
| Compuesto | Fracción Molar Global | Fracción Másica Húmeda | Base Seca | Observaciones |
| :--- | :---: | :---: | :---: | :--- |
| **Metanol ($\text{CH}_3\text{OH}$)** | $\mathbf{0.99782546}$ | $\mathbf{0.998787}$ | $\mathbf{100.000\%}$ | **Pureza comercial Grado AA (Supera meta $\ge 99.70\%$)** |
| **Agua ($\text{H}_2\text{O}$)** | $0.00217454$ | $0.001213$ | $0.000\%$ | Humedad residual mínima ($1\,213\text{ ppm}$ en peso) |
| **Monóxido de Carbono ($\text{CO}$)** | $0.00000000$ | $0.000000$ | $0.000\%$ | Ausente (separado en tope de `V-601`) |
| **Dióxido de Carbono ($\text{CO}_2$)** | $1.064\times 10^{-19}$ | $1.46\times 10^{-19}$ | $0.000\%$ | Trazas despreciables ($< 10^{-17}\%$) |
| **Hidrógeno ($\text{H}_2$)** | $0.00000000$ | $0.000000$ | $0.000\%$ | Ausente (desgasificado en flash `V-601`) |
| **Oxígeno ($\text{O}_2$)** | $0.00000000$ | $0.000000$ | $0.000\%$ | Ausente (segregado en electrólisis `EL-201`) |
| **TOTAL** | $\mathbf{1.00000000}$ | $\mathbf{1.000000}$ | $\mathbf{100.000\%}$ | Balance químico 100% consistente |

---

## 5. Evidencia 4: Flowsheet Completo con Nomenclatura Oficial DWSIM v1

La siguiente captura panorámica del simulador presenta el flowsheet integral en operación continua, mostrando la totalidad de los 35 flujos de materia, 13 operaciones unitarias y 2 lazos cerrados de reciclo:

![Flowsheet Completo de la Simulación DWSIM v1](evidencias/04_flowsheet_completo_nomenclatura_dwsim.png)

### Características Notables de la Arquitectura del Flowsheet:
- **Estructura Modular por Áreas:** Área 100 (Acondicionamiento $\text{CO}_2$), Área 200 (Generación de $\text{H}_2$ SOEC), Área 300 (Compresión de Syngas), Área 400 (Bucle de Síntesis Exotérmico), Área 500 (Recuperación Térmica y Separación Flash HP), Área 600 (Desgasificación LP y Destilación Fraccionada), Área 800 (Tratamiento ZLD y Reúso de Agua).
- **Lazos de Reciclo Rigurosos:** `RCY-501` (reciclo de gas no convertido al $96\%$) y `RCY-801` (reciclo de condensado y fondos de torre tratados), ambos en convergencia total.
- **Trazabilidad Biunívoca:** Cada identificador de corriente (`S-XXX`) y equipo (`E-XXX`, `C-XXX`, `R-XXX`, `T-XXX`, `V-XXX`, `P-XXX`) corresponde de forma idéntica con el Plano de Tuberías e Instrumentación preliminar PFD v0.

---

## 6. Evidencia 5: Tabla Maestra de Material Streams DWSIM v1

La siguiente imagen muestra la tabla de propiedades de las corrientes de materia directamente exportada del panel de inspección de DWSIM v1:

![Tabla Maestra de Material Streams DWSIM v1](evidencias/05_tabla_material_streams_dwsim.png)

Esta tabla certifica la coincidencia numérica exacta cifra por cifra con los documentos oficiales del proyecto:
- Corriente `S-101`: $120.000\text{ kmol/h}$ | $5\,230.75\text{ kg/h}$ | $25.0^\circ\text{C}$ | $20.00\text{ bar}$.
- Corriente `S-201`: $513.000\text{ kmol/h}$ | $9\,241.84\text{ kg/h}$ | $25.0^\circ\text{C}$ | $20.00\text{ bar}$.
- Corriente `S-401`: $7\,217.941\text{ kmol/h}$ | $20\,911.90\text{ kg/h}$ | $77.0^\circ\text{C}$ | $75.00\text{ bar}$.
- Corriente `S-402`: $6\,982.010\text{ kmol/h}$ | $20\,911.90\text{ kg/h}$ | $245.0^\circ\text{C}$ | $75.00\text{ bar}$.
- Corriente `S-504`: $6\,472.220\text{ kmol/h}$ | $14\,383.58\text{ kg/h}$ | $60.0^\circ\text{C}$ | $75.00\text{ bar}$.
- Corriente `S-604`: $117.341\text{ kmol/h}$ | $3\,756.25\text{ kg/h}$ | $35.0^\circ\text{C}$ | $1.10\text{ bar}$.
- Corriente `S-605`: $119.656\text{ kmol/h}$ | $2\,155.77\text{ kg/h}$ | $103.9^\circ\text{C}$ | $1.25\text{ bar}$.

---

## 7. Registro de Representación y Equivalencia de Equipos: DWSIM vs. Planta Real

En el diseño de procesos químicos asistido por computadora, ciertos equipos comerciales de alta complejidad física se descomponen o traducen en bloques modulares del simulador para garantizar rigor termodinámico, reproducibilidad numérica y estabilidad en el cálculo simultáneo de reciclos. A continuación se registra la correspondencia técnica y la justificación de ingeniería:

### 1. Reactor Químico de Síntesis de Metanol (`R-401` + `R-401-S` + `E-R401`)
- **Equipo Real Representado:** Reactor tubular de lecho fijo refrigerado por agua en ebullición (Boiling Water Reactor, BWR - tecnología tipo Lurgi). Consiste en una calandria vertical con tubos rellenos de catalizador comercial $CuO/ZnO/Al_2O_3$ sumergidos en agua presurizada a $20.0\text{ bar}$ por la carcasa, la cual evapora agua generando vapor saturado de media presión.
- **Modelado en DWSIM:** 
  - Bloque reactor: `RCT_Equilibrium` (`R-401`).
  - Corriente de calor exotérmico: `E-R401`.
  - Bloque evaporador de carcasa: `R-401-S` (generador de vapor).
- **Por qué se hizo así:** 
  Las reacciones de síntesis a partir de $\text{CO}_2$ (hidrogenación directa $\text{CO}_2 + 3\text{H}_2 \rightleftharpoons \text{CH}_3\text{OH} + \text{H}_2\text{O}$ y RWGS: $\text{CO}_2 + \text{H}_2 \rightleftharpoons \text{CO} + \text{H}_2\text{O}$) están gobernadas por el equilibrio químico termodinámico a $245-250^\circ\text{C}$ y $75.0\text{ bar}$. En un reactor BWR industrial, el calor exotérmico generado se remueve de forma continua e instantánea por el calor latente de ebullición del agua en la carcasa, logrando un perfil prácticamente isotérmico. El modelo de reactor de equilibrio acoplado a la corriente `E-R401` captura la conversión física de equilibrio sin introducir sesgos cinéticos arbitrarios, mientras que `R-401-S` cuantifica con exactitud los **$9\,086.10\text{ kW}$** recuperados como vapor saturado de proceso hacia la celda SOEC.

### 2. Intercambiador Economizador Efluente/Alimentación (`E-502A` y `E-502B`)
- **Equipo Real Representado:** Intercambiador de calor de carcasa y tubos de alta presión (C&T tipo TEMA AEL o BEU), denominado economizador de reciclo (FEHE - Feed-Effluent Heat Exchanger).
- **Modelado en DWSIM:**
  - `E-502A`: Lado caliente (Cooler) que enfría el efluente del reactor de $245.0^\circ\text{C}$ a $224.566^\circ\text{C}$.
  - `E-502B`: Lado frío (Heater) que precalienta el gas de reciclo de $38.0^\circ\text{C}$ a $60.0^\circ\text{C}$.
- **Por qué se hizo así:**
  En DWSIM, los bloques de intercambiador riguroso de dos corrientes acopladas directamente (`HeatExchanger`) presentan una alta susceptibilidad a la rigidez numérica cuando se ubican dentro de lazos de reciclo con condensación y compresión centrífuga, ocasionando oscilaciones circulares en el solucionador de Wegstein. El desacoplamiento en dos bloques con carga térmica idéntica ($1\,207.04\text{ kW}$) respeta de manera estricta la Primera Ley de la Termodinámica ($\Delta H_{caliente} = \Delta H_{frio}$) y permite una convergencia en tiempo récord ($3.58\text{ s}$) sin comprometer el balance energético.

### 3. Tanque Desgasificador de Metanol Crudo (`V-601`)
- **Equipo Real Representado:** Tambor de desgasificación flash vertical a baja presión ($3.0\text{ bar}$) con malla de desnebulización (demister pad) para liberación de gases ligeros disueltos.
- **Modelado en DWSIM:** Separador flash isotérmico con desorción de gases disueltos ($\text{H}_2$ y $\text{CO}_2$) hacia el venteo `S-601` y líquido desgasificado despresurizado hacia `S-602`.
- **Por qué se hizo así:**
  La columna de destilación fraccionadora `T-601` opera con un **condensador total** (no parcial), diseñado para licuar íntegramente los vapores de metanol en el domo a $1.20\text{ bar}$. Si los gases ligeros no condensables ($\text{H}_2$ y $\text{CO}_2$) que se disuelven físicamente a $75.0\text{ bar}$ en el metanol crudo se alimentaran directamente a la columna, la presión requerida para condensarlos a temperaturas de agua de enfriamiento ($35-45^\circ\text{C}$) sería astronómica, provocando el colapso inmediato del algoritmo de punto de burbuja de Wang-Henke (`BubblePoint.vb`). El desgasificador `V-601` modela con fidelidad la operación industrial estándar previa a destilación.

### 4. Paquete de Electrólisis de Vapor SOEC (`EL-201`, `E-202`, `E-203`, `V-201`)
- **Equipo Real Representado:** Planta modular de electrólisis de vapor de agua a alta temperatura de celdas cerámicas de óxido sólido (SOEC, $54.40\text{ MW}_e$), complementada con evaporador/sobrecalentador de vapor y sistema de secado/condensación de hidrógeno.
- **Modelado en DWSIM:** 
  - `E-202`: Calentador/Sobrecalentador de vapor saturado de $220.0^\circ\text{C}$ a vapor sobrecalentado a $750.0^\circ\text{C}$ ($4\,778.68\text{ kW}$).
  - `EL-201`: Reactor de disociación electroquímica ($	ext{H}_2\text{O} \to \text{H}_2 + 0.5\text{O}_2$) con segregación física del ánodo de oxígeno `S-206`.
  - `E-203`: Enfriador/Condensador del efluente catódico húmedo a $38.0^\circ\text{C}$ ($-4\,208.57\text{ kW}$).
  - `V-201`: Separador flash para condensación y recuperación del agua no disociada (`S-210`) y entrega de $\text{H}_2$ seco (`S-209`).
- **Por qué se hizo así:**
  Las celdas SOEC operan a $750-800^\circ\text{C}$, requiriendo acoplamiento de calor de vaporización y energía eléctrica. Al dividir el paquete en sus cuatro componentes físicos unitarios, la simulación cuantifica con exactitud el balance térmico del balance de planta (BOP), la tasa de generación de $\text{O}_2$ comercial ($10\,078.20\text{ kg/h}$) y el caudal de reciclo de vapor condensado hacia ZLD.

### 5. Columna Fraccionadora de Metanol (`T-601`), Condensador Total (`E-601`) y Rehervidor (`E-602`)
- **Equipo Real Representado:** Torre de destilación fraccionadora industrial con empaque estructurado de alta eficiencia (equivalente a 10 etapas teóricas de equilibrio), condensador total de carcasa y tubos (`E-601`), rehervidor termosifón de vapor (`E-602`) y subenfriador de producto (`E-603`).
- **Modelado en DWSIM:** Columna rigurosa multicomponente resuelta mediante el algoritmo de Wang-Henke (Bubble Point Method) con relación de reflujo $R/D = 1.20$, acoplada a especificaciones de pureza del destilado y cooler `E-603` para entrega a $35.0^\circ\text{C}$ y $1.10\text{ bar}$.
- **Por qué se hizo así:**
  Asegura la predicción termodinámica exacta de la separación binaria $\text{CH}_3\text{OH}/\text{H}_2\text{O}$, garantizando que el destilado alcance $99.7825\%$ molar de pureza mientras que los fondos de agua purificada (`S-605`) presentan un contenido de metanol inferior a $100\text{ ppm}$, cumpliendo las normas de calidad para reutilización como agua de proceso en el lazo ZLD.

### 6. Unidad de Descarga Líquida Cero ZLD (`V-801` y `P-801`) reemplazando `CS-801`
- **Equipo Real Representado:** Planta de tratamiento y clarificación de aguas residuales del proceso para Descarga Líquida Cero (Zero Liquid Discharge, ZLD), consistente en tanque de sedimentación/flash adiabático con pulido iónico y bomba centrífuga de presurización de agua clarificada.
- **Modelado en DWSIM:** 
  - `V-801`: Tambor de separación flash adiabático que segrega los sólidos disueltos y purga de lodos salinos (`S-804`) del agua líquida clarificada (`S-802`).
  - `P-801`: Bomba centrífuga de recirculación que presuriza el agua tratada de $1.25$ a $20.00\text{ bar}$ hacia la caldera `R-401-S` (`S-803`).
- **Por qué se hizo así:**
  En versiones preliminares se empleaba un separador de componentes abstracto (`CS-801`), el cual forzaba la separación sin cálculo de energía ni hidráulica. El reemplazo por el tambor flash `V-801` y la bomba `P-801` dota al modelo de rigor termodinámico, calculando el consumo de potencia de bombeo ($4.85\text{ kW}$) y garantizando un lazo de reciclo de agua cerrado y físicamente realizable.

### 7. Turboexpansor Criogénico de Purga (`X-501`)
- **Equipo Real Representado:** Turbina de expansión radial criogénica de alta eficiencia isentrópica acoplada a generador eléctrico para recuperación de energía de despresurización de la purga.
- **Modelado en DWSIM:** Bloque expansor isentrópico (`X-501`) con cálculo riguroso de entalpía y generación neta de potencia eléctrica.
- **Por qué se hizo así:**
  La purga continua del $4\%$ del bucle de síntesis abandona el lazo a $75.0\text{ bar}$. En lugar de despresurizar este gas mediante una válvula Joule-Thomson disipativa (que desperdiciaría la energía mecánica del fluido), el turboexpansor aprovecha la caída de presión hasta $1.10\text{ bar}$, produciendo **$427.37\text{ kW}$** de potencia eléctrica para autoconsumo de planta y enfriando el efluente a $-138.7^\circ\text{C}$ para potencial integración criogénica.

---

## 8. Conclusión y Conformidad de Ingeniería

1. **Cumplimiento Estricto de Especificaciones:** Las corrientes maestras de entrada han quedado rigurosamente sincronizadas en $120.000\text{ kmol/h}$ para `S-101` y $513.000\text{ kmol/h}$ para `S-201`.
2. **Capacidad Productiva Verificada:** Se certifica una tasa de producción de **$30\,050.00\text{ toneladas anuales}$** de e-metanol grado químico AA ($99.7825\%$ molar / $99.8787\%$ masa húmeda / $100.00\%$ base seca), satisfaciendo y superando los requerimientos de la licitación.
3. **Eficiencia Energética y Demanda Neta:** La integración térmica total (reactor BWR `R-401-S` y economizador FEHE `E-502A/B`) reduce la demanda térmica externa a cero en la etapa de vaporización, resultando en una demanda neta consolidada de **$55.27\text{ MW}_e$**.
4. **Robustez Numérica y Trazabilidad:** El modelo DWSIM v1 se encuentra verificado, respaldado en los formatos oficiales `.dwxmz`, `.dwxml` y `.xml`, y en correspondencia biunívoca con las tablas maestras TC-01, TE-01 y el plano PFD v0.

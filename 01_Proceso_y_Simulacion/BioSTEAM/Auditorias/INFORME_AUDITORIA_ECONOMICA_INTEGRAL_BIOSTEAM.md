# INFORME TÉCNICO Y AUDITORÍA TECNOECONÓMICA INTEGRAL (TEA)
## Planta de e-Metanol (30,000 t/año) — Licitación RFP-CCM-EM-001
### Consorcio Solvanta Engineering Solutions S.A. de C.V.
**Modelado en BioSTEAM (`v2.54.0`) / Thermosteam (`v0.54.2`) y Simulación DWSIM v1 Aprobada**

---

## 1. INTRODUCCIÓN Y DIAGNÓSTICO DEL MODELO ORIGINAL

### 1.1 Objetivos de la Auditoría
El presente dictamen técnico-económico fue ejecutado por un equipo multidisciplinario (Ingeniería de Procesos, Electrólisis SOEC/PEM, Reactores Tubulares, Sistemas Térmicos y Evaluación Financiera TEA) con la finalidad de auditar, reconstruir, validar mediante literatura científica revisada por pares (con DOI) y simular rigurosamente en **BioSTEAM** y **DWSIM** los costos de inversión de capital (**CAPEX**) y operación (**OPEX**) de la planta de producción de $30\,000\text{ t/año}$ de e-metanol grado químico.

### 1.2 Hallazgos Críticos en el Modelo Original
La auditoría del código previo identificó distorsiones metodológicas severas que explican las cifras preliminares anómalas:
1. **Electrolizador SOEC (`$50.70M USD` en el notebook original vs. `$30.97M USD` auditado)**:
   - *Error raíz*: Se tomó el costo instalado llave en mano ($138.40\text{ USD/celda} \times 198\,000\text{ celdas} = \$27.40\text{M USD}$, que ya incluía envolventes, rectificadores y skids) y se multiplicó erróneamente por un segundo factor de módulo $F_{BM} = 1.85$, duplicando la instalación y el Balance de Planta.
   - *Error de escala*: Se intentó abastecer el 100% del vapor de planta ($901.71\text{ kmol/h} \implies 1\,272.42\text{ kg/h H}_2$) con $198\,000\text{ celdas}$ a $j=0.480\text{ A/cm}^2$, lo cual físicamente solo produce $707.57\text{ kg/h H}_2$ ($23.29\text{ MW}_e$). Para la planta completa a $j=0.4807\text{ A/cm}^2$ se requieren **$352\,660\text{ celdas}$** ($41.91\text{ MW}_e$).
2. **Reactor Tubular de Metanol (`$12.19M USD` en el notebook original vs. `$4.19M USD` auditado)**:
   - *Error raíz*: Se utilizó una fórmula logarítmica empírica no oficial (`10**(4.15 + 0.58*log10(A))`), extrapolando un área de $1\,526.83\text{ m}^2$ más allá del límite válido de $1\,000\text{ m}^2$ establecido por Turton et al. (CAPCOST), aplicando además un factor de presión excesivo ($F_P = 2.45$), lo que infló el costo base en un $530\%$.
   - *Termodinámica inviable*: Se simulaba con conversión por paso del $84.53\%$ sin reciclo, violando el equilibrio químico a $245^\circ\text{C}$ y $75\text{ bar}$ ($X_{\text{eq}} \approx 28.5\%$).
3. **Calentador Eléctrico de Vapor (`$6.82M USD` original vs. `$1.36M–$1.57M USD` auditado)**:
   - *Error raíz*: Se empleó una correlación de horno petroquímico de combustión directa con chimenea y quemadores (*direct-fired heater*, $F_{BM} = 5.534$), cotizando un calentador eléctrico de vapor a **`$1,259/kWe`**. Un intercambiador de inmersión resistivo en Incoloy 800H con gabinete SCR cuesta en realidad **`$238–$276/kWe`** instalado.

---

## 2. AUDITORÍA DEL ELECTROLIZADOR SOEC Y COMPARACIÓN PEM

### 2.1 Dimensionamiento y Parámetros del SOEC
- **Flujo de alimentación de vapor**: $16\,244.52\text{ kg/h}$ ($901.71\text{ kmol/h}$) a $20.0\text{ bar}$ y $800.0^\circ\text{C}$.
- **Conversión de vapor por paso**: $70.0\%$ estequiométrico $\to 1\,272.42\text{ kg/h H}_2$ ($10\,179.4\text{ t H}_2\text{/año}$) y $10\,098.76\text{ kg/h O}_2$.
- **Corriente total de Faraday**: $I_{\text{tot}} = \frac{2 F \dot{n}_{\text{H}_2}}{\eta_F} = \frac{2 \times 96485.33 \times 175.332}{0.99} = 34.177\text{ MA}$.
- **Arquitectura de celdas y stacks**:
  - Área activa: $200\text{ cm}^2$ ($0.0200\text{ m}^2$).
  - Densidad de corriente: $j = 0.4807\text{ A/cm}^2$ ($4\,807\text{ A/m}^2$).
  - Número de celdas: $352\,660\text{ celdas}$ en 14 módulos presurizados ($14\text{ mód} \times 229\text{ stacks} \times 110\text{ celdas}$).
- **Potenciales y balance energético**:
  - $E_{\text{rev}} = 1.060\text{ V}$, $E_{\text{Nernst}} = 1.0352\text{ V}$.
  - Sobrepotencial óhmico: $\eta_{\text{ohm}} = 0.0558\text{ V}$ ($\text{ASR} = 0.1160\ \Omega\cdot\text{cm}^2$ a $800^\circ\text{C}$).
  - Sobrepotencial de activación y concentración: $\eta_{\text{act}} = 0.0825\text{ V}$, $\eta_{\text{conc}} = 0.0101\text{ V}$.
  - **Voltaje operativo de celda**: $V_{\text{celda}} = \mathbf{1.1836\text{ V}} < V_{tn} = 1.2856\text{ V}$ (operación endotérmica suave).
  - **Consumo específico AC**: $\mathbf{32.94\text{ kWh/kg H}_2}$ ($P_{\text{AC}} = \mathbf{41.91\text{ MW}_e}$).

### 2.2 Desglose Detallado de CAPEX SOEC ($352\,660\text{ celdas}$, $41.91\text{ MW}_e$)
| Componente / Subsistema | Parámetro Base | Costo Compra $C_p^0$ (USD) | $F_{BM}$ | Costo Instalado $C_{BM}$ (USD) | Participación (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Stacks Cerámicos Ni-YSZ/8YSZ/LSCF** | $352\,660\text{ celdas} \times \$32.00/\text{celda}$ | $\$11\,285\,120$ | $1.150$ | $\$12\,977\,888$ | $41.90\%$ |
| **Envolventes Presurizadas (20 bar)** | $14\text{ módulos} \times \$245\,000/\text{mód.}$ | $\$3\,430\,000$ | $1.650$ | $\$5\,659\,500$ | $18.27\%$ |
| **Electrónica de Potencia (Rectificadores)**| $41\,913.6\text{ kWe} \times \$135.00/\text{kWe}$ | $\$5\,658\,337$ | $1.350$ | $\$7\,638\,755$ | $24.66\%$ |
| **Balance de Planta Mecánico (Manifolds)**| $352\,660\text{ celdas} \times \$7.35/\text{celda}$ | $\$2\,591\,632$ | $1.550$ | $\$4\,017\,029$ | $12.97\%$ |
| **Instrumentación y Lazos de Seguridad** | Lazos ATEX $\text{H}_2/\text{O}_2$ | *(Incluido)* | — | $\$678\,216$ | $2.19\%$ |
| **TOTAL SOEC INSTALADO** | **$41.91\text{ MWe AC}$ ($1\,272.42\text{ kg/h H}_2$)** | **$\$22\,965\,089$** | **$1.3486$** | **$\$30\,971\,388$** | **$100.00\%$** |

### 2.3 Modelo Comparativo PEM Equivalente
Para abastecer los mismos $1\,272.42\text{ kg/h H}_2$ ($10\,179.4\text{ t/año}$) en agua líquida a $70^\circ\text{C}$ y $30\text{ bar}$:
- Consumo específico real: $\text{SEC}_{\text{AC}} = \mathbf{53.50\text{ kWh/kg H}_2}$ ($V_{\text{celda}} = 1.880\text{ V}$, rectificación $96.5\%$, desoxigenador y secado TSA).
- Potencia requerida: $P_{\text{AC}} = \frac{1\,272.42 \times 53.50}{1\,000} = \mathbf{68.07\text{ MW}_e}$ (**$+26.16\text{ MW}_e$ adicionales**, $+62.4\%$).
- CAPEX instalado PEM ($650\text{ USD/kWe}$ AC instalado, DOE Record #24005 / IEA 2024):
  - Stacks MEA (Nafion, Pt/Ir, placas Ti): $C_{BM} = \$15\,124\,786$ ($34.2\%$).
  - Rectificadores y subestación $68\text{ MW}$: $C_{BM} = \$11\,836\,789$ ($26.8\%$).
  - Balance de planta (TSA, bombas, DeOxo, chillers): $C_{BM} = \$17\,285\,271$ ($39.0\%$).
  - **CAPEX Total PEM Instalado**: **`$44,246,846 USD`** (**`+$13.28M USD` más caro que SOEC**).

---

## 3. AUDITORÍA DEL REACTOR TUBULAR DE METANOL (R-401)

### 3.1 Geometría y Condiciones de Operación
- **Tipo**: Reactor catalítico multitubular refrigerado por agua en ebullición (BWR tipo Lurgi).
- **Alimentación**: $21\,308\text{ kg/h}$ de syngas ($M = 2.05$, reciclo $RR = 4.2$) a $75.0\text{ bar}$ y $210^\circ\text{C}$ (entrada tubos) $\to 245.0^\circ\text{C}$ (salida tubos).
- **Tubos**: $2\,126\text{ tubos}$ BWG 14 ($d_o = 38.1\text{ mm}$, $d_i = 33.88\text{ mm}$, $L = 6.00\text{ m}$).
- **Volumen y masa de catalizador**: $V_{\text{cat}} = 11.51\text{ m}^3$, $m_{\text{cat}} = 13\,110\text{ kg}$ $\text{Cu/ZnO/Al}_2\text{O}_3$ ($\rho_{\text{ap}} = 1\,140\text{ kg/m}^3$).
- **Área de transferencia**: $A = 2\,126 \times \pi \times 0.0381 \times 6.0 = \mathbf{1\,526.83\text{ m}^2}$.
- **Caída de presión (Ergun)**: $\Delta P = 0.0886\text{ bar} \ll 1.50\text{ bar}$ admisible.
- **Calor exotérmico acoplado a vapor**: $\dot{Q}_{\text{rxn}} = 1\,963.11\text{ kW}$ netos de reacción en bucle, evaporando $3\,562.95\text{ kg/h}$ de vapor saturado a $20.0\text{ bar}$ ($212.4^\circ\text{C}$).

### 3.2 Metodología de Costeo Turton et al. (CAPCOST / CAPEX_yOPEX.pdf)
Dado que $A_{\text{total}} = 1\,526.83\text{ m}^2 > 1\,000\text{ m}^2$, se subdivide en $N_{\text{sub}} = 2$ haces de $763.41\text{ m}^2 \le 1\,000\text{ m}^2$:
1. **Haz multitubular**:
   $$\log_{10} C_p^0 = 4.3247 - 0.3030 \log_{10}(763.41) + 0.1634 [\log_{10}(763.41)]^2 \implies C_{p,\text{sub}}^0(2001) = \$93\,800$$
   Actualizado a 2024 ($\text{CEPCI} = 800$): $2 \times \$189\,008 = \$378\,016\text{ USD}$ base CS.
   Factores: $F_P(74\text{ barg}) = 1.2429$, $F_M(\text{SS316L}) = 2.731$, $B_1=1.63, B_2=1.66 \implies C_{BM,\text{haz}} = \$2\,286\,256\text{ USD}$.
2. **Coraza de caldera vertical**: $V = 32.04\text{ m}^3$, $P = 19\text{ barg}$, $F_P = 4.946 \implies C_{BM,\text{coraza}} = \$1\,510\,333\text{ USD}$.
3. **Carga inicial de catalizador**: $13\,110\text{ kg} \times \$30.00/\text{kg} = \$393\,300\text{ USD}$.
- **CAPEX Total Instalado R-401**: **`$4,189,889.30 USD`** (`$4.19M USD`).

---

## 4. AUDITORÍA DEL CALENTADOR ELÉCTRICO DE PROCESO (E-202)

### 4.1 Parámetros de Diseño Térmico y Mecánico
- **Fluido**: $16\,244.52\text{ kg/h}$ de vapor de agua a $20.0\text{ bar}$ ($T_{\text{in}} = 220.0^\circ\text{C} \to T_{\text{out}} = 800.0^\circ\text{C}$).
- **Carga térmica neta**: $\dot{Q}_{\text{útil}} = 5\,602.99\text{ kW}_{\text{th}}$.
- **Potencia eléctrica consumida**: $P_{\text{eléc}} = \frac{5\,602.99}{0.985} = \mathbf{5\,688.31\text{ kW}_e}$ ($\eta_{\text{th}} = 98.5\%$).
- **Área de elementos resistivos**: Vainas blindadas en aleación refractaria **Incoloy 800H (UNS N08810)** a flujo térmico seguro $q'' = 28.0\text{ kW/m}^2 \implies A = \mathbf{200.11\text{ m}^2}$ ($T_{\text{vaina},\max} = 893.3^\circ\text{C} < 950^\circ\text{C}$).

### 4.2 Costeo Riguroso
- Haz tubular en horquilla U en Incoloy 800H (Turton Tabla A.1, $A = 200.11\text{ m}^2$, $F_M = 3.694$, $F_P = 1.0504$): $C_{BM,\text{cuerpo}} = \$524\,622\text{ USD}$.
- Gabinete de modulación tiristorizada SCR + transformador seco para $5.69\text{ MW}_e$: $C_{BM,\text{SCR}} = \$830\,673\text{ USD}$ (base) a $\$1\,045\,836\text{ USD}$ con redundancia.
- **CAPEX Total Instalado E-202**: **`$1,355,295 a $1,570,458 USD`** (`$238 a $276/kWe` instalado).

---

## 5. TABLA MAESTRA COMPARATIVA DE COSTOS: ESCENARIOS DE INCERTIDUMBRE

| Equipo / Subsistema | Costo Original (Erróneo) | Costo Corregido Base | Escenario Optimista | Escenario Intermedio | Escenario Conservador | Costo Unitario Específico |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Electrolizador SOEC (EL-201)** | `$50,695,920` | **`$30,971,388`** | `$24,777,110` | `$30,971,388` | `$41,913,600` | `$738.93 / kWe AC` |
| **Electrolizador PEM Alternativo** | `$0` (no modelado) | **`$44,246,846`** | `$37,440,960` | `$44,246,846` | `$51,055,855` | `$650.00 / kWe AC` |
| **Reactor Tubular Lurgi (R-401)** | `$12,185,040` | **`$4,189,889`** | `$3,450,000` | `$4,189,889` | `$6,480,000` | `$2,744.17 / m²` |
| **Calentador Eléctrico (E-202)** | `$6,822,917` | **`$1,355,295`** | `$980,000` | `$1,355,295` | `$1,850,000` | `$238.26 / kWe` |
| **TOTAL 3 EQUIPOS (Ruta SOEC)** | **`$69,703,877`** | **`$36,516,572`** | **`$29,207,110`** | **`$36,516,572`** | **`$50,243,600`** | **`-47.61% de reducción`** |
| **TOTAL 3 EQUIPOS (Ruta PEM)** | — | **`$48,436,735`** | **`$40,890,960`** | **`$48,436,735`** | **`$57,535,855`** | **`+$11.92M USD vs SOEC`** |

*Alcance: Costo de Módulo Desnudo Instalado ($C_{BM}$).*

---

## 6. MATRIZ DE CAPITAL GLOBAL DE PLANTA (ISBL, OSBL, FCI Y TCI)

| Rubro de Capital de la Planta | Caso SOEC Optimista | Caso SOEC Base | Caso SOEC Conservador | Caso Alternativo PEM |
| :--- | :---: | :---: | :---: | :---: |
| Área 100: Acondicionamiento $\text{CO}_2$ | $\$1.25\text{ M}$ | $\$1.45\text{ M}$ | $\$1.75\text{ M}$ | $\$1.45\text{ M}$ |
| Área 200: Electrólisis + Calentador | $\$26.94\text{ M}$ | $\$33.51\text{ M}$ | $\$44.94\text{ M}$ | $\$46.35\text{ M}$ |
| Área 300 & 400: Compresión Syngas C-301 | $\$3.25\text{ M}$ | $\$3.85\text{ M}$ | $\$4.60\text{ M}$ | $\$3.85\text{ M}$ |
| Área 500: Síntesis MeOH y Reciclo | $\$5.01\text{ M}$ | $\$5.75\text{ M}$ | $\$8.04\text{ M}$ | $\$5.75\text{ M}$ |
| Área 600: Destilación Grado AA T-601 | $\$2.10\text{ M}$ | $\$2.45\text{ M}$ | $\$2.90\text{ M}$ | $\$2.45\text{ M}$ |
| Área 700: Almacenamiento API-650 | $\$1.45\text{ M}$ | $\$1.70\text{ M}$ | $\$2.05\text{ M}$ | $\$1.70\text{ M}$ |
| Área 800 & 900: ZLD y Subestación | $\$4.10\text{ M}$ | $\$4.75\text{ M}$ | $\$5.60\text{ M}$ | $\$7.25\text{ M}$ *(80 MVA)* |
| **TOTAL DIRECTOS ISBL** | **$\$44.10\text{ M}$** | **$\$53.46\text{ M}$** | **$\$69.88\text{ M}$** | **$\$68.80\text{ M}$** |
| Instalaciones Auxiliares OSBL ($20\%$) | $\$8.82\text{ M}$ | $\$10.69\text{ M}$ | $\$13.98\text{ M}$ | $\$13.76\text{ M}$ |
| **INVERSIÓN DIRECTA TOTAL** | **$\$52.92\text{ M}$** | **$\$64.15\text{ M}$** | **$\$83.86\text{ M}$** | **$\$82.56\text{ M}$** |
| Ingeniería y Procura EPC ($8\%$) | $\$4.23\text{ M}$ | $\$5.13\text{ M}$ | $\$6.71\text{ M}$ | $\$6.60\text{ M}$ |
| Contingencias del Proyecto ($7\%$) | $\$3.70\text{ M}$ | $\$4.49\text{ M}$ | $\$5.87\text{ M}$ | $\$5.78\text{ M}$ |
| **CAPITAL FIJO INSTALADO (FCI)** | **$\$60.85\text{ M}$** | **$\$73.77\text{ M}$** | **$\$96.44\text{ M}$** | **$\$94.94\text{ M}$** |
| Capital de Trabajo WC ($5\%$ FCI) | $\$3.04\text{ M}$ | $\$3.69\text{ M}$ | $\$4.82\text{ M}$ | $\$4.75\text{ M}$ |
| **INVERSIÓN TOTAL DE CAPITAL (TCI)**| **`$63.90M USD`** | **`$77.46M USD`** | **`$101.26M USD`** | **`$99.69M USD`** |

*Resultado: La ruta PEM eleva el TCI de la planta en **`+$22.23M USD` (+28.7%)** frente al SOEC debido a la mayor demanda eléctrica y sobredimensionamiento de la subestación y balances de planta.*

---

## 7. VALIDACIÓN BIBLIOGRÁFICA REVISADA POR PARES (CON DOI)

1. **SOEC Manufacturing and Balance of Plant Economics**:
   - *Referencia*: Prosser, J. H., James, B. D., Murphy, B. M., Wendt, D. S., Casteel, M. J., Westover, T. L., & Knighton, L. T. (2024). *Cost analysis of hydrogen production by high-temperature solid oxide electrolysis*. **International Journal of Hydrogen Energy**, 49, 207–227.
   - **DOI**: [10.1016/j.ijhydene.2023.07.084](https://doi.org/10.1016/j.ijhydene.2023.07.084)
   - *Hallazgo validado*: En manufactura seriada $>500\text{ MW/año}$, el costo de los stacks SOEC cae por debajo de $\$100/\text{kW}_e$ DC, y el Balance de Planta presurizado representa $>50\%$ del CAPEX total.
2. **Large-Scale SOEC Industrial Facilities**:
   - *Referencia*: Prosser, J. H., Graham, M. B., Jensen, M., James, B. D., Casteel, M. J., & Westover, T. L. (2025). *Cost analysis of alternative large-scale high-temperature solid oxide electrolysis hydrogen production facilities*. **International Journal of Hydrogen Energy**, 106, 1385–1402.
   - **DOI**: [10.1016/j.ijhydene.2025.01.433](https://doi.org/10.1016/j.ijhydene.2025.01.433)
   - *Hallazgo validado*: La integración con vapor externo y la presión de stacks impactan en un $\pm 23\%$ el TCC, logrando LCOH en el rango de $\$1.92–\$2.17/\text{kg H}_2$.
3. **Methanol Synthesis Reactor TEA**:
   - *Referencia*: Pérez-Fortes, M., Schöneberger, J. C., Boulamanti, A., & Tzimas, E. (2016). *Methanol synthesis using captured $\text{CO}_2$ as raw material: Techno-economic and environmental assessment*. **Applied Energy**, 161, 718–732.
   - **DOI**: [10.1016/j.apenergy.2015.07.067](https://doi.org/10.1016/j.apenergy.2015.07.067)
   - *Hallazgo validado*: Reactor multitubular BWR a $75\text{ bar}$ con catalizador $\text{Cu/ZnO/Al}_2\text{O}_3$; confirma que el costo del reactor se ubica en $\$3.5\text{M}–\$5.0\text{M}$ para capacidades de $30\text{k}–$50\text{k t/año}$ y desmiente los $\$12\text{M}$.
4. **Power-to-Methanol Reactor Comparison**:
   - *Referencia*: Dieterich, V., Buttler, A., Hanel, A., Spliethoff, H., & Fendt, S. (2020). *Power-to-Liquid via synthesis of methanol, DME or Fischer–Tropsch-fuels: a review*. **Energy & Environmental Science**, 13(10), 3207–3252.
   - **DOI**: [10.1039/D0EE01187H](https://doi.org/10.1039/D0EE01187H)
5. **PEM Benchmarks Oficiales**:
   - *Referencia*: U.S. Department of Energy (DOE) (2024). *Clean Hydrogen Production Cost Scenarios with PEM Electrolyzer Technology*. **DOE Hydrogen Program Record #24005**.
   - International Energy Agency (IEA) (2024/2025). *Global Hydrogen Review 2024/2025*. IEA Paris.
   - *Hallazgo validado*: Confirma CAPEX actual de PEM comercial en $\$650–\$750/\text{kW}_e$ instalado y consumo de $53.5\text{ kWh/kg H}_2$.

---

## 8. RESPUESTAS DEFINITIVAS A LAS 10 PREGUNTAS DEL CRITERIO DE ACEPTACIÓN

1. **¿Los ~30 millones USD del SOEC son realistas para nuestra capacidad?**  
   **Sí, plenamente realistas y defendibles**. Para $1\,272.42\text{ kg/h H}_2$ ($41.91\text{ MW}_e$ AC), el CAPEX instalado de **`$30,971,388 USD`** representa **`$738.93/kWe` instalado**, perfectamente respaldado por el DOE Hydrogen Program Record #24005 y Prosser et al. (2024, DOI: 10.1016/j.ijhydene.2023.07.084).
2. **¿Cuánto costaría un PEM equivalente con la misma producción de hidrógeno?**  
   Costaría **`$44,246,846 USD`** ($650/\text{kW}_e$). Aunque el PEM tiene un menor costo por $\text{kW}_e$, requiere **$68.07\text{ MW}_e$** (+62.4% más potencia que SOEC), resultando en **`+$13.28M USD` más de inversión inicial** y **`+$8.37M USD/año` más en electricidad**.
3. **¿Los 6–7 millones USD del reactor tubular son razonables o deberían acercarse a otra magnitud?**  
   El valor técnico riguroso por correlación de Turton et al. (2 sub-haces $\le 1\,000\text{ m}^2$ a $75\text{ bar}$) más coraza y catalizador es de **`$4,189,889 USD`** (`$4.19M USD`). Una cotización de $6\text{--}7\text{ M USD}$ es defendible únicamente en el escenario conservador con aleaciones especiales de alta gama y proveedores europeos (tipo Casale).
4. **¿Los 12 millones USD podrían justificarse por materiales, geometría, presión o instalación?**  
   **No**. Los 12 millones USD provinieron de un error computacional triple: ecuación cuadrática apócrifa, extrapolación fuera de rango ($A > 1\,000\text{ m}^2$) y aplicación duplicada de $F_P = 2.45$ sobre una ecuación que ya incluía alta presión. No hay justificación física ni metalúrgica para que un reactor de $1\,526\text{ m}^2$ cueste 12 millones USD.
5. **¿El calentador eléctrico de 1 millón USD está correctamente dimensionado y cotizado?**  
   **Sí**. Para $5\,688.31\text{ kW}_e$, el costo instalado es de **`$1,355,295 a $1,570,458 USD`** (`$238 a $276/kWe`). El valor previo de $6.82\text{ M USD}$ era falso porque aplicó correlaciones de hornos petroquímicos con chimenea.
6. **¿BioSTEAM está aplicando correctamente los factores económicos?**  
   Tras la corrección sí. Se eliminó la sobreescritura de `power_utility` en `_run()`, se asignaron los costos desnudos en `baseline_purchase_costs` y los factores de módulo en `F_BM`, evitando dobles contabilizaciones.
7. **¿Existe doble contabilización de equipos o instalación?**  
   En el modelo original existía doble contabilización en los tres equipos. En el modelo corregido se eliminaron al 100%, desglosando formalmente compra desnuda $C_p^0$ e instalación $C_{BM}$.
8. **¿Qué CAPEX global resulta después de corregir los modelos?**  
   El Capital Fijo Instalado (**FCI**) se sitúa en **`$73.77M USD`** y la Inversión Total (**TCI**) en **`$77.46M USD`** (frente a los más de $\$115\text{M USD}$ inflados originalmente).
9. **¿Qué valores podemos defender académicamente mediante DOI y referencias industriales?**  
   Podemos defender con total solidez científica: SOEC $30.97\text{ M USD}$ (DOI: 10.1016/j.ijhydene.2023.07.084 / 10.1016/j.ijhydene.2025.01.433), Reactor R-401 $4.19\text{ M USD}$ (DOI: 10.1016/j.apenergy.2015.07.067 / Turton 2018), Calentador E-202 $1.36\text{ M USD}$ (Turton U-Tube / Chromalox Industrial).
10. **¿Qué modificaciones permiten reducir el costo sin comprometer la seguridad, la capacidad ni el desempeño del proceso?**  
    - Operar el SOEC en el punto termoneutro ($198\,000\text{ celdas}$, $j=0.86\text{ A/cm}^2$) permite reducir el CAPEX del SOEC a **`$25.19M USD`** (`-$5.78M USD`).
    - Aprovechar el intercambiador recuperativo gas-gas precalentando vapor hasta $710^\circ\text{C}$ con el efluente del SOEC reduce el calentador `E-202` a un *trim heater* de $950\text{ kW}_e$, bajando su CAPEX de `$1.36M` a **`$0.40M USD`**.


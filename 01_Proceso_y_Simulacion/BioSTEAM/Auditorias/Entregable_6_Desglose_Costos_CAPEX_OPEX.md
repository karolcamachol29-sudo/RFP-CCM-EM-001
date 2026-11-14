# Entregable 6: Desglose Tecnoeconómico Auditado de Costos (CAPEX, OPEX y Análisis de Sensibilidad)

**Proyecto de Licitación:** `RFP-CCM-EM-001` — Planta de E-Metanol ($30\,000\text{ t/año}$) — Solvanta Engineering Solutions  
**Guía de Costos Original de Referencia:** `CAPEX_yOPEX.pdf` (*Estimación de Costos de Capital y Operación*, Dr. Jesús Andrés Arzola Flores — Basada en Turton, Bailie, Whiting, Shaeiwitz & Bhattacharyya, *Analysis, Synthesis, and Design of Chemical Processes*, Cap. 22 y Apéndice A: Método del Módulo Desnudo `CAPCOST`, $\text{CEPCI}_{2001} = 397$, actualizado a $\text{CEPCI}_{2024} = 800$).

---

## 1. Trazabilidad Bibliográfica con la Guía de Costos Original (`CAPEX_yOPEX.pdf`)

Para cada uno de los tres equipos se verificaron los diez puntos exigidos en el apartado 6.1 de la licitación:

| Criterio de Auditoría Económica | **Equipo 1: Electrolizador SOEC (`EL101`)** | **Equipo 2: Reactor Multitubular (`R401`)** | **Equipo 3: Calentador Eléctrico (`E202`)** |
| :--- | :--- | :--- | :--- |
| **1. Ecuación de costo utilizada** | Desglose modular bottom-up por componente: stacks cerámicos ($\text{USD/celda}$), recipientes presurizados a $20\text{ bar}$, rectificadores IGBT/SCR ($\text{USD/kW}_e$) y piping/manifold de alta temperatura. | $\log_{10} C_p^0 = K_1 + K_2 \log_{10}(A) + K_3 [\log_{10}(A)]^2$ para haces multitubulares + recipiente vertical de caldera + carga inicial de catalizador. | $\log_{10} C_p^0 = K_1 + K_2 \log_{10}(A) + K_3 [\log_{10}(A)]^2$ para haz de inmersión en U + sistema de potencia SCR/tiristores. |
| **2. Fuente bibliográfica y sección** | DOE Hydrogen Program Record #24005 (2024) / NREL SOEC Manufacturing Cost Model + Turton Apéndice A (`CAPEX_yOPEX.pdf`, diaps. 14–22) para factores de módulo de recipientes y electrónica. | `CAPEX_yOPEX.pdf`, diapositivas 15, 19, 20, 21 y 22 (Turton Tabla A.1: *Fixed tube sheet heat exchanger*, $K_1=4.3247, K_2=-0.3030, K_3=0.1634$; *Vertical process vessel*, $K_1=3.4974, K_2=0.4485, K_3=0.1074$). | `CAPEX_yOPEX.pdf`, diapositivas 15, 19, 20 y 22 (Turton Tabla A.1: *U-tube heat exchanger*, $K_1=4.1884, K_2=-0.2503, K_3=0.1974$) + módulo de control SCR industrial. |
| **3. Parámetros de diseño requeridos** | $N_{\text{celdas}}$ ($550\text{ cm}^2/\text{celda}$), $N_{\text{módulos}}$, $P_{\text{AC}}$ ($\text{kW}_e$). | Área de transferencia $A = 1\,526.83\text{ m}^2$, volumen de coraza $V = 32.04\text{ m}^3$, masa de catalizador $m_{\text{cat}} = 13\,110\text{ kg}$. | Área superficial de elementos $A = 200.11\text{ m}^2$ (a $q'' = 28.0\text{ kW/m}^2$) y potencia eléctrica $P_{\text{eléc}} = 5\,688.31\text{ kW}_e$. |
| **4. Unidades originales de la correlación** | $N_{\text{celdas}}$ adimensional, $P_{\text{AC}}$ en $\text{kW}_e$, costos en $\text{USD}_{2024}$. | Área $A$ en $\text{m}^2$, volumen $V$ en $\text{m}^3$, presión manométrica $P$ en $\text{barg}$. | Área $A$ en $\text{m}^2$, presión manométrica $P$ en $\text{barg}$, potencia en $\text{kW}_e$. |
| **5. Límites de aplicación de la correlación** | Celdas planares de $500\text{--}600\text{ cm}^2$; módulos de $1\text{--}5\text{ MW}_e$. | Tabla A.1: **$10\text{ m}^2 \le A \le 1\,000\text{ m}^2$**; recipiente vertical: **$0.3\text{ m}^3 \le V \le 520\text{ m}^3$**. Se divide $A = 1\,526.83\text{ m}^2$ en **$N_{\text{sub}} = 2$ haces de $763.41\text{ m}^2 \le 1\,000\text{ m}^2$**. | Tabla A.1: **$10\text{ m}^2 \le A \le 1\,000\text{ m}^2$**. Con $A = 200.11\text{ m}^2$, opera en el centro del rango válido ($N_{\text{sub}} = 1$). |
| **6. Factores de corrección ($F_P, F_M, F_{BM}$)** | Factores de módulo desnudo por subsistema: $F_{BM,\text{stack}} = 1.15$, $F_{BM,\text{vessels}} = 1.65$, $F_{BM,\text{power}} = 1.35$, $F_{BM,\text{bop}} = 1.55$ ($\overline{F}_{BM} = 1.3486$). | Haz: $F_P(74\text{ barg, solo tubos}) = 1.2429$ (Tabla A.2: $C_1=-0.00164, C_2=-0.00627, C_3=0.0123$), $F_M(\text{SS316/CS}) = 2.731$, $B_1=1.63, B_2=1.66 \implies F_{BM,\text{haz}} = 6.048$. Coraza: $F_{P,\text{vessel}}(19\text{ barg}) = 4.946$, $F_M = 1.0 \implies F_{BM,\text{coraza}} = 11.883$. | Haz Incoloy 800H: $F_P(19\text{ barg}) = 1.0504$, $F_M(\text{Ni-alloy/CS}) = 3.694$, $B_1=1.63, B_2=1.66 \implies F_{BM,\text{cuerpo}} = 8.071$. Gabinete SCR: $F_{BM,\text{SCR}} = 2.081$. |
| **7. Año base e índice económico** | Año base 2024 ($\text{CEPCI}_{2024} = 800$). | Año base Turton 2001 ($\text{CEPCI}_{2001} = 397$), actualizado a 2024 ($\text{CEPCI}_{2024} = 800$, factor $800/397 = 2.0151$). | Año base Turton 2001 ($\text{CEPCI}_{2001} = 397$), actualizado a 2024 ($\text{CEPCI}_{2024} = 800$, factor $2.0151$). |

---

## 2. Comparativa Antes y Después de la Auditoría de Costos (CAPEX)

| Equipo | Código | CAPEX Notebook Original (Erróneo) | Causa Raíz del Error en el Notebook Original | CAPEX Auditado y Corregido (`BioSTEAM`) | Reducción Absoluta (`USD`) | Reducción Relativa (`%`) |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **Electrolizador SOEC (Planta Completa — 352,660 celdas @ $j=0.4807\text{ A/cm}^2$)** | `EL101` | `$50,695,920.00` | Aplicó $F_{BM}=1.85$ sobre el costo ya instalado de `$27.40M USD` (doble contabilización de instalación y BoP) y mezcló escalas de celdas ($198\text{k}$) con flujo de planta ($901.7\text{ kmol/h}$). | **`$30,971,388.45`** | `-$19,724,531.55` | **`-38.91%`** |
| **Electrolizador SOEC (Réplica DWSIM — 198,000 celdas @ $j=0.8630\text{ A/cm}^2$)** | `EL101` | `$50,695,920.00` | Misma doble contabilización sobre $198\,000$ celdas. | **`$25,188,015.49`** | `-$25,507,904.51` | **`-50.32%`** |
| **Electrolizador SOEC (Benchmark Informe — 198,000 celdas @ $j=0.4800\text{ A/cm}^2$)** | `EL101` | `$50,695,920.00` | Misma doble contabilización para el módulo de $23.29\text{ MW}_e$ ($707.57\text{ kg/h H}_2$). | **`$17,308,687.21`** | `-$33,387,232.79` | **`-65.86%`** |
| **Reactor Multitubular de Metanol ($1\,526.83\text{ m}^2$, $75\text{ bar}$)** | `R401` | `$12,185,040.13` | Ecuación logarítmica apócrifa (`10**(4.15 + 0.58*log10(A))`, $5.3\times$ mayor que Turton), extrapolación fuera de $A_{\max}=1\,000\text{ m}^2$ y $F_P=2.45$ ($F_{BM}=8.448$). | **`$4,189,889.30`** | `-$7,995,150.83` | **`-65.61%`** |
| **Sobrecalentador Eléctrico de Vapor ($5\,603\text{ kW}$, $800^\circ\text{C}$)** | `E202` | `$6,822,917.01` | Usó correlación de horno petroquímico de fuego directo ($C_p^0 = \$1.233\text{M}$) con factor de campo $F_{BM}=5.534$ (`$1,259/kWe`). | **`$1,355,294.75`** | `-$5,467,622.26` | **`-80.14%`** |
| **SUMA DE LOS 3 EQUIPOS AUDITADOS (Escala Planta Completa)** | — | **`$69,703,877.14`** | — | **`$36,516,572.50`** | **`-$33,187,304.64`** | **`-47.61%`** |

---

## 3. Desglose Económico Detallado por Equipo (CAPEX y OPEX Anual)

Base de operación anual para OPEX: **$8\,000\text{ h/año}$** y tarifa eléctrica industrial renovable PPA de **$\$0.040/\text{kWh}$** ($\text{CEPCI}_{2024} = 800$).

### 3.1 Equipo 1: Electrolizador SOEC (`EL101` — Caso Planta Completa, $352\,660\text{ celdas}$, $41.91\text{ MW}_e\text{ AC}$)

#### A. Desglose de CAPEX
| Subsistema / Componente | Parámetro Base | Costo de Compra Desnudo $C_p^0$ (`USD 2024`) | Factor de Módulo Desnudo ($F_{BM}$) | Costo Instalado de Módulo Desnudo $C_{BM}$ (`USD 2024`) | Participación en $C_{BM}$ (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Stacks cerámicos SOEC ($\text{Ni-YSZ / 8YSZ / LSCF}$)** | $352\,660\text{ celdas} \times \$32.00/\text{celda}$ | `$11,285,120.00` | $1.150$ | `$12,977,888.00` | `41.90%` |
| **2. Envolventes presurizadas ($20\text{ bar}$, aislamiento interno)** | $14\text{ módulos} \times \$245\,000/\text{mód.}$ | `$3,430,000.00` | $1.650$ | `$5,659,500.00` | `18.27%` |
| **3. Electrónica de potencia (Rectificadores IGBT/SCR + Trafo)** | $41\,913.61\text{ kW}_e \times \$135.00/\text{kW}_e$ | `$5,658,337.05` | $1.350$ | `$7,638,755.01` | `24.66%` |
| **4. Balance de Planta Mecánico (Manifolds Incoloy 800H, control)** | $352\,660\text{ celdas} \times \$7.35/\text{celda}$ | `$2,591,631.90` | $1.550$ | `$4,017,029.45` | `12.97%` |
| **5. Instrumentación y lazos de seguridad ATEX ($\text{H}_2/\text{O}_2$)** | Integrado en BoP modular | *(Incluido en 2, 3 y 4)* | — | `$678,215.99` | `2.19%` |
| **TOTAL `EL101` (Planta Completa — 352,660 celdas)** | **$41.91\text{ MW}_e\text{ AC}$ ($1\,272.42\text{ kg/h H}_2$)** | **`$22,965,088.95`** | **$\overline{F}_{BM} = 1.3486$** | **`$30,971,388.45`** | **`100.00%`** |

*(Nota: Para el caso Benchmark de $198\,000\text{ celdas}$ a $23.29\text{ MW}_e$, $C_p^0 = \$12\,832\,920.21\text{ USD}$ y $C_{BM} = \$17\,308\,687.21\text{ USD}$; para la réplica DWSIM de $198\,000\text{ celdas}$ a $47.20\text{ MW}_e$, $C_p^0 = \$18\,691\,697.31\text{ USD}$ y $C_{BM} = \$25\,188\,015.49\text{ USD}$).*

#### B. Desglose de OPEX Anual (`EL101` — Planta Completa)
| Rubro de Costo Operativo Anual | Base de Cálculo | Costo Anual (`USD/año`) | Costo por $\text{kg H}_2$ (`USD/kg`) |
| :--- | :--- | :---: | :---: |
| **Consumo eléctrico AC ($41\,913.61\text{ kW}_e$)** | $41\,913.61\text{ kW} \times 8\,000\text{ h/año} \times \$0.040/\text{kWh}$ | `$13,412,354.48` | `$1.3176` |
| **Provisión anualizada reposición de stacks cerámicos** | Vida útil $40\,000\text{ h}$ ($5\text{ años}$), reposición al $60\%$ de $C_{p,\text{stacks}}^0 / 5$ | `$1,354,214.40` | `$0.1330` |
| **Mantenimiento preventivo BoP, instrumentación y válvulas** | $2.5\%$ anual sobre $C_{BM}$ excluyendo stacks | `$449,837.51` | `$0.0442` |
| **TOTAL OPEX ANUAL `EL101`** | **$10\,179\,399\text{ kg H}_2/\text{año}$** | **`$15,216,406.39`** | **`$1.4948`** |

---

### 3.2 Equipo 2: Reactor Multitubular de Síntesis de Metanol (`R401`)

#### A. Desglose de CAPEX
| Subsistema / Componente | Parámetro Base y Correlación Turton (`CAPEX_yOPEX.pdf`) | Costo de Compra Base $C_p^0$ (`USD 2024`) | Factores ($F_P, F_M, F_{BM}$) | Costo Instalado de Módulo Desnudo $C_{BM}$ (`USD 2024`) | Participación en $C_{BM}$ (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Haz multitubular de alta presión ($2\,126$ tubos BWG 14)** | $N_{\text{sub}}=2$ haces de $A_{\text{sub}} = 763.41\text{ m}^2 \le 1\,000\text{ m}^2$ (Tabla A.1: $K_1=4.3247, K_2=-0.3030, K_3=0.1634$) | `$378,015.88` | $F_P=1.2429$, $F_M=2.731$, $F_{BM}=6.048$ | `$2,286,256.37` | `54.57%` |
| **2. Coraza de caldera vertical y domo de vapor ($20\text{ bar}$)** | $V_{\text{coraza}} = 32.04\text{ m}^3$ ($D=2.61\text{ m}, L=6.0\text{ m}$; Tabla A.1: $K_1=3.4974, K_2=0.4485, K_3=0.1074$) | `$127,100.38` | $F_{P,\text{vessel}}=4.946$, $F_M=1.0$, $F_{BM}=11.883$ | `$1,510,332.93` | `36.05%` |
| **3. Carga inicial de catalizador comercial $\text{Cu/ZnO/Al}_2\text{O}_3$** | $V_{\text{cat}} = 11.50\text{ m}^3$, $\rho_{\text{lecho}} = 1\,140\text{ kg/m}^3 \implies m_{\text{cat}} = 13\,110\text{ kg} \times \$30.00/\text{kg}$ | `$393,300.00` *(a costo real)* | $F_{BM} = 1.000$ (inventario inicial) | `$393,300.00` | `9.39%` |
| **TOTAL `R401` (Reactor Multitubular)** | **$A = 1\,526.83\text{ m}^2$, $\dot{Q} = 1\,963.11\text{ kW}$, $30\,504\text{ t/año CH}_3\text{OH}$** | **`$695,726.07`** *(base CS + cat)* | **$\overline{F}_{BM} = 6.022$** | **`$4,189,889.30`** | **`100.00%`** |

#### B. Desglose de OPEX Anual y Crédito de Vapor (`R401`)
| Rubro Operativo Anual | Base de Cálculo | Flujo Económico Anual (`USD/año`) |
| :--- | :--- | :---: |
| **Reposición anualizada de catalizador $\text{Cu/ZnO/Al}_2\text{O}_3$** | Vida útil de $3\text{ años}$ ($24\,000\text{ h}$): $\$393\,300 / 3\text{ años}$ | `+$131,100.00` |
| **Mantenimiento mecánico e inspección de caldera de alta presión** | $3.0\%$ anual sobre $C_{BM,\text{mecánico}}$ ($\$3\,796\,589.30$) | `+$113,897.68` |
| **Crédito energético por generación de vapor MP ($20\text{ bar}$)** | $3.563\text{ t/h} \times 8\,000\text{ h/año} \times \$18.00/\text{t vapor}$ (integración interna con SOEC) | `-$513,064.80` *(crédito térmico)* |
| **OPEX Directo sin crédito de vapor** | — | **`$244,997.68/año`** |

---

### 3.3 Equipo 3: Sobrecalentador Eléctrico de Proceso (`E202`)

#### A. Desglose de CAPEX
| Subsistema / Componente | Parámetro Base y Correlación Turton (`CAPEX_yOPEX.pdf`) | Costo de Compra Base $C_p^0$ (`USD 2024`) | Factores ($F_P, F_M, F_{BM}$) | Costo Instalado de Módulo Desnudo $C_{BM}$ (`USD 2024`) | Participación en $C_{BM}$ (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Haz de inmersión eléctrico en Incoloy 800H + cuerpo a $20\text{ bar}$** | $A = 200.11\text{ m}^2$ ($q''=28\text{ kW/m}^2$; Tabla A.1 *U-tube*: $K_1=4.1884, K_2=-0.2503, K_3=0.1974$) | `$65,002.18` *(base CS)* | $F_P=1.0504$, $F_M=3.694$ (Incoloy 800H), $F_{BM}=8.071$ | `$524,621.92` | `38.71%` |
| **2. Sistema de potencia SCR/tiristores, transformador seco y barras** | $P_{\text{eléc}} = 5\,688.31\text{ kW}_e$ ($K_1=2.62, K_2=0.72$, escalado CEPCI 2024) | `$399,241.52` | $F_M=1.25$, $F_{BM}=2.081$ | `$830,672.83` | `61.29%` |
| **TOTAL `E202` (Sobrecalentador Eléctrico)** | **$\dot{Q}_{\text{útil}} = 5\,602.99\text{ kW}$, $P_{\text{eléc}} = 5\,688.31\text{ kW}_e$, $T_{\text{out}} = 800^\circ\text{C}$** | **`$464,243.70`** | **$\overline{F}_{BM} = 2.919$** | **`$1,355,294.75`** | **`100.00%`** |

#### B. Desglose de OPEX Anual (`E202`)
| Rubro de Costo Operativo Anual | Base de Cálculo | Costo Anual (`USD/año`) |
| :--- | :--- | :---: |
| **Consumo eléctrico de red ($5\,688.31\text{ kW}_e$)** | $5\,688.31\text{ kW}_e \times 8\,000\text{ h/año} \times \$0.040/\text{kWh}$ | `$1,820,259.65` |
| **Mantenimiento eléctrico y reposición de elementos radiantes** | $2.0\%$ anual sobre $C_{BM}$ (`$1,355,294.75`) | `$27,105.90` |
| **TOTAL OPEX ANUAL `E202`** | — | **`$1,847,365.55`** |

---

## 4. Análisis de Sensibilidad Económica y Operativa

### 4.1 Sensibilidad de `EL101` a la Densidad de Corriente ($j$) y Costo de Celda (Flujo Planta Completa: $1\,272.42\text{ kg/h H}_2$)

| Densidad de Corriente $j$ ($\text{A/cm}^2$) | Celdas Requeridas ($550\text{ cm}^2$) | Voltaje $V_{\text{celda}}$ ($\text{V}$) | Potencia AC $P_{\text{AC}}$ ($\text{MW}_e$) | $\text{SEC}_{\text{AC}}$ ($\text{kWh/kg H}_2$) | CAPEX Instalado $C_{BM}$ (`M USD`) | OPEX Eléctrico Anual @ $\$0.04/\text{kWh}$ (`M USD/año`) | Costo Anualizado Total ($\text{CAPEX}/10 + \text{OPEX}$, `M USD/año`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$0.350\text{ A/cm}^2$** | $484\,330$ | $1.142$ | $40.44$ | $31.78$ | `$40.82` | `$12.94` | `$18.88` |
| **$0.4807\text{ A/cm}^2$ (Óptimo Esc. D)** | **$352\,660$** | **$1.184$** | **$41.91$** | **$32.94$** | **`$30.97`** | **`$13.41`** | **`$18.31` (Mínimo Global)** |
| **$0.650\text{ A/cm}^2$** | $260\,810$ | $1.242$ | $43.98$ | $34.56$ | `$26.45` | `$14.07` | `$18.49` |
| **$0.8630\text{ A/cm}^2$ (Réplica 198k)** | $198\,000$ | $1.333$ | $47.20$ | $37.09$ | `$25.19` | `$15.10` | `$19.12` |

**Conclusión de ingeniería**: Operar en el punto óptimo del Escenario D ($j = 0.4807\text{ A/cm}^2$, $352\,660\text{ celdas}$) requiere `$5.78M USD` más de CAPEX inicial que forzar el flujo por $198\,000\text{ celdas}$ a $j = 0.8630\text{ A/cm}^2$, pero ahorra **`$1.69M USD/año`** en electricidad ($5.29\text{ MW}_e$ menos) y evita la degradación térmica acelerada por operar sobre el voltaje termoneutro, recuperando la inversión diferencial en solo **$3.4\text{ años}$**.


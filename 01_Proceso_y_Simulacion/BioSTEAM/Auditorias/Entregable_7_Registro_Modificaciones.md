# Entregable 7: Registro Trazable de Modificaciones (Celda por Celda y Función por Función)

**Proyecto de Licitación:** `RFP-CCM-EM-001` — Planta de E-Metanol ($30\,000\text{ t/año}$) — Solvanta Engineering Solutions  
**Archivo Original Conservado Intacto (Entregable 1):** `BioSTEAM_E_Metanol_Colab_ORIGINAL.ipynb`  
**Archivo Corregido y Validado (Entregable 2):** `BioSTEAM_E_Metanol_Colab_CORREGIDO.ipynb`

---

## 1. Mapa Comparativo de Arquitectura entre el Notebook Original y el Notebook Corregido

| Índice en Original | Contenido en `BioSTEAM_E_Metanol_Colab_ORIGINAL.ipynb` | Problemas Detectados en la Auditoría | Índice en Corregido | Contenido en `BioSTEAM_E_Metanol_Colab_CORREGIDO.ipynb` | Modificación Realizada y Justificación Técnica |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **Celda 0** *(Markdown)* | Título general del notebook. | Referencias ambiguas sin especificar independencia modular ni versión exacta de BioSTEAM. | **Celda 0** *(Markdown)* | Encabezado técnico de auditoría y arquitectura modular en BioSTEAM `v2.54.0`. | Documentación explícita del alcance (3 equipos independientes) y distinción entre diagrama nativo, modelo de simulación y modelo matemático. |
| **Celda 1** *(Código)* | Instalación de paquetes con `pip` y configuración de `SALIDA`. | Instalaba paquetes innecesarios en cada corrida sin verificar el entorno local. | **Celda 2** *(Código)* | Configuración del entorno, verificación de versiones (`biosteam 2.54.0`, `thermosteam 0.54.2`, `graphviz`) y función `crear_termodinamica_emetanol()`. | Función termodinámica reutilizable e independiente para que cada equipo pueda instanciar su propio paquete de propiedades sin depender de variables globales previas. |
| **Celda 2** *(Código)* | Definición global de `chemicals = bst.Chemicals(...)` en un único flowsheet compartido (`EMETHANOL_PLANT`). | Todos los equipos compartían el mismo flowsheet global, contaminando los diagramas de flujo. | **Celdas 4, 6, 8** *(Código)* | Tres flowsheets independientes: `flujo_soec`, `flujo_reactor` y `flujo_calentador`. | Garantiza el aislamiento total de corrientes, unidades y sistemas (`SYS_SOEC_EL101`, `SYS_REACTOR_R401`, `SYS_CALENTADOR_E202`). |
| **Celda 3** *(Código)* | Clase `SOEC_Unit(bst.Unit)`. | 1. Caja negra sin ecuaciones electroquímicas.<br>2. Asignaba `power_utility` en `_run()`.<br>3. Mezclaba $198\,000$ celdas ($j=0.48\text{ A/cm}^2$) con flujo de planta ($901.7\text{ kmol/h}$).<br>4. Multiplicaba el costo ya instalado (`$27.40M`) por `F_BM=1.85` (`$50.70M`). | **Celda 4** *(Código)* | Clase `SOECElectrolyzer(bst.Unit)` + función `simular_equipo_soec()`. | 1. Implementa modelo electroquímico completo (Nernst, Butler-Volmer, ASR Arrhenius, difusión Knudsen, $V_{tn}$).<br>2. Mueve utilidades a `_design()`.<br>3. Acopla Ley de Faraday ($352\,660$ celdas óptimas, $198\,000$ celdas réplica DWSIM y $198\,000$ celdas benchmark).<br>4. Corrige CAPEX desglosado (`$30.97M`, `$25.19M` y `$17.31M`). |
| **Celda 4** *(Código)* | Clases `HighTempElectricHeater(bst.Unit)` y `MethanolReactor(bst.Unit)`. | **En `MethanolReactor`**:<br>1. Conversión por paso imposible ($84.53\%$).<br>2. Calor fijo `3,385 kW` violando Primera Ley.<br>3. Costo `$12.19M` por ecuación apócrifa y extrapolación $A > 1\,000\text{ m}^2$.<br>**En `HighTempElectricHeater`**:<br>1. Asignaba `power_utility` en `_run()`.<br>2. Costo `$6.82M` usando correlación de horno de fuego directo. | **Celdas 6 y 8** *(Código)* | Clase `MultitubularBoilingWaterReactor(bst.Unit)` (Celda 6) y Clase `ElectricProcessHeater(bst.Unit)` (Celda 8). | **En `R401`**:<br>1. Usa `bst.Reaction` con $X_{\text{CO}_2}=26.40\%$ sobre gas con reciclo (`S-303`).<br>2. Acopla $\dot{Q}_{\text{rxn}} = 1\,963.11\text{ kW}$ con vaporización de BFW e incluye caída de presión de Ergun.<br>3. Divide $A=1\,526.83\text{ m}^2$ en 2 haces $\le 1\,000\text{ m}^2$ con Turton Tabla A.1 (`$4.19M`).<br>**En `E202`**:<br>1. Corrige $T_{\text{in}}=220^\circ\text{C}$.<br>2. Costea haz Incoloy 800H + gabinete SCR (`$1.36M`). |
| **Celda 5** *(Código)* | Instanciación de corrientes y creación de `SOEC_TRAIN` (`[E202, EL101]` acoplados) y `REACTOR_SYS` (`[R401]`). | Violaba el requisito de independencia al unir `E202` y `EL101` en `SOEC_TRAIN`, e ingresaba corrientes erróneas en `E202` ($250^\circ\text{C}$) y `R401` (sin reciclo). | **Celdas 5, 7, 9** *(Código)* | Ejecución independiente de `SYS_SOEC_EL101` (Celda 5), `SYS_REACTOR_R401` (Celda 7) y `SYS_CALENTADOR_E202` (Celda 9). | Cada equipo tiene su propia celda de ejecución, tabla de corrientes, balance de masa/energía, desglose de costos y diagrama nativo de BioSTEAM. |
| **Celdas 7, 8 y 15** *(Código)* | Funciones `dibujar_esquema_ingenieria()` y `generar_pfd_profesional()` con `graphviz.Digraph` manual. | Dibujaban cajas HTML y elipses manuales que simulaban ser diagramas de proceso pero no provenían de BioSTEAM. | *(Eliminadas y reemplazadas en Celdas 5, 7, 9)* | Llamadas exclusivas a `unidad.diagram()` y `sistema.diagram(kind='thorough')` nativos de BioSTEAM. | Cumplimiento estricto del apartado 3 y 4: cero bibliotecas gráficas externas para fingir diagramas de BioSTEAM. |
| **Celda 9** *(Código)* | Intento fallido de `sist.diagram(file=str(SALIDA / f"{sist.ID}.png"), format="png")`. | Lanzaba `ValueError: cannot specify format extension; file already has format extension` en `biosteam.digraph.save_digraph`. | **Celdas 5, 7, 9** *(Código)* | `sist.diagram(kind='thorough', file=str(DIRECTORIO_SALIDA / nombre_sin_extension), format='png')`. | Pasa la ruta sin extensión junto con `format='png'` y `format='svg'`, generando los 12 archivos nativos sin ningún `RuntimeWarning`. |
| **Celdas 10–14** *(Código)* | Exportación de tablas parciales con valores erróneos de CAPEX (`$69.70M` suma). | Arrastraba los errores de costos, balances y escalas. | **Celdas 11 y 13** *(Código)* | Suite automatizada de 10 pruebas de validación, tablas comparativas DWSIM vs. BioSTEAM, auditoría CAPEX/OPEX y exportación CSV/JSON. | Verificación integral reproducible con `assert` en todas las leyes de conservación y restricciones de diseño. |

---

## 2. Detalle de Modificaciones por Método en las Clases `bst.Unit`

### 2.1 Clase `SOECElectrolyzer` (reemplaza a `SOEC_Unit`)
- **Atributos de clase BioSTEAM**:
  - Antes: `_N_ins = 1`, `_N_outs = 2`, sin declaración formal de `_units`.
  - Ahora: `_N_ins = 1`, `_N_outs = 2`, diccionario formal `_units` con 18 variables ingenieriles tipadas para integración nativa con `design_results`.
- **Método `_run(self)`**:
  - Antes: calculaba fracciones másicas manualmente, modificaba `self.power_utility.consumption` dentro de `_run()` (provocando `RuntimeWarning` de BioSTEAM) y no empleaba `bst.Reaction`.
  - Ahora: instancia `self.reaccion_electrolisis = bst.Reaction('Water -> Hydrogen + 0.5 O2', reactant='Water', X=self.conversion_vapor)`, la aplica sobre la corriente en condiciones de operación ($770^\circ\text{C}, 20\text{ bar}$) y separa estequiométricamente el gas catódico (`outs[0]`) y el oxígeno anódico (`outs[1]`), sin tocar `power_utility`.
- **Método `_design(self)`**:
  - Antes: fijaba `Area_total_m2 = 198000 * 0.055` sin verificar si $198\,000\text{ celdas}$ a $j=0.480\text{ A/cm}^2$ podían producir el flujo de $\text{H}_2$ de `outs[0]`.
  - Ahora: calcula la corriente total de Faraday $I_{\text{tot}} = 2 F \dot{n}_{\text{H}_2}$, dimensiona el número de módulos/stacks/celdas (en modo `'escalar_celdas'`) o la densidad de corriente resultante (en modo `'celdas_fijas'`), evalúa $\Delta H^\circ(T)$, $\Delta G^\circ(T)$, $V_{tn}(T)$, $E_{\text{Nernst}}$, $\eta_{\text{ohm}}$, $\eta_{\text{act}}$, $\eta_{\text{conc}}$, $V_{\text{celda}}$, $P_{\text{DC}}$, $P_{\text{AC}}$, $\dot{Q}_{\text{térmico}}$ y registra `self.power_utility(P_AC_kW)`.
- **Método `_cost(self)`**:
  - Antes: `self.baseline_purchase_cost['Stacks SOEC + BoP'] = 198000 * 138.40` (`$27.40M`) y `self.F_BM['Stacks SOEC + BoP'] = 1.85` (`$50.70M`).
  - Ahora: desglosa `Stacks ceramicos SOEC` ($F_{BM}=1.15$), `Envolventes presurizadas 20bar` ($F_{BM}=1.65$), `Rectificadores IGBT/SCR y trafo` ($F_{BM}=1.35$) y `Piping alta T Incoloy y control` ($F_{BM}=1.55$) usando costos de compra desnudos auditados.

### 2.2 Clase `MultitubularBoilingWaterReactor` (reemplaza a `MethanolReactor`)
- **Método `_run(self)`**:
  - Antes: restaba `n_rxn = 118.34 kmol/h` directamente a una alimentación de $140\text{ kmol/h}$ de $\text{CO}_2$ ($X = 84.53\%$) y fijaba un flujo arbitrario de agua de enfriamiento de $6\,600\text{ kg/h}$.
  - Ahora: aplica `bst.Reaction('CO2 + 3Hydrogen -> Methanol + Water', reactant='CO2', X=0.2640)` sobre la corriente `S-303` ($450.758\text{ kmol/h CO}_2$, $1\,374.811\text{ kmol/h H}_2$), calcula la caída de presión de Ergun en los $2\,126$ tubos catalíticos ($\Delta P = 0.0886\text{ bar}$) y ajusta el flujo de BFW saturado a $20\text{ bar}$ ($3\,562.95\text{ kg/h}$) para que el calor latente de vaporización en la coraza iguale exactamente el calor liberado por la reacción ($\dot{Q}_{\text{rxn}} = 1\,963.11\text{ kW}$).
- **Método `_design(self)`**:
  - Antes: asignaba `duty_kW = 3385.0` fijo.
  - Ahora: extrae $\dot{Q}_{\text{rxn}} = H_{\text{in,gas}} - H_{\text{out,gas}} = 1\,963.11\text{ kW}$, verifica la transferencia de calor ($\Delta T_{\text{lm}} = 32.62\text{ K}$, $U_{\text{req}} = 39.42\text{ W/m}^2\text{K} \le U_{\text{disp}} = 185\text{ W/m}^2\text{K}$), calcula $\text{GHSV} = 3\,616\text{ h}^{-1}$, dimensiones de coraza ($D_s = 2.61\text{ m}, V_s = 32.04\text{ m}^3$) y masa de catalizador ($13\,110\text{ kg}$).
- **Método `_cost(self)`**:
  - Antes: `C_p0_2001 = 10**(4.15 + 0.58 * np.log10(1526.83))` y `F_BM = 1.63 + 1.66 * 2.75 * 2.45 = 12.81` / `8.448` (`$12.19M`).
  - Ahora: divide $A = 1\,526.83\text{ m}^2$ en $N_{\text{sub}} = 2$ haces de $763.41\text{ m}^2 \le 1\,000\text{ m}^2$, aplica los coeficientes exactos de Turton Tabla A.1 ($K_1=4.3247, K_2=-0.3030, K_3=0.1634$), Tabla A.2 ($F_P=1.2429$) y Tabla A.3 ($F_M=2.731$), y suma la envolvente vertical de caldera a $19\text{ barg}$ más el inventario inicial de catalizador (`$4.19M` total instalado).

### 2.3 Clase `ElectricProcessHeater` (reemplaza a `HighTempElectricHeater`)
- **Método `_run(self)`**:
  - Antes: calentaba desde $250^\circ\text{C}$ hasta $800^\circ\text{C}$ sin caída de presión y asignaba `power_utility` dentro de `_run()`.
  - Ahora: calienta la corriente desde $220.0^\circ\text{C}$ ($493.15\text{ K}$, condición exacta de `S-203` en DWSIM) hasta $800.0^\circ\text{C}$ con $\Delta P = 0.20\text{ bar}$ ($P_{\text{out}} = 19.80\text{ bar}$), dejando el registro eléctrico para `_design()`.
- **Método `_design(self)`**:
  - Ahora: calcula $\dot{Q}_{\text{útil}} = 5\,602.99\text{ kW}$, $P_{\text{eléc}} = \dot{Q}_{\text{útil}} / 0.985 = 5\,688.31\text{ kW}_e$, dimensiona el área de elementos de Incoloy 800H ($A = 200.11\text{ m}^2$ a $q'' = 28.0\text{ kW/m}^2$), verifica la temperatura superficial de vaina ($T_{s,\max} = 893.3^\circ\text{C} < 950^\circ\text{C}$) y registra `self.power_utility(5688.31)`.
- **Método `_cost(self)`**:
  - Antes: usaba correlación de horno de combustión directa con $F_{BM} = 5.534$ (`$6.82M`).
  - Ahora: costea el haz tubular en U de Incoloy 800H con Turton Tabla A.1 ($K_1=4.1884, K_2=-0.2503, K_3=0.1974$, $F_M=3.694, F_P=1.0504$) y el gabinete de potencia SCR/tiristores (`$1.36M` total instalado).


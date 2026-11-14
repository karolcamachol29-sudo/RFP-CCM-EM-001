# Matriz Ponderada de Selección Técnica — MP-02: Ruta de Síntesis de e-Metanol (RFP-CCM-EM-001)

> **Proyecto:** Planta de Producción de e-Metanol a partir de CO2 y H2 Verde (46,300 kg/h de Metanol)  
> **Consorcio:** Solvanta S.A. de C.V.  
> **Código Documental:** `MP-02_DOC_MatrizPonderada_SintesisMetanol_v1.0`  
> **Fecha:** 2026-09-10  

---

## 1. Objeto del Análisis
Determinar la ruta termoquímica de reacción y el diseño del reactor químico para convertir $CO_2$ capturado e hidrógeno verde en e-metanol grado refinado, cumpliendo con la capacidad nominal de 46.3 t/h.

---

## 2. Alternativas Evaluadas
* **Opción A: Hidrogenación Catalítica Directa de $CO_2$ ($CO_2 + 3H_2 \leftrightarrow CH_3OH + H_2O$):** Reactor multitubular lecho fijo tipo Lurgi ($R-401$) refrigerado por agua en ebullición en la coraza, catalizador comercial $Cu/ZnO/Al_2O_3$, $250^\circ\text{C}$ y 50 bar.
* **Opción B: Bi-reforming de Gas Natural con $CO_2$ y Vapor:** Generación intermedia de gas de síntesis ($CO + H_2 + CO_2$) seguida de síntesis convencional de metanol.
* **Opción C: Gasificación de Residuos Agroindustriales / Biomasa:** Gasificación de biomasa para producir syngas con enriquecimiento de $H_2$ electrolítico.

---

## 3. Matriz de Comparación Ponderada

| ID | Criterio de Evaluación | Peso (%) | Opción A: Hidrogenación Directa | Opción A (Pond.) | Opción B: Bi-reforming | Opción B (Pond.) | Opción C: Gasificación | Opción C (Pond.) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | **Neutralidad de Carbono y Cumplimiento Estricto RFP** | 30% | 5 | 1.50 | 2 | 0.60 | 3 | 0.90 |
| **C2** | **Selectividad a Metanol y Supresión de Subproductos** | 20% | 5 | 1.00 | 4 | 0.80 | 3 | 0.60 |
| **C3** | **Evacuación de Calor Exotérmico y Seguridad Térmica** | 20% | 4 | 0.80 | 3 | 0.60 | 2 | 0.40 |
| **C4** | **CAPEX del Sistema de Reacción y Compresores** | 15% | 4 | 0.60 | 3 | 0.45 | 2 | 0.30 |
| **C5** | **Convergencia y Precisión en DWSIM / BioSTEAM** | 15% | 5 | 0.75 | 3 | 0.45 | 2 | 0.30 |
| **TOTAL**| | **100%** | — | **4.65** | — | **2.90** | — | **2.50** |

---

## 4. Conclusión y Dictamen Técnico
* **Opción Seleccionada:** **Opción A — Hidrogenación Catalítica Directa de $CO_2$ en Reactor Multitubular PFR**
* **Puntaje Ponderado Obtenido:** **4.65 / 5.00**
* **Justificación de Ingeniería:** La hidrogenación directa garantiza emisiones netas cero de gases de efecto invernadero (alcances 1 y 2), cumple al 100% las especificaciones de licitación y aprovecha al máximo la selectividad del catalizador $Cu/ZnO/Al_2O_3$ (>99.5% hacia metanol en el ciclo de reciclo), evitando el uso de gas natural fósil.
* **Evaluadores Responsables:**
  - **Gildardo Ocaña Barrales** — Ingeniería de Procesos / DTI / P&ID.
  - **Paulina Mota Macip** — Simulación / Instrumentación y Control.

# Matriz Ponderada de Selección Técnica — MP-01: Tecnología de Electrólisis (RFP-CCM-EM-001)

> **Proyecto:** Planta de Producción de e-Metanol a partir de CO2 y H2 Verde (46,300 kg/h de Metanol)  
> **Consorcio:** Solvanta S.A. de C.V.  
> **Código Documental:** `MP-01_DOC_MatrizPonderada_Electrolisis_v1.0`  
> **Fecha:** 2026-09-08  

---

## 1. Objeto del Análisis
Seleccionar la tecnología de electrólisis de agua óptima para el suministro continuo de **5,830 kg/h de Hidrógeno Verde ($H_2$)** requerido como reactivo estequiométrico en la planta de e-Metanol, maximizando la eficiencia energética global mediante la integración térmica de calor residual de reacción.

---

## 2. Alternativas Evaluadas
* **Opción A: Electrólisis de Óxido Sólido (SOEC - Solid Oxide Electrolysis Cell):** Operación a alta temperatura ($750^\circ\text{C}$, 20 bar), electrólito cerámico de circonia estabilizada con itria (YSZ). Aprovecha vapor de alta entalpía generado en el enfriamiento del reactor de metanol.
* **Opción B: Membrana de Intercambio Protónico (PEM):** Operación a baja temperatura ($60 - 80^\circ\text{C}$), electrólito polimérico de Nafion, electrodos de metales nobles (Pt/Ir). Excelente respuesta dinámica ante renovables.
* **Opción C: Electrólisis Alcalina Convencional (AEL):** Operación a baja temperatura ($70 - 90^\circ\text{C}$), solución de KOH al 30% p/p, diafragma poroso. Tecnología ampliamente madura en la industria.

---

## 3. Matriz de Comparación Ponderada

| ID | Criterio de Evaluación | Peso (%) | Opción A: SOEC (Alta T) | Opción A (Pond.) | Opción B: PEM | Opción B (Pond.) | Opción C: AEL (Alcalina) | Opción C (Pond.) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | **Eficiencia Energética y Exergética (kWh/kg $H_2$)** | 30% | 5 | 1.50 | 4 | 1.20 | 3 | 0.90 |
| **C2** | **Integración Térmica con Calor de Reacción de Metanol** | 25% | 5 | 1.25 | 2 | 0.50 | 1 | 0.25 |
| **C3** | **Costo Nivelado de Hidrógeno (LCOH / OPEX Eléctrico)** | 20% | 4 | 0.80 | 3 | 0.60 | 4 | 0.80 |
| **C4** | **Madurez Tecnológica y Confiabilidad (TRL)** | 10% | 3 | 0.30 | 5 | 0.50 | 5 | 0.50 |
| **C5** | **Huella de Espacio (Footprint) y Modularidad** | 10% | 4 | 0.40 | 5 | 0.50 | 3 | 0.30 |
| **C6** | **Rigor de Modelado y Simulación en Python/BioSTEAM** | 5% | 5 | 0.25 | 4 | 0.20 | 3 | 0.15 |
| **TOTAL**| | **100%** | — | **4.50** | — | **3.50** | — | **2.90** |

*Escala: 1 = Muy Desfavorable, 2 = Desfavorable, 3 = Aceptable, 4 = Favorable, 5 = Altamente Favorable.*

---

## 4. Conclusión y Dictamen Técnico
* **Opción Seleccionada:** **Opción A — Electrólisis de Óxido Sólido (SOEC)**
* **Puntaje Ponderado Obtenido:** **4.50 / 5.00**
* **Justificación de Ingeniería:** La tecnología SOEC disminuye el consumo de energía eléctrica específica de $50\text{ kWh/kg }H_2$ (PEM/AEL) a solo $37.5\text{ kWh/kg }H_2$ gracias al aprovechamiento del vapor sobrecalentado generado por la fuerte exotermicidad de la reacción de síntesis de metanol en $R-401$. Esto reduce el OPEX anual de electricidad en más del 24% y viabiliza la rentabilidad del proyecto Solvanta.
* **Evaluadores Responsables:**
  - **Karol Paola Camacho López** — Dirección del Proyecto / Ingeniera de Optimización de Procesos (Python).
  - **Gildardo Ocaña Barrales** — Ingeniería de Procesos / DTI / P&ID.

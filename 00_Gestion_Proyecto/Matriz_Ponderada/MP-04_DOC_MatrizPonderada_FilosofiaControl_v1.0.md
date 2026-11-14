# Matriz Ponderada de Selección Técnica — MP-04: Filosofía de Control e Instrumentación (RFP-CCM-EM-001)

> **Proyecto:** Planta de Producción de e-Metanol a partir de CO2 y H2 Verde (46,300 kg/h de Metanol)  
> **Consorcio:** Solvanta S.A. de C.V.  
> **Código Documental:** `MP-04_DOC_MatrizPonderada_FilosofiaControl_v1.0`  
> **Fecha:** 2026-09-15  

---

## 1. Objeto del Análisis
Definir la arquitectura de automatización, lazos de control regulatorio y sistemas instrumentados de seguridad (SIS) para garantizar la estabilidad operativa del reactor $R-401$, compresores $K-501$ y columna $C-501$.

---

## 2. Alternativas Evaluadas
* **Opción A: Control Jerárquico Multivariable con Lazos Cascada y SIS Independiente (FC-01):** Control de temperatura de reacción mediante cascada TIC-401 sobre flujo de agua de enfriamiento; control de presión en bucle con PIC-501 en split-range; lazo de nivel LIC-501 en V-501; sistema de paro de emergencia SIL-2/SIL-3.
* **Opción B: Lazos Descentralizados SISO Clásicos:** PIDs individuales sin desacoplamiento ni lazos en cascada.
* **Opción C: Control Predictivo Basado en Modelos (MPC) en la Nube:** Algoritmo de control predictivo centralizado en servidor externo con optimizador económico en tiempo real (RTO).

---

## 3. Matriz de Comparación Ponderada

| ID | Criterio de Evaluación | Peso (%) | Opción A: Jerárquico Cascada | Opción A (Pond.) | Opción B: SISO Simple | Opción B (Pond.) | Opción C: MPC en Nube | Opción C (Pond.) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | **Seguridad de Proceso y Prevención de Runaway Térmico** | 30% | 5 | 1.50 | 2 | 0.60 | 4 | 1.20 |
| **C2** | **Estabilidad Operativa ante Rampas de Carga del SOEC** | 25% | 5 | 1.25 | 3 | 0.75 | 4 | 1.00 |
| **C3** | **Cumplimiento Normativo (ISA 5.1 / IEC 61508 / IEC 61511)** | 20% | 5 | 1.00 | 3 | 0.60 | 3 | 0.60 |
| **C4** | **Confiabilidad e Independencia de Redes Externas** | 15% | 5 | 0.75 | 5 | 0.75 | 2 | 0.30 |
| **C5** | **Costo de Hardware DCS y Facilidad de Mantenimiento** | 10% | 4 | 0.40 | 5 | 0.50 | 2 | 0.20 |
| **TOTAL**| | **100%** | — | **4.90** | — | **3.20** | — | **3.30** |

---

## 4. Conclusión y Dictamen Técnico
* **Opción Seleccionada:** **Opción A — Arquitectura de Control Jerárquico con Lazos en Cascada y SIS Integrado (FC-01)**
* **Puntaje Ponderado Obtenido:** **4.90 / 5.00**
* **Justificación de Ingeniería:** Elimina el riesgo de embalamiento térmico en el reactor exotérmico de síntesis y garantiza máxima tolerancia a fallos conforme a las recomendaciones del análisis HAZOP (AC-HAZOP-01). Es una solución probada en la industria petroquímica que no depende de conectividad externa para salvaguardar vidas y activos.
* **Evaluadores Responsables:**
  - **Paulina Mota Macip** — Instrumentación y Control / Simulación.
  - **Gildardo Ocaña Barrales** — DTI / P&ID / Ingeniería de Procesos.

# MATRIZ DE TRAZABILIDAD INTEGRAL DE ACTIVIDADES — RFP-CCM-EM-001
**Proyecto:** Planta de Producción de e-Metanol Grado AA (30,000 t/año)  
**Consorcio:** Solvanta Engineering Solutions S.A. de C.V.  
**Licitación:** RFP-CCM-EM-001 (FIQ - BUAP / DPyPQ)  
**Fecha de Consolidación:** 14 de Noviembre de 2026  
**Responsable:** Karol Paola Camacho López (@Karoc) — Dirección del Proyecto  

---

## 1. Cadena de Precedencia y Maduración Técnica Documental

El proyecto `RFP-CCM-EM-001` sigue una rigurosa secuencia de maduración documental donde cada entregable deriva directamente de los datos validados del hito anterior, garantizando cero discrepancias numéricas:

```
[E0: Acta Constitutiva] ➔ Fundación jurídica e identidad corporativa Solvanta
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
[E1.1: Bases de Diseño]                   [E1.4: Video Pitch Oficial]
Capacidad (30,000 t/año), normas          4 Segmentos: Karol, Gildardo, Paulina, Grecia
         │                                          │
         ├──────────────────────────────────────────┘
         ▼
[E1.2: Simulación DWSIM] ➔ Balances de materia y energía convergidos (Peng-Robinson / NRTL)
         │
         ▼
[E1.3: Diagramación Plant 3D] ➔ BFD y PFD preliminar de 5 áreas de proceso
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
[E1.3.1: Propuesta Equipos EQ-01]         [RT-01: Revisión Técnica 01]
Pre-dimensionamiento paramétrico          Defensa Bases, NB-01 y BFD v0 (Sesión 4)
         │                                          │
         ├──────────────────────────────────────────┘
         ▼
[MP-00: Matrices Ponderadas MP01-05] ➔ Decisiones: SOEC, Lurgi, Flash+C501, Cascada, Cangrejera
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
[E1.5: Verificación VTP-01]               [E1.6: Matriz Ambiental]
TC-01, TE-01 y DFP v1                     AC-AMB-01 (SEMARNAT / NOM)
         │
         ▼
[E2.1: Lista de Equipos LE-01] ➔ 28 equipos calibrados a 20 bar
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
[FC-01: Filosofía de Control]             [RT-02: Revisión Técnica 02]
28 lazos primarios y cascadas             Diapositivas oficiales (4 expositores)
         │
         ▼
[DTI v0.1 / v0.2 / v1] ➔ Tuberías, válvulas de control e instrumentación ISA-5.1
         │
         ▼
[AC-HAZOP-01: Seguridad] ➔ 42 desviaciones, matriz interbloqueos MI-01 y MCE-01
         │
         ▼
[PIB-01: Paquete Ing. Básica] ➔ Expediente integrador de ingeniería de proceso
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
[E4.1 - E4.7: Suite Auditorías BioSTEAM / SOEC]  [DIF-01: Cartel PyDay]
Paquete soec_optimization/ (Python)       Excepción: Karol & Grecia
         │
         ▼
[RT-03: Defensa Final y Guía Maestra] ➔ Presentación oficial en diapositivas (19 pág)
         │
         ▼
[EF: Informe Final de Licitación] ➔ Expediente Maestro (Tomos I a V) y cierre de oferta
```

---

## 2. Matriz de Trazabilidad Actividad ➔ Responsable ➔ Evidencia ➔ Entregable

| Código | Actividad Específica | Responsable | Cargo Desempeñado | Archivo / Evidencia Primaria | Entregable Final Resultante | Estado |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **E0-01** | Redacción de estatutos y objeto social | Karol Camacho | Dirección del Proyecto | Minuta notarial de acuerdos | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E0-02** | Organigrama y alcance de ingeniería de procesos | Gildardo Ocaña | Ingeniería de Procesos | Especificación de áreas operativas | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E0-03** | Infraestructura de simulación y control | Paulina Mota | Simulación / Control | Selección de DWSIM y plataformas | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E0-04** | Protocolos HSE y presupuesto inicial | Grecia Figueroa | Seguridad HSE / Economía | Marco corporativo de seguridad | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E1.1-01**| Compilación de normas ASTM D1152 e ISO | Grecia Figueroa | Especialista en HSE | `Referencias_y_Bases/Actividades/` | `E1.1_DOC_BasesDiseno_v1.0.pdf` | ✅ Finalizado |
| **E1.1-02**| Especificación de capacidad (30,000 t/a) y pureza | Gildardo Ocaña | Ingeniería de Procesos | Balances estequiométricos NB-01 | `E1.1_DOC_BasesDiseno_v1.0.pdf` | ✅ Finalizado |
| **E1.1-03**| Paquete termodinámico Peng-Robinson/NRTL | Paulina Mota | Simulación | Envolventes de fase preliminares | `E1.1_DOC_BasesDiseno_v1.0.pdf` | ✅ Finalizado |
| **E1.1-04**| Integración de bases y supervisión técnica | Karol Camacho | Dirección del Proyecto | Verificación RFP-CCM-EM-001 | `E1.1_DOC_BasesDiseno_v1.0.pdf` | ✅ Finalizado |
| **E1.2-01**| Configuración termodinámica DWSIM | Paulina Mota | Simulación | `DWSIM_v1_APROBADA_Solvanta.dwxml` | `E1.2_DOC_ReporteSimulacion_v1.0.pdf` | ✅ Finalizado |
| **E1.2-02**| Balances de materia por componente | Gildardo Ocaña | Ingeniería de Procesos | Tabulación de corrientes molares | `E1.2_DOC_ReporteSimulacion_v1.0.pdf` | ✅ Finalizado |
| **E1.2-03**| Auditoría de venteos y purgas (HSE) | Grecia Figueroa | Especialista en HSE | Verificación de emisiones CO2/H2 | `E1.2_DOC_ReporteSimulacion_v1.0.pdf` | ✅ Finalizado |
| **E1.2-04**| Análisis de sensibilidad en Python y LHS | Karol Camacho | Optimización Python | Scripts `analisis_sensibilidad.py` | `E1.2_DOC_ReporteSimulacion_v1.0.pdf` | ✅ Finalizado |
| **E1.3-01**| Modelado vectorial de BFD y PFD en Plant 3D | Gildardo Ocaña | DTI / P&ID / Ing. Procesos | Planos CAD Plant 3D 2025 | `E1.3_DOC_EspecificacionDiagramas_v1.0.pdf` | ✅ Finalizado |
| **E1.3-02**| Traspaso de P, T y caudales desde DWSIM | Paulina Mota | Simulación | Tablas de datos en corrientes | `E1.3_DOC_EspecificacionDiagramas_v1.0.pdf` | ✅ Finalizado |
| **E1.3-03**| Marcado de zonas de venteo y seguridad HSE | Grecia Figueroa | Especialista en HSE | Delimitación de áreas de riesgo | `E1.3_DOC_EspecificacionDiagramas_v1.0.pdf` | ✅ Finalizado |
| **E1.3-04**| Control de calidad de planos y nomenclatura | Karol Camacho | Dirección del Proyecto | Verificación de rotulación ASME | `E1.3_DOC_EspecificacionDiagramas_v1.0.pdf` | ✅ Finalizado |
| **E1.3.1-01**| Dimensionamiento mecánico preliminar de recipientes | Gildardo Ocaña | Ingeniería de Procesos | Cálculos ASME Sección VIII | `E1.3.1_DOC_PropuestaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E1.3.1-02**| Cargas térmicas y flujos extremos de DWSIM | Paulina Mota | Simulación | Hojas de datos de intercambiadores | `E1.3.1_DOC_PropuestaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E1.3.1-03**| Selección de aleaciones y prevención H2 | Grecia Figueroa | Especialista en HSE | Metalurgia de Acero Inox 316L | `E1.3.1_DOC_PropuestaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E1.3.1-04**| Script generador paramétrico en Python EQ-01 | Karol Camacho | Optimización Python | Algoritmo de hojas técnicas | `E1.3.1_DOC_PropuestaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E1.4-01**| Segmento 1: Introducción, Solvanta y Optimización | Karol Camacho | Dirección / Optimización Py | Video grabado y locución oficial | `E1.4_VID_EnlacePitch_v1.0.pdf` | ✅ Finalizado |
| **E1.4-02**| Segmento 2: Arquitectura del Proceso y Síntesis | Gildardo Ocaña | Ingeniería de Procesos / DTI | Video grabado y demostración P&ID | `E1.4_VID_EnlacePitch_v1.0.pdf` | ✅ Finalizado |
| **E1.4-03**| Segmento 3: Simulación DWSIM y Control | Paulina Mota | Simulación / Control | Video grabado y pantalla DWSIM | `E1.4_VID_EnlacePitch_v1.0.pdf` | ✅ Finalizado |
| **E1.4-04**| Segmento 4: Sostenibilidad, Riesgos y Economía | Grecia Figueroa | Seguridad HSE / Economía | Video grabado y métricas verdes | `E1.4_VID_EnlacePitch_v1.0.pdf` | ✅ Finalizado |
| **E1.4-05**| Montaje audiovisual, postproducción y ficha PDF | Karol Camacho | Dirección del Proyecto | Master 1080p en Google Drive | `E1.4_VID_EnlacePitch_v1.0.pdf` | ✅ Finalizado |
| **RT-01-01**| Presentación de diapositivas RT-01 (AR-01) | Los 4 Integrantes | Cargos respectivos en defensa | `Solvanta_Act4_v0.0.pdf` | `RT-01_DOC_PresentacionDiapositivas_v1.0.pdf`| ✅ Finalizado |
| **MP-00-01**| Compendio de Matrices Ponderadas MP-01 a MP-05 | Los 4 Integrantes | Cargos respectivos en selección | Compendio foliado con RACI | `MP-00_DOC_CompendioMatricesPonderadas_v1.0.pdf`| ✅ Finalizado |
| **E1.5-01**| Verificación de equilibrios ELV en flash V-501 | Paulina Mota | Simulación | Comparativa Peng-Robinson / NRTL | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.5-02**| Balances de materia y tablas TC-01 / TE-01 | Gildardo Ocaña | Ingeniería de Procesos | `Tablas/TC-01_Solvanta.xlsx`, `TE-01` | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.5-03**| Evaluación de emisiones fugitivas en flash | Grecia Figueroa | Especialista en HSE | Análisis toxicológico de venteos | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.5-04**| Script Python de verificación y DFP v1 | Karol Camacho | Optimización Python / Dir. | Compilación LaTeX de 23 páginas | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.6-01**| Matriz de aspectos e impactos Leopold/Conesa | Grecia Figueroa | Especialista en HSE | `AC-AMB-01_XLSX_MatrizAmbiental_v1.0.xlsx` | `E1.6_DOC_MatrizAmbiental_v1.0.pdf` | ✅ Finalizado |
| **E1.6-02**| Inventario de efluentes y emisiones de proceso | Gildardo Ocaña | Ingeniería de Procesos | Datos de corrientes del DFP | `E1.6_DOC_MatrizAmbiental_v1.0.pdf` | ✅ Finalizado |
| **E1.6-03**| Consumos energéticos y huella térmica DWSIM | Paulina Mota | Simulación | Balances de energía en servicios | `E1.6_DOC_MatrizAmbiental_v1.0.pdf` | ✅ Finalizado |
| **E1.6-04**| Análisis de ciclo de vida preliminar y cierre | Karol Camacho | Dirección del Proyecto | Supervisión contra NOMs SEMARNAT | `E1.6_DOC_MatrizAmbiental_v1.0.pdf` | ✅ Finalizado |
| **E2.1-01**| Hojas de datos mecánicos de 28 equipos LE-01 | Gildardo Ocaña | Ingeniería de Procesos | Catálogo dimensional de equipos | `E2.1_DOC_ListaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E2.1-02**| Calibración de potencias y condensadores | Paulina Mota | Simulación | Cargas térmicas a 20 bar | `E2.1_DOC_ListaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E2.1-03**| Clasificación de áreas Clase I Div 1/2 | Grecia Figueroa | Seguridad HSE / Economía | Evaluación eléctrica de seguridad | `E2.1_DOC_ListaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E2.1-04**| Generación automatizada de catálogo en LaTeX | Karol Camacho | Optimización Python / Dir. | Script de cotejo y maquetación | `E2.1_DOC_ListaEquipos_v1.0.pdf` | ✅ Finalizado |
| **RT-02-01**| Diapositivas oficiales de avance RT-02 | Los 4 Integrantes | Expositores (reparto 23-27%) | 21 láminas foliadas con RACI | `RT-02_DOC_PresentacionDiapositivas_v1.0.pdf`| ✅ Finalizado |
| **E2.2-01** | Video oficial de sustentación RT-02 en Canva | Los 4 Integrantes (Líder: Karol C.) | Expositores / Dirección | Video HD en Canva y ficha foliada con RACI | `E2.2_VID_EnlaceRevisionTecnica02_v1.0.pdf`| ✅ Finalizado |
| **FC-01-01**| Lazos de control cascada TIC-101 y regulación | Paulina Mota | Instrumentación y Control | Arquitectura de bucles PID | `FC-01_DOC_FilosofiaControl_v1.0.pdf` | ✅ Finalizado |
| **FC-01-02**| Conexiones de instrumentos en planos DTI | Gildardo Ocaña | DTI / P&ID / Ing. Procesos | Simbología ANSI/ISA-5.1 en planos | `FC-01_DOC_FilosofiaControl_v1.0.pdf` | ✅ Finalizado |
| **FC-01-03**| Capas de protección IPL, ESD y SIS SIL-2 | Grecia Figueroa | Especialista en HSE | Matriz de interbloqueos de seguridad | `FC-01_DOC_FilosofiaControl_v1.0.pdf` | ✅ Finalizado |
| **FC-01-04**| Optimización de sintonía dinámica en Python | Karol Camacho | Optimización Python / Dir. | Validación de estabilidad operativa | `FC-01_DOC_FilosofiaControl_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-01**| Facilitación del taller de nodos 1 a 6 | Grecia Figueroa | Especialista en HSE | `Solvanta_AC-HAZOP-01_HAZOP.xlsx` | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-02**| Trazado de límites de nodos en planos DTI | Gildardo Ocaña | Custodio del DTI / P&ID | Marcado sobre DTI v0.2 | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-03**| Modelado de sobrepresión y fuga térmica DWSIM | Paulina Mota | Simulación / Control | Simulación de escenarios críticos | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-04**| Matriz Causa-Efecto MCE-01 y recomendaciones | Karol Camacho & Grecia F.| Dirección / Seguridad HSE | 42 desviaciones y 34 acciones | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-01**| Memorias de cálculo y planos DTI v1 integrados | Gildardo Ocaña | Ingeniería de Procesos / DTI | Paquete de ingeniería Plant 3D | `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-02**| Balances de materia y energía extendidos | Paulina Mota | Simulación / Control | Cuaderno de balance global | `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-03**| Manual de operación segura y plan contingencias | Grecia Figueroa | Especialista en HSE | Protocolos de arranque y paro | `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-04**| Dirección ejecutiva y maquetación de 47 pág | Karol Camacho | Dirección del Proyecto | Expediente técnico en LaTeX | `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **E4.1-01** | Modelado económico CAPEX/OPEX en BioSTEAM | Grecia Figueroa & Karol C.| Evaluación Económica / Python | Simulación tecno-económica | `E4.1_RPT_AuditoriaEconomicaIntegral_v1.0.pdf` | ✅ Finalizado |
| **E4.2-01** | Cotejo riguroso DWSIM vs BioSTEAM | Paulina Mota & Karol C.| Simulación / Optimización Py | Validación cruzada de balances | `E4.2_RPT_ComparativaDWSIMvsBioSTEAM_v1.0.pdf` | ✅ Finalizado |
| **E4.3-01** | Desglose analítico de factores de Guthrie | Grecia Figueroa & Karol C.| Evaluación Económica / Dirección | Desglose de inversión y activos | `E4.3_RPT_DesgloseCostosCAPEXOPEX_v1.0.pdf` | ✅ Finalizado |
| **E4.4-01** | Registro histórico de desviaciones y cambios | Gildardo Ocaña & Karol C.| Ingeniería de Procesos / Dir. | Trazabilidad de reingeniería | `E4.4_RPT_RegistroModificaciones_v1.0.pdf` | ✅ Finalizado |
| **E4.5-01** | Segunda auditoría y recalibración de LCOMe | Grecia Figueroa & Karol C.| Evaluación Económica / Python | Sensibilidad eléctrica 20-60 USD | `E4.5_RPT_SegundaAuditoriaBioSTEAM_v1.0.pdf` | ✅ Finalizado |
| **E4.6-01** | Modelado numérico SOEC Butler-Volmer Python | Karol Camacho | Ingeniera de Optimización (Py) | Paquete `soec_optimization/` | `E4.6_RPT_AuditoriaOptimizacionSOEC_v1.0.pdf` | ✅ Finalizado |
| **E4.7-01** | Banco de 12 pruebas unitarias automatizadas | Karol Camacho & Paulina M.| Optimización Python / Sim. | Batería de tests con `pytest` | `E4.7_RPT_ValidacionPruebasSOEC_v1.0.pdf` | ✅ Finalizado |
| **DIF-01-01**| Modelado SOEC, curvas Pareto y diseño gráfico | Karol Camacho | Optimización Python / Dir. | Cartel técnico PyDay BUAP | `DIF-01_DOC_CartelPyDay_v1.0.pdf` | ✅ Finalizado |
| **DIF-01-02**| Métricas de descarbonización y economía verde | Grecia Figueroa | Evaluación Económica / HSE | Resumen tecno-económico cartel | `DIF-01_DOC_CartelPyDay_v1.0.pdf` | ✅ Finalizado |
| **RT-03-01**| Diapositivas de defensa técnica final (19 láminas)| Los 4 Integrantes | Expositores multidisciplinarios | Set de diapositivas foliado | `RT-03_DOC_PresentacionDiapositivas_v1.0.pdf`| ✅ Finalizado |
| **E3.1-01** | Video oficial de defensa maestra RT-03 en Canva | Los 4 Integrantes (Líder: Karol C.) | Expositores / Dirección | Video HD en Canva y ficha foliada con RACI | `E3.1_VID_EnlaceRevisionTecnica03_v1.0.pdf`| ✅ Finalizado |
| **EF-01** | Tomo I: Bases de Diseño y Gobernanza | Karol Camacho | Dirección del Proyecto | Integración institucional | `EF_Informe_Final/` | ⏳ En proceso |
| **EF-02** | Tomo II: Memorias de Proceso y Planos Plant 3D | Gildardo Ocaña | Ingeniería de Procesos / DTI | Planos y memorias mecánicas | `EF_Informe_Final/` | ⏳ En proceso |
| **EF-03** | Tomo III: Balances DWSIM y Control de Proceso | Paulina Mota | Simulación / Control | Simulación y filosofía de control | `EF_Informe_Final/` | ⏳ En proceso |
| **EF-04** | Tomo IV: Expediente HAZOP, HSE y Economía | Grecia Figueroa | Especialista en HSE / Economía | Riesgos y rentabilidad financiera | `EF_Informe_Final/` | ⏳ En proceso |
| **EF-05** | Tomo V: Auditorías Python y Optimización SOEC | Karol Camacho | Ingeniera de Optimización (Py) | Código fuente y algoritmos | `EF_Informe_Final/` | ⏳ En proceso |
| **EF-06** | Compilación, autocontrol y dictamen final | Karol Camacho | Dirección del Proyecto | Cierre de expediente licitatorio | `EF_Informe_Final/` | ⏳ En proceso |

---

## 3. Registro Histórico de Incidencias y Acciones de Mitigación

1. **Incidencia E0: Archivo Corrupto de 2 Bytes en Git:**
   - *Hallazgo:* `03_Entregables_Finales/E0_Constitucion/E0_DOC_ActaConstitutiva_v0.2.pdf` pesaba 2 bytes (`\n\n`) en el repositorio.
   - *Trazabilidad de corrección:* Se rastreó la copia local auténtica de 4,281,422 bytes (4.08 MB) protocolizada notarialmente y se promovió oficialmente como `E0_DOC_ActaConstitutiva_v1.0.pdf`. El archivo dañado fue archivado en el histórico.
2. **Incidencia E1.5 / E2.1: Identificación de Equipo E-301:**
   - *Hallazgo:* Discrepancia en la nomenclatura del precalentador de gas de síntesis (etiquetado preliminarmente como E-101 en algunas memorias frente a E-301 en DWSIM).
   - *Trazabilidad de corrección:* Commits `b627fd2` y `546425c` del 18 de septiembre de 2026 unificaron oficialmente la designación a **E-301**, actualizando DWSIM, tablas de corriente y plano DFP v1.
3. **Incidencia FC-01: Sobrediseño en Columnas de Alarmas:**
   - *Hallazgo:* Inclusión de alarmas complejas redundantes contrarias a la guía docente en la versión preliminar de Filosofía de Control.
   - *Trazabilidad de corrección:* Commit `96953fb` del 06 de octubre de 2026 suprimió la sobreingeniería de alarmas, reenfocando el documento en las estrategias de control primario, cascada y protección esencial.
4. **Excepción de Participación en Cartel PyDay (DIF-01):**
   - *Principio de Veracidad Documental:* Únicamente las ingenieras **Karol Paola Camacho López** y **Grecia Figueroa Rincón** participaron en la programación, cálculo y diseño del cartel. Queda expresamente asentado en la matriz RACI individual y general que los integrantes Gildardo Ocaña y Paulina Mota figuraron como Informados (I).
5. **Gobernanza de Guiones Orales de Revisión Técnica (RT-02 y RT-03):**
   - *Políticas de Confidencialidad de Bidding:* Los guiones de locución y speeches cronometrados de defensa oral fueron excluidos de GitHub y resguardados en el directorio privado local `00_Documentos_Internos_Equipo/Guiones_Speech_Defensa/`. En el repositorio público de GitHub se publican exclusivamente las presentaciones oficiales en diapositivas en formato PDF foliado con marca de agua y hoja RACI.

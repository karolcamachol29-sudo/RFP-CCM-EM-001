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
         ▼
[E1.1: Bases de Diseño] ➔ Capacidad (30,000 t/año), especificación de reactivos y normas
         │
         ▼
[E1.2: Simulación DWSIM] ➔ Balances de materia y energía convergidos (Peng-Robinson / NRTL)
         │
         ▼
[E1.3: Diagramación Plant 3D] ➔ BFD y PFD preliminar de 5 áreas de proceso
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
28 lazos primarios y cascadas             Speech 6:28 min (4 expositores)
         │
         ▼
[DTI v0.1 / v0.2] ➔ Tuberías, válvulas de control e instrumentación ISA-5.1
         │
         ▼
[AC-HAZOP-01: Seguridad] ➔ 42 desviaciones, matriz interbloqueos MI-01 y MCE-01
         │
         ▼
[PIB-01: Paquete Ing. Básica] ➔ Expediente integrador de ingeniería de proceso
         │
         ├──────────────────────────────────────────┐
         ▼                                          ▼
[E4: Auditorías BioSTEAM / SOEC]          [DIF-01: Cartel PyDay]
Paquete soec_optimization/ (Python)       Excepción: Karol & Grecia
         │
         ▼
[RT-03: Defensa Final y Guía Maestra] ➔ Speech 10 min, Q&A y memorias
         │
         ▼
[EF: Informe Final de Licitación] ➔ Consolidación y cierre de oferta
```

---

## 2. Matriz de Trazabilidad Actividad ➔ Responsable ➔ Evidencia ➔ Entregable

| Código | Actividad Específica | Responsable | Cargo Desempeñado | Archivo / Evidencia Primaria | Entregable Final Resultante | Estado |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **E0-01** | Redacción de estatutos y objeto social | Karol Camacho | Dirección del Proyecto | Minuta notarial de acuerdos | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E0-02** | Diseño de logotipo e identidad Solvanta | Karol Camacho | Dirección del Proyecto | `02_Ingenieria_y_Diagramas/Recursos_Graficos/Logos/` | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E0-03** | Protocolización y firma de los 4 socios | Los 4 Integrantes | Socios Fundadores | Acta constitutiva firmada (4.08 MB) | `E0_DOC_ActaConstitutiva_v1.0.pdf` | ✅ Finalizado |
| **E1.1-01**| Compilación de normas ASTM D1152 e ISO | Grecia Figueroa | Especialista en HSE | `Referencias_y_Bases/Actividades/` | `E1.1_DOC_BasesDiseno_v1.0.pdf` | ✅ Finalizado |
| **E1.1-02**| Especificación de pureza de e-metanol | Grecia Figueroa | Especialista en HSE | Tablas de especificación técnica | `E1.1_DOC_BasesDiseno_v1.0.pdf` | ✅ Finalizado |
| **E1.2-01**| Configuración termodinámica DWSIM | Paulina Mota | Simulación | `DWSIM_v1_APROBADA_Solvanta.dwxml` | `E1.2_DOC_ReporteSimulacion_v1.0.pdf` | ✅ Finalizado |
| **E1.2-02**| Convergencia de reciclo y destilación | Paulina Mota | Simulación | `E1.2_SIM_Balances_v1.0.dwxmz` | `E1.2_DOC_ReporteSimulacion_v1.0.pdf` | ✅ Finalizado |
| **E1.3-01**| Modelado 3D de diagramas de bloques BFD | Gildardo Ocaña | Ingeniería de Procesos | `02_Ingenieria_y_Diagramas/BFD/` | `E1.3_DOC_EspecificacionDiagramas_v1.0.pdf` | ✅ Finalizado |
| **E1.3-02**| Trazado de diagrama PFD en Plant 3D | Gildardo Ocaña | DTI / P&ID | `02_Ingenieria_y_Diagramas/DFP_PFD/` | `E1.3_DOC_EspecificacionDiagramas_v1.0.pdf` | ✅ Finalizado |
| **E1.3.1-01**| Dimensionamiento paramétrico de equipos | Karol Camacho | Ingeniera de Optimización (Py) | Scripts matemáticos de cálculo | `E1.3.1_DOC_PropuestaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E1.4-01**| Elaboración de guion y grabación pitch | Karol Camacho | Dirección del Proyecto | Grabación de video y enlace Drive | `E1.4_VID_EnlacePitch_v1.0.txt` | ✅ Finalizado |
| **E1.5-01**| Verificación de equilibrios ELV en flash | Karol Camacho | Ingeniera de Optimización (Py) | `Memoria_Calculo_Balance_Flash_V501.pdf` | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.5-02**| Tablas de corrientes TC-01 y equipos TE-01| Paulina Mota | Simulación | `Tablas/TC-01_Solvanta.xlsx`, `TE-01.xlsx` | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.5-03**| Exportación vectorial DFP v1 Rev. 1 | Gildardo Ocaña | Ingeniería de Procesos | `DFP-v1_Solvanta.pdf` (AutoCAD Plant 3D) | `E1.5_DOC_ActividadVTP_v1.0.pdf` | ✅ Finalizado |
| **E1.6-01**| Matriz de aspectos e impactos ambientales | Grecia Figueroa | Especialista en HSE | `AC-AMB-01_XLSX_MatrizAmbiental_v1.0.xlsx` | `E1.6_DOC_MatrizAmbiental_v1.0.pdf` | ✅ Finalizado |
| **E2.1-01**| Inventario técnico de los 28 equipos | Paulina Mota | Simulación | Tabulación de datos de simulación DWSIM | `E2.1_DOC_ListaEquipos_v1.0.pdf` | ✅ Finalizado |
| **E2.1-02**| Redacción y maquetación LaTeX LE-01 | Karol Camacho | Ingeniera de Optimización (Py) | `Lista_Equipos/E2.1_DOC_ListaEquipos_v1.0.tex`| `E2.1_DOC_ListaEquipos_v1.0.pdf` | ✅ Finalizado |
| **FC-01-01**| Formulación de los 28 lazos de control | Paulina Mota | Instrumentación y Control | `Filosofia_Control/FC-01_...tex` | `FC-01_DOC_FilosofiaControl_v1.0.pdf` | ✅ Finalizado |
| **FC-01-02**| Control en cascada R-401 y compresores | Paulina Mota & Karol C.| Inst. Control / Optimización Py | Lazos AIC-FIC y PIC en DTI v0.1 | `FC-01_DOC_FilosofiaControl_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-01**| Delimitación de nodos en DTI v0.2 | Gildardo Ocaña | Custodio del DTI / Procesos | `figuras/dti_v0_2.pdf` rotulado | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-02**| Taller multidisciplinario (42 desviaciones)| Todo el consorcio | Roles del taller formal | `Solvanta_AC-HAZOP-01_HAZOP.xlsx` | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **HAZOP-03**| Catálogo MCE-01 y salvaguardas simples | Grecia Figueroa | Especialista en HSE | `Solvanta_MCE-01_Rev1.xlsx` | `AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-01**| Planos de arreglo general e implantación | Gildardo Ocaña | Ingeniería de Procesos | Memorias descriptivas de implantación | `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-02**| Maquetación del paquete básico PIB-01 | Karol Camacho | Dirección del Proyecto | `PIB_Paquete_.../Solvanta_PIB-01_Expediente.tex`| `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **PIB-01-03**| Revisión técnica independiente PIB-01 | Paulina Mota | Simulación / Inst. Control | Dictamen técnico formal de carátula | `PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf` | ✅ Finalizado |
| **RT-02-01**| Preparación de diapositivas RT-02 | Todo el consorcio | Expositores (reparto 23-27%) | Diapositivas Canva / PowerPoint | `RT-02_DOC_PresentacionDiapositivas_v1.0.pdf`| ✅ Finalizado |
| **RT-02-02**| Guion de locución cronometrado (6:28 min) | Todo el consorcio | Expositores | `RT-02_DOC_GuionOficialSpeech_v1.0.pdf` | `RT-02_DOC_GuionOficialSpeech_v1.0.pdf` | ✅ Finalizado |
| **RT-03-01**| Guía Maestra de Defensa y Banco Q&A | Karol Camacho & Grecia F.| Dirección / Evaluación Económica | `Guia_Maestra_Defensa_Speech_...pdf` | `RT-03_DOC_GuiaMaestraDefensaSpeech_v1.0.pdf`| ✅ Finalizado |
| **RT-03-02**| Diapositivas de defensa técnica final | Karol Camacho & Grecia F.| Dirección / Evaluación Económica | `RT-03_DOC_PresentacionDiapositivas_v1.0.pdf`| `RT-03_DOC_PresentacionDiapositivas_v1.0.pdf`| ✅ Finalizado |
| **DIF-01-01**| Modelado SOEC y análisis OAT/LHS/Morris | Karol Camacho | Ingeniera de Optimización (Py) | Scripts `sensitivity.py` y curvas Pareto | `DIF-01_DOC_CartelPyDay_v1.0.pdf` | ✅ Finalizado |
| **DIF-01-02**| Modelado económico BioSTEAM y LCOMe | Grecia Figueroa | Evaluación Económica | Módulos de costeo y corrida económica | `DIF-01_DOC_CartelPyDay_v1.0.pdf` | ✅ Finalizado |
| **DIF-01-03**| Diseño y maquetación del Cartel PyDay | Karol Camacho | Ingeniera de Optimización (Py) | Archivo vectorial de gran escala | `DIF-01_DOC_CartelPyDay_v1.0.pdf` | ✅ Finalizado |
| **E4-01** | Desarrollo de paquete `soec_optimization/` | Karol Camacho | Ingeniera de Optimización (Py) | Módulos `cell_model.py`, `degradation.py` | `E4.6_RPT_AuditoriaOptimizacionSOEC_v1.0.md`| ✅ Finalizado |
| **E4-02** | Auditoría tecno-económica BioSTEAM | Karol Camacho & Grecia F.| Optimización / Evaluación Económica | `Auditoria_Economica_Integral_BioSTEAM.xlsx`| `E4.1_RPT_AuditoriaEconomicaIntegral_v1.0.md`| ✅ Finalizado |
| **E4-03** | Redacción de reportes E4.1 a E4.7 | Karol Camacho | Ingeniera de Optimización (Py) | Reportes técnicos en Markdown | `E4.1` a `E4.7` en `03_Entregables_Finales/` | ✅ Finalizado |
| **EF-01** | Consolidación y auditoría de autocontrol | Karol Camacho | Dirección del Proyecto | Sistema CI/CD GitHub y bitácoras | `EF_Informe_Final/` | ⏳ En proceso |

---

## 3. Registro Histórico de Incidencias y Acciones de Mitigación

1. **Incidencia E0: Archivo Corrupto de 2 Bytes en Git:**
   - *Hallazgo:* `03_Entregables_Finales/E0_Constitucion/E0_DOC_ActaConstitutiva_v0.2.pdf` pesaba 2 bytes (`\n\n`) en el repositorio.
   - *Trazabilidad de corrección:* Se rastreó la copia local auténtica de 4,281,422 bytes (4.08 MB) protocolizada notarialmente y se promovió oficialmente como `E0_DOC_ActaConstitutiva_v1.0.pdf`. El archivo dañado fue archivado en `_auxiliar/versiones_previas_incompletas/`.
2. **Incidencia E1.5 / E2.1: Identificación de Equipo E-301:**
   - *Hallazgo:* Discrepancia en la nomenclatura del precalentador de gas de síntesis (etiquetado preliminarmente como E-101 en algunas memorias frente a E-301 en DWSIM).
   - *Trazabilidad de corrección:* Commits `b627fd2` y `546425c` del 18 de septiembre de 2026 unificaron oficialmente la designación a **E-301**, actualizando DWSIM, tablas de corriente y plano DFP v1.
3. **Incidencia FC-01: Sobrediseño en Columnas de Alarmas:**
   - *Hallazgo:* Inclusión de alarmas complejas redundantes contrarias a la guía docente en la versión preliminar de Filosofía de Control.
   - *Trazabilidad de corrección:* Commit `96953fb` del 06 de octubre de 2026 suprimió la sobreingeniería de alarmas, reenfocando el documento en las estrategias de control primario, cascada y protección esencial.
4. **Excepción de Participación en Cartel PyDay (DIF-01):**
   - *Principio de Veracidad Documental:* Únicamente las ingenieras **Karol Paola Camacho López** y **Grecia Figueroa Rincón** participaron en la programación, cálculo y diseño del cartel. Queda expresamente asentado en la matriz RACI individual y general que los integrantes Gildardo Ocaña y Paulina Mota figuraron como Informados (I).

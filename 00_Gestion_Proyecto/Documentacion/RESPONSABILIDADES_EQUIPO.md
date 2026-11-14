# ASIGNACIÓN OFICIAL DE RESPONSABILIDADES Y ESTRUCTURA DEL EQUIPO
**Proyecto:** Licitación Internacional RFP-CCM-EM-001 — Planta de Producción de e-Metanol Grado Químico AA (30,000 t/año)  
**Consorcio Contratista:** Solvanta Engineering Solutions S.A. de C.V.  
**Entidad Convocante:** Benemérita Universidad Autónoma de Puebla (BUAP) — FIQ / DPyPQ  
**Fecha de Emisión Oficial:** 14 de Noviembre de 2026  
**Dirección Documental:** Karol Paola Camacho López (@Karoc) — Dirección de Proyecto  

---

## 1. Integrantes Oficiales y Asignación Dual de Cargos

En cumplimiento con los requerimientos contractuales y metodológicos de la cátedra de Diseño de Procesos y Productos Químicos (DPyPQ) y las bases de licitación, cada uno de los cuatro socios y profesionales de **Solvanta Engineering Solutions S.A. de C.V.** ejerce **dos cargos oficiales de ingeniería**, respondiendo por áreas funcionales y técnicas complementarias a lo largo de todo el ciclo de vida del proyecto:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           CONSORCIO SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.                  │
│                                           DIRECCIÓN GENERAL                                      │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│      GILDARDO OCAÑA BARRALES   │       PAULINA MOTA MACIP       │      GRECIA FIGUEROA RINCÓN    │
│  1. Ingeniería de Procesos     │  1. Simulación                 │  1. Especialista en Seguridad, │
│  2. DTI / P&ID                 │  2. Instrumentación y Control  │     Salud y Medio Ambiente     │
│                                │                                │  2. Evaluación Económica       │
├────────────────────────────────┴────────────────────────────────┴────────────────────────────────┤
│                                  KAROL PAOLA CAMACHO LÓPEZ                                       │
│                              1. Dirección del Proyecto                                           │
│                              2. Ingeniera de Optimización de Procesos (Python)                   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Ficha Técnica Individual por Integrante

#### 1. Gildardo Ocaña Barrales (`@GildardoOca25`)
* **Cargo Oficial 1:** **Ingeniería de Procesos**
  - *Competencias y Alcance:* Conceptualización de balances de materia y energía en diagramas de flujo de proceso (DFP/PFD), delimitación de límites de batería (BL) de las seis áreas de la planta, cálculo de especificaciones mecánicas de equipos mayores, tuberías y servicios industriales auxiliares (vapor, agua de enfriamiento, nitrógeno, purga).
* **Cargo Oficial 2:** **DTI / P&ID**
  - *Competencias y Alcance:* Modelado tridimensional y desarrollo de planos de ingeniería en **AutoCAD Plant 3D 2025**, codificación estandarizada de líneas de tubería conforme a normas ASME/ANSI, representación gráfica de simbología ISA-5.1 para instrumentos, válvulas de control y enclavamientos de seguridad en el Diagrama de Tubería e Instrumentación (DTI/P&ID).

#### 2. Paulina Mota Macip (`@paulina145`)
* **Cargo Oficial 1:** **Simulación**
  - *Competencias y Alcance:* Modelado riguroso secuencial-modular y simultáneo en el simulador de procesos **DWSIM**, selección y parametrización de paquetes termodinámicos de alta presión (Peng-Robinson y NRTL-RK), convergencia de reciclos cerrados de síntesis (Área 400 y 500), simulación rigurosa de columnas de destilación fraccionada (T-601) y reactores catalíticos multitubulares (R-401).
* **Cargo Oficial 2:** **Instrumentación y Control**
  - *Competencias y Alcance:* Diseño y formulación de estrategias de control automático de procesos, selección de variables controladas ($CV$), manipuladas ($MV$) y perturbaciones ($DV$), estructuración de lazos de control por retroalimentación y lazos en cascada (temperatura-ebullición en R-401, nivel-caudal en V-601/V-801, presión en compresores C-301/C-501), y redacción de la Filosofía de Control (FC-01).

#### 3. Grecia Figueroa Rincón (`@Cho0bb`)
* **Cargo Oficial 1:** **Especialista en Seguridad, Salud y Medio Ambiente (HSE)**
  - *Competencias y Alcance:* Análisis de identificación sistemática de peligros industriales, liderazgo en la facilitación del estudio de Análisis de Peligros y Operabilidad (**HAZOP**), formulación de la Matriz de Causa-Efecto (MCE-01) y matriz de interbloqueos de seguridad (MI-01), evaluación de consecuencias ambientales y redacción de la Matriz de Requisitos e Impactos Ambientales (AC-AMB-01 / E1.6) bajo normativas SEMARNAT y NOMs vigentes.
* **Cargo Oficial 2:** **Evaluación Económica**
  - *Competencias y Alcance:* Modelado tecno-económico y estimación de costos de capital (**CAPEX**) y costos operativos (**OPEX**) mediante la plataforma en Python **BioSTEAM**, dimensionamiento de equipos para costeo, análisis de costo nivelado de producción de e-metanol (**LCOMe**), análisis de flujo de caja descontado, TIR, VPN y valor residual de activos.

#### 4. Karol Paola Camacho López (`@Karoc`)
* **Cargo Oficial 1:** **Dirección del Proyecto**
  - *Competencias y Alcance:* Dirección ejecutiva y metodológica del consorcio licitatorio, interlocución técnica institucional ante la convocante (BUAP / DPyPQ), administración del repositorio GitHub, orquestación de integración documental, gestión del control de versiones (CI/CD, GitHub Actions), auditoría de autocontrol de calidad documental y rendición final de cuentas de todos los entregables ante dictamen (Accountable general).
* **Cargo Oficial 2:** **Ingeniera de Optimización de Procesos (Python)**
  - *Competencias y Alcance:* Modelado electroquímico riguroso y optimización matemática en Python del electrolizador de óxido sólido (**SOEC**, celda `EL-201`), sustitución de scripts simplificados por termodinámica NIST y Butler-Volmer, acoplamiento térmico SOEC-Reactor, análisis de sensibilidad multivariable (OAT, Hipercubo Latino LHS, Morris), resolución de inconsistencias en suites de simulación y desarrollo de utilidades de compilación de ingeniería.

---

## 2. Criterio de Participación y Filosofía de Gobernanza

### 2.1 Autoría Colectiva vs. Distribución Específica del Trabajo
El proyecto licitatorio `RFP-CCM-EM-001` constituye una obra de ingeniería colegiada desarrollada por el consorcio **Solvanta Engineering Solutions S.A. de C.V.**. Por lo tanto:
1. **Autoría Institucional Colectiva:** Todos los entregables oficiales de ingeniería representan el consenso técnico de los cuatro integrantes, quienes respaldan solidariamente la integridad de la planta diseñada.
2. **Distribución Específica de Responsabilidades:** No todos los integrantes ejecutaron cada línea de código, plano o cálculo. La asignación documental debe reflejar la **actividad técnica real** que cada integrante desempeñó según su especialidad técnica. Atribuir la ejecución indiscriminada de cada documento a los cuatro integrantes desvirtúa la trazabilidad técnica y la auditoría documental exigida por las normas ISO 9001 e IEC 61882.

### 2.2 Excepción Específica Obligatoria: Cartel de Difusión PyDay (DIF-01)
> [!IMPORTANT]
> **Excepción de Participación en el Cartel:**  
> En la elaboración, modelado numérico, redacción técnica, diseño gráfico y presentación del cartel institucional para el congreso académico **PyDay Puebla** (`DIF-01_DOC_CartelPyDay_v1.0.pdf`), **participaron exclusivamente:**
> - **Ing. Karol Paola Camacho López** (Programación Python, optimización SOEC, análisis de sensibilidad y renderizado gráfico).
> - **Ing. Grecia Figueroa Rincón** (Evaluación económica en BioSTEAM, LCOMe y redacción de conclusiones tecno-económicas).
>
> Los integrantes Gildardo Ocaña Barrales y Paulina Mota Macip no formaron parte del equipo de redacción ni de diseño del cartel, figurando únicamente informados del evento en su calidad de socios de la firma.

---

## 3. Matriz de Roles y Liderazgo por Entregable Oficial y Secciones

| Entregable | Denominación Oficial | Integrante Responsable de Ejecución (R) | Cargo Oficial Desempeñado | Integrante Aprobador (A) | Cargo de Aprobación |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **E0** | Acta Constitutiva y Constitución de Empresa | Todo el Consorcio (Líder: Karol Camacho) | Dirección / Cargos respectivos | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.1** | Bases de Diseño y Marco Normativo (NB-01) | Grecia Figueroa Rincón | Especialista en HSE | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.2** | Simulación DWSIM y Balances de Proceso | Paulina Mota Macip | Simulación | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.3** | Diagramación (BFD, PFD) en Plant 3D | Gildardo Ocaña Barrales | Ingeniería de Procesos / DTI | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.3.1**| Propuesta Preliminar de Equipos (EQ-01) | Karol Paola Camacho López | Ingeniera de Optimización (Python) | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.4** | Video Pitch Oficial (4 Segmentos Grabados) | Todo el Consorcio (Los 4 Expositores) | Cargos respectivos en pantalla | Karol Paola Camacho López | Dirección del Proyecto |
| **RT-01** | Revisión Técnica 01: Defensa Bases (AR-01) | Todo el Consorcio (Los 4 Expositores) | Cargos respectivos en defensa | Karol Paola Camacho López | Dirección del Proyecto |
| **MP-00** | Compendio de Matrices Ponderadas (MP01-05)| Todo el Consorcio (Líder: Karol Camacho) | Dirección / Cargos respectivos | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.5** | Verificación Termodinámica VTP-01 y DFP v1 | Paulina Mota / Gildardo Ocaña / Karol Camacho | Simulación / Ing. Procesos / Python | Karol Paola Camacho López | Dirección del Proyecto |
| **E1.6** | Matriz de Impacto Ambiental (AC-AMB-01) | Grecia Figueroa Rincón | Especialista en HSE | Karol Paola Camacho López | Dirección del Proyecto |
| **E2.1** | Lista Maestra de Equipos LE-01 y DFP v1 | Gildardo Ocaña / Paulina Mota / Karol Camacho | Ing. Procesos / Simulación / Python | Karol Paola Camacho López | Dirección del Proyecto |
| **RT-02** | Revisión Técnica 02: Simulación y Control | Todo el Consorcio (Los 4 Expositores) | Cargos respectivos en exposición | Karol Paola Camacho López | Dirección del Proyecto |
| **FC-01** | Filosofía de Control del Proceso | Paulina Mota Macip | Instrumentación y Control | Karol Paola Camacho López | Dirección del Proyecto |
| **HAZOP** | Expediente Integral HAZOP y MCE-01 | Grecia Figueroa Rincón | Especialista en HSE | Karol Paola Camacho López | Dirección del Proyecto |
| **PIB-01** | Paquete de Ingeniería Básica del Proceso | Karol Camacho / Gildardo / Paulina / Grecia | Dirección y Especialidades Técnicas | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.1** | RPT Auditoría Económica Integral BioSTEAM | Grecia Figueroa / Karol Camacho | Evaluación Económica / Python | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.2** | RPT Comparativa DWSIM vs BioSTEAM | Paulina Mota / Karol Camacho | Simulación / Optimización Python | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.3** | RPT Desglose Costos CAPEX / OPEX | Grecia Figueroa / Karol Camacho | Evaluación Económica / Dirección | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.4** | RPT Registro Modificaciones Técnicas | Gildardo Ocaña / Karol Camacho | Ingeniería de Procesos / Dirección | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.5** | RPT Segunda Auditoría BioSTEAM (LCOMe) | Grecia Figueroa / Karol Camacho | Evaluación Económica / Python | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.6** | RPT Auditoría y Optimización SOEC Python | Karol Paola Camacho López | Ingeniera de Optimización (Python) | Karol Paola Camacho López | Dirección del Proyecto |
| **E4.7** | RPT Validación y Pruebas Unitarias SOEC | Karol Camacho / Paulina Mota | Optimización Python / Simulación | Karol Paola Camacho López | Dirección del Proyecto |
| **DIF-01**| Cartel PyDay (*Excepción Exclusiva*) | Karol Camacho / Grecia Figueroa | Optimización (Py) / Eval. Económica | Karol Paola Camacho López | Dirección del Proyecto |
| **RT-03** | Revisión Técnica 03: Guía Maestra y Diap. | Todo el Consorcio (Los 4 Expositores) | Cargos respectivos en defensa | Karol Paola Camacho López | Dirección del Proyecto |
| **EF** | Informe Final Consolidado de Licitación | Todo el Consorcio (Tomos I a V) | Dirección y Especialidades Técnicas | Karol Paola Camacho López | Dirección del Proyecto |

---

## 4. Reglas de Gobernanza y Control Documental

1. **Unicidad de Aprobación (Accountable único):**  
   Para cada entregable y actividad existe un único responsable ante el cliente y la convocante (**A**), recayendo en la **Dirección del Proyecto** para garantizar la coherencia institucional, el cumplimiento de las bases del RFP y la responsabilidad contractual.
2. **Responsabilidad de Ejecución (Responsible):**  
   El ejecutor directo (**R**) es el especialista técnico que realiza los cálculos, genera los modelos, dibuja los planos o redacta los informes. Cuando una actividad es interdisciplinaria por naturaleza (como el taller HAZOP o la Revisión Técnica RT-02), la ejecución se distribuye en roles específicos plenamente definidos.
3. **Consulta Técnica Obligatoria (Consulted):**  
   Ningún entregable se libera sin la revisión previa de los especialistas de las disciplinas adyacentes (e.g., simulación consulta a instrumentación y tuberías; HSE consulta a balances de emisión).
4. **Información y Transparencia (Informed):**  
   Todos los avances, advertencias y cierres de versión se publican de forma transparente en el repositorio oficial de GitHub (`04_Bitacora/` y `KANBAN.md`) para conocimiento de todo el equipo y evaluación académica.

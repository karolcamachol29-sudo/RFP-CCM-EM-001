# INFORME DE ESTANDARIZACIÓN DOCUMENTAL, INTEGRACIÓN DE MATRICES RACI Y MARCA DE AGUA
**Proyecto:** Licitación Internacional RFP-CCM-EM-001 — Planta de Producción de e-Metanol ($30\,000\text{ t/año}$)  
**Firma Consultora:** Solvanta Engineering Solutions S.A. de C.V.  
**Cátedra:** Diseño de Procesos y Productos Químicos (DPyPQ) — Facultad de Ingeniería Química, BUAP  
**Catedrático Evaluador:** Dr. Jesús Andrés Arzola Flores  
**Fecha de Emisión:** 14 de Noviembre de 2026  
**Estatus:** Versión 2.0 Oficial — 100% Estandarizado, Matrices RACI Integradas y Marca de Agua Propuesta B Aplicada  

---

## 1. Resumen Ejecutivo de la Fase 3

En estricto apego a las directrices de aseguramiento de calidad documental, control editorial y gobernanza técnica del proyecto de licitación `RFP-CCM-EM-001`, se completó con éxito la **Fase 3: Estandarización Documental, Integración de Matrices RACI y Marca de Agua**.

### Logros y Resultados Consolidados:
1. **Auditoría Documental al 100%:** Se inspeccionaron y validaron los 17 entregables oficiales ubicados en `03_Entregables_Finales/` (enlazados transparentemente mediante el symlink raíz `Entregables/`).
2. **Preservación Rigurosa de la Identidad Visual:** Se mantuvo intacta la línea gráfica corporativa desarrollada desde el inicio (tipografía Latin Modern, colores institucionales `navyblue` `#1A4F7C`, `accentblue` `#337CCF`, `darkred` `#8C1E1E`, `tealcolor` `#1E6E6E`, fondos `boxbg` y sombreado `tablerowalt`, cajas `tcolorbox`, márgenes y encabezados formales `fancyhdr`).
3. **Restauración y Validación de Código Fuente:**
   - Se reemplazó el archivo truncado de 2 bytes del Acta Constitutiva (`E0`) por la versión oficial de 10 páginas íntegras generada en LaTeX (`pdfTeX-1.40.29`, 2.32 MB).
   - Se restauró la carpeta `figuras/` de `PIB-01` (`Solvanta_PIB-01_Expediente.tex`) con `logo_empresa.png`, `dti_v0_2.pdf` y `Solvanta_AG-01.png`.
   - Se restauraron las subcarpetas `evidencias/` y `figuras/` en `02_Ingenieria_y_Diagramas/Verificacion_Termodinamica/` para garantizar la compilación 100% reproducible de `E1.5_DOC_ActividadVTP_v0.1.tex`.
4. **Integración de Matrices RACI Individuales en los Entregables:**
   - Se compilaron 17 hojas de control y gobernanza RACI individuales (1 página de alta resolución en LaTeX por entregable).
   - Se insertaron como Página 2 (inmediatamente después de la portada) en los 16 documentos PDF oficiales, sumando una página formal sin alterar la paginación ni los contenidos técnicos originales.
   - Para las presentaciones `RT-02` y `RT-03`, se diseñaron y compilaron diapositivas apaisadas (`landscape`, $792\times 612\text{ pt}$) insertadas como Slide 2.
   - Para `E4.1` a `E4.7`, se embebió la sección completa de gobernanza RACI en formato Markdown.
   - Para `E1.4`, se añadió el bloque de control RACI en el archivo de texto oficial.
5. **Cumplimiento Estricto de la Excepción del Cartel (`DIF-01`):** La hoja integrada en `DIF-01_DOC_CartelPyDay_v1.0.pdf` contiene la alerta institucional obligatoria certificando que fue elaborado exclusiva y autónomamente por **Karol Paola Camacho López** y **Grecia Figueroa Rincón**.
6. **Aplicación de la Marca de Agua Aprobada (Propuesta B):**
   - Tras la notificación de ausencia de marca de agua previa en el repositorio, el usuario aprobó formalmente la **Propuesta B** (Isotipo institucional translúcido al 6% de opacidad con pie de página de control licitatorio).
   - Se procesaron todos los PDFs aplicando la marca de agua en modo `underlay` (`over=False`), asegurando **cero interferencia** con textos, fórmulas, balances ni diagramas de proceso (DFP/DTI).

---

## 2. Inventario de Entregables Auditados y Estandarizados

Todos los archivos se encuentran actualizados en `03_Entregables_Finales/` (accesible en `Entregables/`). Los archivos originales previos se resguardaron intactos en `_auxiliar/backup_entregables_pre_fase3/`.

| Código | Denominación Oficial del Entregable | Formato | Pág. Orig. | Pág. Final | Integración RACI | Marca de Agua (Propuesta B) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **E0** | Acta Constitutiva de Solvanta Engineering Solutions S.A. de C.V. | PDF | 10 | **11** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E1.1** | Matriz de Clasificación de las Bases de Diseño (Actividad A2.1) | PDF | 7 | **8** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E1.2** | Balance Estequiométrico y Demanda Preliminar de Materias Primas | PDF | 8 | **9** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E1.3** | Síntesis Conceptual del Proceso y Diagrama de Bloques (BFD) | PDF | 16 | **17** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E1.3.1**| Propuesta Preliminar de Equipos y Parámetros de Diseño (EQ-01) | PDF | 13 | **14** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E1.4** | Video Pitch Ejecutivo del Proyecto de Licitación | TXT | N/A | N/A | Bloque RACI en texto | N/A (formato URL) |
| **E1.5** | Verificación Termodinámica DWSIM v1, Tablas TC-01/TE-01 y PFD v0 | PDF | 22 | **23** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E1.6** | Matriz Integral de Aspectos, Impactos y Requisitos Ambientales | PDF | 13 | **14** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **E2.1** | Lista Maestra de Equipos (LE-01) y Diagrama de Flujo DFP v1 | PDF | 25 | **26** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **FC-01** | Filosofía de Control del Proceso de Síntesis y Purificación | PDF | 14 | **15** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **PIB-01**| Paquete de Ingeniería Básica e Integración General de Proceso | PDF | 46 | **47** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **AC-HAZOP-01** | Estudio HAZOP, Matriz Causa-Efecto (MCE-01) y Salvaguardas | PDF | 49 | **50** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **RT-02 (Doc)**| Guion Oficial de Locución Sincronizado para Speech de 6:28 min | PDF | 8 | **9** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **RT-02 (PPT)**| Presentación Oficial de Diapositivas de Avance (18 Slides) | PDF | 20 | **21** | Slide RACI (Slide 2) | ✅ Aplicada (6% fondo + pie) |
| **RT-03 (Doc)**| Guía Maestra de Defensa Técnica, Speech de 10 min y Q&A | PDF | 23 | **24** | Hoja RACI (Pág. 2) | ✅ Aplicada (6% fondo + pie) |
| **RT-03 (PPT)**| Presentación de Diapositivas de Defensa Final (18 Slides) | PDF | 18 | **19** | Slide RACI (Slide 2) | ✅ Aplicada (6% fondo + pie) |
| **DIF-01**| Cartel Oficial de Difusión Científica — Congreso PyDay BUAP | PDF | 1 | **2** | Hoja RACI (Pág. 2, Excep.) | ✅ Aplicada (6% fondo + pie) |
| **E4.1 a E4.7**| Paquete de Reportes de Auditoría BioSTEAM y SOEC (7 docs) | MD | N/A | N/A | Sección RACI Markdown | N/A (formato Markdown) |
| **EF** | Informe Final Consolidado de la Licitación RFP-CCM-EM-001 | MD / PDF | N/A | N/A | `RACI_EF.pdf` compilado | Listo para integración final |

---

## 3. Características de la Marca de Agua Implementada (Propuesta B)

La marca de agua seleccionada y aplicada de forma uniforme en todos los documentos PDF presenta las siguientes propiedades fisico-digitales:

1. **Isotipo Central:**
   - Logotipo oficial vectorizado de Solvanta Engineering Solutions S.A. de C.V. (`logo_solvanta_clean.png`, canal alfa transparente).
   - Ancho: escalado dinámicamente al 55% del ancho de la página (máximo 380 pt en retrato, 420 pt en apaisado y 1400 pt en gran formato).
   - Opacidad: **6% (alpha = 0.06)** en escala RGB calibrada.
2. **Cintillo Perimetral de Control Licitatorio:**
   - Texto: `SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.  |  LICITACIÓN INTERNACIONAL RFP-CCM-EM-001  |  DOCUMENTO CONTROLADO`
   - Tipografía: Helvetica Bold con tamaño proporcional ($7\text{ a }10\text{ pt}$).
   - Color: Azul institucional `#1A4F7C` con opacidad calibrada al **22% (alpha = 0.22)**.
   - Posición: Centrado en el margen inferior ($y = 12\text{ a }18\text{ pt}$).
3. **Mecanismo de Renderizado:** Inyección mediante `page.merge_page(wm_page, over=False)`. Al situarse en la capa inferior de lienzo (`underlay`), la totalidad de los caracteres tipográficos, trazos vectoriales y tablas se imprimen sobre la marca de agua, eliminando cualquier riesgo de ilegibilidad o interferencia óptica.

---

## 4. Estructura y Contenido de las Hojas de Gobernanza RACI

Cada hoja de control RACI integrada en la Página 2 contiene:
1. **Encabezado Formal:** Clave del entregable, título completo del documento, nombre de la firma consultora y código licitatorio `RFP-CCM-EM-001`.
2. **Tabla 1: Asignación Institucional del Equipo Multidisciplinario:**
   - **Gildardo Ocaña Barrales:** 1. Ingeniería de Procesos \textbar\ 2. DTI / P&ID
   - **Paulina Mota Macip:** 1. Simulación \textbar\ 2. Instrumentación y Control
   - **Grecia Figueroa Rincón:** 1. Especialista en Seguridad, Salud y Medio Ambiente (HSE) \textbar\ 2. Evaluación Económica
   - **Karol Paola Camacho López:** 1. Dirección del Proyecto \textbar\ 2. Ingeniera de Optimización de Procesos (Python)
   - Rol RACI específico (R, A, C, I) y justificación técnica fundada en las actividades reales del proyecto.
3. **Tabla 2: Desglose del Ciclo de Vida de Elaboración:** Desglose secuencial de 5 a 6 fases (análisis contractual, diseño conceptual, modelado computacional, redacción técnica, revisión interna y liberación formal), con fechas auditadas en Git, responsables asignados y funciones RACI individuales.
4. **Alerta de Excepción en `DIF-01` (Cartel PyDay):**
   ```latex
   \begin{tcolorbox}[colframe=darkred,colback=redboxbg,arc=2mm,boxrule=0.8pt]
   \textbf{Regla de Excepción Obligatoria del Cartel (DIF-01):} En la concepción, diseño
   y elaboración técnica del cartel de difusión participaron única y exclusivamente
   la Ing. Karol Paola Camacho López y la Ing. Grecia Figueroa Rincón. Los integrantes
   Gildardo Ocaña Barrales y Paulina Mota Macip no participaron en su elaboración técnica
   ni gráfica, fungiendo únicamente como Informados (I).
   \end{tcolorbox}
   ```

---

## 5. Auditoría de Consistencia Técnica y Figuras

1. **Resolución e Integridad de Recursos Gráficos:**
   - Se validaron las 55 imágenes y diagramas contenidos en `02_Ingenieria_y_Diagramas/Recursos_Graficos/`.
   - Se verificaron los planos maestros de proceso: BFD v0, BFD v1.0, DFP v0, DFP v1.0 (`dfp_plpl_1_1.png` en $4500\times 3178\text{ px}$), DTI v0.2 (`dti_v0_2.pdf`) y Arreglo General Preliminar (`Solvanta_AG-01.png`).
   - Todos los esquemas conservan proporciones originales de aspecto y no sufrieron distorsiones durante el estampado digital.
2. **Consistencia de Nombres y Nomenclatura:**
   - La totalidad de las referencias personales concuerdan con la ortografía canónica: *Gildardo Ocaña Barrales*, *Paulina Mota Macip*, *Grecia Figueroa Rincón* y *Karol Paola Camacho López*.
   - Los nombres de archivo siguen la regla de tres bloques de estandarización documental (`[CODIGO]_[TIPO]_[DESCRIPCION]_[VERSION].[EXT]`).

---

## 6. Estado de Cumplimiento de la Fase 3

| Requerimiento de la Fase 3 | Estado | Evidencia de Verificación |
| :--- | :---: | :--- |
| **1. Revisión de entregables** | ✅ Cumplido | 17 paquetes auditados; baseline documental congelado. |
| **2. Integración de matrices RACI** | ✅ Cumplido | 17 hojas RACI generadas e integradas como Pág. 2 en PDFs y tablas en Markdown. |
| **3. Marca de agua oficial** | ✅ Cumplido | Propuesta B seleccionada por el usuario y aplicada al 100% de los PDFs en fondo al 6%. |
| **4. Revisión de figuras e imágenes** | ✅ Cumplido | Rutas restablecidas en PIB-01 y VTP; 0% alteración de resultados técnicos. |
| **5. Consistencia técnica y documental** | ✅ Cumplido | Cuatro integrantes con dualidad de cargos oficiales estandarizada. |
| **6. Generación de versiones finales** | ✅ Cumplido | PDFs generados en `03_Entregables_Finales/` (symlink `Entregables/`) con respaldo en `_auxiliar/`. |
| **7. Informe de estandarización** | ✅ Cumplido | Documento `INFORME_ESTANDARIZACION_DOCUMENTAL.md` formalizado. |

# Matriz RACI y Cronograma General — Proyecto RFP-CCM-EM-001 (Solvanta Engineering Solutions S.A. de C.V.)

> **Razón Social:** Solvanta Engineering Solutions S.A. de C.V.  
> **Eslogan:** "Soluciones que transforman la industria"  
>
> **Organigrama y Equipo de Proyecto:**  
> 👑 **Karol Paola Camacho López (@Karoc):** Directora de Proyecto, Python y Optimización  
> ⚙️ **Gildardo Ocaña Barrales (@GildardoOca25):** Ingeniería de Procesos, AutoCAD Plant 3D y DTI/P&ID  
> 🧪 **Paulina Mota Macip (@paulina145):** Simulación de Procesos (DWSIM) e Instrumentación y Control  
> 💰 **Grecia Figueroa Rincón (@Cho0bb):** Evaluación Económica (BioSTEAM) y Seguridad/Medio Ambiente (HSE)  
>
> **Roles RACI:** **R** = Responsable | **A** = Aprobador | **C** = Consultado | **I** = Informado  
> **Nomenclatura Entregables:** `E[N]` o `E[N].[sub]_[TIPO]_[NombreDescriptivo]_v[M].[m].[ext]`  
> **Regla de Ubicación por Tipo:**
> * `DOC` / `RPT` ➔ `03_Entregables_Finales/` (o `00_Gestion_Proyecto/`)
> * `VID` ➔ `03_Entregables_Finales/` (.mp4)
> * `SIM` ➔ `01_Proceso_y_Simulacion/DWSIM/`
> * `PY`  ➔ `01_Proceso_y_Simulacion/Python/`
> * `DWG` ➔ `02_Ingenieria_y_Diagramas/`

---

## 📋 Cuadro General RACI — Matriz Completa R / A / C / I

| Código | Tarea / Entregable | Responsable (R) | Archivos Requeridos | Ubicaciones Esperadas | Fecha Límite | Estado |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| **E0** | Redactar Acta Constitutiva & Identidad Solvanta | @Karoc | 1 File (`.pdf`) | `03_Entregables_Finales/` | 2026-08-17 | ✅ Finalizado |
| **E1.1** | Configuración de Bases de Diseño & Termodinámica | @Cho0bb | 1 File (`.pdf`) | `00_Gestion_Proyecto/` | 2026-08-25 | ✅ Done |
| **E1.2** | Simulación DWSIM & Reporte de Balances | @paulina145 | 2 Files (`.dwxmz`, `.pdf`) | `01_Proceso_y_Simulacion/DWSIM/`, `03_Entregables_Finales/` | 2026-08-25 | ✅ Done |
| **E1.3** | Diagramación (BFD, PFD, DTI) en Plant 3D | @GildardoOca25 | 2 Files (`.dwg`, `.pdf`) | `02_Ingenieria_y_Diagramas/`, `03_Entregables_Finales/` | 2026-08-24 | ✅ Done |
| **E1.4** | Video Pitch del Proyecto | @Karoc | 1 File (`.mp4`) | `03_Entregables_Finales/` | 2026-08-25 | ⏳ In Progress |

---

## 🔄 Tareas de Integración Interna para Documento Consolidado E1 (Bases de Diseño Preliminares)

> **Fecha Límite:** 2026-08-27 antes de las 16:00 h (4:00 PM)  
> **Modo de cierre:** Validación vía Git Commit (sin requerir carga de PDF individual adicional).

| Versión | Tarea de Integración en E1 | Responsable | Modalidad | Fecha Límite | Estado |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **v0.0** | Integración del E0 (Constitución de la empresa e identidad corporativa) | @Karoc | Git Commit | 2026-08-27 16:00 | ⏳ In Progress |
| **v0.1** | Integración del E1.1 (Bases de diseño preliminares y marco normativo) | @Cho0bb | Git Commit | 2026-08-27 16:00 | ⏳ In Progress |
| **v0.2** | Integración del E1.2 (Balance estequiométrico y marco termodinámico NB-01) | @paulina145 | Git Commit | 2026-08-27 16:00 | ⏳ In Progress |
| **v0.3** | Integración del E1.3 (Diagrama de Bloques del Proceso BFD v0) | @GildardoOca25 | Git Commit | 2026-08-27 16:00 | ⏳ In Progress |

---

## 🎯 Tasklist Detallada del Cronograma y Desglose de Archivos

- [x] **[E0] Redactar Acta Constitutiva & Identidad Solvanta**
  - **Asignado a:** @Karoc (Karol Paola Camacho López)
  - **Roles RACI:** R: @Karoc | A: @Karoc | C: @GildardoOca25, @paulina145, @Cho0bb | I: Cliente
  - **Archivos Requeridos (1):**
    - [x] `03_Entregables_Finales/E0_DOC_ActaConstitutiva_v1.0.pdf`
  - **Estado:** ✅ Finalizado

- [x] **[E1.1] Configuración de Bases de Diseño & Termodinámica**
  - **Asignado a:** @Cho0bb (Grecia Figueroa Rincón)
  - **Roles RACI:** R: @Cho0bb | A: @Karoc | C: @paulina145, @GildardoOca25 | I: Equipo
  - **Archivos Requeridos (1):**
    - [x] `00_Gestion_Proyecto/E1.1_DOC_BasesDiseno_v1.0.pdf`
  - **Estado:** ✅ Done

- [x] **[E1.2] Simulación de Procesos & Balances (DWSIM)**
  - **Asignado a:** @paulina145 (Paulina Mota Macip)
  - **Roles RACI:** R: @paulina145 | A: @Karoc | C: @GildardoOca25, @Cho0bb | I: Equipo
  - **Archivos Requeridos (2):**
    - [x] Archivo Simulación: `01_Proceso_y_Simulacion/DWSIM/E1.2_SIM_Balances_v1.0.dwxmz`
    - [x] Archivo Reporte DOC: `03_Entregables_Finales/E1.2_DOC_ReporteSimulacion_v1.0.pdf`
  - **Estado:** ✅ Done

- [x] **[E1.3] Diagramación (BFD, PFD, DTI) en Plant 3D**
  - **Asignado a:** @GildardoOca25 (Gildardo Ocaña Barrales)
  - **Roles RACI:** R: @GildardoOca25 | A: @Karoc | C: @paulina145, @Cho0bb | I: Equipo
  - **Archivos Requeridos (2):**
    - [x] Archivo Plano DWG: `02_Ingenieria_y_Diagramas/E1.3_DWG_PFD_v1.0.dwg`
    - [x] Archivo Documento DOC: `03_Entregables_Finales/E1.3_DOC_EspecificacionDiagramas_v1.0.pdf`
  - **Estado:** ✅ Done

- [ ] **[E1.4] Video Pitch del Proyecto**
  - **Asignado a:** @Karoc (Karol Paola Camacho López)
  - **Roles RACI:** R: @Karoc | A: @Karoc | C: @paulina145, @GildardoOca25 | I: @Cho0bb
  - **Archivos Requeridos (1):**
    - [ ] Archivo Video Pitch: `03_Entregables_Finales/E1.4_VID_PitchProyecto_v1.0.mp4`
  - **Estado:** ⏳ In Progress

---

### 🧩 Subtareas de Integración E1 (Cierre vía Commit — Límite: 27/08/2026 16:00)
- [ ] **v0.0 — Integración E0 en Documento E1** (@Karoc)
- [ ] **v0.1 — Integración E1.1 en Documento E1** (@Cho0bb)
- [ ] **v0.2 — Integración E1.2 en Documento E1** (@paulina145)
- [ ] **v0.3 — Integración E1.3 en Documento E1** (@GildardoOca25)


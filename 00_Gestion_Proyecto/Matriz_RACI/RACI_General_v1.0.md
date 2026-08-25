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
> * `SIM` ➔ `01_Proceso_y_Simulacion/DWSIM/`
> * `PY`  ➔ `01_Proceso_y_Simulacion/Python/`
> * `DWG` ➔ `02_Ingenieria_y_Diagramas/`

---

## 📋 Cuadro General RACI — Matriz Completa R / A / C / I

| Código | Tarea / Entregable | Responsable (R) | Archivos Requeridos | Ubicaciones Esperadas | Fecha Límite | Estado |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| **E0** | Redactar Acta Constitutiva & Identidad Solvanta | @Karoc | 1 File (`.pdf`) | `03_Entregables_Finales/` | 2026-08-17 | ✅ Finalizado |
| **E1.1** | Configuración de Bases de Diseño & Termodinámica | @Cho0bb | 1 File (`.pdf`) | `00_Gestion_Proyecto/` | 2026-08-25 | 🔍 Review / QA |
| **E1.2** | Simulación DWSIM & Reporte de Balances | @paulina145 | 2 Files (`.dwxmz`, `.pdf`) | `01_Proceso_y_Simulacion/DWSIM/`, `03_Entregables_Finales/` | 2026-08-25 | 🔍 Review / QA |
| **E1.3** | Diagramación (BFD, PFD, DTI) en Plant 3D | @GildardoOca25 | 2 Files (`.dwg`, `.pdf`) | `02_Ingenieria_y_Diagramas/`, `03_Entregables_Finales/` | 2026-08-24 | 🔍 Review / QA |
| **E1.4** | Integración Python & Reporte Técnico | @Karoc | 2 Files (`.py`, `.pdf`) | `01_Proceso_y_Simulacion/Python/`, `03_Entregables_Finales/` | 2026-08-25 | ⏳ In Progress |

---

## 🎯 Tasklist Detallada del Cronograma y Desglose de Archivos

- [x] **[E0] Redactar Acta Constitutiva & Identidad Solvanta**
  - **Asignado a:** @Karoc (Karol Paola Camacho López)
  - **Roles RACI:** R: @Karoc | A: @Karoc | C: @GildardoOca25, @paulina145, @Cho0bb | I: Cliente
  - **Archivos Requeridos (1):**
    - [x] `03_Entregables_Finales/E0_DOC_ActaConstitutiva_v1.0.pdf`
  - **Estado:** ✅ Finalizado

- [ ] **[E1.1] Configuración de Bases de Diseño & Termodinámica**
  - **Asignado a:** @Cho0bb (Grecia Figueroa Rincón)
  - **Roles RACI:** R: @Cho0bb | A: @Karoc | C: @paulina145, @GildardoOca25 | I: Equipo
  - **Archivos Requeridos (1):**
    - [ ] `00_Gestion_Proyecto/E1.1_DOC_BasesDiseno_v1.0.pdf`
  - **Estado:** 🔍 Review / QA

- [ ] **[E1.2] Simulación de Procesos & Balances (DWSIM)**
  - **Asignado a:** @paulina145 (Paulina Mota Macip)
  - **Roles RACI:** R: @paulina145 | A: @Karoc | C: @GildardoOca25, @Cho0bb | I: Equipo
  - **Archivos Requeridos (2):**
    - [ ] Archivo Simulación: `01_Proceso_y_Simulacion/DWSIM/E1.2_SIM_Balances_v1.0.dwxmz`
    - [ ] Archivo Reporte DOC: `03_Entregables_Finales/E1.2_DOC_ReporteSimulacion_v1.0.pdf`
  - **Estado:** 🔍 Review / QA

- [ ] **[E1.3] Diagramación (BFD, PFD, DTI) en Plant 3D**
  - **Asignado a:** @GildardoOca25 (Gildardo Ocaña Barrales)
  - **Roles RACI:** R: @GildardoOca25 | A: @Karoc | C: @paulina145, @Cho0bb | I: Equipo
  - **Archivos Requeridos (2):**
    - [ ] Archivo Plano DWG: `02_Ingenieria_y_Diagramas/E1.3_DWG_PFD_v1.0.dwg`
    - [ ] Archivo Documento DOC: `03_Entregables_Finales/E1.3_DOC_EspecificacionDiagramas_v1.0.pdf`
  - **Estado:** 🔍 Review / QA

- [ ] **[E1.4] Integración, Optimización con Python & Reporte**
  - **Asignado a:** @Karoc (Karol Paola Camacho López)
  - **Roles RACI:** R: @Karoc | A: @Karoc | C: @paulina145, @GildardoOca25 | I: @Cho0bb
  - **Archivos Requeridos (2):**
    - [ ] Archivo Script Python: `01_Proceso_y_Simulacion/Python/E1.4_PY_Optimizacion_v1.0.py`
    - [ ] Archivo Reporte DOC: `03_Entregables_Finales/E1.4_DOC_ReporteOptimizacion_v1.0.pdf`
  - **Estado:** ⏳ In Progress

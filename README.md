# 🚀 Repositorio Oficial de Ingeniería — RFP-CCM-EM-001

¡Bienvenido al repositorio del equipo! Este espacio está diseñado para coordinar la documentación, simulaciones, diagramas y entregables del proyecto de manera organizada y automatizada.

---

## 🗂️ Estructura del Repositorio

| Carpeta / Archivo | Descripción | Uso Principal |
| :--- | :--- | :--- |
| **`00_Gestion_Proyecto`** | Minutas, plantillas oficiales, matrices de evaluación, selección y matriz RACI. | Consulta y gestión |
| **`01_Proceso_y_Simulacion`** | Modelos convergidos en DWSIM (`.dwxmz`, `.dwxml`), BioSTEAM y memorias descriptivas. | Modelado y simulación |
| **`02_Ingenieria_y_Diagramas`** | Diagramas de ingeniería (BFD, DFP/PFD, DTI/P&ID `DTI-v0_Solvanta.pdf`), fuentes LaTeX de filosofía de control (`FC-01`), lista de equipos y verificación. | Ingeniería de detalle |
| **`03_Entregables_Finales`** | Documentos formales y versiones finales en PDF/TXT para cliente y docencia (E0-E4, EF). **Solo archivos finales** (sin `.tex`, `.aux`, `.log` ni `.zip`). | **Entregables Oficiales** |
| **`04_Bitacora`** | Reportes de avance y diario de trabajo técnico. | Registro individual |
| **`KANBAN.md`** | Tablero oficial de tareas del proyecto en Markdown. | Seguimiento de flujo |
| **`generar_documento.sh`** | Script interactivo para generación de documentos y tarjetas. | Automatización |

### 📌 Entregables Clave de Ingeniería de Control y Proceso
* **DTI Oficial:** `02_Ingenieria_y_Diagramas/DTI_PID/DTI-v0_Solvanta.pdf`
* **Filosofía de Control Oficial (E2):** `03_Entregables_Finales/E2/FC-01_Solvanta/FC-01_DOC_FilosofiaControl_v1.0.pdf`
* **Fuente Técnica de Filosofía de Control:** `02_Ingenieria_y_Diagramas/Filosofia_Control/FC-01_DOC_FilosofiaControl_v1.0.tex`
* **Carpeta Única de Evidencias:** `03_Entregables_Finales/E1/VTP-01_Solvanta/02_Verificacion/Evidencias/`

---

## 🏷️ Reglas de Nomenclatura de Archivos y Jerarquía

Antes de subir cualquier archivo, asegúrate de renombrarlo siguiendo el estándar oficial del proyecto:

$$\text{[Entregable]\_[Tipo]\_[NombreDescriptivo]\_v[Mayor].[Menor].[ext]}$$

* **Entregables Principales:** `E0`, `E1`, `E2`, `E3`, `E4`, `EF`
* **Subentregables / Desgloses:** `E1.1`, `E1.2`, `E2.1`, `E2.2`, etc.
* **Tipos permitidos:** `DOC` (Documento), `DWG` (CAD/Diagrama), `SIM` (Simulación), `PY` (Script), `RPT` (Reporte), `VID` (Video Pitch / Presentación).

### Ejemplos de Aplicación
* **Ejemplo Documento:** `E0_DOC_ActaConstitutiva_v1.0.pdf`
* **Ejemplo Simulación Subentregable:** `E1.1_SIM_ReactoresCSTR_v1.0.dwzx`
* **Ejemplo Plano Subentregable:** `E2.1_DWG_PFD_Planta_v1.0.dwg`
* **Ejemplo Video Subentregable:** `E1.4_VID_PitchOptimizacion_v1.0.mp4`

---

## ⚡ Automatización e Interacción (`generar_documento.sh`)

El repositorio incluye un script Bash totalmente interactivo. Para ejecutarlo:

```bash
./generar_documento.sh
```

El script permite:
1. Generar **Minutas de Reunión** con metadatos completos.
2. Generar **Matrices Ponderadas** y de **Evaluación de Calidad**.
3. Registrar/Actualizar **Tareas RACI** y **Subentregables** (`E1.1`, `E2.1`).
4. Sincronizar automáticamente el tablero **`KANBAN.md`**.
5. Crear bitácoras diarias de trabajo técnico.

---

## 📦 Guía Rápida: Subir Entregables desde GitHub Web

1. Navega dentro del repositorio a la carpeta correspondiente (ejemplo: `03_Entregables_Finales/E1/`).
2. Haz clic en **`Add file`** ➔ **`Upload files`**.
3. Asegúrate de verificar la nomenclatura antes de confirmar el commit.
4. En el mensaje de commit, agrega `closes #NÚMERO` para vincular tu entrega con la tarjeta Kanban.

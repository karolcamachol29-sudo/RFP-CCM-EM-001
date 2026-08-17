# 🚀 Repositorio Oficial de Ingeniería

¡Bienvenido al repositorio del equipo! Este espacio está diseñado para coordinar la documentación, simulaciones, diagramas y entregables del proyecto de manera organizada y automatizada.

---

## 🗂️ Estructura del Repositorio

| Carpeta | Descripción | Uso Principal |
| :--- | :--- | :--- |
| **`00_Gestion_Proyecto`** | Minutas, plantillas oficiales, cronogramas y reglas. | Consulta y gestión |
| **`01_Proceso_y_Simulacion`** | Archivos de DWSIM, BioSTEAM y scripts de Python. | **Zona de Entrega** |
| **`02_Ingenieria_y_Diagramas`** | Diagramas PFD, P&ID y planos AutoCAD Plant 3D. | **Zona de Entrega** |
| **`03_Entregables_Finales`** | Documentos formales y versiones finales en PDF. | **Zona de Entrega** |
| **`04_Bitacora`** | Reportes de avance y diario de trabajo. | Registro individual |

---

## 🏷️ Reglas de Nomenclatura de Archivos

Antes de subir cualquier archivo, asegúrate de renombrarlo siguiendo el estándar del proyecto:

$$\text{[Entregable]\_\_[Tipo]\_\_[NombreDescriptivo]\_\_v[Versión].[ext]}$$

* **Ejemplo Documento:** `E0_DOC_ActaConstitutiva_v1.0.pdf`
* **Ejemplo Simulación:** `E1_SIM_ReactoresCSTR_v1.0.dwzx`
* **Ejemplo Plano/Diagrama:** `E2_DWG_PFD_Planta_v1.0.dwg`

---

## 📦 Guía Rápida: Subir Entregables desde la Web (GitHub.com)

Si vas a entregar avances, simulaciones o diagramas directamente desde tu navegador, sigue estos **3 sencillos pasos**:

### 1. Entra a la carpeta correspondiente
Navega dentro del repositorio a la subcarpeta donde debes guardar tu trabajo (ejemplo: `03_Entregables_Finales/E0_Constitucion/`).

### 2. Sube tu archivo
1. Haz clic en el botón **`Add file`** (esquina superior derecha) ➔ **`Upload files`**.
2. Arrastra tu archivo o haz clic para seleccionarlo desde tu computadora.
3. Asegúrate de verificar la nomenclatura antes de confirmar.

### 3. Cierra tu tarjeta automáticamente (**El Truco Maestro**)
En el cuadro **Commit changes** (mensaje de entrega) al final de la página:
1. Escribe una breve descripción del archivo subido.
2. Agrega la frase `closes #NÚMERO` o `fixes #NÚMERO` correspondiente a tu tarjeta del tablero Kanban.

```text
Subiendo borrador de acta constitutiva final closes #12

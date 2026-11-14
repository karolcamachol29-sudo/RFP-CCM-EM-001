# Matriz RACI Individual — Entregable [E4]
**Entregable:** Paquete de Auditorías Técnicas, Modelado BioSTEAM y Optimización Multivariable SOEC (E4.1 a E4.7)  
**Código Oficial:** `E4`  
**Archivo Oficial Relacionado:** `03_Entregables_Finales/E4_Auditorias_y_Optimizacion/ (E4.1 a E4.7)`  
**Consorcio:** Solvanta Engineering Solutions S.A. de C.V. — Licitación RFP-CCM-EM-001  
**Periodo de Ejecución:** 2026-10-28 al 2026-11-05 (9 días de duración total)  
**Tipo de Fechas:** Verificada en scripts de auditoría y Git  


---

## 1. Asignación General de Roles RACI

| Integrante | Cargo Oficial Desempeñado | Función RACI | Justificación Técnica de la Asignación |
| :--- | :--- | :---: | :--- |
| **Karol Paola Camacho López** | Ingeniera de Optimización de Procesos (Python) | **R** (Responsible) | Ejecutor directo del trabajo técnico, modelado, cálculos o redacción del entregable. |
| **Karol Paola Camacho López** | Dirección del Proyecto | **A** (Accountable) | Responsable único ante la Dirección de Proyecto, la cátedra y la entidad convocante por la calidad y entrega final. |
| **Grecia Figueroa Rincón** | Evaluación Económica | Consultado (C) | Co-validación de los 12 hallazgos en BioSTEAM, depreciación y CAPEX/OPEX. |
| **Paulina Mota Macip** | Simulación | Consultado (C) | Co-validación del acoplamiento térmico de corrientes en DWSIM y balances energéticos. |
| **Gildardo Ocaña Barrales** | Ingeniería de Procesos | Consultado (C) | Verificación de la consistencia de inventario de equipos afectados. |
| **Todo el consorcio Solvanta** | Equipo Técnico | Informado (I) | Informado sobre los resultados de optimización energética (-13.66% en SEC). |

---

## 2. Desglose Cronológico de Actividades del Entregable

| Actividad del Ciclo de Vida | Fecha Inicio | Fecha Fin | Tipo de Fecha | Responsable | Cargo Desempeñado | Rol RACI |
| :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| 1. Detección de inconsistencias y discrepancias en el notebook original de BioSTEAM | 2026-10-28 | 2026-11-02 | Verificada | Karol Camacho | Optimización Py | **R** |
| 2. Desarrollo del paquete modular en Python soec_optimization/ | 2026-11-02 | 2026-11-03 | Verificada | Karol Camacho | Optimización Py | **R** |
| 3. Ejecución de optimizaciones multivariables (OAT, Hipercubo Latino LHS, Morris) | 2026-11-02 | 2026-11-03 | Verificada | Karol Camacho | Optimización Py | **R** |
| 4. Auditoría económica integral en BioSTEAM y corrección de funciones de costeo | 2026-11-04 | 2026-11-05 | Verificada | Karol Camacho, Grecia Figueroa | Optimización / Economía | **R / C** |
| 5. Consulta técnica con simulación DWSIM | 2026-11-04 | 2026-11-05 | Verificada | Paulina Mota | Simulación | **C** |
| 6. Redacción técnica de los reportes E4.1, E4.2, E4.3, E4.4, E4.5, E4.6 y E4.7 | 2026-11-05 | 2026-11-05 | Verificada | Karol Camacho | Optimización Py | **R** |
| 7. Aprobación y liberación del paquete de auditorías E4 | 2026-11-05 | 2026-11-05 | Verificada | Karol Camacho | Dirección Proyecto | **A** |

---

## 3. Trazabilidad con Archivos y Evidencias en Repositorio

* **Documento Oficial Final:** `03_Entregables_Finales/E4_Auditorias_y_Optimizacion/ (E4.1 a E4.7)`
* **Control de Tareas:** Tarjeta `[E4]` en `KANBAN.md` y sincronización con GitHub Projects.
* **Registro Histórico:** Inscrito en las actas de bitácora técnica de `04_Bitacora/`.

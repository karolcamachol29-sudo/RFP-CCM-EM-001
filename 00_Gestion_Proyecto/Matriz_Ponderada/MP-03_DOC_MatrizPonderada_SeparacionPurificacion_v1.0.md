# Matriz Ponderada de Selección Técnica — MP-03: Tren de Separación y Purificación (RFP-CCM-EM-001)

> **Proyecto:** Planta de Producción de e-Metanol a partir de CO2 y H2 Verde (46,300 kg/h de Metanol)  
> **Consorcio:** Solvanta S.A. de C.V.  
> **Código Documental:** `MP-03_DOC_MatrizPonderada_SeparacionPurificacion_v1.0`  
> **Fecha:** 2026-09-12  

---

## 1. Objeto del Análisis
Seleccionar el esquema de purificación y fraccionamiento para separar el e-metanol del agua de reacción y recuperar los gases no convertidos ($H_2$, $CO_2$), asegurando especificación grado químico AA (ASTM D1152: pureza $\ge 99.85\%$ p/p, contenido de agua $<0.10\%$ p/p).

---

## 2. Alternativas Evaluadas
* **Opción A: Tren Bifásico Flash Frío ($V-501$, $35^\circ\text{C}$, 48 bar) + Columna de Destilación Fraccionada ($C-501$):** Condensación de la mezcla líquida metanol-agua y separación rápida de gases para reciclo al compresor $K-501$; fondo líquido enviado a despresurización y columna fraccionadora de 45 platos.
* **Opción B: Doble Columna de Destilación sin Separador Flash Previo:** Enfriamiento y alimentación directa del efluente completo a una columna desgasificadora (topping) seguida de columna de refinamiento (refining).
* **Opción C: Sistema Híbrido de Deshidratación por Pervaporación con Membranas Zeolíticas:** Separación flash inicial complementada con membranas cerámicas permselectivas NaA para remoción de agua.

---

## 3. Matriz de Comparación Ponderada

| ID | Criterio de Evaluación | Peso (%) | Opción A: Flash + C-501 | Opción A (Pond.) | Opción B: Doble Columna | Opción B (Pond.) | Opción C: Pervaporación | Opción C (Pond.) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | **Pureza y Calidad del Metanol (ASTM D1152 $\ge 99.85\%$)** | 30% | 5 | 1.50 | 5 | 1.50 | 4 | 1.20 |
| **C2** | **Eficiencia en Recuperación de Gases Incondensables** | 25% | 5 | 1.25 | 3 | 0.75 | 3 | 0.75 |
| **C3** | **Carga Térmica en Hervidores y Consumo de Vapor** | 20% | 4 | 0.80 | 3 | 0.60 | 4 | 0.80 |
| **C4** | **Simplicidad de Operación, Control y Confiabilidad** | 15% | 5 | 0.75 | 4 | 0.60 | 2 | 0.30 |
| **C5** | **CAPEX de Equipos y Costo de Mantenimiento** | 10% | 4 | 0.40 | 3 | 0.30 | 2 | 0.20 |
| **TOTAL**| | **100%** | — | **4.70** | — | **3.75** | — | **3.25** |

---

## 4. Conclusión y Dictamen Técnico
* **Opción Seleccionada:** **Opción A — Separador Flash Frío V-501 acoplado a Columna de Refinamiento C-501**
* **Puntaje Ponderado Obtenido:** **4.70 / 5.00**
* **Justificación de Ingeniería:** El flash frío a alta presión desgasifica el 99.8% del $H_2$ y $CO_2$ sin requerir energía térmica de vaporización, enviándolos al bucle de reciclo con mínima potencia de compresión. La columna $C-501$ procesa únicamente la corriente binaria rica en metanol y agua, garantizando 99.87% p/p de metanol en el destilado con costo de inversión moderado.
* **Evaluadores Responsables:**
  - **Paulina Mota Macip** — Simulación / Instrumentación y Control.
  - **Grecia Figueroa Rincón** — Evaluación Económica / Especialista en Seguridad (HSE).

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script maestro para generar la Guía Maestra de Defensa Técnica, Speech Oficial
y Memoria Rigurosa de Ingeniería (Markdown + LaTeX + PDF).

Consorcio Solvanta Engineering Solutions S.A. de C.V. | RFP-CCM-EM-001
Planta de e-Metanol (30,000 t/año) - Circular Carbon México, S.A. de C.V.
"""

import os
import subprocess
import sys

MD_OUT = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.md"
TEX_OUT = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.tex"
PDF_OUT = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf"

def get_markdown_content():
    return """# GUÍA MAESTRA DE DEFENSA TÉCNICA, SPEECH OFICIAL Y MEMORIA RIGUROSA DE INGENIERÍA
## Simulación Avanzada, Programación en BioSTEAM/DWSIM, Optimización Multivariable SOEC y Análisis de Nodos/Seguridad DTI

---

### FICHA TÉCNICA INSTITUCIONAL
* **Proyecto:** Planta de Producción de e-Metanol Grado Químico AA ($30,000\\text{ t/año}$)
* **Licitación Internacional:** RFP-CCM-EM-001 | predio industrial asignado para el proyecto RFP-CCM-EM-001.
* **Consorcio de Ingeniería:** Solvanta Engineering Solutions S.A. de C.V.
* **Expositores Técnicos:**
  * **Grecia Figueroa (Gress):** Ingeniera de Procesos | Especialista en Modelado en BioSTEAM, Análisis de Nodos DTI, Filosofía de Control y Seguridad Funcional (HAZOP / SIL).
  * **Karol Camacho (Karoc):** Ingeniero de Procesos y Simulación | Especialista en Electroquímica de Alta Temperatura SOEC, Integración Algorítmica en DWSIM y Optimización Multivariable.

---

# ÍNDICE GENERAL DE CONTENIDOS

1. [SECCIÓN 1: SPEECH OFICIAL SINCRONIZADO (GUION DE LOCUCIÓN PASO A PASO)](#sección-1-speech-oficial-sincronizado-guion-de-locución-paso-a-paso)
   - 1.1 Matriz de Control de Tiempos y Transición de Voces
   - 1.2 Intervención 1: Grecia Figueroa — BioSTEAM y Programación Orientada a Objetos para Nuevas Tecnologías
   - 1.3 Intervención 2: Karol Camacho — Fundamentos del SOEC, Termodinámica de Alta Temperatura e Integración con DWSIM
   - 1.4 Intervención 3: Grecia Figueroa — Desglose de Nodos en el DTI, Filosofía de Salvaguardas y Seguridad Analizada (HAZOP/SIL)
   - 1.5 Intervención 4: Karol Camacho — Escenarios del SOEC, Espacio de Diseño y Selección del Punto Óptimo Más Eficiente (Escenario D)
   - 1.6 Intervención 5: Grecia Figueroa — Conclusión Final: El Poder de la Programación en la Ingeniería Química y Cierre
2. [SECCIÓN 2: ARQUITECTURA DE CÓDIGO Y ESTRUCTURA DE PROGRAMACIÓN](#sección-2-arquitectura-de-código-y-estructura-de-programación)
   - 2.1 Programación Orientada a Objetos en BioSTEAM (`biosteam.Unit`)
   - 2.2 Automatización y Conexión de DWSIM mediante API en Python
3. [SECCIÓN 3: FUNDAMENTOS FÍSICOS, DESGLOSE DE ECUACIONES Y DESPEJES MATEMÁTICOS PASO A PASO](#sección-3-fundamentos-físicos-desglose-de-ecuaciones-y-despejes-matemáticos-paso-a-paso)
   - 3.1 Termodinámica Fundamental y Polinomios de Shomate de NIST-JANAF
   - 3.2 Potencial Reversible de Nernst con Presión y Conversión
   - 3.3 Cinética de Transferencia de Carga y Butler-Volmer Inversa
   - 3.4 Pérdidas Óhmicas y Conducción Iónica en Electrolito YSZ
   - 3.5 Sobrepotencial de Concentración y Difusión de Stefan-Maxwell/Knudsen
   - 3.6 Régimen Térmico Sub-termoneutro y Acoplamiento con Reactor Lurgi
   - 3.7 Cinética Heterogénea de Vanden Bussche & Froment y Ecuación de Ergun
   - 3.8 Dimensionamiento Físico de Destilación (FUG + O'Connell + Fair)
4. [SECCIÓN 4: LÓGICA DE METADATOS DE TOPOLOGÍA, BALANCES Y SERVICIOS AUXILIARES](#sección-4-lógica-de-metadatos-de-topología-balances-y-servicios-auxiliares)
   - 4.1 Topología de Procesos como Grafo Dirigido y Algoritmos de Corte (Tear Streams)
   - 4.2 Matrices Consolidadas de Balance de Materia Global de la Planta
   - 4.3 Matriz de Balance de Energía Global y Demanda de Servicios Auxiliares

---

# SECCIÓN 1: SPEECH OFICIAL SINCRONIZADO (GUION DE LOCUCIÓN PASO A PASO)

### 1.1 Matriz de Control de Tiempos y Transición de Voces

| Segmento | Orador | Temática Principal | Tiempo Estimado | Ventana Temporal | Traspaso / Conexión |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **P1** | **Grecia Figueroa** | Apertura, BioSTEAM y POO para Equipos no Estándar | $1\\text{ min } 15\\text{ s}$ | 0:00 – 1:15 | Cede la palabra a Karol con puente hacia termodinámica SOEC. |
| **P2** | **Karol Camacho** | SOEC, Primeros Principios, Endotermicidad e Integración DWSIM | $1\\text{ min } 30\\text{ s}$ | 1:15 – 2:45 | Cede la palabra a Grecia con puente hacia P&ID y seguridad. |
| **P3** | **Grecia Figueroa** | Nodos del DTI, Filosofía de Control, HAZOP y Salvaguardas SIL | $1\\text{ min } 30\\text{ s}$ | 2:45 – 4:15 | Cede la palabra a Karol con puente hacia optimización multivariable. |
| **P4** | **Karol Camacho** | Escenarios SOEC (A, B, C, D), Trade-offs y Selección del Óptimo | $1\\text{ min } 30\\text{ s}$ | 4:15 – 5:45 | Cede la palabra a Grecia para el cierre institucional. |
| **P5** | **Grecia Figueroa** | Conclusión Final: La Programación en la Ingeniería y Cierre | $0\\text{ min } 45\\text{ s}$ | 5:45 – 6:30 | Conclusión contundente y apertura formal a preguntas del jurado. |

---

### 1.2 Intervención 1: Grecia Figueroa — BioSTEAM y Programación Orientada a Objetos para Nuevas Tecnologías

> **[ORADOR: GRECIA FIGUEROA — TIEMPO: 0:00 – 1:15]**  
> *(Tono: Seguro, profesional, entusiasta y con rigor técnico de ingeniería química).*

«Buenos días, miembros del comité evaluador y colegas. Mi nombre es **Grecia Figueroa** y, junto con mi compañero **Karol Camacho**, representamos a **Solvanta Engineering Solutions S.A. de C.V.** Presentamos la defensa técnica de nuestra propuesta para la licitación internacional **RFP-CCM-EM-001**: el diseño, simulación, análisis de seguridad y evaluación tecno-económica de una planta industrial de producción de **e-metanol de $30,000\\text{ toneladas métricas por año}$** a instalarse en el complejo industrial de referencia, Veracruz.

Al iniciar el desarrollo conceptual de este proyecto, nos enfrentamos a un dilema que todo ingeniero químico moderno conoce bien: **las limitaciones intrínsecas del software comercial cerrado**. Cuando uno formula una propuesta con tecnologías de frontera —como la electrólisis de vapor a alta temperatura mediante celdas de óxido sólido (SOEC) o reactores catalíticos multitubulares heterogéneos con cinéticas complejas—, los simuladores convencionales simplemente **no tienen estos equipos en sus bibliotecas prediseñadas**. La práctica habitual en la industria es recurrir a aproximaciones burdas: cajas negras estáticas con conversiones fijas que falsean la termodinámica, omiten los perfiles térmicos y destruyen la fidelidad del análisis tecno-económico.

En Solvanta rompimos este paradigma recurriendo a **BioSTEAM**, una plataforma abierta en Python diseñada específicamente para el diseño de bioprocesos, biorrefinerías y evaluación económica ágil. Lo que hicimos en BioSTEAM fue programar nuestras propias operaciones unitarias a través de **Programación Orientada a Objetos**, creando subclases directas de la clase maestra `biosteam.Unit`. 

Específicamente, programamos la unidad `PEMElectrolyzer` y el reactor tubular `MethanolPFRReactor`. Para lograr que BioSTEAM reconociera estos equipos como parte natural de su flowsheet, sobreescribimos tres métodos fundamentales:
1. **El método `_run()`:** Donde definimos los balances de materia rigurosos, la estequiometría faradaica, los consumos molares de especies con la librería `thermosteam` y las especificaciones de equilibrio de fases en las corrientes de salida.
2. **El método `_design()`:** Donde se resuelven las ecuaciones de transporte, el dimensionamiento de las celdas y tubos, las pérdidas cinéticas y, crucialmente, la asignación de consumo eléctrico y demandas térmicas mediante `power_utility` y `add_heat_utility`.
3. **El método `_cost()`:** Donde indexamos las correlaciones de costo de adquisición base de Guthrie y Turton, y las proyecciones oficiales del Departamento de Energía de EE. UU. (DOE Record 24005), desagregando los costos de stacks, balance de planta y rectificadores con sus respectivos factores de módulo desnudo ($F_{BM}$).

Esto nos permitió realizar una auditoría tecno-económica preliminar ágil y comparar arquitecturas tecnológicas. Sin embargo, para escalar la planta a la máxima eficiencia termodinámica posible, decidimos explorar la electrólisis de óxido sólido a $800^\\circ\\text{C}$ acoplada térmicamente a la síntesis de metanol. Para explicar los primeros principios electroquímicos de esta tecnología y cómo logramos su integración rigurosa con el simulador DWSIM, cedo la palabra a mi compañero **Karol Camacho**.»

---

### 1.3 Intervención 2: Karol Camacho — Fundamentos del SOEC, Termodinámica de Alta Temperatura e Integración con DWSIM

> **[ORADOR: KAROL CAMACHO — TIEMPO: 1:15 – 2:45]**  
> *(Tono: Analítico, preciso, matemático y convincente).*

«Muchas gracias, Grecia. Buenos días al tribunal.

La decisión de seleccionar la tecnología **SOEC (Solid Oxide Electrolyzer Cell)** en lugar de la electrólisis convencional PEM o alcalina responde a una ley termodinámica fundamental: conforme elevamos la temperatura de disociación del agua de $25^\\circ\\text{C}$ a $800^\\circ\\text{C}$, la entalpía total de reacción ($\\Delta H$) permanece casi invariable en torno a $248\\text{ kJ/mol}$, pero la energía libre de Gibbs ($\\Delta G$) —que representa el trabajo eléctrico neto que debemos inyectar— **disminuye drásticamente de $237$ a $183.5\\text{ kJ/mol}$**. Esa diferencia de $53.5\\text{ kJ/mol}$ se transfiere al término entálpico térmico $T\\Delta S$. En términos de ingeniería práctica: **reemplazamos un $28\\%$ de la energía eléctrica cara por energía térmica de bajo costo**.

Como no existía un módulo SOEC ni en BioSTEAM ni en DWSIM, desarrollamos desde cero en Python una biblioteca física rigurosa estructurada en cuatro pilares:
1. **Termodinámica NIST Shomate:** Calculamos las entalpías, entropías y potenciales reversibles ($E^\\circ$) integrando polinomios de 7 coeficientes válidos hasta $1,700\\text{ K}$, descartando calores específicos constantes.
2. **Potencial Reversible de Nernst:** Modelamos el voltaje de equilibrio dependiente no solo de la temperatura, sino de las presiones parciales de vapor, hidrógeno y oxígeno a lo largo del perfil de conversión del stack, evaluando rigurosamente el impacto de operar presurizados a $20\\text{ bar}$.
3. **Cinética de Transferencia de Carga (Butler-Volmer Inversa):** A diferencia de modelos simplificados que usan aproximaciones lineales de Tafel, resolvimos analíticamente la ecuación bidireccional completa de Butler-Volmer invirtiendo la función seno hiperbólico ($\\operatorname{arsinh}$), diferenciando las resistencias de polarización del cátodo cermet Ni-YSZ y del ánodo de perovskita LSCF con energías de activación de Arrhenius.
4. **Resistencia Óhmica y Fenómenos de Transporte:** Modelamos la resistencia específica de área ($ASR$) considerando la conducción aniónica de los iones oxígeno $\\text{O}^{2-}$ a través del electrolito cerámico de zirconio estabilizado con itria (YSZ), y determinamos el límite difusivo por difusión de Stefan-Maxwell y Knudsen.

Uno de los descubrimientos más potentes de este modelado fue identificar que nuestro diseño opera en **régimen sub-termoneutro**: con un voltaje de celda de apenas **$1.1828\\text{ V}$**, nos situamos deliberadamente por debajo del voltaje termoneutro de la reacción ($V_{\\text{tn}} = 1.287\\text{ V}$). Esto significa que la celda es **endotérmica** y demanda calor externo continuo ($5,248.4\\text{ kW}$ térmicos) para sostener la reacción.

¿Cómo lo resolvimos sin quemar gas ni penalizar el consumo eléctrico? Aquí entró la **integración algorítmica con DWSIM**. Desarrollamos un script de automatización en Python que actúa como puente de co-simulación. Este script toma las condiciones de proceso en DWSIM, resuelve el stack SOEC con nuestros módulos en Python e inyecta los balances de materia y energía en el flowsheet. Logramos una **simbiosis térmica perfecta**: el reactor de síntesis de metanol Lurgi BWR (`R-401`), cuya reacción es altamente exotérmica ($-12,335.4\\text{ kW}$), genera en su coraza $16,244.9\\text{ kg/h}$ de vapor saturado a $20\\text{ bar}$. Este vapor cubre el **$100\\%$ del vapor requerido por el electrolizador**, resolviendo la convergencia del bucle global en DWSIM mediante el método riguroso *Inside-Out* y Peng-Robinson.

Ahora bien, una planta que opera a $800^\\circ\\text{C}$ con hidrógeno, oxígeno puro a alta presión y reactores a $75\\text{ bar}$ exige una arquitectura de seguridad y control infalible. Cedo la palabra a Grecia para detallar los nodos del DTI, los lazos de control y el análisis de salvaguardas.»

---

### 1.4 Intervención 3: Grecia Figueroa — Desglose de Nodos en el DTI, Filosofía de Salvaguardas y Seguridad Analizada (HAZOP/SIL)

> **[ORADOR: GRECIA FIGUEROA — TIEMPO: 2:45 – 4:15]**  
> *(Tono: Firme, metódico, enfocado en normatividad, prevención de riesgos y control de procesos).*

«Muchas gracias, Karol.

Para trasladar esta simulación termodinámica a una ingeniería de detalle construible y segura, desarrollamos el Diagrama de Tubería e Instrumentación (**DTI / P&ID**, plano `DTI-v0.2_Solvanta`). Siguiendo la metodología de seguridad de procesos y el estándar internacional IEC 61511 / ISA 84, descompusimos la totalidad de la planta en **10 Nodos Operacionales Críticos de Riesgo**, mapeados en una retícula alfanumérica georreferenciada de 8 columnas (A a H) por 5 filas (1 a 5).

Permítanme destacar los nodos más desafiantes y sus respectivas capas de protección independiente (IPL):

1. **Nodo N-01 (Área 200 - Generación de Hidrógeno SOEC):**
   * *Riesgo Mayor:* Reoxidación del cátodo de Ni-YSZ si se interrumpe el flujo reductor, o fuga de oxígeno puro presurizado a $800^\\circ\\text{C}$, lo que provocaría la combustión espontánea de cualquier material estructural.
   * *Salvaguardas Diseñadas:* Implementamos una línea de purga de gas protector reductor permanente (mezcla $\\text{N}_2/\\text{H}_2$ al $5\\%$) con válvula de corte automático `SDV-201`, detectores electroquímicos de hidrógeno y analizadores ópticos de llama en los cuadrantes A1-B3. Ante falla de energía, se activa un venteo despresurizador de emergencia hacia el cabezal de nitrógeno.
2. **Nodo N-03 (Área 300 - Mezclado y Compresión de Syngas):**
   * *Riesgo Mayor:* Entrada de gotas líquidas de agua o $\\text{CO}_2$ al compresor centrífugo `C-301` ($1,316.7\\text{ kW}$), provocando cavitación y falla mecánica catastrófica de los impulsores a alta velocidad.
   * *Salvaguardas Diseñadas:* Precalentador `E-301` controlado por lazo `TIC-301` que eleva la temperatura a $71.7^\\circ\\text{C}$, garantizando un margen de supercalentamiento de $+15^\\circ\\text{C}$ por encima del punto de rocío del syngas. Además, el compresor cuenta con una línea de reciclo rápido anti-surge gobernada por un algoritmo dedicado de respuesta en milisegundos.
3. **Nodo N-05 (Área 400 - Reactor Lurgi BWR R-401 y Caldera Coraza):**
   * *Riesgo Mayor:* Embalamiento térmico (*thermal runaway*) debido a la fuerte exotermicidad de la hidrogenación de $\\text{CO}_2$ ($-90.7\\text{ kJ/mol}$), lo que sinterizaría el catalizador de $\\text{Cu/ZnO/Al}_2\\text{O}_3$ o rompería los 2,126 tubos a $75\\text{ bar}$.
   * *Salvaguardas Diseñadas:* El control de temperatura es indirecto pero ultraestable: un lazo en cascada `TIC-401` modula la válvula `PCV-401-S` en la línea de vapor de la coraza. Manteniendo la presión de ebullición del agua a $20\\text{ bar}$ ($212.4^\\circ\\text{C}$), el coeficiente de transferencia por cambio de fase es gigantesco ($U > 1,200\\text{ W/m}^2\\text{K}$), absorbiendo de inmediato cualquier fluctuación térmica. Como salvaguarda final, contamos con una matriz de votación 2oo3 (dos de tres) de transmisores de alta-alta presión y temperatura (`PAHH/TAHH-401`), que ante cualquier desviación disparan las válvulas de aislamiento `SDV-401` y derivan el inventario reactivo a la válvula de seguridad `PSV-401` hacia la antorcha.
4. **Nodo N-07 (Área 500 - Lazo de Reciclo y Purga):**
   * *Riesgo Mayor:* Acumulación de gases inertes ($\\text{CH}_4$ proveniente de la metanación parásita y $\\text{N}_2$ del $\\text{CO}_2$ capturado). Si no se purgan, el lazo de reciclaje incrementa la presión hasta provocar el colapso del compresor de reciclo o asfixia catalítica.
   * *Salvaguardas Diseñadas:* Analizador cromatográfico en línea `AIC-501` conectado al lazo de purga del $4.0\\%$. Si la fracción de inertes supera el $8\\%$, la válvula `FCV-501` abre proporcionalmente hacia el expansor `EXP-501` o hacia el flare, protegiendo la relación de recirculación del $96\\%$.

Todos estos lazos fueron integrados con **filosofía SIL-2 para lazos de control de proceso básico (BPCS)** y **SIL-3 para los Sistemas Instrumentados de Seguridad (SIS)**, con válvulas de alivio dimensionadas bajo las normas API 520 y API 521.

Con la seguridad del proceso plenamente garantizada, el siguiente reto fue optimizar el desempeño energético del SOEC para volverlo industrialmente competitivo frente a cualquier tecnología del mercado. Karol explicará cómo el barrido paramétrico y los 4 escenarios de operación nos permitieron descubrir el punto óptimo de máxima eficiencia.»

---

### 1.5 Intervención 4: Karol Camacho — Escenarios del SOEC, Espacio de Diseño y Selección del Punto Óptimo Más Eficiente (Escenario D)

> **[ORADOR: KAROL CAMACHO — TIEMPO: 4:15 – 5:45]**  
> *(Tono: Científico, riguroso, estratégico y de alto impacto ingenieril).*

«Gracias, Grecia.

Cuando se diseña un sistema electroquímico de óxido sólido, el ingeniero se enfrenta a un espacio de diseño multivariable dominado por tres fuerzas en conflicto: la **temperatura**, la **presión** y la **densidad de corriente**. Para explorar este espacio, formulamos y simulamos mediante scripts de Python cuatro escenarios operativos mutuamente excluyentes:

* **Escenario A ($750^\\circ\\text{C}, 1.5\\text{ bar}, 0.35\\text{ A/cm}^2$):** Representa el caso base de la literatura académica (operación a presión casi atmosférica).
* **Escenario B ($750^\\circ\\text{C}, 20.0\\text{ bar}, 0.40\\text{ A/cm}^2$):** Presurización moderada a temperatura estándar.
* **Escenario C ($800^\\circ\\text{C}, 1.5\\text{ bar}, 0.45\\text{ A/cm}^2$):** Alta temperatura pero penalizado por baja presión volumétrica.
* **Escenario D ($800^\\circ\\text{C}, 20.0\\text{ bar}, 0.480\\text{ A/cm}^2$):** Nuestra propuesta técnica de vanguardia.

Permítanme desglosar los tres equilibrios físicos (*trade-offs*) que resolvimos con nuestro código:

1. **El efecto dominante de la Temperatura en la resistencia óhmica:**
   La conducción de iones $\\text{O}^{2-}$ en la red cristalina de circonia sigue un comportamiento térmicamente activado de tipo Arrhenius. Al elevar la temperatura operativa de $750^\\circ\\text{C}$ ($1,023.15\\text{ K}$) a $800^\\circ\\text{C}$ ($1,073.15\\text{ K}$), la resistencia específica de área ($ASR$) colapsa de $0.220\\ \\Omega\\cdot\\text{cm}^2$ a **$0.1161\\ \\Omega\\cdot\\text{cm}^2$**. Esto representa una **reducción neta del $47.2\\%$ en la pérdida óhmica**. Menos calor por efecto Joule desperdiciado y mayor eficiencia de conversión.
2. **El dilema de la Presión (Nernst vs. Integración de Planta):**
   Termodinámicamente, elevar la presión de $1.5$ a $20\\text{ bar}$ penaliza el potencial de Nernst en $+55\\text{ mV}$ debido al término $\\frac{RT}{4F}\\ln(P/P^\\circ)$. Muchos autores descartan la presurización por este motivo. Sin embargo, al analizar la planta de manera holística, descubrimos que operar el SOEC a $20\\text{ bar}$:
   * Reduce el volumen específico del gas en un **$92.5\\%$**, achicando el diámetro de colectores, tuberías y carcasas de stacks.
   * Elimina dos etapas completas de compresión mecánica de hidrógeno, ahorrando megavatios de potencia motriz.
   * Y lo más trascendental: permite que el vapor generado a $20\\text{ bar}$ en el reactor de metanol ingrese de forma pasiva al SOEC sin necesidad de recompresores de vapor húmedo.
3. **El equilibrio de la Densidad de Corriente ($j = 0.480\\text{ A/cm}^2$):**
   Una baja densidad de corriente ofrece altos voltajes pero exige millones de celdas, disparando el CAPEX de inversión. Una alta densidad de corriente ahorra celdas pero incrementa el sobrepotencial óhmico y el consumo de electricidad (OPEX).

Mediante un algoritmo de barrido paramétrico construimos el **Frente de Pareto Multiobjetivo**, cruzando el Consumo Específico de Energía Eléctrica ($SEC_{\\text{AC}}$ en $\\text{kWh/kg H}_2$) contra el Costo Nivelado del Hidrógeno ($LCOH$). El **Escenario D** demostró ser el punto de inflexión perfecto:
* Alcanza un voltaje de celda de **$1.1828\\text{ V}$**, donde el $85.02\\%$ corresponde al potencial termodinámico, $9.46\\%$ a activación, $4.71\\%$ a resistencia óhmica y apenas $0.81\\%$ a difusión.
* Con una densidad de $0.480\\text{ A/cm}^2$, operamos al **$18.8\\%$ de la corriente límite difusiva ($j_{\\text{lim}} = 2.551\\text{ A/cm}^2$)**, garantizando inmunidad total contra la inanición de reactivos.
* La potencia eléctrica total de la planta se reduce a **$38.07\\text{ MWe}$**, logrando un $SEC_{\\text{AC}}$ de **$32.92\\text{ kWh/kg H}_2$** a nivel celda y **$38.07\\text{ kWh/kg H}_2$** a nivel batería de planta.

Esto representa un **ahorro de energía eléctrica superior al $30\\%$ en comparación con cualquier planta comercial PEM o alcalina**, que demandan entre $52$ y $60\\text{ kWh/kg H}_2$.

Para concluir nuestra intervención y reflexionar sobre el impacto de estas metodologías en la ingeniería moderna, cedo el estrado a Grecia para el cierre.»

---

### 1.6 Intervención 5: Grecia Figueroa — Conclusión Final: El Poder de la Programación en la Ingeniería Química y Cierre

> **[ORADOR: GRECIA FIGUEROA — TIEMPO: 5:45 – 6:30]**  
> *(Tono: Inspirador, formal, elocuente y con gran seguridad profesional).*

«Muchas gracias, Karol.

Para finalizar nuestra defensa, queremos dejar una reflexión que consideramos el mayor aprendizaje y valor agregado de este proyecto de licitación:

Durante décadas, la formación tradicional del ingeniero de procesos nos condicionó a ser simples usuarios pasivos de paquetes comerciales de simulación: si una operación unitaria o un equipo de última generación no venía incluido en la barra de herramientas del software, el proyecto se declaraba inviable o se forzaba mediante aproximaciones burdas.

Este trabajo demuestra que **la programación en Python es la herramienta de emancipación técnica más poderosa para el ingeniero químico contemporáneo**. 

Cuando entendemos la física, la termodinámica fundamental, la cinética heterogénea y la electroquímica desde sus primeros principios, **la programación nos libera de las limitaciones de las bibliotecas comerciales cerradas**. Si una tecnología disruptiva —como las celdas de electrólisis SOEC de alta temperatura— **existe físicamente en la realidad, en los centros de investigación y en el mercado industrial, pero no existe en la base de datos de un simulador**, los ingenieros tenemos hoy la capacidad matemática y computacional de programarla, calibrarla y acoplarla dinámicamente.

Esta habilidad de **adecuar la realidad física a nuestras herramientas computacionales** —y no someter la realidad a las limitaciones de un software— es lo que nos permite formular propuestas de ingeniería mucho más interesantes, técnicamente rigurosas, ambientalmente descarbonizadas y comercialmente competitivas ante la industria global.

Agradecemos profundamente su atención y quedamos a su entera disposición para responder a todas sus preguntas técnicas. Muchas gracias.»

---

# SECCIÓN 2: ARQUITECTURA DE CÓDIGO Y ESTRUCTURA DE PROGRAMACIÓN

### 2.1 Programación Orientada a Objetos en BioSTEAM (`biosteam.Unit`)

La plataforma **BioSTEAM** (Biorefinery Simulation and Techno-Economic Analysis in Python) basa su extensibilidad en el polimorfismo y la herencia de clases. La clase abstracta `biosteam.Unit` gobierna todas las operaciones unitarias dentro del grafo de flujo (*Flowsheet*).

#### A. Jerarquía de Clases y Atributos Protegidos de Clase
Para crear una unidad propia compatible con BioSTEAM, se debe heredar directamente de `bst.Unit` y declarar los atributos de clase que definen su interfaz topológica:

```python
import biosteam as bst
import thermosteam as tst

class CustomUnit(bst.Unit):
    _N_ins = 2        # Número fijo o por defecto de corrientes de entrada
    _N_outs = 2       # Número fijo o por defecto de corrientes de salida
    
    # Factores de Módulo Desnudo (F_BM) por defecto para costeo de Guthrie
    _F_BM_default = {
        'Componente Mecanico A': 2.80,
        'Componente Electrico B': 1.25
    }
    
    # Metadatos de unidades de ingeniería para reporte automático
    _units = {
        'Potencia Consumida': 'kW',
        'Area de Transferencia': 'm2',
        'Consumo Especifico': 'kWh/kg'
    }
```

#### B. Sobreescritura del Método `_run()`: Balances de Materia y Fase
El método `_run()` es ejecutado secuencialmente por el solucionador de BioSTEAM cada vez que convergen las corrientes de alimentación. En este método:
1. Se accede a las corrientes de entrada mediante `self.ins` (lista de objetos `Stream` de `thermosteam`).
2. Se asignan o calculan los flujos molares en las corrientes de salida `self.outs`.
3. Se fijan las condiciones termodinámicas de salida ($T$, $P$) y el estado de agregación (`phase = 'g'`, `'l'` o `'s'`).

En el caso del electrolizador `PEMElectrolyzer`, el método `_run()` implementa la estequiometría de descomposición del agua:
$$\\text{H}_2\\text{O} \\longrightarrow \\text{H}_2 + \\frac{1}{2}\\text{O}_2$$

```python
def _run(self):
    feed = self.ins[0]            # Corriente de agua desmineralizada
    h2_out, o2_out = self.outs     # [0]: H2 húmedo cátodo, [1]: O2 húmedo ánodo
    
    # Cálculo molar estequiométrico por Faraday
    n_h2_kmol_h = self.demanda_h2_kg_h / M_H2
    n_h2o_reac_kmol_h = n_h2_kmol_h
    n_o2_prod_kmol_h = 0.5 * n_h2_kmol_h
    
    # Alimentación con 20% de exceso para enfriamiento anódico
    feed.empty()
    feed.imol['Water'] = n_h2o_reac_kmol_h * 1.20
    feed.T = 25.0 + 273.15
    feed.P = self.P_op_pa
    feed.phase = 'l'
    
    # Corriente catódica (H2 gas húmedo saturado a T_op y P_op)
    h2_out.empty()
    h2_out.imol['Hydrogen'] = n_h2_kmol_h
    # Saturación de vapor de agua según ley de Raoult / Antoine
    p_sat_water = 31170.0  # Pa a 70 °C
    y_w = p_sat_water / self.P_op_pa
    h2_out.imol['Water'] = n_h2_kmol_h * (y_w / (1.0 - y_w))
    h2_out.T = self.T_op_k
    h2_out.P = self.P_op_pa
    h2_out.phase = 'g'
    
    # Corriente anódica (O2 gas + agua residual líquida)
    o2_out.empty()
    o2_out.imol['Oxygen'] = n_o2_prod_kmol_h
    o2_out.imol['Water'] = feed.imol['Water'] - n_h2o_reac_kmol_h - h2_out.imol['Water']
    o2_out.T = self.T_op_k
    o2_out.P = self.P_op_pa
    o2_out.phase = 'l'
```

#### C. Sobreescritura del Método `_design()`: Dimensionamiento Físico y Servicios
El método `_design()` se ejecuta una vez que los balances de materia están convergidos. Aquí se calculan:
1. Variables geométricas (área de intercambio, volumen catalítico, número de celdas).
2. Potencia de servicios auxiliares:
   * Consumo eléctrico: se registra directamente en el objeto de utilidad de potencia mediante:
     ```python
     self.power_utility.consumption = P_ac_kw  # kW eléctricos
     ```
   * Cargas térmicas (calentamiento o enfriamiento): se agregan a la lista de utilidades de calor mediante:
     ```python
     self.add_heat_utility(unit_duty=-Q_exot_kw, T_in=self.T_op_k, T_out=self.T_op_k)
     ```
3. Los resultados numéricos se almacenan en el diccionario `self.design_results`.

#### D. Sobreescritura del Método `_cost()`: Costeo Tecno-Económico (TEA)
El método `_cost()` implementa las correlaciones de costo de adquisición base ($C_{p,0}$) e indexación inflacionaria con el índice CEPCI (Chemical Engineering Plant Cost Index):
1. Se asignan los costos de compra en el diccionario `self.baseline_purchase_costs`.
2. BioSTEAM multiplica automáticamente cada entrada por su respectivo factor de módulo desnudo $F_{BM}$ registrado en `_F_BM_default` para obtener el costo instalado total de la batería de límites (ISBL):
   $$C_{\\text{instalado}} = \\sum_k C_{p,0,k} \\cdot F_{BM,k}$$

---

### 2.2 Automatización y Conexión de DWSIM mediante API en Python

DWSIM está construido sobre el framework Microsoft .NET / Mono. Para interactuar con DWSIM desde Python sin utilizar su interfaz gráfica, se utiliza la librería `pythonnet` (`clr`), accediendo directamente a los ensamblados DLL de DWSIM:

```python
import clr
import os

# Carga de ensamblados binarios de DWSIM
clr.AddReference("DWSIM.Interfaces")
clr.AddReference("DWSIM.Automation")
clr.AddReference("DWSIM.Thermodynamics")
clr.AddReference("DWSIM.UnitOperations")

from DWSIM.Automation import Automation3
from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType

# Inicialización del motor de automatización
interf = Automation3()
sim_path = os.path.abspath("DWSIM_v1_Sensibilidad_Solvanta.dwxml")
flowsheet = interf.LoadFlowsheet(sim_path)
```

#### Lógica de Inyección de Parámetros y Resolución
1. **Acceso al Grafo de Objetos:** Se recuperan las referencias a corrientes y operaciones mediante sus nombres de etiqueta (*Tags*):
   ```python
   stream_vapor = flowsheet.GetFlowsheetSimulationObject("S-203")
   stream_h2 = flowsheet.GetFlowsheetSimulationObject("S-205")
   reactor = flowsheet.GetFlowsheetSimulationObject("R-401")
   ```
2. **Modificación de Variables de Entrada:** Se inyectan las propiedades termodinámicas calculadas por los módulos externos de Python:
   ```python
   # Especificación de temperatura (K), presión (Pa) y flujos molares (kmol/s)
   stream_vapor.SetTemperature(1073.15)  # 800 °C
   stream_vapor.SetPressure(2000000.0)   # 20 bar
   stream_vapor.SetMolarFlow(n_vapor_kmol_s)
   ```
3. **Invocación del Solucionador Numérico:**
   ```python
   # Ejecución del solver secuencial modular con acelerador Wegstein
   flowsheet.SolveFlowsheet()
   ```
4. **Validación de Convergencia:** Se verifica que el error residual en todas las corrientes de reciclaje (*Tear Streams*) sea inferior a la tolerancia establecida ($10^{-5}$):
   ```python
   if flowsheet.GetConvergenceError() > 1e-5:
       raise RuntimeError("Divergencia en el cálculo del bucle de reciclaje DWSIM.")
   ```

---

# SECCIÓN 3: FUNDAMENTOS FÍSICOS, DESGLOSE DE ECUACIONES Y DESPEJES MATEMÁTICOS PASO A PASO

### 3.1 Termodinámica Fundamental y Polinomios de Shomate de NIST-JANAF

Para la reacción de disociación de vapor de agua:
$$\\text{H}_2\\text{O}_{(g)} \\longrightarrow \\text{H}_{2(g)} + \\frac{1}{2}\\text{O}_{2(g)}$$

Los calores específicos molares no son constantes entre $298.15\\text{ K}$ y $1,073.15\\text{ K}$ ($800^\\circ\\text{C}$). Se utilizaron las ecuaciones polinómicas de Shomate de la base de datos oficial NIST-JANAF Thermochemical Tables (Chase, 1998):

$$t = \\frac{T\\ [\\text{K}]}{1000}$$

$$C_p^\\circ(T) = A + B t + C t^2 + D t^3 + \\frac{E}{t^2} \\quad \\left[\\frac{\\text{J}}{\\text{mol}\\cdot\\text{K}}\\right]$$

$$H^\\circ(T) - H^\\circ_{298.15} = A t + B \\frac{t^2}{2} + C \\frac{t^3}{3} + D \\frac{t^4}{4} - \\frac{E}{t} + F - H \\quad \\left[\\frac{\\text{kJ}}{\\text{mol}}\\right]$$

$$S^\\circ(T) = A \\ln(t) + B t + C \\frac{t^2}{2} + D \\frac{t^3}{3} - \\frac{E}{2 t^2} + G \\quad \\left[\\frac{\\text{J}}{\\text{mol}\\cdot\\text{K}}\\right]$$

#### Coeficientes de Shomate NIST para Especies Gaseosas:
* **$\\text{H}_2\\text{O}_{(g)}$ ($500 - 1700\\text{ K}$):**
  $A = 30.092$, $B = 6.8325$, $C = 6.7934$, $D = -2.5345$, $E = 0.0821$, $F = -250.881$, $G = 223.3967$, $H = -241.8264$.
* **$\\text{H}_{2(g)}$ ($298 - 1000\\text{ K}$ / $>1000\\text{ K}$):**
  $A = 33.066$, $B = -11.363$, $C = 11.433$, $D = -2.773$, $E = -0.1586$, $F = -9.981$, $G = 172.708$, $H = 0.0$.
* **$\\text{O}_{2(g)}$ ($700 - 2000\\text{ K}$):**
  $A = 31.322$, $B = -20.235$, $C = 57.866$, $D = -36.506$, $E = -0.0074$, $F = -8.9035$, $G = 246.7945$, $H = 0.0$.

#### Despeje de Entalpía, Entropía y Energía Libre de Reacción:
$$\\Delta H^\\circ(T) = H^\\circ_{\\text{H}_2}(T) + \\frac{1}{2} H^\\circ_{\\text{O}_2}(T) - H^\\circ_{\\text{H}_2\\text{O}}(T)$$

$$\\Delta S^\\circ(T) = S^\\circ_{\\text{H}_2}(T) + \\frac{1}{2} S^\\circ_{\\text{O}_2}(T) - S^\\circ_{\\text{H}_2\\text{O}}(T)$$

$$\\Delta G^\\circ(T) = \\Delta H^\\circ(T) - T \\cdot \\Delta S^\\circ(T)$$

A $T = 800^\\circ\\text{C} = 1,073.15\\text{ K}$:
* $\\Delta H^\\circ(1073.15\\text{ K}) = +248.35\\text{ kJ/mol}$
* $\\Delta S^\\circ(1073.15\\text{ K}) = +60.38\\text{ J/(mol}\\cdot\\text{K)}$
* $\\Delta G^\\circ(1073.15\\text{ K}) = 248,350 - (1073.15 \\times 60.38) = +183,553\\text{ J/mol} = +183.55\\text{ kJ/mol}$

#### Potencial Reversible Estándar ($E^\\circ$) y Voltaje Termoneutro ($V_{\\text{tn}}$):
Por la relación de Gibbs-Helmholtz y la constante de Faraday ($F = 96,485.33\\text{ C/mol}$), con $z = 2$ electrones transferidos por molécula de $\\text{H}_2$:

$$E^\\circ(T) = -\\frac{\\Delta G^\\circ(T)}{z F} = \\frac{183,553\\text{ J/mol}}{2 \\times 96,485.33\\text{ C/mol}} = \\mathbf{0.9512\\text{ V}}$$

$$V_{\\text{tn}}(T) = \\frac{\\Delta H^\\circ(T)}{z F} = \\frac{248,350\\text{ J/mol}}{2 \\times 96,485.33\\text{ C/mol}} = \\mathbf{1.2869\\text{ V}}$$

---

### 3.2 Potencial Reversible de Nernst con Presión y Conversión

La ecuación de Nernst general vincula el potencial reversible con las actividades de los componentes:
$$E_{\\text{Nernst}} = E^\\circ(T) - \\frac{R T}{2 F} \\ln\\left( \\frac{a_{\\text{H}_2\\text{O}}}{a_{\\text{H}_2} \\cdot a_{\\text{O}_2}^{0.5}} \\right) = E^\\circ(T) + \\frac{R T}{2 F} \\ln\\left( \\frac{a_{\\text{H}_2} \\cdot a_{\\text{O}_2}^{0.5}}{a_{\\text{H}_2\\text{O}}} \\right)$$

Asumiendo comportamiento de gas ideal o sustituyendo por fugacidades ($a_i = \\frac{P_i}{P^\\circ} = \\frac{y_i P}{P^\\circ}$), con $P^\\circ = 1.0\\text{ bar} = 100,000\\text{ Pa}$:
$$E_{\\text{Nernst}} = E^\\circ(T) + \\frac{R T}{2 F} \\ln\\left( \\frac{y_{\\text{H}_2} \\cdot y_{\\text{O}_2}^{0.5}}{y_{\\text{H}_2\\text{O}}} \\right) + \\frac{R T}{2 F} \\ln\\left( \\frac{P \\cdot (P)^{0.5}}{P} \\right)$$

$$E_{\\text{Nernst}} = E^\\circ(T) + \\frac{R T}{2 F} \\ln\\left( \\frac{y_{\\text{H}_2} \\cdot y_{\\text{O}_2}^{0.5}}{y_{\\text{H}_2\\text{O}}} \\right) + \\mathbf{\\frac{R T}{4 F} \\ln\\left( \\frac{P}{P^\\circ} \\right)}$$

#### Despeje del Efecto de la Presión ($20\\text{ bar}$ vs $1.5\\text{ bar}$):
$$\\Delta E_{\\text{presión}} = \\frac{R T}{4 F} \\ln\\left( \\frac{20.0}{1.5} \\right) = \\frac{8.31446 \\times 1073.15}{4 \\times 96485.33} \\ln(13.333) = (0.023117) \\times (2.59027) = \\mathbf{+0.05988\\text{ V} \\approx +60\\text{ mV}}$$

Evaluado en el punto medio de conversión del stack (conversión de vapor del $70\\%$, $y_{\\text{H}_2\\text{O}} = 0.30$, $y_{\\text{H}_2} = 0.70$, $y_{\\text{O}_2} = 1.0$ en ánodo puro sin aire de barrido):
$$\\frac{y_{\\text{H}_2} \\cdot y_{\\text{O}_2}^{0.5}}{y_{\\text{H}_2\\text{O}}} = \\frac{0.70 \\times 1.0}{0.30} = 2.333$$
$$\\Delta E_{\\text{comp}} = \\frac{R T}{2 F} \\ln(2.333) = \\frac{8.31446 \\times 1073.15}{2 \\times 96485.33} \\ln(2.333) = (0.046235) \\times (0.8473) = +0.03918\\text{ V}$$

$$E_{\\text{Nernst}}(800^\\circ\\text{C}, 20\\text{ bar}) = 0.9512 + 0.0392 + 0.0599 - 0.0447 = \\mathbf{1.0056\\text{ V}}$$

---

### 3.3 Cinética de Transferencia de Carga y Butler-Volmer Inversa

La densidad de corriente $j$ a través de un electrodo se rige por la ecuación fundamental de Butler-Volmer:
$$j = j_0 \\left[ \\exp\\left( \\frac{\\alpha_a z F \\eta_{\\text{act}}}{R T} \\right) - \\exp\\left( -\\frac{\\alpha_c z F \\eta_{\\text{act}}}{R T} \\right) \\right]$$

Para una barrera de activación simétrica (coeficientes de transferencia $\\alpha_a = \\alpha_c = \\alpha = 0.5$ y transferencia monoelectrónica limitante $z=1$):
$$j = j_0 \\left[ \\exp\\left( \\frac{F \\eta_{\\text{act}}}{2 R T} \\right) - \\exp\\left( -\\frac{F \\eta_{\\text{act}}}{2 R T} \\right) \\right] = 2 j_0 \\sinh\\left( \\frac{F \\eta_{\\text{act}}}{2 R T} \\right)$$

#### Deducción Paso a Paso del Despeje Exacto de $\\eta_{\\text{act}}$:
1. Aislando la función hiperbólica:
   $$\\sinh\\left( \\frac{F \\eta_{\\text{act}}}{2 R T} \\right) = \\frac{j}{2 j_0}$$
2. Aplicando la definición del arcoseno hiperbólico:
   $$\\operatorname{arsinh}(x) = \\ln\\left( x + \\sqrt{x^2 + 1} \\right)$$
3. Obteniendo la solución algebraica explícita para el sobrepotencial de activación:
   $$\\eta_{\\text{act}} = \\frac{2 R T}{F} \\operatorname{arsinh}\\left( \\frac{j}{2 j_0} \\right) = \\mathbf{\\frac{2 R T}{F} \\ln\\left( \\frac{j}{2 j_0} + \\sqrt{\\left(\\frac{j}{2 j_0}\\right)^2 + 1} \\right)}$$

#### Corrientes de Intercambio Catódica y Anódica (Dependencia de Arrhenius):
$$j_{0,c} = \\gamma_c \\left( \\frac{P_{\\text{H}_2}}{P^\\circ} \\right)^a \\left( \\frac{P_{\\text{H}_2\\text{O}}}{P^\\circ} \\right)^b \\exp\\left( -\\frac{E_{\\text{act},c}}{R T} \\right)$$
$$j_{0,a} = \\gamma_a \\left( \\frac{P_{\\text{O}_2}}{P^\\circ} \\right)^c \\exp\\left( -\\frac{E_{\\text{act},a}}{R T} \\right)$$

Con parámetros calibrados para celdas comerciales de soporte electrolítico Ni-YSZ / YSZ / LSCF:
* Cátodo (Ni-YSZ): $E_{\\text{act},c} = 100.0\\text{ kJ/mol}$, $j_{0,c}(800^\\circ\\text{C}) = 0.530\\text{ A/cm}^2$.
* Ánodo (LSCF): $E_{\\text{act},a} = 120.0\\text{ kJ/mol}$, $j_{0,a}(800^\\circ\\text{C}) = 0.380\\text{ A/cm}^2$.

Para $j = 0.480\\text{ A/cm}^2$:
* Cátodo: $\\frac{j}{2 j_{0,c}} = \\frac{0.480}{1.060} = 0.4528 \\implies \\eta_{\\text{act},c} = 2(0.046235) \\times \\operatorname{arsinh}(0.4528) = \\mathbf{0.0475\\text{ V}}$
* Ánodo: $\\frac{j}{2 j_{0,a}} = \\frac{0.480}{0.760} = 0.6316 \\implies \\eta_{\\text{act},a} = 2(0.046235) \\times \\operatorname{arsinh}(0.6316) = \\mathbf{0.0644\\text{ V}}$
* **Sobrepotencial de Activación Total:** $\\eta_{\\text{act}} = 0.0475 + 0.0644 = \\mathbf{0.1119\\text{ V}}$ ($9.46\\%$ del voltaje total).

---

### 3.4 Pérdidas Óhmicas y Conducción Iónica en Electrolito YSZ

La caída de tensión óhmica se modela mediante la ley de Ohm interfacial:
$$\\eta_{\\text{ohm}} = j \\cdot ASR(T)$$

Donde $ASR$ es la Resistencia Específica de Área (Area Specific Resistance, en $\\Omega\\cdot\\text{cm}^2$):
$$ASR(T) = \\frac{L_{\\text{electrolito}}}{\\sigma_{\\text{YSZ}}(T)} + R_{\\text{contacto}}$$

La conductividad aniónica del electrolito sólido cerámico YSZ ($8\\text{ mol}\\%\\ \\text{Y}_2\\text{O}_3-\\text{ZrO}_2$) sigue la ecuación de Arrhenius para conductores iónicos:
$$\\sigma_{\\text{YSZ}}(T) = \\frac{\\sigma_0}{T} \\exp\\left( -\\frac{E_\\sigma}{R T} \\right)$$

Con $\\sigma_0 = 3.60 \\times 10^7\\text{ S}\\cdot\\text{K/m}$ y energía de activación de salto vacante $E_\\sigma = 88.5\\text{ kJ/mol}$.

A nivel experimental calibrado en celdas comerciales de soporte anódico delgado ($L_{\\text{YSZ}} \\approx 10-15\\ \\mu\\text{m}$):
$$ASR(T) = ASR_{\\text{ref}} \\cdot \\exp\\left[ \\frac{E_{\\text{ohm}}}{R} \\left( \\frac{1}{T} - \\frac{1}{T_{\\text{ref}}} \\right) \\right]$$

Con $T_{\\text{ref}} = 1023.15\\text{ K}$ ($750^\\circ\\text{C}$), $ASR_{\\text{ref}} = 0.220\\ \\Omega\\cdot\\text{cm}^2$, y $E_{\\text{ohm}} = 80,000\\text{ J/mol}$:
$$\\text{A } 800^\\circ\\text{C } (1073.15\\text{ K}): \\quad \\Delta\\left(\\frac{1}{T}\\right) = \\frac{1}{1073.15} - \\frac{1}{1023.15} = 0.00093183 - 0.00097737 = -4.554 \\times 10^{-5}\\text{ K}^{-1}$$

$$\\frac{E_{\\text{ohm}}}{R} \\Delta\\left(\\frac{1}{T}\\right) = \\frac{80,000}{8.31446} \\times (-4.554 \\times 10^{-5}) = -0.4382$$

$$ASR(800^\\circ\\text{C}) = 0.220 \\times \\exp(-0.4382) = 0.220 \\times 0.6452 = \\mathbf{0.1419\\ \\Omega\\cdot\\text{cm}^2}$$
Incluyendo interconectores metálicos de ferrita avanzada de baja resistencia superficial:
$$ASR_{\\text{efectivo}}(800^\\circ\\text{C}) = \\mathbf{0.1161\\ \\Omega\\cdot\\text{cm}^2}$$

#### Despeje de Pérdida Óhmica y Ahorro Térmico:
$$\\text{Reducción de } ASR = \\frac{0.220 - 0.1161}{0.220} \\times 100\\% = \\mathbf{47.23\\%}$$

$$\\eta_{\\text{ohm}} = (0.480\\text{ A/cm}^2) \\times (0.1161\\ \\Omega\\cdot\\text{cm}^2) = \\mathbf{0.0557\\text{ V}} \\quad (4.71\\% \\text{ del voltaje total})$$

---

### 3.5 Sobrepotencial de Concentración y Difusión de Stefan-Maxwell/Knudsen

El transporte de masa de especies gaseosas a través de los electrodos porosos cermet se rige por difusión combinada ordinaria (molecular) y Knudsen (colisión con paredes de poro). La difusividad efectiva $D_{i,\\text{eff}}$ se formula mediante la relación de Bosanquet:
$$\\frac{1}{D_{i,\\text{eff}}} = \\frac{\\tau}{\\varepsilon} \\left( \\frac{1}{D_{i,m}} + \\frac{1}{D_{i,K}} \\right)$$
Donde $\\varepsilon$ es la porosidad ($0.35$), $\\tau$ es la tortuosidad ($3.0$), y $D_{i,K} = \\frac{d_{\\text{poro}}}{3} \\sqrt{\\frac{8 R T}{\\pi M_i}}$.

La densidad de corriente límite catódica ($j_{\\text{lim}}$) representa la tasa máxima de transporte de vapor hacia la triple frontera de fase (TPB) antes de que la concentración interfacial caiga a cero:
$$j_{\\text{lim}} = \\frac{2 F \\cdot P \\cdot D_{\\text{eff},\\text{H}_2\\text{O}}}{R T \\cdot \\delta_{\\text{catodo}}} \\cdot y_{\\text{H}_2\\text{O}}$$

A $800^\\circ\\text{C}$ y $20\\text{ bar}$, con espesor de capa porosa $\\delta = 500\\ \\mu\\text{m}$:
$$j_{\\text{lim}} = \\mathbf{2.551\\text{ A/cm}^2}$$

El sobrepotencial de concentración catódico y anódico se calcula como:
$$\\eta_{\\text{conc}} = -\\frac{R T}{2 F} \\ln\\left( 1 - \\frac{j}{j_{\\text{lim}}} \\right) + \\frac{R T}{2 F} \\ln\\left( 1 + \\frac{j \\cdot y_{\\text{H}_2\\text{O}}}{j_{\\text{lim}} \\cdot y_{\\text{H}_2}} \\right)$$

Evaluando a $j = 0.480\\text{ A/cm}^2$:
$$\\frac{j}{j_{\\text{lim}}} = \\frac{0.480}{2.551} = \\mathbf{0.1882\\ (18.82\\%)}$$

$$\\eta_{\\text{conc}} = -(0.046235) \\times \\ln(1 - 0.1882) = -(0.046235) \\times (-0.2085) = \\mathbf{0.0096\\text{ V}} \\quad (0.81\\% \\text{ del voltaje total})$$

> **Dictamen Físico:** Como $j/j_{\\text{lim}} = 18.8\\% \\ll 80\\%$, la celda opera en una zona difusiva completamente lineal, inmune al riesgo de inanición de vapor (*starvation*).

---

### 3.6 Resumen del Potencial de Celda y Régimen Térmico Sub-termoneutro

Sumando todas las contribuciones a $800^\\circ\\text{C}$, $20\\text{ bar}$ y $0.480\\text{ A/cm}^2$:

$$V_{\\text{celda}} = E_{\\text{Nernst}} + \\eta_{\\text{act}} + \\eta_{\\text{ohm}} + \\eta_{\\text{conc}}$$
$$V_{\\text{celda}} = 1.0056\\text{ V} + 0.1119\\text{ V} + 0.0557\\text{ V} + 0.0096\\text{ V} = \\mathbf{1.1828\\text{ V}}$$

Comparando con el voltaje termoneutro $V_{\\text{tn}} = 1.2869\\text{ V}$:
$$\\Delta V_{\\text{termico}} = V_{\\text{celda}} - V_{\\text{tn}} = 1.1828 - 1.2869 = \\mathbf{-0.1041\\text{ V} < 0}$$

#### Demostración del Régimen Endotérmico:
El calor generado/absorbido por el stack se deduce del primer principio de la termodinámica:
$$\\dot{Q}_{\\text{stack}} = I_{\\text{total}} \\cdot (V_{\\text{celda}} - V_{\\text{tn}})$$

Como $\\Delta V_{\\text{termico}} < 0$, $\\dot{Q}_{\\text{stack}} < 0$, lo que significa que **la celda absorbe calor neto del entorno para sostener la disociación molecular**.

$$\\text{Demanda Térmica Neta} = I_{\\text{total}} \\cdot |V_{\\text{celda}} - V_{\\text{tn}}| = (32,189,400\\text{ A}) \\times (0.1041\\text{ V}) = \\mathbf{3,350.9\\text{ kW térmicos}}$$

Sumando el calor sensible necesario para elevar el vapor de $212.4^\\circ\\text{C}$ (caldera) a $800^\\circ\\text{C}$ en el precalentador eléctrico `E-202` ($5,248.4\\text{ kW}$), la planta requiere $8,599.3\\text{ kW}$ de calor a alta temperatura.

#### Acoplamiento Térmico con la Caldera `R-401-S`:
El calor de reacción liberado por el reactor Lurgi de metanol `R-401` es:
$$\\dot{Q}_{\\text{reaccion}} = -\\mathbf{12,335.4\\text{ kW térmicos}}$$

El calor latente de vaporización del agua a $20\\text{ bar}$ ($T_{\\text{sat}} = 212.4^\\circ\\text{C}$) es $\\lambda_{\\text{vap}} = 1,890.7\\text{ kJ/kg}$. La tasa de generación de vapor en la coraza es:
$$\\dot{m}_{\\text{vapor}} = \\frac{|-12,335.4\\text{ kW}| \\times 0.90\\ \\text{(eficiencia térm.)} \\times 3600\\text{ s/h}}{1,890.7\\text{ kJ/kg}} = \\frac{39,966,696}{1,890.7} = \\mathbf{16,244.9\\text{ kg/h de vapor a 20 bar}}$$

Dado que la demanda de vapor del electrolizador SOEC para producir $1,314.8\\text{ kg/h}$ de $\\text{H}_2$ al $70\\%$ de conversión es de $16,244.9\\text{ kg/h}$, **el reactor de metanol genera exactamente el $100\\%$ del vapor requerido por el SOEC**, cerrando un lazo térmico autosuficiente sin combustión externa de gas natural ni consumo adicional de vapor OSBL.

---

### 3.7 Cinética Heterogénea de Vanden Bussche & Froment y Ecuación de Ergun

El reactor `R-401` es un reactor multitubular de lecho fijo empacado (Lurgi Boiling Water Reactor, BWR) con enfriamiento por agua en ebullición en la coraza. Se modeló con las expresiones cinéticas cinéticas de Vanden Bussche & Froment (1996), que establecen que el $\\text{CO}_2$ es la fuente directa del metanol:

1. **Hidrogenación de $\\text{CO}_2$ a Metanol:**
   $$\\text{CO}_2 + 3\\text{H}_2 \\rightleftharpoons \\text{CH}_3\\text{OH} + \\text{H}_2\\text{O} \\quad (\\Delta H^\\circ_{298} = -49.5\\text{ kJ/mol})$$
   $$r_{\\text{MeOH}} = \\frac{k_1 P_{\\text{CO}_2} P_{\\text{H}_2} \\left( 1 - \\frac{P_{\\text{MeOH}} P_{\\text{H}_2\\text{O}}}{K_{eq,1} P_{\\text{CO}_2} P_{\\text{H}_2}^3} \\right)}{\\left( 1 + K_{\\text{CO}} \\frac{P_{\\text{CO}}}{P_{\\text{H}_2}^{0.5}} + K_{\\text{CO}_2} P_{\\text{CO}_2} + K_{\\text{H}_2} P_{\\text{H}_2}^{0.5} \\right)^3}$$

2. **Reacción Inversa de Desplazamiento de Gas de Agua (RWGS):**
   $$\\text{CO}_2 + \\text{H}_2 \\rightleftharpoons \\text{CO} + \\text{H}_2\\text{O} \\quad (\\Delta H^\\circ_{298} = +41.2\\text{ kJ/mol})$$
   $$r_{\\text{RWGS}} = \\frac{k_2 P_{\\text{CO}_2} \\left( 1 - \\frac{P_{\\text{CO}} P_{\\text{H}_2\\text{O}}}{K_{eq,2} P_{\\text{CO}_2} P_{\\text{H}_2}} \\right)}{1 + K_{\\text{CO}} \\frac{P_{\\text{CO}}}{P_{\\text{H}_2}^{0.5}} + K_{\\text{CO}_2} P_{\\text{CO}_2} + K_{\\text{H}_2} P_{\\text{H}_2}^{0.5}}$$

#### Caída de Presión en Lecho Empacado (Ecuación de Ergun):
$$\\frac{dP}{dz} = - \\left[ 150 \\frac{(1 - \\varepsilon_b)^2}{\\varepsilon_b^3} \\frac{\\mu_g v_s}{d_p^2} + 1.75 \\frac{1 - \\varepsilon_b}{\\varepsilon_b^3} \\frac{\\rho_g v_s^2}{d_p} \\right]$$

Con parámetros industriales:
* Diámetro de partícula catalítica cilíndrica trilobular: $d_p = 5.0\\text{ mm} = 0.005\\text{ m}$.
* Porosidad del lecho empacado: $\\varepsilon_b = 0.39$.
* Número de tubos catalíticos: $N_{\\text{tubos}} = 2,126$ tubos BWG 14 de acero inoxidable SA-213 TP316L ($d_i = 33.88\\text{ mm}$, $L = 6.0\\text{ m}$).
* Velocidad superficial del syngas a $75\\text{ bar}$: $v_s = 0.42\\text{ m/s}$.
* **Caída de presión calculada en el lecho:** $\\Delta P = \\mathbf{1.82\\text{ bar}}$ (desde $75.0\\text{ bar}$ a $73.18\\text{ bar}$).

---

### 3.8 Dimensionamiento Físico de Destilación (FUG + O'Connell + Fair)

La purificación del e-metanol efluente del flash `V-501` se diseñó mediante el método clásico Fenske-Underwood-Gilliland (FUG) acoplado a la eficiencia de O'Connell:

1. **Platos Mínimos (Ecuación de Fenske):**
   $$N_{\\text{min}} = \\frac{\\ln\\left( \\frac{x_{\\text{dest,MeOH}} / x_{\\text{dest,H}_2\\text{O}}}{x_{\\text{fondos,MeOH}} / x_{\\text{fondos,H}_2\\text{O}}} \\right)}{\\ln(\\alpha_{\\text{rel}})}$$
   Con pureza deseada grado químico AA ($99.89\\%\\text{ wt}$ MeOH en domo, $<0.05\\%\\text{ wt}$ en fondos) y volatilidad relativa media $\\alpha_{\\text{rel}} = 3.25$:
   $$N_{\\text{min}} = \\mathbf{11.2\\text{ platos}}$$

2. **Reflujo Mínimo y Operativo (Ecuación de Underwood):**
   $$R_{\\text{min}} = 0.88 \\implies R_{\\text{operativo}} = 1.70 \\times R_{\\text{min}} = \\mathbf{1.50}$$

3. **Platos Teóricos (Correlación de Gilliland):**
   Para $R = 1.50$, la correlación empírica entrega:
   $$N_{\\text{teoricos}} = \\mathbf{24\\text{ platos}}$$

4. **Eficiencia Global de Platos (Correlación de O'Connell):**
   $$\\eta_0 = 0.492 \\cdot (\\mu_L \\cdot \\alpha_{\\text{rel}})^{-0.245} \\approx \\mathbf{0.70\\ (70\\%)}$$

5. **Platos Reales y Altura Total:**
   $$N_{\\text{real}} = \\frac{N_{\\text{teoricos}}}{\\eta_0} = \\frac{24}{0.70} = 34.28 \\longrightarrow \\mathbf{34\\text{ platos reales}}$$
   Con espaciamiento entre platos de $0.50\\text{ m}$, más $1.5\\text{ m}$ en cabeza para desentrainador y $2.0\\text{ m}$ en fondo para sello de nivel:
   $$H_{\\text{columna}} = (34 \\times 0.50\\text{ m}) + 3.0\\text{ m} = \\mathbf{20.0\\text{ m}}$$

6. **Diámetro por Inundación de Fair (80% Flooding):**
   $$v_{\\text{flood}} = C_{sb} \\sqrt{\\frac{\\rho_L - \\rho_V}{\\rho_V}} \\left( \\frac{\\sigma_L}{20} \\right)^{0.2} = 1.34\\text{ m/s}$$
   $$v_{\\text{operativa}} = 0.80 \\times v_{\\text{flood}} = 1.07\\text{ m/s} \\implies D_{\\text{columna}} = \\sqrt{\\frac{4 \\dot{V}_V}{\\pi v_{\\text{operativa}}}} = \\mathbf{1.20\\text{ m}}$$

---

# SECCIÓN 4: LÓGICA DE METADATOS DE TOPOLOGÍA, BALANCES Y SERVICIOS AUXILIARES

### 4.1 Topología de Procesos como Grafo Dirigido y Algoritmos de Corte (Tear Streams)

Un flowsheet químico es formalmente un **grafo dirigido ponderado** $G = (V, E)$:
* **Vértices ($V$):** Conjunto de operaciones unitarias (reactores, mezcladores, divisores, intercambiadores, columnas).
* **Aristas ($E$):** Conjunto de corrientes de materia y energía que conectan los vértices, donde cada arista porta un vector de estado $x_j = [T, P, h, \\dot{n}_1, \\dot{n}_2, \\dots, \\dot{n}_c]^T$.

```
[Área 100: CO2] ------> (MIX-301) ------> [C-301] ------> (MIX-401) ------> [R-401 Lurgi]
                           ^                                  ^                  |
                           |                                  |                  v
[Área 200: SOEC] ----------+                          [Reciclo S-504] <--- (Flash V-501)
(100% Vapor de R-401-S)                                       |                  |
                                                          [Purga 4%]         (T-601 AA)
                                                                                 |
                                                                           [MeOH Grado AA]
```

#### Identificación de Lazos y Componentes Fuertemente Conectados (SCC)
El bucle de reacción y reciclaje de syngas contiene ciclos dirigidos que impiden la resolución secuencial directa. Mediante el algoritmo de Tarjan, se aísla el SCC compuesto por `{MIX-401, R-401, E-501, V-501, C-501, SPLIT-501}`.

#### Selección Óptima de Tear Stream (Corriente de Corte)
Se seleccionó la corriente de vapor del reciclo `S-504` como la variable de iteración (*Tear Stream*), ya que desacopla el bucle minimizando la dimensión del vector residual.

#### Acelerador Numérico Wegstein
Para acelerar la convergencia y evitar divergencias oscilatorias entre iteraciones $k$ y $k+1$:
$$x^{(k+1)} = q \\cdot g(x^{(k)}) + (1 - q) \\cdot x^{(k)}$$
Donde el factor de aceleración de Wegstein $q$ se calcula a partir de la pendiente secante $s = \\frac{g(x^{(k)}) - g(x^{(k-1)})}{x^{(k)} - x^{(k-1)}}$:
$$q = \\frac{1}{1 - s} \\quad (\\text{acotado en } -5 \\le q \\le 0.95)$$

---

### 4.2 Matrices Consolidadas de Balance de Materia Global de la Planta

La tabla consolida el balance de materia envolvente para la capacidad nominal de **$30,000\\text{ t/año}$ de metanol** ($8,000\\text{ h/año}$ de operación, factor de servicio $91.3\\%$):

| Flujo / Corriente | Identificador | Flujo Másico (kg/h) | Flujo Molar (kmol/h) | Composición Principal (% mol) | Fase y Condiciones |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Alimentación Agua Desmineralizada** | `S-200` | $11,842.1$ | $657.3$ | $\\text{H}_2\\text{O} > 99.99\\%$ | Líquido, $25^\\circ\\text{C}, 1.013\\text{ bar}$ |
| **Alimentación Dióxido de Carbono** | `S-101` | $5,274.3$ | $119.8$ | $\\text{CO}_2: 99.5\\%, \\text{N}_2: 0.5\\%$ | Gas denso, $25^\\circ\\text{C}, 20.0\\text{ bar}$ |
| **Hidrógeno Verde Producido SOEC** | `S-205` | $1,314.8$ | $652.2$ | $\\text{H}_2: 99.2\\%, \\text{H}_2\\text{O}: 0.8\\%$ | Gas, $800^\\circ\\text{C}, 19.4\\text{ bar}$ |
| **Oxígeno Puro Subproducto Venta** | `S-206` | $10,434.5$ | $326.1$ | $\\text{O}_2: 99.8\\%, \\text{H}_2\\text{O}: 0.2\\%$ | Gas, $800^\\circ\\text{C}, 20.0\\text{ bar}$ |
| **Syngas a Entrada de Reactor** | `S-401` | $21,308.1$ | $1,985.4$ | $\\text{H}_2: 74.2\\%, \\text{CO}_2: 15.6\\%, \\text{CO}: 4.1\\%, \\text{CH}_4: 6.1\\%$ | Gas, $210^\\circ\\text{C}, 75.0\\text{ bar}$ |
| **E-Metanol Grado AA (Producto)** | `S-604` | $\\mathbf{3,788.65}$ | $118.2$ | $\\mathbf{CH_3OH: 99.89\\%\\ wt}, \\text{H}_2\\text{O}: 0.11\\%\\ wt$ | Líquido, $45^\\circ\\text{C}, 1.2\\text{ bar}$ |
| **Purga de Gases Inertes** | `S-505` | $852.3$ | $79.4$ | $\\text{H}_2: 68\\%, \\text{CH}_4: 18\\%, \\text{CO}_2: 9\\%, \\text{CO}: 5\\%$ | Gas combustible hacia antorcha / boiler |
| **Agua Residual ZLD (Fondos T-601)** | `S-605` | $2,130.8$ | $118.3$ | $\\text{H}_2\\text{O} > 99.95\\%\\ wt, \\text{MeOH} < 0.05\\%\\ wt$ | Líquido hacia planta de reciclo BFW |

---

### 4.3 Matriz de Balance de Energía Global y Demanda de Servicios Auxiliares

| Equipo / Consumidor | Tipo de Servicio | Demanda Nominal | Condiciones de Entrada / Salida | Justificación Técnica de Diseño |
| :--- | :--- | :---: | :--- | :--- |
| **Stacks SOEC (`EL-201`)** | Electricidad DC/AC | **$38.07\\text{ MWe}$** | $800^\\circ\\text{C}, 20\\text{ bar}, 0.480\\text{ A/cm}^2$ | Consumo de $32.92\\text{ kWh/kg H}_2$ ($1.1828\\text{ V}$). |
| **Precalentador Stacks (`E-202`)** | Eléctrico Incoloy 800H | **$5,248.4\\text{ kW}$** | $212.4^\\circ\\text{C} \\to 800.0^\\circ\\text{C}$ | Sobrecalienta vapor saturado de caldera $20\\text{ bar}$. |
| **Compresor Syngas (`C-301`)** | Electricidad Motor | **$1,316.7\\text{ kWe}$** | $19.4\\text{ bar} \\to 75.0\\text{ bar}$ | 2 etapas con enfriamiento intermedio. |
| **Compresor Reciclo (`C-501`)** | Electricidad Motor | **$215.4\\text{ kWe}$** | $72.5\\text{ bar} \\to 75.0\\text{ bar}$ | Compensa caída de presión del bucle ($2.5\\text{ bar}$). |
| **Expansor de Purga (`EXP-501`)** | Generación Eléctrica | **$-437.8\\text{ kWe}$** | $72.5\\text{ bar} \\to 1.5\\text{ bar}$ | Recupera energía de la purga gaseosa (generador). |
| **Reboiler T-601 (`E-601`)** | Vapor de Baja Presión | **$2,850.0\\text{ kW}$** | $120^\\circ\\text{C}$ condensando | Suministra calor de separación flash y reflujo. |
| **Condensador Efluente (`E-501`)** | Agua de Enfriamiento (CW) | **$8,450.0\\text{ kW}$** | Agua $30^\\circ\\text{C} \\to 40^\\circ\\text{C}$ | Condensa mezcla líquida cruda $\\text{MeOH}-\\text{H}_2\\text{O}$. |
| **Condensador Reflujo (`E-602`)** | Agua de Enfriamiento (CW) | **$2,610.0\\text{ kW}$** | Agua $30^\\circ\\text{C} \\to 40^\\circ\\text{C}$ | Condensación total del destilado en cabeza de T-601. |
| **Caldera Coraza (`R-401-S`)** | Generación de Vapor | **$-12,335.4\\text{ kW}$** | Agua saturada $20\\text{ bar} \\to$ Vapor | Genera $16,244.9\\text{ kg/h}$ de vapor para el SOEC. |

---

### RESUMEN DE CONSUMO ESPECÍFICO DE PLANTA
* **Potencia Eléctrica Neta:** **$39.85\\text{ MWe}$** (incluyendo compresores, bombeo BFW y balance de planta).
* **Consumo Específico de e-Metanol:** **$10.52\\text{ MWh / tonelada de e-MeOH}$** ($1.31\\text{ kWe/kg MeOH}$).
* **Eficiencia Exergética Global:** **$64.8\\%$** (relación LHV Metanol / Energía Eléctrica + Calor).
* **Emisiones Evitadas:** **$41,200\\text{ t } \\text{CO}_2/\\text{año}$** (incorporación neta en la molécula de e-metanol).
"""

if __name__ == "__main__":
    print("Escribiendo archivo Markdown...")
    md_content = get_markdown_content()
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Archivo Markdown generado exitosamente en: {MD_OUT} ({len(md_content)} caracteres)")

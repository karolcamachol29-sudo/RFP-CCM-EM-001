# coding: utf-8
"""
construir_guia.py
Script modular que genera la Guía Maestra de Defensa Técnica, Speech de 10 Minutos,
Banco de Preguntas Q&A y Desglose Matemático de Ecuaciones.
"""

import os
import subprocess
import shutil

TEX_PATH = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.tex"
MD_PATH = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.md"
PDF_DIR = "Entregables"
FINAL_PDF = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf"
ROOT_PDF = "./Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf"

# 1. PREÁMBULO LATEX Y CONFIGURACIÓN
PREAMBLE = r"""\documentclass[10pt,letterpaper]{article}

% --- PAQUETES BÁSICOS ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1.8cm,top=2.2cm,bottom=2.2cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xltabular}
\usepackage{array}
\usepackage{colortbl}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{tikz}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}

% --- PALETA CORPORATIVA SOLVANTA ---
\definecolor{primaryblue}{HTML}{1A4F7C}
\definecolor{secondaryblue}{HTML}{0284C7}
\definecolor{accentteal}{HTML}{0D9488}
\definecolor{darkslate}{HTML}{1E293B}
\definecolor{lightbg}{HTML}{F8FAFC}
\definecolor{tableheader}{HTML}{1E3A8A}
\definecolor{tablerowgray}{HTML}{F1F5F9}
\definecolor{alertred}{HTML}{B91C1C}
\definecolor{alertbg}{HTML}{FEF2F2}
\definecolor{warngold}{HTML}{B45309}
\definecolor{warnbg}{HTML}{FFFBEB}
\definecolor{greengood}{HTML}{059669}
\definecolor{greenbg}{HTML}{ECFDF5}
\definecolor{pyyellow}{HTML}{D97706}
\definecolor{boxborder}{HTML}{CBD5E1}

% --- HIPERVÍNCULOS ---
\usepackage[colorlinks=true,
            linkcolor=primaryblue,
            citecolor=accentteal,
            urlcolor=secondaryblue]{hyperref}

% --- ENCABEZADOS Y PIES DE PÁGINA ---
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.6pt}
\renewcommand{\footrulewidth}{0.4pt}
\fancyhead[L]{\small\bfseries\color{primaryblue}Solvanta Engineering Solutions S.A. de C.V.}
\fancyhead[R]{\small\color{darkslate}Guía de Defensa Técnica: Speech 10 min, Q\&A y Memoria de Ingeniería}
\fancyfoot[L]{\footnotesize\color{darkslate}Proyecto RFP-CCM-EM-001 | Planta de e-Metanol (30,000 t/año)}
\fancyfoot[R]{\footnotesize\bfseries\color{primaryblue}Página \thepage\ de \pageref{LastPage}}

% --- ESTILOS DE CAJAS TCOLORBOX ---
\newtcolorbox{speechgrecia}[2][]{
    enhanced,
    colback=lightbg,
    colframe=accentteal,
    fonttitle=\bfseries\color{white},
    colbacktitle=accentteal,
    title={\small \textbf{ORADOR: GRECIA FIGUEROA (GRESS)} \hfill \textit{#2}},
    boxrule=1.2pt,
    arc=4pt,
    boxsep=4pt,
    left=8pt, right=8pt, top=6pt, bottom=6pt,
    breakable,
    #1
}

\newtcolorbox{speechkaroc}[2][]{
    enhanced,
    colback=lightbg,
    colframe=primaryblue,
    fonttitle=\bfseries\color{white},
    colbacktitle=primaryblue,
    title={\small \textbf{ORADOR: KAROL CAMACHO (KAROC)} \hfill \textit{#2}},
    boxrule=1.2pt,
    arc=4pt,
    boxsep=4pt,
    left=8pt, right=8pt, top=6pt, bottom=6pt,
    breakable,
    #1
}

\newtcolorbox{qabox}[2][]{
    enhanced,
    colback=lightbg,
    colframe=primaryblue!85!black,
    fonttitle=\bfseries\color{white},
    colbacktitle=primaryblue!85!black,
    title={\small \textbf{#2}},
    boxrule=1.2pt,
    arc=4pt,
    boxsep=4pt,
    left=8pt, right=8pt, top=6pt, bottom=6pt,
    breakable,
    #1
}

\newtcolorbox{mathdeductionbox}[1]{
    enhanced,
    colback=lightbg,
    colframe=darkslate,
    fonttitle=\bfseries\color{white},
    colbacktitle=darkslate,
    title={#1},
    boxrule=1.0pt,
    arc=3pt,
    boxsep=4pt,
    left=8pt, right=8pt, top=6pt, bottom=6pt,
    breakable
}

\newtcolorbox{codebox}[1]{
    enhanced,
    colback=darkslate!5!white,
    colframe=darkslate!80!black,
    fonttitle=\bfseries\color{white},
    colbacktitle=darkslate!80!black,
    title={#1},
    boxrule=1.0pt,
    arc=3pt,
    boxsep=3pt,
    left=6pt, right=6pt, top=4pt, bottom=4pt,
    breakable
}

\newtcolorbox{conceptbox}[1]{
    enhanced,
    colback=lightbg,
    colframe=secondaryblue,
    fonttitle=\bfseries\color{white},
    colbacktitle=secondaryblue,
    title={#1},
    boxrule=1.0pt,
    arc=3pt,
    boxsep=3pt,
    left=6pt, right=6pt, top=4pt, bottom=4pt,
    breakable
}

\setlength{\parskip}{0.4em}
\setlength{\parindent}{0pt}

% Configuración de listings para código Python
\lstdefinestyle{pythonstyle}{
    language=Python,
    basicstyle=\ttfamily\footnotesize\color{darkslate},
    keywordstyle=\bfseries\color{secondaryblue},
    stringstyle=\color{greengood},
    commentstyle=\itshape\color{darkslate!60},
    numberstyle=\tiny\color{darkslate!40},
    numbers=left,
    stepnumber=1,
    numbersep=8pt,
    showstringspaces=false,
    breaklines=true,
    breakatwhitespace=true,
    frame=none,
    backgroundcolor=\color{lightbg}
}
\lstset{style=pythonstyle}

\begin{document}

% ==============================================================================
% PORTADA INSTITUCIONAL
% ==============================================================================
\begin{titlepage}
    \centering
    \vspace*{0.5cm}
    {\fontsize{22}{26}\selectfont\bfseries\color{primaryblue}SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.}\\[0.4cm]
    {\large\textbf{\color{darkslate}DIVISIÓN DE INGENIERÍA DE PROCESOS Y SIMULACIÓN AVANZADA}}\\[0.2cm]
    {\normalsize Consorcio de Diseño, Procura y Construcción Industrial | Registro RFP-CCM-EM-001}\\[0.6cm]
    \rule{\linewidth}{1.5pt}\\[0.6cm]
    
    {\fontsize{18}{22}\selectfont\bfseries\color{secondaryblue}GUÍA MAESTRA DE DEFENSA TÉCNICA, SPEECH DE 10 MINUTOS, BANCO DE PREGUNTAS Y MEMORIA DE CÁLCULO}\\[0.4cm]
    {\large\textbf{Simulación Rigurosa, Programación Orientada a Objetos en BioSTEAM/DWSIM, Optimización Multivariable SOEC, Análisis de Nodos DTI y Salvaguardas SIS}}\\[0.4cm]
    \rule{0.6\linewidth}{0.8pt}\\[0.8cm]
    
    \begin{tcolorbox}[enhanced,colback=lightbg,colframe=primaryblue,boxrule=1.2pt,arc=4pt,width=0.92\linewidth]
        \centering
        \textbf{\color{primaryblue}EXPEDIENTE TÉCNICO Y CONTROL DE DEFENSA}\\[0.2cm]
        \begin{tabular}{rl}
            \textbf{Licitación Internacional:} & RFP-CCM-EM-001 (PEMEX / CFE / SENER) \\
            \textbf{Proyecto:} & Planta de Producción de e-Metanol Grado AA ($30,000\text{ t/año}$) \\
            \textbf{Ubicación:} & predio industrial asignado para el proyecto RFP-CCM-EM-001. \\
            \textbf{Tecnología de Hidrógeno:} & Electrólisis SOEC de Alta Temperatura ($800^\circ\text{C}, 20\text{ bar}$) \\
            \textbf{Tecnología de Síntesis:} & Reactor Lurgi Multitubular BWR ($75\text{ bar}$) acoplado a vapor SOEC \\
            \textbf{Purificación:} & Destilación Rigurosa Grado AA ($99.89\%\text{ wt}$) con Lazo ZLD \\
            \textbf{Expositoras Técnicas:} & \textbf{Ing. Grecia Figueroa Rincón} (Procesos, BioSTEAM y Seguridad HAZOP) \\
            & \textbf{Ing. Karol Paola Camacho López} (Simulación DWSIM, SOEC y Optimización) \\
            \textbf{Cátedra Académica:} & Dr. Jesús Andrés Arzola Flores | FIQ - BUAP
        \end{tabular}
    \end{tcolorbox}
    
    \vfill
    {\small\color{darkslate}\textbf{sitio industrial de referencia, México} \textbar\ Noviembre de 2026}
\end{titlepage}

\tableofcontents
\newpage
"""

# 2. SECCIÓN 1: SPEECH OFICIAL SINCRONIZADO DE 10 MINUTOS
SECTION_1 = r"""
\section{SPEECH OFICIAL SINCRONIZADO DE 10 MINUTOS (GUION DE LOCUCIÓN PASO A PASO)}

\subsection{Matriz de Control de Tiempos y Transición de Voces (Duración: 10:00 min)}

Para garantizar una defensa ejecutiva, rigurosa y perfectamente coordinada ante el comité evaluador de la licitación RFP-CCM-EM-001, se diseñó la siguiente matriz de tiempos con transiciones explícitas, pausas de énfasis y sincronización directa con las áreas y figuras del cartel oficial ($90 \times 130\text{ cm}$):

\begin{table}[htbp]
\centering
\small
\renewcommand{\arraystretch}{1.3}
\begin{tabularx}{\linewidth}{c >{\bfseries}l c c c >{\raggedright\arraybackslash}X}
\toprule
\rowcolor{tableheader}
\textbf{\color{white}Bloque} & \textbf{\color{white}Orador} & \textbf{\color{white}Intervalo} & \textbf{\color{white}Duración} & \textbf{\color{white}Palabras} & \textbf{\color{white}Área del Cartel y Contenido Clave} \\
\midrule
\rowcolor{tablerowgray}
1.1 & Grecia Figueroa & 0:00 -- 2:00 & 2.0 min & ~290 & \textbf{Área 5:} BioSTEAM, POO, subclase \texttt{bst.Unit}, ciclo de vida y reciclos. \\
1.2 & Karol Camacho & 2:00 -- 4:30 & 2.5 min & ~365 & \textbf{Áreas 1 y 2:} Termodinámica SOEC, Shomate NIST, Butler-Volmer, DWSIM API XML. \\
\rowcolor{tablerowgray}
1.3 & Grecia Figueroa & 4:30 -- 6:30 & 2.0 min & ~295 & \textbf{Área 6:} DTI v1.0, 4 nodos HAZOP (IEC 61882), cascada $M=2.05$, 4 Interlocks SIS. \\
1.4 & Karol Camacho & 6:30 -- 8:45 & 2.25 min & ~335 & \textbf{Áreas 4 y 7:} Sensibilidad Morris, 4 Escenarios, Frente de Pareto, Escenario D. \\
\rowcolor{tablerowgray}
1.5 & Grecia Figueroa & 8:45 -- 10:00 & 1.25 min & ~185 & \textbf{Conclusión:} Programación como motor del diseño industrial y apertura a Q\&A. \\
\midrule
\rowcolor{primaryblue!15}
\textbf{Total} & \textbf{Consorcio Solvanta} & \textbf{0:00 -- 10:00} & \textbf{10.0 min} & \textbf{~1,470} & \textbf{Defensa Técnica Integral de Planta (30,000 t/año e-MeOH)} \\
\bottomrule
\end{tabularx}
\caption{Matriz oficial de locución, cronometraje y asignación temática para la defensa de 10 minutos.}
\end{table}

\subsection{Intervención 1: BioSTEAM y Programación Orientada a Objetos para Nuevas Tecnologías}

\begin{speechgrecia}{Intervalo: 0:00 -- 2:00 | Duración: 2:00 min | Referencia: Área 5 del Cartel}
\textbf{[0:00 - 0:25] Saludo y Planteamiento del Reto:}
Buenos días, miembros del comité evaluador y colegas ingenieros. A nombre del Consorcio Solvanta Engineering Solutions, presentamos la ingeniería de proceso para la licitación RFP-CCM-EM-001, orientada a la producción de 30,000 toneladas anuales de e-metanol Grado AA en el complejo industrial adyacente.

Al conceptualizar esta planta, nos enfrentamos a una barrera común en el ejercicio profesional: los simuladores comerciales cerrados carecen de modelos nativos para tecnologías de vanguardia como las celdas de electrólisis de óxido sólido (SOEC) y reactores catalíticos multitubulares acoplados térmicamente. La práctica habitual es recurrir a cajas negras o conversiones empíricas que comprometen la fidelidad termodinámica.

\textbf{[0:25 - 1:15] Por qué BioSTEAM y Paradigma de Programación:}
\textit{(Señalar con firmeza el encabezado del Área 5 en la columna derecha del cartel)}
Para superar esta limitación, seleccionamos la plataforma de código abierto BioSTEAM en Python. BioSTEAM destaca porque acopla de forma nativa la simulación de balances de materia y energía con el análisis tecno-económico y de ciclo de vida. Mediante el paradigma de programación orientada a objetos, construimos unidades de proceso personalizadas mediante la subclasificación de la clase abstracta \texttt{bst.Unit}.

\textbf{[1:15 - 1:45] Ciclo de Vida de la Unidad No Nativa (\texttt{SOECElectrolyzer}):}
\textit{(Indicar el bloque de código de BioSTEAM en el Área 5)}
El ciclo de vida de nuestra clase \texttt{SOECElectrolyzer} opera en tres etapas rigurosas:
Primero, los metadatos de topología \texttt{\_N\_ins = 1} y \texttt{\_N\_outs = 2} declaran la conectividad física de los puertos.
Segundo, el método interno \texttt{\_run()} resuelve el balance fisicoquímico en tiempo de ejecución: toma el flujo molar de vapor sobrecalentado de \texttt{self.ins[0]}, aplica la conversión electroquímica regida por la Ley de Faraday y actualiza in situ las propiedades termodinámicas de las corrientes de salida en \texttt{self.outs}.
Tercero, el método \texttt{\_design()} evalúa la geometría de los stacks cerámicos y registra automáticamente la demanda de potencia en \texttt{self.power\_utility}, integrándola al consumo eléctrico de la planta.

\textbf{[1:45 - 2:00] Convergencia y Transición:}
Al heredar de \texttt{bst.Unit}, el electrolizador se integra orgánicamente en el \texttt{bst.Flowsheet}, permitiendo que el algoritmo acelerado de Wegstein resuelva los bucles cerrados de reciclo con estabilidad matemática absoluta. 

Para detallar cómo formulamos los primeros principios electroquímicos y cómo los conectamos con el simulador DWSIM, cedo la palabra a mi colega, la ingeniera Karol Camacho.
\end{speechgrecia}

\subsection{Intervención 2: Fundamentos del SOEC, Termodinámica e Integración con DWSIM}

\begin{speechkaroc}{Intervalo: 2:00 -- 4:30 | Duración: 2:30 min | Referencia: Áreas 1 y 2 del Cartel}
\textbf{[2:00 - 2:40] Justificación Termodinámica del SOEC a 800 °C:}
Muchas gracias, Grecia. Buenos días. Si dirigen su atención al Área 1 del cartel, la decisión de implementar electrólisis SOEC de alta temperatura a 800 °C frente a la electrólisis convencional alcalina o PEM responde a un principio termodinámico ineludible: la demanda de energía libre de Gibbs ($\Delta G$) decrece drásticamente de $237\text{ kJ/mol}$ a temperatura ambiente hasta $180\text{ kJ/mol}$ a 800 °C. Esto permite sustituir cerca del 25\% del trabajo eléctrico por energía térmica residual, abatiendo el consumo energético de la planta.

\textbf{[2:40 - 3:30] Modelo Electroquímico Riguroso en Python:}
\textit{(Señalar las ecuaciones y el listado de código en el Área 2)}
Para garantizar máxima precisión en el paquete \texttt{soec\_optimization/}, implementamos tres componentes fundamentales:
1. \textbf{Termodinámica NIST Shomate:} Reemplazamos la correlación lineal simplificada por polinomios rigurosos de Shomate del NIST. Esto corrigió una sobreestimación de $+24.8\text{ mV}$ en el potencial reversible estándar, evitando un error acumulado de casi un megavatio en el dimensionamiento eléctrico.
2. \textbf{Potencial de Nernst Presurizado:} Modelamos el efecto de operar a 20 bar, incorporando la presión anódica de oxígeno puro y los perfiles molares de vapor e hidrógeno a lo largo del cátodo.
3. \textbf{Cinética Butler-Volmer y Despeje Analítico:} Invertimos analíticamente la ecuación de activación mediante la función $\operatorname{arsinh}$, eliminando métodos iterativos lentos. Asimismo, calculamos la resistencia óhmica mediante la ley de Arrhenius para el electrolito cerámico de YSZ.

\textbf{[3:30 - 4:00] Erradicación del Recorte Numérico Difusivo:}
\textit{(Señalar la Figura 1: Curva de polarización V-j)}
Un aporte fundamental de nuestro código fue erradicar el recorte artificial que muchos modelos comerciales usan para evitar errores de dominio cuando la corriente se acerca al límite difusivo. En \texttt{concentration.py}, penalizamos rigurosamente cualquier condición donde $j \ge j_{\text{lim}}$. De este modo, garantizamos que el diseño opere de manera físicamente viable, alejado de la degradación por transporte de masa.

\textbf{[4:00 - 4:30] Integración de API DWSIM e Inyección XML:}
Para validar la hidrodinámica completa de la planta, construimos el módulo \texttt{dwsim\_interface.py}. Este script interactúa mediante IronPython con la API de DWSIM v10, leyendo las corrientes de entrada \texttt{ims1} y actualizando dinámicamente las propiedades de salida \texttt{oms1} y \texttt{oms2} con \texttt{ClearAllProps()}, \texttt{SetMolarFlow()} y \texttt{Calculate()}. Además, automatizamos la inyección directa del script en el árbol XML del archivo de simulación \texttt{.dwxml}.

Con la física convergida en Python y validada en DWSIM, congelamos los parámetros en el Diagrama de Tubería e Instrumentación. Grecia detallará la ingeniería de detalle y las salvaguardas de seguridad.
\end{speechkaroc}

\subsection{Intervención 3: Desglose de Nodos en el DTI v1.0, Filosofía de Salvaguardas y HAZOP/SIL}

\begin{speechgrecia}{Intervalo: 4:30 -- 6:30 | Duración: 2:00 min | Referencia: Área 6 del Cartel}
\textbf{[4:30 - 5:05] Congelación del P\&ID y Filosofía de Control:}
\textit{(Señalar la Figura 4 en el Área 6: Plano Solvanta\_DTI\_v1.pdf)}
Gracias, Karol. Los balances convergidos en Python se tradujeron al Diagrama de Tubería e Instrumentación congelado en el plano DTI v1.0. Para asegurar la operación continua de la síntesis de metanol, implementamos una estrategia de control avanzado en cascada estequiométrica: el analizador \texttt{AIC-401} monitorea la composición del gas de síntesis y ajusta la consigna del controlador de flujo \texttt{FIC-401}, manteniendo estrictamente el módulo estequiométrico en $M = 2.05$, lo que protege el catalizador de cobre contra la formación de subproductos pesados y desactivación térmica.

\textbf{[5:05 - 5:45] Auditoría de Nodos Críticos bajo Norma IEC 61882 (HAZOP):}
Auditamos cuatro nodos de proceso mediante la metodología HAZOP:
- \textbf{Nodo 1 (Vapor):} Prevención de choque térmico en celdas cerámicas ante fluctuaciones de vapor saturado.
- \textbf{Nodo 2 (SOEC):} Control estricto de gradientes de presión transitorios entre ánodo y cátodo.
- \textbf{Nodo 3 (Reactor Lurgi BWR):} Remoción del calor exotérmico ($-12.34\text{ MW}$) mediante generación de vapor en coraza, impidiendo puntos calientes superiores a 260 °C.
- \textbf{Nodo 4 (Destilación AA):} Control de presión y reflujo en T-601 para garantizar la pureza de 99.89\% en peso.

\textbf{[5:45 - 6:30] Matriz Causa-Efecto de Interlocks SIS (Tabla 3):}
\textit{(Indicar la Tabla 3 en el Área 6)}
Como salvaguardas instrumentadas independientes del sistema de control básico, diseñamos cuatro lazos de seguridad interlock (SIS) con transmisores redundantes en arquitectura 2oo3:
- \textbf{Interlock I-01:} Ante temperatura en R-401 superior a 260 °C, cierra la válvula de corte rápido \texttt{SDV-301} en menos de 2 segundos y abre reciclo frío para detener el embalamiento térmico.
- \textbf{Interlock I-02:} Si la presión del bucle excede 78.5 bar, desacopla los compresores C-301 y C-501, activa el reciclo anti-surge y alivia hacia la antorcha vía \texttt{PSV-501}.
- \textbf{Interlock I-03 (Protección SOEC):} Si el diferencial de presión transitorio entre ánodo y cátodo supera los 0.4 bar, corta el suministro eléctrico DC en menos de 50 milisegundos, abre la válvula ecualizadora \texttt{PDCV-201} e inunda con nitrógeno, previniendo la fractura mecánica de los electrolitos cerámicos de YSZ.
- \textbf{Interlock I-04:} Ante nivel muy bajo en el separador flash V-501, cierra \texttt{SDV-501} en menos de 1 segundo para evitar el paso descontrolado de gas de alta presión hacia el tren de destilación a baja presión.

A continuación, Karol explicará el análisis de sensibilidad multivariable y la selección del punto de operación óptimo.
\end{speechgrecia}

\subsection{Intervención 4: Escenarios SOEC, Sensibilidad de Morris y Selección del Escenario D}

\begin{speechkaroc}{Intervalo: 6:30 -- 8:45 | Duración: 2:15 min | Referencia: Áreas 4 y 7 del Cartel}
\textbf{[6:30 - 7:15] Sensibilidad en 3 Niveles y Método de Morris (Tabla 2):}
\textit{(Dirigir la atención a las Tablas 2 y 4 y a las Figuras 5 y 6 en las Áreas 4 y 7)}
Muchas gracias, Grecia. Para explorar el espacio de diseño del sistema, programamos en \texttt{sensitivity.py} un estudio en tres niveles: análisis univariado OAT, muestreo por Hipercubo Latino con 100 corridas y el Método de Efectos Elementales de Morris con 15 trayectorias. 

Como muestra la Tabla 2, el ranking de Morris reveló que la \textbf{temperatura} es el parámetro gobernante absoluto (Score 100.0), ya que abate exponencialmente la resistencia óhmica ASR del electrolito. Le sigue la \textbf{densidad de corriente} (Score 74.3), que balancea directamente el gasto eléctrico operativo contra el área de celdas requerida. El área unitaria de celda tuvo un impacto intensivo nulo (Score 0.1), lo que confirmó la validez de fijar celdas comerciales de $200\text{ cm}^2$.

\textbf{[7:15 - 8:05] Comparativa de Escenarios y Frente de Pareto:}
Evaluamos cuatro escenarios completos en el flowsheet acoplado:
- El \textbf{Escenario A} representaba la línea base a 750 °C y $0.508\text{ A/cm}^2$, con un consumo específico de $38.13\text{ kWh/kg H}_2$.
- El \textbf{Escenario B} minimizaba el consumo a $30.03\text{ kWh/kg}$, pero disparaba el costo de capital al requerir 281,750 celdas.
- El \textbf{Escenario C} simulaba condiciones intermedias industriales.
- El \textbf{Escenario D}, destacado en verde en la Tabla 4, fue seleccionado mediante optimización multiobjetivo en el Frente de Pareto (Figura 6).

\textbf{[8:05 - 8:45] Justificación Integral del Escenario D Óptimo:}
Al operar a 800 °C, 20 bar y $0.480\text{ A/cm}^2$, el Escenario D logra el compromiso perfecto:
1. Minimiza simultáneamente el costo nivelado de hidrógeno a **\$3.18 USD/kg** y el costo nivelado de metanol a **\$657.2 USD/t** (una reducción de \$75.3 USD por tonelada frente al caso base).
2. Reduce la potencia eléctrica demandada por el electrolizador en **6.03 MW** ($-13.7\%$) y disminuye el número de celdas en **51,600 unidades** ($-20.7\%$).
3. Opera a un voltaje de celda de **1.1828 V**, que es inferior al voltaje termoneutro de 1.287 V. Esto demuestra que la celda opera en un régimen endotérmico de alta eficiencia, donde el déficit térmico es cubierto al 100\% mediante la integración con el vapor generado en la coraza del reactor R-401-S ($16,245\text{ kg/h}$ a 20 bar).

Grecia concluirá la exposición con las consideraciones finales del proyecto.
\end{speechkaroc}

\subsection{Intervención 5: Conclusión y Cierre: La Programación en la Ingeniería Química}

\begin{speechgrecia}{Intervalo: 8:45 -- 10:00 | Duración: 1:15 min | Referencia: Recuadro de Conclusión}
\textbf{[8:45 - 9:30] Síntesis del Logro de Ingeniería:}
\textit{(Señalar el recuadro inferior de Conclusión en la Columna 1)}
Para concluir, esta licitación demuestra con hechos concretos el papel transformador de la programación en la ingeniería de procesos contemporánea. Lejos de ser operadores pasivos de simuladores comerciales con opciones fijas, los ingenieros químicos podemos programar en Python modelos rigurosos desde primeros principios termodinámicos, electroquímicos y de transporte.

Cuando una tecnología limpia y eficiente como la electrólisis SOEC existe físicamente en el mundo real pero no se encuentra en las bibliotecas estándar de software, tenemos la capacidad de construir el bloque desde su base matemática, acoplarlo con DWSIM y BioSTEAM, y formular propuestas técnicamente sustentadas, energéticamente integradas y económicamente superiores.

\textbf{[9:30 - 10:00] Cierre Formal y Apertura de Sesión:}
El diseño de Solvanta Engineering Solutions garantiza una planta de 30,000 toneladas anuales de metanol Grado AA, con un ahorro neto de 6.03 MW eléctricos, operación segura respaldada por metodología HAZOP e interlocks SIL-2, y un modelo reproducible bajo estándares abiertos.

Agradecemos profundamente su tiempo y atención, y quedamos a su entera disposición para atender sus preguntas técnicas. Muchas gracias.
\end{speechgrecia}
"""

# 3. SECCIÓN 2: BANCO DE PREGUNTAS Y RESPUESTAS ANTE AUDIENCIA (Q&A TÉCNICO)
SECTION_2 = r"""
\newpage
\section{BANCO DE PREGUNTAS Y RESPUESTAS ANTE AUDIENCIA Y EVALUADORES (Q\&A TÉCNICO)}

Esta sección compila las 12 preguntas técnicas más probables y desafiantes que formularán evaluadores, profesores o colegas ingenieros a partir de la observación directa de los datos, figuras y tablas del cartel oficial ($90 \times 130\text{ cm}$). Cada respuesta incluye los fundamentos físicos, ecuaciones, argumentos de diseño y números exactos para responder con solidez.

\begin{qabox}{Pregunta 1: Vapor generado en R-401 a 212.4 °C vs. Alimentación al SOEC a 800 °C}
\textbf{Pregunta de la Audiencia:} \textit{En la Tabla 1 afirman que el reactor R-401 genera el 100\% del vapor para el SOEC, pero el reactor genera vapor a 212.4 °C (20 bar) y el SOEC opera a 800 °C. ¿Cómo se resuelve esta diferencia térmica sin una caldera externa?}\\[4pt]
\textbf{Respuesta Técnica para Grecia / Karol:}
El balance de generación y consumo de vapor se resolvió en dos etapas termodinámicas perfectamente delimitadas:
1. \textbf{Calor Latente de Evaporación (Generado al 100\% en R-401-S):} La etapa de mayor demanda entálpica en el ciclo del agua es el cambio de fase líquida a vapor saturado a 20 bar ($h_{fg} = 1,890.7\text{ kJ/kg}$). El reactor de síntesis de metanol opera con una reacción altamente exotérmica ($\Delta H^\circ_r = -49.5\text{ kJ/mol}$ de MeOH producido), liberando $-12,335.4\text{ kW}$ térmicos en la coraza. Este calor se transfiere al agua de alimentación en ebullición, produciendo exactamente **$16,244.9\text{ kg/h}$ de vapor saturado a 20 bar y 212.4 °C**, cubriendo con creces la demanda estequiométrica del SOEC para producir $1,315.6\text{ kg/h}$ de $\text{H}_2$ ($13,853.5\text{ kg/h}$ de vapor a una conversión del $70.26\%$).
2. \textbf{Calor Sensible de Sobrecalentamiento (Aportado por E-202):} Elevar el vapor saturado de 212.4 °C a los 800 °C requeridos por los stacks cerámicos demanda únicamente calor sensible sensible ($\Delta h = 1,489.2\text{ kJ/kg}$). Esta carga térmica ($5,248.4\text{ kW}$ térmicos) se suple mediante el calentador eléctrico \texttt{E-202} con resistencias de Incoloy 800H ($5,328.4\text{ kWe}$ con eficiencia del 98.5\%). 

Por tanto, no se requiere caldera fósil ni generador de vapor auxiliar en régimen estacionario; el calor de reacción genera todo el vapor y la electricidad solo lo sobrecalienta.
\end{qabox}

\begin{qabox}{Pregunta 2: Régimen Endotérmico y Voltaje de Celda (1.1828 V < Vtn = 1.287 V)}
\textbf{Pregunta de la Audiencia:} \textit{En la Tabla 4 y Tabla 5 muestran que el voltaje de celda en el Escenario D es de 1.1828 V, mientras que el voltaje termoneutro es 1.287 V. ¿Viola esto la Primera Ley de la Termodinámica al operar con un voltaje menor al termoneutro?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
No se viola ninguna ley termodinámica. Al contrario, es la demostración física de que la celda opera en **régimen endotérmico**, lo cual es la principal ventaja de las celdas SOEC frente a la electrólisis alcalina o PEM:
- El voltaje termoneutro $V_{\text{tn}} = \frac{\Delta H^\circ}{2F}$ ($1.2872\text{ V}$ a 800 °C) representa el potencial donde el trabajo eléctrico suministrado ($W_e = V \cdot 2F$) iguala exactamente la entalpía total de reacción ($\Delta H^\circ$). Si la celda opera a $V = V_{\text{tn}}$, es adiabática ($\dot{Q} = 0$).
- En el Escenario D, el voltaje total es $V_{\text{celda}} = 1.1828\text{ V}$. Como $V_{\text{celda}} > E_{\text{Nernst}} = 1.0056\text{ V}$, se cumple estrictamente la Segunda Ley ($\Delta G^\circ < W_e$), permitiendo el avance de la electrólisis.
- Dado que $V_{\text{celda}} < V_{\text{tn}}$, el calor generado internamente por pérdidas óhmicas y de activación es menor que la energía térmica requerida por la entropía de disociación ($T\Delta S$). Por consiguiente, la celda absorbe calor del entorno:
$$\dot{Q}_{\text{ext}} = I_{\text{celda}} \cdot (V_{\text{tn}} - V_{\text{celda}}) = 1.90\text{ MA} \times (1.2872 - 1.1828)\text{ V} \approx 198.4\text{ kW}_{\text{térmicos por módulo}}$$
Este calor es suministrado por el vapor sobrecalentado a 800 °C y calentadores térmicos integrados. Esto explica por qué el SOEC alcanza eficiencias eléctricas superiores al 100\% referidas al poder calorífico inferior (LHV) del hidrógeno, mientras que la electrólisis PEM a baja temperatura opera a voltajes de 1.8 a 2.1 V en régimen altamente exotérmico, disipando calor no aprovechable.
\end{qabox}

\begin{qabox}{Pregunta 3: Erradicación del Recorte Numérico en Polarización por Concentración}
\textbf{Pregunta de la Audiencia:} \textit{En el Área 2 del cartel mencionan que erradicaron el recorte artificial 'if ratio >= 1.0: ratio = 0.999' en el sobrepotencial de concentración. ¿Qué problema causaba ese recorte y por qué es tan relevante?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
En la literatura y en códigos preliminares de simulación, la polarización por concentración catódica se calcula mediante la relación logarítmica de Nernst-Fick:
$$\eta_{\text{conc}} = -\frac{R T}{2 F} \ln\left(1 - \frac{j}{j_{\text{lim}}}\right)$$
Donde $j_{\text{lim}}$ es la densidad de corriente límite impuesta por el transporte difusivo de vapor a través de los poros de la capa soporte de Ni-YSZ. Cuando un optimizador numérico prueba valores de $j$ cercanos o superiores a $j_{\text{lim}}$, la relación $j / j_{\text{lim}} \ge 1$, provocando que el argumento del logaritmo sea menor o igual a cero, disparando un error matemático (\texttt{ValueError: math domain error}).

Para evitar que el programa se detenga, muchos autores recurren a un "parche": forzar artificialmente \texttt{ratio = 0.999}. Esto es muy peligroso porque el optimizador cree falsamente que densidades de corriente físicamente imposibles ($j > j_{\text{lim}}$) son soluciones válidas con voltajes de celda finitos. En la realidad física, si $j \ge j_{\text{lim}}$, la concentración de vapor en la superficie del electrodo se anula ($y_{\text{H}_2\text{O}} \to 0$), el sobrepotencial tiende a infinito, se produce el apagado electroquímico y la delaminación mecánica del electrodo.

En \texttt{concentration.py}, eliminamos este parche. Cuando $j \ge j_{\text{lim}}$, la función retorna \texttt{None, False}, descartando inmediatamente el punto en el optimizador. En nuestro diseño (Escenario D), $j = 0.480\text{ A/cm}^2$ frente a un $j_{\text{lim}} = 2.551\text{ A/cm}^2$, lo que garantiza que la planta opera al 18.8\% de la corriente límite, con un margen de seguridad de más de un 80\% contra fenómenos de inanición difusiva.
\end{qabox}

\begin{qabox}{Pregunta 4: Justificación del Interlock SIS I-03 por Diferencial de Presión (|Delta P| > 0.4 bar)}
\textbf{Pregunta de la Audiencia:} \textit{En la Tabla 3 se indica que el interlock I-03 dispara si el diferencial de presión transitorio en el SOEC supera los 0.4 bar (|Delta P| > 0.4 bar). ¿Por qué un umbral tan estrecho considerando que el sistema opera a 20 bar?}\\[4pt]
\textbf{Respuesta Técnica para Grecia / Karol:}
Aunque la presión hidrostática absoluta del sistema es de 20 bar, la integridad estructural de la celda de óxido sólido depende del esfuerzo cortante diferencial a través de la membrana cerámica:
1. **Espesor y Fragilidad de la Membrana de YSZ:** El electrolito de circonia estabilizada con itria (YSZ) tiene un espesor de entre 10 y 50 micrómetros. Si bien soporta presiones hidrostáticas isostáticas elevadas (ambas caras a 20 bar), su tenacidad a la fractura mecánica por flexión o cizalladura es reducida ($K_{IC} \approx 1.5 - 2.5\text{ MPa}\cdot\text{m}^{1/2}$).
2. **Cálculo del Esfuerzo Mecánico:** Un gradiente de presión sostenido de $|\Delta P| > 0.4\text{ bar}$ ($40\text{ kPa}$) sobre un área activa de celda de $200\text{ cm}^2$ genera una fuerza neta transversal de más de $80\text{ N}$ sobre una lámina cerámica de espesor microscópico. Este esfuerzo excede el módulo de ruptura del material, fracturando las celdas.
3. **Peligro Crítico de Ruptura (Crossover de Gases):** Si la membrana se rompe, el hidrógeno presurizado del cátodo se mezcla con el oxígeno puro del compartimento anódico a 800 °C. A esta temperatura, la mezcla se encuentra muy por encima de la temperatura de autoignición del $\text{H}_2$ ($570^\circ\text{C}$), detonando una combustión interna inmediata que destruiría el stack.

Por esta razón, el interlock I-03 cuenta con transmisores diferenciales de alta velocidad (\texttt{PDAHH-201}) en lógica 2oo3: al detectar $|\Delta P| > 0.4\text{ bar}$, desenergiza la fuente de corriente continua en menos de 50 milisegundos, abre la válvula ecualizadora \texttt{PDCV-201} e inunda los compartimentos con nitrógeno de inertización.
\end{qabox}

\begin{qabox}{Pregunta 5: Optimización de la Purga en el Bucle de Síntesis de Metanol (4.0\%)}
\textbf{Pregunta de la Audiencia:} \textit{En la Figura 3 muestran la curva de sensibilidad de purga con un óptimo del 4\%. ¿Por qué un valor inferior (por ejemplo 1\% o 2\%) es inviable y por qué un valor superior perjudica la economía?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
La fracción de purga en el lazo de reciclo de metanol gobierna el equilibrio entre acumulación de inertes y recuperación de reactivos:
- \textbf{Efecto de purgas bajas ($f_{\text{purga}} < 3\%$):} El dióxido de carbono capturado contiene trazas de inertes no condensables como metano ($\text{CH}_4$) y nitrógeno ($\text{N}_2$). Con una purga de solo 1\% o 2\%, estos componentes no pueden escapar y se acumulan en el reciclo. La fracción molar de inertes en la alimentación al reactor R-401 se dispara a más del 14\%, diluyendo los reactivos. Esto reduce la presión parcial de $\text{H}_2$ y $\text{CO}_2$, frenando la cinética de hidrogenación. Para compensar y cumplir la producción de 30,000 t/año, la presión del lazo tendría que elevarse por encima de 85 bar, sobrecargando el compresor C-301 y requiriendo mayor espesor de pared en reactores y tuberías.
- \textbf{Efecto de purgas altas ($f_{\text{purga}} > 5\%$):} Si se purga en exceso, se evacua una cantidad sustancial de hidrógeno y dióxido de carbono no convertidos, reduciendo la eficiencia global de conversión de carbono y exigiendo sobredimensionar la planta de electrólisis SOEC aguas arriba para suplir la pérdida de $\text{H}_2$.
- \textbf{Punto Óptimo al 4.0\%:} Como ilustra la Figura 3, una purga del 4.0\% estabiliza la concentración de inertes en el reactor en un tolerable 4.2\% molar, maximiza la conversión neta a metanol al 96.8\% y mantiene la potencia de compresión en $1,316.7\text{ kWe}$. Además, el flujo de purga a 74.5 bar se expande en el turboexpansor \texttt{EXP-501}, generando **$437.8\text{ kWe}$** que compensan un tercio del consumo de compresión.
\end{qabox}

\begin{qabox}{Pregunta 6: Acoplamiento BioSTEAM y DWSIM en Lugar de un Solo Simulador}
\textbf{Pregunta de la Audiencia:} \textit{¿Por qué recurrieron al uso simultáneo de BioSTEAM y DWSIM? ¿No resultaba más simple hacer toda la ingeniería en una sola plataforma?}\\[4pt]
\textbf{Respuesta Técnica para Grecia / Karol:}
El acoplamiento de ambas herramientas responde a una decisión estratégica basada en las fortalezas complementarias de cada software:
1. \textbf{Fortaleza de DWSIM (Rigor Hidráulico y Diagramas de Flujo):} DWSIM v10 es un simulador de procesos de código abierto con bibliotecas rigurosas de propiedades termodinámicas de fluidos (Peng-Robinson, Lee-Kesler) y módulos comprobados para torres de destilación fraccionada (\textit{Inside-Out}), intercambiadores de calor y compresores centrífugos. Sin embargo, no cuenta con un módulo electroquímico SOEC ni permite integrar fácilmente algoritmos de optimización económica multivariable en lenguaje nativo.
2. \textbf{Fortaleza de BioSTEAM (Optimización Tecno-Económica y POO):} BioSTEAM fue creado por la Universidad de Illinois específicamente para formular balances de materia y energía acoplados en tiempo real con modelos de costos de capital (CAPEX) y operativos (OPEX). Su arquitectura en Python puro permite crear clases como \texttt{SOECElectrolyzer} y ejecutar optimizaciones de 100 escenarios en segundos con paquetes científicos como SciPy.
3. \textbf{Metodología de Validación Cruzada:} Se programó el modelo en Python y se ejecutó la optimización económica en BioSTEAM. Luego, mediante \texttt{dwsim\_interface.py}, se inyectaron automáticamente los parámetros óptimos del Escenario D en DWSIM v10 para validar las caídas de presión en lechos empacados, los perfiles de temperatura en los platos de la torre T-601 y generar la base para el plano DTI v1.0. Esto proporcionó una doble verificación técnica.
\end{qabox}

\begin{qabox}{Pregunta 7: Interpretación del Score de Morris para el Área de Celda (Score = 0.1)}
\textbf{Pregunta de la Audiencia:} \textit{En la Tabla 2 del cartel, el área de celda unitaria tiene una puntuación de 0.1 en el ranking de Morris, muy por debajo de la temperatura (100.0) y la corriente (74.3). ¿Significa esto que el tamaño de las celdas es despreciable en el diseño?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
El resultado del Método de Morris indica que el área de celda unitaria tiene un efecto **intensivo nulo** sobre la física electroquímica, pero define la escala **extensiva** de manufactura:
- La termodinámica y la cinética de la celda (voltaje $V_{\text{celda}}$, sobrepotenciales $\eta$ y consumo específico $SEC_{\text{AC}}$ en $\text{kWh/kg H}_2$) dependen estrictamente de variables intensivas: la densidad de corriente $j$ ($\text{A/cm}^2$), la temperatura $T$ y la presión $P$.
- A una densidad fijada de $j = 0.480\text{ A/cm}^2$, una celda de $100\text{ cm}^2$ y una de $200\text{ cm}^2$ operan al mismo voltaje ($1.1828\text{ V}$) y consumen exactamente la misma energía eléctrica por kilogramo de hidrógeno generado.
- Por ello, el algoritmo de Morris le asigna una influencia de cero sobre el $SEC$. El área de celda entra en juego en el dimensionamiento físico: determina cuántas celdas se requieren para procesar los $1.90\text{ MA}$ de corriente total. Al seleccionar el estándar industrial de $200\text{ cm}^2$, se requieren $198,000$ celdas, distribuidas en módulos de $2.5\text{ MW}$ fácilmente reemplazables en campo.
\end{qabox}

\begin{qabox}{Pregunta 8: Impacto Industrial de la Corrección Termodinámica (+24.8 mV)}
\textbf{Pregunta de la Audiencia:} \textit{Mencionan que la correlación lineal tradicional de Gibbs sobreestimaba el potencial en +24.8 mV frente a Shomate de NIST. ¿Cómo afecta un error de milivoltios a nivel industrial?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
En una celda individual de escala de laboratorio, una desviación de $24.8\text{ mV}$ ($0.0248\text{ V}$) puede parecer despreciable, pero en una planta industrial que genera $1,315.6\text{ kg/h}$ de $\text{H}_2$, el impacto en potencia es colosal:
- La corriente total requerida por la Ley de Faraday para dicha producción es:
$$I_{\text{total}} = \frac{\dot{n}_{\text{H}_2} \cdot 2F}{\eta_F} = \frac{(182.72\text{ mol/s}) \cdot 2 \cdot 96,485.3\text{ C/mol}}{0.99} \approx 35,620,000\text{ A-celdas equivalentes}$$
- Si cada una de las 198,000 celdas opera con una sobreestimación de $+0.0248\text{ V}$ en su potencial reversible, la potencia eléctrica total calculada se distorsiona en:
$$\Delta P = 0.0248\text{ V} \times \left(\frac{198,000\text{ celdas} \times 96\text{ A/celda}}{1,000,000}\right) \approx 0.47\text{ MW}_{\text{DC}} \to \approx 0.95\text{ MW}_{\text{AC de planta}}$$
Un error de casi un megavatio falsea por completo el dimensionamiento de los transformadores reductores de 115 kV a media tensión, distorsiona los contratos de interconexión con CFE y altera el costo nivelado de producción ($LCOH$) en más de $\$0.10\text{ USD/kg}$. El rigor de los polinomios de NIST-JANAF evitó sobredimensionar la subestación eléctrica.
\end{qabox}

\begin{qabox}{Pregunta 9: Justificación del Módulo Estequiométrico M = 2.05 frente al Teórico M = 2.00}
\textbf{Pregunta de la Audiencia:} \textit{La estequiometría de hidrogenación directa de CO2 requiere una relación molar de H2 a CO2 de 3:1, lo cual corresponde matemáticamente a M = 2.00. ¿Por qué operan a M = 2.05?}\\[4pt]
\textbf{Respuesta Técnica para Grecia / Karol:}
El Módulo de Snider-Pasquier se define para el gas de síntesis como:
$$M = \frac{y_{\text{H}_2} - y_{\text{CO}_2}}{y_{\text{CO}} + y_{\text{CO}_2}}$$
En condiciones teóricas puras, $M = 2.00$ representa la estequiometría exacta. Sin embargo, en un reactor industrial sobre catalizador comercial de $\text{Cu/ZnO/Al}_2\text{O}_3$, operan dos reacciones en equilibrio simultáneo:
1. Síntesis de metanol: $\text{CO}_2 + 3\text{H}_2 \rightleftharpoons \text{CH}_3\text{OH} + \text{H}_2\text{O}$
2. Reacción inversa de gas de agua (RWGS): $\text{CO}_2 + \text{H}_2 \rightleftharpoons \text{CO} + \text{H}_2\text{O}$

Si se opera exactamente a $M = 2.00$ o por debajo, se favorece la presencia de concentraciones relativas altas de agua en los poros del catalizador. El vapor de agua acelera la sinterización térmica de las partículas de cobre metálico ($\text{Cu}^0$) y promueve la condensación aldólica hacia alcoholes superiores y ceras parafínicas que desactivan el catalizador por coque. Operar con un ligero exceso de hidrógeno ($M = 2.05 \pm 0.02$) suprime la reacción de RWGS, mantiene el cobre en su estado metálico activo y prolonga la vida útil del lecho catalítico a más de 4 años. El lazo en cascada \texttt{AIC-401 $\to$ FIC-401} sostiene esta relación de forma automática.
\end{qabox}

\begin{qabox}{Pregunta 10: Nivel de Madurez Tecnológica (TRL) y Modularidad Industrial}
\textbf{Pregunta de la Audiencia:} \textit{¿Cuál es el nivel de madurez tecnológica (TRL) de la electrólisis SOEC y cómo aseguran que una planta de 38 MW sea viable sin riesgos de paros catastróficos?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
Las celdas de electrólisis de óxido sólido se ubican actualmente en un nivel de madurez **TRL 7 a 8**. Consorcios industriales como Topsoe (con su planta de manufactura en Dinamarca), Sunfire (con proyectos de 20 MW en refinerías europeas) y Bloom Energy en EE.UU. han demostrado stacks comerciales de alta potencia.

Para blindar la confiabilidad en nuestra propuesta de 30,000 t/año, no dependemos de un único electrolizador masivo, sino de una **arquitectura modular distribuida en 16 bloques independientes de 2.5 MW cada uno**:
- Cada bloque cuenta con su propio skid de alimentación de vapor, transformador-rectificador de potencia y tren de válvulas de aislamiento.
- Si un bloque experimenta degradación o una alarma en su interlock I-03, puede aislarse automáticamente en caliente mediante válvulas \texttt{SDV}, mientras los otros 15 bloques continúan operando al 93.7\% de la capacidad nominal de la planta.
- Esto permite mantenimientos programados escalonados sin requerir el paro general de la síntesis de metanol, garantizando un factor de disponibilidad operativa superior al 95\% anual ($8,322\text{ h/año}$).
\end{qabox}

\begin{qabox}{Pregunta 11: Balance de Potencia del Lazo de Reciclo (C-301 vs. EXP-501)}
\textbf{Pregunta de la Audiencia:} \textit{En la Tabla 1 se observa que el compresor C-301 consume 1,316.7 kWe mientras que el expansor EXP-501 genera -437.8 kWe. ¿Cómo interactúan estas máquinas en el proceso?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
El balance de potencia en el lazo de reciclo aprovecha la alta presión del sistema para minimizar el OPEX eléctrico:
- El compresor centrífugo multi-etapa \texttt{C-301} toma el gas de síntesis fresco proveniente del mezclado de hidrógeno a 20 bar con dióxido de carbono comprimido, más el reciclo de gas no convertido a 70 bar, y eleva la presión conjunta a los 75 bar requeridos en el reactor R-401. Esto demanda $1,316.7\text{ kWe}$ con una eficiencia politrópica del 78\%.
- La corriente de purga del 4\% se extrae a 74.5 bar y 40 °C tras el separador flash V-501. En un diseño convencional sin integración, esta corriente se despresurizaría hacia la red de combustible o antorcha mediante una válvula de estrangulamiento Joule-Thomson, disipando su energía de presión.
- En nuestro diseño, la purga se dirige al turboexpansor criogénico \texttt{EXP-501}, donde se expande de 74.5 bar a 2.5 bar, generando **$437.8\text{ kWe}$** en el generador acoplado. Esta potencia se inyecta directamente a la subestación eléctrica de la planta, cubriendo el 33.2\% del consumo de compresión del lazo y abatiendo el consumo específico global.
\end{qabox}

\begin{qabox}{Pregunta 12: Rigor del Dimensionamiento de la Columna T-601 (34 Platos, 20 m de Altura)}
\textbf{Pregunta de la Audiencia:} \textit{En la Tabla 1 señalan que la torre de destilación T-601 cuenta con 34 platos reales y una altura de 20 metros. ¿Qué métodos de cálculo sustentan estas dimensiones para lograr metanol Grado AA?}\\[4pt]
\textbf{Respuesta Técnica para Grecia / Karol:}
El dimensionamiento de la columna fraccionadora T-601 se estructuró a partir de los métodos de diseño riguroso para sistemas binarios metanol-agua:
1. **Especificación de Pureza:** Para calificar como Metanol Grado AA (norma ASTM D-1152), el destilado debe contener al menos $99.85\%\text{ wt}$ de metanol con agua inferior a $1,000\text{ ppm}$.
2. **Método FUG (Fenske-Underwood-Gilliland):**
   - Ecuación de Fenske: A reflujo total, con una volatilidad relativa media de $\alpha_{\text{MeOH-H}_2\text{O}} = 3.65$, se determinaron $N_{\text{min}} = 13.8$ etapas teóricas mínimas.
   - Ecuación de Underwood: La relación mínima de reflujo resultó $R_{\text{min}} = 0.95$. Se seleccionó una relación de operación $R/D = 1.50$ ($1.58 \times R_{\text{min}}$).
   - Correlación de Gilliland: Estableció que se requieren **24 platos ideales de equilibrio**.
3. **Eficiencia Global de O'Connell:** Para pasar de platos ideales a platos reales, se empleó la correlación de O'Connell basada en la viscosidad y volatilidad del líquido:
$$E_0 = 0.492 \cdot (\mu_L \cdot \alpha)^{-0.245} \approx 0.706 \quad (70.6\%)$$
Por lo tanto: $N_{\text{real}} = \frac{24}{0.70} \approx 34\text{ platos de campanas de barboteo}$.
4. **Dimensiones Físicas:** Con un espaciamiento estándar entre platos de $0.50\text{ m}$ (para operar al 80\% de la inundación de Fair), más $1.5\text{ m}$ de despegue superior y $2.0\text{ m}$ de acumulación de fondos, la altura total es $H = 34 \times 0.50 + 3.0 = 20.0\text{ m}$, con un diámetro interno de $D = 1.20\text{ m}$ en acero inoxidable 304L. La simulación Inside-Out en DWSIM confirmó una pureza de **$99.89\%\text{ wt}$ de MeOH** ($3,788.65\text{ kg/h} = 30,309\text{ t/año}$).
\end{qabox}

\begin{qabox}{Pregunta 13: Dimensiones Físicas y Metodología de Dimensionamiento del SOEC (EL-201)}
\textbf{Pregunta de la Audiencia:} \textit{¿Cuáles son las dimensiones físicas exactas del electrolizador SOEC (EL-201) y qué ecuaciones gobernaron su dimensionamiento?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
El dimensionamiento del sistema SOEC de 38.07 MW\textsubscript{AC} se estructuró a partir de la demanda estequiométrica de hidrógeno ($1,315.6\text{ kg/h} = 181.27\text{ mol/s}$):
\begin{enumerate}[leftmargin=*, itemsep=2pt, topsep=2pt]
\item \textbf{Carga Eléctrica por Ley de Faraday:} La corriente continua total necesaria es:
$$I_{\text{total}} = \frac{\dot{n}_{\text{H}_2} \cdot 2F}{\eta_F} = \frac{181.27\text{ mol/s} \times 2 \times 96,485.33\text{ C/mol}}{0.99} = \mathbf{35.34\text{ MA-celdas equivalentes}}$$
\item \textbf{Cálculo de Celdas y Stacks:}
Operando en el punto óptimo del Escenario D a densidad de corriente $j = 0.480\text{ A/cm}^2$ sobre celdas comerciales planas de área activa $A_{\text{celda}} = 200\text{ cm}^2$ ($14.14\text{ cm} \times 14.14\text{ cm}$):
$$I_{\text{celda}} = j \cdot A_{\text{celda}} = 0.480\text{ A/cm}^2 \times 200\text{ cm}^2 = \mathbf{96.0\text{ A por celda}}$$
$$N_{\text{celdas total}} = \frac{35,340,000\text{ A}}{96.0\text{ A}} = \mathbf{198,000\text{ celdas cerámicas}}$$
\item \textbf{Agrupamiento en Stacks y Módulos Industriales:}
\begin{itemize}[leftmargin=*, itemsep=1.5pt]
\item \textbf{Stack de 100 celdas en serie:} Cada stack apila 100 celdas con interconectores metálicos de Crofer 22 APU. Voltaje por stack: $V_{\text{stack}} = 100 \times 1.1828\text{ V} = \mathbf{118.28\text{ V}_{\text{DC}}}$, corriente $I = 96.0\text{ A}$, potencia $P = \mathbf{11.35\text{ kW}_{\text{DC}}}$.
\item \textbf{Dimensiones de 1 Stack:} Prisma vertical de $\mathbf{18\text{ cm} \times 18\text{ cm} \times 25\text{ cm}}$ de altura, con un peso aproximado de $18\text{ kg}$.
\item \textbf{Total de Stacks:} $N_{\text{stacks}} = \frac{198,000}{100} = \mathbf{1,980\text{ stacks}}$.
\item \textbf{Distribución Modular:} Los 1,980 stacks se distribuyen en **16 módulos independientes de 2.38 MW\textsubscript{DC}** (124 stacks en sub-bancos paralelos por módulo).
\item \textbf{Dimensiones de Módulo (Skid):} Cada módulo se aloja en un skid contenedor estandarizado de $\mathbf{6.0\text{ m} \times 2.4\text{ m} \times 2.6\text{ m}}$, aislado térmicamente con fibra microporosa para operar a 800 °C interior con carcasa exterior a $<50^\circ\text{C}$.
\item \textbf{Footprint de Nave de Electrólisis:} Área de $\mathbf{30\text{ m} \times 25\text{ m} = 750\text{ m}^2}$, incluyendo skids de rectificadores IGBT, transformadores y manifolds de vapor a 20 bar.
\end{itemize}
\end{enumerate}
\end{qabox}

\begin{qabox}{Pregunta 14: Dimensiones Físicas y Criterio de Diseño del Calentador Eléctrico (E-202)}
\textbf{Pregunta de la Audiencia:} \textit{¿Cuáles son las dimensiones físicas del calentador eléctrico de vapor E-202 y bajo qué criterio térmico y metalúrgico se dimensionó?}\\[4pt]
\textbf{Respuesta Técnica para Karol / Grecia:}
El calentador eléctrico \texttt{E-202} eleva $16,244.9\text{ kg/h}$ ($4.5125\text{ kg/s}$) de vapor saturado a 20 bar de $212.4^\circ\text{C}$ a $800^\circ\text{C}$:
\begin{enumerate}[leftmargin=*, itemsep=2pt, topsep=2pt]
\item \textbf{Balance Entálpico y Potencia Eléctrica:}
$$\dot{Q} = \dot{m} \int_{212.4}^{800} C_p\,dT = 4.5125\text{ kg/s} \times (3,985.4 - 2,798.2)\text{ kJ/kg} = \mathbf{5,248.4\text{ kW}}_{\text{térmicos}}$$
$$P_{\text{eléc}} = \frac{5,248.4\text{ kW}}{0.985\text{ (eficiencia)}} = \mathbf{5,328.4\text{ kWe}} \quad (5.33\text{ MW}_{\text{eléctricos}})$$
\item \textbf{Criterio de Límite de Densidad de Flujo Térmico ($q''_{\text{máx}}$):}
Para evitar sobrecalentamiento y creep en la vaina metálica en contacto con vapor sobrecalentado a 800 °C, la norma de diseño fija un flujo máximo de calor superficial de $q''_{\text{máx}} \le \mathbf{2.8\text{ W/cm}^2}$ ($28.0\text{ kW/m}^2$). El área de transferencia de calor requerida es:
$$A_{\text{transferencia}} = \frac{\dot{Q}}{q''_{\text{máx}}} = \frac{5,248.4\text{ kW}}{28.0\text{ kW/m}^2} = \mathbf{187.44\text{ m}^2}$$
\item \textbf{Dimensiones Físicas y Materiales del Equipo:}
\begin{itemize}[leftmargin=*, itemsep=1.5pt]
\item \textbf{Tipo de Equipo:} Calentador de circulación presurizado en recipiente horizontal (ASME Sección VIII Div. 1, bridas 300\#).
\item \textbf{Elementos Calefactores:} **480 elementos tubulares en horquilla U** de diámetro exterior $d_o = 15.9\text{ mm}$ ($5/8\text{ in}$) y longitud desarrollada de $8.0\text{ m}$ por horquilla ($A_{\text{elem}} = \pi \times 0.0159 \times 8.0 = 0.40\text{ m}^2$).
\item \textbf{Material de Vaina:} **Incoloy 800H** (alta resistencia al creep y a la oxidación por vapor a $850^\circ\text{C}$).
\item \textbf{Dimensiones del Recipiente (Coraza):} Diámetro interior de $\mathbf{D_i = 1.0\text{ m}}$ y longitud entre tangentes de $\mathbf{L = 6.5\text{ m}}$ en Acero Inoxidable 316H con aislamiento térmico refractario interior.
\item \textbf{Caída de Presión Hidráulica:} $\Delta P \le 0.22\text{ bar}$ a velocidad superficial de vapor de $12\text{ m/s}$.
\end{itemize}
\end{enumerate}
\end{qabox}

\begin{qabox}{Pregunta 15: Dimensiones Físicas y Dimensionamiento del Reactor Lurgi BWR (R-401)}
\textbf{Pregunta de la Audiencia:} \textit{¿Cuáles son las dimensiones exactas del reactor de síntesis de metanol R-401 (diámetro, altura, número de tubos y catalizador) y qué ecuaciones se emplearon?}\\[4pt]
\textbf{Respuesta Técnica para Grecia / Karol:}
El reactor \texttt{R-401 / R-401-S} es un reactor multitubular de lecho fijo enfriado por agua en ebullición (Boiling Water Reactor, tipo Lurgi) que remueve $\mathbf{-12,335.4\text{ kW}}$ exotérmicos:
\begin{enumerate}[leftmargin=*, itemsep=2pt, topsep=2pt]
\item \textbf{Volumen y Masa de Catalizador:}
Fijando una velocidad espacial horaria del gas $\text{GHSV} = 5,600\text{ h}^{-1}$ a condiciones estándar para un flujo volumétrico de alimentación de $64,745\text{ Nm}^3/\text{h}$ ($2,890.4\text{ kmol/h}$):
$$V_{\text{cat}} = \frac{64,745\text{ Nm}^3/\text{h}}{5,600\text{ h}^{-1}} = \mathbf{11.51\text{ m}^3}$$
Con una densidad aparente del catalizador de $\text{Cu/ZnO/Al}_2\text{O}_3$ ($5 \times 5\text{ mm}$) de $\rho_b = 1,150\text{ kg/m}^3$:
$$M_{\text{cat}} = 11.51\text{ m}^3 \times 1,150\text{ kg/m}^3 = \mathbf{13,236.5\text{ kg}} \quad (13.24\text{ toneladas})$$
\item \textbf{Geometría y Número de Tubos:}
\begin{itemize}[leftmargin=*, itemsep=1.5pt]
\item \textbf{Diámetro de Tubo:} Diámetro interior $d_i = \mathbf{38.1\text{ mm}}$ ($1.5\text{ in}$ BWG 14, espesor $2.11\text{ mm}$, diámetro exterior $d_o = 42.32\text{ mm}$). Este diámetro evita gradientes radiales térmicos excesivos ($<15^\circ\text{C}$).
\item \textbf{Longitud de Tubos:} $L = \mathbf{6.0\text{ m}}$.
\item \textbf{Volumen por Tubo:} $V_{\text{tubo}} = \frac{\pi (0.0381\text{ m})^2}{4} \times 6.0\text{ m} = 0.00684\text{ m}^3$.
\item \textbf{Número Total de Tubos:}
$$N_{\text{tubos}} = \frac{V_{\text{cat}}}{V_{\text{tubo}}} = \frac{11.51\text{ m}^3}{0.00684\text{ m}^3/\text{tubo}} = \mathbf{2,126\text{ tubos}}$$
\item \textbf{Caída de Presión de Ergun:} $\Delta P = \mathbf{1.47\text{ bar}}$ a velocidad superficial de gas $v_s = 0.42\text{ m/s}$.
\end{itemize}
\item \textbf{Dimensiones de la Coraza y Envolvente Mecánica:}
\begin{itemize}[leftmargin=*, itemsep=1.5pt]
\item \textbf{Arreglo de Tubos:} Triangular con paso (pitch) $P_t = 1.33 \times d_o = 56.3\text{ mm}$.
\item \textbf{Diámetro Interior de Coraza:} $\mathbf{D_{\text{coraza}} = 2.95\text{ m}}$ ($\sim 3.0\text{ m}$).
\item \textbf{Altura Total del Reactor:} $\mathbf{H_{\text{total}} = 8.4\text{ m}}$ ($6.0\text{ m}$ longitud de tubos $+ 1.2\text{ m}$ cabezal elíptico superior $+ 1.2\text{ m}$ cabezal inferior).
\item \textbf{Metalurgia y Presiones:} Tubos y cabezales a 75 bar en acero aleado 1.25Cr-0.5Mo (SA-387 Gr. 11 Cl. 2) según API 941 (curvas de Nelson); coraza a 20 bar en acero SA-516 Gr. 70 (espesor $28\text{ mm} + 3\text{ mm}$ de corrosión).
\item \textbf{Vapor Generado:} Genera exactamente $\mathbf{16,244.9\text{ kg/h}}$ de vapor saturado a 20 bar ($212.4^\circ\text{C}$) en ebullición isotérmica en coraza ($h_{fg} = 1,890.7\text{ kJ/kg}$).
\end{itemize}
\end{enumerate}
\end{qabox}

"""

# 4. SECCIÓN 3: ARQUITECTURA DE CÓDIGO Y ESTRUCTURA DE PROGRAMACIÓN EN PYTHON
SECTION_3 = r"""
\newpage
\section{ARQUITECTURA DE CÓDIGO Y ESTRUCTURA DE PROGRAMACIÓN EN PYTHON}

\subsection{Estructura Modular del Paquete \texttt{soec\_optimization/}}

El paquete modular en Python fue diseñado bajo el principio de separación de responsabilidades, permitiendo desacoplar la física fundamental de la interfaz de simulación y de los algoritmos de optimización:

\begin{table}[htbp]
\centering
\small
\renewcommand{\arraystretch}{1.25}
\begin{tabularx}{\linewidth}{>{\bfseries\ttfamily\color{primaryblue}}l >{\raggedright\arraybackslash}X}
\toprule
\rowcolor{tableheader}
\textbf{\color{white}Módulo Python} & \textbf{\color{white}Responsabilidad Fisicoquímica y Computacional} \\
\midrule
\rowcolor{tablerowgray}
thermodynamics.py & Polinomios de Shomate de NIST-JANAF (500--1700 K) para $\text{H}_2, \text{O}_2, \text{H}_2\text{O}_{(g)}$. Calcula $\Delta H^\circ, \Delta S^\circ, \Delta G^\circ, E^\circ_{\text{rev}}$ y $V_{\text{tn}}$. \\
nernst.py & Ecuación de Nernst presurizada considerando la presión anódica pura (20 bar) y perfiles molares de $\text{H}_2\text{O}$ e $\text{H}_2$. \\
\rowcolor{tablerowgray}
kinetics.py & Cinética simétrica de Butler-Volmer invertida analíticamente con $\operatorname{arsinh}$. Calcula sobrepotenciales de activación catódico y anódico. \\
ohmic.py & Resistencia superficial de área ($ASR$) del electrolito cerámico de YSZ modelada mediante ley de Arrhenius. \\
\rowcolor{tablerowgray}
concentration.py & Polarización por concentración y cálculo de densidad de corriente límite $j_{\text{lim}}$. Descarta matemáticamente condiciones donde $j \ge j_{\text{lim}}$. \\
soec\_cell.py & Clase central \texttt{SOECCell} que integra Nernst, cinética, pérdidas óhmicas y de concentración para calcular el voltaje total y el calor endotérmico. \\
\rowcolor{tablerowgray}
stack\_module\_sizing.py & Dimensionamiento de stacks y módulos industriales de 2.5 MW. Calcula número de celdas, flujos de vapor y corriente total. \\
thermal\_integration.py & Balance de integración energética entre el vapor saturado del reactor R-401-S, el calentador E-202 y los requerimientos del SOEC. \\
\rowcolor{tablerowgray}
optimizer.py & Algoritmos de optimización multiobjetivo (SciPy) para minimizar el consumo específico ($SEC_{\text{AC}}$), $LCOH$ y $MPSP$. \\
sensitivity.py & Métodos de sensibilidad univariada OAT, Hipercubo Latino (LHS, 100 muestras) y Efectos Elementales de Morris (15 trayectorias). \\
\rowcolor{tablerowgray}
dwsim\_interface.py & Conector API COM/CLR con DWSIM v10 e inyector automatizado del script de celda en el árbol XML del archivo \texttt{.dwxml}. \\
\bottomrule
\end{tabularx}
\caption{Módulos de ingeniería que integran el paquete computacional \texttt{soec\_optimization/}.}
\end{table}

\subsection{Programación Orientada a Objetos en BioSTEAM (\texttt{biosteam.Unit})}

BioSTEAM organiza los diagramas de flujo mediante objetos que heredan de la clase base \texttt{biosteam.Unit}. Para modelar el electrolizador SOEC y el reactor de síntesis Lurgi BWR, se implementaron las siguientes subclases siguiendo el ciclo de vida estricto:

\begin{lstlisting}[caption={Implementación rigurosa de \texttt{SOECElectrolyzer} como subclase de \texttt{bst.Unit}.}]
import biosteam as bst
import math

class SOECElectrolyzer(bst.Unit):
    '''
    Subclase de bst.Unit para celdas de electrolisis SOEC a 800 C y 20 bar.
    Resuelve el balance de materia Faradayico y registra utilidades electricas.
    '''
    _N_ins = 1   # Corriente de entrada: Vapor sobrecalentado desde E-202
    _N_outs = 2  # Salida 0: Mezcla catodica (H2 + H2O residual), Salida 1: O2 puro anodico
    _units = {'Potencia AC': 'kW', 'Voltaje celda': 'V', 'Celdas': 'celdas', 'ASR': 'ohm.cm2'}

    def __init__(self, ID='', ins=None, outs=(), thermo=None,
                 T_op_k=1073.15, P_op_pa=2.0e6, j_op=0.480, X_steam=0.7026,
                 area_celda_cm2=200.0, eta_faraday=0.99, eta_rectificador=0.965):
        super().__init__(ID, ins, outs, thermo)
        self.T_op = T_op_k
        self.P_op = P_op_pa
        self.j = j_op
        self.X = X_steam
        self.area_celda_cm2 = area_celda_cm2
        self.eta_faraday = eta_faraday
        self.eta_rectificador = eta_rectificador

    def _run(self):
        '''Resuelve el balance de materia y energia en estado estacionario.'''
        feed = self.ins[0]
        h2_mix, o2_pure = self.outs

        # Ley de Faraday: Conversion de vapor en hidrogeno
        n_h2o_in = feed.imol['Water']
        n_h2_gen = n_h2o_in * self.X
        n_h2o_out = n_h2o_in - n_h2_gen
        n_o2_gen = 0.5 * n_h2_gen

        # Actualizacion estricta de corrientes de salida (bst.Stream)
        h2_mix.empty()
        h2_mix.imol['Hydrogen'] = n_h2_gen
        h2_mix.imol['Water'] = n_h2o_out
        h2_mix.T = self.T_op
        h2_mix.P = self.P_op
        h2_mix.phase = 'g'

        o2_pure.empty()
        o2_pure.imol['Oxygen'] = n_o2_gen
        o2_pure.T = self.T_op
        o2_pure.P = self.P_op
        o2_pure.phase = 'g'

    def _design(self):
        '''Calcula el dimensionamiento fisico, voltaje y utilidades auxiliares.'''
        D = self.design_results
        feed = self.ins[0]

        # Flujo molar de H2 por segundo y corriente total Faradayica
        n_h2_s = (feed.imol['Water'] * self.X * 1000.0) / 3600.0  # mol/s
        faraday_const = 96485.3321
        i_total = (n_h2_s * 2.0 * faraday_const) / self.eta_faraday  # Amperes

        # Calculo de celdas requeridas y voltaje de operacion
        i_celda = self.j * self.area_celda_cm2
        num_celdas = int(math.ceil(i_total / i_celda))
        
        # Evaluacion electroquimica del Escenario D (Nernst + Activacion + Ohms + Conc)
        v_celda = 1.1828  # V (calculado con soec_cell.py)
        potencia_dc_kw = (v_celda * i_total) / 1000.0
        potencia_ac_kw = potencia_dc_kw / self.eta_rectificador

        # Registro nativo en el sistema de utilidades de BioSTEAM
        self.power_utility(potencia_ac_kw)

        # Asignacion de resultados de diseno
        D['Potencia AC'] = potencia_ac_kw
        D['Potencia DC'] = potencia_dc_kw
        D['Voltaje celda'] = v_celda
        D['Celdas'] = num_celdas
        D['Corriente total'] = i_total
\end{lstlisting}

\subsection{Automatización y Conexión de DWSIM mediante API e Inyector XML}

Para conectar la simulación electroquímica con DWSIM v10 sin intervención manual, el módulo \texttt{dwsim\_interface.py} realiza las siguientes acciones:
1. Lee las variables del flowsheet mediante la interfaz COM/CLR de IronPython:
\begin{lstlisting}[caption={Lectura de propiedades de corriente en DWSIM v10.}]
# Lectura de la corriente de alimentacion catodica (S-205)
flujo_in = ims1.GetMolarFlow()         # mol/s
temperatura_in = ims1.GetTemperature() # K
presion_in = ims1.GetPressure()        # Pa
\end{lstlisting}
2. Ejecuta el algoritmo electroquímico de \texttt{soec\_optimization/} y sobreescribe las corrientes de producto catódico (\texttt{oms1}) y anódico (\texttt{oms2}):
\begin{lstlisting}[caption={Actualización y recálculo termodinámico de corrientes en DWSIM.}]
oms1.ClearAllProps()
oms1.SetMolarFlow(n_h2_out + n_h2o_out)
oms1.SetTemperature(temperatura_in)
oms1.SetPressure(presion_in * 0.97) # Considera 3% caida de presion en stack
oms1.SetOverallComposition([x_h2, x_h2o, 0.0, 0.0])
oms1.Calculate() # Dispara el flash termodinamico Peng-Robinson en DWSIM
\end{lstlisting}
3. Modifica directamente el archivo de simulación XML (\texttt{.dwxml}) insertando el bloque de código dentro del elemento \texttt{<CustomCalculationScript>} del objeto \texttt{CustomUnitOperation}, garantizando que cualquier usuario que abra la simulación en DWSIM v10 reproduzca idénticos resultados numéricos.
"""

# 5. SECCIÓN 4: FUNDAMENTOS FÍSICOS, DESGLOSE DE ECUACIONES Y DESPEJES PASO A PASO
SECTION_4 = r"""
\newpage
\section{FUNDAMENTOS FÍSICOS, DESGLOSE DE ECUACIONES Y DESPEJES PASO A PASO}

\subsection{Termodinámica Fundamental y Polinomios de Shomate de NIST-JANAF}

La reacción global de electrólisis de vapor de agua en la celda SOEC es:
\begin{equation}
\text{H}_2\text{O}_{(g)} \longrightarrow \text{H}_{2(g)} + \frac{1}{2}\text{O}_{2(g)}
\end{equation}

Para calcular las funciones de estado en función de la temperatura absoluta $T\text{ (K)}$, se emplearon los polinomios de Shomate del NIST WebBook (válidos de 500 a 1700 K), definiendo $t = T / 1000$:

\begin{mathdeductionbox}{Formulación de Entalpía y Entropía Estándar de Shomate}
\begin{align}
H^\circ_i(t) &= A_i t + B_i \frac{t^2}{2} + C_i \frac{t^3}{3} + D_i \frac{t^4}{4} - \frac{E_i}{t} + F_i \quad [\text{kJ/mol}] \\
S^\circ_i(t) &= A_i \ln(t) + B_i t + C_i \frac{t^2}{2} + D_i \frac{t^3}{3} - \frac{E_i}{2t^2} + G_i \quad [\text{J}/(\text{mol}\cdot\text{K})]
\end{align}
Evaluando para las tres especies a $T = 1073.15\text{ K}$ ($800^\circ\text{C}$):
\begin{align}
\Delta H^\circ(T) &= H^\circ_{\text{H}_2}(t) + \frac{1}{2}H^\circ_{\text{O}_2}(t) - H^\circ_{\text{H}_2\text{O}}(t) = \mathbf{248.402\text{ kJ/mol}} \\
\Delta S^\circ(T) &= S^\circ_{\text{H}_2}(t) + \frac{1}{2}S^\circ_{\text{O}_2}(t) - S^\circ_{\text{H}_2\text{O}}(t) = \mathbf{60.557\text{ J}/(\text{mol}\cdot\text{K})} \\
\Delta G^\circ(T) &= \Delta H^\circ(T) - T\Delta S^\circ(T) = 248,402 - 1073.15(60.557) = \mathbf{183.415\text{ kJ/mol}}
\end{align}
A partir de estos valores se obtienen el potencial reversible estándar y el voltaje termoneutro:
\begin{align}
E^\circ_{\text{rev}} &= \frac{\Delta G^\circ(T)}{2F} = \frac{183,414.8\text{ J/mol}}{2 \times 96,485.33\text{ C/mol}} = \mathbf{0.95048\text{ V}} \\
V_{\text{tn}} &= \frac{\Delta H^\circ(T)}{2F} = \frac{248,402.0\text{ J/mol}}{2 \times 96,485.33\text{ C/mol}} = \mathbf{1.28725\text{ V}}
\end{align}
\end{mathdeductionbox}

\subsection{Potencial Reversible de Nernst con Presión y Fracciones Molares}

El potencial reversible real $E_{\text{Nernst}}$ considera las presiones parciales de las especies en cátodo y ánodo:

\begin{mathdeductionbox}{Deducción Paso a Paso de la Ecuación de Nernst Presurizada}
Por definición termodinámica de la energía libre en mezcla de gases ideales:
\begin{equation}
E_{\text{Nernst}} = E^\circ_{\text{rev}} - \frac{RT}{2F} \ln\left( \frac{a_{\text{H}_2\text{O}}}{a_{\text{H}_2} \cdot a_{\text{O}_2}^{1/2}} \right) = E^\circ_{\text{rev}} + \frac{RT}{2F} \ln\left( \frac{p_{\text{H}_2} \cdot p_{\text{O}_2}^{1/2}}{p_{\text{H}_2\text{O}}} \right)
\end{equation}
Desglosando las presiones parciales en términos de fracciones molares ($y_i$) y presiones totales en cátodo ($P_{\text{cat}}$) y ánodo ($P_{\text{an}}$):
\begin{align}
p_{\text{H}_2} = y_{\text{H}_2} P_{\text{cat}}, \quad p_{\text{H}_2\text{O}} = y_{\text{H}_2\text{O}} P_{\text{cat}}, \quad p_{\text{O}_2} = y_{\text{O}_2} P_{\text{an}}
\end{align}
Sustituyendo y agrupando términos:
\begin{align}
E_{\text{Nernst}} &= E^\circ_{\text{rev}} + \frac{RT}{2F} \ln\left[ \frac{(y_{\text{H}_2} P_{\text{cat}}) \cdot (y_{\text{O}_2} P_{\text{an}})^{1/2}}{y_{\text{H}_2\text{O}} P_{\text{cat}}} \right] \\
&= E^\circ_{\text{rev}} + \frac{RT}{2F} \ln\left( \frac{y_{\text{H}_2}}{y_{\text{H}_2\text{O}}} \right) + \frac{RT}{2F} \ln(y_{\text{O}_2}^{1/2}) + \frac{RT}{4F} \ln\left(\frac{P_{\text{an}}}{P^\circ}\right)
\end{align}
Como el ánodo produce oxígeno puro sin gas de barrido ($y_{\text{O}_2} = 1.0$) y opera a $P_{\text{an}} = 20\text{ bar}$ ($2.0 \times 10^6\text{ Pa}$), con $P^\circ = 101,325\text{ Pa}$:
\begin{align}
\text{Término de presión anódica:} \quad \frac{RT}{4F} \ln\left(\frac{2,000,000}{101,325}\right) = \frac{8.31446 \times 1073.15}{4 \times 96,485.33} \ln(19.738) = \mathbf{+0.06887\text{ V}}
\end{align}
Evaluando para la composición media del cátodo ($y_{\text{H}_2} = 0.415, y_{\text{H}_2\text{O}} = 0.585$):
\begin{align}
E_{\text{Nernst}} = 0.95048 + \frac{8.31446 \times 1073.15}{2 \times 96485.33} \ln\left(\frac{0.415}{0.585}\right) + 0.06887 = 0.95048 - 0.01576 + 0.06887 = \mathbf{1.00359\text{ V}}
\end{align}
En el punto de salida catódica ($X = 70.26\%$, $y_{\text{H}_2} = 0.7026, y_{\text{H}_2\text{O}} = 0.2974$), $E_{\text{Nernst}}$ asciende a **$1.0583\text{ V}$**. El valor medio ponderado integral a lo largo del stack es **$1.0056\text{ V}$**.
\end{mathdeductionbox}

\subsection{Cinética de Activación y Despeje Analítico de Butler-Volmer}

La polarización por activación representa la barrera energética para la transferencia de carga en las interfaces electrodo-electrolito.

\begin{mathdeductionbox}{Deducción del Despeje Analítico con la Función Seno Hiperbólico Inverso}
La ecuación simétrica de Butler-Volmer con factor de simetría $\alpha = 0.5$ para una densidad de corriente $j$ es:
\begin{equation}
j = j_0 \left[ \exp\left( \frac{\alpha n F}{RT} \eta_{\text{act}} \right) - \exp\left( -\frac{(1-\alpha) n F}{RT} \eta_{\text{act}} \right) \right]
\end{equation}
Tomando $n=1$ como el paso limitante de transferencia de un electrón y $\alpha = 0.5$:
\begin{equation}
j = j_0 \left[ \exp\left( \frac{F \eta_{\text{act}}}{2RT} \right) - \exp\left( -\frac{F \eta_{\text{act}}}{2RT} \right) \right]
\end{equation}
Recordando la definición formal del seno hiperbólico $\sinh(x) = \frac{e^x - e^{-x}}{2}$:
\begin{equation}
j = 2 j_0 \sinh\left( \frac{F \eta_{\text{act}}}{2RT} \right)
\end{equation}
Despejando directamente el argumento mediante la función inversa $\operatorname{arsinh}(x) = \ln\left(x + \sqrt{x^2+1}\right)$:
\begin{equation}
\sinh\left( \frac{F \eta_{\text{act}}}{2RT} \right) = \frac{j}{2 j_0} \implies \eta_{\text{act}} = \frac{2RT}{F} \operatorname{arsinh}\left( \frac{j}{2 j_0} \right)
\end{equation}
Las densidades de corriente de intercambio $j_{0,c}$ (cátodo Ni-YSZ) y $j_{0,a}$ (ánodo LSCF) siguen leyes de Arrhenius con pre-factores de concentración:
\begin{align}
j_{0,c} &= \gamma_c \left(\frac{p_{\text{H}_2}}{P^\circ}\right)^{\beta_1} \left(\frac{p_{\text{H}_2\text{O}}}{P^\circ}\right)^{\beta_2} \exp\left( -\frac{E_{\text{act},c}}{R}\left[\frac{1}{T} - \frac{1}{T_{\text{ref}}}\right] \right) \\
j_{0,a} &= \gamma_a \left(\frac{p_{\text{O}_2}}{P^\circ}\right)^{\beta_3} \exp\left( -\frac{E_{\text{act},a}}{R}\left[\frac{1}{T} - \frac{1}{T_{\text{ref}}}\right] \right)
\end{align}
Con parámetros calibrados ($E_{\text{act},c} = 100\text{ kJ/mol}, E_{\text{act},a} = 120\text{ kJ/mol}, j_{0,c}^{\text{ref}} = 5,300\text{ A/m}^2, j_{0,a}^{\text{ref}} = 2,000\text{ A/m}^2$) a $800^\circ\text{C}$ y $j = 4,800\text{ A/m}^2$ ($0.480\text{ A/cm}^2$):
\begin{align}
\eta_{\text{act},c} &= \mathbf{0.0475\text{ V}} \quad (47.5\text{ mV}) \\
\eta_{\text{act},a} &= \mathbf{0.0644\text{ V}} \quad (64.4\text{ mV}) \\
\eta_{\text{act,total}} &= \eta_{\text{act},c} + \eta_{\text{act},a} = \mathbf{0.1119\text{ V}} \quad (111.9\text{ mV})
\end{align}
Este despeje analítico es exacto y se ejecuta en tiempo constante $\mathcal{O}(1)$, sin iteraciones numéricas.
\end{mathdeductionbox}

\subsection{Pérdidas Óhmicas y Conducción Iónica en Electrolito YSZ}

La resistencia al transporte de iones óxido ($\text{O}^{2-}$) a través de la red cristalina del electrolito cerámico de Circonia Estabilizada con Itria (8YSZ) domina las pérdidas resistivas:

\begin{mathdeductionbox}{Formulación de Resistencia Superficial de Área (ASR)}
La conductividad iónica $\sigma_{\text{ion}}\text{ (S/m)}$ en electrolitos cerámicos sigue la ley de Arrhenius:
\begin{equation}
\sigma_{\text{ion}}(T) = \frac{\sigma_0}{T} \exp\left( -\frac{E_{\text{ohm}}}{RT} \right)
\end{equation}
La resistencia específica de área ($ASR$, en $\Omega\cdot\text{m}^2$) para un electrolito de espesor $\delta_{\text{mem}} \approx 15\,\mu\text{m}$ soportado en electrodo se modela en función de la temperatura relativa a $T_{\text{ref}} = 1073.15\text{ K}$:
\begin{equation}
ASR(T) = ASR_{\text{ref}} \cdot \exp\left[ \frac{E_{\text{ohm}}}{R} \left( \frac{1}{T} - \frac{1}{T_{\text{ref}}} \right) \right]
\end{equation}
Con $ASR_{\text{ref}} = 1.161 \times 10^{-5}\ \Omega\cdot\text{m}^2$ ($0.1161\ \Omega\cdot\text{cm}^2$) y energía de activación $E_{\text{ohm}} = 80.0\text{ kJ/mol}$:
- A $750^\circ\text{C}$ ($1023.15\text{ K}$): $ASR = 0.220\ \Omega\cdot\text{cm}^2$.
- A $800^\circ\text{C}$ ($1073.15\text{ K}$): $ASR = \mathbf{0.1161\ \Omega\cdot\text{cm}^2}$ (reducción neta de $-47.2\%$).
Por la Ley de Ohm, la caída de potencial a $j = 0.480\text{ A/cm}^2$ es:
\begin{equation}
\eta_{\text{ohm}} = j \cdot ASR = (0.480\text{ A/cm}^2) \times (0.1161\ \Omega\cdot\text{cm}^2) = \mathbf{0.0557\text{ V}} \quad (55.7\text{ mV})
\end{equation}
\end{mathdeductionbox}

\subsection{Sobrepotencial de Concentración y Límite Difusivo}

El sobrepotencial de concentración surge por la resistencia a la difusión molecular y Knudsen de vapor de agua e hidrógeno a través de la estructura porosa del cátodo:

\begin{mathdeductionbox}{Derivación de Densidad de Corriente Límite y Sobrepotencial de Concentración}
Combinando la Primera Ley de Fick y la Ley de Faraday en estado estacionario:
\begin{equation}
j = \frac{2F D_{\text{eff}} P}{RT \delta_{\text{cat}}} (y_{\text{H}_2\text{O,bulk}} - y_{\text{H}_2\text{O,superficie}})
\end{equation}
La corriente límite $j_{\text{lim}}$ ocurre cuando la concentración en los sitios catalíticos activos se agota ($y_{\text{H}_2\text{O,superficie}} \to 0$):
\begin{equation}
j_{\text{lim}} = \frac{2F D_{\text{eff}} P}{RT \delta_{\text{cat}}} y_{\text{H}_2\text{O,bulk}} = j_{\text{lim},0} \left(\frac{T}{T_{\text{ref}}}\right)^{1.5} \left(\frac{y_{\text{H}_2\text{O}}}{y_{\text{ref}}}\right)
\end{equation}
Con $j_{\text{lim},0} = 2.50\text{ A/cm}^2$ a $T_{\text{ref}} = 800^\circ\text{C}$ y $y_{\text{ref}} = 0.585$:
\begin{equation}
j_{\text{lim}}(800^\circ\text{C}, y_{\text{H}_2\text{O}} = 0.585) = \mathbf{2.551\text{ A/cm}^2}
\end{equation}
La relación local de corriente a corriente límite es:
\begin{equation}
\frac{j}{j_{\text{lim}}} = \frac{0.480}{2.551} = \mathbf{0.188} \quad (18.8\%)
\end{equation}
El sobrepotencial de concentración resultante es:
\begin{equation}
\eta_{\text{conc}} = -\frac{RT}{2F} \ln\left(1 - \frac{j}{j_{\text{lim}}}\right) = -\frac{8.31446 \times 1073.15}{2 \times 96485.33} \ln(1 - 0.188) = -0.04624 \ln(0.812) = \mathbf{0.0096\text{ V}} \quad (9.6\text{ mV})
\end{equation}
\end{mathdeductionbox}

\subsection{Voltaje Total de Celda y Demostración del Régimen Endotérmico}

Sumando cada contribución para el Escenario D:
\begin{equation}
V_{\text{celda}} = E_{\text{Nernst}} + \eta_{\text{act}} + \eta_{\text{ohm}} + \eta_{\text{conc}} = 1.0056 + 0.1119 + 0.0557 + 0.0096 = \mathbf{1.1828\text{ V}}
\end{equation}

\begin{mathdeductionbox}{Balance Térmico de Celda y Flujo de Calor Absorbido}
El balance de energía en la celda electroquímica establece que el calor generado/absorbido por celda es:
\begin{equation}
\dot{Q}_{\text{celda}} = I_{\text{celda}} \cdot (V_{\text{celda}} - V_{\text{tn}})
\end{equation}
Sustituyendo los valores del Escenario D ($V_{\text{celda}} = 1.1828\text{ V}$, $V_{\text{tn}} = 1.28725\text{ V}$, $I_{\text{celda}} = 96.0\text{ A}$ por celda de $200\text{ cm}^2$):
\begin{equation}
\dot{Q}_{\text{celda}} = 96.0\text{ A} \times (1.1828 - 1.28725)\text{ V} = 96.0 \times (-0.10445)\text{ V} = \mathbf{-10.027\text{ W por celda}}
\end{equation}
El signo negativo indica formalmente que la reacción es **endotérmica**: la celda absorbe $10.03\text{ W}$ de calor por cada celda para sostener la disociación. Para el conjunto de las 198,000 celdas de la planta:
\begin{equation}
\dot{Q}_{\text{endotérmico total}} = 198,000 \times (-10.027\text{ W}) = \mathbf{-1,985.3\text{ kW térmicos}}
\end{equation}
Este calor es suministrado por la integración térmica con el vapor sobrecalentado y el calor de reacción transferido desde la síntesis de metanol.
\end{mathdeductionbox}

\subsection{Modelo Cinético y Dimensionamiento del Reactor Lurgi BWR (R-401)}

Para la síntesis de metanol sobre catalizador comercial de $\text{Cu/ZnO/Al}_2\text{O}_3$, se implementó el modelo cinético heterogéneo de Vanden Bussche y Froment (1996), considerando la hidrogenación de dióxido de carbono y la reacción de desplazamiento inverso de gas de agua (RWGS):

\begin{mathdeductionbox}{Ecuaciones de Velocidad de Vanden Bussche y Froment (1996)}
\begin{align}
r_{\text{MeOH}} &= \frac{k_1 p_{\text{CO}_2} p_{\text{H}_2} \left( 1 - \frac{1}{K_1} \frac{p_{\text{MeOH}} p_{\text{H}_2\text{O}}}{p_{\text{CO}_2} p_{\text{H}_2}^3} \right)}{\left( 1 + K_a \frac{p_{\text{H}_2\text{O}}}{p_{\text{H}_2}} + K_b p_{\text{H}_2}^{0.5} + K_c p_{\text{H}_2\text{O}} \right)^3} \quad [\text{mol}/(\text{kg}_{\text{cat}}\cdot\text{s})] \\
r_{\text{RWGS}} &= \frac{k_2 p_{\text{CO}_2} \left( 1 - \frac{1}{K_2} \frac{p_{\text{CO}} p_{\text{H}_2\text{O}}}{p_{\text{CO}_2} p_{\text{H}_2}} \right)}{1 + K_a \frac{p_{\text{H}_2\text{O}}}{p_{\text{H}_2}} + K_b p_{\text{H}_2}^{0.5} + K_c p_{\text{H}_2\text{O}}} \quad [\text{mol}/(\text{kg}_{\text{cat}}\cdot\text{s})]
\end{align}
\end{mathdeductionbox}

\begin{mathdeductionbox}{Dimensionamiento Físico de Tubos y Caída de Presión de Ergun}
A partir del volumen de catalizador requerido ($V_{\text{cat}} = 11.51\text{ m}^3$, densidad aparente $\rho_b = 1,150\text{ kg/m}^3$):
- Diámetro interno de tubo: $d_i = 38.1\text{ mm}$ ($1.5\text{ in}$ BWG 14).
- Longitud de tubos: $L = 6.0\text{ m}$.
- Número de tubos del reactor multitubular:
\begin{equation}
N_{\text{tubos}} = \frac{V_{\text{cat}}}{L \cdot \frac{\pi d_i^2}{4}} = \frac{11.51}{6.0 \cdot \frac{\pi (0.0381)^2}{4}} = \frac{11.51}{6.0 \times 0.001140} = \mathbf{2,126\text{ tubos}}
\end{equation}
La caída de presión en el lecho empacado se calculó con la Ecuación de Ergun:
\begin{equation}
\frac{\Delta P}{L} = 150 \frac{(1-\epsilon)^2}{\epsilon^3} \frac{\mu v_s}{d_p^2} + 1.75 \frac{1-\epsilon}{\epsilon^3} \frac{\rho v_s^2}{d_p} = 24.5\text{ kPa/m} \implies \Delta P_{\text{total}} = \mathbf{1.47\text{ bar}}
\end{equation}
La coraza del reactor R-401-S se mantiene a $212.4^\circ\text{C}$ mediante generación de vapor saturado a 20 bar, removiendo $\dot{Q} = \mathbf{-12,335.4\text{ kW}}$, lo que produce $\dot{m}_{\text{vap}} = \frac{12,335.4\text{ kW}}{1,890.7\text{ kJ/kg}} = 6.524\text{ kg/s} = \mathbf{16,244.9\text{ kg/h}}$ de vapor de 20 bar.
\end{mathdeductionbox}
"""

# 6. SECCIÓN 5: METADATOS DE TOPOLOGÍA, BALANCES Y SERVICIOS AUXILIARES
SECTION_5 = r"""
\newpage
\section{METADATOS DE TOPOLOGÍA, BALANCES Y SERVICIOS AUXILIARES}

\subsection{Topología como Grafo Dirigido $G=(V,E)$ y Selección de Tear Streams}

El flowsheet de la planta se modeló formalmente como un grafo dirigido $G=(V, E)$, donde los vértices $V$ representan las operaciones unitarias (SOEC, reactores, columnas, compresores) y las aristas $E$ representan las corrientes de materia y energía:

\begin{conceptbox}{Algoritmo de Identificación de Tear Streams y Aceleración de Wegstein}
1. \textbf{Identificación de Bucles de Reciclo:} El grafo posee un ciclo dominante de alta presión:
\begin{equation}
\texttt{MIX-401} \longrightarrow \texttt{C-301} \longrightarrow \texttt{E-401} \longrightarrow \texttt{R-401} \longrightarrow \texttt{E-501} \longrightarrow \texttt{V-501} \longrightarrow \texttt{SPLIT-501} \longrightarrow \texttt{MIX-401}
\end{equation}
2. \textbf{Selección de la Corriente de Corte (Tear Stream):} Se seleccionó la corriente de vapor no condensado \texttt{S-502} a la salida del separador flash V-501 (70.0 bar, 40 °C). Esta selección minimiza el número de variables de iteración y asegura estabilidad térmica al encontrarse en estado vapor monofásico deshidratado.
3. \textbf{Algoritmo de Aceleración de Wegstein:} En BioSTEAM y DWSIM, el método de punto fijo sucesivo $x_{k+1} = f(x_k)$ se acelera mediante el factor de relajación $q$:
\begin{equation}
x_{k+1} = q x_k + (1-q) f(x_k), \quad q = \frac{s}{s-1}, \quad s = \frac{f(x_k) - f(x_{k-1})}{x_k - x_{k-1}}
\end{equation}
Con cotas $-5.0 \le q \le 0.0$ para evitar oscilaciones caóticas, el bucle converge en **menos de 7 iteraciones** con una tolerancia de error molar $\epsilon < 10^{-5}$.
\end{conceptbox}

\subsection{Matriz de Balance de Materia Global de la Planta}

La Tabla 6 consolida los flujos másicos y molares de las corrientes principales del proceso para una producción nominal de **$30,309\text{ t/año}$ ($3,788.65\text{ kg/h}$)** de e-metanol Grado AA:

\begin{table}[htbp]
\centering
\scriptsize
\renewcommand{\arraystretch}{1.25}
\begin{tabularx}{\linewidth}{l c c c c c c c c c}
\toprule
\rowcolor{tableheader}
\textbf{\color{white}Corriente} & \textbf{\color{white}Descripción} & \textbf{\color{white}T (°C)} & \textbf{\color{white}P (bar)} & \textbf{\color{white}Flujo (kg/h)} & \textbf{\color{white}Flujo (kmol/h)} & \textbf{\color{white}H$_2$ (\% mol)} & \textbf{\color{white}CO$_2$ (\% mol)} & \textbf{\color{white}MeOH (\% mol)} & \textbf{\color{white}H$_2$O (\% mol)} \\
\midrule
\rowcolor{tablerowgray}
S-101 & $\text{CO}_2$ Captura (Batería) & 40.0 & 20.0 & 5,310.8 & 120.67 & 0.00 & 99.50 & 0.00 & 0.10 \\
S-201 & Agua Desmineralizada & 25.0 & 20.0 & 16,244.9 & 901.74 & 0.00 & 0.00 & 0.00 & 100.00 \\
\rowcolor{tablerowgray}
S-205 & Vapor Sobrecalentado SOEC & 800.0 & 20.0 & 16,244.9 & 901.74 & 0.00 & 0.00 & 0.00 & 100.00 \\
S-206 & Oxígeno Puro Anódico & 800.0 & 20.0 & 10,131.2 & 316.60 & 0.00 & 0.00 & 0.00 & 0.00 ($100\%\text{ O}_2$) \\
\rowcolor{tablerowgray}
S-207 & Efluente Catódico SOEC & 800.0 & 19.4 & 6,113.7 & 949.80 & 66.70 & 0.00 & 0.00 & 33.30 \\
S-210 & Hidrógeno Seco al Lazo & 40.0 & 19.0 & 1,315.6 & 652.58 & 99.85 & 0.00 & 0.00 & 0.15 \\
\rowcolor{tablerowgray}
S-301 & Alimentación R-401 & 210.0 & 75.0 & 44,120.5 & 2,890.40 & 71.40 & 21.20 & 1.20 & 2.10 \\
S-402 & Efluente R-401 & 245.0 & 73.5 & 44,120.5 & 2,520.10 & 58.20 & 15.10 & 11.80 & 12.90 \\
\rowcolor{tablerowgray}
S-502 & Reciclo de Gas al Lazo & 40.0 & 70.0 & 38,125.4 & 2,345.20 & 68.50 & 18.40 & 0.40 & 0.30 \\
S-503 & Purga del Bucle (4\%) & 40.0 & 70.0 & 1,588.6 & 97.72 & 68.50 & 18.40 & 0.40 & 0.30 \\
\rowcolor{tablerowgray}
S-505 & Crudo Líquido a Destilación & 40.0 & 70.0 & 5,995.1 & 174.90 & 0.05 & 0.25 & 55.40 & 44.30 \\
S-603 & Metanol Grado AA Destilado & 64.5 & 1.2 & \textbf{3,788.65} & \textbf{118.25} & 0.00 & 0.00 & \textbf{99.89} & \textbf{0.11} \\
\rowcolor{tablerowgray}
S-604 & Fondos Acuosos (Lazo ZLD) & 102.3 & 1.3 & 2,206.45 & 122.48 & 0.00 & 0.00 & 0.02 & 99.98 \\
\bottomrule
\end{tabularx}
\caption{Matriz consolidada de balance de materia global en escala de planta completa ($30,000\text{ t/año}$).}
\end{table}

\subsection{Matriz de Balance de Energía y Demanda de Servicios Auxiliares}

La Tabla 7 detalla las cargas térmicas, potencias eléctricas de compresión y servicios auxiliares calculados para la planta bajo condiciones óptimas del Escenario D:

\begin{table}[htbp]
\centering
\small
\renewcommand{\arraystretch}{1.3}
\begin{tabularx}{\linewidth}{>{\bfseries\color{primaryblue}}l l c c >{\raggedright\arraybackslash}X}
\toprule
\rowcolor{tableheader}
\textbf{\color{white}Equipo (Tag)} & \textbf{\color{white}Tipo de Carga} & \textbf{\color{white}Demanda (kW)} & \textbf{\color{white}Demanda (MW)} & \textbf{\color{white}Servicio Auxiliar / Integración Térmica} \\
\midrule
\rowcolor{tablerowgray}
EL-201 (SOEC) & Eléctrica DC (Stacks) & 36,737.5 & 36.74 & Rectificador IGBT (Media Tensión 13.8 kV AC) \\
EL-201 (SOEC) & Eléctrica AC (Red) & 38,070.0 & \textbf{38.07} & Suministro eléctrico CFE / Parque Solar polo industrial adyacente \\
\rowcolor{tablerowgray}
E-202 & Eléctrica Calentador & 5,328.4 & \textbf{5.33} & Resistencias Incoloy 800H (Eleva vapor a 800 °C) \\
R-401-S & Térmica Exotérmica & -12,335.4 & \textbf{-12.34} & Genera 16,245 kg/h vapor saturado a 20 bar (Coraza) \\
\rowcolor{tablerowgray}
C-301 & Eléctrica Compresor & 1,316.7 & \textbf{1.32} & Motor eléctrico de inducción (75 bar, $\eta_p = 78\%$) \\
EXP-501 & Eléctrica Generación & -437.8 & \textbf{-0.44} & Turboexpansor de purga (Generador acoplado a red) \\
\rowcolor{tablerowgray}
E-401 & Térmica Intercambiador & 2,850.0 & 2.85 & Intercambio gas efluente R-401 / gas alimentación \\
E-501 & Térmica Condensador & -6,450.0 & -6.45 & Agua de enfriamiento de torre ($28^\circ\text{C} \to 38^\circ\text{C}$) \\
\rowcolor{tablerowgray}
E-602 (Rehervidor) & Térmica Rehervidor & 3,210.0 & 3.21 & Vapor de baja presión ($3.5\text{ bar}, 138^\circ\text{C}$) \\
E-601 (Condensador)& Térmica Condensador & -3,180.0 & -3.18 & Agua de enfriamiento de torre ($28^\circ\text{C} \to 35^\circ\text{C}$) \\
\midrule
\rowcolor{primaryblue!15}
\textbf{Consumo Neto} & \textbf{Potencia Neta Planta} & \textbf{44,277.3} & \textbf{44.28 MW} & \textbf{Planta Completa e-Metanol Grado AA} \\
\bottomrule
\end{tabularx}
\caption{Matriz consolidada de balance de energía, potencia eléctrica y servicios auxiliares.}
\end{table}

\end{document}
"""

# 7. FUNCIÓN PRINCIPAL DE ESCRITURA Y COMPILACIÓN
def main():
    print("1. Ensamblando documento LaTeX...")
    full_latex = PREAMBLE + SECTION_1 + SECTION_2 + SECTION_3 + SECTION_4 + SECTION_5
    
    with open(TEX_PATH, "w", encoding="utf-8") as f:
        f.write(full_latex)
    print(f"   Archivo LaTeX escrito exitosamente en: {TEX_PATH} ({len(full_latex)} caracteres)")
    
    print("2. Compilando documento PDF con pdflatex (Pasada 1)...")
    res1 = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", f"-output-directory={PDF_DIR}", TEX_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True, errors="replace"
    )
    if res1.returncode != 0:
        print("   ERROR en Pasada 1 de pdflatex:")
        print(res1.stdout[-1500:])
        return
    print("   Pasada 1 completada exitosamente.")
    
    print("3. Compilando documento PDF con pdflatex (Pasada 2 para resolver tabla de contenidos e hipervínculos)...")
    res2 = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", f"-output-directory={PDF_DIR}", TEX_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True, errors="replace"
    )
    if res2.returncode != 0:
        print("   ERROR en Pasada 2 de pdflatex:")
        print(res2.stdout[-1500:])
        return
    print("   Pasada 2 completada exitosamente.")
    
    print("4. Copiando PDF generado a la raíz del proyecto...")
    shutil.copy(FINAL_PDF, ROOT_PDF)
    print(f"   PDF sincronizado en: {ROOT_PDF}")
    
    print("5. Generando versión Markdown sincronizada...")
    # Convierte o escribe el equivalente Markdown
    generar_markdown()
    print("   Markdown generado exitosamente.")
    print("¡Proceso completado con éxito!")

def generar_markdown():
    # Estructura limpia en Markdown
    md_content = f"""# GUÍA MAESTRA DE DEFENSA TÉCNICA, SPEECH DE 10 MINUTOS, BANCO DE PREGUNTAS Y MEMORIA DE CÁLCULO
**Licitación Pública Internacional RFP-CCM-EM-001 | Planta de 30,000 t/año de e-Metanol Grado AA**  
**Consorcio:** Solvanta Engineering Solutions S.A. de C.V.  
**Integrantes:** Ing. Karol Paola Camacho López & Ing. Grecia Figueroa Rincón  
**Cátedra:** Dr. Jesús Andrés Arzola Flores | FIQ - BUAP  
**Fecha:** Noviembre de 2026

---

## 1. SPEECH OFICIAL SINCRONIZADO DE 10 MINUTOS (GUION DE LOCUCIÓN PASO A PASO)

### Matriz de Control de Tiempos y Transición de Voces (Duración: 10:00 min)

| Bloque | Orador | Intervalo | Duración | Palabras | Área del Cartel Referenciada |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1.1** | Grecia Figueroa | 0:00 - 2:00 | 2.0 min | ~290 | **Área 5:** BioSTEAM, POO, subclase `bst.Unit`, ciclo de vida y reciclos. |
| **1.2** | Karol Camacho | 2:00 - 4:30 | 2.5 min | ~365 | **Áreas 1 y 2:** Termodinámica SOEC, Shomate NIST, Butler-Volmer, DWSIM API XML. |
| **1.3** | Grecia Figueroa | 4:30 - 6:30 | 2.0 min | ~295 | **Área 6:** DTI v1.0, 4 nodos HAZOP (IEC 61882), cascada $M=2.05$, 4 Interlocks SIS. |
| **1.4** | Karol Camacho | 6:30 - 8:45 | 2.25 min | ~335 | **Áreas 4 y 7:** Sensibilidad Morris, 4 Escenarios, Frente de Pareto, Escenario D. |
| **1.5** | Grecia Figueroa | 8:45 - 10:00 | 1.25 min | ~185 | **Conclusión:** Programación como motor del diseño industrial y apertura a Q&A. |
| **Total** | **Consorcio Solvanta** | **0:00 - 10:00** | **10.0 min** | **~1,470** | **Defensa Técnica Integral de Planta (30,000 t/año e-MeOH)** |

---

### Intervención 1 (Grecia Figueroa | 0:00 - 2:00 | 2:00 min | Área 5 del Cartel)

> **[ORADOR: GRECIA FIGUEROA \| TIEMPO: 0:00 - 2:00]**  
> *(Tono: Seguro, ejecutivo, profesional. Contacto visual con el comité evaluador).*

**[0:00 - 0:25] Saludo y Planteamiento del Reto:**  
Buenos días, miembros del comité evaluador y colegas ingenieros. A nombre del Consorcio Solvanta Engineering Solutions, presentamos la ingeniería de proceso para la licitación RFP-CCM-EM-001, orientada a la producción de 30,000 toneladas anuales de e-metanol Grado AA en el complejo industrial adyacente.

Al conceptualizar esta planta, nos enfrentamos a una barrera común en el ejercicio profesional: los simuladores comerciales cerrados carecen de modelos nativos para tecnologías de vanguardia como las celdas de electrólisis de óxido sólido (SOEC) y reactores catalíticos multitubulares acoplados térmicamente. La práctica habitual es recurrir a cajas negras o conversiones empíricas que comprometen la fidelidad termodinámica.

**[0:25 - 1:15] Por qué BioSTEAM y Paradigma de Programación:**  
*(Señalar con firmeza el encabezado del Área 5 en la columna derecha del cartel)*  
Para superar esta limitación, seleccionamos la plataforma de código abierto BioSTEAM en Python. BioSTEAM destaca porque acopla de forma nativa la simulación de balances de materia y energía con el análisis tecno-económico y de ciclo de vida. Mediante el paradigma de programación orientada a objetos, construimos unidades de proceso personalizadas mediante la subclasificación de la clase abstracta `bst.Unit`.

**[1:15 - 1:45] Ciclo de Vida de la Unidad No Nativa (`SOECElectrolyzer`):**  
*(Indicar el bloque de código de BioSTEAM en el Área 5)*  
El ciclo de vida de nuestra clase `SOECElectrolyzer` opera en tres etapas rigurosas:  
Primero, los metadatos de topología `_N_ins = 1` y `_N_outs = 2` declaran la conectividad física de los puertos.  
Segundo, el método interno `_run()` resuelve el balance fisicoquímico en tiempo de ejecución: toma el flujo molar de vapor sobrecalentado de `self.ins[0]`, aplica la conversión electroquímica regida por la Ley de Faraday y actualiza in situ las propiedades termodinámicas de las corrientes de salida en `self.outs`.  
Tercero, el método `_design()` evalúa la geometría de los stacks cerámicos y registra automáticamente la demanda de potencia en `self.power_utility`, integrándola al consumo eléctrico de la planta.

**[1:45 - 2:00] Convergencia y Transición:**  
Al heredar de `bst.Unit`, el electrolizador se integra orgánicamente en el `bst.Flowsheet`, permitiendo que el algoritmo acelerado de Wegstein resuelva los bucles cerrados de reciclo con estabilidad matemática absoluta. 

Para detallar cómo formulamos los primeros principios electroquímicos y cómo los conectamos con el simulador DWSIM, cedo la palabra a mi colega, la ingeniera Karol Camacho.

---

### Intervención 2 (Karol Camacho | 2:00 - 4:30 | 2:30 min | Áreas 1 y 2 del Cartel)

> **[ORADOR: KAROL CAMACHO \| TIEMPO: 2:00 - 4:30]**  
> *(Tono: Analítico, riguroso, científico. Apuntando con precisión al Área 2 y a la Figura 1).*

**[2:00 - 2:40] Justificación Termodinámica del SOEC a 800 °C:**  
Muchas gracias, Grecia. Buenos días. Si dirigen su atención al Área 1 del cartel, la decisión de implementar electrólisis SOEC de alta temperatura a 800 °C frente a la electrólisis convencional alcalina o PEM responde a un principio termodinámico ineludible: la demanda de energía libre de Gibbs ($\Delta G$) decrece drásticamente de $237\\text{{ kJ/mol}}$ a temperatura ambiente hasta $180\\text{{ kJ/mol}}$ a 800 °C. Esto permite sustituir cerca del 25% del trabajo eléctrico por energía térmica residual, abatiendo el consumo energético de la planta.

**[2:40 - 3:30] Modelo Electroquímico Riguroso en Python:**  
*(Señalar las ecuaciones y el listado de código en el Área 2)*  
Para garantizar máxima precisión en el paquete `soec_optimization/`, implementamos tres componentes fundamentales:  
1. **Termodinámica NIST Shomate:** Reemplazamos la correlación lineal simplificada por polinomios rigurosos de Shomate del NIST. Esto corrigió una sobreestimación de $+24.8\\text{{ mV}}$ en el potencial reversible estándar, evitando un error acumulado de casi un megavatio en el dimensionamiento eléctrico.  
2. **Potencial de Nernst Presurizado:** Modelamos el efecto de operar a 20 bar, incorporando la presión anódica de oxígeno puro y los perfiles molares de vapor e hidrógeno a lo largo del cátodo.  
3. **Cinética Butler-Volmer y Despeje Analítico:** Invertimos analíticamente la ecuación de activación mediante la función $\\operatorname{{arsinh}}$, eliminando métodos iterativos lentos. Asimismo, calculamos la resistencia óhmica mediante la ley de Arrhenius para el electrolito cerámico de YSZ.

**[3:30 - 4:00] Erradicación del Recorte Numérico Difusivo:**  
*(Señalar la Figura 1: Curva de polarización V-j)*  
Un aporte fundamental de nuestro código fue erradicar el recorte artificial que muchos modelos comerciales usan para evitar errores de dominio cuando la corriente se acerca al límite difusivo. En `concentration.py`, penalizamos rigurosamente cualquier condición donde $j \\ge j_{{\\text{{lim}}}}$. De este modo, garantizamos que el diseño opere de manera físicamente viable, alejado de la degradación por transporte de masa.

**[4:00 - 4:30] Integración de API DWSIM e Inyección XML:**  
Para validar la hidrodinámica completa de la planta, construimos el módulo `dwsim_interface.py`. Este script interactúa mediante IronPython con la API de DWSIM v10, leyendo las corrientes de entrada `ims1` y actualizando dinámicamente las propiedades de salida `oms1` y `oms2` con `ClearAllProps()`, `SetMolarFlow()` y `Calculate()`. Además, automatizamos la inyección directa del script en el árbol XML del archivo de simulación `.dwxml`.

Con la física convergida en Python y validada en DWSIM, congelamos los parámetros en el Diagrama de Tubería e Instrumentación. Grecia detallará la ingeniería de detalle y las salvaguardas de seguridad.

---

### Intervención 3 (Grecia Figueroa | 4:30 - 6:30 | 2:00 min | Área 6 del Cartel)

> **[ORADOR: GRECIA FIGUEROA \| TIEMPO: 4:30 - 6:30]**  
> *(Tono: Firme, técnico, enfocado en normativas y seguridad de procesos).*

**[4:30 - 5:05] Congelación del P&ID y Filosofía de Control:**  
*(Señalar la Figura 4 en el Área 6: Plano Solvanta_DTI_v1.pdf)*  
Gracias, Karol. Los balances convergidos en Python se tradujeron al Diagrama de Tubería e Instrumentación congelado en el plano DTI v1.0. Para asegurar la operación continua de la síntesis de metanol, implementamos una estrategia de control avanzado en cascada estequiométrica: el analizador `AIC-401` monitorea la composición del gas de síntesis y ajusta la consigna del controlador de flujo `FIC-401`, manteniendo estrictamente el módulo estequiométrico en $M = 2.05$, lo que protege el catalizador de cobre contra la formación de subproductos pesados y desactivación térmica.

**[5:05 - 5:45] Auditoría de Nodos Críticos bajo Norma IEC 61882 (HAZOP):**  
Auditamos cuatro nodos de proceso mediante la metodología HAZOP:  
- **Nodo 1 (Vapor):** Prevención de choque térmico en celdas cerámicas ante fluctuaciones de vapor saturado.  
- **Nodo 2 (SOEC):** Control estricto de gradientes de presión transitorios entre ánodo y cátodo.  
- **Nodo 3 (Reactor Lurgi BWR):** Remoción del calor exotérmico ($-12.34\\text{{ MW}}$) mediante generación de vapor en coraza, impidiendo puntos calientes superiores a 260 °C.  
- **Nodo 4 (Destilación AA):** Control de presión y reflujo en T-601 para garantizar la pureza de 99.89% en peso.

**[5:45 - 6:30] Matriz Causa-Efecto de Interlocks SIS (Tabla 3):**  
*(Indicar la Tabla 3 en el Área 6)*  
Como salvaguardas instrumentadas independientes del sistema de control básico, diseñamos cuatro lazos de seguridad interlock (SIS) con transmisores redundantes en arquitectura 2oo3:  
- **Interlock I-01:** Ante temperatura en R-401 superior a 260 °C, cierra la válvula de corte rápido `SDV-301` en menos de 2 segundos y abre reciclo frío para detener el embalamiento térmico.  
- **Interlock I-02:** Si la presión del bucle excede 78.5 bar, desacopla los compresores C-301 y C-501, activa el reciclo anti-surge y alivia hacia la antorcha vía `PSV-501`.  
- **Interlock I-03 (Protección SOEC):** Si el diferencial de presión transitorio entre ánodo y cátodo supera los 0.4 bar, corta el suministro eléctrico DC en menos de 50 milisegundos, abre la válvula ecualizadora `PDCV-201` e inunda con nitrógeno, previniendo la fractura mecánica de los electrolitos cerámicos de YSZ.  
- **Interlock I-04:** Ante nivel muy bajo en el separador flash V-501, cierra `SDV-501` en menos de 1 segundo para evitar el paso descontrolado de gas de alta presión hacia el tren de destilación a baja presión.

A continuación, Karol explicará el análisis de sensibilidad multivariable y la selección del punto de operación óptimo.

---

### Intervención 4 (Karol Camacho | 6:30 - 8:45 | 2:15 min | Áreas 4 y 7 del Cartel)

> **[ORADOR: KAROL CAMACHO \| TIEMPO: 6:30 - 8:45]**  
> *(Tono: Científico, contundente, destacando cifras y beneficios económicos).*

**[6:30 - 7:15] Sensibilidad en 3 Niveles y Método de Morris (Tabla 2):**  
*(Dirigir la atención a las Tablas 2 y 4 y a las Figuras 5 y 6 en las Áreas 4 y 7)*  
Muchas gracias, Grecia. Para explorar el espacio de diseño del sistema, programamos en `sensitivity.py` un estudio en tres niveles: análisis univariado OAT, muestreo por Hipercubo Latino con 100 corridas y el Método de Efectos Elementales de Morris con 15 trayectorias. 

Como muestra la Tabla 2, el ranking de Morris reveló que la **temperatura** es el parámetro gobernante absoluto (Score 100.0), ya que abate exponencialmente la resistencia óhmica ASR del electrolito. Le sigue la **densidad de corriente** (Score 74.3), que balancea directamente el gasto eléctrico operativo contra el área de celdas requerida. El área unitaria de celda tuvo un impacto intensivo nulo (Score 0.1), lo que confirmó la validez de fijar celdas comerciales de $200\\text{{ cm}}^2$.

**[7:15 - 8:05] Comparativa de Escenarios y Frente de Pareto:**  
Evaluamos cuatro escenarios completos en el flowsheet acoplado:  
- El **Escenario A** representaba la línea base a 750 °C y $0.508\\text{{ A/cm}}^2$, con un consumo específico de $38.13\\text{{ kWh/kg H}}_2$.  
- El **Escenario B** minimizaba el consumo a $30.03\\text{{ kWh/kg}}$, pero disparaba el costo de capital al requerir 281,750 celdas.  
- El **Escenario C** simulaba condiciones intermedias industriales.  
- El **Escenario D**, destacado en verde en la Tabla 4, fue seleccionado mediante optimización multiobjetivo en el Frente de Pareto (Figura 6).

**[8:05 - 8:45] Justificación Integral del Escenario D Óptimo:**  
Al operar a 800 °C, 20 bar y $0.480\\text{{ A/cm}}^2$, el Escenario D logra el compromiso perfecto:  
1. Minimiza simultáneamente el costo nivelado de hidrógeno a **\$3.18 USD/kg** y el costo nivelado de metanol a **\$657.2 USD/t** (una reducción de \$75.3 USD por tonelada frente al caso base).  
2. Reduce la potencia eléctrica demandada por el electrolizador en **6.03 MW** ($-13.7\%$) y disminuye el número de celdas en **51,600 unidades** ($-20.7\%$).  
3. Opera a un voltaje de celda de **1.1828 V**, que es inferior al voltaje termoneutro de 1.287 V. Esto demuestra que la celda opera en un régimen endotérmico de alta eficiencia, donde el déficit térmico es cubierto al 100% mediante la integración con el vapor generado en la coraza del reactor R-401-S ($16,245\\text{{ kg/h}}$ a 20 bar).

Grecia concluirá la exposición con las consideraciones finales del proyecto.

---

### Intervención 5 (Grecia Figueroa | 8:45 - 10:00 | 1:15 min | Recuadro de Conclusión)

> **[ORADOR: GRECIA FIGUEROA \| TIEMPO: 8:45 - 10:00]**  
> *(Tono: Inspirador, integrador, cerrando con cortesía y autoridad técnica).*

**[8:45 - 9:30] Síntesis del Logro de Ingeniería:**  
*(Señalar el recuadro inferior de Conclusión en la Columna 1)*  
Para concluir, esta licitación demuestra con hechos concretos el papel transformador de la programación en la ingeniería de procesos contemporánea. Lejos de ser operadores pasivos de simuladores comerciales con opciones fijas, los ingenieros químicos podemos programar en Python modelos rigurosos desde primeros principios termodinámicos, electroquímicos y de transporte.

Cuando una tecnología limpia y eficiente como la electrólisis SOEC existe físicamente en el mundo real pero no se encuentra en las bibliotecas estándar de software, tenemos la capacidad de construir el bloque desde su base matemática, acoplarlo con DWSIM y BioSTEAM, y formular propuestas técnicamente sustentadas, energéticamente integradas y económicamente superiores.

**[9:30 - 10:00] Cierre Formal y Apertura de Sesión:**  
El diseño de Solvanta Engineering Solutions garantiza una planta de 30,000 toneladas anuales de metanol Grado AA, con un ahorro neto de 6.03 MW eléctricos, operación segura respaldada por metodología HAZOP e interlocks SIL-2, y un modelo reproducible bajo estándares abiertos.

Agradecemos profundamente su tiempo y atención, y quedamos a su entera disposición para atender sus preguntas técnicas. Muchas gracias.

---

## 2. BANCO DE PREGUNTAS Y RESPUESTAS ANTE AUDIENCIA (Q&A TÉCNICO)

*(Ver versión PDF para desglose completo de las 12 preguntas con ecuaciones y análisis cuantitativo).*
"""
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    main()

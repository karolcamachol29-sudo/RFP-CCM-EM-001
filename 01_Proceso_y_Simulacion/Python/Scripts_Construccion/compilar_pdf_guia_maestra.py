#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador LaTeX para la Guía Maestra de Defensa Técnica y Memoria de Ingeniería.
Consorcio Solvanta Engineering Solutions S.A. de C.V. | RFP-CCM-EM-001
"""

import os
import subprocess
import shutil
import sys

TEX_PATH = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.tex"
PDF_PATH = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf"

def build_latex_content():
    return r"""\documentclass[10pt,letterpaper]{article}

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
\fancyhead[R]{\small\color{darkslate}Guía de Defensa Técnica: Speech y Memoria de Ingeniería}
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
    
    {\fontsize{18}{22}\selectfont\bfseries\color{secondaryblue}GUÍA MAESTRA DE DEFENSA TÉCNICA, SPEECH OFICIAL Y MEMORIA RIGUROSA DE INGENIERÍA}\\[0.4cm]
    {\large\textbf{Simulación Avanzada, Programación en BioSTEAM/DWSIM, Optimización Multivariable SOEC y Análisis de Nodos/Seguridad en el DTI}}\\[0.4cm]
    \rule{0.6\linewidth}{0.8pt}\\[0.8cm]
    
    \begin{tcolorbox}[enhanced,colback=lightbg,colframe=primaryblue,boxrule=1.2pt,arc=4pt,width=0.92\linewidth]
        \centering
        \textbf{\color{primaryblue}FICHA TÉCNICA DEL PROYECTO Y EXPEDIENTE}\\[0.2cm]
        \begin{tabular}{rl}
            \textbf{Licitación Internacional:} & RFP-CCM-EM-001 (PEMEX / CFE / SENER) \\
            \textbf{Proyecto:} & Planta de Producción de e-Metanol Grado AA ($30,000\text{ t/año}$) \\
            \textbf{Ubicación:} & predio industrial asignado para el proyecto RFP-CCM-EM-001. \\
            \textbf{Tecnología de Hidrógeno:} & Electrólisis SOEC de Alta Temperatura ($800^\circ\text{C}, 20\text{ bar}$) \\
            \textbf{Tecnología de Síntesis:} & Reactor Lurgi Multitubular BWR ($75\text{ bar}$) acoplado a vapor SOEC \\
            \textbf{Purificación:} & Destilación Rigurosa Grado AA ($99.89\%\text{ wt}$) con Lazo ZLD \\
            \textbf{Expositores Técnicos:} & \textbf{Grecia Figueroa} (Procesos, BioSTEAM y Seguridad HAZOP) \\
            & \textbf{Karol Camacho} (Simulación DWSIM, SOEC y Optimización)
        \end{tabular}
    \end{tcolorbox}
    
    \vfill
    {\small\color{darkslate}\textbf{sitio industrial de referencia, México} \textbar\ Noviembre de 2026}
\end{titlepage}

\tableofcontents
\newpage

% ==============================================================================
% SECCIÓN 1: SPEECH OFICIAL SINCRONIZADO
% ==============================================================================
\section{SPEECH OFICIAL SINCRONIZADO (GUION DE LOCUCIÓN PASO A PASO)}

\subsection{Matriz de Control de Tiempos y Transición de Voces}

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\linewidth}{c c X c c}
\toprule
\rowcolor{tableheader}
\color{white}\textbf{Fase} & \color{white}\textbf{Orador} & \color{white}\textbf{Temática Central} & \color{white}\textbf{Duración} & \color{white}\textbf{Ventana} \\
\midrule
\rowcolor{tablerowgray}
\textbf{P1} & \textbf{Grecia Figueroa} & Apertura, BioSTEAM y POO para Equipos Ausentes & 1 min 15 s & 0:00 -- 1:15 \\
\textbf{P2} & \textbf{Karol Camacho} & SOEC, Primeros Principios, Endotermicidad y DWSIM & 1 min 30 s & 1:15 -- 2:45 \\
\rowcolor{tablerowgray}
\textbf{P3} & \textbf{Grecia Figueroa} & Nodos DTI, Filosofía de Control, HAZOP y SIL & 1 min 30 s & 2:45 -- 4:15 \\
\textbf{P4} & \textbf{Karol Camacho} & Escenarios SOEC (A, B, C, D) y Selección Óptima & 1 min 30 s & 4:15 -- 5:45 \\
\rowcolor{tablerowgray}
\textbf{P5} & \textbf{Grecia Figueroa} & Conclusión Final: La Programación en Ingeniería & 0 min 45 s & 5:45 -- 6:30 \\
\bottomrule
\end{tabularx}
\caption{Cronograma maestro de exposición para la defensa técnica de licitación.}
\end{table}

\subsection{Intervención 1: BioSTEAM y Programación Orientada a Objetos}

\begin{speechgrecia}{0:00 -- 1:15 \textbar\ Tono: Seguro, profesional y riguroso}
«Buenos días, miembros del comité evaluador y colegas. Mi nombre es \textbf{Grecia Figueroa} y, junto con mi compañero \textbf{Karol Camacho}, representamos a \textbf{Solvanta Engineering Solutions S.A. de C.V.} Presentamos la defensa técnica de nuestra propuesta para la licitación internacional \textbf{RFP-CCM-EM-001}: el diseño, simulación, análisis de seguridad y evaluación tecno-económica de una planta industrial de producción de \textbf{e-metanol de $30,000\text{ toneladas métricas por año}$} a instalarse en el complejo industrial de referencia, Veracruz.

Al iniciar el desarrollo conceptual de este proyecto, nos enfrentamos a un dilema que todo ingeniero químico moderno conoce bien: \textbf{las limitaciones intrínsecas del software comercial cerrado}. Cuando uno formula una propuesta con tecnologías de frontera ---como la electrólisis de vapor a alta temperatura mediante celdas de óxido sólido (SOEC) o reactores catalíticos multitubulares heterogéneos con cinéticas complejas---, los simuladores convencionales simplemente \textbf{no tienen estos equipos en sus bibliotecas prediseñadas}. La práctica habitual en la industria es recurrir a aproximaciones burdas: cajas negras estáticas con conversiones fijas que falsean la termodinámica, omiten los perfiles térmicos y destruyen la fidelidad del análisis tecno-económico.

En Solvanta rompimos este paradigma recurriendo a \textbf{BioSTEAM}, una plataforma abierta en Python diseñada específicamente para el diseño de bioprocesos, biorrefinerías y evaluación económica ágil. Lo que hicimos en BioSTEAM fue programar nuestras propias operaciones unitarias a través de \textbf{Programación Orientada a Objetos}, creando subclases directas de la clase maestra \texttt{biosteam.Unit}.

Específicamente, programamos la unidad \texttt{PEMElectrolyzer} y el reactor tubular \texttt{MethanolPFRReactor}. Para lograr que BioSTEAM reconociera estos equipos como parte natural de su flowsheet, sobreescribimos tres métodos fundamentales:
\begin{enumerate}[nosep]
    \item \textbf{El método \texttt{\_run()}:} Donde definimos los balances de materia rigurosos, la estequiometría faradaica, los consumos molares de especies con la librería \texttt{thermosteam} y las especificaciones de equilibrio de fases en las corrientes de salida.
    \item \textbf{El método \texttt{\_design()}:} Donde se resuelven las ecuaciones de transporte, el dimensionamiento de las celdas y tubos, las pérdidas cinéticas y, crucialmente, la asignación de consumo eléctrico y demandas térmicas mediante \texttt{power\_utility} y \texttt{add\_heat\_utility}.
    \item \textbf{El método \texttt{\_cost()}:} Donde indexamos las correlaciones de costo de adquisición base de Guthrie y Turton, y las proyecciones oficiales del Departamento de Energía de EE. UU. (DOE Record 24005), desagregando los costos de stacks, balance de planta y rectificadores con sus respectivos factores de módulo desnudo ($F_{BM}$).
\end{enumerate}

Esto nos permitió realizar una auditoría tecno-económica preliminar ágil y comparar arquitecturas tecnológicas. Sin embargo, para escalar la planta a la máxima eficiencia termodinámica posible, decidimos explorar la electrólisis de óxido sólido a $800^\circ\text{C}$ acoplada térmicamente a la síntesis de metanol. Para explicar los primeros principios electroquímicos de esta tecnología y cómo logramos su integración rigurosa con el simulador DWSIM, cedo la palabra a mi compañero \textbf{Karol Camacho}.»
\end{speechgrecia}

\subsection{Intervención 2: Fundamentos del SOEC e Integración con DWSIM}

\begin{speechkaroc}{1:15 -- 2:45 \textbar\ Tono: Analítico, preciso y matemático}
«Muchas gracias, Grecia. Buenos días al tribunal.

La decisión de seleccionar la tecnología \textbf{SOEC (Solid Oxide Electrolyzer Cell)} en lugar de la electrólisis convencional PEM o alcalina responde a una ley termodinámica fundamental: conforme elevamos la temperatura de disociación del agua de $25^\circ\text{C}$ a $800^\circ\text{C}$, la entalpía total de reacción ($\Delta H$) permanece casi invariable en torno a $248\text{ kJ/mol}$, pero la energía libre de Gibbs ($\Delta G$) ---que representa el trabajo eléctrico neto que debemos inyectar--- \textbf{disminuye drásticamente de $237$ a $183.5\text{ kJ/mol}$}. Esa diferencia de $53.5\text{ kJ/mol}$ se transfiere al término entálpico térmico $T\Delta S$. En términos de ingeniería práctica: \textbf{reemplazamos un $28\%$ de la energía eléctrica cara por energía térmica de bajo costo}.

Como no existía un módulo SOEC ni en BioSTEAM ni en DWSIM, desarrollamos desde cero en Python una biblioteca física rigurosa estructurada en cuatro pilares:
\begin{enumerate}[nosep]
    \item \textbf{Termodinámica NIST Shomate:} Calculamos las entalpías, entropías y potenciales reversibles ($E^\circ$) integrando polinomios de 7 coeficientes válidos hasta $1,700\text{ K}$, descartando calores específicos constantes.
    \item \textbf{Potencial Reversible de Nernst:} Modelamos el voltaje de equilibrio dependiente no solo de la temperatura, sino de las presiones parciales de vapor, hidrógeno y oxígeno a lo largo del perfil de conversión del stack, evaluando rigurosamente el impacto de operar presurizados a $20\text{ bar}$.
    \item \textbf{Cinética de Transferencia de Carga (Butler-Volmer Inversa):} A diferencia de modelos simplificados que usan aproximaciones lineales de Tafel, resolvimos analíticamente la ecuación bidireccional completa de Butler-Volmer invirtiendo la función seno hiperbólico ($\operatorname{arsinh}$), diferenciando las resistencias de polarización del cátodo cermet Ni-YSZ y del ánodo de perovskita LSCF con energías de activación de Arrhenius.
    \item \textbf{Resistencia Óhmica y Fenómenos de Transporte:} Modelamos la resistencia específica de área ($ASR$) considerando la conducción aniónica de los iones oxígeno $\text{O}^{2-}$ a través del electrolito cerámico de zirconio estabilizado con itria (YSZ), y determinamos el límite difusivo por difusión de Stefan-Maxwell y Knudsen.
\end{enumerate}

Uno de los descubrimientos más potentes de este modelado fue identificar que nuestro diseño opera en \textbf{régimen sub-termoneutro}: con un voltaje de celda de apenas \textbf{$1.1828\text{ V}$}, nos situamos deliberadamente por debajo del voltaje termoneutro de la reacción ($V_{\text{tn}} = 1.287\text{ V}$). Esto significa que la celda es \textbf{endotérmica} y demanda calor externo continuo ($5,248.4\text{ kW}$ térmicos) para sostener la reacción.

¿Cómo lo resolvimos sin quemar gas ni penalizar el consumo eléctrico? Aquí entró la \textbf{integración algorítmica con DWSIM}. Desarrollamos un script de automatización en Python que actúa como puente de co-simulación. Este script toma las condiciones de proceso en DWSIM, resuelve el stack SOEC con nuestros módulos en Python e inyecta los balances de materia y energía en el flowsheet. Logramos una \textbf{simbiosis térmica perfecta}: el reactor de síntesis de metanol Lurgi BWR (\texttt{R-401}), cuya reacción es altamente exotérmica ($-12,335.4\text{ kW}$), genera en su coraza $16,244.9\text{ kg/h}$ de vapor saturado a $20\text{ bar}$. Este vapor cubre el \textbf{$100\%$ del vapor requerido por el electrolizador}, resolviendo la convergencia del bucle global en DWSIM mediante el método riguroso \textit{Inside-Out} y Peng-Robinson.

Ahora bien, una planta que opera a $800^\circ\text{C}$ con hidrógeno, oxígeno puro a alta presión y reactores a $75\text{ bar}$ exige una arquitectura de seguridad y control infalible. Cedo la palabra a Grecia para detallar los nodos del DTI, los lazos de control y el análisis de salvaguardas.»
\end{speechkaroc}

\subsection{Intervención 3: Nodos del DTI, Filosofía de Salvaguardas y HAZOP/SIL}

\begin{speechgrecia}{2:45 -- 4:15 \textbar\ Tono: Firme, metódico y normativo}
«Muchas gracias, Karol.

Para trasladar esta simulación termodinámica a una ingeniería de detalle construible y segura, desarrollamos el Diagrama de Tubería e Instrumentación (\textbf{DTI / P\&ID}, plano \texttt{DTI-v0.2\_Solvanta}). Siguiendo la metodología de seguridad de procesos y el estándar internacional IEC 61511 / ISA 84, descompusimos la totalidad de la planta en \textbf{10 Nodos Operacionales Críticos de Riesgo}, mapeados en una retícula alfanumérica georreferenciada de 8 columnas (A a H) por 5 filas (1 a 5).

Permítanme destacar los nodos más desafiantes y sus respectivas capas de protección independiente (IPL):
\begin{enumerate}
    \item \textbf{Nodo N-01 (Área 200 - Generación de Hidrógeno SOEC):}
    \begin{itemize}[nosep]
        \item \textit{Riesgo Mayor:} Reoxidación del cátodo de Ni-YSZ si se interrumpe el flujo reductor, o fuga de oxígeno puro presurizado a $800^\circ\text{C}$, lo que provocaría la combustión espontánea de cualquier material estructural.
        \item \textit{Salvaguardas Diseñadas:} Implementamos una línea de purga de gas protector reductor permanente (mezcla $\text{N}_2/\text{H}_2$ al $5\%$) con válvula de corte automático \texttt{SDV-201}, detectores electroquímicos de hidrógeno y analizadores ópticos de llama en los cuadrantes A1-B3. Ante falla de energía, se activa un venteo despresurizador de emergencia hacia el cabezal de nitrógeno.
    \end{itemize}
    \item \textbf{Nodo N-03 (Área 300 - Mezclado y Compresión de Syngas):}
    \begin{itemize}[nosep]
        \item \textit{Riesgo Mayor:} Entrada de gotas líquidas de agua o $\text{CO}_2$ al compresor centrífugo \texttt{C-301} ($1,316.7\text{ kW}$), provocando cavitación y falla mecánica catastrófica de los impulsores a alta velocidad.
        \item \textit{Salvaguardas Diseñadas:} Precalentador \texttt{E-301} controlado por lazo \texttt{TIC-301} que eleva la temperatura a $71.7^\circ\text{C}$, garantizando un margen de supercalentamiento de $+15^\circ\text{C}$ por encima del punto de rocío del syngas. Además, el compresor cuenta con una línea de reciclo rápido anti-surge gobernada por un algoritmo dedicado de respuesta en milisegundos.
    \end{itemize}
    \item \textbf{Nodo N-05 (Área 400 - Reactor Lurgi BWR R-401 y Caldera Coraza):}
    \begin{itemize}[nosep]
        \item \textit{Riesgo Mayor:} Embalamiento térmico (\textit{thermal runaway}) debido a la fuerte exotermicidad de la hidrogenación de $\text{CO}_2$ ($-90.7\text{ kJ/mol}$), lo que sinterizaría el catalizador de $\text{Cu/ZnO/Al}_2\text{O}_3$ o rompería los 2,126 tubos a $75\text{ bar}$.
        \item \textit{Salvaguardas Diseñadas:} El control de temperatura es indirecto pero ultraestable: un lazo en cascada \texttt{TIC-401} modula la válvula \texttt{PCV-401-S} en la línea de vapor de la coraza. Manteniendo la presión de ebullición del agua a $20\text{ bar}$ ($212.4^\circ\text{C}$), el coeficiente de transferencia por cambio de fase es gigantesco ($U > 1,200\text{ W/m}^2\text{K}$), absorbiendo de inmediato cualquier fluctuación térmica. Como salvaguarda final, contamos con una matriz de votación 2oo3 (dos de tres) de transmisores de alta-alta presión y temperatura (\texttt{PAHH/TAHH-401}), que ante cualquier desviación disparan las válvulas de aislamiento \texttt{SDV-401} y derivan el inventario reactivo a la válvula de seguridad \texttt{PSV-401} hacia la antorcha.
    \end{itemize}
    \item \textbf{Nodo N-07 (Área 500 - Lazo de Reciclo y Purga):}
    \begin{itemize}[nosep]
        \item \textit{Riesgo Mayor:} Acumulación de gases inertes ($\text{CH}_4$ proveniente de la metanación parásita y $\text{N}_2$ del $\text{CO}_2$ capturado). Si no se purgan, el lazo de reciclaje incrementa la presión hasta provocar el colapso del compresor de reciclo o asfixia catalítica.
        \item \textit{Salvaguardas Diseñadas:} Analizador cromatográfico en línea \texttt{AIC-501} conectado al lazo de purga del $4.0\%$. Si la fracción de inertes supera el $8\%$, la válvula \texttt{FCV-501} abre proporcionalmente hacia el expansor \texttt{EXP-501} o hacia el flare, protegiendo la relación de recirculación del $96\%$.
    \end{itemize}
\end{enumerate}

Todos estos lazos fueron integrados con \textbf{filosofía SIL-2 para lazos de control de proceso básico (BPCS)} y \textbf{SIL-3 para los Sistemas Instrumentados de Seguridad (SIS)}, con válvulas de alivio dimensionadas bajo las normas API 520 y API 521.

Con la seguridad del proceso plenamente garantizada, el siguiente reto fue optimizar el desempeño energético del SOEC para volverlo industrialmente competitivo frente a cualquier tecnología del mercado. Karol explicará cómo el barrido paramétrico y los 4 escenarios de operación nos permitieron descubrir el punto óptimo de máxima eficiencia.»
\end{speechgrecia}

\subsection{Intervención 4: Escenarios SOEC, Trade-offs y Selección del Punto Óptimo}

\begin{speechkaroc}{4:15 -- 5:45 \textbar\ Tono: Científico, riguroso y estratégico}
«Gracias, Grecia.

Cuando se diseña un sistema electroquímico de óxido sólido, el ingeniero se enfrenta a un espacio de diseño multivariable dominado por tres fuerzas en conflicto: la \textbf{temperatura}, la \textbf{presión} y la \textbf{densidad de corriente}. Para explorar este espacio, formulamos y simulamos mediante scripts de Python cuatro escenarios operativos mutuamente excluyentes:
\begin{itemize}[nosep]
    \item \textbf{Escenario A ($750^\circ\text{C}, 1.5\text{ bar}, 0.35\text{ A/cm}^2$):} Caso base académico a baja presión.
    \item \textbf{Escenario B ($750^\circ\text{C}, 20.0\text{ bar}, 0.40\text{ A/cm}^2$):} Presurizado estándar.
    \item \textbf{Escenario C ($800^\circ\text{C}, 1.5\text{ bar}, 0.45\text{ A/cm}^2$):} Alta temperatura a baja presión.
    \item \textbf{Escenario D ($800^\circ\text{C}, 20.0\text{ bar}, 0.480\text{ A/cm}^2$):} Nuestra propuesta técnica de vanguardia.
\end{itemize}

Permítanme desglosar los tres equilibrios físicos (\textit{trade-offs}) que resolvimos con nuestro código:
\begin{enumerate}
    \item \textbf{El efecto dominante de la Temperatura en la resistencia óhmica:}
    La conducción de iones $\text{O}^{2-}$ en la red cristalina de circonia sigue un comportamiento térmicamente activado de tipo Arrhenius. Al elevar la temperatura operativa de $750^\circ\text{C}$ ($1,023.15\text{ K}$) a $800^\circ\text{C}$ ($1,073.15\text{ K}$), la resistencia específica de área ($ASR$) colapsa de $0.220\ \Omega\cdot\text{cm}^2$ a \textbf{$0.1161\ \Omega\cdot\text{cm}^2$}. Esto representa una \textbf{reducción neta del $47.2\%$ en la pérdida óhmica}. Menos calor por efecto Joule desperdiciado y mayor eficiencia de conversión.
    \item \textbf{El dilema de la Presión (Nernst vs. Integración de Planta):}
    Termodinámicamente, elevar la presión de $1.5$ a $20\text{ bar}$ penaliza el potencial de Nernst en $+55\text{ mV}$ debido al término $\frac{RT}{4F}\ln(P/P^\circ)$. Muchos autores descartan la presurización por este motivo. Sin embargo, al analizar la planta de manera holística, descubrimos que operar el SOEC a $20\text{ bar}$:
    \begin{itemize}[nosep]
        \item Reduce el volumen específico del gas en un \textbf{$92.5\%$}, achicando el diámetro de colectores, tuberías y carcasas de stacks.
        \item Elimina dos etapas completas de compresión mecánica de hidrógeno, ahorrando megavatios de potencia motriz.
        \item Y lo más trascendental: permite que el vapor generado a $20\text{ bar}$ en el reactor de metanol ingrese de forma pasiva al SOEC sin necesidad de recompresores de vapor húmedo.
    \end{itemize}
    \item \textbf{El equilibrio de la Densidad de Corriente ($j = 0.480\text{ A/cm}^2$):}
    Una baja densidad de corriente ofrece altos voltajes pero exige millones de celdas, disparando el CAPEX de inversión. Una alta densidad de corriente ahorra celdas pero incrementa el sobrepotencial óhmico y el consumo de electricidad (OPEX).
\end{enumerate}

Mediante un algoritmo de barrido paramétrico construimos el \textbf{Frente de Pareto Multiobjetivo}, cruzando el Consumo Específico de Energía Eléctrica ($SEC_{\text{AC}}$ en $\text{kWh/kg H}_2$) contra el Costo Nivelado del Hidrógeno ($LCOH$). El \textbf{Escenario D} demostró ser el punto de inflexión perfecto:
\begin{itemize}[nosep]
    \item Alcanza un voltaje de celda de \textbf{$1.1828\text{ V}$}, donde el $85.02\%$ corresponde al potencial termodinámico, $9.46\%$ a activación, $4.71\%$ a resistencia óhmica y apenas $0.81\%$ a difusión.
    \item Con una densidad de $0.480\text{ A/cm}^2$, operamos al \textbf{$18.8\%$ de la corriente límite difusiva ($j_{\text{lim}} = 2.551\text{ A/cm}^2$)}, garantizando inmunidad total contra la inanición de reactivos.
    \item La potencia eléctrica total de la planta se reduce a \textbf{$38.07\text{ MWe}$}, logrando un $SEC_{\text{AC}}$ de \textbf{$32.92\text{ kWh/kg H}_2$} a nivel celda y \textbf{$38.07\text{ kWh/kg H}_2$} a nivel batería de planta.
\end{itemize}

Esto representa un \textbf{ahorro de energía eléctrica superior al $30\%$ en comparación con cualquier planta comercial PEM o alcalina}, que demandan entre $52$ y $60\text{ kWh/kg H}_2$.

Para concluir nuestra intervención y reflexionar sobre el impacto de estas metodologías en la ingeniería moderna, cedo el estrado a Grecia para el cierre.»
\end{speechkaroc}

\subsection{Intervención 5: Conclusión Final y Cierre}

\begin{speechgrecia}{5:45 -- 6:30 \textbar\ Tono: Inspirador, formal y contundente}
«Muchas gracias, Karol.

Para finalizar nuestra defensa, queremos dejar una reflexión que consideramos el mayor aprendizaje y valor agregado de este proyecto de licitación:

Durante décadas, la formación tradicional del ingeniero de procesos nos condicionó a ser simples usuarios pasivos de paquetes comerciales de simulación: si una operación unitaria o un equipo de última generación no venía incluido en la barra de herramientas del software, el proyecto se declaraba inviable o se forzaba mediante aproximaciones burdas.

Este trabajo demuestra que \textbf{la programación en Python es la herramienta de emancipación técnica más poderosa para el ingeniero químico contemporáneo}.

Cuando entendemos la física, la termodinámica fundamental, la cinética heterogénea y la electroquímica desde sus primeros principios, \textbf{la programación nos libera de las limitaciones de las bibliotecas comerciales cerradas}. Si una tecnología disruptiva ---como las celdas de electrólisis SOEC de alta temperatura--- \textbf{existe físicamente en la realidad, en los centros de investigación y en el mercado industrial, pero no existe en la base de datos de un simulador}, los ingenieros tenemos hoy la capacidad matemática y computacional de programarla, calibrarla y acoplarla dinámicamente.

Esta habilidad de \textbf{adecuar la realidad física a nuestras herramientas computacionales} ---y no someter la realidad a las limitaciones de un software--- es lo que nos permite formular propuestas de ingeniería mucho más interesantes, técnicamente rigurosas, ambientalmente descarbonizadas y comercialmente competitivas ante la industria global.

Agradecemos profundamente su atención y quedamos a su entera disposición para responder a todas sus preguntas técnicas. Muchas gracias.»
\end{speechgrecia}

\newpage

% ==============================================================================
% SECCIÓN 2: ARQUITECTURA DE CÓDIGO Y ESTRUCTURA DE PROGRAMACIÓN
% ==============================================================================
\section{ARQUITECTURA DE CÓDIGO Y ESTRUCTURA DE PROGRAMACIÓN}

\subsection{Programación Orientada a Objetos en BioSTEAM (\texttt{biosteam.Unit})}

La plataforma \textbf{BioSTEAM} basa su extensibilidad en la jerarquía de herencia de clases. La clase abstracta \texttt{biosteam.Unit} gobierna la interfaz estandarizada de cálculo:

\begin{codebox}{Estructura Esquemática de una Unidad en BioSTEAM}
\begin{lstlisting}[language=Python,basicstyle=\ttfamily\footnotesize]
import biosteam as bst
import thermosteam as tst

class CustomElectrolyzer(bst.Unit):
    _N_ins = 1         # 1 corriente de entrada (H2O)
    _N_outs = 2        # 2 corrientes de salida (H2 catodo, O2 anodo)
    
    _F_BM_default = {
        'Stacks SOEC': 1.65,
        'Rectificadores AC/DC': 1.25,
        'Balance de Planta y Calentador': 1.80
    }
    
    _units = {
        'Potencia AC': 'kW',
        'Consumo Especifico': 'kWh/kg H2',
        'Area Activa': 'm2'
    }
\end{lstlisting}
\end{codebox}

\subsubsection{Mecanismos Internos de los Tres Métodos Maestros}
\begin{enumerate}
    \item \textbf{Método \texttt{\_run()}:} Resuelve los balances de materia estequiométricos y equilibrio de fases. Modifica directamente las corrientes de salida \texttt{self.outs[0]} y \texttt{self.outs[1]} especificando flujos molares con \texttt{thermosteam}, temperatura $T$, presión $P$ y estado de fase (\texttt{phase = 'g'} o \texttt{'l'}).
    \item \textbf{Método \texttt{\_design()}:} Resuelve las ecuaciones de transporte y dimensionamiento geométrico. Asigna los servicios auxiliares:
    \begin{itemize}[nosep]
        \item Consumo eléctrico: \texttt{self.power\_utility.consumption = P\_ac\_kw}
        \item Cargas térmicas: \texttt{self.add\_heat\_utility(unit\_duty=-Q\_kw, T\_in=T, T\_out=T)}
    \end{itemize}
    \item \textbf{Método \texttt{\_cost()}:} Registra los costos de compra base $C_{p,0}$ en el diccionario \texttt{self.baseline\_purchase\_costs}. BioSTEAM multiplica automáticamente estos valores por los factores de módulo desnudo $F_{BM}$ para calcular el CAPEX total instalado.
\end{enumerate}

\subsection{Automatización y Conexión de DWSIM mediante API en Python}

La integración con DWSIM se programó en Python utilizando la pasarela binaria .NET (\texttt{pythonnet}):

\begin{codebox}{Script de Co-Simulación DWSIM en Python}
\begin{lstlisting}[language=Python,basicstyle=\ttfamily\footnotesize]
import clr
clr.AddReference("DWSIM.Interfaces")
clr.AddReference("DWSIM.Automation")
from DWSIM.Automation import Automation3

interf = Automation3()
fs = interf.LoadFlowsheet("DWSIM_v1_Sensibilidad_Solvanta.dwxml")

# Modificacion parametrica de corriente S-203 (Vapor a 800 C y 20 bar)
s_vap = fs.GetFlowsheetSimulationObject("S-203")
s_vap.SetTemperature(1073.15)      # 800 C (1073.15 K)
s_vap.SetPressure(2000000.0)       # 20 bar
s_vap.SetMolarFlow(n_molar_vap)    # kmol/s

# Resolucion secuencial con acelerador Wegstein
fs.SolveFlowsheet()
\end{lstlisting}
\end{codebox}

\newpage

% ==============================================================================
% SECCIÓN 3: FUNDAMENTOS FÍSICOS, DESGLOSE DE ECUACIONES Y DESPEJES
% ==============================================================================
\section{FUNDAMENTOS FÍSICOS, DESGLOSE DE ECUACIONES Y DESPEJES PASO A PASO}

\subsection{Termodinámica Fundamental y Polinomios de Shomate de NIST-JANAF}

La reacción de disociación de vapor es:
\begin{equation}
\text{H}_2\text{O}_{(g)} \longrightarrow \text{H}_{2(g)} + \frac{1}{2}\text{O}_{2(g)}
\end{equation}

Los calores específicos molares se calculan mediante los polinomios de Shomate del NIST (Chase, 1998) con $t = T / 1000$:
\begin{align}
C_p^\circ(T) &= A + B t + C t^2 + D t^3 + \frac{E}{t^2} \quad \left[\frac{\text{J}}{\text{mol}\cdot\text{K}}\right] \\
H^\circ(T) - H^\circ_{298.15} &= A t + B \frac{t^2}{2} + C \frac{t^3}{3} + D \frac{t^4}{4} - \frac{E}{t} + F - H \quad \left[\frac{\text{kJ}}{\text{mol}}\right] \\
S^\circ(T) &= A \ln(t) + B t + C \frac{t^2}{2} + D \frac{t^3}{3} - \frac{E}{2 t^2} + G \quad \left[\frac{\text{J}}{\text{mol}\cdot\text{K}}\right]
\end{align}

\begin{mathdeductionbox}{Evaluación Numérica Exacta a $800^\circ\text{C}$ ($1,073.15\text{ K}$)}
Sustituyendo los coeficientes para $\text{H}_2\text{O}_{(g)}$, $\text{H}_{2(g)}$ y $\text{O}_{2(g)}$ a $t = 1.07315$:
\begin{align*}
\Delta H^\circ(1073.15\text{ K}) &= H^\circ_{\text{H}_2} + 0.5 H^\circ_{\text{O}_2} - H^\circ_{\text{H}_2\text{O}} = \mathbf{+248.35\text{ kJ/mol}} \\
\Delta S^\circ(1073.15\text{ K}) &= S^\circ_{\text{H}_2} + 0.5 S^\circ_{\text{O}_2} - S^\circ_{\text{H}_2\text{O}} = \mathbf{+60.38\text{ J/(mol}\cdot\text{K)}} \\
\Delta G^\circ(1073.15\text{ K}) &= \Delta H^\circ - T \Delta S^\circ = 248,350 - (1073.15 \times 60.38) = \mathbf{+183.55\text{ kJ/mol}}
\end{align*}
Potencial reversible estándar $E^\circ$ y voltaje termoneutro $V_{\text{tn}}$ ($z=2, F=96,485.33\text{ C/mol}$):
\begin{equation}
E^\circ(800^\circ\text{C}) = -\frac{\Delta G^\circ}{z F} = \frac{183,553}{2 \times 96,485.33} = \mathbf{0.9512\text{ V}}, \qquad
V_{\text{tn}}(800^\circ\text{C}) = \frac{\Delta H^\circ}{z F} = \frac{248,350}{2 \times 96,485.33} = \mathbf{1.2869\text{ V}}
\end{equation}
\end{mathdeductionbox}

\subsection{Potencial Reversible de Nernst con Presión y Conversión}

La ecuación de Nernst expandida en función de las fracciones molares y la presión total $P$ ($P^\circ = 1.0\text{ bar}$):
\begin{equation}
E_{\text{Nernst}} = E^\circ(T) + \frac{R T}{2 F} \ln\left( \frac{y_{\text{H}_2} \cdot y_{\text{O}_2}^{0.5}}{y_{\text{H}_2\text{O}}} \right) + \mathbf{\frac{R T}{4 F} \ln\left( \frac{P}{P^\circ} \right)}
\end{equation}

\begin{mathdeductionbox}{Despeje y Evaluación del Efecto de Presión ($20\text{ bar}$ vs $1.5\text{ bar}$)}
\begin{equation}
\Delta E_{\text{presion}} = \frac{R T}{4 F} \ln\left( \frac{20.0}{1.5} \right) = \frac{8.31446 \times 1073.15}{4 \times 96,485.33} \ln(13.333) = \mathbf{+0.0599\text{ V} \approx +60\text{ mV}}
\end{equation}
A una conversión de vapor del $70\%$ ($y_{\text{H}_2\text{O}} = 0.30$, $y_{\text{H}_2} = 0.70$, $y_{\text{O}_2} = 1.0$):
\begin{equation}
E_{\text{Nernst}}(800^\circ\text{C}, 20\text{ bar}) = 0.9512 + 0.0392 + 0.0599 - 0.0447 = \mathbf{1.0056\text{ V}}
\end{equation}
\end{mathdeductionbox}

\subsection{Cinética de Activación y Despeje Analítico de Butler-Volmer}

La ecuación de Butler-Volmer simétrica ($\alpha = 0.5$):
\begin{equation}
j = 2 j_0 \sinh\left( \frac{F \eta_{\text{act}}}{2 R T} \right)
\end{equation}

\begin{mathdeductionbox}{Deducción Paso a Paso del Despeje de $\eta_{\text{act}}$ con $\operatorname{arsinh}$}
Despejando el argumento hiperbólico y aplicando la definición funcional del arcoseno hiperbólico:
\begin{equation}
\sinh\left( \frac{F \eta_{\text{act}}}{2 R T} \right) = \frac{j}{2 j_0} \implies
\eta_{\text{act}} = \mathbf{\frac{2 R T}{F} \operatorname{arsinh}\left( \frac{j}{2 j_0} \right) = \frac{2 R T}{F} \ln\left( \frac{j}{2 j_0} + \sqrt{\left(\frac{j}{2 j_0}\right)^2 + 1} \right)}
\end{equation}
Evaluando a $800^\circ\text{C}$ y $j = 0.480\text{ A/cm}^2$ con $j_{0,c} = 0.530\text{ A/cm}^2$ y $j_{0,a} = 0.380\text{ A/cm}^2$:
\begin{equation}
\eta_{\text{act},c} = 0.0475\text{ V}, \qquad \eta_{\text{act},a} = 0.0644\text{ V} \implies \eta_{\text{act}} = \mathbf{0.1119\text{ V}}
\end{equation}
\end{mathdeductionbox}

\subsection{Pérdidas Óhmicas y Conducción Iónica en Electrolito YSZ}

La resistencia específica de área ($ASR$) sigue la conducción de Arrhenius en la red cristalina:
\begin{equation}
ASR(T) = ASR_{\text{ref}} \cdot \exp\left[ \frac{E_{\text{ohm}}}{R} \left( \frac{1}{T} - \frac{1}{T_{\text{ref}}} \right) \right]
\end{equation}

\begin{mathdeductionbox}{Abatimiento Térmico de Resistencia Óhmica ($750^\circ\text{C} \to 800^\circ\text{C}$)}
Con $ASR(750^\circ\text{C}) = 0.220\ \Omega\cdot\text{cm}^2$ y $E_{\text{ohm}} = 80\text{ kJ/mol}$:
\begin{equation}
ASR(800^\circ\text{C}) = \mathbf{0.1161\ \Omega\cdot\text{cm}^2} \implies \text{Reducción de } \mathbf{47.23\%}
\end{equation}
\begin{equation}
\eta_{\text{ohm}} = j \cdot ASR = (0.480\text{ A/cm}^2) \times (0.1161\ \Omega\cdot\text{cm}^2) = \mathbf{0.0557\text{ V}}
\end{equation}
\end{mathdeductionbox}

\subsection{Sobrepotencial de Concentración y Límite Difusivo}

\begin{equation}
j_{\text{lim}} = \frac{2 F \cdot P \cdot D_{\text{eff}}}{R T \cdot \delta} y_{\text{H}_2\text{O}} = \mathbf{2.551\text{ A/cm}^2}
\end{equation}
\begin{equation}
\frac{j}{j_{\text{lim}}} = \frac{0.480}{2.551} = \mathbf{0.1882\ (18.8\%)} \ll 80\% \implies \eta_{\text{conc}} = \mathbf{0.0096\text{ V}}
\end{equation}

\subsection{Voltaje Total y Balance Térmico Endotérmico}

\begin{equation}
V_{\text{celda}} = 1.0056 + 0.1119 + 0.0557 + 0.0096 = \mathbf{1.1828\text{ V}} < V_{\text{tn}} = 1.2869\text{ V}
\end{equation}
\begin{equation}
\dot{Q}_{\text{stack}} = I_{\text{total}} \cdot (V_{\text{celda}} - V_{\text{tn}}) = \mathbf{-3,350.9\text{ kW térmicos (Endotérmico)}}
\end{equation}
El calor exotérmico liberado por el reactor Lurgi de metanol \texttt{R-401} ($\dot{Q} = -12,335.4\text{ kW}$) evapora en su coraza $16,244.9\text{ kg/h}$ de vapor a $20\text{ bar}$, suministrando el \textbf{$100\%$ del vapor del SOEC}.

\newpage

% ==============================================================================
% SECCIÓN 4: METADATOS DE TOPOLOGÍA, BALANCES Y SERVICIOS AUXILIARES
% ==============================================================================
\section{METADATOS DE TOPOLOGÍA, BALANCES Y SERVICIOS AUXILIARES}

\subsection{Topología como Grafo Dirigido $G=(V,E)$ y Tear Streams}

El flowsheet se modela como un grafo dirigido donde los vértices $V$ son las operaciones unitarias y las aristas $E$ las corrientes. El bucle de reciclaje se resuelve mediante el algoritmo de Tarjan para componentes fuertemente conexos, seleccionando la corriente \texttt{S-504} como \textit{Tear Stream} bajo el acelerador de Wegstein:
\begin{equation}
x^{(k+1)} = q \cdot g(x^{(k)}) + (1 - q) x^{(k)}, \qquad q = \frac{1}{1 - s}
\end{equation}

\subsection{Matriz de Balance de Materia Global de la Planta}

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\linewidth}{l c c c X}
\toprule
\rowcolor{tableheader}
\color{white}\textbf{Corriente (Tag)} & \color{white}\textbf{Flujo (kg/h)} & \color{white}\textbf{Flujo (kmol/h)} & \color{white}\textbf{Fase} & \color{white}\textbf{Composición Clave} \\
\midrule
\rowcolor{tablerowgray}
Agua Alimentación (\texttt{S-200}) & $11,842.1$ & $657.3$ & Líquido & $\text{H}_2\text{O} > 99.99\%$ \\
$\text{CO}_2$ Batería (\texttt{S-101}) & $5,274.3$ & $119.8$ & Gas denso & $\text{CO}_2: 99.5\%, \text{N}_2: 0.5\%$ \\
\rowcolor{tablerowgray}
$\text{H}_2$ SOEC (\texttt{S-205}) & $1,314.8$ & $652.2$ & Gas & $\text{H}_2: 99.2\%, \text{H}_2\text{O}: 0.8\%$ \\
$\text{O}_2$ Venta (\texttt{S-206}) & $10,434.5$ & $326.1$ & Gas & $\text{O}_2: 99.8\%, \text{H}_2\text{O}: 0.2\%$ \\
\rowcolor{tablerowgray}
Syngas Reactor (\texttt{S-401}) & $21,308.1$ & $1,985.4$ & Gas ($75\text{ bar}$) & $\text{H}_2: 74.2\%, \text{CO}_2: 15.6\%, M=2.05$ \\
\textbf{e-Metanol Grado AA (\texttt{S-604})} & $\mathbf{3,788.65}$ & $\mathbf{118.2}$ & \textbf{Líquido} & $\mathbf{CH_3OH: 99.89\%\ wt}$ ($30.3\text{ kt/año}$) \\
\rowcolor{tablerowgray}
Purga Inertes (\texttt{S-505}) & $852.3$ & $79.4$ & Gas & $\text{H}_2: 68\%, \text{CH}_4: 18\%, \text{CO}_2: 9\%$ \\
Agua Efluente ZLD (\texttt{S-605}) & $2,130.8$ & $118.3$ & Líquido & $\text{H}_2\text{O} > 99.95\%\ wt$ \\
\bottomrule
\end{tabularx}
\caption{Matriz consolidada de balances de materia globales de la planta.}
\end{table}

\subsection{Matriz de Balance de Energía y Demanda de Servicios Auxiliares}

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\linewidth}{l c c X}
\toprule
\rowcolor{tableheader}
\color{white}\textbf{Equipo (Tag)} & \color{white}\textbf{Servicio Auxiliar} & \color{white}\textbf{Carga Nominal} & \color{white}\textbf{Criterio de Diseño y Optimización} \\
\midrule
\rowcolor{tablerowgray}
Stacks SOEC (\texttt{EL-201}) & Electricidad DC/AC & $\mathbf{38.07\text{ MWe}}$ & $800^\circ\text{C}, 20\text{ bar}, 0.480\text{ A/cm}^2, SEC = 32.92\text{ kWh/kg H}_2$. \\
Precalentador (\texttt{E-202}) & Eléctrico Incoloy 800H & $\mathbf{5,248.4\text{ kW}}$ & Eleva vapor de $212.4^\circ\text{C}$ a $800.0^\circ\text{C}$ ($A = 187.4\text{ m}^2$). \\
\rowcolor{tablerowgray}
Compresor Syngas (\texttt{C-301}) & Electricidad Motor & $\mathbf{1,316.7\text{ kWe}}$ & 2 etapas ($19.4 \to 75\text{ bar}$) con intercooling. \\
Compresor Reciclo (\texttt{C-501}) & Electricidad Motor & $\mathbf{215.4\text{ kWe}}$ & Compensa pérdida de carga del lazo ($2.5\text{ bar}$). \\
\rowcolor{tablerowgray}
Expansor Purga (\texttt{EXP-501}) & Generación Eléctrica & $\mathbf{-437.8\text{ kWe}}$ & Generador de recuperación energética ($72.5 \to 1.5\text{ bar}$). \\
Reboiler Destilación (\texttt{E-601}) & Vapor Baja Presión & $\mathbf{2,850.0\text{ kW}}$ & Vapor saturado $120^\circ\text{C}$ para hervidor de fondo T-601. \\
\rowcolor{tablerowgray}
Condensador Flash (\texttt{E-501}) & Cooling Water (CW) & $\mathbf{8,450.0\text{ kW}}$ & Agua de torre $30^\circ\text{C} \to 40^\circ\text{C}$ para condensar efluente. \\
Condensador Reflujo (\texttt{E-602}) & Cooling Water (CW) & $\mathbf{2,610.0\text{ kW}}$ & Condensación total del destilado en domo de T-601. \\
\rowcolor{tablerowgray}
\textbf{Caldera Coraza (\texttt{R-401-S})} & \textbf{Generación de Vapor} & $\mathbf{-12,335.4\text{ kW}}$ & \textbf{Genera $16,244.9\text{ kg/h}$ de vapor saturado a $20\text{ bar}$ para SOEC.} \\
\bottomrule
\end{tabularx}
\caption{Matriz consolidada de servicios auxiliares y balances energéticos.}
\end{table}

\begin{conceptbox}{Resumen Técnico Global de la Planta}
\begin{itemize}[nosep]
    \item \textbf{Potencia Eléctrica Neta de Planta:} $\mathbf{39.85\text{ MWe}}$ (incluyendo compresores y auxiliares de bombeo BFW).
    \item \textbf{Consumo Específico Global:} $\mathbf{10.52\text{ MWh / tonelada de e-Metanol}}$ ($1.31\text{ kWe/kg MeOH}$).
    \item \textbf{Eficiencia Exergética Global:} $\mathbf{64.8\%}$ (LHV Metanol / Potencia Eléctrica + Calor).
    \item \textbf{Emisiones de $\text{CO}_2$ Evitadas:} $\mathbf{41,200\text{ t }\text{CO}_2/\text{año}}$ capturadas e incorporadas al producto químico.
\end{itemize}
\end{conceptbox}

\end{document}
"""

def main():
    print("Escribiendo código fuente LaTeX en:", TEX_PATH)
    tex_code = build_latex_content()
    with open(TEX_PATH, "w", encoding="utf-8") as f:
        f.write(tex_code)
    
    print("Compilando documento con pdflatex (Pasada 1)...")
    res1 = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory=Entregables", TEX_PATH],
        capture_output=True, text=True, errors="replace"
    )
    if res1.returncode != 0:
        print("Error en Pasada 1 de pdflatex:")
        for line in res1.stdout.split("\n"):
            if "!" in line or "Error" in line:
                print("  ", line)
        sys.exit(1)
        
    print("Compilando documento con pdflatex (Pasada 2 para índice y referencias cruzadas)...")
    res2 = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory=Entregables", TEX_PATH],
        capture_output=True, text=True, errors="replace"
    )
    if res2.returncode == 0:
        print(f"Compilación exitosa. PDF generado en: {PDF_PATH}")
        # Copiar también a la raíz para fácil acceso
        shutil.copy(PDF_PATH, "./Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf")
        print("Copia sincronizada en: ./Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf")
    else:
        print("Error en Pasada 2 de pdflatex.")
        sys.exit(1)

if __name__ == "__main__":
    main()

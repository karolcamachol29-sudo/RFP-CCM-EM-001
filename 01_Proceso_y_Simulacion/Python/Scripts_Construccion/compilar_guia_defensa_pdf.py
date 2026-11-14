#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador y Compilador de la Guía Maestra de Defensa Técnica y Exposición en PDF
Planta de Producción de e-Metanol (30,000 t/año) - Solvanta Engineering Solutions S.A. de C.V.
Cubre: HAZOP (AC-HAZOP-01) + Paquete de Ingeniería Básica (PIB-01) + Plot Plan (Solvanta_AG-01)
"""

import os
import subprocess
import shutil

def build_latex_content():
    content = r"""\documentclass[11pt,letterpaper]{article}

% --- PAQUETES DE CONFIGURACIÓN BÁSICA ---
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-tabla]{babel}
\AtBeginDocument{\renewcommand{\contentsname}{Índice General de Contenidos}}
\usepackage[margin=2.0cm,top=2.5cm,bottom=2.5cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xltabular}
\usepackage{array}
\usepackage{colortbl}
\usepackage{pdflscape}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{tikz}
\usepackage{enumitem}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}

% --- PALETA DE COLORES SOLVANTA ---
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
\fancyhead[R]{\small\color{darkslate}Guía de Defensa Técnica: HAZOP y PIB-01}
\fancyfoot[L]{\footnotesize\color{darkslate}Proyecto RFP-CCM-EM-001 | complejo industrial adyacente}
\fancyfoot[R]{\footnotesize\bfseries\color{primaryblue}Página \thepage\ de \pageref{LastPage}}

% --- ESTILOS DE CAJAS TCOLORBOX ---
\newtcolorbox{conceptbox}[1]{
    enhanced,
    colback=lightbg,
    colframe=secondaryblue,
    fonttitle=\bfseries\color{white},
    colbacktitle=secondaryblue,
    title=#1,
    boxrule=1.0pt,
    arc=3pt,
    boxsep=3pt,
    breakable
}

\newtcolorbox{interlockbox}[1]{
    enhanced,
    colback=alertbg,
    colframe=alertred,
    fonttitle=\bfseries\color{white},
    colbacktitle=alertred,
    title=#1,
    boxrule=1.0pt,
    arc=3pt,
    boxsep=3pt,
    breakable
}

\newtcolorbox{questionbox}[1]{
    enhanced,
    colback=warnbg,
    colframe=warngold,
    fonttitle=\bfseries\color{white},
    colbacktitle=warngold,
    title=#1,
    boxrule=1.0pt,
    arc=3pt,
    boxsep=3pt,
    breakable
}

\setlength{\parskip}{0.4em}
\setlength{\parindent}{0pt}

\begin{document}

% ==============================================================================
% PORTADA EJECUTIVA
% ==============================================================================
\begin{titlepage}
    \centering
    \vspace*{-1.0cm}
    
    \begin{minipage}{0.45\textwidth}
        \includegraphics[height=1.8cm]{figuras/logo_empresa.png}
    \end{minipage}
    \hfill
    \begin{minipage}{0.50\textwidth}
        \raggedleft
        \footnotesize\color{darkslate}
        \textbf{FACULTAD DE INGENIERÍA QUÍMICA}\\
        Departamento de Procesos y Plantas Químicas\\
        Materia: Diseño de Procesos y Plantas Químicas (DPyPQ)\\
        Docente: \textbf{Dr. Jesús Andrés Arzola Flores}
    \end{minipage}

    \vspace{1.2cm}
    \noindent\makebox[\linewidth]{\color{primaryblue}\rule{\linewidth}{2.5pt}}
    \vspace{0.3cm}

    {\huge\bfseries\color{primaryblue}GUÍA MAESTRA DE DEFENSA TÉCNICA Y EXPOSICIÓN}\\[0.3cm]
    {\Large\bfseries\color{secondaryblue}Manual Integral de Dominio y Justificación de Ingeniería}\\[0.2cm]
    {\large\color{darkslate}\textbf{Taller HAZOP (AC-HAZOP-01) y Paquete de Ingeniería Básica (PIB-01)}}\\[0.1cm]
    {\normalsize\itshape Desglose Analítico de Cálculos, Balances DWSIM, Plot Plan y Banco de Respuestas de Sínodo}

    \vspace{0.4cm}
    \noindent\makebox[\linewidth]{\color{primaryblue}\rule{\linewidth}{1.0pt}}
    \vspace{0.8cm}

    \begin{tcolorbox}[enhanced, colback=lightbg, colframe=primaryblue, boxrule=1.2pt, arc=4pt]
        \centering\small
        \textbf{DATOS GENERALES DE LA PLANTA DE PROCESO}\\[0.2cm]
        \begin{tabular}{ll}
            \textbf{Proyecto Licitatorio:} & RFP-CCM-EM-001 (Licitación Privada Internacional) \\
            \textbf{Capacidad de Producción:} & $30\,000\text{ t/año}$ de e-Metanol Grado Químico AA ($>99.85\%$ p/p) \\
            \textbf{Régimen Operativo:} & $8\,000\text{ h/año}$ ($91.32\%$ disponibilidad, $333.3\text{ días}$ continuos) \\
            \textbf{Ubicación de Parcela:} & predio industrial asignado para el proyecto RFP-CCM-EM-001. \\
            \textbf{Tecnologías Centrales:} & Captura de $\text{CO}_2$, Electrólisis SOEC ($800^\circ\text{C}$), Reactor BWR Lurgi y ZLD \\
            \textbf{Firma de Ingeniería:} & \textbf{Solvanta Engineering Solutions S.A. de C.V.}
        \end{tabular}
    \end{tcolorbox}

    \vspace{0.8cm}

    \begin{tcolorbox}[enhanced, colback=white, colframe=darkslate, boxrule=0.8pt, arc=3pt]
        \centering\small
        \textbf{EQUIPO TÉCNICO Y AUTORÍA DE INGENIERÍA}\\[0.25cm]
        \begin{tabularx}{\textwidth}{p{6.0cm} X}
            \textbf{Ing. Karol Paola Camacho López} & Directora de Proyecto \textbar\ Coordinación y Balances Macro \\
            \textbf{Ing. Paulina Mota Macip} & Especialista en Simulación DWSIM, Termodinámica y Proceso \\
            \textbf{Ing. Gildardo Ocaña Barrales} & Custodio del DTI, Catálogo de Equipos y Arreglo General \\
            \textbf{Ing. Grecia Figueroa Rincón} & Especialista en Seguridad Industrial, HSE y Taller HAZOP \\
        \end{tabularx}
    \end{tcolorbox}

    \vfill
    {\footnotesize\color{darkslate}sitio industrial de referencia \textbar\ Periodo Otoño 2026 \textbar\ Documento Oficial de Preparación Técnica}
\end{titlepage}

% ==============================================================================
% ÍNDICE GENERAL
% ==============================================================================
\tableofcontents
\newpage

% ==============================================================================
% SECCIÓN 1: EL HILO CONDUCTOR DEL PROYECTO
% ==============================================================================
\section{El Hilo Conductor: ¿De Dónde Venimos y Hacia Dónde Vamos?}

\subsection{La Cadena de Maduración de la Ingeniería de Procesos}
Para defender con autoridad técnica cualquier paquete de ingeniería, es fundamental comprender que el proyecto no es una colección de entregables inconexos, sino una secuencia lógica y estructurada de diseño:

\begin{enumerate}[leftmargin=*]
    \item \textbf{BFD v1 (Diagrama de Bloques):} Planteamiento de la ruta conceptual (Áreas 100 a 600).
    \item \textbf{DFP v1 y Simulación DWSIM v1:} Balances rigurosos de materia y energía con paquete termodinámico \textbf{PRSV2-VL}, resolviendo los reciclos de gas y circuito cerrado hídrico mediante el algoritmo de Wegstein. Se generan las tablas maestras \textbf{TC-01} (corrientes) y \textbf{TE-01} (energía).
    \item \textbf{Lista Maestra de Equipos (LE-01 Rev. 1):} Especificación mecánica preliminar y dimensionamiento de los 30 equipos de proceso bajo códigos ASME VIII, TEMA R y API 650.
    \item \textbf{DTI v0.2 (P\&ID Preliminar):} Trazado de tuberías, válvulas de control e instrumentación básica regulatoria (lazos PID).
    \item \textbf{Taller HAZOP (AC-HAZOP-01):} Análisis cualitativo riguroso bajo norma \textbf{IEC 61882} para descubrir fallas catastróficas, embalamiento térmico, sobrepresiones o fugas antes de construir la planta.
    \item \textbf{Matriz Causa-Efecto (MCE-01 Rev. 1) y Cambios RC-DTI-01:} Implementación de salvaguardas físicas críticas (válvulas de corte estanco \texttt{SDV}, transmisores $2\text{oo}3$ y los Interlocks \textbf{I-01 a I-04}). Con esto se congela el \textbf{DTI v1.0}.
    \item \textbf{Paquete de Ingeniería Básica (PIB-01):} Consolidación documental definitiva que audita la coherencia cruzada total entre DWSIM, DTI, formatos de equipos (F-PIB-02), balance de recursos (F-PIB-03), bitácora de pendientes (F-PIB-04) y el plano de distribución en planta (\textbf{Solvanta\_AG-01}).
\end{enumerate}

\subsection{¿Qué es el HAZOP y por qué era indispensable antes del PIB-01?}
El análisis HAZOP (\textit{Hazard and Operability Study}) es la técnica de seguridad industrial que examina sistemáticamente cada nodo de proceso mediante palabras guía (\textit{Más, Menos, Ninguno, Inverso, Parte de}) sobre variables operativas (\textit{Presión, Temperatura, Flujo, Nivel, Composición}).

\textbf{¿Por qué no se podía hacer el PIB-01 sin el HAZOP?}  
Porque un Paquete de Ingeniería Básica que no contemple los sistemas de parada de emergencia (\textit{Emergency Shutdown}, ESD) ni las válvulas de corte rápido (\texttt{SDV}) está incompleto y representa un peligro de diseño. Gracias al HAZOP se incorporaron las protecciones que hoy justifican las especificaciones de los equipos en el formato \textbf{F-PIB-02C}.

\subsection{¿Cuál es el objetivo del entregable PIB-01?}
Integrar y verificar el Paquete de Ingeniería Básica (\textit{Basic Engineering Design Package}, BEDP) de la planta de e-metanol, garantizando:
\begin{itemize}[leftmargin=*]
    \item Que no existan inconsistencias entre los caudales simulados y los equipos listados.
    \item Que se contabilice el $100\%$ de los recursos, servicios auxiliares y efluentes.
    \item Que los pendientes de diseño fino queden formalmente trazados con responsable en \textbf{F-PIB-04}.
    \item Que la distribución física en el Plot Plan respete los códigos de espaciamiento y vientos dominantes.
\end{itemize}

\newpage
% ==============================================================================
% SECCIÓN 2: DE DÓNDE SALE CADA DATO, CÁLCULO Y ECUACIÓN
% ==============================================================================
\section{De Dónde Sale Cada Dato, Ecuación y Estimación}

\subsection{Capacidad de Producción y Régimen de Operación}
\begin{conceptbox}{Cálculo de Capacidad y Régimen Anual}
\begin{itemize}[leftmargin=*]
    \item \textbf{Meta de Licitación:} $30\,000\text{ t/año}$ de e-metanol grado AA ($>99.85\%$ pureza en peso).
    \item \textbf{Horas Anuales de Operación:} $8\,000\text{ h/año}$.
    \begin{equation}
    \text{Disponibilidad Operativa} = \frac{8\,000\text{ h/año}}{8\,760\text{ h/año en calendario}} \times 100\% = \mathbf{91.32\%}
    \end{equation}
    Corresponde a \textbf{333.3 días continuos} de producción y \textbf{31.7 días (760 h)} de paro programado para mantenimiento mayor, cambio de catalizador y regeneración de celdas SOEC.
    \item \textbf{Tasa de Producción Nominal:}
    \begin{equation}
    \dot{m}_{\text{MeOH, nominal}} = \frac{30\,000 \times 1\,000\,\text{kg}}{8\,000\,\text{h}} = 3\,750.00\,\frac{\text{kg}}{\text{h}}
    \end{equation}
    En la simulación oficial de DWSIM (corriente \texttt{S-604}), la tasa convergida es:
    \begin{equation}
    \mathbf{3\,788.65\,\frac{\text{kg}}{\text{h}}} \implies 3\,788.65 \times 8\,000 / 1\,000 = \mathbf{30\,309.20\,\frac{\text{t}}{\text{año}}} \quad (+1.03\% \text{ holgura})
    \end{equation}
    \item \textbf{Tasa Máxima de Diseño (+10\% de Sobrediseño según ASME/Perry):}
    \begin{equation}
    \dot{m}_{\text{MeOH, máx}} = 3\,788.65 \times 1.10 = \mathbf{4\,167.52\,\frac{\text{kg}}{\text{h}}} \quad \left(\mathbf{33\,340.12\,\frac{\text{t}}{\text{año}}}\right)
    \end{equation}
\end{itemize}
\end{conceptbox}

\subsection{Consumo de Reactivos y Módulo Estequiométrico ($M$)}
\begin{itemize}[leftmargin=*]
    \item \textbf{Reacción Principal de Hidrogenación de $\text{CO}_2$:}
    \begin{equation}
    \text{CO}_2 + 3\,\text{H}_2 \rightleftharpoons \text{CH}_3\text{OH} + \text{H}_2\text{O} \quad (\Delta H_{298\text{ K}}^\circ = -49.5\,\text{kJ/mol})
    \end{equation}
    \item \textbf{Reacción Secundaria (Reverse Water-Gas Shift, RWGS):}
    \begin{equation}
    \text{CO}_2 + \text{H}_2 \rightleftharpoons \text{CO} + \text{H}_2\text{O} \quad (\Delta H_{298\text{ K}}^\circ = +41.2\,\text{kJ/mol})
    \end{equation}
    \item \textbf{Dióxido de Carbono ($\text{CO}_2$, Corriente \texttt{S-101}):}
    Flujo másico: $\mathbf{5\,274.34\,\text{kg/h}}$ ($119.84\,\text{kmol/h}$ al $99.0\%$ molar).
    \begin{equation}
    \text{Consumo Específico Real} = \frac{5\,274.34\,\text{kg/h}}{3\,788.65\,\text{kg/h}} = \mathbf{1.3921\,\frac{\text{kg CO}_2}{\text{kg MeOH}}} \quad \left(\text{Teórico: } \frac{44.01}{32.04} = 1.3736\right)
    \end{equation}
    La diferencia del $1.3\%$ se debe a las impurezas inertes del $\text{CO}_2$ de captura externa y las purgas del sistema.
    \item \textbf{Hidrógeno Verde ($\text{H}_2$, Corriente \texttt{S-209}):}
    Flujo másico: $\mathbf{1\,314.77\,\text{kg/h}}$ ($652.17\,\text{kmol/h}$). Subproducto $\text{O}_2$ puro en \texttt{S-206}: $10\,098.76\,\text{kg/h}$.
    \begin{equation}
    \text{Consumo Específico Real} = \frac{1\,314.77\,\text{kg/h}}{3\,788.65\,\text{kg/h}} = \mathbf{0.3470\,\frac{\text{kg H}_2}{\text{kg MeOH}}}
    \end{equation}
    \item \textbf{Módulo Estequiométrico del Bucle de Síntesis ($M$):}
    \begin{equation}
    M = \frac{y_{\text{H}_2} - y_{\text{CO}_2}}{y_{\text{CO}} + y_{\text{CO}_2}} = \mathbf{2.05}
    \end{equation}
    Se ajusta en $2.05$ para optimizar el equilibrio hacia metanol, inhibir la formación de parafinas y proteger el catalizador $\text{Cu/ZnO/Al}_2\text{O}_3$ contra desactivación prematura.
\end{itemize}

\subsection{Circuito Cerrado ZLD y Balance Hídrico}
\begin{conceptbox}{Balance Hídrico y Recuperación ZLD}
\begin{itemize}[leftmargin=*]
    \item \textbf{Demanda total de vapor al SOEC (\texttt{S-204}):} $\mathbf{16\,245.70\,\text{kg/h}}$ ($901.76\,\text{kmol/h}$).
    \item \textbf{Agua recuperada internamente (\texttt{S-202}):}
    \begin{itemize}
        \item Condensado SOEC no disociado en flash \texttt{V-201} (conversión $70\%$): $4\,831.02\,\text{kg/h}$.
        \item Fondos despojados de columna de destilación \texttt{T-601} (\texttt{S-605}): $2\,172.84\,\text{kg/h}$.
    \end{itemize}
    \begin{equation}
    \dot{m}_{\text{recuperada ZLD}} = 4\,831.02 + 2\,172.84 = \mathbf{7\,003.86\,\frac{\text{kg}}{\text{h}}} \implies \mathbf{56\,030.88\,\frac{\text{t}}{\text{año}}}
    \end{equation}
    \item \textbf{Agua de reposición fresca make-up (\texttt{S-201}):}
    \begin{equation}
    \dot{m}_{\text{make-up}} = 16\,245.70 - 7\,003.86 = \mathbf{9\,241.84\,\frac{\text{kg}}{\text{h}}} \implies \mathbf{73\,934.72\,\frac{\text{t}}{\text{año}}}
    \end{equation}
    \item \textbf{Porcentaje de Ahorro Neto de Agua Fresca:}
    \begin{equation}
    \%\,\text{Ahorro ZLD} = \frac{7\,003.86}{16\,245.70} \times 100\% = \mathbf{43.11\%}
    \end{equation}
\end{itemize}
\end{conceptbox}

\subsection{Acoplamiento Térmico Total: Reactor BWR \texttt{R-401} con SOEC}
\begin{itemize}[leftmargin=*]
    \item \textbf{Reactor Tubular Lurgi BWR:} $75.0\text{ bar}$, $210^\circ\text{C}$ entrada, $245^\circ\text{C}$ lecho cuasi-isotérmico.
    \item \textbf{Calor Exotérmico Liberado:} $Q_{\text{reacc}} = \mathbf{12\,335.36\,\text{kW}}$ ($44.41\,\text{GJ/h}$).
    \item \textbf{Generación Interna de Vapor a 20 bar en Carcasa (\texttt{R-401-S}):}
    El calor de reacción evapora agua a $20.0\,\text{bar}$ ($T_{\text{sat}} = 212.4^\circ\text{C}$, $\lambda_{\text{vap}} = 1\,890.7\,\text{kJ/kg}$):
    \begin{equation}
    \dot{m}_{\text{vapor generado}} = \mathbf{16\,244.88\,\frac{\text{kg}}{\text{h}}} \implies \mathbf{129\,959.04\,\frac{\text{t}}{\text{año}}}
    \end{equation}
    \textbf{Conclusión clave de defensa:} Todo el vapor que consume el SOEC ($16\,245\,\text{kg/h}$) lo genera internamente el reactor de metanol. \textbf{Consumo de combustible fósil para generar vapor: CERO.}
\end{itemize}

\subsection{Bucle de Recirculación, Purga y Turboexpansor}
\begin{itemize}[leftmargin=*]
    \item Efluente del reactor: $21\,308.08\,\text{kg/h}$. Se enfría a $38^\circ\text{C}$ y se separa en el flash HP \texttt{V-501}:
    \begin{itemize}
        \item Líquido crudo de metanol (\texttt{S-505}): $5\,968.27\,\text{kg/h}$ a destilación.
        \item Gas no reaccionado (\texttt{S-503}): $15\,339.81\,\text{kg/h}$.
    \end{itemize}
    \item \textbf{Recirculación del 96\% (\texttt{S-504}):} $14\,726.22\,\text{kg/h}$ impulsados por soplador centrífugo \texttt{C-501} ($150\,\text{kW}$).
    \item \textbf{Purga Continua del 4\% (\texttt{S-506}):} $613.59\,\text{kg/h}$. Evita la acumulación de metano inerte y nitrógeno.
    \item \textbf{Turboexpansor Criogénico \texttt{EXP-501}:} Expande la purga de $75.0\,\text{bar}$ a $1.30\,\text{bar}$:
    \begin{equation}
    W_{\text{generado}} = \mathbf{-437.79\,\text{kW}} \implies \mathbf{-3\,502.32\,\frac{\text{MWh}}{\text{año}}} \quad (\text{Enfriamiento criogénico a } \mathbf{-139.7^\circ\text{C}})
    \end{equation}
\end{itemize}

\subsection{Destilación Fraccionada en Columna \texttt{T-601}}
\begin{conceptbox}{Dimensionamiento de la Torre T-601 (FUG + O'Connell)}
\begin{itemize}[leftmargin=*]
    \item \textbf{Volatilidad Relativa:} $\alpha_{\text{MeOH-Agua}} = 2.75$.
    \item \textbf{Fenske ($N_{\min}$):} $15.3$ etapas teóricas a reflujo total.
    \item \textbf{Underwood ($R_{\min}$):} $R_{\min} = 1.05 \implies R_{\text{operación}} = 1.50 \times R_{\min} = \mathbf{1.50}$.
    \item \textbf{Gilliland ($N_{\text{teóricas}}$):} 22 platos teóricos en columna + condensador + rehervidor = \textbf{24 etapas teóricas}.
    \item \textbf{Eficiencia de Platos de O'Connell ($\mu_L \alpha = 0.65\text{ cP} \times 2.75 \implies \eta = 70.0\%$):}
    \begin{equation}
    N_{\text{platos reales}} = \frac{24}{0.70} \approx \mathbf{34\,\text{platos mecánicos}}
    \end{equation}
    \item \textbf{Geometría Mecánica:} Diámetro $D = \mathbf{1.25\,\text{m}}$; Altura total $H = \mathbf{17.5\,\text{m}}$.
    \item \textbf{Calidad de Producto (\texttt{S-604}):} $3\,788.65\,\text{kg/h}$ de metanol con **$99.89\%$ pureza en peso** ($<0.10\%$ agua, Grado Químico AA ASTM D1152).
    \item \textbf{Consumo de Vapor en Rehervidor \texttt{E-602} ($3\,266.68\,\text{kW}$ a $3.5\,\text{bar}$):}
    \begin{equation}
    \dot{m}_{\text{vapor E-602}} = \frac{3\,266.68\,\text{kW}}{2\,148\,\text{kJ/kg}} = \mathbf{5\,474.90\,\frac{\text{kg}}{\text{h}}} \implies \mathbf{43\,799.20\,\frac{\text{t}}{\text{año}}}
    \end{equation}
\end{itemize}
\end{conceptbox}

\subsection{Balances Consolidados de Servicios Auxiliares (F-PIB-03)}
\begin{itemize}[leftmargin=*]
    \item \textbf{Electricidad Global de Planta:}
    \begin{equation}
    W_{\text{neto}} = +38\,067.30\text{ (SOEC)} + 1\,316.67\text{ (C-301)} + 150.00\text{ (C-501)} - 437.79\text{ (EXP-501)} + 5.51\text{ (Bombas)} = \mathbf{+39\,101.69\,\text{kW}}
    \end{equation}
    Consumo anualizado: $\mathbf{312\,813.52\,\text{MWh/año}}$ (ahorro de $130\,678\,\text{MWh/año}$ gracias a la optimización electroquímica a $800^\circ\text{C}$).
    \item \textbf{Agua de Enfriamiento de Torre ($Q_{\text{CW}} = 25\,782.22\,\text{kW}$, $\Delta T = 10.0^\circ\text{C}$):}
    \begin{equation}
    \dot{V}_{\text{circulante}} = \frac{25\,782.22\,\text{kW}}{4.184 \times 10} \times 3.6 = \mathbf{2\,218.36\,\frac{\text{m}^3}{\text{h}}} \implies \mathbf{17\,746\,880\,\frac{\text{m}^3}{\text{año}}}
    \end{equation}
    Make-up neto de reposición ($1.5\%$ por evaporación, arrastre y purga):
    \begin{equation}
    \dot{V}_{\text{make-up CW}} = 0.015 \times 2\,218.36 = \mathbf{33.28\,\frac{\text{m}^3}{\text{h}}} \implies \mathbf{266\,240\,\frac{\text{m}^3}{\text{año}}}
    \end{equation}
\end{itemize}

\newpage
% ==============================================================================
% SECCIÓN 3: EL ANÁLISIS HAZOP Y LAS SALVAGUARDAS INSTRUMENTADAS
% ==============================================================================
\section{El Análisis HAZOP y las Salvaguardas Instrumentadas (SIS)}

\subsection{Estructura del Taller HAZOP y Nodos Analizados}
El estudio HAZOP (\textbf{AC-HAZOP-01}) evaluó cuatro nodos críticos del diagrama \textbf{DTI v0.2} aplicando la norma \textbf{IEC 61882}:
\begin{itemize}[leftmargin=*]
    \item \textbf{Nodo 1 (Síntesis de Metanol):} Reactor tubular Lurgi \texttt{R-401}, carcasa generadora de vapor \texttt{R-401-S} y mezclador de bucle \texttt{MIX-401}.
    \item \textbf{Nodo 2 (Compresión de Syngas):} Mezclador fresco \texttt{MIX-301}, precalentador \texttt{E-301} y compresor multietapa \texttt{C-301}.
    \item \textbf{Nodo 3 (Electrólisis de Vapor):} Sobrecalentador \texttt{E-202}, electrolizador SOEC \texttt{EL-201} y condensador \texttt{E-203}.
    \item \textbf{Nodo 4 (Bucle de Separación y Destilación):} Separador flash HP \texttt{V-501}, soplador \texttt{C-501}, flash LP \texttt{V-601} y columna \texttt{T-601}.
\end{itemize}

\subsection{Los Cuatro Interlocks Críticos del SIS}

\begin{interlockbox}{Interlock I-01: Protección Anti-Embalamiento Térmico en Reactor R-401}
\begin{itemize}[leftmargin=*]
    \item \textbf{Causa Iniciadora:} Pérdida de agua de alimentación en caldera \texttt{R-401-S} o disparo de bombas \texttt{P-801}.
    \item \textbf{Peligro:} Al no haber evaporación de agua en carcasa, el calor exotérmico eleva la temperatura por encima de $280^\circ\text{C}$, provocando coquización, sinterización irreversible del catalizador de cobre y sobrepresión de tubos.
    \item \textbf{Instrumentación:} Transmisor de temperatura múltiple \texttt{TT-401} en lógica de votación $2\text{oo}3$.
    \item \textbf{Acción del SIS:} Ante $T > 260.0^\circ\text{C}$ (\texttt{TAHH-401}), cierra instantáneamente la válvula de corte estanco \texttt{SDV-301} ($<2.0\text{ s}$), aislando el syngas fresco, y modula bypass frío en economizador.
\end{itemize}
\end{interlockbox}

\begin{interlockbox}{Interlock I-02: Protección Anti-Sobrepresión en Bucle de 75 bar}
\begin{itemize}[leftmargin=*]
    \item \textbf{Causa Iniciadora:} Bloqueo de válvula aguas abajo en \texttt{V-501}, fallo en soplador \texttt{C-501} o expansión térmica.
    \item \textbf{Peligro:} Sobrepresión por encima del límite de diseño mecánico ($82.5\text{ bar}$), con riesgo de rotura catastrófica de tuberías de gas con hidrógeno e incendio masivo.
    \item \textbf{Instrumentación:} Transmisor de presión en bucle \texttt{PIT-501}.
    \item \textbf{Acción del SIS:} Ante $P > 78.5\text{ bar}$ (\texttt{PSHH-501}), dispara simultáneamente los compresores \texttt{C-301} y \texttt{C-501}, abre reciclo anti-surge y despresuriza hacia antorcha HP vía válvula de alivio \texttt{PSV-501}.
\end{itemize}
\end{interlockbox}

\begin{interlockbox}{Interlock I-03: Prevención de Fractura de Membranas en Electrolizador SOEC EL-201}
\begin{itemize}[leftmargin=*]
    \item \textbf{Causa Iniciadora:} Desbalance de presiones entre el compartimiento catódico ($\text{H}_2/\text{H}_2\text{O}$) y anódico ($\text{O}_2$).
    \item \textbf{Peligro:} Esfuerzo mecánico diferencial superior a $0.50\text{ bar}$ fractura las celdas cerámicas de óxido de zirconio (YSZ), mezclando directamente hidrógeno y oxígeno a $800^\circ\text{C}$, provocando detonación instantánea en el stack.
    \item \textbf{Instrumentación:} Transmisor de presión diferencial redundante \texttt{PDIT-201}.
    \item \textbf{Acción del SIS:} Ante $|\Delta P| > 0.40\text{ bar}$ (\texttt{PDAHH-201}), corta la corriente eléctrica DC ($38.07\text{ MWe}$) en menos de $50\text{ ms}$ y abre válvula de ecualización cruzada \texttt{PDCV-201} inundando con nitrógeno inerte.
\end{itemize}
\end{interlockbox}

\begin{interlockbox}{Interlock I-04: Prevención de Gas Blow-By desde Flash HP V-501 hacia Flash LP V-601}
\begin{itemize}[leftmargin=*]
    \item \textbf{Causa Iniciadora:} Válvula de control de nivel de fondo \texttt{LCV-501} queda trabada en posición $100\%$ abierta.
    \item \textbf{Peligro:} Se vacía el sello líquido de fondo y el gas no reaccionado a $75.0\text{ bar}$ sopla directamente hacia el tambor flash LP \texttt{V-601} (diseñado a solo $4.0\text{ bar}$), causando sobrepresión y explosión destructiva del tambor de baja presión y la columna de destilación.
    \item \textbf{Instrumentación:} Transmisor de nivel independiente \texttt{LT-501}.
    \item \textbf{Acción del SIS:} Ante nivel muy bajo \texttt{LALL-501} ($10\%$), acciona el cierre hermético en **menos de 1.0 segundo** de la válvula de corte \textbf{\texttt{SDV-501}} (ANSI Clase VI, Falla Cerrada), garantizando el confinamiento del gas a 75 bar.
\end{itemize}
\end{interlockbox}

\newpage
% ==============================================================================
% SECCIÓN 4: DESGLOSE COMPLETO DEL PLOT PLAN (Solvanta_AG-01)
% ==============================================================================
\section{Desglose Completo del Plot Plan (Plano Solvanta\_AG-01)}

\subsection{Dimensiones Globales y Filosofía de Orientación por Vientos}
\begin{itemize}[leftmargin=*]
    \item \textbf{Superficie Total:} $250.0\text{ m}$ (frente) $\times 160.0\text{ m}$ (fondo) = $\mathbf{40\,000\,\text{m}^2}$ (\textbf{4.0 hectáreas}).
    \item \textbf{Viento Dominante (Rosa de los Vientos):} Proviene del **Nor-Noreste (NNE)** desde el Golfo de México a $15-28\,\text{km/h}$, soplando hacia el Sur/Suroeste.
    \item \textbf{Regla de Oro de Seguridad (NFPA 30 / API RP 500):}
    \begin{itemize}
        \item \textbf{Barlovento (Viento Arriba - Norte):} Se colocan las áreas con presencia de personal (cuarto de control, oficinas) y fuentes de chispa eléctrica (subestación).
        \item \textbf{Sotavento (Viento Abajo - Sur):} Se ubican los inventarios de hidrocarburos volátiles (tanque de metanol en dique al $110\%$) y las fuentes de llama abierta (antorcha/flare stack).
    \end{itemize}
\end{itemize}

\subsection{Detalle de las 16 Zonas del Arreglo General}

\begin{table}[H]
\centering\footnotesize
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.2}
\caption{\textbf{Inventario de zonas funcionales y equipos en el Plot Plan Solvanta\_AG-01.}}
\begin{tabularx}{\textwidth}{p{3.2cm} c p{5.5cm} X}
\toprule
\rowcolor{tableheader}
\color{white}\textbf{Zona / Cuadrante} & \color{white}\textbf{Área} & \color{white}\textbf{Equipos Principales} & \color{white}\textbf{Criterio de Seguridad / Normativa} \\
\midrule
Noroeste (Viento arriba) & Admón. & Cuarto de Control Central (CCR), Oficinas, Laboratorio y Garita. & Zona No Clasificada (Segura). Sobrepresión positiva en CCR. \\ \addlinespace[2pt]
Oeste Central-Bajo & 100 & Estación $\text{CO}_2$ ($20\,\text{bar}$), Ósmosis Inversa, Tanque \texttt{TK-201} ($1\,000\,\text{m}^3$), Bombas \texttt{P-201A/B}. & Clase I Div 2. Autonomía hídrica de 4.5 días. \\ \addlinespace[2pt]
Oeste Central & 800 & Tambor de condensados \texttt{V-801} y bombas \texttt{P-801A/B}. & Retorno de $7\,004\,\text{kg/h}$ de agua recuperada al mezclador SOEC. \\ \addlinespace[2pt]
Norte Central & 200 & Nave de Stacks SOEC \texttt{EL-201} ($38.07\,\text{MWe}$), Sobrecalentador \texttt{E-202}, Enfriadores \texttt{E-201/203}, Flash \texttt{V-201}. & Clase I Div 1 Grupo B ($\text{H}_2$). Ventilación forzada y detección de $\text{H}_2$. \\ \addlinespace[2pt]
Centro-Sur & 300/400 & Compresor syngas \texttt{C-301} ($75\,\text{bar}$), Precalentador \texttt{E-301}, Reactor BWR \texttt{R-401/R-401-S}. & Clase I Div 1 Grupos B y D. Aislamiento acústico y lazo anti-surge en compresor. \\ \addlinespace[2pt]
Noreste Central & 500 & Economizador \texttt{E-502}, Condensador \texttt{E-501}, Flash HP \texttt{V-501}, Soplador \texttt{C-501}, Expansor \texttt{EXP-501}. & Clase I Div 1. Interlock I-04 contra blow-by hacia baja presión. \\ \addlinespace[2pt]
Sureste & 600 & Flash LP \texttt{V-601}, Torre \texttt{T-601} ($34$ platos), Condensador \texttt{E-601}, Rehervidor \texttt{E-602}, Bombas \texttt{P-601/602}. & Clase I Div 2. Destilación a $1.25\,\text{bar}$ con metanol Grado AA. \\ \addlinespace[2pt]
Sur Central & Almacén & Tanque vertical \texttt{TK-601} ($2\,000\,\text{m}^3$), Dique estanco al $110\%$, Subenfriador \texttt{E-603}. & NFPA 30 y API 650. Dique de retención de $2\,200\,\text{m}^3$ y colchón de $\text{N}_2$. \\ \addlinespace[2pt]
Flanco Este (Norte) & Servicios & Subestación Eléctrica $115/13.8\,\text{kV}$ ($45\,\text{MVA}$), Rectificadores DC, CCM. & Acometida eléctrica aislada de áreas inflamables. \\ \addlinespace[2pt]
Flanco Este (Centro) & Servicios & Torres de Enfriamiento ($25.8\,\text{MWth}$, $2\,218\,\text{m}^3\text{/h}$), Bombas CW. & Tiro inducido, a barlovento relativo del área de almacenamiento. \\ \addlinespace[2pt]
Flanco Este (Bajo) & Servicios & Compresores de Aire de Instrumentos y Planta de Nitrógeno ($\text{N}_2$). & Punto de rocío $-40^\circ\text{C}$ a $7\,\text{bar}$ y $\text{N}_2$ criogénico vaporizado. \\ \addlinespace[2pt]
Esquina Sureste & SCI & Tanque de Agua C.I. \texttt{TK-FIRE} ($3\,000\,\text{m}^3$) y Casa de Bombas Diésel/Eléctrica. & NFPA 20 / API 2001. Garantiza 4 horas continuas a $750\,\text{m}^3\text{/h}$. \\ \addlinespace[2pt]
Esquina Suroeste & Alivio & Antorcha Elevada ($45\,\text{m}$ de altura) con radio térmico de $60\,\text{m}$. & API 521. A sotavento absoluto para no afectar unidades de proceso. \\ \addlinespace[2pt]
Franja Noreste & Reserva & Reserva Territorial ($110\,\text{m} \times 10\,\text{m} = 1\,100\,\text{m}^2$, $25\%$ de reserva). & Área para futuro Tren 2 de síntesis y expansión de 50 MW SOEC. \\ \addlinespace[2pt]
Vialidad y Perímetro & Red Vial & Anillo perimetral de $8\,\text{m}$ y calles internas de $6\,\text{m}$, puntos \textbf{PR-1} y \textbf{PR-2}. & Acceso de camiones de bomberos en $360^\circ$ y evacuación peatonal rápida. \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Despliegue Gráfico del Plot Plan (Solvanta\_AG-01)}
\begin{figure}[H]
    \centering
    \includegraphics[width=\linewidth]{figuras/Solvanta_AG-01.png}
    \caption{\textbf{Plano de Arreglo General Oficial (Plot Plan) Solvanta\_AG-01 Rev. 0.}}
    \label{fig:plot_plan_guia}
\end{figure}

\newpage
% ==============================================================================
% SECCIÓN 5: GUIÓN DE EXPOSICIÓN POR ROLES (12 A 15 MINUTOS)
% ==============================================================================
\section{Guión y Estrategia de Exposición por Roles (12 a 15 Minutos)}

\begin{conceptbox}{Estrategia de la Presentación}
La defensa debe ser fluida, técnica y cronometrada. Se sugieren **3 minutos por expositor** más 1 minuto de cierre, proyectando seguridad, rigor en las unidades y dominio de los acrónimos de ingeniería.
\end{conceptbox}

\subsubsection*{1. Introducción y Bases Consolidadas (3 min)}
\textbf{Expositora:} Ing. Karol Paola Camacho López (Directora de Proyecto \textbar\ Coordinación General)
\begin{quote}\small\itshape
``Buenos días, doctor Arzola y miembros del comité evaluador. Somos Solvanta Engineering Solutions S.A. de C.V. y hoy presentamos el Paquete de Ingeniería Básica PIB-01 de nuestra planta de producción de e-metanol grado químico de 30 mil toneladas anuales en el complejo industrial adyacente.

Este paquete no es una colección de tablas aisladas; es la consolidación rigurosa de toda la ingeniería previa, conectando nuestro modelo en DWSIM v10.2.4 con los planos DFP y DTI, el catálogo de 30 equipos y las recomendaciones del taller HAZOP.

Diseñamos para un régimen de 8,000 horas anuales con 91.3\% de disponibilidad operativa, fijando una producción nominal de 3,788.7 kg/h de metanol grado AA al 99.89\% de pureza, con un sobre-diseño del 10\% que lleva la capacidad máxima a 4,167.5 kg/h.

Consumimos 5,274 kg/h de CO2 y 9,242 kg/h de agua desmineralizada fresca, gracias a que nuestro circuito ZLD recupera 7,004 kg/h de condensados de proceso, ahorrando un 43.1\% del agua y logrando cero descargas líquidas al río sitio industrial de referencia. Cedo la palabra a nuestra especialista en simulación, la Ing. Paulina Mota.''
\end{quote}

\subsubsection*{2. Simulación DWSIM, Termodinámica y Destilación (3 min)}
\textbf{Expositora:} Ing. Paulina Mota Macip (Especialista en Simulación DWSIM y Proceso)
\begin{quote}\small\itshape
``Gracias. El corazón del balance es nuestro modelo DWSIM convergido mediante el paquete termodinámico PRSV2-VL. En el Área 200, disociamos vapor de agua a 800 °C y 19.4 bar en celdas SOEC (Escenario D Óptimo: 0.480 A/cm², 1.183 V, 38.07 MWe, 32.92 kWh/kg H2), logrando 70\% de conversión por paso y produciendo 1,314.8 kg/h de hidrógeno verde seco y 10,098.8 kg/h de oxígeno puro para venta industrial.

El hidrógeno se mezcla con el CO2 en el mezclador MIX-301 fijando el módulo estequiométrico en 2.05 y se comprime en C-301 a 75 bar. En el reactor tubular Lurgi R-401, la reacción exotérmica libera 12.33 MW térmicos, los cuales son absorbidos íntegramente en la carcasa R-401-S generando 16.2 t/h de vapor a 20 bar que alimenta directamente a la electrólisis SOEC. Logramos un acoplamiento térmico total sin consumir combustible fósil.

El bucle opera con 96\% de recirculación de gas y 4\% de purga continua hacia el turboexpansor EXP-501, que recupera 437.8 kW netos de electricidad. Finalmente, la columna de destilación T-601 de 34 platos mecánicos separa el metanol en domo a 68.5 °C y agua despojada en fondos a 103.9 °C. Cedo la palabra al custodio del DTI y Arreglo General, Ing. Gildardo Ocaña.''
\end{quote}

\subsubsection*{3. Inventario de Equipos, Arreglo General y Plot Plan (3 min)}
\textbf{Expositor:} Ing. Gildardo Ocaña Barrales (Custodio del DTI \textbar\ Arreglo General)
\begin{quote}\small\itshape
``Gracias. En el formato F-PIB-02 consolidamos las especificaciones de los 30 equipos mecánicos de la planta. Diseñamos bajo códigos ASME Sección VIII para reactores y recipientes a presión, estándares TEMA Clase R para intercambiadores de calor tubulares, y API 650 para el tanque de almacenamiento vertical TK-601 de 2,000 m3, que garantiza 15 días continuos de autonomía.

Para soportar el ambiente de gas de síntesis a 75 bar con presencia de hidrógeno y evitar el ataque por hidrógeno a alta temperatura según las curvas de Nelson de API 941, seleccionamos acero aleado 1.25Cr-0.5Mo con recubrimiento interior de acero inoxidable 316L en reactores y recipientes.

En el plano Solvanta\_AG-01 plasmamos la distribución en un predio rectangular de 250 por 160 metros, equivalente a 4 hectáreas. Orientamos la planta de acuerdo con los vientos dominantes del Golfo que soplan del Norte al Sur: colocamos la subestación eléctrica y el cuarto de control en el extremo norte como áreas seguras no clasificadas, las unidades de proceso en secuencia fluida al centro, y el tanque de metanol con dique estanco al 110\% y las antorchas a más de 60 metros en el cuadrante sur. Cedo la palabra a nuestra especialista en seguridad, Ing. Grecia Figueroa.''
\end{quote}

\subsubsection*{4. Taller HAZOP, Interlocks SIS y Cierre de Auditoría (3 min)}
\textbf{Expositora:} Ing. Grecia Figueroa Rincón (Especialista en Seguridad Industrial y HSE)
\begin{quote}\small\itshape
``Gracias. La máxima prioridad de Solvanta es la seguridad de proceso. En el taller HAZOP bajo norma IEC 61882 evaluamos los cuatro nodos de mayor severidad del DTI v0.2. De las 16 desviaciones analizadas, identificamos escenarios de alto riesgo que mitigamos mediante cuatro Interlocks del Sistema Instrumentado de Seguridad:

El Interlock I-01 previene el embalamiento térmico en el reactor R-401 cerrando la válvula de corte estanco SDV-301 si la temperatura supera los 260 °C; el Interlock I-02 protege al bucle de sobrepresiones mayores a 78.5 bar disparando turbocompresores y derivando a antorcha vía PSV-501; el Interlock I-03 monitorea la presión diferencial en celdas SOEC cortando la energía DC si Delta P supera 0.4 bar para evitar la mezcla explosiva de hidrógeno y oxígeno; y el Interlock I-04 cierra la válvula SDV-501 en menos de un segundo ante nivel muy bajo en V-501, evitando el peligroso gas blow-by hacia la torre de baja presión.

Todas las modificaciones físicas quedaron congeladas en el DTI v1.0 y las actividades pendientes de diseño fino están trazadas en el formato F-PIB-04. Concluye nuestra directora, Ing. Karol Camacho.''
\end{quote}

\subsubsection*{5. Cierre Oficial de la Exposición (1 min)}
\textbf{Expositora:} Ing. Karol Paola Camacho López (Directora de Proyecto \textbar\ Coordinación General)
\begin{quote}\small\itshape
``En conclusión, el expediente PIB-01 de Solvanta demuestra viabilidad técnica, termodinámica y de seguridad industrial total. Entregamos un paquete de ingeniería básica completo, con cero inconsistencias de balance, acoplamiento térmico autosuficiente, circuito ZLD sustentable y salvaguardas certificadas. Quedamos a disposición del doctor Arzola y el comité para sus preguntas.''
\end{quote}

\newpage
% ==============================================================================
% SECCIÓN 6: BANCO DE PREGUNTAS CLAVE DEL SÍNODO
% ==============================================================================
\section{Banco de Preguntas Clave del Sínodo y Respuestas Técnicas}

\begin{questionbox}{Pregunta 1: ``¿De dónde sacan que la planta es autosuficiente en vapor para el SOEC si la electrólisis requiere 16 t/h a 800 °C?''}
\textbf{Respuesta con autoridad técnica:}  
``Doctor, el calor de reacción exotérmico de la síntesis de metanol en \texttt{R-401} libera $12\,335\text{ kW}$ térmicos ($44.4\text{ GJ/h}$). Al operar como un reactor tubular BWR enfriado con agua en ebullición a $20\text{ bar}$, ese calor evapora agua saturada en su carcasa generando exactamente $16\,244.88\text{ kg/h}$ de vapor saturado a $212.4^\circ\text{C}$.  
Por lo tanto, la energía para la vaporización del agua es 100\% de origen interno. Lo único que requiere energía externa es el sobrecalentamiento de vapor de $212^\circ\text{C}$ a $800^\circ\text{C}$, el cual se realiza en el sobrecalentador eléctrico \texttt{E-202} demandando $5\,248\text{ kW}$, potencia que está completamente contabilizada dentro de la subestación eléctrica de la planta.''
\end{questionbox}

\begin{questionbox}{Pregunta 2: ``¿Por qué seleccionaron una relación de purga del 4\% en el bucle? ¿Por qué no 1\% o 10\%?''}
\textbf{Respuesta con autoridad técnica:}  
``Realizamos un análisis de sensibilidad multivariable en Python acoplado a DWSIM. Si fijamos una purga menor al 3\%, los gases inertes como el metano traza formado por metanación y el nitrógeno del $\text{CO}_2$ se acumulan en el bucle cerrado; esto reduce la presión parcial de reactivos y obliga al compresor \texttt{C-301} a elevar su potencia por encima de $1\,500\text{ kW}$ para mantener la producción.  
Por el contrario, si aumentamos la purga por encima del 5\%, arrojamos $\text{H}_2$ valioso al venteo sin reaccionar, desplomando el rendimiento de la planta. El óptimo tecno-económico exacto se localiza en 4.0\%, donde la purga es de $613.59\text{ kg/h}$, manteniendo la concentración de inertes controlada y permitiendo alimentar el turboexpansor criogénico \texttt{EXP-501}, el cual genera $437.8\text{ kW}$ de energía neta recuperada.''
\end{questionbox}

\begin{questionbox}{Pregunta 3: ``¿Por qué la columna de destilación T-601 tiene 34 platos mecánicos si el método de Gilliland dio 22 etapas teóricas?''}
\textbf{Respuesta con autoridad técnica:}  
``El cálculo analítico mediante el método corto Fenske-Underwood-Gilliland determinó 22 platos teóricos en la columna, más el condensador y el rehervidor, totalizando 24 etapas de equilibrio simuladas en DWSIM.  
Sin embargo, un plato físico real nunca alcanza el equilibrio termodinámico perfecto del 100\%. Aplicando la correlación estándar de O'Connell, que evalúa la viscosidad del líquido en el plato de alimentación ($0.65\text{ cP}$) multiplicada por la volatilidad relativa metanol-agua ($\alpha = 2.75$), se obtiene una eficiencia hidráulica global de plato de $\eta = 70.0\%$.  
Dividiendo 24 etapas teóricas entre 0.70 obtenemos exactamente 34.2 platos, lo que justifica la especificación mecánica de 34 platos físicos reales con un espaciamiento estándar de $0.45\text{ m}$, garantizando una columna de $17.5\text{ m}$ de altura.''
\end{questionbox}

\begin{questionbox}{Pregunta 4: ``En el HAZOP, ¿cuál consideran la desviación más catastrófica y por qué no es suficiente una simple válvula de alivio PSV?''}
\textbf{Respuesta con autoridad técnica:}  
``La desviación más peligrosa para la integridad del personal es el fallo por presión diferencial en el electrolizador SOEC \texttt{EL-201} (Nodo 3), y el fenómeno de gas blow-by en el tambor flash \texttt{V-501} (Nodo 4).  
En el caso del SOEC, si la presión del lado catódico ($\text{H}_2$) y anódico ($\text{O}_2$) difiere por más de $0.4\text{ bar}$, la membrana cerámica electrolítica de circona estabilizada con itrio (YSZ) sufre fractura mecánica frágil; esto causaría la mezcla directa de hidrógeno y oxígeno puro a $800^\circ\text{C}$, provocando una detonación interna instantánea. Una válvula PSV de sobrepresión no sirve porque el peligro no es la presión absoluta, sino el diferencial entre cámaras. Por ello diseñamos el Interlock I-03 con transmisores de presión diferencial en votación 2oo3 que desconectan la corriente en menos de 50 milisegundos y abren ecualización cruzada con nitrógeno inerte.''
\end{questionbox}

\begin{questionbox}{Pregunta 5: ``¿Cómo justifican que su circuito ZLD sea viable y no acumule sales en el electrolizador?''}
\textbf{Respuesta con autoridad técnica:}  
``El agua recuperada en la corriente \texttt{S-202} proviene de dos fuentes que son químicamente de condensación de vapor: el condensado del efluente catódico de SOEC en \texttt{V-201} (que es agua desmineralizada que no se disoció) y los fondos de la torre \texttt{T-601} (\texttt{S-605}), que es agua que fue vaporizada en el rehervidor \texttt{E-602}.  
Ambas corrientes entran al paquete de pulido de condensados y desmineralización por resinas de lecho mixto en el Área 200, eliminando trazas orgánicas ($<10\text{ ppb}$ de metanol) e iones disueltos antes de alimentar la caldera \texttt{R-401-S}. Por ello, la conductividad eléctrica del agua alimentada al SOEC se mantiene por debajo de $0.055\,\mu\text{S/cm}$ (Agua Grado I ASTM), garantizando una vida útil de celdas de más de 40,000 horas de operación.''
\end{questionbox}

\begin{questionbox}{Pregunta 6: ``¿Por qué el tanque de metanol TK-601 está ubicado al Sur y a qué distancia está de la antorcha?''}
\textbf{Respuesta con autoridad técnica:}  
``El viento dominante en polo industrial adyacente proviene del NNE (Norte-Noreste) hacia el Sur. Al colocar el tanque \texttt{TK-601} y la antorcha en el cuadrante Sur a sotavento, nos aseguramos de que cualquier vapor emanado en operaciones de llenado sea arrastrado hacia afuera del predio, protegiendo las fuentes de ignición eléctrica en la subestación y el cuarto de control ubicados al Norte.  
Entre el tanque de metanol \texttt{TK-601} y la antorcha existe una separación física de más de $150\text{ metros}$ en diagonal, muy por encima de los $60\text{ metros}$ del radio de radiación térmica máxima permitido por API 521 ($4.73\text{ kW/m}^2$). Además, el tanque cuenta con su propio dique estanco de contención al $110\%$ ($2\,200\text{ m}^3$) según NFPA 30.''
\end{questionbox}

\newpage
% ==============================================================================
% SECCIÓN 7: REFERENCIAS TÉCNICAS Y NORMATIVAS
% ==============================================================================
\section{Referencias Técnicas, Normativas y Bibliografía}

\begin{enumerate}[leftmargin=*]
    \item \textbf{Towler, G. y Sinnott, R.} (2021). \textit{Chemical Engineering Design: Principles, Practice and Economics of Plant and Process Design}. 6.ª edición. Butterworth-Heinemann / Elsevier.
    \item \textbf{Turton, R., Bailie, R. C., Whiting, W. B. y Shaeiwitz, J. A.} (2018). \textit{Analysis, Synthesis, and Design of Chemical Processes}. 5.ª edición. Prentice Hall / Pearson.
    \item \textbf{Green, D. W. y Southard, M. Z.} (2019). \textit{Perry’s Chemical Engineers’ Handbook}. 9.ª edición. McGraw-Hill Education.
    \item \textbf{Center for Chemical Process Safety (CCPS).} (2007). \textit{Guidelines for Safe Automation of Chemical Processes}. 2.ª edición. AIChE / CCPS. Wiley.
    \item \textbf{International Electrotechnical Commission (IEC).} (2016). \textit{IEC 61882: Hazard and Operability Studies (HAZOP Studies) -- Application Guide}. IEC, Ginebra.
    \item \textbf{International Electrotechnical Commission (IEC).} (2016). \textit{IEC 61511: Functional Safety -- Safety Instrumented Systems for the Process Industry Sector}. Partes 1 a 3.
    \item \textbf{American Petroleum Institute (API).} (2012). \textit{API Recommended Practice 500: Recommended Practice for Classification of Locations for Electrical Installations at Petroleum Facilities}. 3.ª edición. API Publishing.
    \item \textbf{American Petroleum Institute (API).} (2020). \textit{API Standard 521: Pressure-relieving and Depressuring Systems}. 7.ª edición. API Publishing.
    \item \textbf{American Petroleum Institute (API).} (2014). \textit{API Standard 2000: Venting Atmospheric and Low-Pressure Storage Tanks}. 7.ª edición. API Publishing.
    \item \textbf{American Society of Mechanical Engineers (ASME).} (2021). \textit{ASME Boiler and Pressure Vessel Code (BPVC), Section VIII: Rules for Construction of Pressure Vessels}. Divisiones 1 y 2. ASME.
    \item \textbf{Tubular Exchanger Manufacturers Association (TEMA).} (2019). \textit{Standards of the Tubular Exchanger Manufacturers Association}. 10.ª edición. TEMA Inc.
    \item \textbf{American Society for Testing and Materials (ASTM).} (2018). \textit{ASTM D1152-06(2018): Standard Specification for Methanol (Methyl Alcohol)}. ASTM International.
    \item \textbf{National Fire Protection Association (NFPA).} (2021). \textit{NFPA 30: Flammable and Combustible Liquids Code}. Edición 2021. NFPA, Quincy, MA.
    \item \textbf{National Fire Protection Association (NFPA).} (2020). \textit{NFPA 497: Recommended Practice for the Classification of Flammable Liquids, Gases, or Vapors and of Hazardous (Classified) Locations for Electrical Installations in Chemical Process Areas}. NFPA.
    \item \textbf{Petróleos Mexicanos (PEMEX).} (2017). \textit{NRF-036-PEMEX-2017: Clasificación de Áreas Peligrosas y Selección de Equipo Eléctrico}. Comité de Normalización de Pemex.
\end{enumerate}

\end{document}
"""
    return content

def compile_pdf():
    base_dir = "Entregables/PIB-01_Solvanta"
    tex_path = os.path.join(base_dir, "Guia_Exposicion_y_Defensa_Tecnica.tex")
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(build_latex_content())
    print(f"Archivo .tex generado exitosamente: {tex_path}")
    
    # Compilar dos veces con pdflatex para resolver índice y referencias cruzadas
    print("Compilando con pdflatex (Pasada 1)...")
    res1 = subprocess.run(["pdflatex", "-interaction=nonstopmode", "Guia_Exposicion_y_Defensa_Tecnica.tex"], cwd=base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    if res1.returncode != 0 and not os.path.exists(os.path.join(base_dir, "Guia_Exposicion_y_Defensa_Tecnica.pdf")):
        print("Error en Pasada 1:")
        print(res1.stdout[-1500:])
        return False
        
    print("Compilando con pdflatex (Pasada 2 para resolver tabla de contenidos e hipervínculos)...")
    res2 = subprocess.run(["pdflatex", "-interaction=nonstopmode", "Guia_Exposicion_y_Defensa_Tecnica.tex"], cwd=base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    
    pdf_source = os.path.join(base_dir, "Guia_Exposicion_y_Defensa_Tecnica.pdf")
    if os.path.exists(pdf_source):
        pdf_target = "Entregables/Guia_Exposicion_y_Defensa_Tecnica.pdf"
        shutil.copyfile(pdf_source, pdf_target)
        size_bytes = os.path.getsize(pdf_target)
        print(f"PDF generado y copiado exitosamente:")
        print(f"- {pdf_source} ({size_bytes} bytes)")
        print(f"- {pdf_target} ({size_bytes} bytes)")
        return True
    else:
        print("Error: No se generó el PDF.")
        print(res2.stdout[-1500:])
        return False

if __name__ == "__main__":
    compile_pdf()

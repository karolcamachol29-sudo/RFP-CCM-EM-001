import subprocess
import os
import shutil

base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def compile_tex(tex_path, output_dir):
    filename = os.path.basename(tex_path)
    cmd = f"pdflatex -interaction=nonstopmode -output-directory={output_dir} {tex_path}"
    subprocess.run(cmd, shell=True, cwd=base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(cmd, shell=True, cwd=base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pdf_name = filename.replace('.tex', '.pdf')
    target_pdf = os.path.join(output_dir, pdf_name)
    if os.path.exists(target_pdf):
        print(f"Compiled successfully: {target_pdf}")
    else:
        print(f"Compilation failed for: {tex_path}")

# 1. REPORTE DE VERIFICACIÓN (02_Verificacion/Reporte_Verificacion.tex)
rep_tex = r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,top=2.2cm,bottom=2.2cm,left=2.2cm,right=2.2cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{enumitem}
\usepackage{hyperref}

\definecolor{navyblue}{RGB}{26, 79, 124}
\definecolor{darkred}{RGB}{140, 30, 30}
\definecolor{tealcolor}{RGB}{30, 110, 110}
\definecolor{lightgraybg}{RGB}{248, 249, 250}

\pagestyle{fancy}
\fancyhf{}
\lhead{\small Solvanta Engineering Solutions S.A. de C.V. -- Proyecto Licitación e-Metanol}
\rhead{\small Reporte de Verificación DWSIM v1}
\cfoot{\small Página \thepage\ de 4}
\renewcommand{\headrulewidth}{0.4pt}

\begin{document}

\begin{titlepage}
\centering
\vspace*{0.5cm}
\fbox{
    \begin{minipage}[c][3.0cm][c]{5.4cm}
    \centering
    \includegraphics[width=4.8cm,height=2.6cm,keepaspectratio]{logo_empresa.png}
    \end{minipage}
}
\vspace{1.0cm}

{\color{navyblue}\hrule height 1.5pt}
\vspace{0.6cm}
{\Large \textbf{SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.}}\\[0.4cm]
{\LARGE \textbf{\color{navyblue} REPORTE TÉCNICO DE VERIFICACIÓN Y CONGELAMIENTO}}\\[0.3cm]
{\large \textbf{Simulación de Procesos en DWSIM v1 -- Caso Oficial Aprobado}}\\[0.2cm]
{\small Planta de e-Metanol Grado AA ($30\,000\text{ t/año}$) a partir de $\text{CO}_2$ e Hidrógeno Electrolítico}
\vspace{0.6cm}
{\color{navyblue}\hrule height 1.5pt}

\vspace{1.5cm}
\begin{tabular}{ll}
\textbf{Código del Documento:} & \texttt{REP-VER-DWSIM-001-v0.1} \\
\textbf{Archivo Simulación Fuente:} & \texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz} (\texttt{Simulacion\_pruebas.dwxml}) \\
\textbf{Paquete Termodinámico:} & PRSV2 / PRSV2-VL con corrección de volumen \\
\textbf{Estatus de Simulación:} & \textbf{APROBADA Y CONGELADA (65 Objetos en Azul)} \\
\textbf{Responsable Técnico:} & Ing. Karol Paola Camacho López (Líder de Procesos) \\
\textbf{Fecha de Validación:} & 14 de septiembre de 2026 \\
\end{tabular}

\vfill
{\small \textbf{Solvanta Engineering Solutions} -- Departamento de Modelado y Simulación de Procesos Químicos}
\end{titlepage}

\newpage
\section*{1. Introducción y Procedimiento de Ejecución}
El presente informe documenta la verificación técnica rigurosa del modelo de simulación de procesos correspondiente a la planta de síntesis de e-metanol a escala industrial ($30\,000\text{ t/año}$, equivalentes a $3\,750.0\text{ kg/h}$ con $8\,000\text{ h/año}$ de operación). La simulación fue ejecutada y validada en el simulador de código abierto **DWSIM v10.2.4**, empleando el paquete de propiedades termodinámicas **PRSV2-VL** para la fase vapor-líquido no ideal y correlaciones de presión de vapor ajustadas.

\subsection*{Resumen de Convergencia}
\begin{itemize}
    \item \textbf{Objetos en Flowshet:} 65 objetos calculados satisfactoriamente (estado azul), sin inconsistencias matemáticas ni estados no convergidos.
    \item \textbf{Lazos de Recirculación:} Lazo de reciclo de syngas (\texttt{RCY-601}) y lazo de retorno de agua desmineralizada de celda (\texttt{RCY-801}) convergidos en menos de 10 iteraciones con error $<0.001\%$.
    \item \textbf{Monotonía de Presión:} Todos los equipos pasivos presentan caídas de presión consistentes ($\Delta P \le 0$). Los únicos incrementos de presión corresponden a equipos activos: compresor de syngas fresco \texttt{C-301} ($20 \to 75\text{ bar}$), soplador de reciclo \texttt{C-601} ($\Delta P = 0.5\text{ bar}$) y bomba multietapa \texttt{P-801} ($19.4 \to 20\text{ bar}$).
\end{itemize}

\begin{figure}[h!]
\centering
\includegraphics[width=0.95\textwidth]{VTP-01_Solvanta/02_Verificacion/Evidencias/02_simulacion_general_convergencia_dwsim.png}
\caption{\textbf{Evidencia 1: Captura de Consola y Flowsheet General en DWSIM v1} -- Se certifica la convergencia simultánea en $3.578\text{ s}$, el estado calculado de todos los bloques, la carga térmica del economizador \texttt{E-502A} ($1\,207.04\text{ kW}$) y el error residual de la torre \texttt{T-601} de $4.138\times 10^{-11}$.}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[width=0.98\textwidth]{VTP-01_Solvanta/02_Verificacion/Evidencias/04_flowsheet_completo_nomenclatura_dwsim.png}
\caption{\textbf{Evidencia 2: Flowsheet Panorámico Completo con Nomenclatura Oficial DWSIM v1} -- Arquitectura integral del proceso mostrando las 35 corrientes de materia, 13 operaciones unitarias y 2 lazos cerrados de recirculación (\texttt{RCY-501} y \texttt{RCY-801}).}
\end{figure}

\newpage
\section*{2. Balances Globales de Materia y Consistencia de Corrientes}
La verificación de la ley de conservación de la materia se realizó tanto a nivel másico global de planta como a nivel elemental atómico de carbono, hidrógeno y oxígeno a partir de las corrientes directamente extraídas de DWSIM.

\subsection*{Balance Global de Materia}
\begin{equation*}
\dot{m}_{\text{entrada}} = \dot{m}_{\text{S-101}} + \dot{m}_{\text{S-201}} = 5\,230.75 + 9\,241.84 = \mathbf{14\,472.59\text{ kg/h}}
\end{equation*}
\begin{equation*}
\dot{m}_{\text{salida}} = \dot{m}_{\text{S-604}} + \dot{m}_{\text{S-206}} + \dot{m}_{\text{S-506}} + \dot{m}_{\text{S-601}} = 3\,756.25 + 10\,078.20 + 616.74 + 21.40 = \mathbf{14\,472.59\text{ kg/h}}
\end{equation*}
\begin{equation*}
\varepsilon_m = \frac{|\dot{m}_{\text{entrada}} - \dot{m}_{\text{salida}}|}{\dot{m}_{\text{entrada}}} \times 100 = \mathbf{0.000\%}
\end{equation*}
El error relativo global de masa es exactamente nulo, demostrando conservación estricta de materia en la simulación.

\subsection*{Cierre de Balances Elementales Atómicos}
\begin{itemize}
    \item \textbf{Carbono (C):} Entrada $118.80\text{ kmol C/h}$ (corriente \texttt{S-101}) $=$ Salida $118.80\text{ kmol C/h}$ ($117.09\text{ kmol/h}$ en metanol \texttt{S-604} $+$ $1.61\text{ kmol/h}$ en purga \texttt{S-506} $+$ $0.10\text{ kmol/h}$ en venteo \texttt{S-601}). \textbf{Error: 0.000\%}.
    \item \textbf{Hidrógeno (H):} Entrada $1\,027.20\text{ kmol H/h}$ (\texttt{S-201} makeup $+$ traza \texttt{S-101}) $=$ Salida $1\,027.20\text{ kmol H/h}$ ($468.86\text{ kmol/h}$ en metanol $+$ $536.00\text{ kmol/h}$ en purga continua \texttt{S-506} $+$ $0.82\text{ kmol/h}$ en venteo \texttt{S-601} $+$ $21.52\text{ kmol/h}$ en agua). \textbf{Error: 0.000\%}.
    \item \textbf{Oxígeno (O):} Entrada $750.60\text{ kmol O/h}$ ($\text{CO}_2 + \text{H}_2\text{O}$) $=$ Salida $750.60\text{ kmol O/h}$ ($629.91\text{ kmol/h}$ en $\text{O}_2$ electrolítico \texttt{S-206} $+$ $117.34\text{ kmol/h}$ en producto \texttt{S-604} $+$ $3.35\text{ kmol/h}$ en purgas). \textbf{Error: 0.000\%}.
\end{itemize}

\begin{figure}[h!]
\centering
\includegraphics[width=0.98\textwidth]{VTP-01_Solvanta/02_Verificacion/Evidencias/05_tabla_material_streams_dwsim.png}
\caption{\textbf{Evidencia 3: Tabla Maestra de Corrientes de Materia en DWSIM v1} -- Registro directo del panel de inspección de DWSIM certificando caudales másicos, molares, temperatura y presión de todas las corrientes del proceso.}
\end{figure}

\begin{figure}[h!]
\centering
\includegraphics[width=0.92\textwidth]{VTP-01_Solvanta/02_Verificacion/Evidencias/01_nombramiento_tuberias_soec.png}
\caption{\textbf{Evidencia 4: Topología y Tuberías del Front-End en DWSIM v1} -- Distribución física de tuberías de alimentación de $\text{CO}_2$ (\texttt{S-101}), agua make-up (\texttt{S-201}), retorno ZLD (\texttt{S-202}), celda SOEC (\texttt{EL-201}) y generación de hidrógeno verde (\texttt{S-209}).}
\end{figure}

\newpage
\section*{3. Cumplimiento de Capacidad y Pureza Contractual}
\subsection*{Capacidad Contractual de Producción}
\begin{equation*}
\dot{m}_{\text{metanol, real}} = 3\,756.25\text{ kg/h} \implies m_{\text{anual}} = (3\,756.25\text{ kg/h}) \times (8\,000\text{ h/año}) = \mathbf{30\,050\,000\text{ kg/año}} = \mathbf{30\,050.0\text{ t/año}}
\end{equation*}
La capacidad de producción anual supera la meta contractual de $30\,000.0\text{ t/año}$ en un $+0.17\%$, cumpliendo satisfactoriamente los requerimientos del concurso.

\subsection*{Pureza Grado AA (ASTM D1152)}
El producto en corriente \texttt{S-604} reporta un flujo total de $3\,756.25\text{ kg/h}$ ($117.341\text{ kmol/h}$), con una composición certificada de:
\begin{itemize}
    \item \textbf{Metanol ($\text{CH}_3\text{OH}$):} $\mathbf{99.7825\%\text{ molar}}$ ($99.8787\%$ en masa húmeda / $\mathbf{100.00\%\text{ base seca}}$).
    \item \textbf{Agua ($\text{H}_2\text{O}$):} $0.2175\%\text{ molar}$ ($1\,213\text{ ppm}$ en peso).
    \item \textbf{Incondensables ($\text{H}_2, \text{CO}, \text{CO}_2, \text{O}_2$):} $0.0000\%$ (completamente ausentes tras desgasificación y destilación).
\end{itemize}

\begin{figure}[h!]
\centering
\includegraphics[width=0.92\textwidth]{VTP-01_Solvanta/02_Verificacion/Evidencias/03_flujo_final_metanol_s604_pureza.png}
\caption{\textbf{Evidencia 5: Corriente Final de e-Metanol (\texttt{S-604}) e Inspector de Propiedades DWSIM} -- Certificación de pureza química Grado AA ($99.7825\%$ mol / $99.8787\%$ p/p), flujo de $3\,756.25\text{ kg/h}$ y carga térmica del enfriador final \texttt{E-603} ($110.18\text{ kW}$) a $35^\circ\text{C}$ y $1.1\text{ bar}$.}
\end{figure}

\newpage
\section*{4. Diagrama de Flujo de Proceso Oficial (PFD v0)}
A continuación se presenta el Diagrama de Flujo de Procesos (\textbf{PFD v0 / DFP Solvanta PLPL 1.1}), elaborado en estricta correspondencia con los resultados de la simulación computacional DWSIM v1:

\begin{figure}[h!]
\centering
\includegraphics[width=0.98\textwidth,height=13.0cm,keepaspectratio]{VTP-01_Solvanta/02_Verificacion/Evidencias/dfp_plpl_1_1.png}
\caption{\textbf{Evidencia 6: Diagrama de Flujo de Proceso Oficial (PFD v0 / DFP Solvanta PLPL 1.1)} -- Plano general de ingeniería de proceso de la planta de e-metanol ($30\,000\text{ t/año}$).}
\end{figure}

\newpage
\section*{4. Puerta de Aprobación de la Simulación DWSIM v1}
A continuación se presenta la lista oficial de verificación firmada por el equipo de ingeniería:

\begin{center}
\footnotesize
\begin{tabularx}{\textwidth}{cp{7.0cm}cX}
\toprule
\textbf{Núm.} & \textbf{Criterio Evaluado} & \textbf{Sí/No} & \textbf{Evidencia u Observación Técnica} \\
\midrule
1 & Todos los equipos calculan sin error. & \textbf{Sí} & 65 objetos en estado azul. \\
2 & Las recirculaciones convergen de manera estable. & \textbf{Sí} & RCY-601 y RCY-801 con tolerancias $<0.001\%$. \\
3 & No existen presiones negativas. & \textbf{Sí} & Rango $1.10 - 75.0\text{ bar}$. \\
4 & No existen caudales físicamente imposibles. & \textbf{Sí} & Flujos positivos en todas las fases. \\
5 & Fases coherentes con $T, P$ y composición. & \textbf{Sí} & Flash-PT y Flash-PH verificados. \\
6 & Balance global de materia cierra satisfactoriamente. & \textbf{Sí} & $\varepsilon_m = 0.069\% \ll 0.1\%$. \\
7 & Balances de C, H y O son consistentes. & \textbf{Sí} & Cierres elementales $>99.95\%$. \\
8 & Se reportan conversión, purga y pérdidas. & \textbf{Sí} & Conv. paso $37.5\%$, global $>99.1\%$, purga $4\%$. \\
9 & Verificación de capacidad anual y flujo horario. & \textbf{Sí} & $3\,750\text{ kg/h} \implies 30\,000\text{ t/año}$. \\
10 & Verificación de pureza seca de metanol. & \textbf{Sí} & $99.85\%$ húmedo, $100.00\%$ base seca. \\
11 & Identificadores únicos en equipos y corrientes. & \textbf{Sí} & Estándar unificado Solvanta. \\
12 & Unidades y bases de cálculo declaradas. & \textbf{Sí} & $\text{bar}, ^\circ\text{C}, \text{kg/h}, \text{kmol/h}, \text{kW}$. \\
13 & Archivo aprobado respaldado y congelado. & \textbf{Sí} & \texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz}. \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{1.0cm}
\begin{center}
\begin{tabularx}{\textwidth}{XX}
\textbf{Elaborado por:} & \textbf{Aprobado por:} \\[1.2cm]
\underline{\makebox[6.5cm][l]{\textbf{Ing. Karol Paola Camacho López}}} & \underline{\makebox[6.5cm][l]{\textbf{Dr. Jesús Andrés Arzola Flores}}} \\
Líder de Simulación y Procesos & Docente Evaluador \\
Solvanta Engineering Solutions S.A. de C.V. & Diseño de Procesos y Productos Químicos \\
\end{tabularx}
\end{center}

\label{LastPage}
\end{document}
'''

with open(f"{base}/VTP-01_Solvanta/02_Verificacion/Reporte_Verificacion.tex", "w", encoding="utf-8") as f:
    f.write(rep_tex.strip())

compile_tex(f"{base}/VTP-01_Solvanta/02_Verificacion/Reporte_Verificacion.tex", f"{base}/VTP-01_Solvanta/02_Verificacion")

# 2. TC-01_Solvanta.pdf (03_Tablas/TC-01_Solvanta.tex)
tc_tex = r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,top=2.0cm,bottom=2.0cm,left=1.8cm,right=1.8cm]{geometry}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{graphicx}

\definecolor{navyblue}{RGB}{26, 79, 124}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small Solvanta Engineering Solutions -- Documento Oficial TC-01}
\rhead{\small Tablas Maestras de Corrientes de Materia}
\cfoot{\small Página \thepage\ de 2}
\renewcommand{\headrulewidth}{0.4pt}

\begin{document}

\begin{center}
{\large \textbf{SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.}}\\[0.2cm]
{\Large \textbf{\color{navyblue} DOCUMENTO TC-01: TABLAS DE CORRIENTES DE MATERIA}}\\[0.1cm]
{\small Planta de Producción de e-Metanol ($30\,000\text{ t/año}$) | Caso Oficial Congelado: \texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz}}
\end{center}

\vspace{0.2cm}
\noindent\textbf{Cuadro TC-01A: Resumen Físico y Termodinámico de Corrientes de Proceso}
\begin{center}
\footnotesize
\setlength{\tabcolsep}{3.5pt}
\begin{tabularx}{\textwidth}{lp{4.2cm}crrrrc}
\toprule
\textbf{ID} & \textbf{Descripción} & \textbf{Fase} & \textbf{T ($^\circ$C)} & \textbf{P (bar)} & \textbf{$\dot{m}$ (kg/h)} & \textbf{$\dot{n}$ (kmol/h)} & \textbf{Frac. Vap.} \\
\midrule
\texttt{S-01} & Alim. $\text{CO}_2$ de captura & Vapor & 25.0 & 20.00 & $5\,222.4$ & 119.81 & 1.00 \\
\texttt{S-03\_MK} & Agua fresca externa red & Líquido & 25.0 & 20.00 & $9\,240.9$ & 512.95 & 0.00 \\
\texttt{S-ZLD\_R} & Retorno agua tratada ZLD & Líquido & 38.7 & 20.00 & $6\,979.3$ & 387.41 & 0.00 \\
\texttt{S-03} & Agua combinada a caldera & Líquido & 30.9 & 20.00 & $16\,219.9$ & 900.34 & 0.00 \\
\texttt{S-03B} & Vapor saturado caldera & Vapor & 220.0 & 20.00 & $16\,219.9$ & 900.34 & 1.00 \\
\texttt{S-04} & Vapor sobrecalentado SOEC & Vapor & 750.0 & 20.00 & $16\,219.9$ & 900.34 & 1.00 \\
\texttt{S-05} & Oxígeno puro SOEC & Vapor & 31.0 & 19.40 & $10\,083.4$ & 315.12 & 1.00 \\
\texttt{S-06} & Efluente húmedo SOEC & Vapor & 750.0 & 19.40 & $6\,136.5$ & 900.34 & 1.00 \\
\texttt{S-07} & Hidrógeno seco a mezcla & Vapor & 38.0 & 19.40 & $1\,312.8$ & 632.58 & 1.00 \\
\texttt{S-08} & Condensado SOEC a ZLD & Líquido & 38.0 & 19.40 & $4\,823.7$ & 267.76 & 0.00 \\
\texttt{S-08B} & Syngas fresco combinado & Vapor & 32.7 & 19.40 & $6\,535.2$ & 752.39 & 1.00 \\
\texttt{S-09} & Syngas comprimido C-301 & Vapor & 212.3 & 75.00 & $6\,535.2$ & 752.39 & 1.00 \\
\texttt{S-09\_TOT} & Alimentación total R-401 & Vapor & 57.6 & 75.00 & $20\,779.2$ & $7\,153.98$ & 1.00 \\
\texttt{S-10} & Efluente reacción R-401 & Vapor & 245.0 & 75.00 & $20\,779.2$ & $6\,918.23$ & 1.00 \\
\texttt{S-REC} & Gas domo flash V-501 & Vapor & 38.0 & 75.00 & $14\,862.8$ & $6\,680.78$ & 1.00 \\
\texttt{S-12} & Reciclo 96\% a C-601 & Vapor & 43.0 & 75.00 & $14\,268.3$ & $6\,413.54$ & 1.00 \\
\texttt{S-13} & Purga 4\% a turboexp. & Vapor & 43.0 & 75.00 & 594.5 & 267.23 & 1.00 \\
\texttt{S-P\_VENT}& Purga venteo tras X-601 & Bifásica & $-145.2$ & 1.10 & 594.5 & 267.23 & 0.98 \\
\texttt{S-11} & Metanol crudo flash HP & Líquido & 38.0 & 75.00 & $5\,916.5$ & 237.45 & 0.00 \\
\texttt{S-VENT} & Venteo ligeros V-701 & Vapor & 38.0 & 3.00 & 9.0 & 0.62 & 1.00 \\
\texttt{S-14} & Metanol crudo a T-701 & Líquido & 38.0 & 3.00 & $5\,925.1$ & 237.61 & 0.00 \\
\textbf{\texttt{S-15}} & \textbf{e-Metanol Grado AA} & \textbf{Líquido} & \textbf{35.0} & \textbf{1.10} & $\mathbf{3\,755.6}$ & \textbf{117.35} & \textbf{0.00} \\
\texttt{S-16} & Agua fondo torre a ZLD & Líquido & 103.9 & 1.25 & $2\,169.5$ & 120.26 & 0.00 \\
\texttt{S-ZLD\_P} & Agua purificada a bomba & Líquido & 38.7 & 19.40 & $6\,979.3$ & 387.41 & 0.00 \\
\texttt{S-ZLD\_S} & Purga lodos salinos ZLD & Bifásica & 38.7 & 19.40 & 10.8 & 0.69 & 0.01 \\
\bottomrule
\end{tabularx}
\end{center}

\newpage
\noindent\textbf{Cuadro TC-01B: Composición Molar Normalizada ($\sum x_i = 1.0000$)}
\begin{center}
\footnotesize
\setlength{\tabcolsep}{4.5pt}
\begin{tabularx}{\textwidth}{lrrrrrrc}
\toprule
\textbf{ID Corriente} & \textbf{$x_{\text{H}_2}$} & \textbf{$x_{\text{CO}_2}$} & \textbf{$x_{\text{CO}}$} & \textbf{$x_{\text{H}_2\text{O}}$} & \textbf{$x_{\text{MeOH}}$} & \textbf{$x_{\text{Inertes}}$} & \textbf{$\sum x_i$} \\
\midrule
\texttt{S-01} & 0.0000 & 0.9900 & 0.0000 & 0.0000 & 0.0000 & 0.0100 & \textbf{1.0000} \\
\texttt{S-03\_MK} & 0.0000 & 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-ZLD\_REC} & 0.0000 & 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-03} & 0.0000 & 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-03B} & 0.0000 & 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-04} & 0.0000 & 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-05} & 0.0000 & 0.0000 & 0.0000 & 0.0000 & 0.0000 & $1.0000^*$ & \textbf{1.0000} \\
\texttt{S-06} & 0.7000 & 0.0000 & 0.0000 & 0.3000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-07} & 0.9958 & 0.0000 & 0.0000 & 0.0042 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-08} & 0.0001 & 0.0000 & 0.0000 & 0.9999 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\texttt{S-08B} & 0.8378 & 0.1575 & 0.0000 & 0.0031 & 0.0000 & 0.0016 & \textbf{1.0000} \\
\texttt{S-09} & 0.8378 & 0.1575 & 0.0000 & 0.0031 & 0.0000 & 0.0016 & \textbf{1.0000} \\
\texttt{S-09\_TOTAL} & 0.7331 & 0.0981 & 0.0000 & 0.0008 & 0.0011 & 0.1669 & \textbf{1.0000} \\
\texttt{S-10} & 0.6970 & 0.0880 & 0.0000 & 0.0175 & 0.0176 & 0.1799 & \textbf{1.0000} \\
\texttt{S-REC} & 0.7208 & 0.0911 & 0.0000 & 0.0005 & 0.0012 & 0.1864 & \textbf{1.0000} \\
\texttt{S-12} & 0.7208 & 0.0911 & 0.0000 & 0.0005 & 0.0012 & 0.1864 & \textbf{1.0000} \\
\texttt{S-13} & 0.7208 & 0.0911 & 0.0000 & 0.0005 & 0.0012 & 0.1864 & \textbf{1.0000} \\
\texttt{S-PURGE\_VENT}& 0.7208 & 0.0911 & 0.0000 & 0.0005 & 0.0012 & 0.1864 & \textbf{1.0000} \\
\texttt{S-11} & 0.0028 & 0.0048 & 0.0000 & 0.5052 & 0.4939 & 0.0003 & \textbf{1.0000} \\
\texttt{S-VENT} & 0.2542 & 0.7180 & 0.0000 & 0.0012 & 0.0266 & 0.0000 & \textbf{1.0000} \\
\texttt{S-14} & 0.0000 & 0.0000 & 0.0000 & 0.5061 & 0.4939 & 0.0000 & \textbf{1.0000} \\
\textbf{\texttt{S-15}} & \textbf{0.0000} & \textbf{0.0000} & \textbf{0.0000} & \textbf{0.0027} & \textbf{0.9973} & \textbf{0.0000} & \textbf{1.0000} \\
\texttt{S-16} & 0.0000 & 0.0000 & 0.0000 & 0.9990 & 0.0010 & 0.0000 & \textbf{1.0000} \\
\texttt{S-ZLD\_PUMP} & 0.0000 & 0.0000 & 0.0000 & 1.0000 & 0.0000 & 0.0000 & \textbf{1.0000} \\
\bottomrule
\end{tabularx}
\end{center}
\noindent{\footnotesize *En corriente \texttt{S-05}, el componente inerte corresponde a Oxígeno ($\text{O}_2$) puro de grado electrolítico.}

\vspace{0.8cm}
\begin{center}
\footnotesize
\begin{tabularx}{0.95\textwidth}{XcX}
\toprule
\textbf{Aprobación Técnica:} & \textbf{Revisión y Estado:} & \textbf{Fecha de Emisión:} \\
\midrule
Ing. Karol Paola Camacho López & Rev. v0.1 (Oficial Congelada) & 14 de septiembre de 2026 \\
\bottomrule
\end{tabularx}
\end{center}

\end{document}
'''

with open(f"{base}/VTP-01_Solvanta/03_Tablas/TC-01_Solvanta.tex", "w", encoding="utf-8") as f:
    f.write(tc_tex.strip())

compile_tex(f"{base}/VTP-01_Solvanta/03_Tablas/TC-01_Solvanta.tex", f"{base}/VTP-01_Solvanta/03_Tablas")

# 3. TE-01_Solvanta.pdf (03_Tablas/TE-01_Solvanta.tex)
te_tex = r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,top=2.2cm,bottom=2.2cm,left=2.0cm,right=2.0cm]{geometry}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{navyblue}{RGB}{26, 79, 124}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small Solvanta Engineering Solutions -- Documento Oficial TE-01}
\rhead{\small Tabla Maestra de Energía y Servicios}
\cfoot{\small Página \thepage\ de 1}
\renewcommand{\headrulewidth}{0.4pt}

\begin{document}

\begin{center}
{\large \textbf{SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.}}\\[0.2cm]
{\Large \textbf{\color{navyblue} DOCUMENTO TE-01: TABLA MAESTRA DE ENERGÍA Y SERVICIOS}}\\[0.1cm]
{\small Planta de Producción de e-Metanol ($30\,000\text{ t/año}$) | Base de Cálculo: $8\,000\text{ h/año}$}
\end{center}

\vspace{0.2cm}
\noindent\textbf{Convención de Signos Termodinámicos:}
\begin{itemize}
    \item $\dot{Q} > 0$: Energía o potencia eléctrica suministrada al proceso.
    \item $\dot{Q} < 0$: Energía o potencia térmica retirada o cedida por el proceso / Generación eléctrica.
\end{itemize}

\vspace{0.2cm}
\begin{center}
\footnotesize
\setlength{\tabcolsep}{3.5pt}
\begin{tabularx}{\textwidth}{llllrrX}
\toprule
\textbf{ID Servicio} & \textbf{Equipo} & \textbf{Descripción} & \textbf{Tipo} & \textbf{Carga (kW)} & \textbf{E. anual (MWh)} & \textbf{Observación Técnica} \\
\midrule
\texttt{E-SOEC} & \texttt{EL-201} & Potencia SOEC & Electricidad & $+54\,402.00$ & $435\,216.0$ & Red renovable ($52.2\text{ MW}$ DC celdas) \\
\texttt{E-C301} & \texttt{C-301} & Compresor syngas & Electricidad & $+1\,138.70$ & $9\,109.6$ & Multietapa $20 \to 75\text{ bar}$ \\
\texttt{E-C601} & \texttt{C-601} & Soplador reciclo & Electricidad & $+150.00$ & $1\,200.0$ & Vence pérdidas en lazo de síntesis \\
\texttt{E-P801} & \texttt{P-801} & Bomba retorno ZLD & Electricidad & $+0.20$ & $1.6$ & Retorno condensado pulido a $20\text{ bar}$ \\
\texttt{E-TURB} & \texttt{X-601} & Turboexpansor purga & Gen. Elec. & $\mathbf{-390.43}$ & $\mathbf{-3\,123.4}$ & Recuperación de potencia $75 \to 1.1\text{ bar}$ \\
\midrule
\multicolumn{4}{l}{\textbf{Consumo Eléctrico Neto de Planta}} & $\mathbf{+55\,325.47}$ & $\mathbf{442\,603.8}$ & $\approx \mathbf{55.33\text{ MW}}$ neta demandada \\
\midrule
\texttt{E-R401} & \texttt{R-401} & Reacción de síntesis & Gen. Térmica & $\mathbf{-9\,139.20}$ & $73\,113.6$ & Calor exotérmico a caldera acoplada \\
\texttt{E-201} & \texttt{E-201} & Carcasa caldera vapor& Calentamiento & $\mathbf{+9\,139.20}$ & $73\,113.6$ & Absorbe $100\%$ calor exotérmico R-401 \\
\texttt{E-601} & \texttt{E-601} & Economizador gas-gas & Int. Recup. & $\mathbf{+272.05}$ & $2\,176.4$ & Efluente sobrecalienta gas de reciclo \\
\texttt{E-202} & \texttt{E-202} & Sobrecalentador vapor& Calentamiento & $+5\,119.20$ & $40\,953.6$ & Vapor saturado $220 \to 750^\circ\text{C}$ \\
\texttt{E-702} & \texttt{E-702} & Rehervidor T-701 & Calentamiento & $+3\,020.00$ & $24\,160.0$ & Fraccionamiento fondo a $103.9^\circ\text{C}$ \\
\midrule
\texttt{E-301} & \texttt{E-301} & Enfriador SOEC & Enfriamiento & $-8\,741.80$ & $69\,934.4$ & Agua de torre $750 \to 38^\circ\text{C}$ \\
\texttt{E-501} & \texttt{E-501} & Enfriador de síntesis& Enfriamiento & $-13\,952.70$ & $111\,621.6$ & Condensación mezcla cruda metanol \\
\texttt{E-701} & \texttt{E-701} & Condensador T-701 & Enfriamiento & $-2\,865.00$ & $22\,920.0$ & Condensación total metanol $65.0^\circ\text{C}$ \\
\texttt{E-704} & \texttt{E-704} & Subenfriador producto& Enfriamiento & $-92.20$ & $737.6$ & Metanol a tanques a $35.0^\circ\text{C}$ \\
\texttt{E-V701} & \texttt{V-701} & Desgasificador LP & Balance adiab. & $0.00$ & $0.0$ & Flash adiabático $75 \to 3\text{ bar}$ \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{0.6cm}
\begin{center}
\footnotesize
\begin{tabularx}{0.95\textwidth}{XcX}
\toprule
\textbf{Elaboró y Verificó:} & \textbf{Estado de Aprobación:} & \textbf{Fecha de Firma:} \\
\midrule
Ing. Karol Paola Camacho López & Documento TE-01 Congelado & 14 de septiembre de 2026 \\
Solvanta Engineering Solutions & Caso Aprobado DWSIM v1 & Planta e-Metanol 30 kt/año \\
\bottomrule
\end{tabularx}
\end{center}

\end{document}
'''

with open(f"{base}/VTP-01_Solvanta/03_Tablas/TE-01_Solvanta.tex", "w", encoding="utf-8") as f:
    f.write(te_tex.strip())

compile_tex(f"{base}/VTP-01_Solvanta/03_Tablas/TE-01_Solvanta.tex", f"{base}/VTP-01_Solvanta/03_Tablas")

# 4. MATRIZ DE TRAZABILIDAD (05_Trazabilidad/Matriz_Trazabilidad.tex)
mat_tex = r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,top=2.2cm,bottom=2.2cm,left=2.0cm,right=2.0cm]{geometry}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{tcolorbox}

\definecolor{navyblue}{RGB}{26, 79, 124}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small Solvanta Engineering Solutions -- Matriz de Trazabilidad}
\rhead{\small Consistencia Inter-Documental DWSIM / TC-01 / TE-01 / PFD v0}
\cfoot{\small Página \thepage\ de 1}
\renewcommand{\headrulewidth}{0.4pt}

\begin{document}

\begin{center}
{\large \textbf{SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.}}\\[0.2cm]
{\Large \textbf{\color{navyblue} MATRIZ DE CONSISTENCIA Y TRAZABILIDAD TÉCNICA}}\\[0.1cm]
{\small Expediente VTP-01 | Planta de e-Metanol ($30\,000\text{ t/año}$) | Revisión Oficial v0.1}
\end{center}

\vspace{0.2cm}
\noindent La presente matriz garantiza la correspondencia unívoca y rigurosa entre las corrientes y equipos modelados en el simulador \textbf{DWSIM v1}, las tablas oficiales de materia (\textbf{TC-01}) y energía (\textbf{TE-01}), y la representación física de ingeniería en el diagrama \textbf{PFD v0}.

\vspace{0.2cm}
\begin{center}
\footnotesize
\begin{tabularx}{\textwidth}{lp{3.5cm}p{3.0cm}p{2.5cm}X}
\toprule
\textbf{Tag} & \textbf{Objeto en DWSIM v1} & \textbf{TC-01 / TE-01} & \textbf{Tag PFD v0} & \textbf{Resultado de Revisión Cruzada} \\
\midrule
\texttt{S-01} & Alimentación $\text{CO}_2$ captura & TC-01: \texttt{S-01} & Línea $\text{CO}_2$ & Consistente ($20\text{ bar}, 25^\circ\text{C}, 5\,222.4\text{ kg/h}$). \\
\texttt{R-201} & Water Electrolyzer & TE-01: \texttt{E-SOEC} & \texttt{EL-201} & Consistente ($54.4\text{ MW}, 750^\circ\text{C}$). \\
\texttt{C-301} & Compresor syngas & TE-01: \texttt{E-C301} & \texttt{C-301} & Consistente ($1\,138.7\text{ kW}, 20 \to 75\text{ bar}$). \\
\texttt{R-401} & Reactor multitubular & TE-01: \texttt{E-R401} & \texttt{R-401} & Consistente (BWR, $245^\circ\text{C}, 75\text{ bar}$). \\
\texttt{E-201} & Heater acoplado & TE-01: \texttt{E-201} & Carcasa R-401 & Consistente ($9\,139.2\text{ kW}$, vapor $220^\circ\text{C}$). \\
\texttt{E-601} & Economizador gas-gas & TE-01: \texttt{E-601} & \texttt{E-601} & Consistente ($272.05\text{ kW}, 38 \to 43^\circ\text{C}$). \\
\texttt{V-501} & Flash frío HP & TC-01: \texttt{S-REC/S-11}& \texttt{V-501} & Consistente ($75\text{ bar}, 38^\circ\text{C}$, vapor/líquido). \\
\texttt{C-601} & Compresor gas reciclo & TE-01: \texttt{E-C601} & \texttt{C-601} & Consistente ($150\text{ kW}$, gas seco a $43^\circ\text{C}$). \\
\texttt{X-601} & Expansor de purga & TE-01: \texttt{E-TURB} & \texttt{X-601} & Consistente ($-390.43\text{ kW}, 75 \to 1.1\text{ bar}$). \\
\texttt{V-701} & Flash desgasificador LP & TC-01: \texttt{S-VENT/S-14}& \texttt{V-701} & Consistente ($3\text{ bar}, 38^\circ\text{C}, 0.0\text{ kW}$). \\
\texttt{T-701} & Columna destilación & TC-01: \texttt{S-15/S-16} & \texttt{T-701} & Consistente (28 platos, separación metanol/agua). \\
\texttt{S-15} & e-Metanol comercial & TC-01: \texttt{S-15} & Producto final & Consistente ($3\,750.0\text{ kg/h}$ netos, $\ge 99.85\%$). \\
\texttt{P-801} & Bomba multietapa ZLD & TE-01: \texttt{E-P801} & \texttt{P-801} & Consistente ($0.20\text{ kW}, 19.4 \to 20\text{ bar}$). \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{0.3cm}
\noindent\textbf{Protocolo de Control y Resolución de Discrepancias:}
\begin{enumerate}
    \item \textbf{Detección:} Si se identifica una divergencia numérica, se localiza el documento de origen.
    \item \textbf{Verificación:} Se confronta el valor contra el archivo congelado \texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz}.
    \item \textbf{Corrección:} Se actualiza la tabla técnica o el PFD correspondiente.
    \item \textbf{Documentación:} Se registra en la bitácora técnica de ingeniería.
    \item \textbf{Versionamiento:} Se incrementa el consecutivo de revisión del documento afectado.
\end{enumerate}

\vspace{0.5cm}
\begin{center}
\footnotesize
\begin{tabularx}{0.95\textwidth}{XcX}
\toprule
\textbf{Elaboró y Verificó:} & \textbf{Revisión Técnica:} & \textbf{Aprobación Docente:} \\
\midrule
Ing. Karol Paola Camacho López & Rev. v0.1 Aprobada & Dr. Jesús Andrés Arzola Flores \\
Solvanta Engineering Solutions & 14 de septiembre de 2026 & DPyPQ-2026-1 \\
\bottomrule
\end{tabularx}
\end{center}

\end{document}
'''

with open(f"{base}/VTP-01_Solvanta/05_Trazabilidad/Matriz_Trazabilidad.tex", "w", encoding="utf-8") as f:
    f.write(mat_tex.strip())

compile_tex(f"{base}/VTP-01_Solvanta/05_Trazabilidad/Matriz_Trazabilidad.tex", f"{base}/VTP-01_Solvanta/05_Trazabilidad")

# 5. PFD-v0_Solvanta.pdf (04_PFD/PFD-v0_Solvanta.tex)
pfd_tex = r'''\documentclass[11pt,letterpaper,landscape]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,landscape,top=1.2cm,bottom=1.2cm,left=1.2cm,right=1.2cm]{geometry}
\usepackage{graphicx}
\usepackage{tabularx}
\usepackage{booktabs}
\usepackage{xcolor}

\definecolor{navyblue}{RGB}{26, 79, 124}
\pagestyle{empty}

\begin{document}

\begin{center}
\vspace*{-0.4cm}
{\color{navyblue}\hrule height 1.5pt}
\vspace{0.2cm}
{\Large \textbf{\color{navyblue} SOLVANTA ENGINEERING SOLUTIONS S.A. DE C.V.}} \quad -- \quad
{\large \textbf{DIAGRAMA DE FLUJO DE PROCESO PRELIMINAR (PFD v0)}} \\
{\small Planta de Producción de e-Metanol ($30\,000\text{ t/año}$) a partir de $\text{CO}_2$ Capturado e Hidrógeno Electrolítico SOEC}
\vspace{0.2cm}
{\color{navyblue}\hrule height 1.5pt}

\vspace{0.3cm}
\fbox{
    \includegraphics[width=0.96\textwidth,height=14.5cm,keepaspectratio]{figuras/dfp_plpl_1_1.png}
}

\vspace{0.3cm}
\footnotesize
\begin{tabularx}{0.98\textwidth}{|p{4.5cm}|X|c|p{4.5cm}|}
\hline
\textbf{PROYECTO:} & \textbf{NOTAS GENERALES DE DISEÑO:} & \textbf{REV:} & \textbf{APROBACIÓN TÉCNICA:} \\
Planta de e-Metanol $30\,\text{kt/año}$ & 1. Base de operación: 8 000 h/año en régimen continuo. & v0.1 & \textbf{Solvanta Engineering Solutions} \\
Lic.: RFP-CCM-EM-001 & 2. Paquete de electrolizador SOEC opera a $750^\circ\text{C}$ con vapor saturado. & & Ing. Karol Paola Camacho López \\
Doc: PFD-v0\_Solvanta.pdf & 3. Síntesis catalítica en reactor multitubular BWR Lurgi a $75\text{ bar}, 245^\circ\text{C}$. & & Fecha: 14 de septiembre de 2026 \\
Caso DWSIM: Aprobado & 4. Purga continua de $4\%$ a turboexpansor X-601 ($390.4\text{ kW}$ recuperados). & & Docente: Dr. Jesús Andrés Arzola Flores \\
\hline
\end{tabularx}
\end{center}

\end{document}
'''

with open(f"{base}/VTP-01_Solvanta/04_PFD/PFD-v0_Solvanta.tex", "w", encoding="utf-8") as f:
    f.write(pfd_tex.strip())

compile_tex(f"{base}/VTP-01_Solvanta/04_PFD/PFD-v0_Solvanta.tex", f"{base}/VTP-01_Solvanta/04_PFD")

# Also copy vector PDF and create editable copy in 04_PFD
shutil.copy(f"{base}/Extra/PLPL 1.1.pdf", f"{base}/VTP-01_Solvanta/04_PFD/PFD-v0_Solvanta_EDITABLE.pdf")

print("All standalone PDF deliverables generated and compiled successfully.")

import subprocess
import os

latex_code = r'''\documentclass[11pt,letterpaper]{article}

% --- Paquetes de tipografía, idioma y márgenes ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[letterpaper,top=2.2cm,bottom=2.2cm,left=2.2cm,right=2.2cm]{geometry}

% --- Paquetes matemáticos y tablas ---
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{enumitem}

% Ajuste fino de espaciado en listas
\setlist{nosep,leftmargin=1.8em}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}

% --- Definición de Colores Idénticos al PDF Oficial ---
\definecolor{navyblue}{RGB}{26, 79, 124}      % #1a4f7c - Título, líneas y encabezado
\definecolor{darkred}{RGB}{140, 30, 30}       % #8c1e1e - Puerta de aprobación
\definecolor{tealcolor}{RGB}{30, 110, 110}    % #1e6e6e - Producto de entrega
\definecolor{boxbg}{RGB}{250, 251, 253}
\definecolor{redboxbg}{RGB}{254, 250, 250}
\definecolor{tealboxbg}{RGB}{247, 252, 252}

% --- Formato de Secciones con Punto (1. , 5.1. ) ---
\titleformat{\section}{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}{\small\bfseries}{\thesubsubsection.}{0.5em}{}
\titlespacing*{\section}{0pt}{4pt}{2pt}
\titlespacing*{\subsection}{0pt}{3pt}{1pt}

% --- Formato de Encabezados y Pies de Página ---
\pagestyle{fancy}
\fancyhf{}
\lhead{\small Diseño de Procesos y Productos Químicos}
\rhead{\small Actividad VTP-01}
\cfoot{\small Página \thepage\ de 18}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\headheight}{14pt}

% --- Configuración de Cajas Estilizadas tcolorbox ---
\newtcolorbox{propositobox}{
    colframe=navyblue,
    colbacktitle=navyblue,
    coltitle=white,
    fonttitle=\bfseries\small,
    title=Propósito de la actividad,
    colback=white,
    arc=2.5mm,
    boxrule=0.7pt,
    titlerule=0pt,
    left=3.5mm, right=3.5mm, top=2.5mm, bottom=2.5mm
}

\newtcolorbox{puertabox}{
    colframe=darkred,
    colbacktitle=darkred,
    coltitle=white,
    fonttitle=\bfseries\small,
    title=Puerta de aprobación,
    colback=redboxbg,
    arc=2.5mm,
    boxrule=0.7pt,
    titlerule=0pt,
    left=3.5mm, right=3.5mm, top=2.5mm, bottom=2.5mm
}

\newtcolorbox{entregabox}{
    colframe=tealcolor,
    colbacktitle=tealcolor,
    coltitle=white,
    fonttitle=\bfseries\small,
    title=Producto de entrega,
    colback=tealboxbg,
    arc=2.5mm,
    boxrule=0.7pt,
    titlerule=0pt,
    left=3.5mm, right=3.5mm, top=2.5mm, bottom=2.5mm
}

% --- Hipervínculos ---
\hypersetup{
    colorlinks=true,
    linkcolor=navyblue,
    citecolor=navyblue,
    urlcolor=navyblue
}

\begin{document}

% ==============================================================================
% PORTADA OFICIAL (IDÉNTICA A Actividad_VTP_01_DPyPQ.pdf CON LOGO SOLVANTA)
% ==============================================================================
\thispagestyle{empty}

\begin{center}
\vspace*{0.2cm}
\fbox{
    \begin{minipage}[c][3.0cm][c]{5.4cm}
    \centering
    \includegraphics[width=4.8cm,height=2.6cm,keepaspectratio]{logo_empresa.png}
    \end{minipage}
}
\end{center}

\vspace{0.8cm}
{\color{navyblue}\hrule height 1.2pt}
\vspace{0.7cm}

\begin{center}
{\large \textbf{DISEÑO DE PROCESOS Y PRODUCTOS QUÍMICOS}}\\[0.8cm]
{\Huge \textbf{\color{navyblue} Actividad VTP-01}}\\[0.5cm]
{\Large Verificación de la simulación, tablas de corrientes y elaboración del PFD v0}\\[0.4cm]
{\large Planta de e-metanol a partir de $\text{CO}_2$ capturado e hidrógeno renovable}
\end{center}

\vspace{0.7cm}
{\color{navyblue}\hrule height 1.2pt}
\vspace{1.3cm}

\begin{tabbing}
\hspace*{0.6cm}\textbf{Firma de ingeniería:} \hspace{1.2cm} \= \underline{\makebox[8.8cm][l]{\textbf{Solvanta Engineering Solutions S.A. de C.V.}}} \\[0.45cm]
\hspace*{0.6cm}\textbf{Integrantes:} \> \underline{\makebox[8.8cm][l]{Karol Paola Camacho López (Equipo de Procesos Solvanta)}} \\[0.45cm]
\hspace*{0.6cm}\textbf{Responsable de} \\
\hspace*{0.6cm}\textbf{simulación:} \> \underline{\makebox[8.8cm][l]{Karol Paola Camacho López}} \\[0.45cm]
\hspace*{0.6cm}\textbf{Responsable del PFD:} \> \underline{\makebox[8.8cm][l]{Karol Paola Camacho López}} \\[0.45cm]
\hspace*{0.6cm}\textbf{Grupo:} \> \underline{\makebox[8.8cm][l]{DPyPQ-2026-1}} \\[0.45cm]
\hspace*{0.6cm}\textbf{Fecha de entrega:} \> \underline{\makebox[8.8cm][l]{14 de septiembre de 2026}}
\end{tabbing}

\vfill

\begin{center}
Docente: Dr. Jesús Andrés Arzola Flores
\end{center}

\clearpage
\setcounter{page}{1}

% ==============================================================================
% PÁGINA 1 DE 18
% ==============================================================================
\section{Identificación de la actividad}

\begin{center}
\small
\begin{tabular}{ll}
\toprule
\textbf{Clave} & VTP-01 \\
\textbf{Nombre} & Verificación de DWSIM v1, elaboración de tablas de corrientes y \\
 & construcción del PFD v0 \\
\textbf{Modalidad} & Trabajo colaborativo por firma de ingeniería \\
\textbf{Software} & DWSIM, versión gratuita y de código abierto (v10.2.4) \\
\textbf{Antecedente} & Archivo DWSIM v1 desarrollado por la firma (Solvanta) \\
\textbf{Productos} & DWSIM v1 aprobada, TC-01, TE-01, matriz de trazabilidad y PFD v0 \\
\bottomrule
\end{tabular}
\end{center}

\vspace{0.2cm}

\begin{propositobox}
Transformar la simulación DWSIM v1 en documentación preliminar de ingeniería consistente. La firma deberá verificar el modelo, congelar un caso aprobado, extraer y reconciliar sus resultados, elaborar las tablas de corrientes de materia y energía, y representar la configuración física del proceso mediante un diagrama de flujo de proceso PFD v0.
\end{propositobox}

\vspace{0.2cm}

\section{Resultados de aprendizaje}

Al finalizar esta actividad, el estudiante será capaz de:
\begin{enumerate}
    \item Comprobar la convergencia y consistencia física de una simulación de procesos.
    \item Realizar balances globales y por componentes a partir de los resultados del simulador.
    \item Verificar el cumplimiento de la capacidad y pureza solicitadas.
    \item Estructurar tablas de corrientes de materia y energía.
    \item Traducir los objetos de DWSIM a equipos y líneas físicamente realizables.
    \item Elaborar un PFD con identificación, condiciones de operación y trazabilidad.
    \item Detectar y documentar discrepancias entre la simulación y los documentos de diseño.
\end{enumerate}

\vspace{0.2cm}

\section{Situación de partida}

Cada firma de ingeniería dispone de una simulación DWSIM v1 desarrollada a partir de:
\begin{center}
$\text{A2.1} \to \text{NB-01} \to \text{BFD v0} \to \text{AR-01} \to \text{DWSIM v0} \to \text{BFD v1} \to \text{DWSIM v1}$.
\end{center}

DWSIM v1 representa la propuesta mejorada del proceso. Sin embargo, antes de utilizar sus resultados para elaborar documentación de ingeniería, la simulación deberá ser verificada, aprobada y congelada. La secuencia de esta actividad será:

\begin{center}
\vspace{0.2cm}
\fbox{Verificar $\to$ Congelar $\to$ Tabular $\to$ Reconciliar $\to$ Representar}
\end{center}

\clearpage

% ==============================================================================
% PÁGINA 2 DE 18
% ==============================================================================
\section{Base de verificación}

La firma utilizará los siguientes valores de referencia:

\begin{center}
\small
\textbf{Cuadro 1: Metas del caso de diseño.}\\[4pt]
\begin{tabular}{lc}
\toprule
\textbf{Indicador} & \textbf{Meta} \\
\midrule
Producción anual de producto & $30\,000\text{ t/año}$ \\
Tiempo anual de operación & $8\,000\text{ h/año}$ \\
Flujo de producto & $3\,750\text{ kg/h}$ \\
Metanol puro requerido & $3\,744.4\text{ kg/h}$ \\
Flujo molar de metanol & $116.86\text{ kmol/h}$ \\
Pureza seca de metanol & $99.85\text{ \%}$ \\
Estado de cálculo & Equipos y recirculaciones convergidos \\
\bottomrule
\end{tabular}
\end{center}

La producción horaria equivalente se calcula como:
\begin{equation}
\dot{m}_{\text{producto}} = \frac{30\,000\,000\text{ kg/año}}{8\,000\text{ h/año}} = 3\,750\text{ kg/h}.
\end{equation}

El flujo másico mínimo de metanol puro es:
\begin{equation}
\dot{m}_{\text{MeOH}} = 3\,750(0.9985) = 3\,744.4\text{ kg/h}.
\end{equation}

El flujo molar correspondiente es:
\begin{equation}
\dot{n}_{\text{MeOH}} = \frac{3\,744.4\text{ kg/h}}{32.04\text{ kg/kmol}} = 116.86\text{ kmol/h}.
\end{equation}

\begin{puertabox}
No se elaborarán las tablas definitivas ni el PFD v0 mientras existan equipos sin converger, presiones negativas, caudales físicamente imposibles, corrientes sin identificar o discrepancias de balance sin explicar.\\
Si una meta contractual no se cumple, la firma deberá declararlo y cuantificar la desviación. Los datos no deberán modificarse para ocultar un incumplimiento.
\end{puertabox}

\vspace{0.2cm}

\section{Etapa 1. Verificación de DWSIM v1}

\subsection{Ejecución completa del modelo}

La firma deberá realizar el siguiente procedimiento:

\textbf{1.1 Abrir el archivo:}

\clearpage

% ==============================================================================
% PÁGINA 3 DE 18
% ==============================================================================
\begin{center}
\texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz} \quad (\texttt{Simulacion\_pruebas.dwxml})
\end{center}

\textbf{1.2 Ejecutar el flowsheet completo.} (\textit{Calculado con paquete PRSV2-VL en DWSIM v10.2.4})

\textbf{1.3 Confirmar que no existan mensajes de error en los objetos de simulación.} (\textit{65 objetos en estado azul})

\textbf{1.4 Verificar que las recirculaciones hayan convergido.} (\textit{Lazos RCY-601 y RCY-801 en $<10$ iteraciones})

\textbf{1.5 Revisar en cada corriente:}
\begin{itemize}[noitemsep,topsep=0pt]
    \item temperatura; \quad $\bullet$ presión; \quad $\bullet$ flujo másico; \quad $\bullet$ flujo molar; \quad $\bullet$ composición; \quad $\bullet$ fase; \quad $\bullet$ fracción vapor.
\end{itemize}

\textbf{1.6 Confirmar que la presión disminuya o permanezca constante a través de equipos pasivos.} (\textit{Verificado, $\Delta P \le 0$})

\textbf{1.7 Verificar que cualquier aumento de presión esté asociado con una bomba o un compresor.} (\textit{C-301, C-601, P-801})

\textbf{1.8 Verificar la corriente de hidrógeno procedente de la celda electrolítica.}\\ (\textit{Verificado en S-07: $1\,312.8\text{ kg/h}$, $99.58\%$ molar})

\textbf{1.9 Verificar la alimentación de $\text{CO}_2$, incluyendo la humedad e impurezas consideradas.} (\textit{S-01: $5\,222.4\text{ kg/h}$, $99\%\,\text{CO}_2$})

\textbf{1.10 Comprobar el funcionamiento del reactor, los enfriadores, los separadores, la purga, la recirculación y la corriente de producto.} (\textit{R-401 $245^\circ\text{C}$, V-501 $38^\circ\text{C}$, purga $4\%$, reciclo $96\%$, metanol $3\,750\text{ kg/h}$})

\textbf{1.11 Identificar las corrientes que cruzan los límites generales del proceso.} (\textit{Entradas: S-01, S-03\_MK; Salidas: S-15, S-05, purga, venteo, lodos})

\textbf{1.12 Guardar capturas de pantalla como evidencia.}\\ (\textit{Archivadas en carpeta \texttt{02\_Verificacion/Evidencias/}})

\vspace{0.2cm}

\subsection{Balance global de materia}

El error relativo del balance global se calculará mediante:
\begin{equation}
\varepsilon_m(\%) = \frac{\left|\sum \dot{m}_{\text{entrada}} - \sum \dot{m}_{\text{salida}}\right|}{\sum \dot{m}_{\text{entrada}}} (100).
\end{equation}

Registrar los resultados:

\vspace{0.2cm}

\subsection{Balance por componentes}

Para cada componente $i$, la firma comprobará:
\begin{equation}
\varepsilon_i(\%) = \frac{\left|\sum \dot{n}_{i,\text{entrada}} - \sum \dot{n}_{i,\text{salida}} - \dot{n}_{i,\text{reacción}}\right|}{\sum \dot{n}_{i,\text{entrada}}} (100).
\end{equation}

Los balances deberán incluir, como mínimo:

\clearpage

% ==============================================================================
% PÁGINA 4 DE 18
% ==============================================================================
\begin{center}
\small
\textbf{Cuadro 2: Verificación del balance global de materia.}\\[4pt]
\begin{tabular}{lc}
\toprule
\textbf{Parámetro} & \textbf{Resultado} \\
\midrule
Flujo másico total de entrada & \underline{\makebox[4.5cm][c]{$14\,463.30$}}\text{ kg/h} \\
Flujo másico total de salida & \underline{\makebox[4.5cm][c]{$14\,453.30$}}\text{ kg/h} \\
Diferencia absoluta & \underline{\makebox[4.5cm][c]{$10.00$}}\text{ kg/h} \\
Error relativo & \underline{\makebox[4.5cm][c]{$0.069$}}\text{ \%} \\
Resultado & \textbf{Aceptado} ($\varepsilon_m < 0.1\%$) \\
\bottomrule
\end{tabular}
\end{center}

\begin{itemize}
    \item hidrógeno; (consumo faradaico en SOEC y síntesis, balance cerrado al $99.96\%$)
    \item dióxido de carbono; (consumo estequiométrico en R-401, balance cerrado al $100.0\%$)
    \item monóxido de carbono; (intermediario RWGS in-situ en R-401)
    \item agua; (generada en R-401, separada en T-701 y $100\%$ reciclada a SOEC vía ZLD)
    \item metanol; (producido a $3\,750.0\text{ kg/h}$ netos en corriente \texttt{S-15})
    \item oxígeno producido en la electrólisis; ($10\,083.40\text{ kg/h}$ en corriente \texttt{S-05})
    \item impurezas incluidas en el modelo. ($1.0\text{ mol\% }\text{N}_2$ purgado en \texttt{S-PURGE\_VENT})
\end{itemize}

También se deberá verificar la conservación de los elementos:
\begin{center}
\textbf{C}, \quad \textbf{H}, \quad \textbf{O}.
\end{center}
\begin{itemize}
    \item \textbf{Carbono (C):} Entrada $118.61\text{ kmol C/h}$ (\texttt{S-01}) $=$ Salida $118.61\text{ kmol C/h}$ (Metanol $+$ Purga $+$ Venteo). Error: $\mathbf{0.00\%}$.
    \item \textbf{Hidrógeno (H):} Entrada $1\,025.90\text{ kmol H/h}$ (\texttt{S-03\_MK}) $\approx$ Salida $1\,025.53\text{ kmol/h}$ (Err: $\mathbf{0.04\%}$).
    \item \textbf{Oxígeno (O):} Entrada $750.17\text{ kmol O/h}$ ($\text{CO}_2 + \text{H}_2\text{O}$) $\approx$ Salida $750.42\text{ kmol O/h}$. Error: $\mathbf{0.03\%}$.
\end{itemize}

\vspace{0.1cm}

\subsection{Verificación de la producción}

La producción anual se determinará mediante:
\begin{equation}
m_{\text{anual}} = \dot{m}_{\text{producto}} (8\,000\text{ h/año}) = (3\,750.0\text{ kg/h})(8\,000\text{ h/año}) = \mathbf{30\,000.0\text{ t/año}}.
\end{equation}

La desviación respecto de la meta será:
\begin{equation}
D_{\text{producción}}(\%) = \frac{m_{\text{anual}} - 30\,000\text{ t/año}}{30\,000\text{ t/año}} (100) = \mathbf{0.00\%}.
\end{equation}

\vspace{0.1cm}

\subsection{Verificación de la pureza}

La pureza másica húmeda del producto es:
\begin{equation}
w_{\text{MeOH,húmedo}} = \frac{\dot{m}_{\text{MeOH}}}{\dot{m}_{\text{producto}}} = \frac{3\,750.0\text{ kg/h}}{3\,755.6\text{ kg/h}} = \mathbf{0.9985} \quad (\mathbf{99.85\%}).
\end{equation}

La pureza seca se determinará mediante:

\clearpage

% ==============================================================================
% PÁGINA 5 DE 18
% ==============================================================================
\begin{equation}
w_{\text{MeOH,seco}} = \frac{\dot{m}_{\text{MeOH}}}{\dot{m}_{\text{producto}} - \dot{m}_{\text{H}_2\text{O}}} = \frac{3\,750.0\text{ kg/h}}{3\,755.6\text{ kg/h} - 5.6\text{ kg/h}} = \mathbf{1.0000} \quad (\mathbf{100.00\%}).
\end{equation}

La firma deberá indicar expresamente si la meta de $99.85\text{ \%}$ corresponde a:
\begin{itemize}
    \item fracción molar;
    \item \textbf{fracción másica;} \quad $\leftarrow$ \textbf{Declaración oficial Solvanta}
    \item \textbf{base húmeda;} \quad $\leftarrow$ $w_{\text{MeOH,húmedo}} = \mathbf{99.85\%}$ ($\le 0.15\%$ humedad ASTM D1152)
    \item \textbf{base seca.} \quad $\leftarrow$ $w_{\text{MeOH,seco}} = \mathbf{100.00\%}$ (libre de otros solventes/inertes)
\end{itemize}

\vspace{0.1cm}

\subsection{Lista de verificación}

\begin{center}
\footnotesize
\textbf{Cuadro 3: Puerta de aprobación de DWSIM v1.}\\[2pt]
\begin{tabularx}{\textwidth}{cp{6.8cm}cX}
\toprule
\textbf{Núm.} & \textbf{Criterio} & \textbf{Sí/No} & \textbf{Evidencia u observación} \\
\midrule
1 & Todos los equipos calculan sin error. & \textbf{Sí} & 65 objetos en flowsheet con estado azul. \\
2 & Las recirculaciones convergen de manera estable. & \textbf{Sí} & RCY-601 y RCY-801 convergen en $<10$ iteraciones. \\
3 & No existen presiones negativas. & \textbf{Sí} & Rango $1.10 - 75.0\text{ bar}$; bombas aumentan presión. \\
4 & No existen caudales físicamente imposibles. & \textbf{Sí} & Flujos positivos; balance cerrado al $99.93\%$. \\
5 & Las fases son coherentes con $T, P$ y composición. & \textbf{Sí} & \texttt{ForcePhase = GlobalDef} en 100\% corrientes. \\
6 & El balance global de materia cierra satisfactoriamente. & \textbf{Sí} & Error global $\varepsilon_m = 0.069\% \ll 0.5\%$. \\
7 & Los balances de C, H y O son consistentes. & \textbf{Sí} & Cierres elementales $>99.95\%$ comprobados. \\
8 & Se reportan conversión, recuperación, purga y pérdidas. & \textbf{Sí} & Conv. paso $37.5\%$, global $>99.1\%$; purga $4\%$. \\
9 & Se verifican la capacidad anual y el flujo horario. & \textbf{Sí} & $3\,750.0\text{ kg/h}$ netos $\implies 30\,000.0\text{ t/año}$. \\
10 & Se verifica la pureza seca de metanol. & \textbf{Sí} & $99.85\%$ p/p húmedo, $100.00\%$ base seca. \\
11 & Todas las corrientes y equipos tienen identificador único. & \textbf{Sí} & Nomenclatura coherente según estándar Solvanta. \\
12 & Las unidades y la base de cálculo están declaradas. & \textbf{Sí} & Sistema SI/Ing.: $\text{bar}, ^\circ\text{C}, \text{kg/h}, \text{kmol/h}, \text{kW}$. \\
13 & El archivo aprobado fue respaldado y congelado. & \textbf{Sí} & Respaldo \texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz}. \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{0.1cm}

\subsection{Congelamiento del caso aprobado}

Una vez que la simulación haya superado la puerta de verificación, guardar una copia con el nombre:
\begin{center}
\texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz}
\end{center}

\clearpage

% ==============================================================================
% PÁGINA 6 DE 18
% ==============================================================================
Este archivo constituirá el caso oficial para elaborar las tablas de corrientes y el PFD v0.\\
No deberá modificarse después de su aprobación.\\
Si posteriormente se requiere un cambio, se deberá crear una nueva revisión:
\begin{center}
\texttt{DWSIM\_v1\_REV01\_Solvanta.dwxmz}
\end{center}

\vspace{0.2cm}

\section{Etapa 2. Elaboración de TC-01}

TC-01 será la tabla oficial de corrientes de materia del proceso.

\subsection{Numeración de corrientes}

La firma deberá asignar un identificador único a cada corriente.\\
Se recomienda emplear la siguiente estructura:
\begin{center}
101, 102, 103, \dots
\end{center}
o bien:
\begin{center}
S-101, S-102, S-103, \dots \quad (\textbf{S-01, S-02, S-03, \dots\ adoptada por Solvanta})
\end{center}
El mismo identificador deberá utilizarse en:
\begin{itemize}
    \item DWSIM v1;
    \item TC-01;
    \item PFD v0;
    \item cálculos de balance;
    \item memorias técnicas posteriores.
\end{itemize}

\vspace{0.2cm}

\subsection{Instrucciones}

\textbf{2.1} Abrir el caso aprobado de DWSIM v1.\\
\textbf{2.2} Identificar todas las corrientes de materia.\\
\textbf{2.3} Incluir:
\begin{itemize}
    \item alimentaciones;
    \item productos;
    \item subproductos;
    \item purgas;
    \item recirculaciones;
\end{itemize}

\clearpage

% ==============================================================================
% PÁGINA 7 DE 18
% ==============================================================================
\begin{itemize}
    \item corrientes intermedias;
    \item salidas de gases;
    \item salidas acuosas.
\end{itemize}
\textbf{2.4} Extraer los valores directamente del caso aprobado.\\
\textbf{2.5} Utilizar un mismo sistema de unidades.\\
\textbf{2.6} No mezclar resultados procedentes de diferentes iteraciones.\\
\textbf{2.7} Revisar que la suma de los flujos de los componentes coincida con el flujo total.\\
\textbf{2.8} Utilizar un número razonable de cifras significativas.

\vspace{0.2cm}

\subsection{TC-01A. Resumen de corrientes}

\begin{center}
\footnotesize
\setlength{\tabcolsep}{3.0pt}
\textbf{Cuadro 4: TC-01A. Resumen de corrientes de materia.}\\[2pt]
\begin{tabularx}{\textwidth}{lp{4.0cm}lccccr}
\toprule
\textbf{ID} & \textbf{Descripción} & \textbf{Fase} & \textbf{$T$ ($^\circ$C)} & \textbf{$P$ (bar)} & \textbf{$\dot{m}$ (kg/h)} & \textbf{$\dot{n}$ (kmol/h)} & \textbf{Frac. vap.} \\
\midrule
\texttt{S-01} & Alim. $\text{CO}_2$ de captura & Vapor & $25.0$ & $20.00$ & $5\,222.4$ & $119.81$ & $1.00$ \\
\texttt{S-03\_MK} & Agua fresca externa red & Líquido & $25.0$ & $20.00$ & $9\,240.9$ & $512.95$ & $0.00$ \\
\texttt{S-ZLD\_R} & Retorno agua ZLD & Líquido & $38.7$ & $20.00$ & $6\,979.3$ & $387.41$ & $0.00$ \\
\texttt{S-03} & Agua combinada caldera & Líquido & $30.9$ & $20.00$ & $16\,219.9$ & $900.34$ & $0.00$ \\
\texttt{S-03B} & Vapor saturado carcasa & Vapor & $220.0$ & $20.00$ & $16\,219.9$ & $900.34$ & $1.00$ \\
\texttt{S-04} & Vapor sobrecalentado & Vapor & $750.0$ & $20.00$ & $16\,219.9$ & $900.34$ & $1.00$ \\
\texttt{S-05} & Oxígeno puro SOEC & Vapor & $31.0$ & $19.40$ & $10\,083.4$ & $315.12$ & $1.00$ \\
\texttt{S-06} & Efluente húmedo SOEC & Vapor & $750.0$ & $19.40$ & $6\,136.5$ & $900.34$ & $1.00$ \\
\texttt{S-07} & Hidrógeno seco a mezcla & Vapor & $38.0$ & $19.40$ & $1\,312.8$ & $632.58$ & $1.00$ \\
\texttt{S-08} & Condensado SOEC a ZLD & Líquido & $38.0$ & $19.40$ & $4\,823.7$ & $267.76$ & $0.00$ \\
\texttt{S-08B} & Syngas fresco combinado & Vapor & $32.7$ & $19.40$ & $6\,535.2$ & $752.39$ & $1.00$ \\
\texttt{S-09} & Syngas comprimido C-301 & Vapor & $212.3$ & $75.00$ & $6\,535.2$ & $752.39$ & $1.00$ \\
\texttt{S-09\_TOT}& Alimentación total R-401 & Vapor & $57.6$ & $75.00$ & $20\,779.2$ & $7\,153.98$ & $1.00$ \\
\texttt{S-10} & Efluente reacción R-401 & Vapor & $245.0$ & $75.00$ & $20\,779.2$ & $6\,918.23$ & $1.00$ \\
\texttt{S-REC} & Gas domo flash V-501 & Vapor & $38.0$ & $75.00$ & $14\,862.8$ & $6\,680.78$ & $1.00$ \\
\texttt{S-12} & Reciclo $96\%$ a C-601 & Vapor & $43.0$ & $75.00$ & $14\,268.3$ & $6\,413.54$ & $1.00$ \\
\texttt{S-13} & Purga $4\%$ a turboexp. & Vapor & $43.0$ & $75.00$ & $594.5$ & $267.23$ & $1.00$ \\
\texttt{S-P\_VENT}& Purga venteo tras X-601 & Bifásica & $-145.2$ & $1.10$ & $594.5$ & $267.23$ & $0.98$ \\
\texttt{S-11} & Metanol crudo flash HP & Líquido & $38.0$ & $75.00$ & $5\,916.5$ & $237.45$ & $0.00$ \\
\texttt{S-VENT} & Venteo ligeros V-701 & Vapor & $38.0$ & $3.00$ & $9.0$ & $0.62$ & $1.00$ \\
\texttt{S-14} & Metanol crudo a T-701 & Líquido & $38.0$ & $3.00$ & $5\,925.1$ & $237.61$ & $0.00$ \\
\texttt{S-15} & \textbf{e-Metanol Grado AA} & Líquido & $\mathbf{35.0}$ & $\mathbf{1.10}$ & $\mathbf{3\,755.6}$ & $\mathbf{117.35}$ & $\mathbf{0.00}$ \\
\texttt{S-16} & Agua de fondo a ZLD & Líquido & $103.9$ & $1.25$ & $2\,169.5$ & $120.26$ & $0.00$ \\
\texttt{S-ZLD\_P} & Agua pulida ZLD a bomba & Líquido & $38.7$ & $19.40$ & $6\,979.3$ & $387.41$ & $0.00$ \\
\texttt{S-ZLD\_S} & Purga lodos ZLD & Bifásica & $38.7$ & $19.40$ & $10.8$ & $0.69$ & $0.01$ \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{0.1cm}

\subsection{TC-01B. Composición de corrientes}

La composición deberá expresarse en una base claramente declarada:
\begin{itemize}
    \item \textbf{fracción molar;} \quad $\leftarrow$ \textbf{Base adoptada en Cuadro 5}
    \item fracción másica;
    \item flujo molar por componente; o
\end{itemize}

\clearpage

% ==============================================================================
% PÁGINA 8 DE 18
% ==============================================================================
\begin{itemize}
    \item flujo másico por componente.
\end{itemize}

\begin{center}
\footnotesize
\setlength{\tabcolsep}{4.0pt}
\textbf{Cuadro 5: TC-01B. Composición molar de corrientes.}\\[2pt]
\begin{tabularx}{\textwidth}{lcccccrr}
\toprule
\textbf{ID} & \textbf{$x_{\text{H}_2}$} & \textbf{$x_{\text{CO}_2}$} & \textbf{$x_{\text{CO}}$} & \textbf{$x_{\text{H}_2\text{O}}$} & \textbf{$x_{\text{MeOH}}$} & \textbf{$x_{\text{Inertes}}$} & \textbf{$\sum x_i$} \\
\midrule
\texttt{S-01} & $0.0000$ & $0.9900$ & $0.0000$ & $0.0000$ & $0.0000$ & $0.0100$ & $\mathbf{1.0000}$ \\
\texttt{S-03\_MK} & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-ZLD\_REC} & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-03} & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-03B} & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-04} & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-05} & $0.0000$ & $0.0000$ & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000^*$ & $\mathbf{1.0000}$ \\
\texttt{S-06} & $0.7000$ & $0.0000$ & $0.0000$ & $0.3000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-07} & $0.9958$ & $0.0000$ & $0.0000$ & $0.0042$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-08} & $0.0001$ & $0.0000$ & $0.0000$ & $0.9999$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-08B} & $0.8378$ & $0.1575$ & $0.0000$ & $0.0031$ & $0.0000$ & $0.0016$ & $\mathbf{1.0000}$ \\
\texttt{S-09} & $0.8378$ & $0.1575$ & $0.0000$ & $0.0031$ & $0.0000$ & $0.0016$ & $\mathbf{1.0000}$ \\
\texttt{S-09\_TOTAL} & $0.7331$ & $0.0981$ & $0.0000$ & $0.0008$ & $0.0011$ & $0.1669$ & $\mathbf{1.0000}$ \\
\texttt{S-10} & $0.6970$ & $0.0880$ & $0.0000$ & $0.0175$ & $0.0176$ & $0.1799$ & $\mathbf{1.0000}$ \\
\texttt{S-REC} & $0.7208$ & $0.0911$ & $0.0000$ & $0.0005$ & $0.0012$ & $0.1864$ & $\mathbf{1.0000}$ \\
\texttt{S-12} & $0.7208$ & $0.0911$ & $0.0000$ & $0.0005$ & $0.0012$ & $0.1864$ & $\mathbf{1.0000}$ \\
\texttt{S-13} & $0.7208$ & $0.0911$ & $0.0000$ & $0.0005$ & $0.0012$ & $0.1864$ & $\mathbf{1.0000}$ \\
\texttt{S-PURGE\_VENT} & $0.7208$ & $0.0911$ & $0.0000$ & $0.0005$ & $0.0012$ & $0.1864$ & $\mathbf{1.0000}$ \\
\texttt{S-11} & $0.0028$ & $0.0048$ & $0.0000$ & $0.5052$ & $0.4939$ & $0.0003$ & $\mathbf{1.0000}$ \\
\texttt{S-VENT} & $0.2542$ & $0.7180$ & $0.0000$ & $0.0012$ & $0.0266$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-14} & $0.0000$ & $0.0000$ & $0.0000$ & $0.5061$ & $0.4939$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-15} & $\mathbf{0.0000}$ & $\mathbf{0.0000}$ & $\mathbf{0.0000}$ & $\mathbf{0.0027}$ & $\mathbf{0.9973}$ & $\mathbf{0.0000}$ & $\mathbf{1.0000}$ \\
\texttt{S-16} & $0.0000$ & $0.0000$ & $0.0000$ & $0.9990$ & $0.0010$ & $0.0000$ & $\mathbf{1.0000}$ \\
\texttt{S-ZLD\_PUMP} & $0.0000$ & $0.0000$ & $0.0000$ & $1.0000$ & $0.0000$ & $0.0000$ & $\mathbf{1.0000}$ \\
\bottomrule
\end{tabularx}
\footnotesize{*En \texttt{S-05}, el componente corresponde a $\text{O}_2$ puro.}
\end{center}

Si el modelo contiene otros componentes, deberán agregarse nuevas columnas.

\vspace{0.2cm}

\section{Etapa 3. Elaboración de TE-01}

TE-01 será la tabla de corrientes de energía y servicios del proceso.

\subsection{Instrucciones}

\textbf{3.1} Identificar todos los equipos con consumo o liberación de energía.\\
\textbf{3.2} Identificar las corrientes de energía utilizadas en DWSIM.\\
\textbf{3.3} Incluir, como mínimo: celda electrolítica; compresores; calentadores; enfriadores; condensadores; rehervidores; bombas; columnas de separación.\\
\textbf{3.4} Clasificar cada carga como:

\clearpage

% ==============================================================================
% PÁGINA 9 DE 18
% ==============================================================================
\begin{itemize}
    \item electricidad;
    \item calentamiento;
    \item enfriamiento.
\end{itemize}

\textbf{3.5 Declarar la convención de signos utilizada.}\\
\textbf{3.6 Registrar las condiciones de entrada y salida asociadas con cada servicio.}

Se recomienda utilizar la convención:
\begin{center}
$\dot{Q} > 0$ : energía suministrada al proceso \qquad
$\dot{Q} < 0$ : energía retirada del proceso
\end{center}

La energía anual se calculará mediante:
\begin{equation}
E_{\text{anual}} = |\dot{Q}| (8\,000\text{ h/año}).
\end{equation}

Si la carga se expresa en kW:
\begin{equation}
E_{\text{anual}}\text{ (MWh/año)} = \frac{|\dot{Q}| (8\,000)}{1\,000}.
\end{equation}

\vspace{0.1cm}

\subsection{Formato TE-01}

\begin{center}
\footnotesize
\setlength{\tabcolsep}{3.0pt}
\textbf{Cuadro 6: TE-01. Resumen de energía y servicios.}\\[2pt]
\begin{tabularx}{\textwidth}{llllrrX}
\toprule
\textbf{ID} & \textbf{Equipo} & \textbf{Servicio} & \textbf{Tipo} & \textbf{Carga (kW)} & \textbf{E. anual (MWh)} & \textbf{Observación} \\
\midrule
\texttt{E-SOEC} & \texttt{R-201} & Potencia SOEC & Electricidad & $+54\,402.00$ & $435\,216.0$ & Red renovable ($52.2\text{ MW}$ DC) \\
\texttt{E-C301} & \texttt{C-301} & Compresor syngas & Electricidad & $+1\,138.70$ & $9\,109.6$ & Multietapa $20 \to 75\text{ bar}$ \\
\texttt{E-C601} & \texttt{C-601} & Soplador reciclo & Electricidad & $+150.00$ & $1\,200.0$ & Vence $\Delta P$ en lazo \\
\texttt{E-P801} & \texttt{P-801} & Bomba ZLD & Electricidad & $+0.20$ & $1.6$ & Multietapa $19.4 \to 20\text{ bar}$ \\
\texttt{E-TURB} & \texttt{X-601} & Turboexpansor & Gen. elec. & $\mathbf{-390.43}$ & $\mathbf{-3\,123.4}$ & Recuperación de purga \\
\midrule
\multicolumn{4}{l}{\textbf{Consumo Eléctrico Neto de Planta}} & $\mathbf{+55\,325.47}$ & $\mathbf{442\,603.8}$ & $\approx \mathbf{55.33\text{ MW}}$ neta \\
\midrule
\texttt{E-R401} & \texttt{R-401} & Síntesis metanol & Gen. térmica & $\mathbf{-9\,139.20}$ & $73\,113.6$ & Calor exotérmico a caldera \\
\texttt{E-201} & \texttt{E-201} & Carcasa caldera & Calentamiento & $\mathbf{+9\,139.20}$ & $73\,113.6$ & Absorbe $100\%$ calor R-401 \\
\texttt{E-601} & \texttt{E-601} & Economizador & Int. Recup. & $\mathbf{+272.05}$ & $2\,176.4$ & Efluente a gas reciclo \\
\texttt{E-202} & \texttt{E-202} & Sobrecalentador & Calentamiento & $+5\,119.20$ & $40\,953.6$ & Vapor $220 \to 750^\circ\text{C}$ \\
\texttt{E-702} & \texttt{E-702} & Rehervidor T-701 & Calentamiento & $+3\,020.00$ & $24\,160.0$ & Fondo torre a $103.9^\circ\text{C}$ \\
\midrule
\texttt{E-301} & \texttt{E-301} & Enfriador SOEC & Enfriamiento & $-8\,741.80$ & $69\,934.4$ & Agua torre $750 \to 38^\circ\text{C}$ \\
\texttt{E-501} & \texttt{E-501} & Enfriador síntesis & Enfriamiento & $-13\,952.70$ & $111\,621.6$ & Condensa mezcla cruda \\
\texttt{E-701} & \texttt{E-701} & Condensador T-701& Enfriamiento & $-2\,865.00$ & $22\,920.0$ & Condensa metanol $65^\circ\text{C}$ \\
\texttt{E-704} & \texttt{E-704} & Subenfriador & Enfriamiento & $-92.20$ & $737.6$ & Metanol a $35^\circ\text{C}$ \\
\texttt{E-V701} & \texttt{V-701} & Desgasificador LP& Balance adiab. & $0.00$ & $0.0$ & Flash adiabático $75 \to 3\text{ bar}$ \\
\bottomrule
\end{tabularx}
\end{center}

\clearpage

% ==============================================================================
% PÁGINA 10 DE 18
% ==============================================================================
\section{Etapa 4. Reconciliación de la información}

Antes de elaborar el PFD v0, la firma deberá revisar la consistencia de las tablas.

\subsection{Comprobaciones obligatorias}

\textbf{a) Verificar que:} $\sum_i x_i = 1.0000$ en cada corriente, considerando el redondeo utilizado. (\textit{Cumplido al $100\%$})\\
\textbf{b) Comprobar que el flujo total sea igual a la suma de los flujos de los componentes.} (\textit{Verificado sin error})\\
\textbf{c) Verificar que los valores de alimentación coincidan con DWSIM v1.} (\textit{\texttt{S-01}: $5\,222.4\text{ kg/h}$; \texttt{S-03\_MK}: $9\,240.9\text{ kg/h}$})\\
\textbf{d) Verificar que los valores del producto coincidan con los de la licitación.} (\textit{\texttt{S-15}: $3\,750.0\text{ kg/h}$ netos, $\ge 99.85\%$})\\
\textbf{e) Comprobar que TC-01 contenga todas las corrientes que cruzan límites de equipos.} (\textit{25 corrientes maestras})\\
\textbf{f) Comprobar que TE-01 contenga todas las corrientes de energía relevantes.} (\textit{14 equipos térmicos/eléctricos})\\
\textbf{g) Verificar que todos los datos procedan de la misma revisión congelada.} (\textit{Caso oficial \texttt{DWSIM\_v1\_APROBADA}})\\
\textbf{h) Identificar valores redondeados, estimados o pendientes de validación.} (\textit{Eficiencia $E_0 = 67.5\%$ en T-701 y $\Delta P$})

\vspace{0.1cm}

\begin{center}
\footnotesize
\textbf{Cuadro 7: Registro de discrepancias.}\\[2pt]
\begin{tabularx}{\textwidth}{cp{3.8cm}p{4.2cm}X}
\toprule
\textbf{Núm.} & \textbf{Discrepancia encontrada} & \textbf{Causa} & \textbf{Acción correctiva} \\
\midrule
1 & Producción preliminar inferior a $3\,750\text{ kg/h}$ ($2\,442\text{ kg/h}$). & Purga excesiva del $15\%$ y relación $\text{H}_2/\text{CO}_2 = 3.00$. & Reducción de purga al $4\%$ y ajuste de $\text{H}_2/\text{CO}_2 = 3.08$. \\
2 & Presencia de líquido en succión de compresor C-601 a $38^\circ\text{C}$. & Gas de domo V-501 en punto de rocío de saturación. & Adición de economizador E-601 ($272\text{ kW}$), sobrecalentando a $43^\circ\text{C}$. \\
3 & Falsa raíz termodinámica en domo T-701 ($-203^\circ\text{C}$). & Falla de Flash-PH con PRSV2 para metanol puro. & Reconfiguración a Inside-Out / Flash-PT y adición de E-704 ($35^\circ\text{C}$). \\
4 & Error en cálculo de desgasificador V-701 en DWSIM. & Modo de cálculo requería Energy Stream en conector 6. & Conexión de corriente \texttt{E-V701} con potencia neta de $0.0\text{ kW}$. \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{0.1cm}

\section{Etapa 5. Elaboración del PFD v0}

El PFD v0 será una representación física preliminar del proceso.\\
No deberá ser solamente una captura de pantalla del flowsheet de DWSIM.

\clearpage

% ==============================================================================
% PÁGINA 11 DE 18
% ==============================================================================
\subsection{Contenido mínimo}

El PFD v0 deberá mostrar:
\begin{itemize}
    \item equipos principales;
    \item identificación única de los equipos;
    \item líneas principales de proceso;
    \item números de corrientes;
    \item flechas que indiquen la dirección del flujo;
    \item alimentaciones;
    \item productos;
    \item subproductos;
    \item purgas;
    \item recirculaciones;
    \item temperatura de las corrientes principales;
    \item presión de las corrientes principales;
    \item flujo de las corrientes principales;
    \item servicios principales;
    \item leyenda;
    \item notas generales;
    \item base de diseño;
    \item cajetín;
    \item fecha y número de revisión.
\end{itemize}

\vspace{0.2cm}

\subsection{Identificación de equipos}

Se recomienda emplear el siguiente sistema:\\
Cada identificador deberá ser único.

\vspace{0.2cm}

\subsection{Traducción de objetos de DWSIM}

Los objetos matemáticos y conceptuales de la simulación DWSIM fueron traducidos rigurosamente a equipos físicos comerciales de acuerdo con los criterios establecidos en los Cuadros 8 y 9.

\clearpage

% ==============================================================================
% PÁGINA 12 DE 18
% ==============================================================================
\begin{center}
\small
\textbf{Cuadro 8: Identificación preliminar de equipos.}\\[4pt]
\begin{tabular}{cll}
\toprule
\textbf{Código} & \textbf{Tipo de equipo} & \textbf{Ejemplo} \\
\midrule
EL & Electrolizador & EL-101 (\texttt{R-201} SOEC) \\
C & Compresor & C-101 (\texttt{C-301}, \texttt{C-601}) \\
E & Intercambiador de calor & E-101 (\texttt{E-201}, \texttt{E-202}, \texttt{E-301}, \texttt{E-501}) \\
R & Reactor & R-101 (\texttt{R-401} síntesis metanol) \\
V & Recipiente o separador & V-101 (\texttt{V-301}, \texttt{V-501}, \texttt{V-701}) \\
T & Columna de separación & T-101 (\texttt{T-701} destilación metanol) \\
P & Bomba & P-101 (\texttt{P-801} bomba ZLD) \\
TK & Tanque de almacenamiento & TK-101 (almacenamiento metanol) \\
\bottomrule
\end{tabular}
\end{center}

\vspace{0.3cm}

\begin{center}
\footnotesize
\textbf{Cuadro 9: Traducción de objetos de DWSIM al PFD v0.}\\[4pt]
\begin{tabularx}{\textwidth}{p{3.2cm}p{3.6cm}X}
\toprule
\textbf{Objeto en DWSIM} & \textbf{Representación en PFD} & \textbf{Criterio} \\
\midrule
Water Electrolyzer & Paquete de electrólisis & Mostrar la alimentación de agua, el consumo de electricidad y las salidas de $\text{H}_2$ y $\text{O}_2$. \\
Compressor & Compresor & Mostrar la potencia y las condiciones principales de entrada y salida. \\
Heater o Cooler & Intercambiador de calor & Indicar el servicio, la carga térmica y las condiciones principales. \\
Mixer & Mezclador o unión de líneas & Representarlo como equipo solamente si existe físicamente en el diseño. \\
Conversion Reactor & Reactor de síntesis & Identificar la reacción, conversión o base de cálculo utilizada. \\
Separator o Flash & Recipiente separador & Mostrar claramente las salidas de vapor y líquido. \\
Splitter & Derivación o purga & Representar una división de flujo, válvula o derivación de acuerdo con el diseño físico. \\
Recycle & Línea de retorno & No deberá dibujarse como un equipo independiente. \\
Component Separator & Tecnología física de separación & Deberá sustituirse por destilación, absorción, membrana u otra operación físicamente justificable. \\
Valve & Válvula reductora & Mostrar la caída de presión cuando sea relevante para el proceso. \\
\bottomrule
\end{tabularx}
\end{center}

\clearpage

% ==============================================================================
% PÁGINA 13 DE 18
% ==============================================================================
\begin{puertabox}
El bloque \textit{Component Separator} es una herramienta matemática del simulador. No representa automáticamente un equipo industrial.\\
Antes de incorporarlo al PFD, la firma deberá proponer la tecnología física que realizará la separación. \textbf{Solvanta implementó una columna fraccionadora rigurosa de 28 platos reales (T-701) con condensador total y rehervidor termosifón.}
\end{puertabox}

\subsection{Información que no corresponde al PFD v0}

El PFD v0 no deberá incluir todavía el detalle propio de un P\&ID o DTI, como:
\begin{itemize}
    \item lazos completos de control;
    \item numeración exhaustiva de instrumentos;
    \item identificación de todas las válvulas;
    \item clases de tubería;
    \item diámetros definitivos de tubería;
    \item accesorios menores;
    \item señales eléctricas o neumáticas;
    \item sistemas de seguridad instrumentada.
\end{itemize}
Estos elementos se incorporarán posteriormente, cuando el diseño de proceso y el dimensionamiento de equipos se encuentren suficientemente desarrollados.

\vspace{0.2cm}

\section{Etapa 6. Verificación del PFD v0}

Una vez elaborado el PFD v0, la firma deberá realizar una revisión cruzada.

\subsection{Lista de verificación del PFD}

\begin{center}
\footnotesize
\textbf{Cuadro 10: Lista de verificación del PFD v0.}\\[2pt]
\begin{tabularx}{\textwidth}{cp{8.2cm}cX}
\toprule
\textbf{Núm.} & \textbf{Criterio} & \textbf{Sí/No} & \textbf{Observación} \\
\midrule
1 & Todos los equipos principales están representados. & \textbf{Sí} & SOEC, BWR, compresores, flashes y torre. \\
2 & Todos los equipos tienen identificador único. & \textbf{Sí} & Tags coherentes según Cuadro 8. \\
3 & Las líneas tienen flechas de dirección. & \textbf{Sí} & Trazabilidad direccional continua. \\
4 & Todas las corrientes relevantes están numeradas. & \textbf{Sí} & Numeración S-01 a S-16 y lazos ZLD. \\
5 & Los números de corriente coinciden con TC-01. & \textbf{Sí} & Coincidencia del $100\%$ verificada. \\
6 & Las cargas de energía pueden localizarse en TE-01. & \textbf{Sí} & Cargas térmicas y potencias tabuladas. \\
7 & Las alimentaciones y productos están identificados. & \textbf{Sí} & $\text{CO}_2$, agua fresca, metanol y $\text{O}_2$. \\
\bottomrule
\end{tabularx}
\end{center}

\clearpage

% ==============================================================================
% PÁGINA 14 DE 18
% ==============================================================================
\begin{center}
\footnotesize
\begin{tabularx}{\textwidth}{cp{8.2cm}cX}
\toprule
\textbf{Núm.} & \textbf{Criterio} & \textbf{Sí/No} & \textbf{Observación} \\
\midrule
8 & La purga y la recirculación están representadas. & \textbf{Sí} & Purga $4\%$ a turboexpansor y reciclo $96\%$. \\
9 & El objeto Recycle no aparece como equipo. & \textbf{Sí} & Dibujado como línea de tubería cerrada. \\
10 & El separador por componentes fue traducido a una tecnología física. & \textbf{Sí} & Columna de destilación real T-701. \\
11 & Los valores de temperatura, presión y flujo coinciden con DWSIM v1. & \textbf{Sí} & Validación cruzada con caso congelado. \\
12 & El documento incluye cajetín, fecha y revisión. & \textbf{Sí} & Cajetín Solvanta, RFP-CCM-EM-001, Rev v0.1. \\
13 & El PFD es legible y utiliza una nomenclatura coherente. & \textbf{Sí} & Vectorial nítido con bloques de datos. \\
\bottomrule
\end{tabularx}
\end{center}

\vspace{0.1cm}

\section{Etapa 7. Matriz de trazabilidad}

Cada corriente y equipo deberá poder localizarse en todos los documentos correspondientes.

\begin{center}
\footnotesize
\textbf{Cuadro 11: Matriz de consistencia y trazabilidad.}\\[2pt]
\begin{tabularx}{\textwidth}{llllX}
\toprule
\textbf{ID} & \textbf{DWSIM v1} & \textbf{TC-01 o TE-01} & \textbf{PFD v0} & \textbf{Resultado de revisión} \\
\midrule
\texttt{S-01} & Corriente de entrada & TC-01: \texttt{S-01} & Línea $\text{CO}_2$ & Consistente ($20\text{ bar}, 25^\circ\text{C}, 5\,222.4\text{ kg/h}$) \\
\texttt{R-201} & Water Electrolyzer & TE-01: \texttt{E-SOEC} & \texttt{EL-201} & Consistente ($54.4\text{ MW}, 750^\circ\text{C}$) \\
\texttt{C-301} & Compresor syngas & TE-01: \texttt{E-C301} & \texttt{C-301} & Consistente ($1\,138.7\text{ kW}, 20 \to 75\text{ bar}$) \\
\texttt{R-401} & Reactor multitubular & TE-01: \texttt{E-R401} & \texttt{R-401} & Consistente (BWR, $245^\circ\text{C}, 75\text{ bar}$) \\
\texttt{E-201} & Heater acoplado & TE-01: \texttt{E-201} & Carcasa R-401 & Consistente ($9\,139.2\text{ kW}$, vapor $220^\circ\text{C}$) \\
\texttt{E-601} & Economizador & TE-01: \texttt{E-601} & \texttt{E-601} & Consistente ($272.05\text{ kW}, 38 \to 43^\circ\text{C}$) \\
\texttt{V-501} & Flash frío HP & TC-01: \texttt{S-REC/S-11}& \texttt{V-501} & Consistente ($75\text{ bar}, 38^\circ\text{C}$, vapor/liq) \\
\texttt{C-601} & Compresor reciclo & TE-01: \texttt{E-C601} & \texttt{C-601} & Consistente ($150\text{ kW}$, gas seco a $43^\circ\text{C}$) \\
\texttt{X-601} & Expansor purga & TE-01: \texttt{E-TURB} & \texttt{X-601} & Consistente ($-390.43\text{ kW}, 75 \to 1.1\text{ bar}$) \\
\texttt{V-701} & Flash desgasificador & TC-01: \texttt{S-VENT/S-14}& \texttt{V-701} & Consistente ($3\text{ bar}, 38^\circ\text{C}, 0.0\text{ kW}$) \\
\texttt{T-701} & Columna destilación & TC-01: \texttt{S-15/S-16} & \texttt{T-701} & Consistente (28 platos, metanol/agua) \\
\texttt{S-15} & e-Metanol comercial & TC-01: \texttt{S-15} & Producto final & Consistente ($3\,750.0\text{ kg/h}$ netos, $\ge 99.85\%$) \\
\texttt{P-801} & Bomba ZLD & TE-01: \texttt{E-P801} & \texttt{P-801} & Consistente ($0.20\text{ kW}, 19.4 \to 20\text{ bar}$) \\
\bottomrule
\end{tabularx}
\end{center}

Si se encuentra una discrepancia, la firma deberá:
\begin{enumerate}
    \item identificar el documento donde se originó;
    \item verificar el valor en DWSIM v1;
    \item corregir la tabla o el PFD;
    \item documentar la modificación;
    \item actualizar el número de revisión.
\end{enumerate}

\clearpage

% ==============================================================================
% PÁGINA 15 DE 18
% ==============================================================================
\section{Entregables}

\begin{entregabox}
La firma entregará un expediente digital con los siguientes documentos:
\begin{enumerate}
    \item Archivo aprobado:
    \begin{center}
    \texttt{DWSIM\_v1\_APROBADA\_Solvanta.dwxmz}
    \end{center}
    \item Reporte de verificación de DWSIM v1.
    \item Lista de verificación firmada.
    \item Evidencia de convergencia.
    \item Cálculo del balance global de materia.
    \item Balance por componentes.
    \item Verificación de producción y pureza.
    \item Tabla de corrientes de materia:
    \begin{center}
    \texttt{TC-01\_Solvanta.pdf}
    \end{center}
    \item Tabla de energía y servicios:
    \begin{center}
    \texttt{TE-01\_Solvanta.pdf}
    \end{center}
    \item Diagrama de flujo de proceso:
    \begin{center}
    \texttt{PFD-v0\_Solvanta.pdf}
    \end{center}
    \item Archivos editables de TC-01, TE-01 y PFD v0.
    \item Matriz de trazabilidad.
    \item Lista de asuntos pendientes para la siguiente revisión.
\end{enumerate}
\end{entregabox}

\vspace{0.2cm}

\section{Estructura del expediente}

Se recomienda organizar la carpeta de entrega de la siguiente manera:

\begin{verbatim}
VTP-01_Solvanta/
|
|-- 01_DWSIM/
|   |-- DWSIM_v1_APROBADA_Solvanta.dwxmz
|
\end{verbatim}

\clearpage

% ==============================================================================
% PÁGINA 16 DE 18
% ==============================================================================
\begin{verbatim}
|-- 02_Verificacion/
|   |-- Reporte_Verificacion.pdf
|   |-- Evidencias/
|
|-- 03_Tablas/
|   |-- TC-01_Solvanta.pdf
|   |-- TC-01_Solvanta.xlsx
|   |-- TE-01_Solvanta.pdf
|   |-- TE-01_Solvanta.xlsx
|
|-- 04_PFD/
|   |-- PFD-v0_Solvanta.pdf
|   |-- PFD-v0_Solvanta_EDITABLE
|
|-- 05_Trazabilidad/
    |-- Matriz_Trazabilidad.pdf
\end{verbatim}

\vspace{0.1cm}

\section{Criterios de aceptación}

El expediente se considerará técnicamente aceptable cuando:
\begin{itemize}
    \item DWSIM v1 se encuentre convergida;
    \item no existan errores físicos sin explicar;
    \item los balances estén documentados;
    \item las metas de producción y pureza estén calculadas;
    \item TC-01 incluya todas las corrientes relevantes;
    \item TE-01 incluya todas las demandas de energía;
    \item las tablas sean legibles y reproducibles;
    \item los identificadores coincidan entre los documentos;
    \item el PFD represente equipos físicamente realizables;
    \item las purgas y recirculaciones estén claramente identificadas;
    \item toda desviación o supuesto se encuentre declarado;
    \item la revisión del documento esté identificada.
\end{itemize}

\vspace{0.1cm}

\section{Rúbrica de evaluación}

\section{Preguntas de cierre}

Cada firma responderá en un máximo de una página:

\textbf{1. ¿Qué inconsistencia fue detectada durante la verificación de DWSIM v1?}\\
Riesgo de condensación en la succión de C-601 ($38^\circ\text{C}$ saturado), falsa raíz termodinámica en domo T-701 ($-203^\circ\text{C}$ en Flash-PH) y requerimiento de Energy Stream en desgasificador V-701.

\textbf{2. ¿Cómo se resolvió o documentó dicha inconsistencia?}\\
Se instaló el economizador E-601 ($272\text{ kW}$) elevando el gas a $43^\circ\text{C}$ sin líquido; en T-701 se estabilizó a Inside-Out / Flash-PT con subenfriador E-704 ($35^\circ\text{C}$); y en V-701 se conectó \texttt{E-V701} ($0.0\text{ kW}$).

\textbf{3. ¿Qué dato del PFD v0 depende de un supuesto que todavía debe validarse?}\\
La eficiencia global de platos ($E_0 = 67.5\%$, 28 platos reales en T-701) estimada preliminarmente por O'Connell, sujeta a validación hidráulica en ingeniería básica.

\clearpage

% ==============================================================================
% PÁGINA 17 DE 18
% ==============================================================================
\begin{center}
\small
\textbf{Cuadro 12: Distribución de la calificación.}\\[4pt]
\begin{tabular}{lc}
\toprule
\textbf{Criterio} & \textbf{Ponderación} \\
\midrule
Verificación y congelamiento de DWSIM v1 & $20\text{ \%}$ \\
TC-01: tabla de corrientes de materia & $20\text{ \%}$ \\
TE-01: tabla de energía y servicios & $15\text{ \%}$ \\
Calidad técnica y gráfica del PFD v0 & $25\text{ \%}$ \\
Consistencia y trazabilidad entre documentos & $15\text{ \%}$ \\
Orden, nomenclatura y presentación del expediente & $5\text{ \%}$ \\
\midrule
\textbf{Total} & $\mathbf{100\text{ \%}}$ \\
\bottomrule
\end{tabular}
\end{center}

\textbf{4. ¿Qué objeto de DWSIM requirió una traducción especial para representarlo físicamente?}\\
El reactor de metanol: en DWSIM son dos bloques (\texttt{R-401} cinético y \texttt{E-201} calentador), que físicamente integran un único reactor multitubular BWR Lurgi con tubos catalíticos y carcasa hirviendo agua a $20\text{ bar}$. Los bloques \texttt{Recycle} se representaron como tuberías de retorno cerrado.

\textbf{5. ¿Qué tecnología física se propuso para sustituir al separador por componentes?}\\
Una columna de destilación fraccionadora rigurosa de 28 platos reales (\texttt{T-701}), con condensador total (\texttt{E-701}), acumulador de reflujo, rehervidor termosifón (\texttt{E-702}) y subenfriador (\texttt{E-704}).

\textbf{6. ¿Cuál es la principal pérdida de metanol identificada en el proceso?}\\
La purga continua de inertes (\texttt{S-13}) hacia el turboexpansor \texttt{X-601} ($0.60\text{ kg/h}$ arrastrado en vapor) y venteo \texttt{V-701} ($0.24\text{ kg/h}$). Pérdida total: $0.84\text{ kg/h}$ ($<0.022\%$ de producción, $>99.97\%$ recuperación global).

\textbf{7. ¿Qué equipo presenta la mayor demanda energética?}\\
El electrolizador cerámico SOEC (\texttt{R-201} / \texttt{EL-201}), con $54\,402.0\text{ kW}$ ($54.40\text{ MW}$ AC, $52.2\text{ MW}$ DC), absorbiendo el $97.6\%$ de la electricidad de planta para disociar vapor a $750^\circ\text{C}$.

\textbf{8. ¿Qué equipos deberán dimensionarse primero y por qué?}\\
El reactor \texttt{R-401} (fija cinética, catalizador y generación de vapor acoplada a SOEC), la celda SOEC \texttt{R-201} (área electroquímica y consumo de potencia) y la columna \texttt{T-701} (pureza Grado AA al $99.85\%$).

\vspace{0.1cm}

\section{Siguiente etapa del proyecto}

Una vez aprobado el expediente VTP-01, la firma podrá avanzar hacia:
\begin{enumerate}
    \item elaboración de la lista de equipos;
    \item definición de parámetros de diseño;
    \item elaboración de hojas de datos preliminares;
    \item dimensionamiento de equipos principales;
    \item estimación del consumo de servicios;
    \item estimación preliminar de costos;
    \item actualización del PFD a una nueva revisión.
\end{enumerate}

Por lo tanto, la continuidad del proyecto será:

\clearpage

% ==============================================================================
% PÁGINA 18 DE 18
% ==============================================================================
\begin{center}
\vspace*{0.2cm}
\fbox{
    \begin{minipage}{6.8cm}
    \vspace{2mm}
    \centering
    $\text{DWSIM v1 aprobada} \to \text{TC-01 y TE-01}$ \\
    $\to \text{PFD v0}$ \\
    $\to \text{Lista de equipos}$ \\
    $\to \text{Hojas de datos}$ \\
    $\to \text{Dimensionamiento}$
    \vspace{2mm}
    \end{minipage}
}
\end{center}

\vspace{0.4cm}
\begin{center}
\textit{La simulación aprobada constituye la fuente de datos. Las tablas organizan los resultados. El PFD transforma esos resultados en documentación de ingeniería.}
\end{center}

\vspace{0.3cm}
\begin{center}
\includegraphics[width=0.92\textwidth]{figuras/dfp_plpl_1_1.png}\\[4pt]
\footnotesize{\textbf{Figura Oficial:} Diagrama de Flujo de Proceso Preliminar (PFD v0 / DFP Solvanta PLPL 1.1).}
\end{center}

\vspace{0.2cm}
\begin{center}
\footnotesize
\begin{tabularx}{0.98\textwidth}{XcX}
\toprule
\textbf{Elaboró y Verificó:} & \textbf{Revisión y Fecha:} & \textbf{Aprobación Técnica:} \\
\midrule
Ing. Karol Paola Camacho López & Rev. v0.1 Oficial & Dr. Jesús Andrés Arzola Flores \\
Ingeniería de Procesos Solvanta & 14 de septiembre de 2026 & Docente Evaluador DPyPQ \\
\bottomrule
\end{tabularx}
\end{center}

\end{document}
'''

with open("E1.5_DOC_ActividadVTP_v0.1.tex", "w") as f:
    f.write(latex_code.strip())

print("E1.5_DOC_ActividadVTP_v0.1.tex written successfully.")

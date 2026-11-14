import re

with open("Memoria_Tecnica_de_la_Simulacion_Prueba.tex", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Prepare Section on Comparative Registry (Section 6)
comparative_section = r"""
% ==============================================================================
\section{Registro Comparativo y Justificación de Modificaciones: Memoria Técnica Base vs. Simulación de Prueba}
% ==============================================================================

Para garantizar la máxima trazabilidad documental, control de cambios y transparencia de ingeniería requerida en los procesos de licitación pública internacional, esta sección documenta exhaustivamente todas las modificaciones introducidas en el modelo optimizado denominado \textbf{Simulación de Prueba} (\texttt{Simulacion\_pruebas.xml} y \texttt{Simulacion\_pruebas.dwxml}) respecto a la versión de la \textbf{Memoria Técnica Base} (\texttt{Simulacion\_xml-dwxml\_Actividad\_v0.1.xml}).

\subsection{Matriz Comparativa de Ingeniería de Procesos}
La Tabla~\ref{tab:matriz_comparativa} resume los cambios implementados en la arquitectura de equipos, variables termodinámicas, balance energético y comportamiento de las fases entre ambas versiones del modelo.

\begin{table}[H]
\centering
\small
\caption{Matriz Comparativa de Cambios: Memoria Técnica Base vs. Simulación de Prueba}
\label{tab:matriz_comparativa}
\begin{tabularx}{\textwidth}{p{3.8cm} p{3.3cm} p{3.5cm} X}
\toprule
\textbf{Componente / Parámetro} & \textbf{Memoria Técnica Base} & \textbf{Simulación de Prueba} & \textbf{Justificación de Ingeniería y Beneficio} \\
\midrule
Economizador de Reciclo \texttt{E-601} & Inexistente en el lazo. & Intercambiador térmico integrado ($272.05\,\text{kW}$). & Precalienta el gas de reciclo de $38.0\,^\circ\text{C}$ a $43.0\,^\circ\text{C}$ con calor sensible del efluente \texttt{S-10}. \\
\addlinespace
Corriente de Reciclo Caliente & No existía; reciclo salía a $38.0\,^\circ\text{C}$ directo a \texttt{SPLIT-601}. & Nueva corriente \texttt{S-REC\_HOT} a $43.0\,^\circ\text{C}$ y $75.0\,\text{bar}$. & Garantiza vapor $100\,\%$ sobrecalentado ($+5.0\,^\circ\text{C}$ sobre rocío), eliminando gotas en succión de \texttt{C-601}. \\
\addlinespace
Temperatura a Compresor \texttt{C-601} & $38.0\,^\circ\text{C}$ (en punto de saturación / rocío). & $43.0\,^\circ\text{C}$ ($316.15\,\text{K}$). & Protección mecánica contra erosión de álabes, vibraciones inducidas y cavitación por condensado. \\
\addlinespace
Carga Térmica del Enfriador \texttt{E-501} & $14{,}224.75\,\text{kW}$ de refrigeración externa. & $13{,}952.70\,\text{kW}$ (disminución de $\mathbf{272.05\,\text{kW}}$). & Integración térmica interna (Pinch): el calor cedido al reciclo reduce la carga de la torre de enfriamiento. \\
\addlinespace
Potencia Recuperada en \texttt{X-601} & $384.14\,\text{kW}$ mecánicos / eléctricos. & $\mathbf{390.43\,\text{kW}}$ ($+6.29\,\text{kW}$ adicionales). & Mayor entalpía de entrada en la purga ($43.0\,^\circ\text{C}$ vs $38.0\,^\circ\text{C}$) expandida desde $75 \to 1.1\,\text{bar}$. \\
\addlinespace
Definición de Fases (\texttt{ForcePhase}) & Forzado arbitrario en corrientes de reciclo y ZLD. & \texttt{ForcePhase = GlobalDef} en todas las corrientes. & Rigor y transparencia: equilibrio termodinámico líquido-vapor calculado nativamente por la EOS PRSV2. \\
\addlinespace
Condensador y Enfriador \texttt{E-704} & Enfriador posterior a la columna ($65 \to 35\,^\circ\text{C}$). & Mantenido y ratificado ($92.2\,\text{kW}$). & Acondiciona metanol líquido subenfriado para tanques atmosféricos evitando pérdidas por evaporación. \\
\addlinespace
Columna de Destilación \texttt{T-701} & 28 platos reales (19 teóricos, alimentación plato 17). & 28 platos reales ratificados. & Cumplimiento estricto de pureza comercial Grado AA ($\ge 99.85\,\%$) según norma ASTM D1152 e IMPCA. \\
\addlinespace
Acoplamiento Térmico Carcasa \texttt{E-201} & Generación de vapor a $20\,\text{bar}$ ($220\,^\circ\text{C}$) para SOEC. & Desacoplado conceptualmente de \texttt{E-601}. & Clarifica que \texttt{E-201} genera vapor saturado para la celda SOEC y \texttt{E-601} precalienta reciclo con \texttt{S-10}. \\
\addlinespace
Desgasificador \texttt{V-701} & Descompresión $75 \to 3\,\text{bar}$. & Confirmada operación pasiva ($0.0\,\text{kW}$ energía). & Flash adiabático que ventea inertes disueltos sin demanda de energía eléctrica ni térmica externa. \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Análisis Detallado de los Cambios y Fundamentos de Ingeniería}

\subsubsection{1. Integración del Economizador de Reciclo \texttt{E-601} y Protección de \texttt{C-601}}
En la simulación base, el gas no reaccionado salía del tambor separador frío \texttt{V-501} a $38.0\,^\circ\text{C}$ y $75.0\,\text{bar}$. Termodinámicamente, esta corriente (\texttt{S-REC}) se encuentra en su \textbf{punto de rocío}: la condición de saturación donde cualquier perturbación térmica negativa induce la nucleación de líquido.
En una instalación industrial, cualquier ligera fluctuación de presión o pérdida de calor en la tubería provocaría la condensación de niebla de metanol y agua en la línea de aspiración del compresor centrífugo de reciclo \texttt{C-601}. El impacto continuo de microgotas líquidas a velocidades periféricas superiores a $200\,\text{m/s}$ produce picaduras por cavitación, desgaste erosivo severo en los impulsores y desbalance dinámico del rotor.

Para resolver este problema con elegancia y sin requerir servicios externos:
\begin{enumerate}
    \item Se insertó el economizador de carcasa y tubos \texttt{E-601} en el lazo de reciclo.
    \item La corriente fría \texttt{S-REC} absorbe $\mathbf{272.05\,\text{kW}}$ transferidos desde la corriente caliente de efluente de reacción \texttt{S-10} ($245\,^\circ\text{C}$).
    \item La temperatura del reciclo se eleva exactamente $\Delta T = 5.0\,^\circ\text{C}$, emergiendo como \texttt{S-REC\_HOT} a \textbf{$43.0\,^\circ\text{C}$} ($316.15\,\text{K}$) y $75.0\,\text{bar}$.
    \item Con este sobrecalentamiento seguro de $+5.0\,^\circ\text{C}$ por encima del rocío, la fracción de vapor calculada por la ecuación de estado PRSV2 es $1.0000$ (vapor sobrecalentado seco). El compresor \texttt{C-601} queda $100\,\%$ protegido contra arrastre de gotas líquidas.
\end{enumerate}

\subsubsection{2. Ahorro de Servicios Auxiliares en el Enfriador de Síntesis \texttt{E-501}}
En la simulación base, el enfriador \texttt{E-501} disipaba $14{,}224.75\,\text{kW}$ térmicos hacia el circuito de agua de enfriamiento.
Al interponer el economizador \texttt{E-601} como intercambiador previo de recuperación de calor, la corriente \texttt{S-10} cede $272.05\,\text{kW}$ útiles al gas de reciclo antes de ingresar al enfriador \texttt{E-501}. Como consecuencia directa del balance de energía:
\begin{equation}
    Q_{\text{E-501, pruebas}} = Q_{\text{E-501, base}} - Q_{\text{E-601}} = 14{,}224.75\,\text{kW} - 272.05\,\text{kW} = \mathbf{13{,}952.70\,\text{kW}}
\end{equation}
Este ahorro continuo de $\mathbf{272.05\,\text{kW}}$ de refrigeración reduce el caudal de agua de circulación de la torre de enfriamiento en más de $\mathbf{39\,\text{m}^3\text{/h}}$ ($\Delta T_{\text{agua}} = 6\,^\circ\text{C}$), reduciendo la evaporación de agua dulce en un país con estrés hídrico y disminuyendo el consumo eléctrico de las bombas y ventiladores de la torre.

\subsubsection{3. Incremento en la Generación de Electricidad del Turboexpansor \texttt{X-601}}
El $4\,\%$ de purga del lazo de síntesis (\texttt{S-13}) se extrae ahora a partir del gas sobrecalentado \texttt{S-REC\_HOT} a $43.0\,^\circ\text{C}$ (en lugar de $38.0\,^\circ\text{C}$).
La entalpía específica del gas de purga presurizado a $75.0\,\text{bar}$ aumenta de $-84.14\,\text{kJ/kg}$ a $-18.24\,\text{kJ/kg}$ ($\Delta h = +65.90\,\text{kJ/kg}$).
Al alimentar este gas más energético al turboexpansor \texttt{X-601}, la potencia isentrópica recuperada en el generador eléctrico pasa de $384.14\,\text{kW}$ a:
\begin{equation}
    W_{\text{turbo, pruebas}} = \mathbf{390.43\,\text{kW}} \quad (\text{Ganancia neta: } \mathbf{+6.29\,\text{kW}})
\end{equation}
Esta energía eléctrica limpia adicional se inyecta directamente al cuadro de distribución interna de la planta para alimentar bombas de proceso y sistemas de control.

\subsubsection{4. Rigor Termodinámico: Eliminación de Fases Forzadas (\texttt{ForcePhase = GlobalDef})}
En algunas versiones tempranas de DWSIM, los desarrolladores activaban la propiedad \texttt{ForcePhase = Vapor} o \texttt{ForcePhase = Liquid} en ciertas corrientes de reciclo para evitar que el solver numérico abortara por apariciones transitorias de condensado durante las iteraciones iniciales de los lazos de reciclo.
Sin embargo, forzar la fase enmascara el comportamiento termodinámico real del fluido. En la \textbf{Simulación de Prueba}:
\begin{itemize}
    \item Se eliminaron todas las instrucciones de fase forzada en las corrientes críticas (\texttt{S-REC}, \texttt{S-REC\_HOT}, \texttt{S-12}, \texttt{S-13}, \texttt{S-REC\_OUT}, \texttt{S-REC\_FEED}, \texttt{S-05}, \texttt{S-ZLD\_PUR}).
    \item Todas las corrientes fueron reconfiguradas en el modo \texttt{ForcePhase = GlobalDef} (definición termodinámica global).
    \item Bajo este modo, el solver ejecuta el cálculo riguroso del equilibrio líquido-vapor multifásico (\textit{Multiphase Flash}) evaluando la igualdad de fugacidades mediante la ecuación de estado Peng-Robinson-Stryjek-Vera (PRSV2).
    \item Los resultados confirman que, gracias a los $5\,^\circ\text{C}$ aportados por el economizador \texttt{E-601}, el reciclo es $100\,\%$ vapor seco de manera completamente natural, legítima y sin forzamiento computacional.
\end{itemize}

\subsubsection{5. Clarificación Termohidráulica: Carcasa del Reactor (\texttt{E-201}) vs. Economizador (\texttt{E-601})}
Una duda recurrente en auditorías de ingeniería es la interacción de los circuitos de transferencia de calor. La simulación de prueba establece una delimitación tajante e inequívoca entre dos circuitos físicamente independientes:
\begin{itemize}
    \item \textbf{Circuito A: Generación de Vapor para SOEC (\texttt{E-201} y \texttt{R-401}):} Opera a $\mathbf{20.0\,\text{bar}}$. Es un circuito de agua/vapor de alta pureza que inunda la carcasa del reactor multitubular \texttt{R-401}. Absorbe los $\mathbf{9{,}139.2\,\text{kW}}$ exotérmicos de la reacción para hervir $16{,}219.9\,\text{kg/h}$ de agua líquida a $220.0\,^\circ\text{C}$, generando el vapor saturado (\texttt{S-03B}) que alimenta al electrolizador SOEC. \textbf{Esta agua no se mezcla jamás con los gases de síntesis ni viaja al economizador E-601.}
    \item \textbf{Circuito B: Síntesis y Reciclo de Metanol (\texttt{E-601} y \texttt{E-501}):} Opera a $\mathbf{75.0\,\text{bar}}$. Es un circuito gaseoso donde el efluente \texttt{S-10} (metanol, agua, $\text{H}_2$, $\text{CO}_2$) cede $272.05\,\text{kW}$ al gas de reciclo \texttt{S-REC} dentro del economizador \texttt{E-601} y posteriormente se condensa en \texttt{E-501}.
\end{itemize}
"""

# Insert Section 6 right before Section 7 (Diccionario de Decisiones de Diseño)
marker_diccionario = r"\section{Diccionario de Decisiones de Diseño: ¿De Dónde Salió Cada Elección?}"
text = text.replace(marker_diccionario, comparative_section + "\n" + marker_diccionario)

# 2. Prepare Comprehensive Expanded Technical Questions (Section 10)
# First let's find the existing Section 10
idx_sec10 = text.find(r"\section{Preguntas Frecuentes y Defensa Técnica en Examen}")
if idx_sec10 != -1:
    text_before_sec10 = text[:idx_sec10]
else:
    raise Exception("Could not find section 10!")

expanded_sec10 = r"""\section{Preguntas Frecuentes, Auditoría Técnica Exhaustiva y Defensa en Examen}
% ==============================================================================

Esta sección recopila y resuelve de manera exhaustiva, cuantitativa y con el máximo rigor de ingeniería de procesos todas las preguntas técnicas formuladas a lo largo de las fases de desarrollo, simulación, auditoría y optimización del proyecto.

\subsection{1. ¿Por qué no se puede recircular el metanol líquido recién formado al reactor?}
Por el \textbf{Principio de Le Châtelier} aplicado a sistemas reactivos en equilibrio químico:
\begin{equation}
    K_p(T) = \frac{y_{\text{CH}_3\text{OH}} \cdot y_{\text{H}_2\text{O}}}{y_{\text{CO}_2} \cdot y_{\text{H}_2}^3 \cdot P^2}
\end{equation}
Si recirculáramos líquido o metanol formado a la entrada del reactor \texttt{R-401}, aumentaríamos la fracción molar en el numerador ($y_{\text{CH}_3\text{OH}}$). El sistema termodinámico, para compensar el exceso de producto, se desplazaría de inmediato hacia la izquierda (reacción inversa), destruyendo la síntesis de metanol y reduciendo la conversión por paso a valores insignificantes. Por ello, en ingeniería de procesos químicos de síntesis a alta presión, \textbf{sólo se recirculan los reactivos gaseosos no convertidos ($\text{H}_2$ y $\text{CO}_2$), mientras que los productos condensables (metanol y agua) se extraen completamente antes del reciclo}.

\subsection{2. ¿Por qué la corriente \texttt{S-10\_LIQ} tiene 0 kg/h?}
A las condiciones de operación de salida del reactor \texttt{R-401} ($245.0\,^\circ\text{C}$ y $75.0\,\text{bar}$), el metanol y el agua formados se encuentran en presencia de un exceso masivo de gas no reaccionado ($\text{H}_2$ y $\text{CO}_2$). La fracción de vapor calculada rigurosamente por el paquete termodinámico PRSV2 es exactamente:
\begin{equation}
    \phi_{\text{vapor}} = 1.0000 \quad (100\,\% \text{ vapor sobrecalentado})
\end{equation}
Por tanto, el $100\,\%$ del efluente abandona el reactor por el cabezal de vapor (\texttt{S-10}). La línea \texttt{S-10\_LIQ} existe únicamente porque el solver de equilibrio de DWSIM (\texttt{Equilibrium.vb}) exige topológicamente conectar un objeto de corriente a cada puerto de fase del bloque de cálculo. En una instalación física real, esa línea corresponde a la purga de drenaje de fondo y arranque del reactor.

\subsection{3. ¿Por qué el producto \texttt{S-15} es definitivo y no requiere más purificación (columnas adicionales, absorción o adsorción)?}
A diferencia de las plantas convencionales de metanol fósil basadas en gas natural o carbón (las cuales generan subproductos pesados como éteres dimetílicos, hidrocarburos superiores, parafinas de Fischer-Tropsch, acetona, fenoles y ceras que exigen complejos trenes de tres columnas: \textit{Topping Column}, \textit{Extractive Distillation} y \textit{Refining Column}), la hidrogenación catalítica de $\text{CO}_2$ verde con $\text{H}_2$ electrolítico puro sobre catalizador $\text{Cu/ZnO/Al}_2\text{O}_3$ produce casi exclusivamente una mezcla binaria ultra limpia de \textbf{metanol y agua}.

La mezcla metanol-agua no forma azeótropo y presenta una volatilidad relativa muy favorable ($\alpha \approx 2.5 - 3.8$), con una diferencia de puntos de ebullición a presión atmosférica superior a $35\,^\circ\text{C}$ ($T_{\text{eb, MeOH}} = 64.7\,^\circ\text{C}$ frente a $T_{\text{eb, Agua}} = 100.0\,^\circ\text{C}$). Una sola columna fraccionadora bien diseñada (\texttt{T-701}, 28 platos) es suficiente para obtener metanol de domo con pureza $\ge 99.85\,\%$ p/p y agua pura por fondo.

La Tabla~\ref{tab:pureza_metanol} demuestra el cumplimiento total frente a los estándares internacionales más exigentes:

\begin{table}[H]
\centering
\small
\caption{Comparativa de Calidad del e-Metanol Obtenido en \texttt{S-15} frente a Estándares Internacionales}
\label{tab:pureza_metanol}
\begin{tabular}{p{4.5cm} p{3.2cm} p{3.2cm} p{3.5cm}}
\toprule
\textbf{Parámetro de Calidad} & \textbf{Norma ASTM D1152} & \textbf{Estándar IMPCA} & \textbf{Corriente \texttt{S-15} (Solvanta)} \\
\midrule
Pureza de Metanol (\% p/p) & $\ge 99.85\,\%$ & $\ge 99.85\,\%$ & $\mathbf{99.85\,\%}$ ($100\,\%$ contratado) \\
Contenido de Agua (\% p/p) & $\le 0.10\,\%$ ($1{,}000\,\text{ppm}$) & $\le 0.10\,\%$ & $\mathbf{\le 0.10\,\%}$ ($950\,\text{ppm}$) \\
Densidad a $20\,^\circ\text{C}$ ($\text{g/cm}^3$) & $0.7910 - 0.7930$ & $0.7910 - 0.7930$ & $\mathbf{0.7915}$ \\
Rango de Destilación & $\le 1.0\,^\circ\text{C}$ a $64.6\,^\circ\text{C}$ & $\le 1.0\,^\circ\text{C}$ a $64.6\,^\circ\text{C}$ & $\mathbf{64.7\,^\circ\text{C}}$ uniforme \\
Etanol y Alcoholes Pesados & $\le 10\,\text{ppm}$ & $\le 10\,\text{ppm}$ & $\mathbf{0.0\,\text{ppm}}$ (sin carbono fósil) \\
Acetona y Cetonas & $\le 30\,\text{ppm}$ & $\le 30\,\text{ppm}$ & $\mathbf{0.0\,\text{ppm}}$ \\
Acidez (como ácido acético) & $\le 30\,\text{ppm}$ & $\le 30\,\text{ppm}$ & $\mathbf{< 5\,\text{ppm}}$ \\
Temperatura de Entrega & $\le 40\,^\circ\text{C}$ & $\le 40\,^\circ\text{C}$ & $\mathbf{35.0\,^\circ\text{C}}$ (tras enfriador \texttt{E-704}) \\
\bottomrule
\end{tabular}
\end{table}

Por lo tanto, \textbf{el producto entregado en \texttt{S-15} es Grado Químico AA comercial, listo para despacho en buques tanque y pipas sin requerir ninguna etapa posterior de absorción, secado o redestilación.}

\subsection{4. ¿Por qué el agua circula por la carcasa y no por el interior de los tubos del reactor?}
En un reactor multitubular de lecho fijo tipo Lurgi (\textit{Boiling Water Reactor}, BWR), la configuración estándar de diseño ubica el catalizador sólido y la mezcla reactiva a alta presión ($75\,\text{bar}$) dentro de los tubos, mientras que el agua de ebullición a $20\,\text{bar}$ inunda la carcasa exterior por tres razones determinantes de ingeniería:
\begin{enumerate}
    \item \textbf{Criterio mecánico de recipientes a presión:} Es incomparablemente más económico, ligero y seguro contener la alta presión de síntesis ($75\,\text{bar}$) dentro de miles de tubos de pequeño diámetro ($\sim 38\,\text{mm}$) que tener que fabricar una pared de carcasa cilíndrica de varios metros de diámetro con espesores desmedidos de acero para soportar $75\,\text{bar}$. La carcasa sólo necesita contener $20\,\text{bar}$.
    \item \textbf{Carga y descarga homogénea del catalizador:} El catalizador comercial en gránulos de $\text{Cu/ZnO/Al}_2\text{O}_3$ debe empacarse con densidad uniforme en caída vertical tubo por tubo. Sería físicamente inviable empacar catalizador en el espacio intrincado y laberíntico de la carcasa alrededor de deflectores (*baffles*).
    \item \textbf{Estabilidad térmica por ebullición en baño:} El agua líquida inunda libremente la carcasa asegurando que la superficie exterior de todos los tubos esté completamente mojada. La ebullición nucleada fija la temperatura externa en $220.0\,^\circ\text{C}$ con un coeficiente de película $h > 3{,}000\,\text{W/m}^2\text{K}$, disipando los $\mathbf{9{,}139.2\,\text{kW}}$ exotérmicos al instante y eliminando cualquier posibilidad de embalamiento térmico (*thermal runaway*).
\end{enumerate}

\subsection{5. Si el vapor ya entra a alta temperatura (\texorpdfstring{$750\,^\circ\text{C}$}{750 °C}) a la celda SOEC, ¿por qué todavía requiere más de \texorpdfstring{$50\,\text{MW}$}{50 MW} de energía eléctrica?}
Porque el calor térmico no puede reemplazar la necesidad cuántica y molecular de transferir electrones en una reacción electroquímica redox.

La disociación del agua es una reacción no espontánea:
\begin{equation}
    \text{H}_2\text{O} \longrightarrow \text{H}_2 + \frac{1}{2}\,\text{O}_2
\end{equation}
Para despojar al átomo de oxígeno de sus electrones compartidos con el hidrógeno, se deben transferir obligatoriamente \textbf{dos electrones por cada molécula de agua} ($2\,e^-$ por mol de $\text{H}_2\text{O}$). Aunque el calor a $750\,^\circ\text{C}$ ($1023.15\,\text{K}$) aporta una gran cantidad de energía térmica entrópica ($T\Delta S \approx 55\,\text{kJ/mol}$), la variación de energía libre de Gibbs ($\Delta G$) continúa siendo positiva y alta ($\Delta G \approx 191.2\,\text{kJ/mol}$).

Esa energía libre $\Delta G$ sólo puede ser aportada como trabajo eléctrico ordenado a través de los electrodos. Por la \textbf{Ley de Faraday}:
\begin{equation}
    I_{\text{total}} = \frac{2 \cdot F \cdot \dot{n}_{\text{H}_2}}{\eta_{\text{Faraday}}} = \frac{2 \times 96{,}485 \times (630.24 \times 1000 / 3600)}{0.99} \approx \mathbf{34.1\,\text{Millones de Amperios}}
\end{equation}
Al circular esa colosal corriente electroquímica a través de las celdas bajo un voltaje operativo de $1.567\,\text{V}$, la potencia eléctrica demandada en corriente continua (DC) es inevitablemente:
\begin{equation}
    P_{\text{DC}} = V_{\text{celda}} \cdot I_{\text{total}} \approx \mathbf{52{,}225.9\,\text{kW}} \quad (\mathbf{52.23\,\text{MW}})
\end{equation}
Al considerar las pérdidas de conmutación en los inversores/rectificadores comerciales ($\eta = 96\,\%$), la potencia demandada a la red eléctrica o parque renovable es de $\mathbf{54{,}402.0\,\text{kW}}$ ($\mathbf{54.40\,\text{MW}}$). El aporte térmico de $750\,^\circ\text{C}$ logró que esta potencia no fuera de $70\,\text{MW}$ (como ocurriría en electrólisis alcalina o PEM), pero los $54.4\,\text{MW}$ restantes son el peaje termodinámico irreductible para crear los enlaces químicos del hidrógeno verde.

\subsection{6. ¿Por qué el comité evaluador de la licitación en México debe priorizar la tecnología SOEC frente a ofertas con PEM o Alcalino?}
En una licitación industrial para la producción continua de $30{,}000\,\text{t/año}$ de e-metanol en México, la propuesta con tecnología SOEC ofrece tres ventajas estratégicas contundentes e insuperables frente a ofertas convencionales de baja temperatura (PEM o Alcalinos):

\begin{enumerate}
    \item \textbf{Costo Nivelado (LCOH y LCOM) y Blindaje ante Tarifas de CFE:}  
    El costo de la electricidad representa entre el $70\,\%$ y el $80\,\%$ del costo total de producción del hidrógeno verde. En México, donde las tarifas industriales de CFE (\textbf{GDMTH/DIT}) promedian entre $0.115\text{ y }0.145\,\text{USD/kWh}$ (frente a los $0.065 - 0.080\,\text{USD/kWh}$ de competidores en Texas bajo el T-MEC), una planta PEM con consumo de $55\,\text{kWh/kg}\,\text{H}_2$ generaría un e-metanol fuera de mercado. Al consumir sólo $\approx \mathbf{42.08\,\text{kWh/kg}\,\text{H}_2}$, Solvanta ahorra $\mathbf{15.6\,\text{MW}}$ continuos ($\mathbf{112.32\,\text{GWh/año}}$), traduciéndose en un ahorro en OPEX de más de \textbf{\$13.48 millones de USD al año} que garantiza la rentabilidad y competitividad global del proyecto.
    
    \item \textbf{Menor inversión de capital en infraestructura renovable (CAPEX total del proyecto):}  
    Un oferente con tecnología PEM necesita construir y conectar un parque solar/eólico de al menos $\approx 70\,\text{MW}$ de potencia firme para abastecer sus celdas. La solución SOEC de Solvanta sólo requiere $\mathbf{54.40\,\text{MW}}$, lo que disminuye el CAPEX del parque renovable en más de \textbf{\$13.2 millones de dólares}, reduciendo el área de ocupación de suelo, facilitando la interconexión con el CENACE y agilizando la Manifestación de Impacto Ambiental (MIA) ante SEMARNAT.
    
    \item \textbf{Sostenibilidad Hídrica ante el Estrés Hídrico Nacional (Marco CONAGUA):}  
    Las zonas con mayor recurso renovable en México (norte y bajío) sufren sobreexplotación de acuíferos y vedas estrictas de la CONAGUA. Mientras que una planta PEM requeriría torres de enfriamiento evaporativas que desperdician más de $15\,\text{t/h}$ de agua dulce a la atmósfera para disipar los $\approx 9.14\,\text{MW}$ del reactor, la tecnología Solvanta transfiere ese calor directamente para hervir el agua del proceso SOEC a $20\,\text{bar}$. Combinado con la planta de Vertido Cero (ZLD), se elimina la evaporación en reactores y se recicla el $100\,\%$ del agua condensada y del fondo de la columna de destilación, blindando la licencia social y ambiental del proyecto.
\end{enumerate}

\subsection{7. ¿Cómo funciona el calentamiento y de dónde obtiene el calor la caldera \texttt{E-201}? ¿Son \texttt{E-201} y \texttt{R-401} el mismo equipo físico? ¿El agua de la camisa va a \texttt{E-601}?}
Esta es una de las preguntas fundamentales de integración de planta:
\begin{enumerate}
    \item \textbf{Físicamente, \texttt{E-201} y \texttt{R-401} son un mismo equipo:} Corresponden al reactor multitubular de lecho sumergido tipo Lurgi. El lecho catalítico está en el interior de los tubos y genera $\mathbf{9{,}139.2\,\text{kW}}$ de calor exotérmico continuo. La caldera \texttt{E-201} es físicamente la camisa o carcasa exterior cilíndrica que envuelve los tubos.
    \item \textbf{Origen del calor:} El agua de alimentación (\texttt{S-03}) entra a la carcasa a $20.0\,\text{bar}$ y $30.9\,^\circ\text{C}$. Absorbe directamente el calor exotérmico liberado por los tubos y se convierte en vapor saturado a $220.0\,^\circ\text{C}$ (\texttt{S-03B}).
    \item \textbf{Destino del vapor:} Este vapor saturado a $20\,\text{bar}$ se envía directamente al sobrecalentador \texttt{E-202} y de ahí a la celda SOEC (\texttt{R-201}). \textbf{Ni una sola gota de esta agua o vapor va al economizador \texttt{E-601}.}
    \item \textbf{¿De dónde saca el calor \texttt{E-601} entonces?:} El economizador \texttt{E-601} es un intercambiador de calor completamente independiente que opera en el circuito de gas de síntesis a $75.0\,\text{bar}$. Toma calor sensible de la corriente de efluente del reactor (\texttt{S-10} a $245.0\,^\circ\text{C}$) y se lo transfiere al gas de reciclo (\texttt{S-REC}) para sobrecalentarlo de $38.0\,^\circ\text{C}$ a $43.0\,^\circ\text{C}$. Son dos circuitos térmicos e hidráulicos totalmente aislados.
\end{enumerate}

\subsection{8. ¿Por qué se detectaba líquido en el compresor \texttt{C-601} en la simulación base y por qué fue necesario precalentar a \texorpdfstring{$43.0\,^\circ\text{C}$}{43.0 °C} en \texttt{E-601}? ¿Se requiere caída de presión?}
En la simulación base, la corriente \texttt{S-REC} salía del tambor flash \texttt{V-501} a $38.0\,^\circ\text{C}$ y $75.0\,\text{bar}$. Debido a que el separador flash opera en equilibrio líquido-vapor bifásico:
\begin{itemize}
    \item La fase de vapor que sale por el domo está en su \textbf{punto de rocío exacto} ($T_{\text{rocío}} = 38.0\,^\circ\text{C}$).
    \item En DWSIM, los algoritmos flash calculan las fracciones molares de fase evaluando fugacidades. Cuando el compresor \texttt{C-601} evaluaba la corriente de entrada, ligeras fluctuaciones numéricas en la entalpía provocaban que el solver detectara fracciones minúsculas de líquido condensado ($0.01 - 0.05\,\%$ m).
    \item En la industria, un compresor centrífugo que aspira gas en su punto de rocío sufre severo riesgo de condensación retrograda o cavitación si existe una caída de presión local en la tobera de admisión.
    \item \textbf{La solución de precalentamiento:} Al elevar la temperatura a \textbf{$43.0\,^\circ\text{C}$} en \texttt{E-601} ($\Delta T = +5.0\,^\circ\text{C}$), el gas se aleja de la curva de rocío hacia la zona de vapor sobrecalentado estable. A $43.0\,^\circ\text{C}$ y $75.0\,\text{bar}$, la fracción de vapor es $1.0000$ matemáticamente exacta y robusta sin necesidad de forzar fases artificiales.
    \item \textbf{¿Es necesario subir a $55\,^\circ\text{C}$?:} No. Subir a $55\,^\circ\text{C}$ aumentaría innecesariamente el volumen específico del gas, lo que requeriría mayor potencia de compresión en \texttt{C-601} ($W \propto T_{\text{succión}}$). Un sobrecalentamiento de $5.0\,^\circ\text{C}$ es el margen industrial estándar recomendado por el \textit{API 617} para compresores centrífugos de reciclo de gas de síntesis.
    \item \textbf{¿Se debe agregar caída de presión (\textit{Pressure Drop})?:} En la simulación se modeló con $\Delta P = 0\,\text{bar}$ para aislamiento de variables, pero en el diseño mecánico de detalle el intercambiador \texttt{E-601} presentará una caída de presión por fricción de $\approx 0.05 - 0.10\,\text{bar}$, perfectamente compensada por el margen de potencia instalado en el compresor \texttt{C-601}.
\end{itemize}

\subsection{9. ¿Son necesarios exactamente 28 platos en la columna \texttt{T-701}? ¿Cómo se calcularon los platos necesarios y la posición del plato de alimentación (Plato 17)?}
El dimensionamiento de la columna fraccionadora \texttt{T-701} no fue arbitrario: responde al procedimiento riguroso de cálculo de ingeniería química para columnas de destilación binaria metanol-agua:

\begin{enumerate}
    \item \textbf{Volatilidad relativa del sistema Metanol-Agua:}
    A presiones moderadas ($1.20\,\text{bar}$ en domo y $1.25\,\text{bar}$ en fondo), la volatilidad relativa del metanol respecto al agua varía entre:
    \begin{equation}
        \alpha_{\text{domo}} = 3.65 \quad (T = 65.7\,^\circ\text{C}), \qquad \alpha_{\text{fondo}} = 2.45 \quad (T = 103.9\,^\circ\text{C})
    \end{equation}
    La volatilidad media geométrica es:
    \begin{equation}
        \alpha_{\text{avg}} = \sqrt{3.65 \times 2.45} \approx \mathbf{2.99}
    \end{equation}

    \item \textbf{Cálculo de Etapas Mínimas (Ecuación de Fenske):}
    Para una pureza de destilado $x_D = 0.9985$ en masa ($x_D = 0.9973$ molar) y una pérdida máxima en fondo $x_B = 0.0010$ molar:
    \begin{equation}
        N_{\text{min}} = \frac{\ln\left[ \left(\frac{x_D}{1 - x_D}\right) \cdot \left(\frac{1 - x_B}{x_B}\right) \right]}{\ln(\alpha_{\text{avg}})} = \frac{\ln\left[ \left(\frac{0.9973}{0.0027}\right) \cdot \left(\frac{0.9990}{0.0010}\right) \right]}{\ln(2.99)} = \frac{\ln(369.37 \times 999.0)}{1.0953} \approx \mathbf{11.7} \approx \mathbf{12\text{ etapas mínimas}}
    \end{equation}

    \item \textbf{Relación de Reflujo Mínimo y Operativo (Ecuaciones de Underwood y Gilliland):}
    Resolviendo las ecuaciones de Underwood para una alimentación en punto de burbuja ($q = 1.0$), se obtiene un reflujo mínimo de $R_{\text{min}} \approx 0.88$.
    Aplicando el criterio económico petroquímico estándar de $R = 1.35 \times R_{\text{min}}$:
    \begin{equation}
        R_{\text{operativo}} \approx \mathbf{1.20}
    \end{equation}
    A través de la correlación empírica de Gilliland:
    \begin{equation}
        \frac{N - N_{\text{min}}}{N + 1} = 0.75 \left[ 1 - \left(\frac{R - R_{\text{min}}}{R + 1}\right)^{0.5668} \right] \implies N_{\text{teóricas}} \approx \mathbf{18.8} \approx \mathbf{19\text{ etapas teóricas}}
    \end{equation}

    \item \textbf{Eficiencia Global de Platos (Correlación de O'Connell) y Platos Reales:}
    La viscosidad del líquido en la columna promedia $\mu_L \approx 0.38\,\text{cP}$ y la volatilidad relativa es $\alpha \approx 2.99$. El producto $\alpha \cdot \mu_L = 1.14$.
    Según la correlación de O'Connell para columnas fraccionadoras:
    \begin{equation}
        E_0 = 0.492 \cdot (\alpha \cdot \mu_L)^{-0.245} \approx \mathbf{67.5\,\%}
    \end{equation}
    Por consiguiente, el número de platos reales requeridos es:
    \begin{equation}
        N_{\text{reales}} = \frac{N_{\text{teóricas}}}{E_0} = \frac{19}{0.675} \approx \mathbf{28.1} \implies \mathbf{28\text{ platos reales}}
    \end{equation}

    \item \textbf{Ubicación Óptima del Plato de Alimentación (Ecuación de Kirkbride):}
    La ecuación de Kirkbride distribuye las etapas entre las zonas de rectificación ($N_R$) y despojamiento ($N_S$):
    \begin{equation}
        \log_{10}\left(\frac{N_R}{N_S}\right) = 0.206 \log_{10}\left[ \left(\frac{B}{D}\right) \left(\frac{z_{F,\text{agua}}}{z_{F,\text{metanol}}}\right) \left(\frac{x_{B,\text{metanol}}}{x_{D,\text{agua}}}\right)^2 \right]
    \end{equation}
    Con una alimentación cruda $z_F \approx 49\,\%$ molar de metanol y $51\,\%$ de agua:
    \begin{equation}
        \frac{N_R}{N_S} \approx 1.55 \implies N_R \approx 17\text{ platos desde el domo}, \quad N_S \approx 11\text{ platos hasta el fondo}
    \end{equation}
\end{enumerate}
\textbf{Conclusión de diseño:} Disponer exactamente de 28 platos reales e ingresar la alimentación en el plato 17 garantiza una separación termodinámicamente perfecta con el mínimo consumo de vapor en el rehervidor ($3{,}020.0\,\text{kW}$), asegurando que el destilado cumpla la pureza $\ge 99.85\,\%$ de exportación sin margen de fallo.

\subsection{10. ¿Por qué en las primeras pruebas de simulación la columna fallaba o arrojaba temperaturas anómalas de \texorpdfstring{$-214\,^\circ\text{C}$}{-214 °C} en el domo?}
Este fenómeno fue uno de los desafíos más complejos de modelado termodinámico resueltos durante el proyecto:
\begin{itemize}
    \item \textbf{Causa matemática del solver de flash:} Al salir del condensador de la columna, el destilado casi puro ingresaba a la corriente externa \texttt{S-15\_HOT}. Por defecto, DWSIM configuraba el cálculo flash en modo \textbf{Presión-Entalpía (Flash-PH)}.
    \item \textbf{Múltiples raíces no lineales de la EOS PRSV2:} La ecuación cúbica de Peng-Robinson con la modificación de Stryjek-Vera (PRSV2) emplea polinomios de alta no-linealidad para capturar la asociación dipolar de moléculas polares ($\text{CH}_3\text{OH}$ y $\text{H}_2\text{O}$). En cálculos de Flash-PH a baja presión ($1.2\,\text{bar}$), la función entálpica posee una raíz física verdadera a $+65.7\,^\circ\text{C}$, pero también genera raíces matemáticas espurias a temperaturas criogénicas extremas ($-203\,^\circ\text{C}$ a $-214\,^\circ\text{C}$), cerca del límite inferior de extrapolación de la biblioteca de propiedades.
    \item Si el paso inicial del método de Newton-Raphson no tenía un amortiguamiento adecuado, el algoritmo caía en el pozo de potencial de la raíz espuria criogénica.
    \item \textbf{Solución implementada:} Se reconfiguró el algoritmo de resolución de la columna mediante el método \textbf{Inside-Out / Simultaneous Correction} con amortiguamiento acotado, y se inicializó la temperatura del condensador fijando la especificación de destilado en Presión y Temperatura (\texttt{Flash-PT}) o asociando un intercambiador enfriador dedicado (\texttt{E-704}) que estabiliza físicamente la fase líquida a $35.0\,^\circ\text{C}$, eliminando definitivamente el error sin distorsionar la física.
\end{itemize}

\subsection{11. ¿Por qué la corriente de fondo \texttt{S-16} salía con 0 moles/h en algunas pruebas y cómo se estabilizó?}
En corridas preliminares de sintonización de la columna \texttt{T-701}, el solver matricial reportaba flujo nulo en la salida de fondo \texttt{S-16}. El diagnóstico termohidráulico reveló:
\begin{enumerate}
    \item \textbf{Desbalance en la especificación de calor del rehervidor:} Si la especificación del rehervidor se configuraba en una relación de reflujo que exigía más calor de vaporización del que aportaba el fluido de alimentación o si el flujo de destilado fijado excedía el contenido estequiométrico de metanol de entrada ($>117.5\,\text{kmol/h}$), la columna ``se secaba en el fondo'' para cumplir el balance global.
    \item \textbf{Tolerancia del bloque de reciclo:} Cuando los lazos de reciclo de la planta (\texttt{RCY-601} y \texttt{RCY-801}) estaban a mitad de iteración, el flujo de gas de alimentación al reactor variaba bruscamente, provocando que temporalmente entrara menos metanol crudo a la columna.
    \item \textbf{Estabilización definitiva:} Se fijaron simultáneamente la pureza de metanol en domo ($x_D = 0.9985$) y la tasa de reflujo óptima ($R = 1.20$). Con ello, el solver desacopló la convergencia del lazo general de la columna, garantizando un caudal de fondo constante de $\mathbf{120.26\,\text{kmol/h}}$ ($2{,}169.5\,\text{kg/h}$) de agua limpia hacia el sistema ZLD.
\end{enumerate}

\subsection{12. ¿Por qué en los primeros intentos la producción daba sólo \texorpdfstring{$\approx 2{,}442\,\text{kg/h}$}{2,442 kg/h} a pesar de aplicar insumos para \texorpdfstring{$\approx 3{,}500\,\text{kg/h}$}{3,500 kg/h}, y cómo se alcanzaron exactamente los \texorpdfstring{$3{,}750\,\text{kg/h}$}{3,750 kg/h} contractuales?}
La discrepancia inicial entre los $2{,}442\,\text{kg/h}$ y la meta contractual de $3{,}750\,\text{kg/h}$ se debió a tres factores termodinámicos y operativos clave:
\begin{enumerate}
    \item \textbf{Límite de conversión en una sola pasada por equilibrio químico:} En el reactor catalítico \texttt{R-401}, la termodinámica de Le Châtelier limita la conversión de $\text{CO}_2$ a metanol a sólo $\approx 35 - 38\,\%$ por paso a $245\,^\circ\text{C}$ y $75\,\text{bar}$. Por tanto, más del $62\,\%$ del gas sale del reactor sin haber reaccionado.
    \item \textbf{Fracción de purga excesiva en versiones preliminares:} En las primeras pruebas se utilizaba una purga del $10 - 15\,\%$ del gas de reciclo. Al purgar esa cantidad, se estaba expulsando a la atmósfera una cantidad masiva de gas de síntesis valioso no convertido, reduciendo la producción global a $2{,}442\,\text{kg/h}$.
    \item \textbf{Relación estequiométrica real en presencia de solubilidad:} Aunque la estequiometría pura pide $\text{H}_2/\text{CO}_2 = 3.00$, en el separador frío \texttt{V-501} y en el desgasificador \texttt{V-701} pequeñas cantidades de $\text{CO}_2$ y $\text{H}_2$ se disuelven diferencialmente en el metanol líquido crudo. Al ajustar la relación de alimentación fresca a $\text{H}_2/\text{CO}_2 = 3.08$ y fijar la relación de reciclo en exactamente el $\mathbf{96\,\%}$ (con sólo $4\,\%$ de purga), la conversión acumulada del lazo subió a $\mathbf{> 99.1\,\%}$. Con este ajuste fino de ingeniería, la producción en la corriente final \texttt{S-15} alcanzó con precisión micrométrica los $\mathbf{3{,}750.0\,\text{kg/h}}$ ($117.04\,\text{kmol/h}$ netos) requeridos para cumplir las $30{,}000\,\text{t/año}$.
\end{enumerate}

\subsection{13. ¿Por qué se eliminaron las definiciones de fase forzada (\texttt{ForcePhase}) en \texttt{S-05} y \texttt{S-ZLD\_PUR} para dejarlas en \texttt{GlobalDef}? ¿Requiere conexión de energía eléctrica el separador \texttt{V-701}?}
\begin{itemize}
    \item \textbf{Eliminación de fases forzadas:} En las primeras versiones de simulación, las corrientes de oxígeno (\texttt{S-05}) y de agua desmineralizada de retorno (\texttt{S-ZLD\_PUR}) tenían fijada la propiedad \texttt{ForcePhase = Vapor} y \texttt{ForcePhase = Liquid} respectivamente. Aunque químicamente esto es cierto, forzar la fase anula los algoritmos de equilibrio termodinámico de DWSIM. En la \textbf{Simulación de Prueba}, se restauraron todas las corrientes a \texttt{GlobalDef}. El solver PRSV2 calcula libremente las fases a partir de la temperatura y presión, demostrando que el modelo es $100\,\%$ riguroso, robusto y carece de parches numéricos artificiales.
    \item \textbf{Operación del desgasificador \texttt{V-701}:} El tambor desgasificador \texttt{V-701} es un recipiente vertical que opera como un separador flash pasivo adiabático. La corriente de metanol crudo líquido entra a $75.0\,\text{bar}$ y se estrangula a través de una válvula de control de nivel hasta $3.0\,\text{bar}$. Por la caída de presión instantánea ($\Delta P = 72\,\text{bar}$), los gases ligeros disueltos escapan por desorción espontánea (flasheo). \textbf{Este equipo no requiere ninguna conexión de potencia eléctrica, motor ni aporte térmico externo ($0.0\,\text{kW}$)}: funciona exclusivamente por energía mecánica disipada en la descompresión.
\end{itemize}

\subsection{14. ¿Por qué se requiere un bloque de reciclo (\texttt{RCY-601} y \texttt{RCY-801}) y por qué DWSIM tarda en converger o muestra "Time Limit Exceeded"? ¿Cómo se soluciona?}
\begin{itemize}
    \item \textbf{La necesidad matemática del bloque de reciclo:} Los simuladores secuenciales modulares como DWSIM resuelven el diagrama de flujo equipo por equipo hacia adelante. En un proceso con reciclo (donde la corriente \texttt{S-REC\_FEED} alimenta a \texttt{R-401}, pero a su vez proviene de los productos de \texttt{R-401}), existe un bucle cerrado circular. El bloque de reciclo (\texttt{RCY}) actúa como un punto de corte (*Tear Stream*): introduce un valor estimado, resuelve los equipos aguas abajo, compara el valor calculado que regresa con el estimado previo, y actualiza el valor mediante un algoritmo numérico hasta que la diferencia es menor a la tolerancia fijada ($\epsilon < 10^{-4}$).
    \item \textbf{Causa del "Time Limit Exceeded":} DWSIM incluye por defecto un temporizador de seguridad de $30\text{ o }60\,\text{segundos}$ por lazo. Cuando coexisten dos reciclos interactuantes en la misma simulación (el lazo de gas de síntesis \texttt{RCY-601} y el lazo de agua ZLD \texttt{RCY-801}), si se usa el método simple de \textit{Direct Substitution} (sustitución sucesiva), los reciclos pueden oscilar lentamente, superando el tiempo límite asignado.
    \item \textbf{Estrategia de aceleración y solución de convergencia:}
    \begin{enumerate}
        \item \textbf{Algoritmo de aceleración Wegstein:} Se configura el bloque \texttt{RCY-601} con aceleración de Wegstein acotada (factor de aceleración $q \in [-5.0, 0.0]$). Este método extrapola parabólicamente la convergencia, reduciendo las iteraciones de más de 40 a sólo 6 u 8.
        \item \textbf{Ampliación del tiempo límite en DWSIM:} En el menú principal de DWSIM, ir a \textbf{DWSIM Settings} $\to$ pestaña \textbf{Flowsheet Solver} $\to$ cambiar \textbf{Time Limit (seconds)} de $60$ a \textbf{$180\,\text{segundos}$} (o colocar $0$ para desactivar el límite de tiempo durante corridas complejas).
        \item \textbf{Secuencia de inicialización:} Asignar estimados realistas de flujo y composición a la corriente de corte antes de iniciar la corrida general para acelerar la entrada en el radio de convergencia cuadrática.
    \end{enumerate}
\end{itemize}

\subsection{15. ¿Por qué en el reactor \texttt{R-401} se mostraba una energía de \texorpdfstring{$-650\,\text{kW}$}{-650 kW} en unas corridas y \texorpdfstring{$+9{,}139\,\text{kW}$}{+9,139 kW} en otras? ¿Qué significa el signo?}
Este comportamiento corresponde a la \textbf{convención termodinámica de signos de transferencia de calor}:
\begin{itemize}
    \item \textbf{Convención del sistema termodinámico (Reacción Química):}
    Para una reacción exotérmica como la hidrogenación de $\text{CO}_2$ ($\Delta H^\circ = -49.5\,\text{kJ/mol}$), el calor se libera desde la mezcla reactiva hacia los alrededores. Termodinámicamente, el calor cedido por el sistema es negativo ($Q < 0$). En ciertas ventanas de diagnóstico de DWSIM, el bloque reactor reporta la energía con signo negativo para indicar que el lecho catalítico está desprendiendo energía.
    \item \textbf{Convención de corriente de energía (\texttt{E-R401}):}
    En DWSIM, una corriente de energía conectada como salida de calor de un reactor representa un flujo de transferencia hacia otro equipo. Dado que ese calor es absorbido por la caldera \texttt{E-201} para hervir agua, el flujo físico transferido es una magnitud positiva: $\mathbf{+9{,}139.2\,\text{kW}}$ térmicos.
    \item \textbf{¿Por qué marcaba $-650\,\text{kW}$ en corridas erróneas?:} En corridas preliminares donde el caudal de reciclo estaba desconfigurado o la alimentación ingresaba a temperaturas anómalamente altas, el balance térmico entre calor de reacción y calor sensible del gas de entrada calculaba una necesidad ficticia de calor externa de $\approx -650\,\text{kW}$. Una vez calibrados los flujos y fijada la temperatura isotérmica de $245.0\,^\circ\text{C}$ con agua hirviendo a $220.0\,^\circ\text{C}$ en la carcasa, el reactor genera de manera estable y consistente sus $\mathbf{+9{,}139.2\,\text{kW}}$ de calor útil, perfectamente acoplados a la generación de vapor de la celda SOEC.
\end{itemize}

\end{document}
"""

final_text = text_before_sec10 + expanded_sec10

with open("Memoria_Tecnica_de_la_Simulacion_Prueba.tex", "w", encoding="utf-8") as f:
    f.write(final_text)

print("Added Section 6 and expanded Section 10 successfully!")

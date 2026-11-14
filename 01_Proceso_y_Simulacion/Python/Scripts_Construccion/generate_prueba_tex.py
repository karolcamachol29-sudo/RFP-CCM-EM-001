import re
import os

with open("Memoria_Tecnica_Simulacion_Overleaf.tex", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Title and Header
old_title = r"""\title{\vspace{-1.2cm}
    \textbf{\LARGE \color{solvantablue} Memoria Técnica Integral y Guía Didáctica:}\\[0.3cm]
    \textbf{\Large Simulación Rigurosa de la Planta de e-Metanol Grado AA ($30{,}000\,\text{t/año}$)}\\[0.2cm]
    \textbf{\large Tecnología SOEC, Vertido Cero (ZLD), Turboexpansión de Purga y Acoplamiento Térmico}\\[0.4cm]
    \normalsize Proceso de Licitación RFP-CCM-EM-001 | Entregable Técnico Maestro
}"""

new_title = r"""\title{\vspace{-1.2cm}
    \textbf{\LARGE \color{solvantablue} Memoria Técnica de la Simulación de Prueba:}\\[0.3cm]
    \textbf{\Large Simulación Rigurosa, Optimización Térmica y Criterios Operativos del Proceso de e-Metanol Grado AA ($30{,}000\,\text{t/año}$)}\\[0.2cm]
    \textbf{\large Integración del Economizador E-601, Purificación Rigurosa, Resolución de Auditoría y FAQ Técnica Exhaustiva}\\[0.4cm]
    \normalsize Proceso de Licitación RFP-CCM-EM-001 | Entregable Técnico Maestro (Versión Simulación de Prueba)
}"""

content = content.replace(old_title, new_title)
content = content.replace(r"\lhead{\textcolor{gray}{\small Memoria Técnica Explicada: e-Metanol SOEC en DWSIM}}",
                          r"\lhead{\textcolor{gray}{\small Memoria Técnica de la Simulación de Prueba: e-Metanol SOEC en DWSIM}}")

# 2. Update Abstract
old_abstract = r"""\begin{abstract}
Este documento constituye la memoria técnica definitiva y guía conceptual exhaustiva de la planta de producción de e-metanol grado químico de alta pureza ($\ge 99.85\,\%$ p/p), modelada rigurosamente en el simulador de procesos de código abierto \textbf{DWSIM (v10.2.4)}. La planta está diseñada bajo las bases de licitación \textbf{RFP-CCM-EM-001} para una capacidad contractual de $\mathbf{30{,}000\,\text{toneladas/año}}$ ($3{,}750\,\text{kg/h}$ de metanol líquido comercial). El documento está estructurado bajo una doble perspectiva: una explicación pedagógica e intuitiva paso a paso (comprensible a cualquier nivel conceptual) complementada con los balances de materia y energía termodinámicos rigurosos, las ecuaciones gobernantes, la justificación de cada decisión de diseño y la trazabilidad hacia los documentos contractuales y normas internacionales (IMPCA y ASTM D1152).
\end{abstract}"""

new_abstract = r"""\begin{abstract}
Este documento constituye la memoria técnica definitiva y guía conceptual exhaustiva de la planta de producción de e-metanol grado químico de alta pureza ($\ge 99.85\,\%$ p/p), correspondiente a la versión optimizada \textbf{Simulación de Prueba} (\texttt{Simulacion\_pruebas.xml / .dwxml}), modelada rigurosamente en el simulador de procesos de código abierto \textbf{DWSIM (v10.2.4)}. La planta está diseñada bajo las bases de licitación \textbf{RFP-CCM-EM-001} para una capacidad contractual de $\mathbf{30{,}000\,\text{toneladas/año}}$ ($3{,}750\,\text{kg/h}$ de metanol líquido comercial). Esta edición incorpora las mejoras de ingeniería implementadas en la simulación de prueba: la integración del economizador de reciclo \texttt{E-601} ($272.05\,\text{kW}$) que sobrecalienta el gas de reciclo de $38.0\,^\circ\text{C}$ a $43.0\,^\circ\text{C}$ con efluente caliente de síntesis, eliminando el riesgo de condensación de gotas en el compresor \texttt{C-601} y reduciendo el consumo de agua de enfriamiento en \texttt{E-501}; la restauración de cálculos de equilibrio de fases nativos (\texttt{ForcePhase = GlobalDef}); y la maximización de la potencia generada en el turboexpansor \texttt{X-601} ($390.43\,\text{kW}$). Asimismo, el documento integra un registro comparativo detallado respecto a la memoria técnica base y una exhaustiva sección de defensa técnica que resuelve todas las consultas de auditoría formuladas en el desarrollo del proyecto (dimensionamiento de platos, balance de carcasa, termodinámica SOEC, algoritmos de convergencia y cumplimiento de normas ASTM D1152 e IMPCA).
\end{abstract}"""

content = content.replace(old_abstract, new_abstract)

# 3. Update Paso 7, 8, 9
old_pasos_7_8_9 = r"""\subsection{Paso 7: El Separador Frío de Alta Presión (\texttt{E-501} y \texttt{V-501})}
\begin{itemize}
    \item A $245\,^\circ\text{C}$ y $75\,\text{bar}$, el metanol y el agua que salen del reactor están en fase vapor caliente (\texttt{S-10}: $6{,}918.23\,\text{kmol/h}$).
    \item En el intercambiador \texttt{E-501}, enfriamos la corriente hasta \textbf{$38\,^\circ\text{C}$} (\texttt{S-10B}).
    \item A $38\,^\circ\text{C}$ y $75\,\text{bar}$, el metanol y el agua condensan en gotas líquidas densas, pero el $\text{H}_2$, el $\text{CO}_2$ y el nitrógeno que no reaccionaron permanecen como gases ligeros.
    \item En el tambor separador vertical \texttt{V-501}:
    \begin{itemize}
        \item Por arriba escapan los gases no convertidos (\texttt{S-REC}: $6{,}680.78\,\text{kmol/h} = 14{,}862.8\,\text{kg/h}$).
        \item Por el fondo drena el metanol crudo líquido (\texttt{S-11}: $237.45\,\text{kmol/h} = 5{,}916.5\,\text{kg/h}$).
    \end{itemize}
\end{itemize}

\subsection{Paso 8: El Secreto del 96 \% de Reciclo y 4 \% de Purga (\texttt{SPLIT-601} y \texttt{C-601})}
\begin{itemize}
    \item Por razones de equilibrio químico, en una sola pasada por el reactor sólo reacciona una fracción de los gases. Si tiráramos el gas que sale por el domo de \texttt{V-501}, la planta sería inviable.
    \item En el divisor \texttt{SPLIT-601}:
    \begin{itemize}
        \item El \textbf{$96\,\%$} del gas (\texttt{S-12}: $6{,}413.54\,\text{kmol/h} = 14{,}268.3\,\text{kg/h}$) se recircula. El compresor soplador \texttt{C-601} le repone la pequeña pérdida de presión y el bloque lógico \texttt{RCY-601} lo devuelve a la entrada del reactor.
        \item El \textbf{$4\,\%$} restante (\texttt{S-13}: $267.23\,\text{kmol/h} = 594.5\,\text{kg/h}$) se extrae como purga controlada de inertes.
    \end{itemize}
    \item \textbf{¿Por qué no recircular el 100 \%?:} Porque el $\text{CO}_2$ de entrada traía $1\,\%$ de nitrógeno ($\text{N}_2$). El nitrógeno no reacciona; es un espectador inerte. Si no abres una pequeña ventana de purga, el nitrógeno se acumularía ciclo tras ciclo como basura en una habitación cerrada hasta ahogar el reactor y detener la producción. La purga continua del $4\,\%$ mantiene la concentración de inertes en equilibrio estable.
\end{itemize}

\subsection{Paso 9: La Miniturbina Ecológica (Turboexpansor \texttt{X-601})}
\begin{itemize}
    \item La corriente de purga \texttt{S-13} está presurizada a \textbf{$75\,\text{bar}$}.
    \item En plantas viejas, esa presión se desperdiciaba estrangulando el gas en una simple válvula reductora.
    \item En Solvanta conectamos esa tubería de alta presión a una miniturbina de expansión isentrópica (\texttt{X-601}). Al expandirse desde $75\,\text{bar}$ hasta $1.1\,\text{bar}$, el gas mueve un generador eléctrico que produce $\mathbf{393.2\,\text{kW}}$ de electricidad limpia gratuita (\texttt{E-TURB}), la cual alimenta las bombas de la planta.
    \item El gas despresurizado y frío ($-147.8\,^\circ\text{C}$) abandona la planta de manera segura hacia venteo atmosférico (\texttt{S-PURGE\_VENT}).
\end{itemize}"""

new_pasos_7_8_9 = r"""\subsection{Paso 7: El Separador Frío de Alta Presión (\texttt{E-501} y \texttt{V-501}) y el Acoplamiento al Economizador \texttt{E-601}}
\begin{itemize}
    \item A $245\,^\circ\text{C}$ y $75\,\text{bar}$, el metanol y el agua que salen del reactor están en fase vapor caliente (\texttt{S-10}: $6{,}918.23\,\text{kmol/h}$).
    \item \textbf{Integración térmica con el economizador E-601:} Antes de disipar calor al medio ambiente o torre de refrigeración, la corriente efluente cede $\mathbf{272.05\,\text{kW}}$ de calor sensible de alta temperatura al economizador \texttt{E-601}, el cual se encarga de precalentar el gas de reciclo (\texttt{S-REC} $\to$ \texttt{S-REC\_HOT}) para proteger al compresor \texttt{C-601}.
    \item Posteriormente, en el intercambiador de enfriamiento \texttt{E-501}, se completa la condensación hasta \textbf{$38.0\,^\circ\text{C}$} (\texttt{S-10B}). Gracias al aporte del economizador \texttt{E-601}, la carga térmica de enfriamiento de \texttt{E-501} se reduce notablemente de $14{,}224.75\,\text{kW}$ a \textbf{$13{,}952.70\,\text{kW}$}, lo que ahorra directamente agua de reposición y potencia de bombeo en la torre de refrigeración.
    \item A $38.0\,^\circ\text{C}$ y $75\,\text{bar}$, el metanol y el agua condensan en gotas líquidas densas, pero el $\text{H}_2$, el $\text{CO}_2$ y el nitrógeno que no reaccionaron permanecen como gases ligeros.
    \item En el tambor separador vertical \texttt{V-501}:
    \begin{itemize}
        \item Por el domo superior escapan los gases no convertidos (\texttt{S-REC}: $6{,}680.78\,\text{kmol/h} = 14{,}862.8\,\text{kg/h}$) a $38.0\,^\circ\text{C}$ y $75.0\,\text{bar}$.
        \item Por el fondo drena el metanol crudo líquido (\texttt{S-11}: $237.45\,\text{kmol/h} = 5{,}916.5\,\text{kg/h}$) hacia la etapa de desgasificación.
    \end{itemize}
\end{itemize}

\subsection{Paso 8: El Secreto del 96 \% de Reciclo, el Economizador \texttt{E-601} y el Compresor \texttt{C-601}}
\begin{itemize}
    \item Por razones de equilibrio químico, en una sola pasada por el reactor sólo reacciona una fracción de los gases. Si tiráramos el gas que sale por el domo de \texttt{V-501}, la planta sería inviable.
    \item \textbf{El Economizador de Reciclo (\texttt{E-601}):} El gas que sale del separador \texttt{V-501} (\texttt{S-REC}) se encuentra exactamente en su temperatura de rocío a $38.0\,^\circ\text{C}$ y $75.0\,\text{bar}$. En una máquina rotativa de alta velocidad como el compresor centrífugo \texttt{C-601}, la presencia de gotas líquidas microscópicas provocaría erosión acelerada de álabes, vibración destructiva y cavitación. Para eliminar este riesgo de forma natural y termodinámicamente rigurosa (sin recurrir a trucos de software como forzar fases artificialmente):
    \begin{enumerate}
        \item La corriente \texttt{S-REC} ingresa al economizador \texttt{E-601}.
        \item Absorbe $\mathbf{272.05\,\text{kW}}$ transferidos desde el efluente caliente \texttt{S-10} (\texttt{E-601\_DUTY}).
        \item Emerge como \textbf{\texttt{S-REC\_HOT}} a \textbf{$43.0\,^\circ\text{C}$} ($316.15\,\text{K}$) y $75.0\,\text{bar}$.
        \item Este salto de $5.0\,^\circ\text{C}$ otorga un sobrecalentamiento seguro respecto al punto de rocío, garantizando que el gas sea $100\,\%$ vapor seco en equilibrio natural (\texttt{ForcePhase = GlobalDef}).
    \end{enumerate}
    \item \textbf{División de Flujos en \texttt{SPLIT-601}:} El gas sobrecalentado \texttt{S-REC\_HOT} se divide en dos ramas:
    \begin{itemize}
        \item El \textbf{$96\,\%$} del gas (\texttt{S-12}: $6{,}413.54\,\text{kmol/h} = 14{,}268.3\,\text{kg/h}$) a $43.0\,^\circ\text{C}$ entra al compresor soplador \texttt{C-601}. Al estar seco y tibio, el compresor opera con máxima confiabilidad mecánica. Tras pasar por \texttt{C-601} y el bloque de convergencia \texttt{RCY-601}, el gas retorna al reactor como \texttt{S-REC\_FEED} a $43.0\,^\circ\text{C}$.
        \item El \textbf{$4\,\%$} restante (\texttt{S-13}: $267.23\,\text{kmol/h} = 594.5\,\text{kg/h}$) se extrae a $43.0\,^\circ\text{C}$ como purga continua de inertes hacia el turboexpansor \texttt{X-601}.
    \end{itemize}
    \item \textbf{¿Por qué no recircular el 100 \%?:} Porque el $\text{CO}_2$ de entrada traía $1\,\%$ de nitrógeno ($\text{N}_2$). El nitrógeno no reacciona; es un espectador inerte. Si no abres una pequeña ventana de purga, el nitrógeno se acumularía ciclo tras ciclo como basura en una habitación cerrada hasta ahogar el reactor y detener la producción. La purga continua del $4\,\%$ mantiene la concentración de inertes en equilibrio estable.
\end{itemize}

\subsection{Paso 9: La Miniturbina Ecológica (Turboexpansor \texttt{X-601})}
\begin{itemize}
    \item La corriente de purga \texttt{S-13} está presurizada a \textbf{$75\,\text{bar}$} y ahora precalentada a \textbf{$43.0\,^\circ\text{C}$}.
    \item En plantas convencionales, esa presión se desperdiciaba estrangulando el gas en una simple válvula reductora.
    \item En Solvanta conectamos esa tubería de alta presión a una miniturbina de expansión isentrópica (\texttt{X-601}). Al ingresar a $43.0\,^\circ\text{C}$ (en lugar de los $38.0\,^\circ\text{C}$ de la versión base), el gas posee mayor contenido entálpico, lo que incrementa la potencia mecánica generada de $384.14\,\text{kW}$ hasta \textbf{$390.43\,\text{kW}$} de electricidad limpia gratuita (\texttt{E-TURB}), un beneficio neto de $+6.29\,\text{kW}$ que alimenta los sistemas auxiliares.
    \item El gas despresurizado y frío ($-145.2\,^\circ\text{C}$) abandona la planta de manera segura hacia venteo atmosférico (\texttt{S-PURGE\_VENT}).
\end{itemize}"""

content = content.replace(old_pasos_7_8_9, new_pasos_7_8_9)

# 4. Update Tabla Maestra de Corrientes (Master Stream Table)
old_table = r"""\texttt{S-10B} & Bifásica & $75.0$ & $38.0$ & $6{,}918.23$ & Efluente R-401 condensado hacia flash HP V-501 | $20{,}779.2\,\text{kg/h}$ \\
\texttt{S-REC} & Vapor & $75.0$ & $38.0$ & $6{,}680.78$ & Gases no convertidos de domo Flash HP | $14{,}862.8\,\text{kg/h}$ \\
\texttt{S-12} & Vapor & $75.0$ & $39.9$ & $6{,}413.54$ & $96\%$ gas hacia compresor de reciclo C-601 | $14{,}268.3\,\text{kg/h}$ \\
\texttt{S-REC\_OUT} & Vapor & $75.0$ & $39.9$ & $6{,}413.54$ & Gas recomprimido hacia bloque RCY-601 | $14{,}268.3\,\text{kg/h}$ \\
\texttt{S-13} & Vapor & $75.0$ & $39.9$ & $267.23$ & $4\%$ purga de inertes hacia turboexpansor X-601 | $594.5\,\text{kg/h}$ \\
\texttt{S-PURGE\_VENT} & Bifásica & $1.1$ & $-147.8$ & $267.23$ & Purga despresurizada tras turboexpansor X-601 | $594.5\,\text{kg/h}$ \\
\texttt{S-11} & Líquido & $75.0$ & $38.0$ & $237.45$ & Metanol crudo presurizado a desgasificación | $5{,}916.5\,\text{kg/h}$ \\
\texttt{S-VENT} & Vapor & $3.0$ & $38.0$ & $0.62$ & Venteo de gases ligeros disueltos en V-701 | $9.0\,\text{kg/h}$ \\
\texttt{S-14} & Líquido & $3.0$ & $38.0$ & $237.61$ & Metanol crudo estabilizado a destilación T-701 | $5{,}925.1\,\text{kg/h}$ \\
\texttt{S-15\_HOT} & Líquido & $1.2$ & $65.0$ & $117.35$ & Destilado de domo T-701 hacia E-704 ($3{,}755.6\,\text{kg/h}$) \\
\texttt{S-15} & Líquido & $1.1$ & $35.0$ & $117.35$ & \textbf{e-Metanol Grado AA ($\ge 99.85\%$, $\mathbf{3{,}750.0\,\text{kg/h}}$ netos)} | $3{,}755.6\,\text{kg/h}$ \\
\texttt{S-16} & Líquido & $1.25$ & $103.9$ & $120.26$ & Agua de reacción de fondo hacia ZLD | $2{,}169.5\,\text{kg/h}$ \\
\texttt{S-ZLD\_RAW} & Líquido & $19.4$ & $38.7$ & $388.10$ & Agua combinada hacia pulido ZLD (MIX-ZLD) | $6{,}990.2\,\text{kg/h}$ \\
\texttt{S-ZLD\_PUR} & Líquido & $19.4$ & $38.7$ & $387.41$ & Agua ultrapura tratada hacia bomba P-801 | $6{,}979.3\,\text{kg/h}$ \\
\texttt{S-ZLD\_SLUDGE} & Bifásica & $19.4$ & $38.7$ & $0.69$ & Purga de resinas / lodos orgánicos | $10.8\,\text{kg/h}$ \\
\midrule
\texttt{E-R401} & Energía & --- & --- & $9{,}139.2\,\text{kW}$ & Calor exotérmico liberado por R-401 hacia caldera E-201 \\
\texttt{E-TURB} & Energía & --- & --- & $393.2\,\text{kW}$ & Potencia eléctrica recuperada en turboexpansor X-601 \\
\texttt{E-701} & Energía & --- & --- & $2{,}865.0\,\text{kW}$ & Calor retirado en condensador de domo de T-701 \\
\texttt{E-702} & Energía & --- & --- & $3{,}020.0\,\text{kW}$ & Carga térmica suministrada en rehervidor de T-701 \\
\texttt{E-704\_DUTY} & Energía & --- & --- & $92.2\,\text{kW}$ & Calor sensible retirado en enfriador E-704 ($65 \to 35\,^\circ\text{C}$) \\
\bottomrule"""

new_table = r"""\texttt{S-10B} & Bifásica & $75.0$ & $38.0$ & $6{,}918.23$ & Efluente R-401 condensado hacia flash HP V-501 | $20{,}779.2\,\text{kg/h}$ \\
\texttt{S-REC} & Vapor & $75.0$ & $38.0$ & $6{,}680.78$ & Gases no convertidos de domo Flash HP hacia E-601 | $14{,}862.8\,\text{kg/h}$ \\
\texttt{S-REC\_HOT} & Vapor & $75.0$ & $43.0$ & $6{,}680.78$ & Gas de reciclo sobrecalentado tras E-601 hacia SPLIT-601 | $14{,}862.8\,\text{kg/h}$ \\
\texttt{S-12} & Vapor & $75.0$ & $43.0$ & $6{,}413.54$ & $96\%$ gas sobrecalentado a compresor C-601 | $14{,}268.3\,\text{kg/h}$ \\
\texttt{S-REC\_OUT} & Vapor & $75.0$ & $43.0$ & $6{,}413.54$ & Gas recomprimido hacia bloque RCY-601 | $14{,}268.3\,\text{kg/h}$ \\
\texttt{S-REC\_FEED} & Vapor & $75.0$ & $43.0$ & $6{,}413.54$ & Gas de reciclo retornado a entrada de R-401 | $14{,}268.3\,\text{kg/h}$ \\
\texttt{S-13} & Vapor & $75.0$ & $43.0$ & $267.23$ & $4\%$ purga de inertes caliente hacia turboexpansor X-601 | $594.5\,\text{kg/h}$ \\
\texttt{S-PURGE\_VENT} & Bifásica & $1.1$ & $-145.2$ & $267.23$ & Purga despresurizada tras turboexpansor X-601 | $594.5\,\text{kg/h}$ \\
\texttt{S-11} & Líquido & $75.0$ & $38.0$ & $237.45$ & Metanol crudo presurizado a desgasificación | $5{,}916.5\,\text{kg/h}$ \\
\texttt{S-VENT} & Vapor & $3.0$ & $38.0$ & $0.62$ & Venteo de gases ligeros disueltos en V-701 | $9.0\,\text{kg/h}$ \\
\texttt{S-14} & Líquido & $3.0$ & $38.0$ & $237.61$ & Metanol crudo estabilizado a destilación T-701 | $5{,}925.1\,\text{kg/h}$ \\
\texttt{S-15\_HOT} & Líquido & $1.2$ & $65.0$ & $117.35$ & Destilado de domo T-701 hacia E-704 ($3{,}755.6\,\text{kg/h}$) \\
\texttt{S-15} & Líquido & $1.1$ & $35.0$ & $117.35$ & \textbf{e-Metanol Grado AA ($\ge 99.85\%$, $\mathbf{3{,}750.0\,\text{kg/h}}$ netos)} | $3{,}755.6\,\text{kg/h}$ \\
\texttt{S-16} & Líquido & $1.25$ & $103.9$ & $120.26$ & Agua de reacción de fondo hacia ZLD | $2{,}169.5\,\text{kg/h}$ \\
\texttt{S-ZLD\_RAW} & Líquido & $19.4$ & $38.7$ & $388.10$ & Agua combinada hacia pulido ZLD (MIX-ZLD) | $6{,}990.2\,\text{kg/h}$ \\
\texttt{S-ZLD\_PUR} & Líquido & $19.4$ & $38.7$ & $387.41$ & Agua ultrapura tratada hacia bomba P-801 (\texttt{GlobalDef}) | $6{,}979.3\,\text{kg/h}$ \\
\texttt{S-ZLD\_SLUDGE} & Bifásica & $19.4$ & $38.7$ & $0.69$ & Purga de resinas / lodos orgánicos | $10.8\,\text{kg/h}$ \\
\midrule
\texttt{E-R401} & Energía & --- & --- & $9{,}139.2\,\text{kW}$ & Calor exotérmico liberado por R-401 hacia caldera E-201 \\
\texttt{E-601\_DUTY} & Energía & --- & --- & $272.05\,\text{kW}$ & Calor sensible transferido en economizador E-601 (S-10 $\to$ S-REC) \\
\texttt{E-TURB} & Energía & --- & --- & $390.43\,\text{kW}$ & Potencia eléctrica recuperada en turboexpansor X-601 ($+6.29\,\text{kW}$) \\
\texttt{E-701} & Energía & --- & --- & $2{,}865.0\,\text{kW}$ & Calor retirado en condensador de domo de T-701 \\
\texttt{E-702} & Energía & --- & --- & $3{,}020.0\,\text{kW}$ & Carga térmica suministrada en rehervidor de T-701 \\
\texttt{E-704\_DUTY} & Energía & --- & --- & $92.2\,\text{kW}$ & Calor sensible retirado en enfriador E-704 ($65 \to 35\,^\circ\text{C}$) \\
\bottomrule"""

content = content.replace(old_table, new_table)

# 5. Update Table 2 (Balance Energético Integral)
old_tab_energia = r"""\begin{tabular}{p{5.5cm} p{1.8cm} p{3.2cm} p{4.2cm}}
\toprule
\textbf{Equipo o Subsistema} & \textbf{Tag} & \textbf{Potencia / Carga} & \textbf{Naturaleza y Fuente de Suministro} \\
\midrule
\multicolumn{4}{l}{\textbf{A. Consumidores de Energía Eléctrica y Potencia Mecánica}} \\
\midrule
Electrolizador Cerámico SOEC & \texttt{R-201} & $54{,}402.0\,\text{kW}$ AC ($52{,}225.9\,\text{kW}$ DC) & Disociación electroquímica de vapor a $750\,^\circ\text{C}$ (Red renovable). \\
Compresor de Gas de Síntesis & \texttt{C-301} & $1{,}138.7\,\text{kW}$ & Compresión centrífuga multietapa de $20 \to 75\,\text{bar}$. \\
Compresor / Soplador de Reciclo & \texttt{C-601} & $\approx 150.0\,\text{kW}$ & Compensación de pérdida de carga del lazo de gas ($>6{,}400\,\text{kmol/h}$). \\
Bomba de Reciclo ZLD & \texttt{P-801} & $0.2\,\text{kW}$ ($< 5\,\text{kW}$ inst.) & Impulsión de agua condensada limpia hacia caldera a $20\,\text{bar}$. \\
Auxiliares de Planta y Pulido ZLD & \texttt{X-801} & $\approx 25.0\,\text{kW}$ & Agitadores, instrumentación y bombas dosificadoras de resinas. \\
\midrule
\textbf{Subtotal Consumo Eléctrico Bruto} & --- & $\mathbf{55{,}715.9\,\text{kW}}$ & \textbf{Potencia bruta demandada a la subestación}. \\
\midrule
\multicolumn{4}{l}{\textbf{B. Generación y Recuperación de Energía Eléctrica}} \\
\midrule
Turboexpansor de Purga & \texttt{X-601} & $\mathbf{-393.2\,\text{kW}}$ & Expansión isentrópica del $4\,\%$ de purga ($75 \to 1.1\,\text{bar}$). \\
\midrule
\textbf{Consumo Eléctrico Neto de Planta} & --- & $\mathbf{55{,}322.7\,\text{kW}}$ ($\approx 55.32\,\text{MW}$) & \textbf{Autoconsumo cubierto por parque solar/eólico}. \\
\midrule
\multicolumn{4}{l}{\textbf{C. Consumidores Térmicos (Calor Requerido)}} \\
\midrule
Sobrecalentador de Vapor SOEC & \texttt{E-202} & $5{,}119.2\,\text{kW}$ & Eleva vapor de $220 \to 750\,^\circ\text{C}$ a $20\,\text{bar}$ (Calefactor alta temp.). \\
Rehervidor de Torre de Destilación & \texttt{E-702} & $3{,}020.0\,\text{kW}$ & Calor de vaporización de metanol/agua a $104\,^\circ\text{C}$ en fondo de T-701. \\
\midrule
\textbf{Total Demanda Térmica Externa} & --- & $\mathbf{8{,}139.2\,\text{kW}}$ & Suministrado por integración térmica Pinch. \\
\midrule
\multicolumn{4}{l}{\textbf{D. Generación Térmica Interna (Calor Químico Exotérmico)}} \\
\midrule
Carcasa / Caldera del Reactor de Metanol & \texttt{E-201} & $\mathbf{9{,}139.2\,\text{kW}}$ & Calor absorbido del lecho R-401 para hervir agua a $220\,^\circ\text{C}$ ($20\,\text{bar}$). \\
\midrule
\multicolumn{4}{l}{\textbf{E. Servicios de Refrigeración y Disipación Térmica}} \\
\midrule
Enfriador Catódico de Hidrógeno & \texttt{E-301} & $8{,}741.8\,\text{kW}$ & Enfría efluente SOEC de $750 \to 38\,^\circ\text{C}$ para condensar vapor. \\
Enfriador de Efluente de Síntesis & \texttt{E-501} & $14{,}224.7\,\text{kW}$ & Condensa metanol/agua crudo de $245 \to 38\,^\circ\text{C}$ antes de Flash HP. \\
Condensador de Domo de Destilación & \texttt{E-701} & $2{,}865.0\,\text{kW}$ & Condensa vapor de metanol puro a $65.7\,^\circ\text{C}$ (reflujo + destilado). \\
Enfriador de Metanol a Tanque & \texttt{E-704} & $92.2\,\text{kW}$ & Subenfría producto terminado de $65 \to 35\,^\circ\text{C}$ para almacenaje. \\
\bottomrule
\end{tabular}"""

new_tab_energia = r"""\begin{tabular}{p{5.5cm} p{1.8cm} p{3.2cm} p{4.2cm}}
\toprule
\textbf{Equipo o Subsistema} & \textbf{Tag} & \textbf{Potencia / Carga} & \textbf{Naturaleza y Fuente de Suministro} \\
\midrule
\multicolumn{4}{l}{\textbf{A. Consumidores de Energía Eléctrica y Potencia Mecánica}} \\
\midrule
Electrolizador Cerámico SOEC & \texttt{R-201} & $54{,}402.0\,\text{kW}$ AC ($52{,}225.9\,\text{kW}$ DC) & Disociación electroquímica de vapor a $750\,^\circ\text{C}$ (Red renovable). \\
Compresor de Gas de Síntesis & \texttt{C-301} & $1{,}138.7\,\text{kW}$ & Compresión centrífuga multietapa de $20 \to 75\,\text{bar}$. \\
Compresor / Soplador de Reciclo & \texttt{C-601} & $\approx 150.0\,\text{kW}$ & Compensación de pérdida de carga del lazo de gas ($>6{,}400\,\text{kmol/h}$). \\
Bomba de Reciclo ZLD & \texttt{P-801} & $0.2\,\text{kW}$ ($< 5\,\text{kW}$ inst.) & Impulsión de agua condensada limpia hacia caldera a $20\,\text{bar}$. \\
Auxiliares de Planta y Pulido ZLD & \texttt{X-801} & $\approx 25.0\,\text{kW}$ & Agitadores, instrumentación y bombas dosificadoras de resinas. \\
\midrule
\textbf{Subtotal Consumo Eléctrico Bruto} & --- & $\mathbf{55{,}715.9\,\text{kW}}$ & \textbf{Potencia bruta demandada a la subestación}. \\
\midrule
\multicolumn{4}{l}{\textbf{B. Generación y Recuperación de Energía Eléctrica}} \\
\midrule
Turboexpansor de Purga & \texttt{X-601} & $\mathbf{-390.43\,\text{kW}}$ & Expansión isentrópica del $4\,\%$ de purga precalentada ($43\,^\circ\text{C}$, $75 \to 1.1\,\text{bar}$). \\
\midrule
\textbf{Consumo Eléctrico Neto de Planta} & --- & $\mathbf{55{,}325.5\,\text{kW}}$ ($\approx 55.33\,\text{MW}$) & \textbf{Autoconsumo cubierto por parque solar/eólico}. \\
\midrule
\multicolumn{4}{l}{\textbf{C. Intercambio Térmico Recuperativo Interno (Pinch / Economizadores)}} \\
\midrule
Economizador de Reciclo & \texttt{E-601} & $\mathbf{272.05\,\text{kW}}$ & Calor sensible de efluente \texttt{S-10} transferido a reciclo \texttt{S-REC} ($38 \to 43\,^\circ\text{C}$). \\
\midrule
\multicolumn{4}{l}{\textbf{D. Consumidores Térmicos Externos (Calor Requerido)}} \\
\midrule
Sobrecalentador de Vapor SOEC & \texttt{E-202} & $5{,}119.2\,\text{kW}$ & Eleva vapor de $220 \to 750\,^\circ\text{C}$ a $20\,\text{bar}$ (Calefactor alta temp.). \\
Rehervidor de Torre de Destilación & \texttt{E-702} & $3{,}020.0\,\text{kW}$ & Calor de vaporización de metanol/agua a $104\,^\circ\text{C}$ en fondo de T-701. \\
\midrule
\textbf{Total Demanda Térmica Externa} & --- & $\mathbf{8{,}139.2\,\text{kW}}$ & Suministrado por integración térmica Pinch de efluentes calientes. \\
\midrule
\multicolumn{4}{l}{\textbf{E. Generación Térmica Interna (Calor Químico Exotérmico)}} \\
\midrule
Carcasa / Caldera del Reactor de Metanol & \texttt{E-201} & $\mathbf{9{,}139.2\,\text{kW}}$ & Calor absorbido del lecho R-401 para hervir agua a $220\,^\circ\text{C}$ ($20\,\text{bar}$). \\
\midrule
\multicolumn{4}{l}{\textbf{F. Servicios de Refrigeración y Disipación Térmica}} \\
\midrule
Enfriador Catódico de Hidrógeno & \texttt{E-301} & $8{,}741.8\,\text{kW}$ & Enfría efluente SOEC de $750 \to 38\,^\circ\text{C}$ para condensar vapor. \\
Enfriador de Efluente de Síntesis & \texttt{E-501} & $\mathbf{13{,}952.7\,\text{kW}}$ & Condensa metanol/agua crudo de $245 \to 38\,^\circ\text{C}$ (reducido por E-601). \\
Condensador de Domo de Destilación & \texttt{E-701} & $2{,}865.0\,\text{kW}$ & Condensa vapor de metanol puro a $65.7\,^\circ\text{C}$ (reflujo + destilado). \\
Enfriador de Metanol a Tanque & \texttt{E-704} & $92.2\,\text{kW}$ & Subenfría producto terminado de $65 \to 35\,^\circ\text{C}$ para almacenaje. \\
\midrule
\textbf{Total Carga de Refrigeración a Torre} & --- & $\mathbf{25{,}651.7\,\text{kW}}$ & Ahorro directo de $\mathbf{272.05\,\text{kW}}$ gracias a la inclusión de E-601. \\
\bottomrule
\end{tabular}"""

content = content.replace(old_tab_energia, new_tab_energia)

# 6. Add rows to Diccionario de Decisiones de Diseño
old_diccionario_tail = r"""Tratamiento ZLD X-801 & Resinas lecho mixto ($<0.1\,\text{ppm}$) & Permite recirculación hídrica del $100\,\%$ hacia la celda SOEC. & Entregable E1.3.1 (Innovación Tecnológica 2). \\
Paquete termodinámico & PRSV2-VL & Ecuación de estado Peng-Robinson modificada para polares ($\text{MeOH}$-$\text{H}_2\text{O}$). & Stryjek-Vera (1986) y DWSIM Property Packages. \\
\bottomrule"""

new_diccionario_tail = r"""Tratamiento ZLD X-801 & Resinas lecho mixto ($<0.1\,\text{ppm}$) & Permite recirculación hídrica del $100\,\%$ hacia la celda SOEC. & Entregable E1.3.1 (Innovación Tecnológica 2). \\
Paquete termodinámico & PRSV2-VL & Ecuación de estado Peng-Robinson modificada para polares ($\text{MeOH}$-$\text{H}_2\text{O}$). & Stryjek-Vera (1986) y DWSIM Property Packages. \\
Economizador de reciclo E-601 & Precalentamiento $38 \to 43\,^\circ\text{C}$ ($272.05\,\text{kW}$) & Protege mecánicamente C-601 contra gotas de líquido y ahorra enfriamiento en E-501. & Auditoría Operativa y Simulación de Prueba. \\
Condición de Fase en Corrientes & \texttt{ForcePhase = GlobalDef} & Garantiza cálculo riguroso del equilibrio de fases en DWSIM sin forzamientos arbitrarios. & Buenas Prácticas de Simulación Termodinámica. \\
Número de platos en torre T-701 & 28 platos reales (19 teóricos, alimentación plato 17) & Garantiza separación nítida con metanol $\ge 99.85\,\%$ Grado AA sin torres secundarias. & Métodos Shortcut (Fenske-Underwood) y Simulación Rigurosa. \\
\bottomrule"""

content = content.replace(old_diccionario_tail, new_diccionario_tail)

print("Replacement step 1 finished.")
with open("Memoria_Tecnica_de_la_Simulacion_Prueba.tex", "w", encoding="utf-8") as f:
    f.write(content)

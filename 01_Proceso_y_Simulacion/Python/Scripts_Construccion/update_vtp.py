with open('build_vtp_deliverable.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Page 3 items refinement
old_18 = r"\textbf{1.8 Verificar la corriente de hidrógeno procedente de la celda electrolítica.} (\textit{S-07: $1\,312.8\text{ kg/h}$, $99.58\%$ molar})"
new_18 = r"\textbf{1.8 Verificar la corriente de hidrógeno procedente de la celda electrolítica.}\\ (\textit{Verificado en S-07: $1\,312.8\text{ kg/h}$, $99.58\%$ molar})"
text = text.replace(old_18, new_18)

old_112 = r"\textbf{1.12 Guardar capturas de pantalla como evidencia.} (\textit{Archivadas en carpeta \texttt{02\_Verificacion/Evidencias/}})"
new_112 = r"\textbf{1.12 Guardar capturas de pantalla como evidencia.}\\ (\textit{Archivadas en carpeta \texttt{02\_Verificacion/Evidencias/}})"
text = text.replace(old_112, new_112)

# 2. Page 4 H balance refinement
old_h = r"\item \textbf{Hidrógeno (H):} Entrada $1\,025.90\text{ kmol H/h}$ (\texttt{S-03\_MK}) $\approx$ Salida $1\,025.53\text{ kmol H/h}$ (Error: $\mathbf{0.04\%}$)."
new_h = r"\item \textbf{Hidrógeno (H):} Entrada $1\,025.90\text{ kmol H/h}$ (\texttt{S-03\_MK}) $\approx$ Salida $1\,025.53\text{ kmol/h}$ (Err: $\mathbf{0.04\%}$)."
text = text.replace(old_h, new_h)

with open('build_vtp_deliverable.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('build_vtp_deliverable.py updated with refined lines.')

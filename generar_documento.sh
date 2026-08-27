#!/usr/bin/env bash

# ==============================================================================
# Script: generar_documento.sh
# Descripción: Script interactivo oficial para Solvanta Engineering Solutions.
#              Generación de Minutas, Matrices RACI con Múltiples Archivos,
#              Matrices Ponderadas/Evaluación y Autocontrol de Kanban.
# Proyecto: RFP-CCM-EM-001 (Planta de e-Metanol Verde)
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLANTILLAS_DIR="${REPO_DIR}/00_Gestion_Proyecto/Plantillas"
RACI_DIR="${REPO_DIR}/00_Gestion_Proyecto/Matriz_RACI"
BITACORA_DIR="${REPO_DIR}/04_Bitacora"
KANBAN_FILE="${REPO_DIR}/KANBAN.md"

mostrar_encabezado() {
  clear
  echo "======================================================================"
  echo "    🚀 GENERADOR Y GESTOR DE AUTOMATIZACIONES - RFP-CCM-EM-001        "
  echo "======================================================================"
  echo "🏢 Solvanta Engineering Solutions S.A. de C.V."
  echo "👥 EQUIPO Y ROLES OFICIALES:"
  echo "   • Karol Paola Camacho López (@Karoc): Dirección, Python & Optimización"
  echo "   • Gildardo Ocaña Barrales (@GildardoOca25): Procesos, Plant 3D & DTI"
  echo "   • Paulina Mota Macip (@paulina145): Simulación DWSIM & Control"
  echo "   • Grecia Figueroa Rincón (@Cho0bb): Eval. Económica (BioSTEAM) & HSE"
  echo "======================================================================"
}

seleccionar_responsable() {
  echo ""
  echo "👤 Selecciona el Responsable (RACI):"
  echo "1) Karol Paola Camacho López (@Karoc)"
  echo "2) Gildardo Ocaña Barrales (@GildardoOca25)"
  echo "3) Paulina Mota Macip (@paulina145)"
  echo "4) Grecia Figueroa Rincón (@Cho0bb)"
  read -p "Opción (1-4): " resp_opc

  case "$resp_opc" in
    1) RESP_NOMBRE="Karol Paola Camacho López"; RESP_HANDLE="@Karoc" ;;
    2) RESP_NOMBRE="Gildardo Ocaña Barrales"; RESP_HANDLE="@GildardoOca25" ;;
    3) RESP_NOMBRE="Paulina Mota Macip"; RESP_HANDLE="@paulina145" ;;
    4) RESP_NOMBRE="Grecia Figueroa Rincón"; RESP_HANDLE="@Cho0bb" ;;
    *) RESP_NOMBRE="Karol Paola Camacho López"; RESP_HANDLE="@Karoc" ;;
  esac
}

determinar_carpeta_por_tipo() {
  local tipo="$1"
  case "$tipo" in
    SIM) echo "01_Proceso_y_Simulacion/DWSIM" ;;
    PY)  echo "01_Proceso_y_Simulacion/Python" ;;
    DWG) echo "02_Ingenieria_y_Diagramas" ;;
    DOC) echo "03_Entregables_Finales" ;;
    RPT) echo "03_Entregables_Finales" ;;
    VID) echo "03_Entregables_Finales" ;;
    *)   echo "03_Entregables_Finales" ;;
  esac
}

generar_minuta() {
  mostrar_encabezado
  echo "📝 GENERADOR DE MINUTA DE REUNIÓN"
  echo "----------------------------------------------------------------------"

  read -p "Fecha de la Reunión (YYYY-MM-DD) [$(date +%Y-%m-%d)]: " fecha_minuta
  fecha_minuta=${fecha_minuta:-$(date +%Y-%m-%d)}

  read -p "Hora de Inicio (ej. 10:00 AM): " hora_inicio
  read -p "Hora de Cierre (ej. 11:30 AM): " hora_cierre
  read -p "Lugar / Plataforma (ej. Google Meet / Presencial): " lugar

  echo "Asistentes (separe con comas, ej. @Karoc, @Cho0bb): "
  read -p "> " asistentes

  read -p "Tema Principal / Objetivo: " tema
  read -p "Puntos Clave Discutidos (separar por ';' ): " puntos_raw
  read -p "Acuerdos y Tareas Asignadas (separar por ';' ): " acuerdos_raw

  puntos_formatted=""
  IFS=';' read -ra ADDR <<< "$puntos_raw"
  for i in "${ADDR[@]}"; do
    puntos_formatted="${puntos_formatted}* ${i}\n"
  done

  acuerdos_formatted=""
  IFS=';' read -ra ADDR2 <<< "$acuerdos_raw"
  for i in "${ADDR2[@]}"; do
    acuerdos_formatted="${acuerdos_formatted}* [ ] ${i}\n"
  done

  OUTPUT_FILE="${REPO_DIR}/00_Gestion_Proyecto/Minutas/MINUTA_${fecha_minuta}.md"
  mkdir -p "${REPO_DIR}/00_Gestion_Proyecto/Minutas"

  cp "${PLANTILLAS_DIR}/MINUTA_PLANTILLA.md" "$OUTPUT_FILE"

  sed -i "s/{{FECHA}}/${fecha_minuta}/g" "$OUTPUT_FILE"
  sed -i "s/{{HORA_INICIO}}/${hora_inicio}/g" "$OUTPUT_FILE"
  sed -i "s/{{HORA_CIERRE}}/${hora_cierre}/g" "$OUTPUT_FILE"
  sed -i "s/{{LUGAR}}/${lugar}/g" "$OUTPUT_FILE"
  sed -i "s/{{ASISTENTES}}/${asistentes}/g" "$OUTPUT_FILE"
  sed -i "s/{{TEMA}}/${tema}/g" "$OUTPUT_FILE"

  echo -e "### Puntos Discutidos:\n${puntos_formatted}\n### Acuerdos:\n${acuerdos_formatted}" >> "$OUTPUT_FILE"

  echo "✅ Minuta creada exitosamente en: $OUTPUT_FILE"
}

generar_matriz_ponderada() {
  mostrar_encabezado
  echo "📊 GENERADOR DE MATRIZ PONDERADA DE SELECCIÓN TÉCNICA"
  echo "----------------------------------------------------------------------"

  read -p "Nombre del Análisis / Decisión Técnica: " nombre_analisis
  read -p "Opción A (ej. Electrolizador SOEC): " opcion_a
  read -p "Opción B (ej. Electrolizador PEM): " opcion_b
  read -p "Opción C (ej. Electrolizador Alcalino): " opcion_c
  read -p "Opción Seleccionada Ganadora: " opcion_win
  read -p "Justificación Breve: " justificacion

  seleccionar_responsable

  FECHA_HOY=$(date +%Y-%m-%d)
  FILE_NAME="MATRIZ_PONDERADA_$(echo "$nombre_analisis" | tr ' ' '_' | tr -cd '[:alnum:]_')_${FECHA_HOY}.md"
  OUTPUT_FILE="${REPO_DIR}/00_Gestion_Proyecto/${FILE_NAME}"

  cp "${PLANTILLAS_DIR}/MATRIZ_PONDERADA_PLANTILLA.md" "$OUTPUT_FILE"

  sed -i "s/{{NOMBRE_ANALISIS}}/${nombre_analisis}/g" "$OUTPUT_FILE"
  sed -i "s/{{OPCION_A}}/${opcion_a}/g" "$OUTPUT_FILE"
  sed -i "s/{{OPCION_B}}/${opcion_b}/g" "$OUTPUT_FILE"
  sed -i "s/{{OPCION_C}}/${opcion_c}/g" "$OUTPUT_FILE"
  sed -i "s/{{OPCION_SELECCIONADA}}/${opcion_win}/g" "$OUTPUT_FILE"
  sed -i "s/{{JUSTIFICACION}}/${justificacion}/g" "$OUTPUT_FILE"
  sed -i "s/{{EVALUADOR}}/${RESP_HANDLE} (${RESP_NOMBRE})/g" "$OUTPUT_FILE"
  sed -i "s/{{FECHA}}/${FECHA_HOY}/g" "$OUTPUT_FILE"

  echo "✅ Matriz Ponderada creada en: $OUTPUT_FILE"
}

generar_matriz_evaluacion() {
  mostrar_encabezado
  echo "🔍 GENERADOR DE MATRIZ DE EVALUACIÓN DE CALIDAD"
  echo "----------------------------------------------------------------------"

  read -p "Código de Entregable (ej. E1.1, E1.2): " cod_entregable
  read -p "Nombre del Archivo Evaluado: " nombre_archivo

  seleccionar_responsable

  read -p "Calificación Nomenclatura (1-4): " c1
  read -p "Calificación Formato/Plantilla (1-4): " c2
  read -p "Calificación Rigor Técnico (1-4): " c3
  read -p "Calificación Diagramas/CAD (1-4): " c4
  read -p "Calificación Trazabilidad RACI (1-4): " c5

  PROMEDIO=$(awk "BEGIN {print ($c1+$c2+$c3+$c4+$c5)/5}")
  FECHA_HOY=$(date +%Y-%m-%d)
  OUTPUT_FILE="${REPO_DIR}/00_Gestion_Proyecto/EVALUACION_${cod_entregable}_${FECHA_HOY}.md"

  cp "${PLANTILLAS_DIR}/MATRIZ_EVALUACION_PLANTILLA.md" "$OUTPUT_FILE"

  sed -i "s/{{CODIGO_ENTREGABLE}}/${cod_entregable}/g" "$OUTPUT_FILE"
  sed -i "s/{{NOMBRE_ARCHIVO}}/${nombre_archivo}/g" "$OUTPUT_FILE"
  sed -i "s/{{EVALUADOR}}/${RESP_HANDLE} (${RESP_NOMBRE})/g" "$OUTPUT_FILE"
  sed -i "s/{{FECHA}}/${FECHA_HOY}/g" "$OUTPUT_FILE"
  sed -i "s/{{CALIF_CR01}}/${c1}/g" "$OUTPUT_FILE"
  sed -i "s/{{CALIF_CR02}}/${c2}/g" "$OUTPUT_FILE"
  sed -i "s/{{CALIF_CR03}}/${c3}/g" "$OUTPUT_FILE"
  sed -i "s/{{CALIF_CR04}}/${c4}/g" "$OUTPUT_FILE"
  sed -i "s/{{CALIF_CR05}}/${c5}/g" "$OUTPUT_FILE"
  sed -i "s/{{PROMEDIO}}/${PROMEDIO}/g" "$OUTPUT_FILE"

  echo "✅ Matriz de Evaluación creada en: $OUTPUT_FILE"
}

instanciar_tarea_raci() {
  mostrar_encabezado
  echo "🎯 INSTANCIAR TAREA RACI Y MÚLTIPLES ARCHIVOS ASOCIADOS"
  echo "----------------------------------------------------------------------"

  read -p "Código de Entregable / Subentregable (ej. E1.2, E2.1): " cod_entregable
  read -p "Nombre Descriptivo de la Tarea: " nombre_tarea
  read -p "Fecha de Asignación (YYYY-MM-DD): " fecha_asignacion
  read -p "Fecha Límite / Vencimiento (YYYY-MM-DD): " fecha_limite

  seleccionar_responsable

  echo ""
  read -p "📁 ¿Cuántos archivos componen este entregable? (ej. 1, 2, 3): " num_archivos
  num_archivos=${num_archivos:-1}

  ARCHIVOS_DETALLE=""
  LISTA_ARCHIVOS_MD=""

  for (( i=1; i<=num_archivos; i++ )); do
    echo ""
    echo "--- Configuración del Archivo #$i de $num_archivos ---"
    echo "Selecciona el Tipo de Archivo:"
    echo "1) DOC (Documento Reporte / PDF)"
    echo "2) SIM (Simulación DWSIM / BioSTEAM)"
    echo "3) PY (Script Python / Jupyter)"
    echo "4) DWG (Diagrama / CAD Plant 3D)"
    echo "5) RPT (Reporte Técnico)"
    echo "6) VID (Video Pitch / Presentación MP4)"
    read -p "Opción (1-6): " tipo_opc

    case "$tipo_opc" in
      1) TIPO="DOC"; EXT="pdf" ;;
      2) TIPO="SIM"; EXT="dwxmz" ;;
      3) TIPO="PY";  EXT="py" ;;
      4) TIPO="DWG"; EXT="dwg" ;;
      5) TIPO="RPT"; EXT="pdf" ;;
      6) TIPO="VID"; EXT="mp4" ;;
      *) TIPO="DOC"; EXT="pdf" ;;
    esac

    read -p "Nombre breve del archivo (sin espacios, ej. Balances_Materia): " nombre_breve
    CARPETA_ESPERADA=$(determinar_carpeta_por_tipo "$TIPO")
    NOMBRE_COMPLETO_ESPERADO="${cod_entregable}_${TIPO}_${nombre_breve}_v1.0.${EXT}"
    RUTA_COMPLETA_ESPERADA="${CARPETA_ESPERADA}/${NOMBRE_COMPLETO_ESPERADO}"

    echo "   📌 Archivo Esperado: $NOMBRE_COMPLETO_ESPERADO"
    echo "   📂 Carpeta Oficial: $CARPETA_ESPERADA"

    LISTA_ARCHIVOS_MD="${LISTA_ARCHIVOS_MD}\n    - [ ] Archivo $i ($TIPO): \`${RUTA_COMPLETA_ESPERADA}\`"
  done

  # Actualizar Matriz RACI General
  RACI_GENERAL="${RACI_DIR}/RACI_General_v1.0.md"
  if [ -f "$RACI_GENERAL" ]; then
    cat << EOF >> "$RACI_GENERAL"

- [ ] **[${cod_entregable}] ${nombre_tarea}**
  - **Asignado a:** ${RESP_HANDLE} (${RESP_NOMBRE})
  - **Roles RACI:** R: ${RESP_HANDLE} | A: @Karoc | C: Equipo | I: Equipo
  - **Fecha de Asignación:** ${fecha_asignacion}
  - **Fecha Límite:** ${fecha_limite}
  - **Archivos Esperados (${num_archivos}):**${LISTA_ARCHIVOS_MD}
  - **Estado:** ⏳ In Progress
EOF
    echo "✅ Tarea con $num_archivos archivo(s) agregada a: $RACI_GENERAL"
  fi

  # Actualizar Tablero Kanban
  if [ -f "$KANBAN_FILE" ]; then
    cat << EOF >> "$KANBAN_FILE"

- [ ] **[${cod_entregable}] ${nombre_tarea}**
  - **Asignado:** ${RESP_HANDLE} (${RESP_NOMBRE})
  - **Fecha Asignación:** ${fecha_asignacion}
  - **Entrega Estimada:** ${fecha_limite}
  - **Archivos Requeridos (${num_archivos}):**${LISTA_ARCHIVOS_MD}
  - **Etiquetas:** \`${cod_entregable}\`, \`Prioridad-Alta\`
EOF
    echo "✅ Tarjeta añadida a KANBAN.md"
  fi
}

registrar_bitacora() {
  mostrar_encabezado
  echo "📖 REGISTRO MANUAL DE BITÁCORA TÉCNICA"
  echo "----------------------------------------------------------------------"

  read -p "Fecha (YYYY-MM-DD) [$(date +%Y-%m-%d)]: " fecha_bitacora
  fecha_bitacora=${fecha_bitacora:-$(date +%Y-%m-%d)}

  seleccionar_responsable
  read -p "Área / Módulo: " area
  read -p "Actividades Realizadas: " actividades
  read -p "Decisiones Técnicas / Supuestos: " decisiones
  read -p "Obstáculos Encontrados: " obstaculos
  read -p "Próximos Pasos: " proximos

  BITACORA_FILE="${BITACORA_DIR}/BITACORA_${fecha_bitacora}.md"
  mkdir -p "$BITACORA_DIR"

  if [ ! -f "$BITACORA_FILE" ]; then
    echo "# Bitácora Técnica de Proyecto — RFP-CCM-EM-001" > "$BITACORA_FILE"
    echo "" >> "$BITACORA_FILE"
  fi

  cat << EOF >> "$BITACORA_FILE"

---

## [${fecha_bitacora} $(date +%H:%M)] — Registro Manual de Trabajo
**Responsable:** ${RESP_HANDLE} (${RESP_NOMBRE})  
**Área / Módulo:** ${area}  

### 1. Actividades Realizadas
* ${actividades}

### 2. Decisiones Técnicas y Supuestos
* ${decisiones}

### 3. Problemas / Obstáculos Encontrados
* ${obstaculos}

### 4. Próximos Pasos
* ${proximos}
EOF

  echo "✅ Registro de bitácora añadido a: $BITACORA_FILE"
}

# --- MENÚ PRINCIPAL ---
while true; do
  mostrar_encabezado
  echo "1) Nueva Minuta de Reunión"
  echo "2) Nueva Matriz Ponderada de Selección Técnica"
  echo "3) Nueva Matriz de Evaluación de Calidad"
  echo "4) Instanciar / Registrar Tareas RACI (Ex.x) & Múltiples Archivos en Kanban"
  echo "5) Registrar Bitácora Técnica de Trabajo"
  echo "6) Salir"
  echo "======================================================================"
  read -p "Selecciona una opción (1-6): " opcion

  case "$opcion" in
    1) generar_minuta ;;
    2) generar_matriz_ponderada ;;
    3) generar_matriz_evaluacion ;;
    4) instanciar_tarea_raci ;;
    5) registrar_bitacora ;;
    6) echo "👋 Saliendo del Generador RFP-CCM-EM-001."; exit 0 ;;
    *) echo "❌ Opción no válida." ;;
  esac

  echo ""
  read -p "Presiona [Enter] para volver al menú..."
done

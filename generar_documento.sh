#!/bin/bash

# ==============================================================================
# GENERADOR AUTOMATIZADO E INTERACTIVO DE DOCUMENTOS Y MATRICES - RFP-CCM-EM-001
# Lead DevOps & Engineering Automation Standard — Cronograma Exacto
# ==============================================================================

FECHA_ACTUAL=$(date +%Y-%m-%d)
HORA_ACTUAL=$(date +%H:%M)

# Función para agregar una tarjeta individual al tablero KANBAN.md
agregar_a_kanban() {
    local codigo="$1"
    local titulo="$2"
    local asignado="$3"
    local fecha_asig="$4"
    local fecha_limite="$5"
    local labels="$6"

    if [ ! -f "KANBAN.md" ]; then
        cat << 'EOF' > KANBAN.md
# 📋 Tablero Kanban del Proyecto — RFP-CCM-EM-001

> **Leyenda de Estado:**  
> 📌 **Backlog / To Do** | ⏳ **In Progress** | 🔍 **Review / Quality Control** | ✅ **Done**

---

## 📌 To Do / Backlog

---

## ⏳ In Progress

---

## 🔍 Review / Quality Control

---

## ✅ Done
EOF
    fi

    local tarjeta="- [ ] **[${codigo}] ${titulo}**\n  - **Asignado:** ${asignado}\n  - **Fecha Asignación:** ${fecha_asig}\n  - **Entrega Estimada:** ${fecha_limite}\n  - **Etiquetas:** \`${labels}\`"

    if grep -q "## 📌 To Do / Backlog" KANBAN.md; then
        sed -i "/## 📌 To Do \/ Backlog/a \\
${tarjeta}\n" KANBAN.md
        echo "   🎯 Tarjeta individual agregada a KANBAN.md ➔ [${codigo}] (${asignado})"
    fi

    if command -v gh &> /dev/null && gh auth status &> /dev/null; then
        echo "   🌐 Sincronizando issue en GitHub..."
        gh issue create --title "[${codigo}] ${titulo}" --body "Asignado: ${asignado} | Asignado: ${fecha_asig} | Fecha Límite: ${fecha_limite}" --label "${labels}" 2>/dev/null || true
    fi
}

echo "======================================================================"
echo "    🚀 GENERADOR DE MATRICES, MINUTAS Y RACI - RFP-CCM-EM-001         "
echo "======================================================================"
echo "👥 EQUIPO Y ROLES OFICIALES:"
echo "   • Karol Paola Camacho López (@Karoc): Dirección, Python & Optimización"
echo "   • Gildardo Ocaña Barrales (@GildardoOca25): Procesos, Plant 3D & DTI/P&ID"
echo "   • Paulina Mota Macip (@paulina145): Simulación DWSIM & Control"
echo "   • Grecia Figueroa Rincón (@Cho0bb): Eval. Económica (BioSTEAM) & HSE"
echo "======================================================================"
echo "1) Nueva Minuta de Reunión"
echo "2) Nueva Matriz Ponderada de Selección Técnica"
echo "3) Nueva Matriz de Evaluación de Calidad (con tareas correctivas Ex.x)"
echo "4) Instanciar / Registrar Tareas RACI (Ex.x) & Tablero Kanban"
echo "5) Registrar / Consultar Bitácora Técnica de Trabajo"
echo "6) Salir"
echo "======================================================================"
read -p "Selecciona una opción (1-6): " OPCION

case $OPCION in
  1)
    echo -e "\n--- 📝 NUEVA MINUTA DE REUNIÓN ---"
    read -p "Número de minuta (ej. 01, 02) [01]: " NUM
    NUM=${NUM:-01}
    read -p "Fecha (YYYY-MM-DD) [${FECHA_ACTUAL}]: " FECHA
    FECHA=${FECHA:-$FECHA_ACTUAL}
    read -p "Hora (HH:MM) [${HORA_ACTUAL}]: " HORA
    HORA=${HORA:-$HORA_ACTUAL}
    read -p "Lugar / Medio [Google Meet]: " MEDIO
    MEDIO=${MEDIO:-"Google Meet"}
    read -p "Motivo / Tema principal de la reunión: " MOTIVO
    read -p "Moderador / Redactor [@Karoc]: " MODERADOR
    MODERADOR=${MODERADOR:-"@Karoc"}
    read -p "Asistentes (ej. @Karoc, @GildardoOca25, @paulina145, @Cho0bb): " ASISTENTES_RAW
    read -p "Puntos principales tratados: " PUNTOS_RAW
    read -p "Decisiones o acuerdos adoptados: " DECISIONES_RAW

    DEST="00_Gestion_Proyecto/Minutas/${FECHA}_MIN-${NUM}_v0.1.md"
    cp 00_Gestion_Proyecto/Plantillas/MINUTA_PLANTILLA.md "$DEST"

    sed -i "s/{{NUM_MINUTA}}/${NUM}/g" "$DEST"
    sed -i "s/{{FECHA}}/${FECHA}/g" "$DEST"
    sed -i "s/{{HORA}}/${HORA}/g" "$DEST"
    sed -i "s/{{MEDIO}}/${MEDIO}/g" "$DEST"
    sed -i "s/{{MOTIVO}}/${MOTIVO:-"Seguimiento técnico"}/g" "$DEST"
    sed -i "s/{{MODERADOR}}/${MODERADOR}/g" "$DEST"
    sed -i "s|{{ASISTENTES}}|${ASISTENTES_RAW:-""}|g" "$DEST"
    sed -i "s|{{PUNTOS_TRATADOS}}|1. ${PUNTOS_RAW:-"Revisión de avances del proyecto"}|g" "$DEST"
    sed -i "s|{{DECISIONES}}|${DECISIONES_RAW:-"| DEC-01 | General | Acuerdos registrados | Cumplimiento del plan |"}|g" "$DEST"

    echo -e "\n--- 👥 REGISTRO DE COMPROMISOS Y TAREAS POR INTEGRANTE ---"
    TABLA_COMPROMISOS=""
    CONTADOR_COMP=1

    while true; do
      read -p "¿Deseas registrar un compromiso/tarea individual para un integrante? (s/n) [s]: " RESP_ADD
      RESP_ADD=${RESP_ADD:-"s"}
      if [[ "$RESP_ADD" =~ ^[Nn]$ ]]; then
        break
      fi

      echo "  👉 Registro de Tarea #${CONTADOR_COMP}:"
      read -p "     Código de Entregable (ej. E0, E1.1, E1.2, E1.3, E1.4): " COMP_COD
      COMP_COD=${COMP_COD:-"MIN-${NUM}"}
      read -p "     Descripción de la Tarea: " COMP_DESC
      read -p "     Responsable (@Karoc, @GildardoOca25, @paulina145, @Cho0bb) [@Karoc]: " COMP_RESP
      COMP_RESP=${COMP_RESP:-"@Karoc"}
      read -p "     Fecha de Asignación (YYYY-MM-DD) [${FECHA}]: " COMP_FECHA_ASIG
      COMP_FECHA_ASIG=${COMP_FECHA_ASIG:-$FECHA}
      read -p "     Fecha Límite (YYYY-MM-DD) [${FECHA}]: " COMP_FECHA
      COMP_FECHA=${COMP_FECHA:-$FECHA}
      read -p "     Etiquetas [Minuta,${COMP_COD}]: " COMP_LABELS
      COMP_LABELS=${COMP_LABELS:-"Minuta,${COMP_COD}"}

      TABLA_COMPROMISOS="${TABLA_COMPROMISOS}| ${COMP_COD} | ${COMP_DESC} | ${COMP_RESP} | ${COMP_COD} | ${COMP_FECHA} | En Proceso |\n"

      agregar_a_kanban "${COMP_COD}" "${COMP_DESC}" "${COMP_RESP}" "${COMP_FECHA_ASIG}" "${COMP_FECHA}" "${COMP_LABELS}"

      CONTADOR_COMP=$((CONTADOR_COMP + 1))
    done

    if [ -z "$TABLA_COMPROMISOS" ]; then
      TABLA_COMPROMISOS="| MIN-${NUM} | Revisión general de entregables | ${MODERADOR} | General | ${FECHA} | En Proceso |"
    fi

    sed -i "s|{{COMPROMISOS}}|${TABLA_COMPROMISOS}|g" "$DEST"

    read -p "Fecha de próxima reunión [YYYY-MM-DD]: " PROXIMA_FECHA
    sed -i "s/{{PROXIMA_REUNION_FECHA}}/${PROXIMA_FECHA:-"Por definir"}/g" "$DEST"

    echo "✅ Minuta de Reunión creada exitosamente en: $DEST"
    ;;

  2)
    echo -e "\n--- 📊 NUEVA MATRIZ PONDERADA DE SELECCIÓN TÉCNICA ---"
    read -p "Nombre corto del análisis (ej. Seleccion_Reactor_eMethanol): " NOMBRE
    NOMBRE=${NOMBRE:-"Seleccion_Tecnologica"}
    read -p "Nombre Opción A [Electrólisis SOEC High-Temp]: " OPCION_A
    OPCION_A=${OPCION_A:-"Electrólisis SOEC High-Temp"}
    read -p "Nombre Opción B [Electrólisis PEM Standard]: " OPCION_B
    OPCION_B=${OPCION_B:-"Electrólisis PEM Standard"}
    read -p "Nombre Opción C [Electrólisis Alcalina AEL]: " OPCION_C
    OPCION_C=${OPCION_C:-"Electrólisis Alcalina AEL"}
    read -p "Opción Seleccionada [$OPCION_A]: " OPCION_SELECCIONADA
    OPCION_SELECCIONADA=${OPCION_SELECCIONADA:-$OPCION_A}
    read -p "Justificación técnica sustentada: " JUSTIFICACION
    read -p "Evaluador / Auditor [@Karoc]: " EVALUADOR
    EVALUADOR=${EVALUADOR:-"@Karoc"}
    read -p "Fecha [${FECHA_ACTUAL}]: " FECHA
    FECHA=${FECHA:-$FECHA_ACTUAL}

    DEST="00_Gestion_Proyecto/Matriz_Ponderada/${FECHA}_Matriz_Ponderada_${NOMBRE}_v0.1.md"
    cp 00_Gestion_Proyecto/Plantillas/MATRIZ_PONDERADA_PLANTILLA.md "$DEST"

    sed -i "s/{{NOMBRE_ANALISIS}}/${NOMBRE}/g" "$DEST"
    sed -i "s/{{OPCION_A}}/${OPCION_A}/g" "$DEST"
    sed -i "s/{{OPCION_B}}/${OPCION_B}/g" "$DEST"
    sed -i "s/{{OPCION_C}}/${OPCION_C}/g" "$DEST"
    sed -i "s/{{OPCION_SELECCIONADA}}/${OPCION_SELECCIONADA}/g" "$DEST"
    sed -i "s/{{JUSTIFICACION}}/${JUSTIFICACION:-"Mayor eficiencia termodinámica e integración de calor de proceso."}/g" "$DEST"
    sed -i "s/{{EVALUADOR}}/${EVALUADOR}/g" "$DEST"
    sed -i "s/{{FECHA}}/${FECHA}/g" "$DEST"

    echo "✅ Matriz Ponderada creada exitosamente en: $DEST"

    read -p "¿Deseas generar una tarjeta en Kanban para la implementación de la opción seleccionada? (s/n) [s]: " GEN_CARD
    if [[ ! "$GEN_CARD" =~ ^[Nn]$ ]]; then
      read -p "  Código de Entregable Asociado (ej. E1.1, E1.2, E1.4): " IMPL_COD
      read -p "  Responsable (@Karoc, @GildardoOca25, @paulina145, @Cho0bb) [$EVALUADOR]: " IMPL_RESP
      read -p "  Fecha de Asignación: " IMPL_ASIG
      read -p "  Fecha límite de implementación: " IMPL_FECHA
      agregar_a_kanban "${IMPL_COD:-MP-${NOMBRE}}" "Implementar Opción Seleccionada: ${OPCION_SELECCIONADA}" "${IMPL_RESP:-$EVALUADOR}" "${IMPL_ASIG:-$FECHA}" "${IMPL_FECHA:-$FECHA}" "Matriz,Ingenieria"
    fi
    ;;

  3)
    echo -e "\n--- 🔍 NUEVA MATRIZ DE EVALUACIÓN DE CALIDAD DE ENTREGABLES ---"
    while true; do
      read -p "Código del Entregable evaluado (ej. E0, E1, E1.1, E1.2, E1.3, E1.4, EF): " ENT
      if [[ "$ENT" =~ ^(E[0-4](\.[0-9]+)?|EF)$ ]]; then
        break
      else
        echo "❌ Código inválido. Debe ser E0-E4, EF o un subentregable como E1.1, E1.2, E1.3, E1.4."
      fi
    done

    read -p "Nombre del Archivo Evaluado (ej. ${ENT}_SIM_Termodinamica_v1.0.dwxmz): " NOMBRE_ARCHIVO
    read -p "Evaluador / Auditor [@Karoc]: " EVALUADOR
    EVALUADOR=${EVALUADOR:-"@Karoc"}
    read -p "Fecha de Revisión [${FECHA_ACTUAL}]: " FECHA
    FECHA=${FECHA:-$FECHA_ACTUAL}

    echo "Calificación de Criterios (1: No cumple, 2: Parcial, 3: Aceptable, 4: Excelente):"
    read -p "CR-01 Nomenclatura (1-4) [4]: " CR1
    CR1=${CR1:-4}
    read -p "CR-02 Formato y Estructura (1-4) [4]: " CR2
    CR2=${CR2:-4}
    read -p "CR-03 Rigor Técnico y Cálculos (1-4) [4]: " CR3
    CR3=${CR3:-4}
    read -p "CR-04 Soporte Gráfico / CAD (1-4) [4]: " CR4
    CR4=${CR4:-4}
    read -p "CR-05 Trazabilidad RACI (1-4) [4]: " CR5
    CR5=${CR5:-4}

    PROMEDIO=$(awk "BEGIN {print ($CR1 + $CR2 + $CR3 + $CR4 + $CR5)/5}")

    echo "Dictamen Final:"
    echo "1) Aprobado para Entrega Oficial"
    echo "2) Aprobado con Observaciones Menores"
    echo "3) Rechazado"
    read -p "Selecciona dictamen (1-3) [1]: " OP_DICTAMEN

    CHK_APR=" "
    CHK_OBS=" "
    CHK_REC=" "

    case $OP_DICTAMEN in
      2) CHK_OBS="x" ;;
      3) CHK_REC="x" ;;
      *) CHK_APR="x" ;;
    esac

    DEST="00_Gestion_Proyecto/${FECHA}_Evaluacion_Calidad_${ENT}_v0.1.md"
    cp 00_Gestion_Proyecto/Plantillas/MATRIZ_EVALUACION_PLANTILLA.md "$DEST"

    sed -i "s/{{CODIGO_ENTREGABLE}}/${ENT}/g" "$DEST"
    sed -i "s/{{NOMBRE_ARCHIVO}}/${NOMBRE_ARCHIVO:-"${ENT}_DOC_Entregable_v1.0.pdf"}/g" "$DEST"
    sed -i "s/{{EVALUADOR}}/${EVALUADOR}/g" "$DEST"
    sed -i "s/{{FECHA}}/${FECHA}/g" "$DEST"

    sed -i "s/{{CALIF_CR01}}/${CR1}/g" "$DEST"
    sed -i "s/{{OBS_CR01}}/Conforme a la regla oficial./g" "$DEST"
    sed -i "s/{{ESTADO_CR01}}/✅ Aprobado/g" "$DEST"

    sed -i "s/{{CALIF_CR02}}/${CR2}/g" "$DEST"
    sed -i "s/{{OBS_CR02}}/Estructura y formato verificado./g" "$DEST"
    sed -i "s/{{ESTADO_CR02}}/✅ Aprobado/g" "$DEST"

    sed -i "s/{{CALIF_CR03}}/${CR3}/g" "$DEST"
    sed -i "s/{{OBS_CR03}}/Rigor técnico y balances validados./g" "$DEST"
    sed -i "s/{{ESTADO_CR03}}/✅ Aprobado/g" "$DEST"

    sed -i "s/{{CALIF_CR04}}/${CR4}/g" "$DEST"
    sed -i "s/{{OBS_CR04}}/Diagramas y resolución conformes./g" "$DEST"
    sed -i "s/{{ESTADO_CR04}}/✅ Aprobado/g" "$DEST"

    sed -i "s/{{CALIF_CR05}}/${CR5}/g" "$DEST"
    sed -i "s/{{OBS_CR05}}/Trazabilidad asignada en Matriz RACI./g" "$DEST"
    sed -i "s/{{ESTADO_CR05}}/✅ Aprobado/g" "$DEST"

    sed -i "s/{{PROMEDIO}}/${PROMEDIO}/g" "$DEST"
    sed -i "s/{{DICTAMEN_CHECK_APROBADO}}/${CHK_APR}/g" "$DEST"
    sed -i "s/{{DICTAMEN_CHECK_OBS}}/${CHK_OBS}/g" "$DEST"
    sed -i "s/{{DICTAMEN_CHECK_RECHAZADO}}/${CHK_REC}/g" "$DEST"

    echo "✅ Matriz de Evaluación de Calidad creada exitosamente en: $DEST"

    while true; do
      read -p "¿Deseas asignar una tarea de corrección/ajuste a un integrante basado en la auditoría? (s/n) [n]: " ADD_CORR
      if [[ ! "$ADD_CORR" =~ ^[Ss]$ ]]; then
        break
      fi
      read -p "  Descripción del ajuste requerido: " CORR_DESC
      read -p "  Responsable (@Karoc, @GildardoOca25, @paulina145, @Cho0bb) [@Karoc]: " CORR_RESP
      read -p "  Fecha de Asignación: " CORR_ASIG
      read -p "  Fecha límite de corrección: " CORR_FECHA
      agregar_a_kanban "${ENT}" "${CORR_DESC}" "${CORR_RESP:-$EVALUADOR}" "${CORR_ASIG:-$FECHA}" "${CORR_FECHA:-$FECHA}" "QA,Correccion,${ENT}"
    done
    ;;

  4)
    echo -e "\n--- 📋 REGISTRO MULTI-TAREA EN MATRIZ RACI & KANBAN ---"
    MATRIZ_RACI="00_Gestion_Proyecto/Matriz_RACI/RACI_General_v1.0.md"
    NUM_TAREA=1

    while true; do
      echo -e "\n👉 Ingresando Tarea #${NUM_TAREA}:"
      read -p "  Código de Entregable / Subentregable (ej. E0, E1.1, E1.2, E1.3, E1.4): " COD_TAREA
      if [ -z "$COD_TAREA" ]; then
        echo "⚠️ Código de entregable requerido (ej. E0, E1.1)."
        continue
      fi

      read -p "  Título / Descripción de la Tarea: " TITULO_TAREA
      read -p "  Asignado a (@Karoc, @GildardoOca25, @paulina145, @Cho0bb) [@Karoc]: " ASIGNADO
      ASIGNADO=${ASIGNADO:-"@Karoc"}
      read -p "  Rol RACI (R = Responsable, A = Aprobador, C = Consultado, I = Informado) [Responsible]: " ROL_RACI
      ROL_RACI=${ROL_RACI:-"Responsible"}
      read -p "  Ruta o Archivo de Entregables Asociado: " ENT_PATH
      read -p "  Fecha de Asignación (YYYY-MM-DD): " FECHA_ASIG
      read -p "  Fecha Límite (YYYY-MM-DD): " FECHA_ENTREGA
      read -p "  Etiquetas / Labels (ej. ${COD_TAREA}, SIM, DWSIM): " LABELS
      LABELS=${LABELS:-"${COD_TAREA}"}

      if [ -f "$MATRIZ_RACI" ]; then
          echo "- [ ] **[${COD_TAREA}] ${TITULO_TAREA}**" >> "$MATRIZ_RACI"
          echo "  - **Asignado a:** ${ASIGNADO}" >> "$MATRIZ_RACI"
          echo "  - **RACI:** ${ROL_RACI}" >> "$MATRIZ_RACI"
          echo "  - **Fecha de Asignación:** ${FECHA_ASIG}" >> "$MATRIZ_RACI"
          echo "  - **Fecha Límite:** ${FECHA_ENTREGA}" >> "$MATRIZ_RACI"
          echo "  - **Código Entregable:** \`${ENT_PATH:-"Por definir"}\`" >> "$MATRIZ_RACI"
          echo "  - **Labels:** \`${LABELS}\`" >> "$MATRIZ_RACI"
          echo "" >> "$MATRIZ_RACI"
          echo "   ✅ Tarea agregada a Matriz RACI General ($MATRIZ_RACI)"
      fi

      agregar_a_kanban "${COD_TAREA}" "${TITULO_TAREA}" "${ASIGNADO}" "${FECHA_ASIG}" "${FECHA_ENTREGA}" "${LABELS}"

      NUM_TAREA=$((NUM_TAREA + 1))

      read -p "¿Deseas agregar OTRA tarea para otro integrante? (s/n) [n]: " RESP_MAS
      if [[ ! "$RESP_MAS" =~ ^[Ss]$ ]]; then
        break
      fi
    done
    ;;

  5)
    echo -e "\n--- 📖 BITÁCORA TÉCNICA DE TRABAJO ---"
    echo "Nota: La bitácora se actualiza automáticamente en GitHub en cada push/commit."
    echo "Si deseas registrar una entrada manual en la bitácora local de hoy:"
    read -p "Título / Tema de la actividad realizada: " TITULO
    read -p "Responsable (@Karoc, @GildardoOca25, @paulina145, @Cho0bb) [@Karoc]: " RESPONSABLE
    RESPONSABLE=${RESPONSABLE:-"@Karoc"}
    read -p "Área / Módulo (ej. 01_Proceso_y_Simulacion/DWSIM): " AREA
    read -p "Actividades realizadas: " ACTIVIDADES
    read -p "Decisiones técnicas / supuestos: " DECISIONES
    read -p "Obstáculos / Problemas encontrados: " OBSTACULOS
    read -p "Próximos pasos: " PROXIMOS

    DEST="04_Bitacora/BITACORA_${FECHA_ACTUAL}.md"

    if [ ! -f "$DEST" ]; then
      cp 00_Gestion_Proyecto/Plantillas/BITACORA_PLANTILLA.md "$DEST"
      sed -i "s/{{FECHA}}/${FECHA_ACTUAL}/g" "$DEST"
    fi

    sed -i "s/{{TITULO}}/${TITULO:-"Actividad Técnica"}/g" "$DEST"
    sed -i "s/{{RESPONSABLE}}/${RESPONSABLE}/g" "$DEST"
    sed -i "s|{{AREA_MODULO}}|${AREA:-"General"}|g" "$DEST"
    sed -i "s|{{ACTIVIDADES}}|* ${ACTIVIDADES:-"Avance en documentación"}|g" "$DEST"
    sed -i "s|{{DECISIONES}}|* ${DECISIONES:-"Ninguna relevante"}|g" "$DEST"
    sed -i "s|{{OBSTACULOS}}|* ${OBSTACULOS:-"Ninguno"}|g" "$DEST"
    sed -i "s|{{PROXIMOS_PASOS}}|* ${PROXIMOS:-"Continuar según plan"}|g" "$DEST"

    echo "✅ Bitácora actualizada en: $DEST"
    ;;

  6)
    echo "👋 Saliendo del Generador RFP-CCM-EM-001."
    exit 0
    ;;

  *)
    echo "❌ Opción no válida."
    exit 1
    ;;
esac

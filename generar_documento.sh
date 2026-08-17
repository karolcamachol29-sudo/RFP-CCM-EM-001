#!/bin/bash

# Generador de Documentos Oficiales RFP-CCM-EM-001
FECHA=$(date +%Y-%m-%d)

echo "=================================================="
echo " GENERADOR DE DOCUMENTOS Y MATRICES - RFP-CCM-EM-001"
echo "=================================================="
echo "1) Nueva Minuta de Reunión"
echo "2) Nueva Matriz Ponderada de Selección"
echo "3) Nueva Matriz de Evaluación de Calidad"
echo "=================================================="
read -p "Selecciona una opción (1-3): " OPCION

case $OPCION in
  1)
    read -p "Número de minuta (ej. 01, 02): " NUM
    DEST="00_Gestion_Proyecto/Minutas/${FECHA}_MIN-${NUM}_v0.1.md"
    cp 00_Gestion_Proyecto/Plantillas/MINUTA_PLANTILLA.md "$DEST"
    echo "✅ Minuta creada exitosamente en: $DEST"
    ;;
  2)
    read -p "Nombre corto del análisis (ej. Seleccion_Reactor): " NOMBRE
    DEST="00_Gestion_Proyecto/Plantillas/${FECHA}_Matriz_Ponderada_${NOMBRE}_v0.1.md"
    cp 00_Gestion_Proyecto/Plantillas/MATRIZ_PONDERADA_PLANTILLA.md "$DEST"
    echo "✅ Matriz Ponderada creada exitosamente en: $DEST"
    ;;
  3)
    read -p "Código del Entregable evaluado (ej. E0, E1): " ENT
    DEST="00_Gestion_Proyecto/Plantillas/${FECHA}_Evaluacion_Calidad_${ENT}_v0.1.md"
    cp 00_Gestion_Proyecto/Plantillas/MATRIZ_EVALUACION_PLANTILLA.md "$DEST"
    echo "✅ Matriz de Evaluación creada exitosamente en: $DEST"
    ;;
  *)
    echo "❌ Opción no válida."
    exit 1
    ;;
esac

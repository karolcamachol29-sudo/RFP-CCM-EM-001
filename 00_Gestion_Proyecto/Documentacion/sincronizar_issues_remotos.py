#!/usr/bin/env python3
"""
Script de creación y sincronización masiva de GitHub Issues y GitHub Projects V2
Consorcio Solvanta Engineering Solutions S.A. de C.V. — RFP-CCM-EM-001
"""

import subprocess
import json
import os
import csv
import re

TASKS_DEF = [
    # --- E0 ---
    {
        "code": "E0",
        "title": "[E0] Redactar Acta Constitutiva y Gestión Inicial",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-08-14",
        "end": "2026-08-17",
        "labels": "E0,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E0_Constitucion/E0_DOC_ActaConstitutiva_v1.0.pdf"
    },
    # --- E1 ---
    {
        "code": "E1.1",
        "title": "[E1.1] Configuración de Bases de Diseño & Termodinámica",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad, Salud y Medio Ambiente (HSE)",
        "participantes": "@Cho0bb, @Karoc, @paulina145, @GildardoOca25",
        "raci": "R: @Cho0bb | A: @Karoc | C: @GildardoOca25, @paulina145 | I: Convocante",
        "start": "2026-08-17",
        "end": "2026-08-25",
        "labels": "E1.1,DOC,HSE",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.1_DOC_BasesDiseno_v1.0.pdf"
    },
    {
        "code": "E1.2",
        "title": "[E1.2] Simulación de Procesos & Balances (DWSIM)",
        "assignee": "paulina145",
        "cargo": "Simulación",
        "participantes": "@paulina145, @GildardoOca25, @Karoc, @Cho0bb",
        "raci": "R: @paulina145 | A: @Karoc | C: @GildardoOca25, @Cho0bb | I: Consorcio",
        "start": "2026-08-18",
        "end": "2026-08-25",
        "labels": "E1.2,SIM,DWSIM",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.2_DOC_ReporteSimulacion_v1.0.pdf"
    },
    {
        "code": "E1.3",
        "title": "[E1.3] Diagramación Plant 3D & Especificación Técnica",
        "assignee": "GildardoOca25",
        "cargo": "Ingeniería de Procesos / DTI y P&ID",
        "participantes": "@GildardoOca25, @paulina145, @Karoc, @Cho0bb",
        "raci": "R: @GildardoOca25 | A: @Karoc | C: @paulina145, @Cho0bb | I: Consorcio",
        "start": "2026-08-19",
        "end": "2026-08-24",
        "labels": "E1.3,DWG,CAD",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.3_DOC_EspecificacionDiagramas_v1.0.pdf"
    },
    {
        "code": "E1.3.1",
        "title": "[E1.3.1] Propuesta preliminar de equipos y parámetros de diseño (EQ-01)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Ingeniera de Optimización Python / Dirección",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc | A: @Karoc | C: @GildardoOca25, @paulina145 | I: @Cho0bb",
        "start": "2026-08-26",
        "end": "2026-08-28",
        "labels": "E1.3.1,DOC,EQ-01",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.3.1_DOC_PropuestaEquipos_v1.0.pdf"
    },
    {
        "code": "E1.4",
        "title": "[E1.4] Video Pitch del Proyecto (Enlace Drive)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto / Optimización Python",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-08-20",
        "end": "2026-08-25",
        "labels": "E1.4,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.4_VID_EnlacePitch_v1.0.pdf"
    },
    {
        "code": "E1.4-P1",
        "title": "[E1.4-P1] Segmento 1 Video Pitch: Apertura Ejecutiva y Optimización SOEC en Python",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto / Ingeniera de Optimización Python",
        "participantes": "@Karoc",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-08-23",
        "end": "2026-08-24",
        "labels": "E1.4,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.4_VID_EnlacePitch_v1.0.pdf"
    },
    {
        "code": "E1.4-P2",
        "title": "[E1.4-P2] Segmento 2 Video Pitch: Arquitectura de Proceso, Síntesis y Balances",
        "assignee": "GildardoOca25",
        "cargo": "Ingeniería de Procesos / DTI y P&ID",
        "participantes": "@GildardoOca25",
        "raci": "R: @GildardoOca25 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-08-23",
        "end": "2026-08-24",
        "labels": "E1.4,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.4_VID_EnlacePitch_v1.0.pdf"
    },
    {
        "code": "E1.4-P3",
        "title": "[E1.4-P3] Segmento 3 Video Pitch: Simulación en DWSIM y Control de Procesos",
        "assignee": "paulina145",
        "cargo": "Simulación / Instrumentación y Control",
        "participantes": "@paulina145",
        "raci": "R: @paulina145 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-08-23",
        "end": "2026-08-24",
        "labels": "E1.4,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.4_VID_EnlacePitch_v1.0.pdf"
    },
    {
        "code": "E1.4-P4",
        "title": "[E1.4-P4] Segmento 4 Video Pitch: Sostenibilidad Ambiental, Riesgos y Economía",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad HSE / Evaluación Económica",
        "participantes": "@Cho0bb",
        "raci": "R: @Cho0bb | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-08-23",
        "end": "2026-08-24",
        "labels": "E1.4,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.4_VID_EnlacePitch_v1.0.pdf"
    },
    # --- RT-01 ---
    {
        "code": "RT-01",
        "title": "[RT-01] Revisión Técnica 01: Defensa de Bases de Diseño (AR-01)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Cargos respectivos en exposición colegiada",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: Sínodo",
        "start": "2026-08-25",
        "end": "2026-08-28",
        "labels": "RT-01,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/RT-01_DOC_PresentacionDiapositivas_v1.0.pdf"
    },
    # --- MP-00 ---
    {
        "code": "MP-00",
        "title": "[MP-00] Compendio de Matrices Ponderadas de Selección Técnica (MP-01 a MP-05)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto y Especialidades Técnicas",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-09-01",
        "end": "2026-09-10",
        "labels": "MP-00,DOC",
        "done": True,
        "evidencia": "00_Gestion_Proyecto/Matriz_Ponderada/MP-00_DOC_CompendioMatricesPonderadas_v1.0.pdf"
    },
    # --- E1.5 & E1.6 ---
    {
        "code": "E1.5",
        "title": "[E1.5] Verificación Termodinámica, Tablas TC-01/TE-01 y DFP v1 (VTP-01)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Optimización Python / Ing. Procesos / Simulación",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145 | A: @Karoc | C: @Cho0bb | I: Dr. Jesús Andrés Arzola",
        "start": "2026-09-10",
        "end": "2026-09-21",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.5_DOC_ActividadVTP_v1.0.pdf"
    },
    {
        "code": "E1.6",
        "title": "[E1.6] Matriz Integral de Aspectos, Impactos y Requisitos Ambientales (AC-AMB-01)",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad, Salud y Medio Ambiente (HSE)",
        "participantes": "@Cho0bb, @Karoc, @paulina145, @GildardoOca25",
        "raci": "R: @Cho0bb | A: @Karoc | C: @paulina145, @GildardoOca25 | I: Consorcio",
        "start": "2026-09-17",
        "end": "2026-09-21",
        "labels": "DOC,HSE",
        "done": True,
        "evidencia": "03_Entregables_Finales/E1_Bases_y_Verificacion/E1.6_DOC_MatrizAmbiental_v1.0.pdf"
    },
    # --- E2.1 ---
    {
        "code": "E2.1",
        "title": "[E2.1] Lista Maestra de Equipos (LE-01) y DFP v1",
        "assignee": "GildardoOca25",
        "cargo": "Ing. Procesos / Simulación / Optimización Python",
        "participantes": "@GildardoOca25, @paulina145, @Karoc, @Cho0bb",
        "raci": "R: @GildardoOca25, @paulina145, @Karoc | A: @Karoc | C: @Cho0bb | I: Titular DPyPQ",
        "start": "2026-09-17",
        "end": "2026-09-24",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/E2.1_DOC_ListaEquipos_v1.0.pdf"
    },
    # --- RT-02 & E2.2 ---
    {
        "code": "RT-02",
        "title": "[RT-02] Revisión Técnica 02: Diapositivas y Guion Oficial de Speech",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Cargos respectivos en exposición colegiada",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: Sínodo",
        "start": "2026-09-24",
        "end": "2026-09-28",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/RT-02_DOC_PresentacionDiapositivas_v1.0.pdf"
    },
    {
        "code": "E2.2",
        "title": "[E2.2] Video Oficial de la Revisión Técnica 02 (RT-02 en Canva)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto / Cargos Oficiales Respectivos",
        "participantes": "@Karoc, @paulina145, @GildardoOca25, @Cho0bb",
        "raci": "R: @Karoc, @paulina145, @GildardoOca25, @Cho0bb | A: @Karoc | C: Consorcio | I: Convocante BUAP",
        "start": "2026-09-24",
        "end": "2026-09-28",
        "labels": "E2.2,VID,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/E2.2_VID_EnlaceRevisionTecnica02_v1.0.pdf"
    },
    {
        "code": "E2.2-P1",
        "title": "[E2.2-P1] Segmento 1 Video RT-02: Apertura Ejecutiva y Reciclos de Proceso",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto / Ingeniera de Optimización Python",
        "participantes": "@Karoc",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-09-26",
        "end": "2026-09-27",
        "labels": "E2.2,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/E2.2_VID_EnlaceRevisionTecnica02_v1.0.pdf"
    },
    {
        "code": "E2.2-P2",
        "title": "[E2.2-P2] Segmento 2 Video RT-02: Simulación en DWSIM y Lazos de Control",
        "assignee": "paulina145",
        "cargo": "Simulación / Instrumentación y Control",
        "participantes": "@paulina145",
        "raci": "R: @paulina145 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-09-26",
        "end": "2026-09-27",
        "labels": "E2.2,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/E2.2_VID_EnlaceRevisionTecnica02_v1.0.pdf"
    },
    {
        "code": "E2.2-P3",
        "title": "[E2.2-P3] Segmento 3 Video RT-02: Equipos Mayores LE-01 e Instalaciones",
        "assignee": "GildardoOca25",
        "cargo": "Ingeniería de Procesos / DTI y P&ID",
        "participantes": "@GildardoOca25",
        "raci": "R: @GildardoOca25 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-09-26",
        "end": "2026-09-27",
        "labels": "E2.2,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/E2.2_VID_EnlaceRevisionTecnica02_v1.0.pdf"
    },
    {
        "code": "E2.2-P4",
        "title": "[E2.2-P4] Segmento 4 Video RT-02: Sustentabilidad y Matriz Ambiental AC-AMB-01",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad HSE / Evaluación Económica",
        "participantes": "@Cho0bb",
        "raci": "R: @Cho0bb | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-09-26",
        "end": "2026-09-27",
        "labels": "E2.2,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/E2.2_VID_EnlaceRevisionTecnica02_v1.0.pdf"
    },
    # --- FC-01, HAZOP, PIB ---
    {
        "code": "FC-01",
        "title": "[FC-01] Filosofía de Control del Proceso de Síntesis y Separación",
        "assignee": "paulina145",
        "cargo": "Instrumentación y Control / Simulación",
        "participantes": "@paulina145, @GildardoOca25, @Karoc, @Cho0bb",
        "raci": "R: @paulina145 | A: @Karoc | C: @GildardoOca25, @Karoc, @Cho0bb | I: Consorcio",
        "start": "2026-10-01",
        "end": "2026-10-08",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/FC-01_DOC_FilosofiaControl_v1.0.pdf"
    },
    {
        "code": "AC-HAZOP-01",
        "title": "[AC-HAZOP-01] Expediente de Seguridad HAZOP y Matriz Causa-Efecto (MCE-01)",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad, Salud y Medio Ambiente (HSE)",
        "participantes": "@Cho0bb, @Karoc, @GildardoOca25, @paulina145",
        "raci": "R: @Cho0bb | A: @Karoc | C: @GildardoOca25, @paulina145 | I: Consorcio",
        "start": "2026-10-08",
        "end": "2026-10-19",
        "labels": "DOC,HSE",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/AC-HAZOP-01_DOC_ExpedienteHAZOP_v1.0.pdf"
    },
    {
        "code": "PIB-01",
        "title": "[PIB-01] Paquete de Ingeniería Básica del Proceso (Solvanta-PIB-01)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto y Especialidades Técnicas",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc | A: @Karoc | C: @paulina145, @GildardoOca25, @Cho0bb | I: Consorcio",
        "start": "2026-10-20",
        "end": "2026-10-28",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E2_Ingenieria_Basica_y_Control/PIB-01_DOC_ExpedienteIngenieriaBasica_v1.0.pdf"
    },
    # --- E4 AUDITORÍAS ---
    {
        "code": "E4.1",
        "title": "[E4.1] RPT Auditoría Económica Integral en BioSTEAM (CAPEX/OPEX)",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad HSE / Evaluación Económica",
        "participantes": "@Cho0bb, @Karoc",
        "raci": "R: @Cho0bb, @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-10-28",
        "end": "2026-11-01",
        "labels": "E4,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.1_RPT_AuditoriaEconomicaIntegral_v1.0.pdf"
    },
    {
        "code": "E4.2",
        "title": "[E4.2] RPT Comparativa Rigurosa de Balances DWSIM vs BioSTEAM",
        "assignee": "paulina145",
        "cargo": "Simulación / Instrumentación y Control",
        "participantes": "@paulina145, @Karoc",
        "raci": "R: @paulina145, @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-10-29",
        "end": "2026-11-02",
        "labels": "E4,SIM,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.2_RPT_ComparativaDWSIMvsBioSTEAM_v1.0.pdf"
    },
    {
        "code": "E4.3",
        "title": "[E4.3] RPT Desglose Analítico de Costos CAPEX y OPEX (Factores Guthrie)",
        "assignee": "Cho0bb",
        "cargo": "Evaluación Económica / Especialista en Seguridad HSE",
        "participantes": "@Cho0bb, @Karoc",
        "raci": "R: @Cho0bb, @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-10-30",
        "end": "2026-11-03",
        "labels": "E4,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.3_RPT_DesgloseCostosCAPEXOPEX_v1.0.pdf"
    },
    {
        "code": "E4.4",
        "title": "[E4.4] RPT Registro Histórico de Modificaciones Técnicas",
        "assignee": "GildardoOca25",
        "cargo": "Ingeniería de Procesos / DTI y P&ID",
        "participantes": "@GildardoOca25, @Karoc",
        "raci": "R: @GildardoOca25, @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-10-31",
        "end": "2026-11-04",
        "labels": "E4,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.4_RPT_RegistroModificaciones_v1.0.pdf"
    },
    {
        "code": "E4.5",
        "title": "[E4.5] RPT Segunda Auditoría BioSTEAM (Recalibración LCOMe)",
        "assignee": "Cho0bb",
        "cargo": "Evaluación Económica / Especialista en Seguridad HSE",
        "participantes": "@Cho0bb, @Karoc",
        "raci": "R: @Cho0bb, @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-11-01",
        "end": "2026-11-05",
        "labels": "E4,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.5_RPT_SegundaAuditoriaBioSTEAM_v1.0.pdf"
    },
    {
        "code": "E4.6",
        "title": "[E4.6] RPT Auditoría y Optimización Multivariable SOEC en Python",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Ingeniera de Optimización Python / Dirección",
        "participantes": "@Karoc",
        "raci": "R: @Karoc | A: @Karoc | C: @GildardoOca25, @Cho0bb | I: Consorcio",
        "start": "2026-10-28",
        "end": "2026-11-05",
        "labels": "E4,PY,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.6_RPT_AuditoriaOptimizacionSOEC_v1.0.pdf"
    },
    {
        "code": "E4.7",
        "title": "[E4.7] RPT Validación y Banco de 12 Pruebas Unitarias SOEC (pytest)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Ingeniera de Optimización Python / Simulación",
        "participantes": "@Karoc, @paulina145",
        "raci": "R: @Karoc, @paulina145 | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-11-02",
        "end": "2026-11-05",
        "labels": "E4,PY,SIM",
        "done": True,
        "evidencia": "03_Entregables_Finales/E4_Auditorias_y_Optimizacion/E4.7_RPT_ValidacionPruebasSOEC_v1.0.pdf"
    },
    # --- DIF-01 ---
    {
        "code": "DIF-01",
        "title": "[DIF-01] Cartel Oficial de Difusión Técnica para el PyDay BUAP",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Ingeniera de Optimización (Python) & Evaluación Económica",
        "participantes": "ÚNICA Y EXCLUSIVAMENTE @Karoc y @Cho0bb en su elaboración",
        "raci": "R: @Karoc, @Cho0bb | A: @Karoc | C: Ninguno | I: @GildardoOca25, @paulina145",
        "start": "2026-11-03",
        "end": "2026-11-06",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/DIF-01_DOC_CartelPyDay_v1.0.pdf"
    },
    # --- RT-03 & E3.1 ---
    {
        "code": "RT-03",
        "title": "[RT-03] Revisión Técnica 03: Guía Maestra de Defensa y Diapositivas",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Cargos respectivos en defensa final colegiada",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: Comité Licitación",
        "start": "2026-11-01",
        "end": "2026-11-14",
        "labels": "DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/RT-03_DOC_PresentacionDiapositivas_v1.0.pdf"
    },
    {
        "code": "E3.1",
        "title": "[E3.1] Video Oficial de la Revisión Técnica 03 (RT-03 en Canva)",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto / Cargos Oficiales Respectivos",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: Comité Licitación BUAP",
        "start": "2026-11-01",
        "end": "2026-11-14",
        "labels": "E3.1,VID,DOC",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/E3.1_VID_EnlaceRevisionTecnica03_v1.0.pdf"
    },
    {
        "code": "E3.1-P1",
        "title": "[E3.1-P1] Segmento 1 Video RT-03: Visión Directiva y Modelo SOEC en Python",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto / Ingeniera de Optimización Python",
        "participantes": "@Karoc",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-08",
        "end": "2026-11-11",
        "labels": "E3.1,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/E3.1_VID_EnlaceRevisionTecnica03_v1.0.pdf"
    },
    {
        "code": "E3.1-P2",
        "title": "[E3.1-P2] Segmento 2 Video RT-03: Paquete de Planos DTI v1 y Piping",
        "assignee": "GildardoOca25",
        "cargo": "Ingeniería de Procesos / DTI y P&ID",
        "participantes": "@GildardoOca25",
        "raci": "R: @GildardoOca25 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-08",
        "end": "2026-11-11",
        "labels": "E3.1,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/E3.1_VID_EnlaceRevisionTecnica03_v1.0.pdf"
    },
    {
        "code": "E3.1-P3",
        "title": "[E3.1-P3] Segmento 3 Video RT-03: Control Dinámico y Estabilidad en Cascada",
        "assignee": "paulina145",
        "cargo": "Simulación / Instrumentación y Control",
        "participantes": "@paulina145",
        "raci": "R: @paulina145 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-08",
        "end": "2026-11-11",
        "labels": "E3.1,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/E3.1_VID_EnlaceRevisionTecnica03_v1.0.pdf"
    },
    {
        "code": "E3.1-P4",
        "title": "[E3.1-P4] Segmento 4 Video RT-03: Salvaguardas HAZOP MCE-01 y LCOMe BioSTEAM",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad HSE / Evaluación Económica",
        "participantes": "@Cho0bb",
        "raci": "R: @Cho0bb | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-08",
        "end": "2026-11-11",
        "labels": "E3.1,VID",
        "done": True,
        "evidencia": "03_Entregables_Finales/E3_Revisiones_Tecnicas_y_Difusion/E3.1_VID_EnlaceRevisionTecnica03_v1.0.pdf"
    },
    # --- CANVA-REV ---
    {
        "code": "CANVA-REV",
        "title": "[CANVA-REV] Integración y Centralización de Enlaces Oficiales Canva",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto",
        "participantes": "@Karoc, @Cho0bb, @GildardoOca25, @paulina145",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: Convocante",
        "start": "2026-11-14",
        "end": "2026-11-14",
        "labels": "DOC",
        "done": True,
        "evidencia": "00_Gestion_Proyecto/Documentacion/ENLACES_REVISION.txt"
    },
    # --- EF ---
    {
        "code": "EF",
        "title": "[EF] Consolidación del Expediente y Cierre Licitatorio",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto y Especialidades Técnicas",
        "participantes": "@Karoc, @GildardoOca25, @paulina145, @Cho0bb",
        "raci": "R: @Karoc, @GildardoOca25, @paulina145, @Cho0bb | A: @Karoc | C: Consorcio | I: BUAP / DPyPQ",
        "start": "2026-11-10",
        "end": "2026-11-14",
        "labels": "DOC,EF",
        "done": False,
        "evidencia": "03_Entregables_Finales/EF_Informe_Final/"
    },
    {
        "code": "EF-T1",
        "title": "[EF-T1] Tomo I: Bases de Diseño, Capacidad y Gobernanza",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Dirección del Proyecto",
        "participantes": "@Karoc",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-10",
        "end": "2026-11-14",
        "labels": "EF,DOC",
        "done": False,
        "evidencia": "03_Entregables_Finales/EF_Informe_Final/"
    },
    {
        "code": "EF-T2",
        "title": "[EF-T2] Tomo II: Ingeniería de Procesos, Diagramas (BFD/PFD/DTI) y LE-01",
        "assignee": "GildardoOca25",
        "cargo": "Ingeniería de Procesos / DTI y P&ID",
        "participantes": "@GildardoOca25",
        "raci": "R: @GildardoOca25 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-11",
        "end": "2026-11-14",
        "labels": "EF,DOC,DWG",
        "done": False,
        "evidencia": "03_Entregables_Finales/EF_Informe_Final/"
    },
    {
        "code": "EF-T3",
        "title": "[EF-T3] Tomo III: Balances DWSIM y Filosofía de Control Automático",
        "assignee": "paulina145",
        "cargo": "Simulación / Instrumentación y Control",
        "participantes": "@paulina145",
        "raci": "R: @paulina145 | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-11",
        "end": "2026-11-14",
        "labels": "EF,SIM,DOC",
        "done": False,
        "evidencia": "03_Entregables_Finales/EF_Informe_Final/"
    },
    {
        "code": "EF-T4",
        "title": "[EF-T4] Tomo IV: Expediente HAZOP, Matriz Ambiental y Evaluación Financiera",
        "assignee": "Cho0bb",
        "cargo": "Especialista en Seguridad HSE / Evaluación Económica",
        "participantes": "@Cho0bb",
        "raci": "R: @Cho0bb | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-11",
        "end": "2026-11-14",
        "labels": "EF,DOC,HSE",
        "done": False,
        "evidencia": "03_Entregables_Finales/EF_Informe_Final/"
    },
    {
        "code": "EF-T5",
        "title": "[EF-T5] Tomo V: Optimización Tecnológica SOEC y Auditorías Python",
        "assignee": "karolcamachol29-sudo",
        "cargo": "Ingeniera de Optimización Python / Dirección",
        "participantes": "@Karoc",
        "raci": "R: @Karoc | A: @Karoc | C: Consorcio | I: BUAP",
        "start": "2026-11-12",
        "end": "2026-11-14",
        "labels": "EF,PY,DOC",
        "done": False,
        "evidencia": "03_Entregables_Finales/EF_Informe_Final/"
    }
]

def main():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    os.chdir(repo_dir)

    print("=== OBTENIENDO ISSUES EXISTENTES EN GITHUB ===")
    res = subprocess.run(["gh", "issue", "list", "--state", "all", "--limit", "200", "--json", "number,title,state,url"], capture_output=True, text=True, check=True)
    existing = json.loads(res.stdout)
    
    # Mapeo code_prefix -> issue
    issue_map = {}
    for it in existing:
        title = it["title"]
        m = re.match(r"\[([^\]]+)\]", title)
        if m:
            code = m.group(1).strip()
            issue_map[code] = it

    print(f"Encontrados {len(existing)} issues en GitHub.")

    # Asegurar labels
    for L in ["MP-00", "E2.2", "E3.1", "E4", "EF", "RT-01"]:
        subprocess.run(["gh", "label", "create", L, "--force"], capture_output=True)

    results = []
    
    for task in TASKS_DEF:
        code = task["code"]
        title = task["title"]
        body = f"""### 📋 Entregable / Actividad: {code}
**Responsable:** @{task['assignee']}
**Cargo Oficial:** {task['cargo']}
**Integrantes Participantes:** {task['participantes']}
**Roles RACI:** {task['raci']}
**Periodo de Ejecución:** {task['start']} al {task['end']}
**Evidencia / Archivo:** `{task['evidencia']}`
**Estado:** {'✅ Finalizado' if task['done'] else '⏳ En proceso'}"""

        if code in issue_map:
            it = issue_map[code]
            num = it["number"]
            url = it["url"]
            print(f"ℹ️ Ya existe [{code}] -> #{num} ({it['state']})")
        else:
            print(f"✨ Creando Issue [{code}]: {title}...")
            cmd = ["gh", "issue", "create", "--title", title, "--body", body, "--assignee", task["assignee"], "--label", task["labels"]]
            c_res = subprocess.run(cmd, capture_output=True, text=True)
            if c_res.returncode != 0:
                print(f"⚠️ Error creando con labels/assignee, reintentando básico: {c_res.stderr}")
                cmd = ["gh", "issue", "create", "--title", title, "--body", body]
                c_res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            url = c_res.stdout.strip()
            num = int(url.split("/")[-1])
            print(f"   -> Creado exitosamente: #{num} ({url})")
            
            if task["done"]:
                subprocess.run(["gh", "issue", "close", str(num), "--reason", "completed"], capture_output=True, check=True)
                print(f"   -> Cerrado como completed: #{num}")

        results.append({
            "number": num,
            "code": code,
            "title": title,
            "start": task["start"],
            "end": task["end"],
            "assignee": task["assignee"],
            "cargo": task["cargo"],
            "participantes": task["participantes"],
            "raci": task["raci"],
            "done": task["done"],
            "evidencia": task["evidencia"],
            "url": f"https://github.com/karolcamachol29-sudo/RFP-CCM-EM-001/issues/{num}"
        })

    # Guardar mapeo de issues para el workflow
    print("\n=== GENERANDO CONFIGURACIÓN PARA GITHUB ACTIONS PROJECT V2 SYNC ===")
    workflow_issues = [(r["number"], r["start"], r["end"]) for r in results]
    print(f"Total issues preparados para Projects V2: {len(workflow_issues)}")

    with open("/tmp/project_v2_issues.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("✅ Guardado /tmp/project_v2_issues.json")

if __name__ == "__main__":
    main()


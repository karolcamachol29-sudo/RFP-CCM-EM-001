#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_guia_maestra_10min.py
Genera la Guía Maestra de Defensa Técnica, Speech Sincronizado de 10 Minutos,
Banco de Preguntas Q&A (12 preguntas) y Desglose Matemático de Ecuaciones.
Produce la versión LaTeX (.tex) y compila a PDF (.pdf), además de sincronizar a Markdown (.md).
"""

import os
import subprocess
import shutil

TEX_PATH = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.tex"
MD_PATH = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.md"
PDF_DIR = "Entregables"
FINAL_PDF = "Entregables/Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf"
ROOT_PDF = "./Guia_Maestra_Defensa_Speech_Ingenieria_Solvanta.pdf"

print("Compilando generador de Guía Maestra...")

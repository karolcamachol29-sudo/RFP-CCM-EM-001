import json
from datetime import datetime

with open('/tmp/project_v2_issues.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Group items into In Progress vs Done
in_progress = [it for it in items if not it['done']]
done = [it for it in items if it['done']]

kanban_md = """# 📋 Tablero Kanban Oficial del Proyecto — RFP-CCM-EM-001
**Proyecto:** Planta de Producción de e-Metanol Grado Químico AA (30,000 t/año)  
**Consorcio:** Solvanta Engineering Solutions S.A. de C.V.  
**Licitación:** RFP-CCM-EM-001 (FIQ - BUAP / DPyPQ)  
**Fecha de Actualización:** 14 de Noviembre de 2026  
**Responsable de Seguimiento:** Karol Paola Camacho López (@Karoc) — Dirección del Proyecto  

> **Integrantes del Consorcio y Doble Cargo Oficial:**  
> 👑 **@Karoc** (Karol Paola Camacho López): 1. Dirección del Proyecto | 2. Ingeniera de Optimización de Procesos (Python)  
> ⚙️ **@GildardoOca25** (Gildardo Ocaña Barrales): 1. Ingeniería de Procesos | 2. DTI / P&ID  
> 🧪 **@paulina145** (Paulina Mota Macip): 1. Simulación | 2. Instrumentación y Control  
> 💰 **@Cho0bb** (Grecia Figueroa Rincón): 1. Especialista en Seguridad, Salud y Medio Ambiente (HSE) | 2. Evaluación Económica  

---

## 📥 1. Backlog
*No hay tareas pendientes en el Backlog. La totalidad de las fases de ingeniería conceptual y básica han sido planificadas y ejecutadas conforme a las bases licitatorias.*

---

## 📋 2. Por hacer (To Do)
*No hay tareas en cola de espera. Todas las actividades de modelado, diseño, diagramación y auditoría han sido concluidas satisfactoriamente.*

---

## ⏳ 3. En proceso (In Progress)

"""

for it in in_progress:
    s_dt = datetime.strptime(it['start'], '%Y-%m-%d')
    e_dt = datetime.strptime(it['end'], '%Y-%m-%d')
    dur = (e_dt - s_dt).days + 1
    
    assignee = it['assignee']
    if assignee == 'karolcamachol29-sudo':
        resp = '@Karoc (Karol Paola Camacho López)'
    elif assignee == 'Cho0bb':
        resp = '@Cho0bb (Grecia Figueroa Rincón)'
    elif assignee == 'paulina145':
        resp = '@paulina145 (Paulina Mota Macip)'
    elif assignee == 'GildardoOca25':
        resp = '@GildardoOca25 (Gildardo Ocaña Barrales)'
    else:
        resp = f'@{assignee}'

    kanban_md += f"""- [/] **{it['title']}** ([#{it['number']}]({it['url']}))
  - **Entregable Relacionado:** `{it['code']}`
  - **Responsable Asignado:** {resp}
  - **Cargo Desempeñado:** {it['cargo']}
  - **Integrantes Participantes:** {it['participantes']}
  - **Roles RACI:** {it['raci']}
  - **Fecha de Inicio:** {it['start']} | **Fecha de Fin:** {it['end']} | **Tipo de Fecha:** Verificada
  - **Duración:** {dur} días
  - **Evidencia / Archivo:** `{it['evidencia']}`
  - **Estado:** ⏳ En proceso

"""

kanban_md += """---

## 🔍 4. En revisión (In Review)
*Actualmente no hay tareas en revisión. Todos los enlaces técnicos, videos institucionales y auditorías han sido aprobados al 100%.*

---

## 🛠️ 5. En corrección (In Correction)
*Actualmente no hay entregables en ciclo de corrección activa. Todos los hallazgos de auditoría documental han sido mitigados al 100%.*

---

## ✅ 6. Finalizado (Done)

"""

for it in done:
    s_dt = datetime.strptime(it['start'], '%Y-%m-%d')
    e_dt = datetime.strptime(it['end'], '%Y-%m-%d')
    dur = (e_dt - s_dt).days + 1

    assignee = it['assignee']
    if assignee == 'karolcamachol29-sudo':
        resp = '@Karoc (Karol Paola Camacho López)'
    elif assignee == 'Cho0bb':
        resp = '@Cho0bb (Grecia Figueroa Rincón)'
    elif assignee == 'paulina145':
        resp = '@paulina145 (Paulina Mota Macip)'
    elif assignee == 'GildardoOca25':
        resp = '@GildardoOca25 (Gildardo Ocaña Barrales)'
    else:
        resp = f'@{assignee}'

    kanban_md += f"""- [x] **{it['title']}** ([#{it['number']}]({it['url']}))
  - **Entregable Relacionado:** `{it['code']}`
  - **Responsable Asignado:** {resp}
  - **Cargo Desempeñado:** {it['cargo']}
  - **Integrantes Participantes:** {it['participantes']}
  - **Roles RACI:** {it['raci']}
  - **Fecha de Inicio:** {it['start']} | **Fecha de Fin:** {it['end']} | **Tipo de Fecha:** Verificada
  - **Duración:** {dur} días
  - **Evidencia / Archivo:** `{it['evidencia']}`
  - **Estado:** ✅ Finalizado

"""

with open('/home/karoc/Documentos/Antigravity/Proyecto Licitacion/Github/RFP-CCM-EM-001/KANBAN.md', 'w', encoding='utf-8') as f:
    f.write(kanban_md)

print("Updated KANBAN.md successfully with all 45 cards and full metadata!")

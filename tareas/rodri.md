# Tareas - Persona 4: Especialista en Integración, Informe y Presentación (Project Manager)

## Rol Principal
Eres el ancla que une todas las piezas. Asegurarás que el código fluya sin errores en un único programa ejecutable (`main.py`). Eres responsable máximo de la "Organización y Coherencia" (5% de la rúbrica) del informe, conclusiones, originalidad algorítmica y consolidación de la presentación.

## 🚀 Cómo avanzar de forma SOLITARIA (Sin depender de los demás)
**Tu trabajo es altamente independiente y no estás bloqueado.**
1. **En Código:** Crea la estructura de `main.py` importando funciones vacías (firmas). Arma el menú de terminal.
2. **En Informe y PPT:** Tienes a cargo secciones independientes (Reflexiones, Anexos, Formato). Puedes empezar a investigar e ir estructurando el PDF general.

## Tareas de Código (`src/` y general)

> ⚠️ **Avance de Renato (Persona 3) — 14/06/2026:**
> Para integrar el pipeline completo durante sus pruebas de visualización, Renato implementó una **versión base/plantilla** de `main.py` con menú interactivo y modo demo (`--demo`). **Debes revisarlo, entenderlo y personalizarlo** para que puedas defenderlo como propio.
> - `src/main.py` — Menú interactivo con opciones: buscar, generar gráficos, ver vocabulario, ver matriz, exportar CSV. Incluye modo `--demo` con 5 consultas automáticas.

- [ ] **`src/main.py`**: *(plantilla base ya implementada — revisar y personalizar)*
  - [x] Programar el cascarón/menú de la aplicación usando *mock functions*. *(base lista — funcional con datos reales)*
  - [x] Integrar la cadena real: leer datos -> vectorizar -> buscador -> consultas -> resultados. *(base lista)*
  - [ ] **→ Revisar, entender y personalizar el código para poder defenderlo.**
- [ ] **Documentación y Originalidad Algorítmica (Evitar sospecha de IA)**:
  - [ ] Asegurarte que todas las funciones en todos los scripts tengan *docstrings* y comentarios.
  - [ ] **CRÍTICO:** La rúbrica anula proyectos por copia directa de IA. Para el "Anexo V: Código documentado", asegúrate de evidenciar trabajo humano original, documentando detalladamente **por qué se tomaron decisiones algorítmicas** en el código (ej. "usamos `numpy.dot` aquí porque optimiza el tiempo frente a un bucle for tradicional").
  - [ ] Redactar el archivo `README.md` explicando cómo ejecutar el código.

## Tareas del Informe (`informe/`)

- [ ] **Redactar Sección IV (Reflexión y conclusiones)**:
  - [ ] Investigar cómo los vectores han evolucionado en aplicaciones modernas reales (Motores de búsqueda, Modelos de Lenguaje / ChatGPT).
  - [ ] Sintetizar limitaciones del buscador semántico basado en TF.
- [ ] **Gestión, Organización y Coherencia (5% de la nota)**:
  - [ ] Establecer un "Freeze" o cierre interno de redacción al menos **3 días antes de la fecha límite (23 de junio de 2026 a las 11:59h)**.
  - [ ] Leer el documento completo y **reescribir transiciones** entre las partes de la Persona 1, Persona 2 (quien redacta el III.A.1) y Persona 3. Esto evitará que el texto se sienta fragmentado o "parchado", asegurando un tono de lectura fluido y uniforme.
  - [ ] Agregar la Sección V (Anexos), listando bibliotecas y la justificación de originalidad del código.

## Tareas de la Presentación

- [ ] **Consolidar la Presentación (PPT/Canva)**:
  - [ ] Crear la plantilla maestra y juntar las partes. Redactar Introducción y Conclusión.
  - [ ] Controlar tiempo: 15 a 20 minutos.

## Requisito de Conocimiento Global (Cross-Training y Bibliotecas)

- [ ] **Simulacros de Defensa:** Serás el encargado de testear al equipo. Organiza simulacros de preguntas aleatorias donde evalúes a tus compañeros.
- [ ] **Asegurar conocimiento de librerías:** En tus simulacros, incluye obligatoriamente preguntas sobre cómo operan las bibliotecas de Python usadas en el código (`numpy`, `sklearn`, `matplotlib`, `scipy`), ya que cualquiera podría ser interrogado sobre ellas por el profesor (15% de la nota final).

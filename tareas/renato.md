# Tareas - Persona 3: Especialista en Análisis Experimental y Visualización

## Rol Principal
Eres el/la investigador/a del grupo. Tu misión es probar empíricamente que el buscador funciona, estresarlo con diferentes consultas, recolectar los datos y presentarlos de forma visual e interpretativa (científica).

## 🚀 Cómo avanzar de forma SOLITARIA (Sin depender de los demás)
**No necesitas esperar a que el buscador esté listo para crear tus visualizaciones y redactar tu análisis.**
Para avanzar solo, **crea datos simulados (Mock Data)**:
1. Crea una matriz de similitud aleatoria para el mapa de calor: `matriz_similitud_mock = np.random.rand(10, 10)`. Con esto ya puedes dejar programado el `heatmap`.
2. Inventa resultados de búsquedas imaginarios ("para la query X salieron los documentos A, B, C"). Con esto ya puedes redactar gran parte del análisis y cómo el vocabulario impacta, basándote en la teoría, mientras esperas los datos reales.
3. Para el PCA/Scatter, genera puntos aleatorios `np.random.randn(20, 2)` y grafica.
Cuando los demás terminen, solo reemplazas tus `mocks` por los datos reales.

## Tareas de Código (`src/` y `notebooks/`)

- [x] **`src/visualizacion.py`**: ✅ *Completado el 14/06/2026*
  - [x] Implementar la función `plot_matriz_similitud(matriz_similitudes)` utilizando librerías como `matplotlib` y `seaborn` para generar un mapa de calor (heatmap) entre documentos.
  - [x] (Opcional pero muy recomendado) Implementar PCA simple (`sklearn.decomposition.PCA`) para reducir los vectores a 2D y crear un gráfico de dispersión (scatter plot) relacionando documentos y consultas en un plano cartesiano.
  - [x] *(Extra)* Implementar `plot_frecuencia_terminos()` — gráfico de barras con los términos más frecuentes del corpus.
  - [x] *(Extra)* Implementar `plot_resultados_busqueda()` — barras horizontales con similitudes por consulta.
- [x] **`notebooks/evaluacion.ipynb`**: ✅ *Completado el 14/06/2026*
  - [x] Preparar las celdas del Jupyter Notebook para cargar los módulos, ejecutar el pipeline completo y generar/guardar las gráficas en `graficos/`.
  - [x] Incluye análisis del impacto del tamaño del vocabulario (celda 10).

> **Nota:** Para poder avanzar con las visualizaciones usando datos reales en vez de mocks, se implementaron plantillas base de los módulos de Seba (`preprocesamiento.py`, `vectorizacion.py`), Dani (`similitud.py`, `buscador.py`) y Rodri (`main.py`). Ellos deben revisar, personalizar y apropiarse de ese código.

## Tareas del Informe (`informe/`)

> 📝 **Formato:** El informe se redactará en **LaTeX**, compilable en **Overleaf**.
- [ ] **Redactar Sección III (Análisis Experimental - Excluyendo III.A.1)**:
  - [ ] Redactar la estructura del análisis. (Nota: La apertura III.A.1 sobre álgebra lineal la redactará la Persona 2, tú encárgate del análisis empírico).
  - [ ] Analizar críticamente los resultados: describir documentos recuperados, evaluar las similitudes calculadas y debatir sobre la calidad de las recomendaciones.
  - [ ] Redactar un apartado analizando explícitamente **cómo afecta el tamaño del vocabulario** a la representación vectorial y al desempeño general del motor.
  - [ ] Explicar las ventajas y limitaciones de usar la similitud coseno (ej. no detecta sarcasmo, palabras con múltiples significados o contexto temporal).

## Tareas de la Presentación

- [ ] **Preparar diapositivas de Análisis y Resultados**:
  - [ ] Diseñar las diapositivas para exponer los gráficos generados (cómo se lee el heatmap de similitud o la reducción dimensional).
  - [ ] Hablar del impacto del tamaño del vocabulario empíricamente.

## Requisito de Conocimiento Global (Cross-Training y Bibliotecas)

- [ ] Explicar al equipo cómo interpretar correctamente cada gráfico generado para que cualquiera pueda exponer esa diapositiva en caso de que le pregunten aleatoriamente.
- [ ] Revisar que la integración del programa de Persona 4 (`main.py`) arroje los mismos resultados que tienes en tu Jupyter Notebook.
- [ ] **Defensa de Bibliotecas:** Debes dar una pequeña charla al resto del equipo explicando el uso de `matplotlib`, `seaborn` y especialmente **`sklearn.decomposition.PCA`**. Todo el equipo debe ser capaz de defender por qué se utilizó PCA y cómo funcionan estas herramientas científicas (15% de la nota final).

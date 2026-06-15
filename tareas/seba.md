# Tareas - Persona 1: Especialista en Preprocesamiento y Vectorización

## Rol Principal
Eres responsable de tomar los textos en su estado bruto (raw), limpiarlos y transformarlos al mundo matemático mediante una Matriz Documento-Término. Tu trabajo es el puente entre el texto humano y el álgebra lineal.

## 🚀 Cómo avanzar de forma SOLITARIA (Sin depender de los demás)
**Tu trabajo es la base de los datos, por lo que puedes avanzar desde el minuto cero sin depender de nadie.** Solo debes asegurarte de que tu función final entregue una matriz (ej. `numpy array`) y el vocabulario. Tus compañeros asumirán que entregarás esto y crearán datos falsos (mocks) mientras tanto.

## Tareas de Código (`src/`)

> ⚠️ **Avance de Renato (Persona 3) — 14/06/2026:**
> Para poder probar sus visualizaciones con datos reales, Renato implementó una **versión base/plantilla** de tus dos módulos. El código ya está funcional y probado, pero **debes revisarlo, entenderlo y personalizarlo** (ajustar comentarios, estilo, quizás cambiar implementaciones) para que puedas defenderlo como propio en la presentación. Los archivos afectados son:
> - `src/preprocesamiento.py` — Funciones `cargar_documentos()`, `limpiar_texto()`, `tokenizar()`, `remover_stopwords()` y `preprocesar_corpus()`.
> - `src/vectorizacion.py` — Funciones `construir_vocabulario()`, `crear_matriz_documento_termino()` y `obtener_vocabulario_inverso()`.
> - `data/documentos/corpus.txt` — Corpus de 12 documentos sobre tecnología/computación.

- [ ] **`src/preprocesamiento.py`**: *(plantilla base ya implementada — revisar y personalizar)*
  - [x] Implementar función para cargar textos desde la carpeta `data/`. *(base lista)*
  - [x] Implementar función `limpiar_texto(texto: str)` que pase todo a minúsculas, elimine signos de puntuación y caracteres especiales. *(base lista)*
  - [x] Implementar tokenización básica (separar oraciones en palabras) y, si es posible, remoción de *stopwords* (palabras comunes sin significado como "el", "la", "de"). *(base lista)*
  - [ ] **→ Revisar, entender y personalizar el código para poder defenderlo.**
- [ ] **`src/vectorizacion.py`**: *(plantilla base ya implementada — revisar y personalizar)*
  - [x] Implementar función `construir_vocabulario(corpus: list)` que extraiga todas las palabras únicas de todos los documentos y les asigne un índice. *(base lista)*
  - [x] Implementar la función `crear_matriz_documento_termino(corpus: list, vocabulario: dict)` que genere una representación matemática (vectores) donde las filas son documentos, las columnas son términos del vocabulario y los valores son las frecuencias (o conteo) de aparición. *(base lista)*
  - [x] Retornar la matriz en un formato apto para operaciones matemáticas (ej. `numpy.array` o matrices esparsas de `scipy`). *(base lista)*
  - [ ] **→ Revisar, entender y personalizar el código para poder defenderlo.**

## Tareas del Informe (`informe/`)

- [ ] **Redactar Sección I (Marco Teórico) - Espacios Vectoriales de Texto**:
  - [ ] Explicar cómo se representan palabras/documentos usando vectores.
  - [ ] Detallar qué es el espacio vectorial en este contexto, su representación numérica, interpretación geométrica y la dimensión del espacio (qué la determina).
- [ ] **Redactar Sección II (Representación de Documentos)**:
  - [ ] Explicar teóricamente cómo se construye la matriz documento-término.
  - [ ] Hablar sobre la frecuencia de palabras, filas/columnas y un aspecto clave: la **sparsidad** (matriz rala) de los datos en texto.
  - [ ] Presentar en el informe el conjunto de documentos breves que seleccionaste, mostrar el vocabulario generado, la matriz resultante y sus dimensiones.

## Tareas de la Presentación

- [ ] **Preparar diapositivas sobre la representación de datos**:
  - [ ] Explicar la transformación de texto a números (vocabulario).
  - [ ] Mostrar visualmente una matriz de ejemplo para que la audiencia entienda el concepto de filas y columnas.

## Requisito de Conocimiento Global (Cross-Training y Bibliotecas)

- [ ] Explicar el concepto de "sparsidad" y la "matriz documento-término" a tus 3 compañeros, asegurando que si les preguntan en la defensa, sepan responder.
- [ ] Revisar y entender la matemática detrás de `src/similitud.py` que realizará la Persona 2.
- [ ] **Defensa de Bibliotecas:** Entender el funcionamiento básico de las bibliotecas científicas usadas por tus compañeros (ej. cómo funciona `numpy` para similitud, o por qué la Persona 3 usó `sklearn` para PCA). Cualquiera en el grupo puede ser evaluado por esto (15% de la nota final de presentación).

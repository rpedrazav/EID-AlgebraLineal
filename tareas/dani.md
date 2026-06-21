# Tareas - Persona 2: Especialista en Álgebra Lineal y Motor de Búsqueda

## Rol Principal
Eres el núcleo matemático del proyecto. Implementarás las operaciones de álgebra lineal necesarias para comparar vectores numéricamente e identificar cuáles documentos son los más relevantes según una consulta (query).

## 🚀 Cómo avanzar de forma SOLITARIA (Sin depender de los demás)
**No necesitas esperar a que la Persona 1 termine el preprocesamiento.**
Para avanzar solo, **crea datos simulados (Mock Data)** en tu código:
1. Inventa una matriz documento-término falsa usando numpy: `matriz_mock = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 0]])`.
2. Inventa un vector de consulta falso: `query_mock = np.array([1, 0, 0])`.
Con estos datos de prueba, puedes programar todo tu código (`similitud.py` y `buscador.py`). Cuando la Persona 1 termine, simplemente reemplazarás tus variables `mock` por las reales.

## Tareas de Código (`src/`)

> ⚠️ **Avance de Renato (Persona 3) — 14/06/2026:**
> Para poder probar sus visualizaciones con datos reales, Renato implementó una **versión base/plantilla** de tus dos módulos. El código ya está funcional y probado, pero **debes revisarlo, entenderlo y personalizarlo** (ajustar comentarios, estilo, quizás cambiar implementaciones) para que puedas defenderlo como propio en la presentación. Los archivos afectados son:
> - `src/similitud.py` — Funciones `calcular_producto_punto()`, `calcular_norma()` y `similitud_coseno()`.
> - `src/buscador.py` — Clase `BuscadorSemantico` con métodos `vectorizar_consulta()`, `buscar()` y `calcular_matriz_similitud()`.

- [ ] **`src/similitud.py`**: *(plantilla base ya implementada — revisar y personalizar)*
  - [x] Implementar la función `calcular_producto_punto(u, v)` desde cero o usando `numpy.dot`. *(base lista)*
  - [x] Implementar la función `calcular_norma(vector)` (magnitud del vector). *(base lista)*
  - [x] Implementar la función principal `similitud_coseno(u, v)` aplicando estrictamente la fórmula: $cos(\theta) = \frac{u \cdot v}{||u|| ||v||}$. *(base lista)*
  - [ ] **→ Revisar, entender y personalizar el código para poder defenderlo.**
- [ ] **`src/buscador.py`**: *(plantilla base ya implementada — revisar y personalizar)*
  - [x] Implementar la clase o funciones del buscador (`BuscadorSemantico`). *(base lista)*
  - [x] Crear la lógica para calcular la similitud coseno de una consulta (vector) contra **cada fila** de una matriz (matriz de documentos). *(base lista)*
  - [x] Retornar los índices de los documentos ordenados (ranking) de mayor a menor similitud. *(base lista)*
  - [ ] **→ Revisar, entender y personalizar el código para poder defenderlo.**

## Tareas del Informe (`informe/`)

- [x] **Redactar Sección I (Marco Teórico) - Similitud Coseno**:
  - [x] Explicar qué es la similitud coseno y cómo se usa para comparar textos.
  - [x] Explicar su interpretación geométrica (el ángulo entre dos vectores independientemente de su magnitud).
- [x] **Desarrollar el Ejemplo Matemático Simple (Obligatorio en Sección I)**:
  - [x] Inventar dos textos (o frases cortas) representados como vectores.
  - [x] Mostrar paso a paso el cálculo manual: representación vectorial, cálculo de producto punto, cálculo de normas, resultado final de la similitud coseno y su interpretación.
- [x] **Redactar apertura de la Sección III (Implementación Computacional - Punto III.A.1)**:
  - [x] **Importante:** Escribir la subsección introductoria de la Sección III explicando *específicamente cómo el álgebra lineal permite comparar documentos mediante operaciones vectoriales para la recuperación de información*. Esta sección une tu conocimiento matemático con el código.

## Tareas de la Presentación

- [ ] **Preparar diapositivas sobre Álgebra Lineal**:
  - [ ] Mostrar la fórmula de similitud coseno y una gráfica visual de dos flechas (vectores) en 2D o 3D con un ángulo $\theta$.
  - [ ] Exponer el ejemplo matemático simple manual de manera muy didáctica para que el profesor vea el dominio matemático.

## Requisito de Conocimiento Global (Cross-Training y Bibliotecas)

- [ ] Realizar una mini-clase de 15 minutos para tus compañeros de grupo enseñándoles cómo funciona el producto punto y la norma, para que todos dominen el fundamento matemático.
- [ ] Revisar el trabajo de evaluación experimental de la Persona 3 para asegurar que los cálculos de similitud se estén usando correctamente en las gráficas.
- [ ] **Defensa de Bibliotecas:** Comprender y saber explicar por qué tus compañeros utilizaron ciertas funciones de Python (ej. `scipy` para matrices ralas o `matplotlib` para visualización). Prepárate para preguntas aleatorias sobre cualquier parte técnica (15% de la nota final de presentación).

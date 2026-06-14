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

- [ ] **`src/similitud.py`**:
  - [ ] Implementar la función `calcular_producto_punto(u, v)` desde cero o usando `numpy.dot`.
  - [ ] Implementar la función `calcular_norma(vector)` (magnitud del vector).
  - [ ] Implementar la función principal `similitud_coseno(u, v)` aplicando estrictamente la fórmula: $cos(\theta) = \frac{u \cdot v}{||u|| ||v||}$.
- [ ] **`src/buscador.py`**:
  - [ ] Implementar la clase o funciones del buscador (`BuscadorSemantico`).
  - [ ] Crear la lógica para calcular la similitud coseno de una consulta (vector) contra **cada fila** de una matriz (matriz de documentos).
  - [ ] Retornar los índices de los documentos ordenados (ranking) de mayor a menor similitud.

## Tareas del Informe (`informe/`)

- [ ] **Redactar Sección I (Marco Teórico) - Similitud Coseno**:
  - [ ] Explicar qué es la similitud coseno y cómo se usa para comparar textos.
  - [ ] Explicar su interpretación geométrica (el ángulo entre dos vectores independientemente de su magnitud).
- [ ] **Desarrollar el Ejemplo Matemático Simple (Obligatorio en Sección I)**:
  - [ ] Inventar dos textos (o frases cortas) representados como vectores.
  - [ ] Mostrar paso a paso el cálculo manual: representación vectorial, cálculo de producto punto, cálculo de normas, resultado final de la similitud coseno y su interpretación.
- [ ] **Redactar apertura de la Sección III (Implementación Computacional - Punto III.A.1)**:
  - [ ] **Importante:** Escribir la subsección introductoria de la Sección III explicando *específicamente cómo el álgebra lineal permite comparar documentos mediante operaciones vectoriales para la recuperación de información*. Esta sección une tu conocimiento matemático con el código.

## Tareas de la Presentación

- [ ] **Preparar diapositivas sobre Álgebra Lineal**:
  - [ ] Mostrar la fórmula de similitud coseno y una gráfica visual de dos flechas (vectores) en 2D o 3D con un ángulo $\theta$.
  - [ ] Exponer el ejemplo matemático simple manual de manera muy didáctica para que el profesor vea el dominio matemático.

## Requisito de Conocimiento Global (Cross-Training y Bibliotecas)

- [ ] Realizar una mini-clase de 15 minutos para tus compañeros de grupo enseñándoles cómo funciona el producto punto y la norma, para que todos dominen el fundamento matemático.
- [ ] Revisar el trabajo de evaluación experimental de la Persona 3 para asegurar que los cálculos de similitud se estén usando correctamente en las gráficas.
- [ ] **Defensa de Bibliotecas:** Comprender y saber explicar por qué tus compañeros utilizaron ciertas funciones de Python (ej. `scipy` para matrices ralas o `matplotlib` para visualización). Prepárate para preguntas aleatorias sobre cualquier parte técnica (15% de la nota final de presentación).

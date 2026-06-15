"""
Módulo de Vectorización de Texto
=================================
Responsable: Persona 1 (Seba)

Este módulo transforma los documentos preprocesados (listas de tokens)
en representaciones numéricas mediante una Matriz Documento-Término.

Conceptos clave de Álgebra Lineal aplicados:
- Cada documento se convierte en un vector en R^n, donde n = |vocabulario|.
- La Matriz Documento-Término tiene dimensiones m x n (m documentos, n términos).
- Cada entrada (i, j) representa la frecuencia del término j en el documento i.
- Esta matriz suele ser "esparsa" (sparse): la mayoría de sus entradas son 0,
  porque cada documento usa solo un subconjunto pequeño del vocabulario total.

Decisiones de diseño:
- Se usa numpy.array como estructura de datos principal porque permite
  operaciones vectoriales eficientes (producto punto, norma) sin bucles
  explícitos, aprovechando las rutinas optimizadas en C de NumPy.
- El vocabulario se almacena como un diccionario {palabra: índice} para
  búsquedas O(1), y también se genera la lista inversa {índice: palabra}
  para facilitar la interpretación de resultados.
"""

import numpy as np


def construir_vocabulario(corpus_procesado):
    """
    Construye un vocabulario a partir de un corpus ya tokenizado.

    El vocabulario es un mapeo de cada palabra única a un índice numérico.
    Este índice determina la columna correspondiente en la Matriz
    Documento-Término, es decir, define las dimensiones del espacio
    vectorial en el que vivirán los documentos.

    Se ordena alfabéticamente para garantizar reproducibilidad: sin importar
    el orden de los documentos, el vocabulario siempre será el mismo.

    Parámetros
    ----------
    corpus_procesado : list[list[str]]
        Lista de documentos, donde cada documento es una lista de tokens
        (salida de preprocesar_corpus).

    Retorna
    -------
    dict[str, int]
        Diccionario {palabra: índice} ordenado alfabéticamente.

    Ejemplo
    -------
    >>> vocab = construir_vocabulario([["hola", "mundo"], ["mundo", "feliz"]])
    >>> print(vocab)
    {'feliz': 0, 'hola': 1, 'mundo': 2}
    """
    # Recolectar todas las palabras únicas usando un set (O(1) por inserción)
    palabras_unicas = set()
    for documento in corpus_procesado:
        for palabra in documento:
            palabras_unicas.add(palabra)

    # Ordenar alfabéticamente y asignar índices secuenciales
    vocabulario = {
        palabra: indice
        for indice, palabra in enumerate(sorted(palabras_unicas))
    }

    return vocabulario


def crear_matriz_documento_termino(corpus_procesado, vocabulario):
    """
    Genera la Matriz Documento-Término a partir de un corpus tokenizado.

    Esta es la piedra angular del buscador semántico. Cada fila de la
    matriz es un vector que representa a un documento en el espacio
    vectorial definido por el vocabulario. Los valores corresponden a la
    frecuencia de aparición de cada término (modelo Bag-of-Words / TF).

    Matemáticamente:
        M ∈ R^(m x n), donde m = |documentos|, n = |vocabulario|
        M[i][j] = frecuencia del término j en el documento i

    Se inicializa con np.zeros() para crear una matriz densa de ceros.
    Para corpus pequeños (<1000 docs) esto es eficiente; para corpus
    muy grandes se recomendaría scipy.sparse.

    Parámetros
    ----------
    corpus_procesado : list[list[str]]
        Lista de documentos tokenizados.
    vocabulario : dict[str, int]
        Diccionario {palabra: índice} generado por construir_vocabulario().

    Retorna
    -------
    numpy.ndarray
        Matriz de forma (num_documentos, tam_vocabulario) con las
        frecuencias de cada término por documento.

    Ejemplo
    -------
    >>> corpus = [["hola", "mundo", "hola"], ["mundo", "feliz"]]
    >>> vocab = {"feliz": 0, "hola": 1, "mundo": 2}
    >>> M = crear_matriz_documento_termino(corpus, vocab)
    >>> print(M)
    [[0. 2. 1.]
     [1. 0. 1.]]
    """
    num_documentos = len(corpus_procesado)
    tam_vocabulario = len(vocabulario)

    # Inicializar matriz de ceros con tipo float64 para compatibilidad
    # con las operaciones de álgebra lineal posteriores (producto punto, norma)
    matriz = np.zeros((num_documentos, tam_vocabulario), dtype=np.float64)

    # Llenar la matriz contando frecuencias de cada término
    for i, documento in enumerate(corpus_procesado):
        for palabra in documento:
            if palabra in vocabulario:
                j = vocabulario[palabra]
                matriz[i][j] += 1.0

    return matriz


def obtener_vocabulario_inverso(vocabulario):
    """
    Genera un mapeo inverso de índices a palabras.

    Útil para interpretar los resultados: dado un índice de columna
    de la Matriz Documento-Término, poder saber qué palabra representa.

    Parámetros
    ----------
    vocabulario : dict[str, int]
        Diccionario {palabra: índice}.

    Retorna
    -------
    dict[int, str]
        Diccionario {índice: palabra}.
    """
    return {indice: palabra for palabra, indice in vocabulario.items()}

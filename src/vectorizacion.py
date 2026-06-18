"""
Módulo de Vectorización de Texto
=================================
Autor: Sebastián (Persona 1)

En esta etapa, tomamos los textos ya preprocesados y los convertimos a números.
Esto es clave en Álgebra Lineal: pasamos de palabras a un espacio vectorial
donde cada documento es un vector y el vocabulario nos da las dimensiones.

Decisiones:
- Utilizo diccionarios para el vocabulario por su velocidad de búsqueda (O(1)).
- La Matriz Documento-Término la construyo con numpy.array para poder
  aprovechar luego las operaciones algebraicas nativas, ya que es mucho más
  rápido y eficiente en Python.
"""

import numpy as np

def construir_vocabulario(corpus_procesado):
    """
    Genera un diccionario que mapea cada palabra única a un índice numérico.
    Este índice definirá qué columna de nuestra matriz le corresponde
    a dicha palabra. Se ordena alfabéticamente para mantener consistencia.
    """
    terminos_unicos = set()
    
    # Recorrer todos los documentos y guardar palabras sin repetir
    for doc in corpus_procesado:
        for termino in doc:
            terminos_unicos.add(termino)
            
    # Mapear término -> índice
    vocabulario_ordenado = {
        termino: idx 
        for idx, termino in enumerate(sorted(terminos_unicos))
    }
    
    return vocabulario_ordenado

def crear_matriz_documento_termino(corpus_procesado, vocabulario):
    """
    Crea la Matriz Documento-Término.
    Cada fila es un documento, cada columna una palabra del vocabulario.
    El valor en (i, j) es cuántas veces aparece la palabra j en el doc i.
    """
    filas = len(corpus_procesado)
    columnas = len(vocabulario)
    
    # Arrancamos con una matriz llena de ceros (tipo float64 para hacer álgebra)
    matriz_dt = np.zeros((filas, columnas), dtype=np.float64)
    
    # Conteo de frecuencias (TF - Term Frequency)
    for i, doc in enumerate(corpus_procesado):
        for termino in doc:
            if termino in vocabulario:
                j = vocabulario[termino]
                matriz_dt[i][j] += 1.0
                
    return matriz_dt

def obtener_vocabulario_inverso(vocabulario):
    """
    Devuelve un diccionario invertido (índice -> palabra).
    Sirve para poder leer la matriz luego y saber qué significa cada columna.
    """
    vocabulario_inv = {idx: palabra for palabra, idx in vocabulario.items()}
    return vocabulario_inv
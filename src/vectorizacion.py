"""
Módulo de Vectorización de Texto
=================================
"""

import numpy as np

def construir_vocabulario(corpus_procesado):
    """Genera un diccionario que mapea cada palabra única a un índice numérico."""
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
    """Crea la Matriz Documento-Término."""
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
    """Devuelve un diccionario invertido (índice -> palabra)."""
    vocabulario_inv = {idx: palabra for palabra, idx in vocabulario.items()}
    return vocabulario_inv
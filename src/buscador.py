"""
Módulo del Buscador Semántico
==============================
"""

import numpy as np
from src.similitud import similitud_coseno
from src.preprocesamiento import preprocesar_documento


class BuscadorSemantico:
    """Motor de búsqueda semántica basado en similitud coseno."""

    def __init__(self, matriz_doc_termino, vocabulario,
                 documentos_originales=None, etiquetas=None):
        """Inicializa el buscador con la matriz y el vocabulario."""
        self.matriz_doc_termino = matriz_doc_termino
        self.vocabulario = vocabulario
        self.documentos_originales = documentos_originales or []
        num_docs = len(matriz_doc_termino)
        self.etiquetas = etiquetas or [
            f"Doc {i+1}" for i in range(num_docs)
        ]

    def vectorizar_consulta(self, consulta):
        """Convierte una consulta de texto en un vector numérico."""
        tokens = preprocesar_documento(consulta)
        vector = np.zeros(len(self.vocabulario), dtype=np.float64)

        for token in tokens:
            if token in self.vocabulario:
                indice = self.vocabulario[token]
                vector[indice] += 1.0

        return vector

    def buscar(self, consulta, top_n=5):
        """Busca los documentos más similares a una consulta y los retorna en orden."""
        vector_consulta = self.vectorizar_consulta(consulta)

        # Calcular similitud contra cada documento
        similitudes = np.array([
            similitud_coseno(vector_consulta, self.matriz_doc_termino[i])
            for i in range(len(self.matriz_doc_termino))
        ])

        # Ordenar índices de mayor a menor similitud
        indices_ordenados = np.argsort(similitudes)[::-1]

        resultados = []
        for idx in indices_ordenados[:top_n]:
            resultado = {
                "indice": int(idx),
                "etiqueta": self.etiquetas[idx],
                "similitud": float(similitudes[idx]),
            }
            if self.documentos_originales:
                texto = self.documentos_originales[idx]
                resultado["documento"] = texto[:150] + "..." \
                    if len(texto) > 150 else texto
            resultados.append(resultado)

        return resultados

    def calcular_matriz_similitud(self):
        """Genera la matriz de similitud coseno simétrica entre todos los documentos."""
        n = len(self.matriz_doc_termino)
        matriz_sim = np.zeros((n, n), dtype=np.float64)

        for i in range(n):
            for j in range(i, n):
                sim = similitud_coseno(
                    self.matriz_doc_termino[i],
                    self.matriz_doc_termino[j]
                )
                matriz_sim[i][j] = sim
                matriz_sim[j][i] = sim  # Simétrica

        return matriz_sim

"""
Módulo del Buscador Semántico
==============================
Responsable: Persona 2 (Dani)

Implementa la clase BuscadorSemantico que integra la vectorización
y la similitud coseno para buscar documentos relevantes.

Decisiones de diseño:
- Se vectoriza la consulta usando el mismo vocabulario que los documentos
  para garantizar que ambos vivan en el mismo espacio vectorial R^n.
- El ranking se obtiene con np.argsort() que es O(n log n), eficiente
  para nuestro tamaño de corpus.
"""

import numpy as np
from src.similitud import similitud_coseno
from src.preprocesamiento import preprocesar_documento


class BuscadorSemantico:
    """
    Motor de búsqueda semántica basado en similitud coseno.

    Atributos
    ---------
    matriz_doc_termino : numpy.ndarray
        Matriz (m x n) donde m=documentos, n=vocabulario.
    vocabulario : dict
        Mapeo {palabra: índice}.
    documentos_originales : list[str]
        Textos originales para mostrar en resultados.
    etiquetas : list[str]
        Nombres cortos de cada documento.
    """

    def __init__(self, matriz_doc_termino, vocabulario,
                 documentos_originales=None, etiquetas=None):
        """
        Inicializa el buscador con la matriz y el vocabulario.

        Parámetros
        ----------
        matriz_doc_termino : numpy.ndarray
            Matriz documento-término (filas=docs, cols=términos).
        vocabulario : dict
            Diccionario {palabra: índice_columna}.
        documentos_originales : list[str], opcional
            Textos originales de los documentos.
        etiquetas : list[str], opcional
            Nombres/etiquetas para identificar cada documento.
        """
        self.matriz_doc_termino = matriz_doc_termino
        self.vocabulario = vocabulario
        self.documentos_originales = documentos_originales or []
        num_docs = len(matriz_doc_termino)
        self.etiquetas = etiquetas or [
            f"Doc {i+1}" for i in range(num_docs)
        ]

    def vectorizar_consulta(self, consulta):
        """
        Convierte una consulta de texto en un vector numérico.

        La consulta pasa por el mismo pipeline de preprocesamiento
        que los documentos, y se mapea al mismo espacio vectorial
        usando el vocabulario existente.

        Parámetros
        ----------
        consulta : str
            Texto de la consulta del usuario.

        Retorna
        -------
        numpy.ndarray
            Vector de frecuencias de la consulta (1D, tamaño=|vocab|).
        """
        tokens = preprocesar_documento(consulta)
        vector = np.zeros(len(self.vocabulario), dtype=np.float64)

        for token in tokens:
            if token in self.vocabulario:
                indice = self.vocabulario[token]
                vector[indice] += 1.0

        return vector

    def buscar(self, consulta, top_n=5):
        """
        Busca los documentos más similares a una consulta.

        Proceso:
        1. Vectoriza la consulta al espacio del vocabulario.
        2. Calcula similitud coseno contra cada fila de la matriz.
        3. Ordena de mayor a menor similitud.
        4. Retorna los top_n resultados.

        Parámetros
        ----------
        consulta : str
            Texto de la consulta.
        top_n : int
            Cantidad máxima de resultados a retornar.

        Retorna
        -------
        list[dict]
            Lista de diccionarios con claves:
            - 'indice': posición del documento
            - 'etiqueta': nombre del documento
            - 'similitud': valor de similitud coseno
            - 'documento': texto original (si disponible)
        """
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
        """
        Genera la matriz de similitud coseno entre todos los documentos.

        La matriz resultante es simétrica: M[i][j] = M[j][i] = cos(θ)
        entre el documento i y el documento j. La diagonal es siempre
        1.0 (cada documento es idéntico a sí mismo).

        Retorna
        -------
        numpy.ndarray
            Matriz simétrica (m x m) de similitudes coseno.
        """
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

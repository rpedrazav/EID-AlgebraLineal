import numpy as np
from src.similitud import similitud_coseno, _EPSILON_NORMA
from src.preprocesamiento import preprocesar_documento


class BuscadorSemantico:
    """Motor de búsqueda basado en similitud coseno."""

    def __init__(self, matriz_doc_termino, vocabulario,
                 documentos_originales=None, etiquetas=None):
        self.matriz_dt = np.asarray(matriz_doc_termino, dtype=np.float64)
        self.vocabulario = vocabulario
        self.docs_originales = documentos_originales or []
        self.num_documentos = self.matriz_dt.shape[0]
        self.dim_vocabulario = self.matriz_dt.shape[1]
        self.etiquetas = etiquetas or [
            f"Doc {i + 1}" for i in range(self.num_documentos)
        ]
        # Normas pre-calculadas (no cambian después de init)
        self._normas_documentos = np.linalg.norm(self.matriz_dt, axis=1)

    @property
    def matriz_doc_termino(self):
        return self.matriz_dt

    def vectorizar_consulta(self, consulta_texto):
        """Convierte texto de consulta en un vector de frecuencias."""
        tokens = preprocesar_documento(consulta_texto)
        vector_q = np.zeros(self.dim_vocabulario, dtype=np.float64)

        for token in tokens:
            if token in self.vocabulario:
                idx = self.vocabulario[token]
                vector_q[idx] += 1.0

        return vector_q

    def buscar(self, consulta, top_n=5):
        """Retorna los top_n documentos más similares a la consulta."""
        vector_q = self.vectorizar_consulta(consulta)

        norma_q = np.linalg.norm(vector_q)
        if norma_q < _EPSILON_NORMA:
            return []

        # Producto punto vectorizado: M @ q
        productos_punto = self.matriz_dt @ vector_q

        # Similitud coseno = dot(d_i, q) / (||d_i|| * ||q||)
        denominadores = self._normas_documentos * norma_q
        denominadores_seguros = np.where(
            denominadores < _EPSILON_NORMA, 1.0, denominadores
        )
        similitudes = productos_punto / denominadores_seguros
        similitudes[self._normas_documentos < _EPSILON_NORMA] = 0.0

        # Ranking de mayor a menor
        indices_ranking = np.argsort(similitudes)[::-1]

        resultados = []
        for posicion in indices_ranking[:top_n]:
            entrada = {
                "indice": int(posicion),
                "etiqueta": self.etiquetas[posicion],
                "similitud": float(similitudes[posicion]),
            }
            if self.docs_originales:
                texto = self.docs_originales[posicion]
                entrada["documento"] = (
                    texto[:150] + "..." if len(texto) > 150 else texto
                )
            resultados.append(entrada)

        return resultados

    def calcular_matriz_similitud(self):
        """Genera la matriz simétrica de similitud coseno entre todos los documentos."""
        normas = self._normas_documentos.copy()
        normas_seguras = np.where(normas < _EPSILON_NORMA, 1.0, normas)

        # Normalizar filas y multiplicar: M̂ @ M̂ᵀ = matriz de similitudes
        matriz_normalizada = self.matriz_dt / normas_seguras.reshape(-1, 1)
        matriz_sim = matriz_normalizada @ matriz_normalizada.T

        # Docs vacíos → similitud 0
        docs_vacios = normas < _EPSILON_NORMA
        matriz_sim[docs_vacios, :] = 0.0
        matriz_sim[:, docs_vacios] = 0.0

        return matriz_sim

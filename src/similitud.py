"""
Módulo de Similitud y Operaciones de Álgebra Lineal
====================================================
"""

import numpy as np


def calcular_producto_punto(u, v):
    """Calcula el producto punto entre dos vectores."""
    return np.dot(u, v)


def calcular_norma(vector):
    """Calcula la norma euclidiana de un vector."""
    return np.linalg.norm(vector)


def similitud_coseno(u, v):
    """Calcula la similitud coseno entre dos vectores."""
    producto = calcular_producto_punto(u, v)
    norma_u = calcular_norma(u)
    norma_v = calcular_norma(v)

    if norma_u == 0 or norma_v == 0:
        return 0.0

    return producto / (norma_u * norma_v)

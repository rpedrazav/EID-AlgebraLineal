"""
Módulo de Similitud y Operaciones de Álgebra Lineal
====================================================
Responsable: Persona 2 (Dani)

Implementa las operaciones de álgebra lineal para comparar vectores
de documentos: producto punto, norma euclidiana y similitud coseno.

Decisiones de diseño:
- numpy.dot() en vez de bucle for: ~100x más rápido en arrays grandes.
- Protección contra vectores nulos (norma=0) para evitar divisiones por cero.
"""

import numpy as np


def calcular_producto_punto(u, v):
    """
    Calcula el producto punto entre dos vectores.
    Fórmula: u · v = Σᵢ uᵢvᵢ

    Parámetros
    ----------
    u, v : numpy.ndarray  — Vectores 1D de igual dimensión.

    Retorna
    -------
    float — Valor escalar del producto punto.
    """
    return np.dot(u, v)


def calcular_norma(vector):
    """
    Calcula la norma euclidiana (L2) de un vector.
    Fórmula: ||v|| = √(Σᵢ vᵢ²)

    Parámetros
    ----------
    vector : numpy.ndarray — Vector 1D.

    Retorna
    -------
    float — Norma euclidiana (>= 0).
    """
    return np.linalg.norm(vector)


def similitud_coseno(u, v):
    """
    Calcula la similitud coseno entre dos vectores.

    Fórmula: cos(θ) = (u · v) / (||u|| × ||v||)

    Interpretación:
    - 1.0  → documentos muy similares (misma dirección)
    - 0.0  → sin relación (perpendiculares)

    Es independiente de la magnitud: docs largos y cortos sobre
    el mismo tema tendrán alta similitud.

    Parámetros
    ----------
    u, v : numpy.ndarray — Vectores 1D de igual dimensión.

    Retorna
    -------
    float — Similitud en rango [0, 1] para vectores no negativos.
    """
    producto = calcular_producto_punto(u, v)
    norma_u = calcular_norma(u)
    norma_v = calcular_norma(v)

    if norma_u == 0 or norma_v == 0:
        return 0.0

    return producto / (norma_u * norma_v)

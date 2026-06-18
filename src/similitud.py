import numpy as np

# Tolerancia numérica para evitar dividir entre cero
_EPSILON_NORMA = 1e-12


def producto_punto(u, v):
    """Retorna u · v = Σ(u_i * v_i)."""
    return np.dot(u, v)


def norma_euclidiana(vector):
    """Retorna ||v|| = √(Σ v_i²)."""
    return np.linalg.norm(vector)


def similitud_coseno(u, v):
    """Calcula cos(θ) = (u · v) / (||u|| · ||v||). Retorna 0.0 si algún vector es cero."""
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)

    if u.shape != v.shape:
        raise ValueError(
            f"Dimensiones incompatibles: u ∈ R^{u.shape}, v ∈ R^{v.shape}"
        )

    norma_u = norma_euclidiana(u)
    norma_v = norma_euclidiana(v)

    if norma_u < _EPSILON_NORMA or norma_v < _EPSILON_NORMA:
        return 0.0

    return producto_punto(u, v) / (norma_u * norma_v)

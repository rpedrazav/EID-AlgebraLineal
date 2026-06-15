"""
Módulo de Visualización y Análisis Experimental
=================================================
Responsable: Persona 3 (Renato)

Este módulo genera las representaciones gráficas del buscador semántico:
- Heatmap de similitud coseno entre documentos (matplotlib + seaborn)
- Reducción dimensional con PCA (sklearn.decomposition.PCA) + scatter plot
- Gráfico de frecuencia de términos (barras)
- Gráfico de resultados de búsqueda (barras horizontales)

Bibliotecas utilizadas y justificación:
- matplotlib: biblioteca estándar de visualización en Python. Se eligió
  por su control total sobre cada aspecto del gráfico (ejes, colores,
  anotaciones) y su amplia documentación.
- seaborn: capa sobre matplotlib que simplifica la creación de heatmaps
  con anotaciones y paletas de color profesionales. Reduce ~20 líneas
  de configuración manual a una sola llamada.
- sklearn.decomposition.PCA: implementación eficiente de Análisis de
  Componentes Principales. PCA reduce la dimensionalidad de los vectores
  (de n dimensiones a 2) preservando la máxima varianza posible,
  permitiendo visualizar las relaciones entre documentos en un plano 2D.
  Internamente usa SVD (Descomposición en Valores Singulares), otro
  concepto fundamental de álgebra lineal.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Backend sin GUI para servidores/containers
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


# Directorio de salida para los gráficos
DIRECTORIO_GRAFICOS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "graficos"
)


def _asegurar_directorio():
    """Crea el directorio de gráficos si no existe."""
    os.makedirs(DIRECTORIO_GRAFICOS, exist_ok=True)


def plot_matriz_similitud(matriz_similitudes, etiquetas=None,
                          guardar=True, mostrar=False):
    """
    Genera un mapa de calor (heatmap) de la matriz de similitud coseno.

    Cada celda (i, j) muestra qué tan similares son los documentos i y j.
    Colores cálidos = alta similitud, colores fríos = baja similitud.

    Parámetros
    ----------
    matriz_similitudes : numpy.ndarray
        Matriz cuadrada (m x m) de similitudes coseno.
    etiquetas : list[str], opcional
        Nombres de los documentos para los ejes.
    guardar : bool
        Si True, guarda la imagen en graficos/.
    mostrar : bool
        Si True, muestra el gráfico en pantalla.

    Retorna
    -------
    str — Ruta del archivo guardado (o None si no se guardó).
    """
    _asegurar_directorio()

    n = len(matriz_similitudes)
    if etiquetas is None:
        etiquetas = [f"Doc {i+1}" for i in range(n)]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Heatmap con seaborn: paleta "YlOrRd" (amarillo-naranja-rojo)
    # annot=True muestra los valores numéricos en cada celda
    # fmt=".2f" formatea a 2 decimales
    sns.heatmap(
        matriz_similitudes,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd",
        xticklabels=etiquetas,
        yticklabels=etiquetas,
        vmin=0, vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Similitud Coseno"},
        ax=ax
    )

    ax.set_title(
        "Matriz de Similitud Coseno entre Documentos",
        fontsize=14, fontweight="bold", pad=15
    )
    ax.set_xlabel("Documentos", fontsize=11)
    ax.set_ylabel("Documentos", fontsize=11)

    # Rotar etiquetas para legibilidad
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()

    ruta = None
    if guardar:
        ruta = os.path.join(DIRECTORIO_GRAFICOS, "heatmap_similitud.png")
        fig.savefig(ruta, dpi=150, bbox_inches="tight")
        print(f"[✓] Heatmap guardado en: {ruta}")

    if mostrar:
        plt.show()

    plt.close(fig)
    return ruta


def plot_pca_documentos(matriz_doc_termino, etiquetas=None,
                        consulta_vector=None, consulta_texto=None,
                        guardar=True, mostrar=False):
    """
    Reduce los vectores de documentos a 2D con PCA y crea un scatter plot.

    PCA (Análisis de Componentes Principales) busca las 2 direcciones
    de máxima varianza en el espacio n-dimensional y proyecta los
    datos sobre ellas. Esto permite visualizar la "cercanía" entre
    documentos en un plano cartesiano interpretable.

    Internamente, PCA usa SVD: X = UΣVᵀ, y selecciona las primeras
    2 columnas de la proyección.

    Parámetros
    ----------
    matriz_doc_termino : numpy.ndarray
        Matriz (m x n) de documentos vectorizados.
    etiquetas : list[str], opcional
        Nombres de los documentos.
    consulta_vector : numpy.ndarray, opcional
        Vector de una consulta para incluir en el gráfico.
    consulta_texto : str, opcional
        Texto de la consulta para la leyenda.
    guardar : bool
        Si True, guarda en graficos/.
    mostrar : bool
        Si True, muestra en pantalla.

    Retorna
    -------
    str — Ruta del archivo guardado.
    """
    _asegurar_directorio()

    n_docs = len(matriz_doc_termino)
    if etiquetas is None:
        etiquetas = [f"Doc {i+1}" for i in range(n_docs)]

    # Si hay consulta, agregarla a la matriz para proyectar juntos
    if consulta_vector is not None:
        datos = np.vstack([matriz_doc_termino, consulta_vector.reshape(1, -1)])
    else:
        datos = matriz_doc_termino

    # Aplicar PCA: reducir de n dimensiones a 2
    n_components = min(2, datos.shape[0], datos.shape[1])
    pca = PCA(n_components=n_components)
    datos_2d = pca.fit_transform(datos)

    # Varianza explicada por cada componente
    var_explicada = pca.explained_variance_ratio_ * 100

    fig, ax = plt.subplots(figsize=(10, 8))

    # Graficar documentos
    docs_2d = datos_2d[:n_docs]
    ax.scatter(
        docs_2d[:, 0], docs_2d[:, 1],
        c="#2196F3", s=120, alpha=0.8,
        edgecolors="white", linewidth=1.5,
        zorder=3, label="Documentos"
    )

    # Etiquetar cada punto
    for i, etiqueta in enumerate(etiquetas):
        ax.annotate(
            etiqueta,
            (docs_2d[i, 0], docs_2d[i, 1]),
            textcoords="offset points",
            xytext=(8, 8), fontsize=7,
            alpha=0.85,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="gray", alpha=0.7)
        )

    # Graficar consulta si existe
    if consulta_vector is not None:
        query_2d = datos_2d[n_docs:]
        label_q = f"Consulta: \"{consulta_texto}\"" \
            if consulta_texto else "Consulta"
        ax.scatter(
            query_2d[:, 0], query_2d[:, 1],
            c="#F44336", s=200, marker="*",
            edgecolors="darkred", linewidth=1,
            zorder=4, label=label_q
        )

    ax.set_xlabel(
        f"Componente Principal 1 ({var_explicada[0]:.1f}% varianza)",
        fontsize=11
    )
    if n_components >= 2:
        ax.set_ylabel(
            f"Componente Principal 2 ({var_explicada[1]:.1f}% varianza)",
            fontsize=11
        )

    ax.set_title(
        "Reducción Dimensional PCA — Documentos en 2D",
        fontsize=14, fontweight="bold", pad=15
    )
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3, linestyle="--")
    plt.tight_layout()

    ruta = None
    if guardar:
        ruta = os.path.join(DIRECTORIO_GRAFICOS, "pca_documentos.png")
        fig.savefig(ruta, dpi=150, bbox_inches="tight")
        print(f"[✓] PCA guardado en: {ruta}")

    if mostrar:
        plt.show()

    plt.close(fig)
    return ruta


def plot_frecuencia_terminos(matriz_doc_termino, vocabulario,
                             top_n=15, guardar=True, mostrar=False):
    """
    Genera un gráfico de barras con los términos más frecuentes del corpus.

    Suma las frecuencias de cada término a lo largo de todos los documentos
    (suma por columnas de la Matriz Documento-Término).

    Parámetros
    ----------
    matriz_doc_termino : numpy.ndarray
        Matriz (m x n) documento-término.
    vocabulario : dict
        Diccionario {palabra: índice}.
    top_n : int
        Cantidad de términos más frecuentes a mostrar.
    guardar, mostrar : bool
        Control de salida.

    Retorna
    -------
    str — Ruta del archivo guardado.
    """
    _asegurar_directorio()

    # Sumar frecuencias por columna (total de cada término en el corpus)
    frecuencias_totales = np.sum(matriz_doc_termino, axis=0)

    # Mapeo inverso: índice -> palabra
    vocab_inverso = {idx: palabra for palabra, idx in vocabulario.items()}

    # Crear lista de (palabra, frecuencia) y ordenar
    terminos_freq = [
        (vocab_inverso[i], frecuencias_totales[i])
        for i in range(len(frecuencias_totales))
    ]
    terminos_freq.sort(key=lambda x: x[1], reverse=True)

    # Tomar los top_n
    top_terminos = terminos_freq[:top_n]
    palabras = [t[0] for t in top_terminos]
    frecuencias = [t[1] for t in top_terminos]

    fig, ax = plt.subplots(figsize=(10, 6))

    colores = plt.cm.viridis(np.linspace(0.3, 0.9, len(palabras)))
    barras = ax.bar(palabras, frecuencias, color=colores, edgecolor="white",
                    linewidth=0.8)

    # Añadir valores encima de cada barra
    for barra, freq in zip(barras, frecuencias):
        ax.text(
            barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.1,
            str(int(freq)), ha="center", va="bottom", fontsize=9,
            fontweight="bold"
        )

    ax.set_xlabel("Términos", fontsize=11)
    ax.set_ylabel("Frecuencia Total en el Corpus", fontsize=11)
    ax.set_title(
        f"Top {top_n} Términos Más Frecuentes del Corpus",
        fontsize=14, fontweight="bold", pad=15
    )
    plt.xticks(rotation=45, ha="right", fontsize=9)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()

    ruta = None
    if guardar:
        ruta = os.path.join(DIRECTORIO_GRAFICOS, "frecuencia_terminos.png")
        fig.savefig(ruta, dpi=150, bbox_inches="tight")
        print(f"[✓] Frecuencia guardada en: {ruta}")

    if mostrar:
        plt.show()

    plt.close(fig)
    return ruta


def plot_resultados_busqueda(resultados, consulta, guardar=True,
                             mostrar=False, nombre_archivo=None):
    """
    Gráfico de barras horizontal con las similitudes de una búsqueda.

    Parámetros
    ----------
    resultados : list[dict]
        Salida de BuscadorSemantico.buscar().
    consulta : str
        Texto de la consulta realizada.
    guardar, mostrar : bool
        Control de salida.
    nombre_archivo : str, opcional
        Nombre del archivo PNG (sin extensión).

    Retorna
    -------
    str — Ruta del archivo guardado.
    """
    _asegurar_directorio()

    etiquetas = [r["etiqueta"] for r in resultados]
    similitudes = [r["similitud"] for r in resultados]

    # Invertir para que el más similar esté arriba
    etiquetas = etiquetas[::-1]
    similitudes = similitudes[::-1]

    fig, ax = plt.subplots(figsize=(10, 5))

    colores = plt.cm.RdYlGn(
        np.array(similitudes) / max(similitudes) if max(similitudes) > 0
        else np.zeros(len(similitudes))
    )
    barras = ax.barh(etiquetas, similitudes, color=colores,
                     edgecolor="white", linewidth=0.8, height=0.6)

    # Añadir valores al final de cada barra
    for barra, sim in zip(barras, similitudes):
        ax.text(
            barra.get_width() + 0.01, barra.get_y() + barra.get_height() / 2,
            f"{sim:.4f}", ha="left", va="center", fontsize=9
        )

    ax.set_xlabel("Similitud Coseno", fontsize=11)
    ax.set_title(
        f"Resultados de Búsqueda: \"{consulta}\"",
        fontsize=13, fontweight="bold", pad=15
    )
    ax.set_xlim(0, max(similitudes) * 1.2 if max(similitudes) > 0 else 1)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()

    ruta = None
    if guardar:
        nombre = nombre_archivo or "resultados_busqueda"
        ruta = os.path.join(DIRECTORIO_GRAFICOS, f"{nombre}.png")
        fig.savefig(ruta, dpi=150, bbox_inches="tight")
        print(f"[✓] Resultados guardados en: {ruta}")

    if mostrar:
        plt.show()

    plt.close(fig)
    return ruta

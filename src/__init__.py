"""
Paquete src del Buscador Semántico
===================================
Exporta los módulos principales para facilitar imports.
"""

from src.preprocesamiento import (
    cargar_documentos,
    limpiar_texto,
    tokenizar,
    remover_stopwords,
    preprocesar_documento,
    preprocesar_corpus,
)
from src.vectorizacion import (
    construir_vocabulario,
    crear_matriz_documento_termino,
    obtener_vocabulario_inverso,
)
from src.similitud import (
    calcular_producto_punto,
    calcular_norma,
    similitud_coseno,
)
from src.buscador import BuscadorSemantico
from src.visualizacion import (
    plot_matriz_similitud,
    plot_pca_documentos,
    plot_frecuencia_terminos,
    plot_resultados_busqueda,
)

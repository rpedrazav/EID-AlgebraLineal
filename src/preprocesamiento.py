"""
Módulo de Preprocesamiento de Texto
====================================
"""

import os
import re

# ============================================================================
# Lista de palabras vacías en español (Stopwords)
# ============================================================================
# Estas palabras se repiten mucho pero no aportan un significado real
# (artículos, preposiciones, etc.). Las quitamos para reducir el ruido
# en nuestros datos y disminuir las dimensiones de los vectores.
PALABRAS_VACIAS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "a", "en", "con", "por", "para",
    "y", "o", "u", "e", "ni", "que", "como", "se", "su",
    "es", "son", "ser", "está", "están", "fue", "sin",
    "no", "más", "muy", "ya", "lo", "le", "les", "me",
    "mi", "nos", "te", "ti", "si", "este", "esta", "esto",
    "ese", "esa", "eso", "aquel", "aquella", "aquello",
    "pero", "porque", "cuando", "donde", "quien", "cual",
    "todo", "toda", "todos", "todas", "otro", "otra", "otros",
    "entre", "sobre", "desde", "hasta", "hacia", "mediante",
    "también", "además", "así", "bien", "mal", "cada",
    "ha", "han", "hay", "he", "hemos", "sido", "siendo",
}

def cargar_documentos(ruta_carpeta):
    """Carga los textos desde un archivo .txt o una carpeta."""
    textos_cargados = []

    if os.path.isfile(ruta_carpeta) and ruta_carpeta.endswith(".txt"):
        # Leemos archivo único, asumiendo una línea = un documento
        with open(ruta_carpeta, "r", encoding="utf-8") as f:
            for linea in f:
                texto_limpio = linea.strip()
                if texto_limpio:
                    textos_cargados.append(texto_limpio)
                    
    elif os.path.isdir(ruta_carpeta):
        # Leemos todos los txt en la carpeta
        lista_archivos = sorted(os.listdir(ruta_carpeta))
        for nombre in lista_archivos:
            if nombre.endswith(".txt"):
                ruta_entera = os.path.join(ruta_carpeta, nombre)
                with open(ruta_entera, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    if contenido:
                        textos_cargados.append(contenido)
    else:
        raise FileNotFoundError(f"Ruta no válida o inexistente: {ruta_carpeta}")

    if not textos_cargados:
        raise ValueError(f"No se encontró contenido válido en: {ruta_carpeta}")

    return textos_cargados

def limpiar_texto(texto):
    """Aplica normalización al texto bruto (minúsculas, sin puntuación)."""
    # Todo a minúscula
    texto_min = texto.lower()
    
    # Mantener solo letras del abecedario español y espacios
    texto_filtrado = re.sub(r"[^a-záéíóúüñ\s]", "", texto_min)
    
    # Quitar dobles espacios o más
    texto_final = re.sub(r"\s+", " ", texto_filtrado).strip()
    
    return texto_final

def tokenizar(texto):
    """Divide un texto en una lista de palabras."""
    return texto.split()

def remover_stopwords(tokens):
    """Filtra los tokens quitando las palabras vacías."""
    tokens_utiles = [t for t in tokens if t not in PALABRAS_VACIAS_ES]
    return tokens_utiles

def preprocesar_documento(texto):
    """Aplica el pipeline de preprocesamiento a un solo documento."""
    paso1 = limpiar_texto(texto)
    paso2 = tokenizar(paso1)
    paso3 = remover_stopwords(paso2)
    return paso3

def preprocesar_corpus(documentos):
    """Procesa una lista completa de documentos."""
    return [preprocesar_documento(d) for d in documentos]
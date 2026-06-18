"""
Módulo de Preprocesamiento de Texto
====================================
Autor: Sebastián (Persona 1)

Este script se encarga de tomar los datos de texto sin procesar y 
transformarlos a un formato limpio y tokenizado. Esto es fundamental
para luego poder representarlos algebraicamente como vectores.

Notas de diseño:
- He optado por usar un set de palabras vacías (stopwords) manual en español,
  para no tener que depender de librerías grandes como NLTK o spaCy.
- La limpieza se hace utilizando expresiones regulares nativas ('re').
- La tokenización es un simple split por espacios, ideal para nuestro
  modelo de bolsa de palabras (BoW).
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
    """
    Carga los textos desde una ruta específica. 
    Puede ser un archivo único .txt o una carpeta entera.
    
    Argumentos:
        ruta_carpeta (str): Ruta al archivo o directorio.
        
    Retorna:
        list[str]: Lista con el contenido de los documentos leídos.
    """
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
    """
    Aplica normalización al texto bruto.
    - Pasa todo a minúsculas.
    - Quita caracteres especiales y puntuación.
    - Elimina espacios sobrantes.
    """
    # Todo a minúscula
    texto_min = texto.lower()
    
    # Mantener solo letras del abecedario español y espacios
    texto_filtrado = re.sub(r"[^a-záéíóúüñ\s]", "", texto_min)
    
    # Quitar dobles espacios o más
    texto_final = re.sub(r"\s+", " ", texto_filtrado).strip()
    
    return texto_final

def tokenizar(texto):
    """
    Divide un texto (previamente limpiado) en una lista de palabras.
    Uso split(), que corta usando los espacios en blanco.
    """
    return texto.split()

def remover_stopwords(tokens):
    """
    Filtra los tokens quitando las palabras vacías definidas arriba.
    Usamos un set para que la búsqueda sea rápida (O(1)).
    """
    tokens_utiles = [t for t in tokens if t not in PALABRAS_VACIAS_ES]
    return tokens_utiles

def preprocesar_documento(texto):
    """
    Función envoltorio que aplica todos los pasos a un solo documento:
    1. Limpieza
    2. Tokenización
    3. Remoción de stopwords
    """
    paso1 = limpiar_texto(texto)
    paso2 = tokenizar(paso1)
    paso3 = remover_stopwords(paso2)
    return paso3

def preprocesar_corpus(documentos):
    """
    Procesa una lista completa de documentos aplicando
    el pipeline de preprocesamiento a cada uno.
    """
    return [preprocesar_documento(d) for d in documentos]
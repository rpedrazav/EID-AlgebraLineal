"""
Módulo de Preprocesamiento de Texto
====================================
Responsable: Persona 1 (Seba)

Este módulo se encarga de transformar los textos en bruto (raw) a un formato
limpio y tokenizado, listo para la etapa de vectorización.

Decisiones de diseño:
- Se usa una lista manual de stopwords en español en lugar de NLTK para
  minimizar dependencias externas y mantener el proyecto ligero.
- La limpieza elimina toda puntuación y caracteres especiales usando
  expresiones regulares estándar de Python (módulo 're'), evitando
  dependencias adicionales.
- Se optó por tokenización simple (split por espacios) dado que para un
  modelo Bag-of-Words con frecuencia de términos, este enfoque es
  suficiente y transparente.
"""

import os
import re


# ============================================================================
# Stopwords en español (lista curada manualmente)
# ============================================================================
# Estas son palabras funcionales del idioma español que no aportan significado
# semántico al análisis. Se excluyen del vocabulario para reducir la dimensión
# del espacio vectorial y mejorar la calidad de las similitudes calculadas.
STOPWORDS_ES = {
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
    Carga documentos de texto desde un archivo o carpeta.

    Si la ruta apunta a un archivo .txt, lee cada línea no vacía como
    un documento independiente. Si es una carpeta, busca todos los .txt
    dentro de ella.

    Parámetros
    ----------
    ruta_carpeta : str
        Ruta al archivo o carpeta que contiene los documentos.

    Retorna
    -------
    list[str]
        Lista de cadenas de texto, cada una representando un documento.

    Ejemplo
    -------
    >>> docs = cargar_documentos("data/documentos/corpus.txt")
    >>> print(len(docs))
    12
    """
    documentos = []

    if os.path.isfile(ruta_carpeta) and ruta_carpeta.endswith(".txt"):
        # Caso: es un archivo de texto directo (un documento por línea)
        with open(ruta_carpeta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:  # Ignorar líneas vacías
                    documentos.append(linea)
    elif os.path.isdir(ruta_carpeta):
        # Caso: es una carpeta con múltiples archivos .txt
        archivos = sorted(os.listdir(ruta_carpeta))
        for nombre_archivo in archivos:
            if nombre_archivo.endswith(".txt"):
                ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
                with open(ruta_completa, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read().strip()
                    if contenido:
                        documentos.append(contenido)
    else:
        raise FileNotFoundError(
            f"No se encontró el archivo o carpeta: {ruta_carpeta}"
        )

    if not documentos:
        raise ValueError(
            f"No se encontraron documentos en: {ruta_carpeta}"
        )

    return documentos


def limpiar_texto(texto):
    """
    Limpia un texto eliminando caracteres no deseados y normalizándolo.

    Proceso de limpieza:
    1. Convierte a minúsculas para uniformidad.
    2. Elimina signos de puntuación y caracteres especiales con regex.
    3. Colapsa espacios múltiples en uno solo.

    Se usa re.sub() con el patrón [^a-záéíóúüñ\\s] que conserva solo
    letras del alfabeto español y espacios. Esto es más eficiente que
    iterar carácter por carácter con un bucle for.

    Parámetros
    ----------
    texto : str
        Texto en bruto a limpiar.

    Retorna
    -------
    str
        Texto limpio, en minúsculas, sin puntuación.

    Ejemplo
    -------
    >>> limpiar_texto("¡Hola, Mundo! ¿Cómo estás?")
    'hola mundo cómo estás'
    """
    # Paso 1: Convertir a minúsculas
    texto = texto.lower()

    # Paso 2: Eliminar todo lo que no sea letra (incluyendo acentos) o espacio
    texto = re.sub(r"[^a-záéíóúüñ\s]", "", texto)

    # Paso 3: Reducir espacios múltiples a uno solo
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def tokenizar(texto):
    """
    Separa un texto limpio en una lista de palabras individuales (tokens).

    Se usa split() de Python que divide por espacios en blanco. Este método
    es O(n) en tiempo y no requiere librerías externas como NLTK o spaCy.

    Parámetros
    ----------
    texto : str
        Texto previamente limpiado con limpiar_texto().

    Retorna
    -------
    list[str]
        Lista de palabras (tokens).

    Ejemplo
    -------
    >>> tokenizar("hola mundo cómo estás")
    ['hola', 'mundo', 'cómo', 'estás']
    """
    return texto.split()


def remover_stopwords(tokens):
    """
    Elimina palabras vacías (stopwords) de una lista de tokens.

    Las stopwords son palabras funcionales del idioma que no aportan
    significado semántico (artículos, preposiciones, conjunciones).
    Removerlas reduce la dimensionalidad del espacio vectorial y mejora
    la calidad de las similitudes calculadas.

    Se usa una búsqueda O(1) en un set (STOPWORDS_ES) en lugar de una
    lista, lo que hace la operación eficiente incluso con vocabularios
    grandes.

    Parámetros
    ----------
    tokens : list[str]
        Lista de palabras tokenizadas.

    Retorna
    -------
    list[str]
        Lista filtrada sin stopwords.

    Ejemplo
    -------
    >>> remover_stopwords(["la", "inteligencia", "artificial", "es", "genial"])
    ['inteligencia', 'artificial', 'genial']
    """
    return [token for token in tokens if token not in STOPWORDS_ES]


def preprocesar_documento(texto):
    """
    Aplica el pipeline completo de preprocesamiento a un documento.

    Pipeline: texto bruto -> limpieza -> tokenización -> remoción de stopwords.

    Parámetros
    ----------
    texto : str
        Texto en bruto del documento.

    Retorna
    -------
    list[str]
        Lista de tokens limpios y filtrados.
    """
    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)
    tokens_filtrados = remover_stopwords(tokens)
    return tokens_filtrados


def preprocesar_corpus(documentos):
    """
    Aplica el pipeline de preprocesamiento a una lista de documentos.

    Parámetros
    ----------
    documentos : list[str]
        Lista de textos en bruto.

    Retorna
    -------
    list[list[str]]
        Lista de listas de tokens procesados, una por documento.
    """
    return [preprocesar_documento(doc) for doc in documentos]

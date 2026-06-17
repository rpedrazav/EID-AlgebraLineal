#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa Principal — Buscador Semántico Simple
================================================
Responsable: Rodrigo (Persona 4 — Integración y Project Manager)
Curso: Álgebra Lineal para la Computación

Descripción general
-------------------
Este archivo es el punto de entrada único del proyecto. Su función es
ensamblar todas las piezas desarrolladas por el equipo en un pipeline
coherente y ejecutable:

    Corpus de texto
        └─► Preprocesamiento  (src/preprocesamiento.py)
                └─► Vectorización   (src/vectorizacion.py)
                        └─► Similitud Coseno (src/similitud.py)
                                └─► Buscador      (src/buscador.py)
                                        └─► Visualización (src/visualizacion.py)

Formas de ejecución
-------------------
Desde la RAÍZ del proyecto (carpeta EID-AlgebraLineal/):

    Modo interactivo (menú de terminal):
        python -m src.main

    Modo demo automático (sin interacción del usuario):
        python -m src.main --demo

Decisiones de diseño tomadas en este archivo
--------------------------------------------
1. Usamos `python -m src.main` en lugar de ejecutar `src/main.py` directamente,
   porque el flag -m garantiza que Python añade el directorio raíz al sys.path
   automáticamente. Así, los imports del estilo `from src.preprocesamiento import ...`
   funcionan correctamente sin manipular PYTHONPATH desde el sistema operativo.

2. El modo --demo existe para que los gráficos y resultados CSV puedan generarse
   con un solo comando, sin que el evaluador tenga que interactuar manualmente.
   Es clave para reproducibilidad: cualquier persona puede clonar el repo y
   ejecutar `python -m src.main --demo` para obtener todos los resultados.

3. El pipeline se inicializa UNA SOLA VEZ (función inicializar_pipeline) y los
   objetos resultantes se reutilizan en el menú. Si vectorizáramos en cada
   búsqueda, el tiempo por consulta escalaría con el tamaño del corpus.
   Al vectorizar una sola vez y guardar la matriz en RAM, las búsquedas son
   O(m·n) donde m=documentos y n=vocabulario, que es muy eficiente.

4. La exportación a CSV se hace con el módulo estándar `csv` en lugar de pandas
   porque el volumen de datos es pequeño y así se elimina una dependencia pesada
   para una tarea simple de escritura secuencial.
"""

import os
import sys
import csv
import numpy as np

# Forzar salida UTF-8 en Windows para soportar caracteres especiales
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Configuración del sys.path
# ---------------------------------------------------------------------------
# Necesitamos que el directorio raíz del proyecto esté en sys.path para que
# los imports de `src.*` funcionen independientemente de desde dónde se
# ejecute el script.
# os.path.abspath(__file__) → ruta absoluta de main.py
# os.path.dirname(...)      → carpeta src/
# os.path.dirname(...)      → carpeta raíz del proyecto
directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

# ---------------------------------------------------------------------------
# Importaciones de los módulos del proyecto
# ---------------------------------------------------------------------------
from src.preprocesamiento import cargar_documentos, preprocesar_corpus
from src.vectorizacion import (
    construir_vocabulario,
    crear_matriz_documento_termino,
)
from src.buscador import BuscadorSemantico
from src.visualizacion import (
    plot_matriz_similitud,
    plot_pca_documentos,
    plot_frecuencia_terminos,
    plot_resultados_busqueda,
)


# ---------------------------------------------------------------------------
# Constantes de rutas
# ---------------------------------------------------------------------------
# Definimos las rutas como constantes globales para que sean fáciles de
# modificar si el usuario cambia la estructura de carpetas. Es mejor práctica
# que tener las rutas "hardcodeadas" dentro de cada función.
RUTA_CORPUS = os.path.join(
    directorio_raiz, "data", "documentos", "corpus.txt"
)
RUTA_RESULTADOS = os.path.join(
    directorio_raiz, "resultados", "resultados_busquedas.csv"
)


# ===========================================================================
# FUNCIÓN: inicializar_pipeline
# ===========================================================================
def inicializar_pipeline():
    """
    Ejecuta el pipeline completo de preparación de datos del buscador.

    Etapas del pipeline
    -------------------
    1. Carga de documentos desde el corpus (archivo .txt).
    2. Preprocesamiento: limpieza, tokenización y remoción de stopwords.
    3. Vectorización: construcción del vocabulario y la Matriz Documento-Término.
    4. Inicialización del motor de búsqueda (BuscadorSemantico).

    Decisión de diseño — sparsidad
    --------------------------------
    Calculamos y mostramos la sparsidad de la matriz como indicador de
    eficiencia. La sparsidad es el porcentaje de celdas con valor 0.
    En un modelo Bag-of-Words, valores de 80-95% de sparsidad son normales:
    cada documento usa solo una fracción del vocabulario total. Esto valida
    que nuestra implementación es realista.

    Retorna
    -------
    tuple
        (buscador, vocabulario, matriz, documentos, etiquetas)
        - buscador    : instancia de BuscadorSemantico lista para consultas
        - vocabulario : dict {palabra: índice}
        - matriz      : numpy.ndarray (m x n) Matriz Documento-Término
        - documentos  : list[str] textos originales
        - etiquetas   : list[str] nombres cortos para cada documento
    """
    print("=" * 62)
    print("  BUSCADOR SEMANTICO SIMPLE")
    print("  Algebra Lineal para la Computacion - Grupo 2")
    print("  Rodrigo | Seba | Dani | Renato")
    print("=" * 62)

    # ------------------------------------------------------------------
    # Paso 1: Cargar documentos
    # ------------------------------------------------------------------
    # cargar_documentos() soporta tanto un archivo .txt (una línea = un doc)
    # como una carpeta de archivos .txt independientes. Aquí usamos la
    # modalidad de archivo único porque simplifica la gestión del corpus.
    print("\n[1/4] Cargando documentos...")
    documentos = cargar_documentos(RUTA_CORPUS)
    print(f"      -> {len(documentos)} documentos cargados.")

    # Etiquetas cortas para identificar documentos en gráficos y resultados.
    # "Doc 1", "Doc 2", etc. son más manejables que mostrar el texto completo.
    etiquetas = [f"Doc {i + 1}" for i in range(len(documentos))]  # Ej: "Doc 1", "Doc 2"...

    # ------------------------------------------------------------------
    # Paso 2: Preprocesamiento
    # ------------------------------------------------------------------
    # El preprocesamiento normaliza el texto antes de vectorizar:
    # mayúsculas → minúsculas, puntuación eliminada, stopwords removidas.
    # Sin este paso, "Inteligencia" y "inteligencia" serían palabras distintas
    # en el vocabulario, multiplicando dimensiones inútilmente.
    print("[2/4] Preprocesando textos...")
    corpus_procesado = preprocesar_corpus(documentos)
    total_tokens = sum(len(doc) for doc in corpus_procesado)
    print(f"      -> {total_tokens} tokens tras preprocesamiento.")

    # ------------------------------------------------------------------
    # Paso 3: Vectorización
    # ------------------------------------------------------------------
    # construir_vocabulario → asigna un índice único a cada palabra del corpus
    # crear_matriz_documento_termino → rellena la matriz de frecuencias
    #
    # La dimensión del espacio vectorial = tamaño del vocabulario.
    # Cada documento es un punto en R^n donde n = |vocabulario|.
    print("[3/4] Construyendo espacio vectorial...")
    vocabulario = construir_vocabulario(corpus_procesado)
    matriz = crear_matriz_documento_termino(corpus_procesado, vocabulario)
    print(f"      -> Vocabulario: {len(vocabulario)} terminos unicos.")
    print(
        f"      -> Matriz Documento-Termino: "
        f"{matriz.shape[0]} filas x {matriz.shape[1]} columnas"
    )

    # Calculamos sparsidad: % de celdas con valor 0.
    # Usamos np.count_nonzero para contar las celdas NO nulas, luego restamos.
    # Este enfoque es más directo que contar zeros directamente, porque
    # np.count_nonzero está optimizado en C (más rápido que np.sum(matriz==0)).
    ceros = matriz.size - np.count_nonzero(matriz)
    sparsidad = (ceros / matriz.size) * 100
    print(f"      -> Sparsidad de la matriz: {sparsidad:.1f}%")
    print(
        f"      -> Interpretacion: el {sparsidad:.1f}% de las "
        f"celdas son 0 (documento no contiene ese termino)."
    )

    # ------------------------------------------------------------------
    # Paso 4: Inicializar el motor de búsqueda
    # ------------------------------------------------------------------
    # BuscadorSemantico encapsula la matriz y el vocabulario. Al inicializarlo
    # aquí una sola vez, todas las búsquedas posteriores reutilizan la misma
    # representación vectorial sin necesidad de recalcularla.
    print("[4/4] Inicializando motor de búsqueda...")
    buscador = BuscadorSemantico(
        matriz, vocabulario, documentos, etiquetas
    )
    print("      -> Motor listo.\n")

    return buscador, vocabulario, matriz, documentos, etiquetas


# ===========================================================================
# FUNCIÓN: generar_graficos
# ===========================================================================
def generar_graficos(buscador, vocabulario, matriz, etiquetas):
    """
    Genera los tres gráficos base del análisis experimental.

    Gráficos producidos
    -------------------
    1. Heatmap de similitud coseno entre todos los documentos.
       → Permite identificar visualmente clústeres temáticos.
    2. Scatter plot PCA: documentos reducidos a 2 dimensiones.
       → Permite ver la distribución geométrica del corpus.
    3. Barras: top-15 términos más frecuentes del corpus.
       → Valida que el preprocesamiento eliminó correctamente las stopwords.

    Parámetros
    ----------
    buscador   : BuscadorSemantico — motor de búsqueda inicializado.
    vocabulario : dict             — mapeo {palabra: índice}.
    matriz     : numpy.ndarray     — Matriz Documento-Término (m × n).
    etiquetas  : list[str]         — nombres de los documentos.

    Retorna
    -------
    numpy.ndarray
        Matriz de similitudes coseno (m × m), útil para análisis posteriores.
    """
    print("--- Generando graficos base ---")

    # calcular_matriz_similitud() computa cos(θ) entre cada par de documentos.
    # La guarda en una matriz simétrica m×m. Al llamarla aquí y pasar el
    # resultado a plot_matriz_similitud(), evitamos calcularla dos veces.
    matriz_sim = buscador.calcular_matriz_similitud()
    plot_matriz_similitud(matriz_sim, etiquetas)

    # PCA reduce los vectores de n dimensiones a 2 para poder graficarlos.
    # Es visualización, no modifica el buscador.
    plot_pca_documentos(matriz, etiquetas)

    # top_n=15 muestra los 15 términos más usados en todo el corpus.
    # Menos de 10 no da suficiente información; más de 20 hace ilegible el eje.
    plot_frecuencia_terminos(matriz, vocabulario, top_n=15)

    print("--- Graficos base completados ---\n")
    return matriz_sim


# ===========================================================================
# FUNCIÓN: realizar_busqueda
# ===========================================================================
def realizar_busqueda(buscador, consulta, top_n=5):
    """
    Ejecuta una consulta en el buscador semántico y muestra los resultados.

    Proceso interno (dentro de BuscadorSemantico.buscar)
    -----------------------------------------------------
    1. La consulta pasa por el mismo preprocesamiento que los documentos.
    2. Se convierte en un vector usando el vocabulario existente.
       (Palabras de la consulta que no están en el vocabulario se ignoran.)
    3. Se calcula similitud coseno entre el vector consulta y cada fila de
       la Matriz Documento-Término.
    4. Los documentos se ordenan de mayor a menor similitud.
    5. Se retornan los top_n primeros.

    Parámetros
    ----------
    buscador : BuscadorSemantico — motor de búsqueda.
    consulta : str               — texto ingresado por el usuario.
    top_n    : int               — número máximo de resultados (default: 5).

    Retorna
    -------
    list[dict]
        Lista de resultados con claves: 'etiqueta', 'similitud', 'documento'.
    """
    print(f"\n  Consulta: \"{consulta}\"")
    print("  " + "-" * 55)

    resultados = buscador.buscar(consulta, top_n=top_n)

    # Si el primer resultado tiene similitud 0, ningun termino de la consulta
    # aparece en el corpus -> busqueda sin resultados relevantes.
    if not resultados or resultados[0]["similitud"] == 0.0:
        print("  [!] No se encontraron documentos relevantes para esa consulta.")
        print("      Intente con terminos mas relacionados al corpus.")
        return resultados

    for i, r in enumerate(resultados, 1):
        barra = "|" * int(r["similitud"] * 30)
        print(f"\n  #{i} [{r['etiqueta']}]  Similitud: {r['similitud']:.4f}")
        print(f"      {barra}")
        if "documento" in r:
            print(f"      -> {r['documento']}")

    return resultados


# ===========================================================================
# FUNCIÓN: exportar_resultados_csv
# ===========================================================================
def exportar_resultados_csv(todas_busquedas, ruta=None):
    """
    Exporta el historial de búsquedas a un archivo CSV.

    Formato del CSV
    ---------------
    columnas: consulta | ranking | documento | similitud

    Decisión de diseño — módulo csv vs pandas
    ------------------------------------------
    Usamos el módulo estándar `csv` en lugar de pandas.DataFrame.to_csv()
    porque:
    - El volumen de datos es pequeño (máx. ~100 filas por sesión).
    - `csv` no requiere instalar pandas, reduciendo dependencias.
    - El código es transparente: se ve exactamente qué se escribe y cómo.
    pandas sería preferible si necesitáramos transformar o filtrar datos antes
    de exportar.

    Parámetros
    ----------
    todas_busquedas : list[tuple]
        Lista de tuplas (consulta: str, resultados: list[dict]).
    ruta : str, opcional
        Ruta de destino. Si es None, usa RUTA_RESULTADOS.
    """
    ruta = ruta or RUTA_RESULTADOS

    # exist_ok=True evita error si la carpeta ya existe.
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # newline="" es requerido en Windows para evitar líneas en blanco dobles.
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Cabecera del CSV
        writer.writerow(["consulta", "ranking", "documento", "similitud"])
        for consulta, resultados in todas_busquedas:
            for i, r in enumerate(resultados, 1):
                writer.writerow([
                    consulta,
                    i,
                    r["etiqueta"],
                    f"{r['similitud']:.6f}"
                ])

    print(f"\n  [✓] Resultados exportados a: {ruta}")


# ===========================================================================
# FUNCIÓN: menu_interactivo
# ===========================================================================
def menu_interactivo(buscador, vocabulario, matriz, etiquetas):
    """
    Muestra un menú de terminal en bucle para interactuar con el buscador.

    Opciones del menú
    -----------------
    1. Realizar búsqueda → ingresa una consulta y ver los documentos más similares.
    2. Generar todos los gráficos → heatmap, PCA y frecuencia de términos.
    3. Ver vocabulario → lista completa de términos indexados.
    4. Ver matriz documento-término → imprime la matriz numérica.
    5. Exportar resultados a CSV → guarda el historial de búsquedas.
    0. Salir → exporta automáticamente y termina.

    Decisión de diseño — menú en terminal vs. interfaz gráfica
    ------------------------------------------------------------
    Se eligió un menú de texto (stdin/stdout) porque:
    - No requiere bibliotecas adicionales (tkinter, PyQt, etc.).
    - Funciona en cualquier entorno: Windows, Linux, macOS, SSH remoto.
    - Es suficiente para una demo académica donde el foco está en el
      algoritmo, no en la UI.

    Parámetros
    ----------
    buscador    : BuscadorSemantico — motor de búsqueda.
    vocabulario : dict              — mapeo {palabra: índice}.
    matriz      : numpy.ndarray     — Matriz Documento-Término (m × n).
    etiquetas   : list[str]         — nombres de los documentos.
    """
    # Acumulamos todas las búsquedas para poder exportarlas en bloque al final.
    todas_busquedas = []

    while True:
        print("\n" + "=" * 45)
        print("  MENÚ PRINCIPAL — BUSCADOR SEMÁNTICO")
        print("=" * 45)
        print("  1. Realizar búsqueda")
        print("  2. Generar todos los gráficos")
        print("  3. Ver vocabulario completo")
        print("  4. Ver matriz documento-término")
        print("  5. Exportar resultados a CSV")
        print("  0. Salir")
        print("-" * 45)

        opcion = input("  Seleccione opción [0-5]: ").strip()

        if opcion == "1":
            consulta = input("  Ingrese su consulta: ").strip()
            if not consulta:
                print("  [!] La consulta no puede estar vacía.")
                continue

            resultados = realizar_busqueda(buscador, consulta)
            todas_busquedas.append((consulta, resultados))

            # Gráfico de barras horizontal con similitudes de esta búsqueda.
            # El nombre del archivo incluye el número de búsqueda para no
            # sobreescribir los gráficos de búsquedas anteriores.
            nombre_grafico = f"busqueda_{len(todas_busquedas)}"
            plot_resultados_busqueda(
                resultados, consulta, nombre_archivo=nombre_grafico
            )

            # PCA con la consulta proyectada: permite ver visualmente qué tan
            # cerca del clúster de documentos relevantes cayó la consulta.
            vector_q = buscador.vectorizar_consulta(consulta)
            plot_pca_documentos(
                matriz, etiquetas,
                consulta_vector=vector_q,
                consulta_texto=consulta
            )

        elif opcion == "2":
            generar_graficos(buscador, vocabulario, matriz, etiquetas)

        elif opcion == "3":
            print(f"\n  Vocabulario completo ({len(vocabulario)} terminos):")
            print("  " + "-" * 35)
            # sorted() ordena alfabeticamente para facilitar la busqueda visual.
            for palabra, idx in sorted(vocabulario.items()):
                print(f"    [{idx:3d}] {palabra}")

        elif opcion == "4":
            print(
                f"\n  Matriz Documento-Termino "
                f"({matriz.shape[0]} docs x {matriz.shape[1]} terminos):"
            )
            print()
            # Imprimimos con opciones de numpy para formato compacto.
            with np.printoptions(precision=0, suppress=True, linewidth=120):
                print(matriz)

        elif opcion == "5":
            if todas_busquedas:
                exportar_resultados_csv(todas_busquedas)
            else:
                print("  [!] Aún no hay búsquedas registradas.")

        elif opcion == "0":
            # Al salir, exportamos automaticamente si hay busquedas pendientes.
            if todas_busquedas:
                print("\n  Exportando historial de busquedas...")
                exportar_resultados_csv(todas_busquedas)
            print("\n  Hasta luego! - Buscador Semantico cerrado.\n")
            break

        else:
            print("  [!] Opcion invalida. Ingrese un numero entre 0 y 5.")


# ===========================================================================
# FUNCIÓN: ejecutar_demo
# ===========================================================================
def ejecutar_demo():
    """
    Ejecuta una demostración automática con consultas predefinidas.

    Propósito
    ---------
    Permite reproducir todos los resultados del proyecto con un solo comando,
    sin intervención manual. Útil para:
    - Que el profesor verifique el funcionamiento del sistema.
    - Generar automáticamente todos los gráficos e ilustraciones del informe.
    - Comprobar que el entorno está configurado correctamente.

    Consultas de demostración
    -------------------------
    Las 5 consultas cubren los temas principales del corpus para demostrar
    que el buscador recupera documentos temáticamente relevantes:
    1. "inteligencia artificial aprendizaje" → espera recuperar docs 1, 2, 3, 11
    2. "seguridad informática redes protección" → espera doc 4
    3. "programación software desarrollo" → espera docs 7, 9
    4. "datos bases consultas información" → espera docs 6, 8
    5. "robots autónomos ingeniería" → espera doc 12

    Decisión de diseño — 5 consultas
    ---------------------------------
    Se eligieron 5 porque cubren los 5 clústeres temáticos del corpus sin
    redundancia, permitiendo un análisis comparativo representativo.
    """
    # Inicializar el pipeline completo
    buscador, vocabulario, matriz, documentos, etiquetas = \
        inicializar_pipeline()

    # Generar los gráficos base antes de las búsquedas
    matriz_sim = generar_graficos(buscador, vocabulario, matriz, etiquetas)

    # ------------------------------------------------------------------
    # Consultas predefinidas para la demostración
    # ------------------------------------------------------------------
    consultas_demo = [
        "inteligencia artificial aprendizaje",
        "seguridad informática redes protección",
        "programación software desarrollo",
        "datos bases consultas información",
        "robots autónomos ingeniería",
    ]

    print("=" * 62)
    print("  DEMOSTRACION AUTOMATICA --- 5 Busquedas Predefinidas")
    print("=" * 62)

    todas_busquedas = []
    for i, consulta in enumerate(consultas_demo, 1):
        print(f"\n[Búsqueda {i}/{len(consultas_demo)}]")
        resultados = realizar_busqueda(buscador, consulta)
        todas_busquedas.append((consulta, resultados))

        # Gráfico de barras para esta búsqueda
        plot_resultados_busqueda(
            resultados, consulta,
            nombre_archivo=f"busqueda_{i}"
        )

    # PCA final mostrando la primera consulta proyectada sobre el corpus
    vector_q = buscador.vectorizar_consulta(consultas_demo[0])
    plot_pca_documentos(
        matriz, etiquetas,
        consulta_vector=vector_q,
        consulta_texto=consultas_demo[0]
    )

    # Exportar todos los resultados a CSV
    exportar_resultados_csv(todas_busquedas)

    # Resumen final
    print("\n" + "=" * 62)
    print("  DEMOSTRACION COMPLETADA")
    print(f"  -> {len(consultas_demo)} busquedas realizadas")
    print(f"  -> Graficos guardados en: graficos/")
    print(f"  -> Resultados en: resultados/resultados_busquedas.csv")
    print("=" * 62)


# ===========================================================================
# PUNTO DE ENTRADA
# ===========================================================================
if __name__ == "__main__":
    """
    Punto de entrada del programa.

    Lógica de selección de modo
    ---------------------------
    - Si se pasa el argumento --demo en la línea de comandos:
        → Ejecuta la demo automática (no interactiva).
    - En cualquier otro caso:
        → Inicializa el pipeline y lanza el menú interactivo.

    Usamos sys.argv (lista de argumentos de línea de comandos) en lugar de
    argparse porque la lógica de argumentos es simple (un solo flag booleano).
    argparse sería preferible si hubiera múltiples opciones con valores.
    """
    if "--demo" in sys.argv:
        ejecutar_demo()
    else:
        buscador, vocabulario, matriz, documentos, etiquetas = \
            inicializar_pipeline()
        menu_interactivo(buscador, vocabulario, matriz, etiquetas)

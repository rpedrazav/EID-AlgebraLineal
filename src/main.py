#!/usr/bin/env python3
"""
Programa Principal — Buscador Semántico Simple
================================================
Responsable: Persona 4 (Rodri)

Script de entrada que integra todo el pipeline:
  Corpus → Preprocesamiento → Vectorización → Búsqueda → Visualización

Ejecutar desde la raíz del proyecto:
  python -m src.main

Decisiones de diseño:
- Menú interactivo en terminal para facilitar la demostración.
- Se generan automáticamente todos los gráficos al cargar el corpus.
- Los resultados de búsquedas se exportan a CSV en resultados/.
"""

import os
import sys
import csv
import numpy as np

# Asegurar que el directorio raíz del proyecto esté en el path
directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

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


# ============================================================================
# Configuración
# ============================================================================
RUTA_CORPUS = os.path.join(directorio_raiz, "data", "documentos", "corpus.txt")
RUTA_RESULTADOS = os.path.join(directorio_raiz, "resultados",
                               "resultados_busquedas.csv")


def inicializar_pipeline():
    """
    Ejecuta el pipeline completo de preparación de datos.

    Retorna
    -------
    tuple : (buscador, vocabulario, matriz, documentos, etiquetas)
    """
    print("=" * 60)
    print("  BUSCADOR SEMÁNTICO SIMPLE")
    print("  Álgebra Lineal para la Computación")
    print("=" * 60)

    # 1. Cargar documentos
    print("\n[1/4] Cargando documentos...")
    documentos = cargar_documentos(RUTA_CORPUS)
    print(f"      → {len(documentos)} documentos cargados.")

    # Crear etiquetas cortas
    etiquetas = [f"Doc {i+1}" for i in range(len(documentos))]

    # 2. Preprocesar
    print("[2/4] Preprocesando textos...")
    corpus_procesado = preprocesar_corpus(documentos)
    total_tokens = sum(len(doc) for doc in corpus_procesado)
    print(f"      → {total_tokens} tokens tras preprocesamiento.")

    # 3. Vectorizar
    print("[3/4] Construyendo espacio vectorial...")
    vocabulario = construir_vocabulario(corpus_procesado)
    matriz = crear_matriz_documento_termino(corpus_procesado, vocabulario)
    print(f"      → Vocabulario: {len(vocabulario)} términos únicos.")
    print(f"      → Matriz Documento-Término: {matriz.shape[0]} x "
          f"{matriz.shape[1]}")

    # Calcular sparsidad
    ceros = np.count_nonzero(matriz == 0)
    total = matriz.size
    sparsidad = (ceros / total) * 100
    print(f"      → Sparsidad de la matriz: {sparsidad:.1f}%")

    # 4. Crear buscador
    print("[4/4] Inicializando motor de búsqueda...")
    buscador = BuscadorSemantico(
        matriz, vocabulario, documentos, etiquetas
    )
    print("      → Buscador listo.\n")

    return buscador, vocabulario, matriz, documentos, etiquetas


def generar_graficos(buscador, vocabulario, matriz, etiquetas):
    """Genera todos los gráficos del proyecto."""
    print("\n--- Generando gráficos ---")

    # Heatmap de similitud
    matriz_sim = buscador.calcular_matriz_similitud()
    plot_matriz_similitud(matriz_sim, etiquetas)

    # PCA
    plot_pca_documentos(matriz, etiquetas)

    # Frecuencia de términos
    plot_frecuencia_terminos(matriz, vocabulario, top_n=15)

    print("--- Gráficos generados ---\n")
    return matriz_sim


def realizar_busqueda(buscador, consulta, top_n=5):
    """Ejecuta una búsqueda y muestra los resultados."""
    print(f"\n🔍 Consulta: \"{consulta}\"")
    print("-" * 50)

    resultados = buscador.buscar(consulta, top_n=top_n)

    if not resultados or resultados[0]["similitud"] == 0:
        print("  No se encontraron documentos relevantes.")
        return resultados

    for i, r in enumerate(resultados, 1):
        print(f"  {i}. [{r['etiqueta']}] Similitud: {r['similitud']:.4f}")
        if "documento" in r:
            print(f"     {r['documento']}")

    return resultados


def exportar_resultados_csv(todas_busquedas, ruta=None):
    """Exporta los resultados de múltiples búsquedas a CSV."""
    ruta = ruta or RUTA_RESULTADOS
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "consulta", "ranking", "documento", "similitud"
        ])
        for consulta, resultados in todas_busquedas:
            for i, r in enumerate(resultados, 1):
                writer.writerow([
                    consulta, i, r["etiqueta"], f"{r['similitud']:.6f}"
                ])

    print(f"\n[✓] Resultados exportados a: {ruta}")


def menu_interactivo(buscador, vocabulario, matriz, etiquetas):
    """Menú interactivo de terminal."""
    todas_busquedas = []

    while True:
        print("\n" + "=" * 40)
        print("  MENÚ PRINCIPAL")
        print("=" * 40)
        print("  1. Realizar búsqueda")
        print("  2. Generar todos los gráficos")
        print("  3. Ver vocabulario")
        print("  4. Ver matriz documento-término")
        print("  5. Exportar resultados a CSV")
        print("  0. Salir")
        print("-" * 40)

        opcion = input("  Seleccione opción: ").strip()

        if opcion == "1":
            consulta = input("  Ingrese su consulta: ").strip()
            if consulta:
                resultados = realizar_busqueda(buscador, consulta)
                todas_busquedas.append((consulta, resultados))
                # Generar gráfico de esta búsqueda
                nombre = f"busqueda_{len(todas_busquedas)}"
                plot_resultados_busqueda(
                    resultados, consulta, nombre_archivo=nombre
                )
                # PCA con consulta
                vector_q = buscador.vectorizar_consulta(consulta)
                plot_pca_documentos(
                    matriz, etiquetas,
                    consulta_vector=vector_q,
                    consulta_texto=consulta
                )

        elif opcion == "2":
            generar_graficos(buscador, vocabulario, matriz, etiquetas)

        elif opcion == "3":
            print(f"\n  Vocabulario ({len(vocabulario)} términos):")
            for palabra, idx in sorted(vocabulario.items()):
                print(f"    [{idx:3d}] {palabra}")

        elif opcion == "4":
            print(f"\n  Matriz Documento-Término ({matriz.shape}):")
            print(matriz)

        elif opcion == "5":
            if todas_busquedas:
                exportar_resultados_csv(todas_busquedas)
            else:
                print("  No hay búsquedas realizadas aún.")

        elif opcion == "0":
            print("\n  ¡Hasta luego!")
            if todas_busquedas:
                exportar_resultados_csv(todas_busquedas)
            break

        else:
            print("  Opción no válida.")


def ejecutar_demo():
    """
    Ejecuta una demostración automática con consultas predefinidas.
    Útil para generar todos los datos y gráficos sin interacción.
    """
    buscador, vocabulario, matriz, documentos, etiquetas = \
        inicializar_pipeline()

    # Generar gráficos base
    matriz_sim = generar_graficos(buscador, vocabulario, matriz, etiquetas)

    # Consultas de demostración
    consultas_demo = [
        "inteligencia artificial aprendizaje",
        "seguridad informática redes protección",
        "programación software desarrollo",
        "datos bases consultas información",
        "robots autónomos ingeniería",
    ]

    print("=" * 60)
    print("  DEMOSTRACIÓN — Búsquedas Automáticas")
    print("=" * 60)

    todas_busquedas = []
    for i, consulta in enumerate(consultas_demo, 1):
        resultados = realizar_busqueda(buscador, consulta)
        todas_busquedas.append((consulta, resultados))

        # Gráfico de resultados por búsqueda
        plot_resultados_busqueda(
            resultados, consulta,
            nombre_archivo=f"busqueda_{i}"
        )

    # PCA con la última consulta
    vector_q = buscador.vectorizar_consulta(consultas_demo[0])
    plot_pca_documentos(
        matriz, etiquetas,
        consulta_vector=vector_q,
        consulta_texto=consultas_demo[0]
    )

    # Exportar resultados
    exportar_resultados_csv(todas_busquedas)

    print("\n" + "=" * 60)
    print("  DEMOSTRACIÓN COMPLETADA")
    print(f"  → {len(consultas_demo)} búsquedas realizadas")
    print(f"  → Gráficos en: graficos/")
    print(f"  → Resultados en: resultados/")
    print("=" * 60)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        ejecutar_demo()
    else:
        buscador, vocabulario, matriz, documentos, etiquetas = \
            inicializar_pipeline()
        menu_interactivo(buscador, vocabulario, matriz, etiquetas)

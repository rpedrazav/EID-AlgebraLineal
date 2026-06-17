# Buscador Semántico Simple
**Álgebra Lineal para la Computación — Proyecto 2**  
**Grupo 2:** Rodrigo · Seba · Dani · Renato

---

## ¿Qué hace este proyecto?

Implementa un **buscador semántico basado en álgebra lineal**. Dada una consulta de texto, el sistema recupera y ordena los documentos del corpus según su similitud semántica, usando:

- **Modelo Bag-of-Words (TF)**: cada documento se representa como un vector de frecuencias de términos.
- **Similitud Coseno**: mide el ángulo entre vectores para determinar qué tan similares son dos documentos, independientemente de su longitud.
- **PCA**: reduce los vectores de alta dimensión a 2D para visualizar la distribución del corpus.

---

## Requisitos previos

- Python **3.9 o superior**
- pip (gestor de paquetes de Python)

---

## Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone <url-del-repositorio>
cd EID-AlgebraLineal
```

### 2. (Recomendado) Crear un entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las bibliotecas requeridas son:

| Biblioteca     | Versión  | Uso en el proyecto                          |
|----------------|----------|---------------------------------------------|
| numpy          | ≥1.24    | Vectores, matrices, operaciones de álgebra  |
| matplotlib     | ≥3.7     | Gráficos de barras y scatter plots          |
| seaborn        | ≥0.12    | Heatmap de similitud coseno                 |
| scikit-learn   | ≥1.3     | PCA para reducción dimensional              |
| scipy          | ≥1.11    | Utilidades matemáticas de soporte           |
| pandas         | ≥2.0     | (Opcional) manipulación de resultados CSV   |

---

## Estructura del proyecto

```
EID-AlgebraLineal/
│
├── data/
│   └── documentos/
│       └── corpus.txt          ← Corpus: un documento por línea
│
├── src/
│   ├── __init__.py             ← Exporta todos los módulos
│   ├── preprocesamiento.py     ← Limpieza, tokenización, stopwords
│   ├── vectorizacion.py        ← Vocabulario y Matriz Documento-Término
│   ├── similitud.py            ← Producto punto, norma, similitud coseno
│   ├── buscador.py             ← Clase BuscadorSemantico
│   ├── visualizacion.py        ← Gráficos (heatmap, PCA, barras)
│   └── main.py                 ← Punto de entrada (menú + demo)
│
├── graficos/                   ← PNGs generados automáticamente
├── resultados/                 ← CSV con historial de búsquedas
├── notebooks/                  ← Análisis exploratorio en Jupyter
├── informe/                    ← Documento escrito del proyecto
├── presentacion/               ← Diapositivas de la presentación
├── tareas/                     ← Asignaciones por integrante
│
├── requirements.txt
└── README.md
```

---

## Ejecución

> ⚠️ **Importante:** Todos los comandos deben ejecutarse desde la **carpeta raíz** del proyecto (`EID-AlgebraLineal/`), no desde dentro de `src/`.

### Modo interactivo (menú de terminal)

```bash
python -m src.main
```

Aparecerá un menú con las siguientes opciones:

```
1. Realizar búsqueda          → ingresa una consulta de texto
2. Generar todos los gráficos → heatmap + PCA + frecuencia de términos
3. Ver vocabulario completo   → lista todos los términos indexados
4. Ver matriz documento-término → imprime la matriz numérica
5. Exportar resultados a CSV  → guarda el historial de búsquedas
0. Salir                      → exporta automáticamente y cierra
```

### Modo demo automático (sin interacción)

Ejecuta 5 búsquedas predefinidas, genera todos los gráficos y exporta el CSV:

```bash
python -m src.main --demo
```

Ideal para reproducir los resultados del informe con un solo comando.

---

## Corpus de documentos

El archivo `data/documentos/corpus.txt` contiene **12 documentos** sobre temas de Ciencias de la Computación (una línea = un documento):

| Doc | Tema principal                          |
|-----|-----------------------------------------|
| 1   | Inteligencia Artificial                 |
| 2   | Redes Neuronales Artificiales           |
| 3   | Aprendizaje Automático (Machine Learning)|
| 4   | Ciberseguridad                          |
| 5   | Sistemas Operativos                     |
| 6   | Computación en la Nube                  |
| 7   | Desarrollo de Software                  |
| 8   | Bases de Datos Relacionales             |
| 9   | Programación Orientada a Objetos        |
| 10  | Algoritmos de Búsqueda y Ordenamiento   |
| 11  | Procesamiento del Lenguaje Natural      |
| 12  | Robótica                                |

Para añadir o modificar documentos, edita `corpus.txt` (una oración por línea, sin líneas en blanco entre documentos).

---

## Gráficos generados

Todos los gráficos se guardan automáticamente en la carpeta `graficos/`:

| Archivo                    | Descripción                                               |
|----------------------------|-----------------------------------------------------------|
| `heatmap_similitud.png`    | Mapa de calor de similitud coseno entre todos los docs    |
| `pca_documentos.png`       | Dispersión 2D de documentos reducidos con PCA             |
| `frecuencia_terminos.png`  | Top-15 términos más frecuentes del corpus                 |
| `busqueda_1.png`           | Resultados de la búsqueda 1 (barras horizontales)         |
| `busqueda_N.png`           | Resultados de la búsqueda N                               |

---

## Resultados exportados

Las búsquedas se exportan a `resultados/resultados_busquedas.csv` con el formato:

```
consulta,ranking,documento,similitud
inteligencia artificial aprendizaje,1,Doc 1,0.623450
inteligencia artificial aprendizaje,2,Doc 3,0.541230
...
```

---

## Ejemplo de uso (modo interactivo)

```
============================================================
  BUSCADOR SEMÁNTICO SIMPLE
  Álgebra Lineal para la Computación — Grupo 2
============================================================

[1/4] Cargando documentos...
      → 12 documentos cargados.
[2/4] Preprocesando textos...
      → 145 tokens tras preprocesamiento.
[3/4] Construyendo espacio vectorial...
      → Vocabulario: 98 términos únicos.
      → Matriz Documento-Término: 12 filas × 98 columnas
      → Sparsidad de la matriz: 90.4%
[4/4] Inicializando motor de búsqueda...
      → Motor listo.

  Seleccione opción [0-5]: 1
  Ingrese su consulta: inteligencia artificial aprendizaje

  Consulta: "inteligencia artificial aprendizaje"
  -------------------------------------------------------

  #1 [Doc 3]  Similitud: 0.6804
      ████████████████████
      → El aprendizaje automático es un subcampo de la inteligencia ...

  #2 [Doc 1]  Similitud: 0.5774
      █████████████████
      → La inteligencia artificial es una rama de la informática ...
```

---

## Flujo del pipeline

```
corpus.txt
    │
    ▼
cargar_documentos()          ← src/preprocesamiento.py
    │  Lee líneas del archivo .txt
    ▼
preprocesar_corpus()         ← src/preprocesamiento.py
    │  limpieza → tokenización → remoción de stopwords
    ▼
construir_vocabulario()      ← src/vectorizacion.py
    │  {palabra: índice} ordenado alfabéticamente
    ▼
crear_matriz_doc_termino()   ← src/vectorizacion.py
    │  Matriz m×n de frecuencias (Bag-of-Words)
    ▼
BuscadorSemantico            ← src/buscador.py
    │  vectorizar_consulta() + similitud_coseno() + argsort()
    ▼
Resultados ordenados por similitud coseno
    │
    ├──► Gráficos PNG  (src/visualizacion.py → graficos/)
    └──► CSV de resultados (src/main.py → resultados/)
```

---

## Integrantes y responsabilidades

| Integrante | Rol                                     | Módulo principal       |
|------------|-----------------------------------------|------------------------|
| Seba       | Preprocesamiento y Vectorización        | `preprocesamiento.py`, `vectorizacion.py` |
| Dani       | Similitud y Motor de Búsqueda           | `similitud.py`, `buscador.py` |
| Renato     | Visualización y Análisis Experimental   | `visualizacion.py`     |
| Rodrigo    | Integración, Informe y Presentación     | `main.py`, `README.md` |

---

## Tecnologías utilizadas

- **Python 3.9+** — Lenguaje principal
- **NumPy** — Álgebra lineal: vectores, matrices, producto punto, norma
- **Matplotlib** — Visualización: gráficos de barras y scatter plots
- **Seaborn** — Heatmap de similitud coseno con anotaciones
- **scikit-learn (PCA)** — Reducción dimensional para visualización 2D

---

## Bibliografía básica

- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
- Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press.
- NumPy Documentation: https://numpy.org/doc/
- scikit-learn PCA: https://scikit-learn.org/stable/modules/decomposition.html#pca

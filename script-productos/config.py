"""
config.py

Este módulo define la configuración del sistema:
- Carpetas de entrada y salida
- Columnas por defecto
- Configuración específica por archivo de entrada
"""

# Carpeta donde se encuentran los archivos CSV originales
CARPETA_ENTRADA = "productos_csv"

# Carpeta donde se guardan los archivos procesados (.xlsx)
CARPETA_SALIDA = "resultados"

# Columnas estándar esperadas en el procesamiento
COLUMNAS_DEFAULT = [
    "title",
    "brand",
    "description",
    "final_price",
    "currency",
    "categories",
    "rating"
]

# Configuración de archivos de entrada
# Permite definir columnas personalizadas por archivo
# Si no se define "columnas", se usará COLUMNAS_DEFAULT
CONFIG_ARCHIVOS = [
    {
        "archivo": "amazon-products.csv",
    },
    {
        "archivo": "walmart-products.csv",
        "columnas": [
            "product_name",
            "brand",
            "description",
            "final_price",
            "currency",
            "categories",
            "rating"
        ]
    }
]
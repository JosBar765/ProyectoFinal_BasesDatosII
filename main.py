"""
main.py

Punto de entrada del sistema. Orquesta el flujo completo:
1. Procesa archivos CSV a Excel
2. Extrae categorías válidas
3. Filtra datasets según categorías
4. Valida consistencia de categorías

Ejecuta todo
"""

import os

from config import CONFIG_ARCHIVOS, CARPETA_ENTRADA, CARPETA_SALIDA, COLUMNAS_DEFAULT
from processor import procesar_archivo
from categories import extraer_categorias
from category_filter import filtrar_categorias
from validator import validar_categorias


def procesar_csvs(config_archivos, ruta_entrada_base, ruta_salida_base, columnas_default):
    """
    Procesa múltiples archivos CSV según configuración:

    - Aplica transformación y limpieza
    - Exporta a Excel
    - Retorna lista de archivos generados
    """
    archivos_procesados = []

    for config in config_archivos:
        archivo = config["archivo"]
        columnas = config.get("columnas", columnas_default)

        ruta_entrada = os.path.join(ruta_entrada_base, archivo)

        nombre_base = archivo.replace(".csv", "")
        nombre_salida = f"resultado-{nombre_base}.xlsx"

        ruta_salida = os.path.join(ruta_salida_base, nombre_salida)

        print(f"\n📦 Procesando: {archivo}")
        procesar_archivo(ruta_entrada, columnas, ruta_salida)
        print(f"✅ Listo: {ruta_salida}")

        archivos_procesados.append(nombre_salida)

    return archivos_procesados


def generar_categorias(archivos_procesados, ruta_salida_base):
    """
    Genera archivo de categorías válidas a partir de datasets procesados.
    """
    print("\n🧠 Extrayendo categorías...")

    ruta_categorias = os.path.join(
        ruta_salida_base,
        "resultado-categorias-validas.xlsx"
    )

    extraer_categorias(
        archivos=archivos_procesados,
        ruta_salida=ruta_categorias
    )

    return ruta_categorias


def filtrar_datasets(archivos_procesados, ruta_categorias, ruta_salida_base):
    """
    Filtra las categorías de los datasets usando el listado válido.
    Retorna nombres de archivos filtrados generados.
    """
    print("\n🧹 Filtrando categorías en datasets...")

    filtrar_categorias(
        archivos=archivos_procesados,
        ruta_archivo_categorias=ruta_categorias,
        ruta_salida=ruta_salida_base
    )

    # Genera nombres esperados de salida
    archivos_filtrados = [
        f.replace(".xlsx", "-filtrado.xlsx")
        for f in archivos_procesados
    ]

    return archivos_filtrados


def validar_datasets(ruta_categorias, archivos_filtrados):
    """
    Verifica que los datasets filtrados usen únicamente categorías válidas.
    """
    print("\n🧪 Validando uso de categorías en filtrados...")

    validar_categorias(
        ruta_categorias_validas=ruta_categorias,
        archivos_filtrados=archivos_filtrados
    )


def main():
    """
    Ejecuta el flujo completo del sistema.
    """

    # Define rutas
    ruta_base = os.getcwd()
    ruta_entrada_base = os.path.join(ruta_base, CARPETA_ENTRADA)
    ruta_salida_base = os.path.join(ruta_base, CARPETA_SALIDA)

    # Crea carpeta de salida si no existe
    os.makedirs(ruta_salida_base, exist_ok=True)

    # 1. Procesar CSVs
    archivos_procesados = procesar_csvs(
        CONFIG_ARCHIVOS,
        ruta_entrada_base,
        ruta_salida_base,
        COLUMNAS_DEFAULT
    )

    # 2. Generar categorías válidas
    ruta_categorias = generar_categorias(
        archivos_procesados,
        ruta_salida_base
    )

    # 3. Filtrar datasets
    archivos_filtrados = filtrar_datasets(
        archivos_procesados,
        ruta_categorias,
        ruta_salida_base
    )

    # 4. Validar resultados
    validar_datasets(
        ruta_categorias,
        archivos_filtrados
    )


if __name__ == "__main__":
    main()
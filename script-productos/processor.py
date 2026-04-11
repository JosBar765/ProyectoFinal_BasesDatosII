"""
processor.py

Este módulo se encarga de limpiar y transformar datos de archivos CSV.
Incluye funciones para limpiar precios, textos y estructurar DataFrames
antes de exportarlos a formato Excel.
"""

import pandas as pd
import re


def limpiar_precio(x):
    """
    Intenta convertir un valor a float.
    Retorna None si no es posible.
    """
    try:
        return float(x)
    except:
        return None


def limpiar_texto(texto):
    """
    Limpia texto eliminando emojis y caracteres no permitidos.
    Conserva letras, números y algunos signos básicos.
    """
    if isinstance(texto, str):
        # Elimina emojis
        texto = re.sub(r'[\U0001F600-\U0001FAFF\U00002700-\U000027BF]+', '', texto)
        # Elimina caracteres no deseados
        texto = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ|.,:;()\-\s]', '', texto)
        return texto.strip()
    return texto


def procesar_dataframe(df):
    """
    Aplica limpieza general a un DataFrame:
    - Elimina duplicados
    - Quita comillas en strings
    - Normaliza precios, moneda y descripción si existen
    """
    df = df.drop_duplicates()
    df = df.apply(lambda col: col.map(
        lambda x: x.replace('"', '').replace("'", "") if isinstance(x, str) else x
    ))

    # Limpia columna de precio
    if "final_price" in df.columns:
        df["final_price"] = df["final_price"].apply(limpiar_precio)

    # Normaliza moneda a USD
    if "currency" in df.columns:
        df["currency"] = "USD"

    # Limpia descripción
    if "description" in df.columns:
        df["description"] = df["description"].apply(limpiar_texto)

    return df


def procesar_archivo(ruta_entrada, columnas, ruta_salida):
    """
    Procesa un archivo CSV:
    - Lee el archivo
    - Aplica limpieza general
    - Filtra columnas existentes
    - Exporta a Excel
    """
    df = pd.read_csv(ruta_entrada, encoding="utf-8")

    df = procesar_dataframe(df)

    # Mantiene solo columnas definidas que existan en el archivo
    columnas_existentes = [c for c in columnas if c in df.columns]
    df = df[columnas_existentes]

    df.to_excel(ruta_salida, index=False)
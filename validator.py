"""
validator.py

Este módulo valida que las categorías utilizadas en archivos filtrados
coincidan únicamente con un conjunto de categorías válidas definido en un archivo Excel.
También normaliza categorías (singularización) y extrae categorías únicas desde múltiples archivos.
"""

import pandas as pd
import os
from nltk.stem import WordNetLemmatizer
import nltk
from config import CARPETA_SALIDA

# Descarga silenciosa del recurso necesario para lematización
nltk.download('wordnet', quiet=True)
lemmatizer = WordNetLemmatizer()


def singularizar_categoria(cat):
    """
    Convierte una categoría a su forma base (singular) usando lematización.
    Mantiene formato tipo título.
    """
    palabras = cat.split()
    return " ".join([
        lemmatizer.lemmatize(p.lower()) for p in palabras
    ]).title()


def extraer_categorias_set(archivos):
    """
    Extrae un conjunto único de categorías desde una lista de archivos Excel.

    - Lee la columna 'categories'
    - Limpia formato de listas tipo string
    - Separa por comas y '&'
    - Normaliza cada categoría

    Aplica las mismas reglas que categories.py
    """
    carpeta = CARPETA_SALIDA
    ruta = os.path.join(os.getcwd(), carpeta)
    categorias_set = set()

    for archivo in archivos:
        ruta_archivo = os.path.join(ruta, archivo)

        df = pd.read_excel(ruta_archivo)

        # Ignora archivos sin columna de categorías
        if "categories" not in df.columns:
            continue

        for fila in df["categories"].dropna():
            # Ignora valores no string
            if not isinstance(fila, str):
                continue

            # Limpia formato tipo lista
            fila = fila.replace("[", "").replace("]", "")
            categorias = fila.split(",")

            for cat in categorias:
                cat = cat.strip()
                if not cat:
                    continue

                # Divide subcategorías y normaliza
                for sub in cat.split("&"):
                    sub = singularizar_categoria(sub.strip())
                    categorias_set.add(sub)

    return categorias_set


def validar_categorias(ruta_categorias_validas, archivos_filtrados):
    """
    Valida que todas las categorías usadas en archivos filtrados
    estén dentro del conjunto de categorías válidas.

    Compara:
    categorías usadas ⊆ categorías válidas
    """

    carpeta = CARPETA_SALIDA
    ruta = os.path.join(os.getcwd(), carpeta)

    # Carga categorías válidas desde Excel
    df_validas = pd.read_excel(os.path.join(ruta, ruta_categorias_validas))
    categorias_validas = set(df_validas["categoria"].dropna().astype(str))
    print(f"📦 Categorías válidas: {len(categorias_validas)}")

    # Extrae categorías usadas en archivos filtrados
    categorias_usadas = extraer_categorias_set(archivos_filtrados)
    print(f"📦 Categorías usadas en filtrados: {len(categorias_usadas)}")

    # Detecta categorías inválidas
    no_validas = categorias_usadas - categorias_validas

    print("\n==============================")
    print("📊 RESULTADO VALIDACIÓN")
    print("==============================")

    if len(no_validas) == 0:
        print("✅ OK: Todos los filtrados usan SOLO categorías válidas")
    else:
        print("❌ ERROR: Hay categorías inválidas en filtrados")

        print(f"\n🚨 Categorías inválidas: {len(no_validas)}")
        print("Ejemplos:", list(no_validas)[:10])
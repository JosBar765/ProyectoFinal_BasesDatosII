"""
category_filter.py

Este módulo filtra las categorías de archivos Excel según un conjunto
de categorías permitidas. Normaliza las categorías y elimina aquellas
que no están dentro del listado válido.
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
    palabras_singular = [
        lemmatizer.lemmatize(p.lower()) for p in palabras
    ]
    return " ".join(palabras_singular).title()


def filtrar_categorias(archivos, ruta_archivo_categorias, ruta_salida):
    """
    Filtra las categorías de una lista de archivos Excel:

    - Carga categorías permitidas desde un archivo
    - Normaliza y divide categorías por coma y '&'
    - Conserva solo las categorías válidas
    - Guarda nuevos archivos con sufijo '-filtrado'
    """
    carpeta = CARPETA_SALIDA
    ruta_base = os.path.join(os.getcwd(), carpeta)

    # Carga categorías permitidas desde Excel
    df_cat = pd.read_excel(ruta_archivo_categorias)
    categorias_permitidas = set(df_cat["categoria"].dropna().astype(str))

    print("✅ Categorías permitidas:", len(categorias_permitidas))

    # Procesa cada archivo
    for archivo in archivos:
        ruta_archivo = os.path.join(ruta_base, archivo)
        df = pd.read_excel(ruta_archivo)

        # Verifica existencia de la columna
        if "categories" not in df.columns:
            print(f"❌ {archivo} no tiene columna 'categories'")
            continue

        nuevas_categorias = []

        for fila in df["categories"]:
            # Mantiene valores no string sin cambios
            if not isinstance(fila, str):
                nuevas_categorias.append(fila)
                continue

            # Limpia formato tipo lista
            fila = fila.replace("[", "").replace("]", "")
            categorias = fila.split(",")

            resultado = []

            for cat in categorias:
                cat = cat.strip()

                if not cat:
                    continue

                # Divide subcategorías
                subcats = cat.split("&")

                for sub in subcats:
                    sub = singularizar_categoria(sub.strip())

                    # Agrega solo si es válida y no repetida
                    if sub in categorias_permitidas and sub not in resultado:
                        resultado.append(sub)

            nueva_fila = "[" + ", ".join(resultado) + "]"
            nuevas_categorias.append(nueva_fila)

        df["categories"] = nuevas_categorias

        # Genera nombre de salida
        nombre_salida = archivo.replace(".xlsx", "-filtrado.xlsx")
        ruta_final = os.path.join(ruta_salida, nombre_salida)

        df.to_excel(ruta_final, index=False)

        print(f"✅ Archivo filtrado: {nombre_salida}")
"""
category_mapper.py

Este módulo convierte las categorías en texto de la columna 'categories'
a sus respectivos IDs usando el archivo de categorías válidas.
Sobrescribe los archivos filtrados agregando la columna 'categories_ids'.
"""

import pandas as pd
import os
from config import CARPETA_SALIDA


def mapear_categorias_archivos(archivos_filtrados, ruta_categorias):
    """
    Procesa múltiples archivos filtrados:

    - Lee cada archivo desde carpeta de salida
    - Convierte [cat1, cat2] → [id1, id2]
    - Agrega columna 'categories_ids'
    - Sobrescribe el archivo original
    """

    ruta_base = os.path.join(os.getcwd(), CARPETA_SALIDA)

    # Cargar catálogo de categorías (categoria → id)
    df_cat = pd.read_excel(ruta_categorias)
    mapa = dict(zip(df_cat["categoria"], df_cat["id"]))

    for archivo in archivos_filtrados:
        ruta_archivo = os.path.join(ruta_base, archivo)

        df = pd.read_excel(ruta_archivo)

        if "categories" not in df.columns:
            print(f"❌ {archivo} no tiene columna 'categories'")
            continue

        nuevas_ids = []

        for fila in df["categories"]:
            if not isinstance(fila, str):
                nuevas_ids.append(fila)
                continue

            # Limpia formato tipo lista
            fila = fila.replace("[", "").replace("]", "")
            categorias = fila.split(",")

            ids = []

            for cat in categorias:
                cat_limpia = cat.strip()

                if not cat_limpia:
                    continue

                # Obtiene ID (se asume válida)
                id_cat = mapa.get(cat_limpia)

                if id_cat is not None:
                    ids.append(str(id_cat))

            nueva_fila = "[" + ", ".join(ids) + "]"
            nuevas_ids.append(nueva_fila)

        # Agrega nueva columna al final
        df["categories_ids"] = nuevas_ids

        # Sobrescribe el archivo original
        df.to_excel(ruta_archivo, index=False)

        print(f"✅ IDs agregados en: {archivo}")
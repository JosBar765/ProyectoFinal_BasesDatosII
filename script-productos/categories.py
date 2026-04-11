"""
categories.py

Este módulo extrae, limpia y valida categorías desde archivos Excel.
Aplica normalización (singularización), elimina categorías inválidas
y reduce redundancias (categorías hijas contenidas en otras más generales).
Finalmente guarda un listado único de categorías válidas.
"""

import pandas as pd
import os
from nltk.stem import WordNetLemmatizer
import nltk
import re 
from config import CARPETA_SALIDA

# Descarga silenciosa del recurso necesario para lematización
nltk.download('wordnet', quiet=True)
lemmatizer = WordNetLemmatizer()

# Configuración de categorías inválidas explícitas
BLACKLIST = {
    "2Ds", "3 Piece Patio Dining Set", "7 Piece Patio Dining Set", "9 Drawer Dresser",
    "Accent", "Active", "Novelty", "Rc", "Rv", "Vas"
}


def es_categoria_valida(cat):
    """
    Valida una categoría según reglas básicas:
    - No vacía
    - No incluida en blacklist
    - Evita palabras muy cortas (ej. 'A', 'X')
    - Solo contiene letras, números y espacios
    """
    if not cat:
        return False

    # Filtra blacklist directa
    if cat in BLACKLIST:
        return False

    # Evita términos demasiado cortos
    if len(cat.split()) == 1 and len(cat) <= 2:
        return False

    # Valida caracteres permitidos
    if not re.match(r'^[A-Za-z\d\s]+$', cat):
        return False

    return True


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


def extraer_categorias(archivos, ruta_salida):
    """
    Extrae categorías desde archivos Excel:

    - Limpia y separa categorías
    - Normaliza cada categoría
    - Filtra categorías inválidas
    - Elimina redundancias (subcategorías contenidas)
    - Guarda resultado en Excel
    """
    categorias_set = set()
    categorias_descartadas = set()

    carpeta = CARPETA_SALIDA
    ruta_base = os.path.join(os.getcwd(), carpeta)

    for archivo in archivos:
        ruta_archivo = os.path.join(ruta_base, archivo)

        df = pd.read_excel(ruta_archivo)

        # Verifica existencia de la columna
        if "categories" not in df.columns:
            print(f"❌ {archivo} no tiene columna 'categories'")
            continue

        for fila in df["categories"].dropna():
            if isinstance(fila, str):
                # Limpia formato tipo lista
                fila = fila.replace("[", "").replace("]", "")
                categorias = fila.split(",")

                for cat in categorias:
                    cat_limpia = cat.strip()

                    if not cat_limpia:
                        continue

                    # Divide subcategorías
                    subcategorias = cat_limpia.split("&")

                    for sub in subcategorias:
                        sub_limpia = singularizar_categoria(sub.strip())

                        # Clasifica en válidas o descartadas
                        if es_categoria_valida(sub_limpia):
                            categorias_set.add(sub_limpia)
                        else:
                            categorias_descartadas.add(sub_limpia)

    # Elimina categorías redundantes (ej. "Chair Wood" si existe "Chair")
    categorias_lista = list(categorias_set)
    categorias_set_total = set(categorias_lista)

    categorias_filtradas = []

    for cat in categorias_lista:
        palabras = cat.split()
        eliminar = False

        for i in range(1, len(palabras)):
            posible_base = " ".join(palabras[:i])

            if posible_base in categorias_set_total:
                eliminar = True
                break

        if not eliminar:
            categorias_filtradas.append(cat)

    # Ordena alfabéticamente
    categorias_ordenadas = sorted(categorias_filtradas)

    # Guarda resultado en Excel
    df_resultado = pd.DataFrame({
        "id": range(1, len(categorias_ordenadas) + 1),
        "categoria": categorias_ordenadas
    })
    df_resultado.to_excel(ruta_salida, index=False)

    # Logs de resultado
    print("✅ Categorías guardadas en:", ruta_salida)
    print("📊 Total finales:", len(categorias_ordenadas))
    print("🗑️ Categorías descartadas:", len(categorias_descartadas))
    print("Ejemplo descartadas:", list(categorias_descartadas)[:10])
# 📊 Obtención Masiva de Datos

Estos scripts permiten ejecutar un flujo completo de procesamiento de datos de manera automática.

---

## 🚀 Ejecución

Para ejecutar todo el proceso, simplemente hay que correr:

```bash
python main.py
```

Esto ejecutará todas las etapas del programa de forma secuencial.

---

## 📦 Dependencias

El proyecto utiliza las siguientes librerías:

```python
import pandas as pd
import nltk
```

> [!NOTE]
> Asegurate de tener instaladas las dependencias antes de ejecutar el programa. 

En caso de no tenerlas instaladas, se puden instalar usando `pip`:

```bash
pip install pandas nltk
```

---

## 📁 Estructura de archivos

- 📂 **productos_csv/**  
  Contiene los *datasets* originales.

- 📂 **resultados/**  
  Almacena los archivos procesados.

---

## 🧠 Detalles del código

- Todos los archivos `.py` están comentados para facilitar su comprensión.
- El flujo del programa está centralizado en `main.py`.
- En la salida de consola se pueden verificar las categorías luego de ser filtradas.
- Los archivos que deben utilizarse para la base de datos son aquellos que contienen el sufijo:
  
  ```text
  -filtrado.xlsx
  ```
    Se encuentran 📂**resultados/**

---

## ⚙️ Configuración

> [!IMPORTANT]
> Cualquier cambio en la estructura del proyecto debe realizarse en el archivo `config.py`.

> [!IMPORTANT]
> Siempre mantener como primer columna el nombre del producto.

Podés modificar:

- Nombre o rutas de las carpetas
- Agregar o quitar archivos `.csv`
- Definir columnas personalizadas para algún archivo `.csv`
- Definir el orden de las columnas

---

## 🛠️ Solución de Problemas

> [!WARNING]
> Si ocurre algún error durante la ejecución, podés guiarte con los siguientes casos comunes:

### 🔹 Errores durante el procesamiento de archivos `.csv`

- Verificá el archivo `config.py`
- Asegurate de que:
  - Las rutas de las carpetas estén bien definidas
  - Los nombres de las columnas existan y coincidan exactamente con los archivos

---

### 🔹 Errores en la identificación de categorías

- Verificá que exista la columna:

```text
categories
```

- Esta columna debe estar presente en los archivos generados por el procesador

---

### 🔹 Errores durante el filtrado de archivos

- Puede deberse a:
  - Nombres de archivos incorrectos
  - Archivos inexistentes
  - Falta de la columna `categories` en los archivos

---

### 🔹 Errores en la validación de resultados

- Modificá el archivo `categories.py`
- Agregá las categorías problemáticas en la variable:

```python
BLACKLIST
```

---

## 📝 Notas

> [!NOTE]
> Si todo el proceso se ejecuta correctamente, los archivos intermedios/auxiliares serán eliminados automáticamente.

> [!NOTE]
> En caso de error, estos archivos se conservarán en la carpeta de destino definida en `config.py`, lo cual permite su análisis para fines de depuración.

> [!NOTE]
> Asegurarse de mantener la estructura de carpetas para evitar errores durante la ejecución.

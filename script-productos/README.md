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

Podés modificar:

- Nombre o rutas de las carpetas
- Agregar o quitar archivos `.csv`
- Definir columnas personalizadas para algún archivo `.csv`

---

## 📝 Notas

> [!TIP]
> Asegurarse de mantener la estructura de carpetas para evitar errores durante la ejecución.

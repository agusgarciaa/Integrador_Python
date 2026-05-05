# Seminario de Lenguajes - Python 🐍
---
## Trabajo Integrador 2026
Este proyecto corresponde al Trabajo Integrador de la materia Seminario de Lenguajes, utilizando Python como lenguaje principal.

## 📖 Descripción
Desarrollo de una aplicación en Python para analizar y visualizar datos de biodiversidad (Darwin Core), incluyendo limpieza de datos e interfaz gráfica con Streamlit.

## 🛠️ Tecnologías
- Python (v3.13.x)
- Streamlit
- Jupyter Notebook 

--- 
## 📁 Estructura del Proyecto

- `documentation/`: Contiene la documentación de los tres datasets utilizados en el proyecto.
- `notebooks/`: Contiene los archivos `.ipynb` con los ejercicios de análisis y limpieza de datos de los datasets.
- `src/`: Código fuente adicional y módulos auxiliares.
- `raw_datasets/`: Directorios para los datos crudos. 
`processed_datasets/`: Directorios para los datos procesados.
- `Inicio.py`: Archivo principal para la ejecución de la aplicación web Streamlit.
- `pages/`: Páginas secundarias de la aplicación Streamlit.
- `logs/`: Contiene el archivo `operations.log` con el registro de las operaciones de los datasets.

#### - Para el correcto funcionamiento de las rutas, es necesario organizar los archivos de la siguiente manera:

1. Datos Crudos (raw_datasets/)
Debes crear manualmente estas carpetas (iadiza, xenocanto e inaturalist) y colocar los archivos originales en su interior:

- `raw_datasets/iadiza/`
- `raw_datasets/xenocanto/`
- `raw_datasets/inaturalist/`

2. Datos Procesados (processed_datasets/)
Igual que en raw_datasets/, deben existir las carpetas de destino (iadiza, xenocanto e inaturalist), el archivo final se crea solo al ejecutar el código:

- `processed_datasets/iadiza/`
- `processed_datasets/xenocanto/`
- `processed_datasets/inaturalist/`


---

## ⚙️ Requisitos Previos

Antes de descargar y ejecutar el proyecto, es necesario tener instalado:

* [Visual Studio Code](https://code.visualstudio.com/)
* Python **3.13.x** (Podés comprobar tu versión ejecutando `python --version` en la terminal).
* Extensión **Python** para VS Code.
* Extensión **Jupyter** para VS Code.

> **Nota:** Al abrir un notebook (`.ipynb`) en VS Code, normalmente el editor detecta si faltan extensiones o dependencias relacionadas con Jupyter/Python y suele sugerir su instalación automáticamente.

---

## 🚀 Guía de Configuración e Instalación

Seguí estos pasos en tu terminal para configurar el proyecto localmente en tu computadora:

### 1. Clonar el repositorio
Descargá el proyecto en tu máquina local y accedé a la carpeta principal:

        git clone https://gitlab.catedras.linti.unlp.edu.ar/python-2026/proyectos/grupo04/code.git

Accedé a la carpeta principal:

        cd code
### 2. Crear el entorno virtual (VENV)
Para mantener las librerías del proyecto aisladas y no interferir con tu sistema, creá un entorno virtual ejecutando:

        python -m venv .venv

### 3. Activar el entorno
Para comenzar a usar el entorno, debés activarlo. Según tu sistema operativo, utilizá el comando correspondiente:

        Windows: .venv\Scripts\activate

        Mac/Linux: source .venv/bin/activate

(Nota: Te vas a dar cuenta de que el entorno está activo porque vas a ver el prefijo (.venv) al inicio de la línea en tu terminal).

### 4. Instalar las dependencias
Con el entorno activado, procedé a instalar Streamlit, Jupyter y las demás librerías necesarias para que el proyecto funcione:

        pip install -r requirements.txt



## ▶️ Cómo Ejecutar el Código
Una vez configurado el entorno, podés ejecutar las distintas partes del proyecto según lo que necesites revisar:

### Ejecutar los Notebooks en VS Code:
Para correr los ejercicios de análisis, tomaremos como ejemplo el notebook iadiza.ipynb:

1. Abrir la carpeta: Abrí la carpeta principal del proyecto en VS Code.

2. Abrir el archivo: En el panel lateral, navegá hacia la carpeta notebooks/ y abrí el notebook deseado (ejemplo: notebooks/iadiza.ipynb).

3. Seleccionar el intérprete: En la esquina superior derecha o mediante la paleta de comandos (Ctrl+Shift+P -> Python: Select Interpreter), seleccioná el intérprete de Python de tu entorno virtual (.venv).

4. Seleccionar el kernel: Asegurate de que el kernel de Jupyter seleccionado coincida con el intérprete de tu entorno.

5. Ejecutar: Ejecutá las celdas del notebook normalmente utilizando el botón de "Play" al lado de cada celda o con el atajo Shift + Enter.

### Ejecutar la Aplicación Web (Streamlit)
Dado que la interfaz gráfica está desarrollada con Streamlit, el proyecto se inicia con un comando específico en lugar del habitual de Python. En la terminal, con el entorno activado, ejecutá:

        streamlit run Inicio.py

## 👥 Grupo 4
- Agustin Garcia
- Ana Freitas
- Fe Sofia Cordoba
- Lucia Cipolla
- Sofia Martins
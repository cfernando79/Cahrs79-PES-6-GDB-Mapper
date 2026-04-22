# Cahrs79 PES 6 GDB Mapper

Aplicación con interfaz gráfica para leer y visualizar los datos de un archivo de opciones (Option File) de **Pro Evolution Soccer 6** (versión PC).  
Muestra la lista de jugadores con su ID, nombre, nacionalidad y club, y permite filtrar la tabla por cualquiera de estos campos.

## ✨ Características

- Carga y descifra automáticamente el archivo `KONAMI-WIN32PES6OPT` (sin extensión).
- Detecta las plantillas de los clubes sin necesidad de conocer nombres de equipos ni IDs de jugadores específicos.
- Interfaz con tabla ordenable y barras de desplazamiento.
- Filtro en tiempo real por ID, nombre, nacionalidad o club (EN PROCESO DE MEJORAR, NO CARGA CORRECTAMENTE).

## 🖥️ Requisitos

- Python 3.6 o superior.
- Tkinter (incluido por defecto en Windows).
- Ninguna biblioteca externa adicional.

## 📥 Instalación y ejecución

1. **Clona o descarga** este repositorio.
2. Abre una terminal en la carpeta del proyecto y ejecuta:
   ```bash
   python main.py

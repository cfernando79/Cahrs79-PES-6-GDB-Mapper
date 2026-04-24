# Cahrs79 PES 6 GDB Mapper

Aplicación con interfaz gráfica para leer y visualizar los datos de un archivo de opciones (Option File) de **Pro Evolution Soccer 6** (versión PC).  
Muestra la lista de jugadores con su ID, nombre, nacionalidad y club, y permite filtrar la tabla por cualquiera de estos campos.

## ✨ Características

- Carga y descifra automáticamente el archivo `KONAMI-WIN32PES6OPT` (sin extensión).
- Detecta las plantillas de los clubes sin necesidad de conocer nombres de equipos ni IDs de jugadores específicos.
- Interfaz con tabla ordenable y barras de desplazamiento.
- Filtro en tiempo real por ID, nombre, nacionalidad o club.

## 🖥️ Requisitos

- Python 3.6 o superior.
- Tkinter (incluido por defecto en Windows).
- Ninguna biblioteca externa adicional.

## 📥 Instalación y ejecución

1. **Clona o descarga** este repositorio.
2. Abre una terminal en la carpeta del proyecto y ejecuta:
   ```bash
   python main.py
## 🕹️ Uso

1. Haz clic en **"Load Option File"**.
2. Selecciona tu archivo `KONAMI-WIN32PES6OPT` (sin extensión). Normalmente se encuentra en `Mis Documentos\KONAMI\Pro Evolution Soccer 6\save\folder1\`.
3. La tabla se llenará con todos los jugadores del juego.
4. Usa el campo de filtro y elige la columna para buscar rápidamente.

## 🛠️ Estructura del proyecto (modular)

Cahrs79-PES-6-GDB-Mapper/

├── constants.py       # Constantes del OF (bloques, claves, offsets)

├── optionfile.py      # Clase para cargar y descifrar el archivo

├── club_db.py         # Lectura de nombres de clubes

├── player.py          # Clase que representa a un jugador

├── player_db.py       # Carga de todos los jugadores y mapeo de clubes

├── gui.py             # Interfaz gráfica (Tkinter)

├── main.py            # Punto de entrada

└── README.md          # Este archivo

## 📝 Notas importantes

- El programa funciona con **archivos de PC** (no PS2). Aunque el método de detección de plantillas es genérico y debería funcionar también con versiones de PS2, no ha sido probado.
- Los nombres de los clubes y las nacionalidades se muestran en inglés (idioma original del Option File).
- Si el programa no detecta correctamente las plantillas, se mostrará "Free Agent" para todos los jugadores. En ese caso, ajusta manualmente los parámetros en `squad_detector.py`.

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **GNU General Public License v3.0** (en honor al editor original PES Editor 6 de Compulsion). Ver archivo `LICENSE` (puedes añadirlo después).

## 🙏 Agradecimientos

- Código basado en el trabajo de **Compulsion** (PES Editor 6) y **lazanet** (versiones posteriores).
- Inspirado en la comunidad de editores de PES 6.

---

¡Disfruta editando y explorando tu Option File!

# Py-autocad-geotransformer

**Py-autocad-geotransformer** es una herramienta de escritorio diseñada para automatizar la extracción y conversión de coordenadas directamente desde **AutoCAD** (de UTM a grados decimales). El proyecto es de código abierto, lo que permite editar la lógica según sea necesario y recompilar la aplicación; para facilitar esto, he incluido el comando de compilación detallado como un comentario al final del archivo `convertidor.py`.

Esta aplicación detecta en tiempo real los objetos seleccionados en el dibujo y convierte sus coordenadas **UTM (WGS84)** a **Grados Decimales** y formato **GMS** (Grados, Minutos y Segundos) de forma instantánea.

> **Advertencia de Instancia Única:** > El programa está diseñado para interactuar con la instancia activa de AutoCAD. Actualmente, **no detecta múltiples procesos simultáneos de AutoCAD** (varias sesiones de programa abiertas al mismo tiempo). Sin embargo, funciona con total normalidad en una sola sesión que contenga **múltiples ventanas y diferentes planos abiertos** (MDI - Multiple Document Interface).

## Características

- **Sincronización en tiempo real:** Lee automáticamente los objetos seleccionados (bloques, puntos, etc.) sin comandos adicionales.
- **Sin Dependencias:** Versión compilada en `.exe`, no requiere instalación de Python ni librerías externas.
- **Conversión Geodésica:** Transformación precisa basada en la librería `PyProj` (EPSG:32718 por defecto para Lima/Perú).
- **Formato Profesional:** Salida de datos con orientación cardinal (N/S, E/W) ideal para informes topográficos.

## Requisitos de Sistema

- **Sistema Operativo:** Windows 10 / 11.
- **Software Base:** AutoCAD (debe estar abierto y con un dibujo activo).
- **Permisos:** Ejecutar como administrador si AutoCAD tiene privilegios elevados.

## Cómo usar (Versión Portable)

1. Descarga el archivo `AutoCAD_GeoDetector.exe` desde la sección de **Releases** (o la carpeta `dist`).
2. Abre tu plano en **AutoCAD**.
3. Ejecuta el programa.
4. Selecciona cualquier objeto con punto de inserción en el CAD.
5. Los resultados aparecerán automáticamente en la ventana de la app:
   - **UTM:** Este (E), Norte (N).
   - **DEC:** Latitud, Longitud decimal.
   - **GMS:** `12°30'45.22" S, 77°01'15.05" W`.

## Desarrollo Técnico

Aunque se distribuye como ejecutable, el core del proyecto fue desarrollado con:

- **Python + Tkinter** (Interfaz gráfica).
- **PyWin32** (Interacción con la API COM de AutoCAD).
- **PyProj** (Cálculos de geodesia y transformación de coordenadas).

## 👤 Autor

**Jesús Martín Bautista Ramírez** Bachiller de Ingeniería Civil - UPC  
_Especialista en automatización de procesos de ingeniería y soluciones tecnológicas._

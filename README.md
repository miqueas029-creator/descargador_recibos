# Descargador de recibos

Automatización en Python que descarga recibos de donaciones mensuales desde un sistema contable web, los cruza con una planilla de donantes y guarda cada recibo en PDF.

## Qué hace

1. Inicia sesión en el sistema contable con Playwright (navegador automatizado).
2. Abre el informe de libro mayor y lee todos los recibos de la grilla, que carga de a pocos mientras se hace scroll.
3. Lee desde Google Sheets la lista de donantes mensuales y su monto.
4. Cruza ambas tablas con pandas, por ID de organización y monto.
5. Descarga el PDF de cada recibo que coincide.
6. Guarda un historial para no descargar dos veces el mismo recibo.
7. Genera un listado de los donantes sin coincidencia, indicando el motivo.

## Tecnologías

Python, Playwright, pandas, python-dotenv.

## Cómo usarlo

1. Instalar las dependencias: `pip install playwright pandas python-dotenv`
2. Copiar `.env.example` como `.env` y completar los valores.
3. Ejecutar `python scripts/main.py`

## Estado del proyecto

En desarrollo. Falta terminar el módulo que mueve los PDF descargados a la carpeta de cada donante.

## Nota

Este repositorio no incluye datos reales: las credenciales, los recibos y la lista de donantes quedan fuera con `.gitignore`.
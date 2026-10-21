import sys
import os
import time
import pandas as pd

# Añade la carpeta raíz del proyecto al sistema de rutas de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.login import login
from src.libro_mayor import libro_mayor
from src.leer_recibos import obtener_todos_los_recibos
from src.historial import cargar_historial, guardar_estado
from src.leer_gloogle_sheets import leer_sheet
from src.preparar_df import mergeador
from src.descargar_recibos import descargar_recibo
from src.mover_archivos import mover_archivos

p, page, context = login()

frame = libro_mayor(page)

recibos = obtener_todos_los_recibos(frame)

coincidencias = mergeador(recibos) #mergeo con los donantes que tenemos y el monto que donan
historial = cargar_historial()

for _, recibo in coincidencias.iterrows():

    transaccionid = str(recibo["transaccionid"])

    if transaccionid in historial:
        print("Ya descargado, salteo:", recibo["Donante"])
        continue

    descargar_recibo(page, context, recibo)
    guardar_estado(historial, transaccionid, "descargado")
    
context.close()
p.stop()

# mover_archivos

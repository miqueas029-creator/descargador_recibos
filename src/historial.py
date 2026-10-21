import json
import os

ARCHIVO = "historial.json"

def cargar_historial():
    if not os.path.exists(ARCHIVO):
        return {}
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_estado(historial, transaccionid, estado):
    historial[transaccionid] = estado
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)



import pandas as pd
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Añade la carpeta raíz del proyecto al sistema de rutas de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.leer_gloogle_sheets import leer_sheet

def mergeador(recibos):
    
    finnegans = pd.DataFrame(recibos)
    finnegans.to_csv('prueba.csv', index=False)

    #Aseguramos que sea texto, reemplazamos la coma por punto y después lo convertimos a número
    finnegans["Monto"] = pd.to_numeric(
        finnegans["haber_ppal"].astype(str).str.replace(",", "."),
        errors="coerce"
    )

    donantes = leer_sheet(
        sheet_id=os.getenv("SHEET_ID"),
        gid=os.getenv("SHEET_GID")
)
    donantes = donantes.dropna(subset=["Monto actual"])
    donantes["Monto"] = (donantes["Monto actual"].astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", "", regex=False)
    )
    
    donantes["Monto"] = pd.to_numeric( donantes["Monto"], errors="coerce").astype("Int64")
    finnegans["Monto"] = finnegans["Monto"].round(0).astype("int64")

    finnegans["organizacionid"] = pd.to_numeric(finnegans["organizacionid"], errors="coerce").astype("Int64")
    donantes["organizacionid"] = pd.to_numeric(donantes["organizacionid"], errors="coerce").astype("Int64")

    coincidencias = finnegans.merge(
        donantes,
        on=["organizacionid",
            "Monto"],
        how="inner"
    )

    coincidencias["fecha"] = pd.to_datetime(coincidencias["fecha"], format="%d/%m/%Y", errors="coerce")

    # Donantes del Sheet que NO tuvieron coincidencia
    ids_con_coincidencia = coincidencias["organizacionid"].unique()
    no_encontrados = donantes[~donantes["organizacionid"].isin(ids_con_coincidencia)].copy()

    # ¿Su organizacionid aparece al menos en algún recibo?
    ids_en_recibos = finnegans["organizacionid"].unique()
    no_encontrados["motivo"] = no_encontrados["organizacionid"].apply(
        lambda x: "Pagó, pero con otro monto" if x in ids_en_recibos else "No aparece en los recibos"
    )

    no_encontrados.to_csv("no_encontrados.csv", index=False)
    
    return coincidencias
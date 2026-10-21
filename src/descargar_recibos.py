import os
import random
import datetime
from src.leer_datos_recibos import frame_con, leer_datos_recibo

LINKS = "div[column='3'] div.webix_cell a"


def descargar_recibo(page, context, recibo):
    print("Voy a procesar:", recibo["Donante"])

    # Abrir el recibo
    frame_grilla = frame_con(page, LINKS)
    frame_grilla.evaluate(
        "(onclick) => { new Function(onclick)(); }",
        recibo["onclick"]
    )

    frame_recibo = frame_con(page, "div[name='wdg_Organizacion'] input")
    datos = leer_datos_recibo(frame_recibo)

    frame_recibo.locator("#toolbarContainerSuperior a#close").click(force=True)

    # Abrir menú de impresión y tildar el casillero
    frame_recibo.locator("#_onPrint").evaluate("el => el.click()")
    popup = frame_recibo.locator("#overDivPrint")
    fila = popup.locator("tr.gridRow", has_text="Recibo Simple UTDT")

    page.wait_for_timeout((random.uniform(1, 3) * 1000))
    fila.locator("img").first.evaluate("el => el.click()")
    page.wait_for_timeout((random.uniform(1, 3) * 1000))

    # Previsualizar (abre pestaña nueva) y guardar el PDF
    with context.expect_page() as nueva:
        frame_recibo.locator("a.WIDGETWidgetButton", has_text="Previsualizar").evaluate("el => el.click()")
    pestana = nueva.value
    pestana.wait_for_load_state()    

    os.makedirs("recibos", exist_ok=True)
    respuesta = context.request.get(pestana.url)

    nombre_archivo = f"recibos/{str(recibo["fecha"].month)+" - Recibo UTDT - "+recibo["nombre_finnegans"]}.pdf"
    with open(nombre_archivo, "wb") as f:
        f.write(respuesta.body())
    print("Guardado:", nombre_archivo)
    pestana.close()

    # Cerrar popup y recibo
    popup.locator("a.WIDGETWidgetButton", has_text="Cerrar").evaluate("el => el.click()")
    popup.wait_for(state="hidden")
    frame_recibo.locator("#toolbarContainerSuperior a#close").click(force=True)

    page.wait_for_timeout((random.uniform(1, 3) * 1000))
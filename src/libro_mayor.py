from playwright.sync_api import sync_playwright
import time
import random
from datetime import datetime

def libro_mayor(page):

    page.wait_for_timeout((random.uniform(2, 7) * 1000))
    page.locator("i.fas.fa-bars").wait_for()
    menu = page.locator("i.fas.fa-bars")
    menu.click()

    page.get_by_text("Informes", exact=True).click()

    page.wait_for_timeout((random.uniform(4, 7) * 1000))

    contabilidad = page.get_by_label("Informes").get_by_text("Contabilidad")
    contabilidad.hover()

    page.wait_for_timeout((random.uniform(3, 5) * 1000))

    libro_mayor = page.locator("label.category-option-label", has_text="Libro Mayor UTDT Donación con Pedido")
    libro_mayor.click()

    page.wait_for_timeout((random.uniform(5, 7) * 1000))

    # Esperamos que cargue el iframe
    frame = next(f for f in page.frames if "appItem.jsp" in f.url)

    # Fecha del primer día del mes actual
    hoy = datetime.today()

    page.wait_for_timeout((random.uniform(1, 4) * 1000))


    dia = "01"
    mes = f"{hoy.month:02d}"
    anio = str(hoy.year)

    page.wait_for_timeout((random.uniform(2, 7) * 1000))

    # Fecha Desde
    fecha_desde = frame.locator("div.widgetDate").first
    page.wait_for_timeout((random.uniform(1, 3) * 1000))
    fecha_desde.locator("input[name='day']").fill(dia)
    fecha_desde.locator("input[name='month']").fill(mes)
    fecha_desde.locator("input[name='year']").fill(anio)

    aceptar = frame.locator("#hightlighted")
    aceptar.wait_for(state="visible")
    aceptar.evaluate("el => el.click()")

    frame.wait_for_timeout((random.uniform(1, 3) * 1000))

    return frame
import time

def frame_con(page, selector, timeout=15_000):
    limite = time.time() + timeout / 1000
    while time.time() < limite:
        for frame in page.frames:
            try:
                if frame.locator(selector).count() > 0:
                    return frame
            except Exception:
                pass
        page.wait_for_timeout(200)
    raise TimeoutError(f"No se encontró frame con selector: {selector}")


def parser(texto):
    texto = texto.strip()
    # Formato con comas de miles: "191,940,000.00" -> quitar comas
    texto = texto.replace(",", "")
    return float(texto)


def leer_datos_recibo(frame, timeout=20_000, debug=True):
    org_input = frame.locator("div[name='wdg_Organizacion'] input")
    org_input.wait_for(state="visible", timeout=timeout)
    nombre = org_input.input_value()

    monto = None

    monto_locator = frame.locator("div[name='wdg_Monto'] input")
    try:
        monto_locator.wait_for(state="visible", timeout=3000)
        monto = parser(monto_locator.input_value())
    except Exception as e:
        if debug:
            print(f"   (wdg_Monto no encontrado: {type(e).__name__})")

    if monto is None:
        importe_locator = frame.locator("div[name='wdg_ImporteTotal'] input")
        try:
            count = importe_locator.count()
            if debug:
                print(f"   (wdg_ImporteTotal count={count})")
            importe_locator.first.wait_for(state="visible", timeout=5000)
            monto = parser(importe_locator.first.input_value())
        except Exception as e:
            print(f"⚠️ No se encontró monto para '{nombre}' — motivo: {type(e).__name__}: {e}")
            # Guardamos evidencia para inspeccionar qué pasó
            try:
                frame.page.screenshot(path=f"debug_{nombre[:20]}.png")
                with open(f"debug_{nombre[:20]}.html", "w", encoding="utf-8") as f:
                    f.write(frame.content())
            except Exception:
                pass

    return {
        "nombre": nombre,
        "monto": monto
    }
import re
import random

JS_LEER_VISIBLES = """
() => {
    const cols = {};
    document.querySelectorAll('.webix_ss_center_scroll > div.webix_column').forEach(c => {
        cols[c.getAttribute('column')] = Array.from(c.querySelectorAll('.webix_cell'));
    });
    const n = cols['0'] ? cols['0'].length : 0;
    const txt = (k, i) => (cols[k] && cols[k][i]) ? cols[k][i].innerText.trim() : '';
    const filas = [];
    for (let i = 0; i < n; i++) {
        const a = cols['3'] && cols['3'][i] ? cols['3'][i].querySelector('a') : null;
        filas.push({
            indice: i, // <--- GUARDAMOS EL ÍNDICE
            fecha: txt('0', i),
            transaccionid: txt('1', i),
            tipodoc: txt('2', i),
            documento: txt('3', i),
            organizacionid: txt('4', i),
            comprobante: txt('6', i),
            moneda: txt('7', i),
            haber_ppal: txt('8', i),
            haber_sec: txt('9', i),
            documento_pedido: txt('10', i),
            onclick: a ? a.getAttribute('onclick') : null,
        });
    }
    return filas;
}
"""

JS_SCROLL = """
(dy) => {
    const el = document.querySelector('.webix_ss_vscroll');
    const antes = el.scrollTop;
    el.scrollTop = antes + dy;
    return [antes, el.scrollTop];
}
"""


def obtener_todos_los_recibos(frame, timeout=((random.uniform(1, 3) * 1000)), paso=200):
    frame.wait_for_selector("div[column='3'] div.webix_cell a", timeout=timeout)

    # Total esperado: "122 registros encontrados."
    texto = frame.get_by_text(re.compile(r"\d+\s+registros encontrados")).first.inner_text()
    total = int(re.search(r"(\d+)", texto).group(1))
    print(f"Total esperado: {total}")

    recibos = {}
    sin_avance = 0

    while len(recibos) < total and sin_avance < 5:
        for fila in frame.evaluate(JS_LEER_VISIBLES):
            if fila["transaccionid"]:
                recibos.setdefault(fila["transaccionid"], fila)

        antes, despues = frame.evaluate(JS_SCROLL, paso)
        frame.wait_for_timeout(300)

        # Si no se pudo bajar más, contamos intentos para no quedar en loop infinito
        sin_avance = sin_avance + 1 if despues == antes else 0

    # Última lectura, por si la última tanda quedó sin leer
    for fila in frame.evaluate(JS_LEER_VISIBLES):
        if fila["transaccionid"]:
            recibos.setdefault(fila["transaccionid"], fila)

    print(f"Encontré {len(recibos)} de {total} recibos.")
    return list(recibos.values())
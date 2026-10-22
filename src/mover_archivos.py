import os
import re
import shutil
from dotenv import load_dotenv
load_dotenv(override=True)

def mover_archivos():
    origen = "recibos"
    destino = os.getenv("CARPETA_DESTINO")
    
    carpetas_personas = [
    nombre for nombre in os.listdir(destino)
    if os.path.isdir(os.path.join(destino, nombre))
    ]
    
    movidos, errores = 0, []
    archivos = [f for f in os.listdir(origen) if os.path.isfile(os.path.join(origen, f))]
    for archivo in sorted(archivos):
        persona = extraer_nombre_persona(archivo)
        carpeta = encontrar_carpeta_destino(persona, carpetas_personas)

        if not carpeta:
            errores.append(archivo)
            continue

        origen_path  = os.path.join(origen, archivo)
        destino_path = os.path.join(destino, carpeta, archivo)

        # Si ya existe un archivo con ese nombre, agrega un sufijo
        if os.path.exists(destino_path):
            base, ext = os.path.splitext(archivo)
            destino_path = os.path.join(destino, carpeta, f"{base}_duplicado{ext}")

        shutil.move(origen_path, destino_path)
        print(f"  ✅ Movido: {archivo}")
        movidos += 1

    print(f"\n{'='*60}")
    print(f"✅ Archivos movidos: {movidos}")
    if errores:
        print(f"❌ Sin destino ({len(errores)}):")
        for e in errores:
            print(f"   - {e}")

def extraer_nombre_persona(nombre_archivo):
    """Extrae la parte del nombre"""
    
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
    # Busca el patrón: dígito(s) - Recibo UTDT - NOMBRE
    patron = r'^\d+\s*-\s*Recibo UTDT\s*-\s*(.+)$'
    match = re.match(patron, nombre_sin_ext, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def encontrar_carpeta_destino(nombre_persona, carpetas):
    """ Busca la carpeta cuyo nombre coincide exactamente con el nombre extraído."""

    if not nombre_persona:
        return None

    # 1. Coincidencia exacta (sin importar mayúsculas ni puntos finales)
    nombre_buscado = nombre_persona.strip().rstrip(".").lower()
    for carpeta in carpetas:
        if carpeta.strip().rstrip(".").lower() == nombre_buscado:
            return carpeta

    return None
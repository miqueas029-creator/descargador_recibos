import os
import re
from dotenv import load_dotenv
load_dotenv()

def mover_archivos():
    origen = "recibos"
    destino = os.getenv("CARPETA_DESTINO")

    carpetas_personas = [
    nombre for nombre in os.listdir(destino)
    if os.path.isdir(os.path.join(destino, nombre))
    ]

def extraer_nombre_persona(nombre_archivo):
    """Extrae la parte del nombre"""
    
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
    # Busca el patrón: dígito(s) - Recibo UTDT - NOMBRE
    patron = r'^\d+\s*-\s*Recibo UTDT\s*-\s*(.+)$'
    match = re.match(patron, nombre_sin_ext, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
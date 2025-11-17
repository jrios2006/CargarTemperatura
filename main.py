#!/usr/bin/env python3
"""
Programa principal para lectura de sensores TEMPer y registro de datos en un log rotativo.

- Lee sensores TEMPer usando `temper_reader.get_medicion()`.
- Registra la información en un log rotativo para no saturar el disco.
- Imprime por consola los resultados.
"""

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from module.temper_reader import get_medicion
from module.system_info import get_system_info
from module.location_info import get_location_data  
from module.json_builder import insert_into_db


# Configuración del log rotativo
LOG_FILE = "temperatura.log"
MAX_BYTES = 1_000_000  # 1 MB por archivo
BACKUP_COUNT = 2       # Mantener hasta 5 archivos antiguos

logger = logging.getLogger("TemperLogger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    """Función principal que lee sensores y guarda la información en el log."""
    try:
        # 1️ Información del sistema
        system = get_system_info(use_dynamic_ip=True)

        # 2️ Información de ubicación y offset
        location = get_location_data("config/config.json")
        offset = location["offset_celsius"]

        # 3️ Lectura de sensores TEMPer usando el offset
        mediciones = get_medicion(offset_celsius=offset)

        if not mediciones:
            #print("No se detectaron sensores TEMPer.")
            logger.warning("No se detectaron sensores TEMPer.")
            return

        for sensor in mediciones:
            temp = sensor["temperature_c"]
            metadata = sensor["metadata"]

            # Construir payload (opcional)
            payload = {
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre_sensor": metadata.get("product", "Desconocido"),
                "numero_serie": metadata.get("serial_number"),
                "ubicacion": location["ubicacion"],
                "hostname_maquina": system["hostname"],
                "ip_maquina": system["ip_maquina"],
                "id_maquina": system["id_maquina"],
                "temperatura": round(temp, 2),
                "humedad": None,
                "bateria": None,
                "cpd": location["cpd"],
                "sala": location["sala"]
            }

            #msg = f"{payload['nombre_sensor']} (SN: {payload['numero_serie']}): {payload['temperatura']:.2f}°C"
            #logger.info(msg)
            logger.info(payload)

            success = insert_into_db(payload)

            if success:
                logger.info(f"Payload insertado en DB: {payload['nombre_sensor']} | {payload['temperatura']:.2f}°C")
            else:
                logger.error(f"Error al insertar en DB: {payload['nombre_sensor']}")

    except Exception as e:
        logger.error(f"Error al leer sensores: {e}")


if __name__ == "__main__":
    main()

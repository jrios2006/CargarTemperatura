# module/temper_reader.py
#!/usr/bin/env python3
"""
Módulo para lectura de sensores USB TEMPer.

Este módulo utiliza la librería `temperusb` y `pyusb` para detectar dispositivos
TEMPer conectados al sistema, extraer su metadata USB y obtener la temperatura
medida por cada uno.

Funciones principales:
- get_device_metadata(): Obtiene información del dispositivo USB.
- get_medicion(): Lee temperatura de todos los dispositivos TEMPer detectados.
"""

import json
from temperusb import TemperHandler
import usb.core
import usb.util


def get_device_metadata(device) -> dict:
    """Obtiene la metadata del dispositivo USB TEMPer.

    Esta función inspecciona el descriptor USB para extraer:
    - Vendor ID
    - Product ID
    - Manufacturer
    - Product Description
    - Serial Number

    Algunas versiones del driver de `temperusb` no exponen el atributo interno
    `_device`, por lo que se manejan errores y se devuelven campos en `None` cuando
    no es posible obtenerlos.

    Args:
        device: Objeto de dispositivo proporcionado por `TemperHandler().get_devices()`.

    Returns:
        dict: Diccionario con los campos:
            - "vendor_id": str | None
            - "product_id": str | None
            - "manufacturer": str | None
            - "product": str | None
            - "serial_number": str | None

    Example:
        >>> handler = TemperHandler()
        >>> devices = handler.get_devices()
        >>> get_device_metadata(devices[0])
        {
            "vendor_id": "0x413d",
            "product_id": "0x2107",
            "manufacturer": "RDing",
            "product": "TEMPer Sensor",
            "serial_number": "A1B2C3D4"
        }
    """
    metadata = {}
    try:
        metadata["vendor_id"] = hex(device._device.idVendor)
        metadata["product_id"] = hex(device._device.idProduct)

        try:
            metadata["manufacturer"] = usb.util.get_string(device._device, device._device.iManufacturer)
        except:
            metadata["manufacturer"] = None

        try:
            metadata["product"] = usb.util.get_string(device._device, device._device.iProduct)
        except:
            metadata["product"] = None

        try:
            serial = usb.util.get_string(device._device, device._device.iSerialNumber)
            metadata["serial_number"] = serial if serial else 'Desconocido'
        except:
            metadata["serial_number"] = 'Desconocido'

    except AttributeError:
        # Algunas versiones del driver no exponen _device
        metadata = {
            "vendor_id": None,
            "product_id": None,
            "manufacturer": None,
            "product": None,
            "serial_number": 'Desconocido'
        }

    return metadata


def get_medicion(offset_celsius: float = -6.14) -> list[dict]:
    """Obtiene una o varias mediciones de temperatura de dispositivos TEMPer USB.

    Usa `TemperHandler()` para detectar automáticamente todos los sensores TEMPer
    conectados. Para cada dispositivo:
      - Obtiene su metadata USB mediante `get_device_metadata()`.
      - Lee la temperatura corregida con un offset configurable.

    Args:
        offset_celsius (float): Corrección aplicada a la lectura del sensor.
            Algunos sensores TEMPer presentan un error sistemático que se ajusta
            restando un offset (por defecto -6.14 °C).

    Returns:
        list[dict]: Lista de diccionarios, uno por cada dispositivo, cada uno con:
            - "metadata": dict
            - "temperature_c": float

    Example:
        >>> get_medicion()
        [
            {
                "metadata": {
                    "vendor_id": "0x413d",
                    "product_id": "0x2107",
                    "manufacturer": "RDing",
                    "product": "TEMPer Sensor",
                    "serial_number": "A1B2C3D4"
                },
                "temperature_c": 22.37
            }
        ]

    Notes:
        - Si no hay sensores conectados, devuelve una lista vacía.
        - La temperatura devuelta ya incluye la corrección del offset.
    """
    handler = TemperHandler()
    devices = handler.get_devices()

    output = []

    for device in devices:
        data = {
            "metadata": get_device_metadata(device),
            "temperature_c": device.get_temperature() + offset_celsius
        }
        output.append(data)
    #print(output)
    return output

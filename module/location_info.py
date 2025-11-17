import json
import os
from typing import Dict, Any

def get_location_data(config_path: str = "config/config.json") -> Dict[str, Any]:
    """Carga los datos de ubicación y offset de calibración desde un JSON de configuración.

    Args:
        config_path (str): Ruta al archivo JSON de configuración.

    Returns:
        dict: Diccionario con claves:
            - 'ubicacion': str
            - 'cpd': str
            - 'sala': str
            - 'offset_celsius': float

    Raises:
        FileNotFoundError: Si no se encuentra el archivo.
        json.JSONDecodeError: Si el JSON no es válido.
        KeyError: Si faltan las claves requeridas.
        ValueError: Si 'offset_celsius' no es un número.
    """
    full_path = os.path.abspath(config_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = ["ubicacion", "cpd", "sala", "offset_celsius"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Falta la clave '{key}' en {full_path}")

    # Validar que offset_celsius sea numérico
    try:
        data["offset_celsius"] = float(data["offset_celsius"])
    except (TypeError, ValueError):
        raise ValueError(f"El valor de 'offset_celsius' debe ser numérico, se encontró: {data['offset_celsius']}")

    return data

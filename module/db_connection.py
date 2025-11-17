# module/db_connection.py
"""
Módulo de conexión a MariaDB.

Este módulo carga credenciales desde un archivo JSON externo y establece una
conexión con una base de datos MariaDB.

Estructura esperada del archivo config/credenciales.json:

{
  "database": {
    "host": "servidor",
    "port": 3306,
    "user": "usuario",
    "password": "pass",
    "database": "BBDD"
  }
}

Asegúrate de que el archivo exista y respete este formato.
"""

import json
import os
import mariadb
from typing import Dict, Any


def load_credentials(config_path: str = "config/credenciales.json") -> Dict[str, Any]:
    """Carga y devuelve las credenciales de conexión desde un archivo JSON.

    El archivo debe tener la siguiente estructura:

    ```json
    {
      "database": {
        "host": "servidor",
        "port": 3306,
        "user": "usuario",
        "password": "pass",
        "database": "BBDD"
      }
    }
    ```

    Args:
        config_path (str): Ruta al archivo de credenciales.
            Por defecto: "config/credenciales.json".

    Returns:
        Dict[str, Any]: Diccionario con las credenciales de base de datos.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        json.JSONDecodeError: Si el JSON es inválido.
        KeyError: Si falta la clave "database".
    """
    full_path = os.path.abspath(config_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Credenciales no encontradas: {full_path}")

    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)["database"]


def get_db_connection():
    """Establece y devuelve una conexión activa a MariaDB.

    Utiliza las credenciales obtenidas por `load_credentials()`.  
    Si ocurre un error, devuelve `None` en lugar de lanzar una excepción.

    Returns:
        mariadb.Connection | None: Conexión activa o None si falla.
    """
    creds = load_credentials()

    try:
        conn = mariadb.connect(
            host=creds["host"],
            port=creds["port"],
            user=creds["user"],
            password=creds["password"],
            database=creds["database"],
            autocommit=True
        )
        print("Conexión a MariaDB exitosa.")
        return conn

    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return None

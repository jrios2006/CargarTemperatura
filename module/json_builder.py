# module/json_builder.py
import json
import mariadb
from datetime import datetime
from .db_connection import get_db_connection

def insert_into_db(telemetry_data: dict) -> bool:
    """Inserta un registro de telemetría en la tabla `telemetria_sensores`.

    Esta función utiliza la conexión a MariaDB proporcionada por `get_db_connection()`
    para insertar los datos de un sensor en la tabla `telemetria_sensores`. 
    El diccionario `telemetry_data` debe contener todos los campos requeridos
    por la tabla.

    Args:
        telemetry_data (dict): Diccionario con los datos de telemetría. Debe contener:
            - "fecha_hora" (str/datetime): Fecha y hora de la medición.
            - "nombre_sensor" (str): Nombre identificador del sensor.
            - "numero_serie" (str): Número de serie del sensor.
            - "ubicacion" (str): Ubicación física del sensor.
            - "hostname_maquina" (str): Nombre del host donde se registra la medición.
            - "ip_maquina" (str | None): IP de la máquina que registra la medición.
            - "id_maquina" (str | None): ID único de la máquina.
            - "temperatura" (float | int): Valor de temperatura en °C.
            - "humedad" (float | int): Valor de humedad en %.
            - "bateria" (float | int): Nivel de batería en % o voltaje.
            - "cpd" (str | None): Centro de procesamiento de datos u otra etiqueta.
            - "sala" (str | None): Ubicación de sala o área del sensor.

    Returns:
        bool: `True` si la inserción fue exitosa, `False` si hubo error
        o no se pudo conectar a la base de datos.

    Raises:
        mariadb.Error: Si ocurre un error de base de datos durante la ejecución
        del query.

    Example:
        >>> telemetry = {
        ...     "fecha_hora": "2025-11-15 12:00:00",
        ...     "nombre_sensor": "Sensor_A1",
        ...     "numero_serie": "SN123456",
        ...     "ubicacion": "Sala 1",
        ...     "hostname_maquina": "Servidor1",
        ...     "ip_maquina": "192.168.0.10",
        ...     "id_maquina": "a3f87b94eaf34936bd2f35c12d5be901",
        ...     "temperatura": 23.5,
        ...     "humedad": 45.2,
        ...     "bateria": 3.7,
        ...     "cpd": "CPD1",
        ...     "sala": "Sala A"
        ... }
        >>> insert_into_db(telemetry)
        Registro insertado: Sensor_A1 | 23.5°C
        True
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO telemetria_sensores 
        (fecha_hora, nombre_sensor, numero_serie, ubicacion, hostname_maquina, 
         ip_maquina, id_maquina, temperatura, humedad, bateria, cpd, sala)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            telemetry_data["fecha_hora"],
            telemetry_data["nombre_sensor"],
            telemetry_data["numero_serie"],
            telemetry_data["ubicacion"],
            telemetry_data["hostname_maquina"],
            telemetry_data["ip_maquina"],
            telemetry_data["id_maquina"],
            telemetry_data["temperatura"],
            telemetry_data["humedad"],
            telemetry_data["bateria"],
            telemetry_data["cpd"],
            telemetry_data["sala"]
        )
        cursor.execute(query, values)
        conn.commit()
        print(f"Registro insertado: {telemetry_data['nombre_sensor']} | {telemetry_data['temperatura']}°C")
        return True
    except mariadb.Error as e:
        print(f"Error al insertar: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


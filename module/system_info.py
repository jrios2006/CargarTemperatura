# module/system_info.py
"""
Módulo para obtener información del sistema.

Este módulo proporciona funciones para extraer datos como:
- Hostname del sistema
- Dirección IP local (no loopback)
- Identificador único de la máquina (machine-id en Linux o UUID del hardware)
- Información general consolidada del sistema

Estas utilidades pueden ser usadas para registro, auditoría,
identificación de dispositivos o diagnósticos.
"""

import socket
import uuid
import platform


def get_hostname() -> str:
    """Obtiene el hostname del sistema.

    Returns:
        str: Nombre de host configurado en el sistema operativo.

    Example:
        >>> get_hostname()
        'mi-servidor-local'
    """
    return socket.gethostname()


def get_ip() -> str | None:
    """Obtiene la dirección IP local (no loopback).

    Esta función crea un socket UDP "falso" hacia un servidor externo (8.8.8.8),
    sin enviar datos, solo para que el sistema determine la IP de salida.

    Returns:
        str | None: IP local del equipo (por ejemplo "192.168.1.23").
        Devuelve `None` si no puede determinarse (falta de red, permisos, etc.).

    Example:
        >>> get_ip()
        '192.168.0.14'
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def get_machine_id() -> str | None:
    """Obtiene un identificador único de la máquina.

    Intenta leer `/etc/machine-id` (Linux).  
    Si falla, usa el UUID basado en la MAC (`uuid.getnode()`), común en Windows y macOS.

    Returns:
        str | None: Machine ID si está disponible, o None si no se puede obtener.

    Example:
        >>> get_machine_id()
        'a3f87b94eaf34936bd2f35c12d5be901'
    """
    try:
        # Linux: machine-id estándar
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except:
        try:
            # Windows / macOS: fallback usando MAC del hardware
            return str(uuid.getnode())
        except:
            return None


def get_system_info(use_dynamic_ip: bool = True) -> dict:
    """Devuelve información general del sistema en formato diccionario.

    Args:
        use_dynamic_ip (bool): Si es True, intenta obtener la IP dinámica.
            Si es False, el campo "ip_maquina" será None.

    Returns:
        dict: Información del sistema con las claves:
            - "hostname": str
            - "ip_maquina": str | None
            - "id_maquina": str | None

    Example:
        >>> get_system_info()
        {
            "hostname": "mi-servidor",
            "ip_maquina": "192.168.1.50",
            "id_maquina": "a3f87b94..."
        }
    """
    hostname = get_hostname()
    ip = get_ip() if use_dynamic_ip else None
    machine_id = get_machine_id()

    return {
        "hostname": hostname,
        "ip_maquina": ip,
        "id_maquina": machine_id
    }

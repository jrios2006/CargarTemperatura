# Proyecto de Telemetría con Sensores TEMPer

Este proyecto permite la **lectura, almacenamiento y monitorización en tiempo real** de sensores de temperatura y humedad TEMPer conectados vía USB. Incluye:

- Ingesta de datos periódica desde los sensores.
- Registro en base de datos MariaDB.
- Log rotativo de mediciones.
- Generación de payloads JSON estructurados.
- Preparación para visualización en tiempo real con WebSocket (FastAPI).

---

## 1. Estructura del proyecto



```bash
project/
├── config/
│ ├── config.json # Configuración de ubicación y offset
│ └── credenciales.json # Credenciales de base de datos
├── module/
│ ├── db_connection.py # Conexión a MariaDB
│ ├── json_builder.py # Inserción de payloads en DB
│ ├── temper_reader.py # Lectura de sensores TEMPer
│ ├── system_info.py # Información del sistema
│ └── location_info.py # Lectura de configuración de ubicación y offset
├── main.py # Programa principal de ingesta y logging
└── README.md
```


---

## 2. Configuración

### 2.1 Base de datos

Define las credenciales en `config/credenciales.json`:

```json
{
  "database": {
    "host": "localhost",
    "port": 3306,
    "user": "usuario",
    "password": "pass",
    "database": "telemetria"
  }
}
```

Crea la tabla principal:

```sql
CREATE TABLE telemetria_sensores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nombre_sensor VARCHAR(50) NOT NULL,
    numero_serie VARCHAR(50) NOT NULL,
    cpd VARCHAR(20) NOT NULL,
    sala VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    hostname_maquina VARCHAR(50) NOT NULL,
    ip_maquina VARCHAR(45) NULL,
    id_maquina VARCHAR(50) NULL,
    temperatura DECIMAL(5,2) NULL,
    humedad DECIMAL(5,2) NULL,
    bateria DECIMAL(5,2) NULL,
    INDEX idx_fecha (fecha_hora),
    INDEX idx_cpd (cpd),
    INDEX idx_sensor (nombre_sensor, numero_serie),
    INDEX idx_ubicacion (ubicacion(50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

---

## 2.2 Configuración de ubicación y offset

Archivo `config/config.json`:

Son datos que no conoce el programa y si el operador del sistemas

```json
{
  "ubicacion": "Sala A",
  "cpd": "CPD1",
  "sala": "Sala A",
  "offset_celsius": -6.14
}
```

* offset_celsius: permite calibrar el sensor TEMPer.

---

## Uso

1. Instala dependencias:

```bash
pip install mariadb pyusb temperusb
```

--- 

2. Permitir que un usuario normal acceda al sensor USB

Identificar el dispositivo USB TEMPer:

```bash
lsusb

...

Bus 001 Device 004: ID 0c45:7401 RDing TEMPerV1.4

```

Crear una regla de udev para dar permisos al usuario:

```bash
sudo nano /etc/udev/rules.d/99-temper.rules
```

Agregar

```bash
SUBSYSTEM=="usb", ATTR{idVendor}=="0c45", ATTR{idProduct}=="7401", MODE="0666"
```

* Reemplaza idVendor e idProduct según tu sensor (lsusb).
* MODE="0666" permite lectura y escritura a todos los usuarios.

Recargar reglas de udev:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

3. Ejecuta el programa principal:

```bash
python main.py
```

* Se generará un log rotativo temperatura.log.
* Se insertarán los datos en la tabla telemetria_sensores.
* Si el sensor no tiene número de serie, se usa "DESCONOCIDO".

---

## Estructura del payload JSON

Cada registro insertado sigue esta estructura:


```json
{
  "fecha_hora": "2025-11-15 23:45:57",
  "nombre_sensor": "TEMPerV1.4",
  "numero_serie": "DESCONOCIDO",
  "ubicacion": "Sala A",
  "hostname_maquina": "Servidor1",
  "ip_maquina": "192.168.0.10",
  "id_maquina": "a3f87b94eaf34936bd2f35c12d5be901",
  "temperatura": 23.5,
  "humedad": 45.2,
  "bateria": 3.7,
  "cpd": "CPD1",
  "sala": "Sala A"
}
```

---

## Consideraciones

* El programa aplica automáticamente el offset de calibración al leer la temperatura.
* Se recomienda ejecutar la ingesta con un cron o servicio para leer datos cada 15 minutos o menos.
* Se puede extender con alertas por cambios bruscos de parámetros o falta de datos.
* Preparado para integrarse con WebSocket FastAPI para monitorización en tiempo real.

---

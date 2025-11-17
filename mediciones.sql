CREATE TABLE telemetria_sensores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único de cada lectura (BIGINT para escalabilidad)',
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de la lectura (automática en el servidor)',
    nombre_sensor VARCHAR(50) NOT NULL COMMENT 'Nombre descriptivo del sensor (ej: TEMP Rm 12-01)',
    numero_serie VARCHAR(50) NOT NULL COMMENT 'Número de serie único del sensor físico',
    cpd VARCHAR(20) NOT NULL COMMENT 'Identificador del CPD (ej: CPD-01, CPD-MAD, CPD-BCN)',
    sala VARCHAR(50) NOT NULL COMMENT 'Sala dentro del CPD (ej: Sala Blanca, Sala UPS)',
    ubicacion VARCHAR(100) NOT NULL COMMENT 'Ubicación específica (ej: Rack 12 - Armario Superior)',
    hostname_maquina VARCHAR(50) NOT NULL COMMENT 'Hostname de la máquina que ejecuta el programa',
    ip_maquina VARCHAR(45) NULL COMMENT 'IP de la máquina (IPv4 o IPv6). NULL si no disponible',
    id_maquina VARCHAR(50) NULL COMMENT 'ID único del sistema (machine-id, UUID, etc.)',
    temperatura DECIMAL(5,2) NULL COMMENT 'Temperatura en grados Celsius (°C)',
    humedad DECIMAL(5,2) NULL COMMENT 'Humedad relativa en porcentaje (%)',
    bateria DECIMAL(5,2) NULL COMMENT 'Nivel de batería del sensor (%) o voltaje (V)',
    -- Índices para rendimiento
    INDEX idx_fecha (fecha_hora),
    INDEX idx_cpd (cpd),
    INDEX idx_sensor (nombre_sensor, numero_serie),
    INDEX idx_ubicacion (ubicacion(50))
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_general_ci 
  COMMENT='Tabla principal para telemetría de sensores en múltiples CPDs';

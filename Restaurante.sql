
SHOW ENGINES;

SHOW VARIABLES;

SET default_storage_engine = 'InnoDB';

SHOW DATABASES;

CREATE DATABASE reservaciones_db CHARACTER SET UTF8MB4
COLLATE UTF8MB4_UNICODE_CI;
USE reservaciones_db;
-- Tabla de Mesas
CREATE TABLE mesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidad INT NOT NULL
);

-- Tabla de Disponibilidad (Registra los horarios disponibles y la cantidad de mesas libres)
CREATE TABLE disponibilidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL UNIQUE,
    mesas_disponibles INT NOT NULL CHECK (mesas_disponibles >= 0)
);

-- Tabla de Reservaciones (Relacionada con clientes y mesas)
CREATE TABLE reservaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    mesa_id INT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mesa FOREIGN KEY (mesa_id) REFERENCES mesas(id) ON DELETE CASCADE,
    CONSTRAINT unique_reservacion UNIQUE (mesa_id, fecha_hora) -- Evita doble reserva de una mesa en la misma hora
    
INSERT INTO mesas (numero, capacidad) VALUES 
(1, 4),
(2, 2),
(3, 6),
(4, 4),
(5, 2);

INSERT INTO disponibilidad (fecha_hora, mesas_disponibles) VALUES 
('2025-03-22 13:00:00', 5),
('2025-03-22 14:00:00', 5),
('2025-03-22 19:00:00', 5),
('2025-03-23 13:00:00', 5),
('2025-03-23 19:00:00', 5);
INSERT INTO reservaciones (nombre, email, fecha_hora, mesa_id) VALUES 
('Juan Pérez', 'juan.perez@email.com', '2025-03-22 13:00:00', 1),
('María Gómez', 'maria.gomez@email.com', '2025-03-22 14:00:00', 2),
('Carlos López', 'carlos.lopez@email.com', '2025-03-22 19:00:00', 3),
('Ana Torres', 'ana.torres@email.com', '2025-03-23 13:00:00', 4),
('Luis Ramírez', 'luis.ramirez@email.com', '2025-03-23 19:00:00', 5);
SELECT * FROM reservaciones

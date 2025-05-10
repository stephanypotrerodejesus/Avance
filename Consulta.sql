reservaciones
CREATE DATABASE IF NOT EXISTS reservaciones_db CHARACTER SET UTF8MB4 COLLATE UTF8MB4_UNICODE_CI;


USE reservaciones_db;


CREATE TABLE IF NOT EXISTS mesas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL UNIQUE,
    capacidad INT NOT NULL
);


CREATE TABLE IF NOT EXISTS disponibilidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL UNIQUE,
    mesas_disponibles INT NOT NULL CHECK (mesas_disponibles >= 0)
);



CREATE TABLE IF NOT EXISTS reservaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    mesa_id INT NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mesa FOREIGN KEY (mesa_id) REFERENCES mesas(id) ON DELETE CASCADE,
    CONSTRAINT unique_reservacion UNIQUE (mesa_id, fecha_hora)
);

INSERT INTO mesas (numero, capacidad) VALUES
(1, 4),
(2, 4),
(3, 2),
(4, 6);
CREATE DATABASE IF NOT EXISTS vehiculos_db;
USE vehiculos_db;

CREATE TABLE IF NOT EXISTS vehiculos (
    placa VARCHAR(10) PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INT NOT NULL,
    color VARCHAR(30) NOT NULL
);

-- Datos de ejemplo 
INSERT INTO vehiculos (placa, marca, modelo, año, color) VALUES
('ABC123', 'Toyota', 'Corolla', 2020, 'Rojo'),
('DEF456', 'Honda', 'Civic', 2021, 'Azul'),
('GHI789', 'Ford', 'Mustang', 2022, 'Negro');
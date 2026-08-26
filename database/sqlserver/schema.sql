-- Crear la base de datos
CREATE DATABASE vehiculos_db;
GO

-- Usar la base de datos
USE vehiculos_db;
GO

-- Crear la tabla
CREATE TABLE vehiculos (
    placa NVARCHAR(10) PRIMARY KEY,
    marca NVARCHAR(50) NOT NULL,
    modelo NVARCHAR(50) NOT NULL,
    año INT NOT NULL,
    color NVARCHAR(30) NOT NULL
);
GO

-- Datos de ejemplo
INSERT INTO vehiculos (placa, marca, modelo, año, color) VALUES
('ABC123', 'Toyota', 'Corolla', 2020, 'Rojo'),
('DEF456', 'Honda', 'Civic', 2021, 'Azul'),
('GHI789', 'Ford', 'Mustang', 2022, 'Negro');
GO

-- Verificar datos
SELECT * FROM vehiculos;
GO
CREATE TABLE vehiculos (
    placa VARCHAR2(10) PRIMARY KEY,
    marca VARCHAR2(50) NOT NULL,
    modelo VARCHAR2(50) NOT NULL,
    año NUMBER(4) NOT NULL,
    color VARCHAR2(30) NOT NULL
);


INSERT INTO vehiculos (placa, marca, modelo, año, color) VALUES
('ABC123', 'Toyota', 'Corolla', 2020, 'Rojo');

INSERT INTO vehiculos (placa, marca, modelo, año, color) VALUES
('DEF456', 'Honda', 'Civic', 2021, 'Azul');

INSERT INTO vehiculos (placa, marca, modelo, año, color) VALUES
('GHI789', 'Ford', 'Mustang', 2022, 'Negro');

COMMIT;
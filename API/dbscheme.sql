DROP TABLE IF EXISTS data;

CREATE TABLE data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    nacionalidad TEXT,
    fechaContrato TEXT NOT NULL,
    sexo TEXT NOT NULL
);
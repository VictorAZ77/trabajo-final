-- MySQL
CREATE DATABASE IF NOT EXISTS Empresa;
USE Empresa;

CREATE TABLE IF NOT EXISTS Departamentos (
    depto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Empleados (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Asignaciones (
    emp_id INT,
    depto_id INT,
    fecha_asignacion DATE,
    PRIMARY KEY (emp_id, depto_id),
    FOREIGN KEY (emp_id) REFERENCES Empleados(emp_id),
    FOREIGN KEY (depto_id) REFERENCES Departamentos(depto_id)
);

INSERT INTO Departamentos (nombre) VALUES ('Recursos Humanos'), ('Desarrollo'), ('Ventas');
INSERT INTO Empleados (nombre, fecha_contratacion, salario) VALUES ('Alice', '2020-01-10', 50000), ('Bob', '2020-05-23', 60000);

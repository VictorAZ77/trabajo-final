-- SQL Server
CREATE DATABASE Empresa;
GO

USE Empresa;
GO

CREATE TABLE Departamentos (
    depto_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL
);
GO

CREATE TABLE Empleados (
    emp_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
);
GO

CREATE TABLE Asignaciones (
    emp_id INT,
    depto_id INT,
    fecha_asignacion DATE,
    PRIMARY KEY (emp_id, depto_id),
    FOREIGN KEY (emp_id) REFERENCES Empleados(emp_id),
    FOREIGN KEY (depto_id) REFERENCES Departamentos(depto_id)
);
GO

INSERT INTO Departamentos (nombre) VALUES (N'Recursos Humanos'), (N'Desarrollo'), (N'Ventas');
INSERT INTO Empleados (nombre, fecha_contratacion, salario) VALUES (N'Alice', '2020-01-10', 50000), (N'Bob', '2020-05-23', 60000);
GO

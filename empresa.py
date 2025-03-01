import mysql.connector
import pyodbc
from tabulate import tabulate
from decimal import Decimal
import datetime

def conectar_a_base_de_datos():
    """Permite al usuario elegir la base de datos y establece la conexión correspondiente"""
    db_choice = input("Elige la basepip install pyodbc de datos (1 para MySQL, 2 para SQL Server): ")
    if db_choice == '1':  # MySQL
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='Empresa'
            )
            placeholder = '%s'  # Placeholder para MySQL
            return connection, placeholder, db_choice
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None, None, db_choice
    elif db_choice == '2':  # SQL Server
        try:
            connection = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=TRABAJO\SQLEXPRESS02;"
                "Database=Empresa;"
                "Trusted_Connection=yes;"
            )
            placeholder = '?'  # Placeholder para SQL Server
            return connection, placeholder, db_choice
        except pyodbc.Error as e:
            print(f"Error al conectar a SQL Server: {e}")
            return None, None, db_choice
    else:
        print("Selección no válida.")
        return None, None, None

def convertir_tipo_datos(resultados):
    """Convierte los tipos de datos en los resultados para que sean compatibles con tabulate"""
    resultados_convertidos = []
    for fila in resultados:
        fila_convertida = []
        for valor in fila:
            if isinstance(valor, Decimal):
                valor = float(valor)
            elif isinstance(valor, datetime.date):
                valor = str(valor)
            fila_convertida.append(valor)
        resultados_convertidos.append(tuple(fila_convertida))
    return resultados_convertidos

def ejecutar_consulta(cursor, consulta, params=None):
    """Ejecuta una consulta SQL y devuelve los resultados formateados en una tabla"""
    try:
        cursor.execute(consulta, params or ())
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        # print(f"Descripción de las columnas: {columns}")
        # print(f"Resultados obtenidos: {results}")
        if not results:
            print("No se encontraron resultados.")
            return "No data available"
        results = convertir_tipo_datos(results)
        table = tabulate(results, headers=columns, tablefmt="grid")
        print("Consulta ejecutada correctamente.")
        return table
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return "Error ejecutando la consulta"

def leer_script_sql(nombre_archivo):
    """Lee el contenido de un archivo SQL"""
    try:
        with open(nombre_archivo, 'r') as file:
            script = file.read()
        return script
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
        return None
    
def obtener_tablas(connection):
                    try:
                        cursor = connection.cursor()
                        cursor.execute("""
                            SELECT TABLE_NAME 
                            FROM INFORMATION_SCHEMA.TABLES 
                            WHERE TABLE_TYPE = 'BASE TABLE'
                        """)
                        return [tabla[0] for tabla in cursor.fetchall()]
                    except pyodbc.Error as e:
                        print(f"Error al conectar a SQL Server: {e}")
                        return []
def consultar_tabla(conexion, nombre_tabla):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al consultar la tabla {nombre_tabla}: {err}")
        return []

def obtener_nombres_columnas(conexion, nombre_tabla):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{nombre_tabla}'")
        return [columna[0] for columna in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"Error al obtener columnas de {nombre_tabla}: {err}")
        return []   

def main():
    conexion, placeholder, db_choice = conectar_a_base_de_datos()
    if conexion:
        try:
            cursor = conexion.cursor()
            while True:
                print("\n1. Mostrar todas las tablas")
                print("2. Añadir un nuevo empleado")
                print("3. Añadir nuevo departamento")
                print("4. Eliminar empleado")
                print("5. Eliminar departamento")
                print("6. Actualizar fecha de contratación de un empleado")
                print("7. Actualizar salario del empleado")
                print("8. Top 3 de empleados con salario mas alto")
                print("9. Salario de empleados de forma descendente")
                print("10. Numero de empleados contratados por mes")
                print("11. Ultimo empleado contratado")
                print("12. Salir")
                opcion = input("Elige una opción: ")

                if opcion == '1':
                    tablas = obtener_tablas(conexion)
                        # Consultar cada tabla
                    for tabla in tablas:
                        print(f"\n=== Contenido de la tabla: {tabla} ===")
                        print("-" * 50)
                        
                        # Obtener datos y columnas
                        datos = consultar_tabla(conexion, tabla)
                        columnas = obtener_nombres_columnas(conexion, tabla)
                        
                        # Imprimir resultados formateados
                        if datos:
                            print(tabulate(datos, headers=columnas, tablefmt="grid"))
                        else:
                            print("La tabla no contiene registros")
                elif opcion == '2':
                    
                    print("\nListado de Empleados Actuales:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                    nombre = input("Nombre del nuevo empleado: ")
                    fecha = input("Fecha de contratación (YYYY-MM-DD): ")
                    salario = input("Salario: ")
                    consulta = f"INSERT INTO Empleados (nombre, fecha_contratacion, salario) VALUES ({placeholder}, {placeholder}, {placeholder})"
                    cursor.execute(consulta, (nombre, fecha, salario))
                    conexion.commit()
                    print("Empleado añadido.")

                    print("Empleado añadido.")
                    print("\nListadp de Empleados Actualizado:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                elif opcion == '3':


                    print("\nListado de Departamentos Actuales:")
                    consulta = "SELECT * FROM Departamentos"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                    nombre_depto = input("Nombre del nuevo departamento: ")
                    consulta = f"INSERT INTO Departamentos (nombre) VALUES ({placeholder})"
                    cursor.execute(consulta, (nombre_depto,))
                    conexion.commit()
                    print("Departamento añadido.")

                    print("\nListadp de Departamentos Actualizado:")
                    consulta = "SELECT * FROM Departamentos"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                elif opcion == '4':

                    print("\nListado de Empleados Actuales:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                    emp_id = input("ID del empleado a eliminar: ")
                    consulta_dependencias = f"SELECT * FROM Asignaciones WHERE emp_id = {placeholder}"
                    cursor.execute(consulta_dependencias, (emp_id,))
                    if cursor.fetchall():
                        print("No se puede eliminar: el empleado tiene asignaciones activas.")
                    else:
                        consulta_borrar = f"DELETE FROM Empleados WHERE emp_id = {placeholder}"
                        cursor.execute(consulta_borrar, (emp_id,))
                        conexion.commit()
                        print("Empleado eliminado exitosamente.")

                    
                    print("\nListadp de Empleados Actualizado:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)


                elif opcion == '5':

                    print("\nListado de Departamentos Actuales:")
                    consulta = "SELECT * FROM Departamentos"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                    dept_id = input("ID del departamento a eliminar: ")
                    consulta_dependencias2 = f"SELECT * FROM Asignaciones WHERE depto_id = {placeholder}"
                    cursor.execute(consulta_dependencias2, (dept_id,))
                    if cursor.fetchall():
                        print("No se puede eliminar: el departamento tiene asignaciones activas.")
                    else:
                        consulta_borrar2 = f"DELETE FROM Departamentos WHERE depto_id = {placeholder}"
                        cursor.execute(consulta_borrar2, (dept_id,))
                        conexion.commit()
                        print("Departamento eliminado exitosamente.")

                        print("\nListado de Departamentos Actualizado:")
                        consulta = "SELECT * FROM Departamentos"
                        resultado = ejecutar_consulta(cursor, consulta)
                        print(resultado)

                elif opcion == '6':
                    print("\nListado de Empleados Actuales:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                    emp_id = input("ID del empleado a actualizar: ")
                    nueva_fecha_contratacion = input("Nueva fecha de contratacion del empleado (YYYY-MM-DD): ")
                    consulta_actualizar = f"UPDATE Empleados SET fecha_contratacion = {placeholder} WHERE emp_id = {placeholder}"
                    cursor.execute(consulta_actualizar, (nueva_fecha_contratacion, emp_id))
                    conexion.commit()
                    print("Empleado actualizado exitosamente.")

                    print("\nListadp de Empleados Actualizado:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)


                elif opcion == '7':

                    print("\nListado de Empleados Actuales:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)


                    emp_id = input("ID del empleado a actualizar: ")
                    nuevo_salario = input("Nuevo salario del empleado: ")
                    consulta_actualizar = f"UPDATE Empleados SET salario = {placeholder} WHERE emp_id = {placeholder}"
                    cursor.execute(consulta_actualizar, (nuevo_salario, emp_id))
                    conexion.commit()
                    print("Empleado actualizado exitosamente.")

                    print("\nListadp de Empleados Actualizado:")
                    consulta = "SELECT * FROM Empleados"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)
                
                elif opcion == '8':

                    print("Top 3 Empleados con el salario mas alto")
                    consulta = "SELECT TOP 3 * FROM Empleados ORDER BY salario DESC"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)

                elif opcion == '9':
                    print("Salario de empleados del mas bajo al mas alto")
                    consulta = "SELECT * FROM Empleados ORDER BY salario DESC"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)
                
                elif opcion == '10':
                    print("Numero de empleados contratados por mes")
                    consulta = "SELECT DATENAME(MONTH,fecha_contratacion) AS mes, COUNT(*) AS num_empleados FROM Empleados GROUP BY DATENAME(MONTH,fecha_contratacion)"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)
                
                elif opcion == '11':
                    print("Ultimo empleado contratado")
                    consulta = "SELECT TOP 1 * FROM Empleados ORDER BY fecha_contratacion DESC"
                    resultado = ejecutar_consulta(cursor, consulta)
                    print(resultado)
                
                
                
                
                elif opcion == '12':
                    print("Saliendo...")
                    break
                else:
                    print("Opción no válida, intenta de nuevo.")
        except Exception as e:
            print(f"Error durante la operación: {e}")
        finally:
            cursor.close()
            conexion.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    main()
import mysql.connector
from mysql.connector import Error

class ConexionPM:
    def __init__(self, host='localhost', database='gestion_titulacion', user='root', password='vida'):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def conectar(self):
        """Establece la conexión a la base de datos y la valida."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
                return True
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False
        return False

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

    def ejecutar_consulta(self, consulta, parametros=None):
        """
        Ejecuta una consulta SQL de tipo SELECT y devuelve los resultados como tuplas.
        """
        if not self.connection or not self.connection.is_connected():
            print("Error: No hay conexión activa a la base de datos")
            return None

        try:
            cursor = self.connection.cursor()  # Usamos un cursor normal
            cursor.execute(consulta, parametros or ())
            resultados = cursor.fetchall()
            cursor.close()
            print("Consulta ejecutada con éxito")
            return resultados
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def ejecutar_actualizacion(self, consulta, parametros=None):
        """
        Ejecuta una consulta SQL de tipo INSERT, UPDATE o DELETE.
        """
        if not self.connection or not self.connection.is_connected():
            print("Error: No hay conexión activa a la base de datos")
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(consulta, parametros or ())
            self.connection.commit()
            cursor.close()
            print("Actualización realizada con éxito")
            return True
        except Error as e:
            print(f"Error al ejecutar la actualización: {e}")
            return False

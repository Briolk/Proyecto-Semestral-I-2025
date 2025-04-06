from ConexionPM import ConexionPM

class EstudiantesCRUD:
    def __init__(self):
        self.conexion = ConexionPM()
        self.conexion.conectar()

    def registrar_estudiante(self, ci, ru, nombre, apellidos, correo, estado, id_modalidad):
        """
        Inserta un nuevo estudiante en la base de datos.
        """
        consulta = """
        INSERT INTO estudiantes (ci, ru, nombre, apellidos, correo_electronico, estado, id_modalidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        parametros = (ci, ru, nombre, apellidos, correo, estado, id_modalidad)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True  # Operación exitosa
        except Exception as e:
            print(f"Error al registrar estudiante: {e}")
            return False

    def modificar_estudiante(self, ci, ru, nombre, apellidos, correo, estado, id_modalidad):
        """
        Modifica los datos de un estudiante existente.
        """
        consulta = """
        UPDATE estudiantes
        SET ru = %s, nombre = %s, apellidos = %s, correo_electronico = %s, estado = %s, id_modalidad = %s
        WHERE ci = %s
        """
        parametros = (ru, nombre, apellidos, correo, estado, id_modalidad, ci)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al modificar estudiante: {e}")
            return False

    def consultar_estudiantes(self):
        """
        Consulta todos los estudiantes de la base de datos y devuelve solo los datos.
        """
        consulta = "SELECT ci, ru, nombre, apellidos, correo_electronico, estado, id_modalidad FROM estudiantes"
        try:
            resultado = self.conexion.ejecutar_consulta(consulta)
            return resultado  # Aquí solo regresamos las filas
        except Exception as e:
            print(f"Error al consultar estudiantes: {e}")
            return []

    def eliminar_estudiante(self, ci):
        """
        Elimina un estudiante por su CI.
        """
        consulta = "DELETE FROM estudiantes WHERE ci = %s"
        parametros = (ci,)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            return False

    def consultar_modalidades(self):
        """Consulta las modalidades desde la base de datos."""
        consulta = "SELECT * FROM modalidades_graduacion"  
        try:
            modalidades = self.conexion.ejecutar_consulta(consulta)
            return modalidades  # Devuelve las filas completas como lista de tuplas
        except Exception as e:
            print(f"Error al consultar modalidades: {e}")
            return []

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            self.conexion.desconectar()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")




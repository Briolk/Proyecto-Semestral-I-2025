from ConexionPM import ConexionPM

class FasesEvaluacionCRUD:
    def __init__(self):
        self.conexion = ConexionPM()
        self.conexion.conectar()

    def registrar_fase(self, nombre_fase, descripcion, orden):
        """
        Inserta una nueva fase de evaluación en la base de datos.
        """
        consulta = """
        INSERT INTO fases_evaluacion (nombre_fase, descripcion, orden)
        VALUES (%s, %s, %s)
        """
        parametros = (nombre_fase, descripcion, orden)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True  # Operación exitosa
        except Exception as e:
            print(f"Error al registrar fase de evaluación: {e}")
            return False

    def modificar_fase(self, id_fase, nombre_fase, descripcion, orden):
        """
        Modifica los datos de una fase de evaluación existente.
        """
        consulta = """
        UPDATE fases_evaluacion
        SET nombre_fase = %s, descripcion = %s, orden = %s
        WHERE id_fase = %s
        """
        parametros = (nombre_fase, descripcion, orden, id_fase)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al modificar fase de evaluación: {e}")
            return False

    def consultar_fases(self):
        """
        Consulta todas las fases de evaluación de la base de datos y devuelve solo los datos.
        """
        consulta = "SELECT id_fase, nombre_fase, descripcion, orden FROM fases_evaluacion"
        try:
            resultado = self.conexion.ejecutar_consulta(consulta)
            return resultado  # Aquí solo regresamos las filas
        except Exception as e:
            print(f"Error al consultar fases de evaluación: {e}")
            return []

    def eliminar_fase(self, id_fase):
        """
        Elimina una fase de evaluación por su id.
        """
        consulta = "DELETE FROM fases_evaluacion WHERE id_fase = %s"
        parametros = (id_fase,)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al eliminar fase de evaluación: {e}")
            return False

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            self.conexion.desconectar()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

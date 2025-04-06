from ConexionPM import ConexionPM

class AvanceEvaluacionCRUD:
    def __init__(self):
        self.conexion = ConexionPM()
        self.conexion.conectar()

    def registrar_avance(self, ci_estudiante, id_fase, fecha_aprobacion, estado_fase='Pendiente'):
        """
        Inserta un nuevo avance de evaluación en la base de datos.
        """
        consulta = """
        INSERT INTO avance_evaluacion (ci_estudiante, id_fase, fecha_aprobacion, estado_fase)
        VALUES (%s, %s, %s, %s)
        """
        parametros = (ci_estudiante, id_fase, fecha_aprobacion, estado_fase)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True  # Operación exitosa
        except Exception as e:
            print(f"Error al registrar avance: {e}")
            return False

    def modificar_avance(self, id_avance, ci_estudiante, id_fase, fecha_aprobacion, estado_fase):
        """
        Modifica un avance de evaluación existente.
        """
        consulta = """
        UPDATE avance_evaluacion
        SET ci_estudiante = %s, id_fase = %s, fecha_aprobacion = %s, estado_fase = %s
        WHERE id_avance = %s
        """
        parametros = (ci_estudiante, id_fase, fecha_aprobacion, estado_fase, id_avance)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al modificar avance: {e}")
            return False

    def consultar_avances(self):
        """
        Consulta todos los avances de evaluación y devuelve los datos.
        """
        consulta = """
        SELECT id_avance, ci_estudiante, id_fase, fecha_aprobacion, estado_fase
        FROM avance_evaluacion
        """
        try:
            resultado = self.conexion.ejecutar_consulta(consulta)
            return resultado  # Retorna solo las filas consultadas
        except Exception as e:
            print(f"Error al consultar avances: {e}")
            return []

    def eliminar_avance(self, id_avance):
        """
        Elimina un avance de evaluación por su ID.
        """
        consulta = "DELETE FROM avance_evaluacion WHERE id_avance = %s"
        parametros = (id_avance,)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al eliminar avance: {e}")
            return False

    def consultar_avances_por_estudiante(self, ci_estudiante):
        """
        Consulta todos los avances de evaluación de un estudiante por su CI.
        """
        consulta = """
        SELECT id_avance, ci_estudiante, id_fase, fecha_aprobacion, estado_fase
        FROM avance_evaluacion
        WHERE ci_estudiante = %s
        """
        parametros = (ci_estudiante,)
        try:
            resultado = self.conexion.ejecutar_consulta(consulta, parametros)
            return resultado
        except Exception as e:
            print(f"Error al consultar avances por estudiante: {e}")
            return []

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            self.conexion.desconectar()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

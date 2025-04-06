from ConexionPM import ConexionPM
from datetime import date

class CrudAsignacion:
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        try:
            self.conexion = ConexionPM()
            if not self.conexion.conectar():
                raise Exception("No se pudo establecer la conexión con la base de datos")
        except Exception as e:
            print(f"Error al inicializar la conexión: {e}")
            self.conexion = None

    def buscar_estudiante_por_ru(self, ru_estudiante):
        """Busca un estudiante por su número de RU."""
        if not self.conexion:
            print("Conexión no disponible")
            return None
        try:
            query = """
                SELECT e.ci, e.nombre, e.apellidos
                FROM estudiantes e
                WHERE e.ru = %s
            """
            parametros = (ru_estudiante,)
            estudiante = self.conexion.ejecutar_consulta(query, parametros)
            return estudiante[0] if estudiante else None
        except Exception as e:
            print(f"Error al buscar estudiante por RU: {e}")
            return None

    def obtener_tutores(self):
        """Obtiene la lista de tutores disponibles."""
        if not self.conexion:
            print("Conexión no disponible")
            return []
        try:
            query = "SELECT id_tutor, nombre_tutor FROM tutores"
            tutores = self.conexion.ejecutar_consulta(query)
            return tutores if tutores else []
        except Exception as e:
            print(f"Error al obtener tutores: {e}")
            return []

    def obtener_estudiantes_sin_tutor(self):
        """Obtiene la lista de estudiantes que no tienen tutor asignado."""
        if not self.conexion:
            print("Conexión no disponible")
            return []
        try:
            query = """
            SELECT e.ci, e.nombre, e.apellidos
            FROM estudiantes e
            LEFT JOIN asignacion_tutor at ON e.ci = at.ci_estudiante 
            WHERE at.id_tutor IS NULL
            """
            estudiantes = self.conexion.ejecutar_consulta(query)
            return estudiantes if estudiantes else []
        except Exception as e:
            print(f"Error al obtener estudiantes sin tutor: {e}")
            return []

    def obtener_estudiantes_con_tutor(self):
        """Obtiene la lista de estudiantes que tienen un tutor asignado."""
        if not self.conexion:
            print("Conexión no disponible")
            return []
        try:
            query = """
            SELECT e.ci, e.nombre, e.apellidos, t.nombre_tutor
            FROM estudiantes e
            JOIN asignacion_tutor at ON e.ci = at.ci_estudiante
            JOIN tutores t ON at.id_tutor = t.id_tutor
            """
            estudiantes_con_tutor = self.conexion.ejecutar_consulta(query)
            return estudiantes_con_tutor if estudiantes_con_tutor else []
        except Exception as e:
            print(f"Error al obtener estudiantes con tutor: {e}")
            return []

    def asignar_tutor_a_estudiante(self, ci_estudiante, id_tutor):
        """Asigna un tutor a un estudiante en la base de datos."""
        if not self.conexion:
            print("Conexión no disponible")
            return False
        try:
            query = """
            INSERT INTO asignacion_tutor (ci_estudiante, id_tutor, fecha_asignacion)
            VALUES (%s, %s, CURDATE())
            """
            parametros = (ci_estudiante, id_tutor)
            success = self.conexion.ejecutar_actualizacion(query, parametros)
            return success
        except Exception as e:
            print(f"Error al asignar tutor a estudiante: {e}")
            return False


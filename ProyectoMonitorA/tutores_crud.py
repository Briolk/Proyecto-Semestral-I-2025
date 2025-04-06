from ConexionPM import ConexionPM

class TutoresCRUD:
    def __init__(self):
        self.conexion = ConexionPM()
        if not self.conexion.conectar():
            print("No se pudo establecer la conexión a la base de datos")
            return

    def registrar_tutor(self, nombre_tutor, especialidad):
        """
        Registra un nuevo tutor en la base de datos.
        """
        consulta = "INSERT INTO tutores (nombre_tutor, especialidad) VALUES (%s, %s)"
        parametros = (nombre_tutor, especialidad)

        if self.conexion.ejecutar_actualizacion(consulta, parametros):
            print("Tutor registrado exitosamente")
            return True
        return False

    def modificar_tutor(self, id_tutor, nombre_tutor, especialidad):
        """
        Modifica los detalles de un tutor en la base de datos.
        """
        consulta = "UPDATE tutores SET nombre_tutor = %s, especialidad = %s WHERE id_tutor = %s"
        parametros = (nombre_tutor, especialidad, id_tutor)

        if self.conexion.ejecutar_actualizacion(consulta, parametros):
            print("Tutor modificado exitosamente")
            return True
        return False

    def eliminar_tutor(self, id_tutor):
        """
        Elimina un tutor de la base de datos.
        """
        consulta = "DELETE FROM tutores WHERE id_tutor = %s"
        parametros = (id_tutor,)

        if self.conexion.ejecutar_actualizacion(consulta, parametros):
            print("Tutor eliminado exitosamente")
            return True
        return False

    def consultar_tutores(self):
        """
        Consulta todos los tutores registrados en la base de datos.
        """
        consulta = "SELECT * FROM tutores"
        resultados = self.conexion.ejecutar_consulta(consulta)

        tutores = []
        if resultados:
            for resultado in resultados:
                tutor = {
                    'id_tutor': resultado[0],
                    'nombre_tutor': resultado[1],
                    'especialidad': resultado[2]
                }
                tutores.append(tutor)
        return tutores


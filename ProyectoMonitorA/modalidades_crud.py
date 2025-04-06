from ConexionPM import ConexionPM

class ModalidadesCRUD:
    def __init__(self):
        self.conexion = ConexionPM()
        self.conexion.conectar()

    def registrar_modalidad(self, nombre_modalidad, descripcion):
        consulta = """
        INSERT INTO modalidades_graduacion (nombre_modalidad, descripcion)
        VALUES (%s, %s)
        """
        parametros = (nombre_modalidad, descripcion)
        return self.conexion.ejecutar_actualizacion(consulta, parametros)

    def modificar_modalidad(self, id_modalidad, nombre_modalidad, descripcion):
        consulta = """
        UPDATE modalidades_graduacion
        SET nombre_modalidad = %s, descripcion = %s
        WHERE id_modalidad = %s
        """
        parametros = (nombre_modalidad, descripcion, id_modalidad)
        return self.conexion.ejecutar_actualizacion(consulta, parametros)

    def consultar_modalidades(self):
        consulta = "SELECT * FROM modalidades_graduacion"
        return self.conexion.ejecutar_consulta(consulta)

    def eliminar_modalidad(self, id_modalidad):
        consulta = "DELETE FROM modalidades_graduacion WHERE id_modalidad = %s"
        parametros = (id_modalidad,)
        return self.conexion.ejecutar_actualizacion(consulta, parametros)

    def cerrar_conexion(self):
        self.conexion.desconectar()

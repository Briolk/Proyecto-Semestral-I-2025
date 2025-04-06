from ConexionPM import ConexionPM

class PagosTitulacionCRUD:
    def __init__(self):
        self.conexion = ConexionPM()
        self.conexion.conectar()

    def registrar_pago(self, ci_estudiante, id_fase, monto, fecha_pago, estado_pago):
        """
        Inserta un nuevo pago por titulación en la base de datos.
        """
        consulta = """
        INSERT INTO pagos_titulacion (ci_estudiante, id_fase, monto, fecha_pago, estado_pago)
        VALUES (%s, %s, %s, %s, %s)
        """
        parametros = (ci_estudiante, id_fase, monto, fecha_pago, estado_pago)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True  # Operación exitosa
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            return False

    def modificar_pago(self, id_pago, ci_estudiante, id_fase, monto, fecha_pago, estado_pago):
        """
        Modifica los datos de un pago por titulación existente.
        """
        consulta = """
        UPDATE pagos_titulacion
        SET ci_estudiante = %s, id_fase = %s, monto = %s, fecha_pago = %s, estado_pago = %s
        WHERE id_pago = %s
        """
        parametros = (ci_estudiante, id_fase, monto, fecha_pago, estado_pago, id_pago)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al modificar pago: {e}")
            return False

    def consultar_pagos(self):
        """
        Consulta todos los pagos por titulación de la base de datos y devuelve los datos.
        """
        consulta = "SELECT id_pago, ci_estudiante, id_fase, monto, fecha_pago, estado_pago FROM pagos_titulacion"
        try:
            resultado = self.conexion.ejecutar_consulta(consulta)
            return resultado  # Regresa las filas de los pagos
        except Exception as e:
            print(f"Error al consultar pagos: {e}")
            return []

    def eliminar_pago(self, id_pago):
        """
        Elimina un pago por su ID.
        """
        consulta = "DELETE FROM pagos_titulacion WHERE id_pago = %s"
        parametros = (id_pago,)
        try:
            self.conexion.ejecutar_actualizacion(consulta, parametros)
            return True
        except Exception as e:
            print(f"Error al eliminar pago: {e}")
            return False

    def consultar_fases(self):
        """Consulta las fases de evaluación desde la base de datos."""
        consulta = "SELECT id_fase FROM fases_evaluacion"  # Ajusta el nombre de la tabla y columna según tu base de datos
        try:
            fases = self.conexion.ejecutar_consulta(consulta)
            return [fase[0] for fase in fases]  # Devuelve solo los IDs de las fases
        except Exception as e:
            print(f"Error al consultar fases: {e}")
            return []

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            self.conexion.desconectar()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

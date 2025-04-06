import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
from PyQt6.QtGui import QIcon
from ConexionPM import ConexionPM
from pagosTitulacionCRUD import PagosTitulacionCRUD  # Importa la clase de CRUD para pagos de titulación

class PagosTitulacionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Pagos de Titulación")
        self.setGeometry(100, 100, 650, 400)
        self.setWindowIcon(QIcon("sal.ico"))
        
        self.pagos_titulacion_crud = PagosTitulacionCRUD()

        # Interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input.setPlaceholderText("Buscar pago...")  # Ajustar el texto para pagos
        self.search_input.textChanged.connect(self.on_search_text_changed)

        # Añadir el campo de búsqueda al layout principal
        main_layout.addWidget(self.search_input)

        # Layout de formulario de ingreso
        form_layout = QHBoxLayout()

        self.inputs = {
            "id_pago": QLineEdit(),  # Campo para id_pago, utilizado solo para modificación y eliminación
            "ci_estudiante": QLineEdit(),
            "id_fase": QLineEdit(),
            "monto": QLineEdit(),
            "fecha_pago": QLineEdit(),
            "estado_pago": QLineEdit()
        }

        for label, widget in self.inputs.items():
            widget.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
            form_layout.addWidget(QLabel(label.replace("_", " ").capitalize()))
            form_layout.addWidget(widget)

        main_layout.addLayout(form_layout)

        # Botones para las operaciones CRUD
        button_layout = QHBoxLayout()

        self.registrar_button = QPushButton("Registrar Pago")
        self.registrar_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.registrar_button.clicked.connect(self.registrar_pago)
        button_layout.addWidget(self.registrar_button)

        self.modificar_button = QPushButton("Modificar Pago")
        self.modificar_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        self.modificar_button.clicked.connect(self.modificar_pago)
        button_layout.addWidget(self.modificar_button)

        self.eliminar_button = QPushButton("Eliminar Pago")
        self.eliminar_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        self.eliminar_button.clicked.connect(self.eliminar_pago)
        button_layout.addWidget(self.eliminar_button)

        main_layout.addLayout(button_layout)

        # Tabla para mostrar los pagos
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Ajustar el número de columnas a 6 para incluir id_pago
        self.table.setHorizontalHeaderLabels(["ID Pago", "CI Estudiante", "ID Fase", "Monto", "Fecha de Pago", "Estado de Pago"])
        self.table.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table.selectionModel().selectionChanged.connect(self.on_row_selected)
        self.table.horizontalHeader().setFixedHeight(35)
        self.table.setColumnWidth(0, 80)  # Ajustar el ancho de las columnas
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 120)

        main_layout.addWidget(self.table)

        # Establecer el layout principal en la ventana
        self.setLayout(main_layout)

        # Listar los pagos en la tabla
        self.listar_pagos()

    def listar_pagos(self):
        """
        Lista todos los pagos en la tabla.
        """
        pagos = self.pagos_titulacion_crud.consultar_pagos()
        self.table.setRowCount(len(pagos))

        for row, pago in enumerate(pagos):
            # Asumiendo que los valores de pago están en el orden correcto
            self.table.setItem(row, 0, QTableWidgetItem(str(pago[0])))  # id_pago
            self.table.setItem(row, 1, QTableWidgetItem(str(pago[1])))  # ci_estudiante
            self.table.setItem(row, 2, QTableWidgetItem(str(pago[2])))  # id_fase
            self.table.setItem(row, 3, QTableWidgetItem(str(pago[3])))  # monto
            self.table.setItem(row, 4, QTableWidgetItem(str(pago[4])))  # fecha_pago
            self.table.setItem(row, 5, QTableWidgetItem(str(pago[5])))  # estado_pago

    def on_row_selected(self):
        """
        Rellena los campos de entrada con los datos de la fila seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_pago = self.table.item(selected_row, 0).text()
            ci_estudiante = self.table.item(selected_row, 1).text()
            id_fase = self.table.item(selected_row, 2).text()
            monto = self.table.item(selected_row, 3).text()
            fecha_pago = self.table.item(selected_row, 4).text()
            estado_pago = self.table.item(selected_row, 5).text()

            self.inputs["id_pago"].setText(id_pago)
            self.inputs["ci_estudiante"].setText(ci_estudiante)
            self.inputs["id_fase"].setText(id_fase)
            self.inputs["monto"].setText(monto)
            self.inputs["fecha_pago"].setText(fecha_pago)
            self.inputs["estado_pago"].setText(estado_pago)

    def on_search_text_changed(self):
        """Se llama cuando el texto de búsqueda cambia"""
        text = self.search_input.text()
        self.listar_pagos()  # Vuelve a cargar todos los pagos
        self.filter_table(text, 1)  # Aplica el filtro a la columna "CI Estudiante"
        
    def filter_table(self, text, col):
        """Filtra los datos en la tabla según el texto ingresado en un filtro."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if item:
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def registrar_pago(self):
        """
        Registra un nuevo pago en la base de datos.
        """
        ci_estudiante = self.inputs["ci_estudiante"].text()
        id_fase = self.inputs["id_fase"].text()
        monto = self.inputs["monto"].text()
        fecha_pago = self.inputs["fecha_pago"].text()
        estado_pago = self.inputs["estado_pago"].text()

        if ci_estudiante and id_fase and monto and fecha_pago and estado_pago:
            self.pagos_titulacion_crud.registrar_pago(ci_estudiante, id_fase, monto, fecha_pago, estado_pago)
            self.limpiar_campos()
            self.listar_pagos()

            # Mostrar mensaje de éxito
            self.show_message("Éxito", "Pago registrado correctamente.", QMessageBox.Icon.Information)

    def modificar_pago(self):
        """
        Modifica los datos de un pago.
        """
        id_pago = self.inputs["id_pago"].text()
        ci_estudiante = self.inputs["ci_estudiante"].text()
        id_fase = self.inputs["id_fase"].text()
        monto = self.inputs["monto"].text()
        fecha_pago = self.inputs["fecha_pago"].text()
        estado_pago = self.inputs["estado_pago"].text()

        if id_pago and ci_estudiante and id_fase and monto and fecha_pago and estado_pago:
            self.pagos_titulacion_crud.modificar_pago(id_pago, ci_estudiante, id_fase, monto, fecha_pago, estado_pago)
            self.limpiar_campos()
            self.listar_pagos()

            # Mostrar mensaje de éxito
            self.show_message("Éxito", "Pago modificado correctamente.", QMessageBox.Icon.Information)


    def eliminar_pago(self):
        """
        Elimina un pago de titulación de la base de datos.
        """
        id_pago = self.inputs["id_pago"].text()

        if id_pago:
            self.pagos_titulacion_crud.eliminar_pago(id_pago)
            self.limpiar_campos()
            self.listar_pagos()

            # Mostrar mensaje de éxito
            self.show_message("Éxito", "Pago eliminado correctamente.", QMessageBox.Icon.Information)

    def show_message(self, title, message, icon):
        """
        Muestra un mensaje en pantalla.
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def limpiar_campos(self):
        """
        Limpia los campos de entrada.
        """
        for input_field in self.inputs.values():
            input_field.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PagosTitulacionApp()
    window.show()
    sys.exit(app.exec())



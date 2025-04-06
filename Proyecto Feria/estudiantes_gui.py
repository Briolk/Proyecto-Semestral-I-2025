from PyQt6.QtWidgets import ( 
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QPushButton, QLineEdit, QHBoxLayout, QLabel, QMessageBox, QComboBox
)
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCore import Qt
from estudiantes_crud import EstudiantesCRUD  # Clase proporcionada


class EstudiantesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Estudiantes")
        self.resize(500, 500)
        self.setWindowIcon(QIcon("sal.ico"))
        
        # Colores
        self.color_primario = "#D90718"
        self.color_secundario = "#2A438C"
        self.color_fondo = "#F2F2F2"
        self.color_texto = "#0D0D0D"

        self.crud = EstudiantesCRUD()

        self.init_ui()

    def init_ui(self):
        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Diseño principal
        main_layout = QVBoxLayout()
        
        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Aumentamos la columna por la modalidad
        self.table.setHorizontalHeaderLabels(
            ["CI", "RU", "Nombre", "Apellidos", "Correo", "Estado", "Modalidad"]
        )
        # Establece el color de fondo de la tabla.
        self.table.setStyleSheet("background-color: #F2D64B;")

        # Cambia el color del texto en el encabezado horizontal de la tabla.
        self.table.horizontalHeader().setStyleSheet(f"color: {self.color_texto}")

        # Oculta el encabezado vertical de la tabla.
        self.table.verticalHeader().setVisible(False)

        # Establece el comportamiento de la selección de filas para que se seleccione toda la fila en lugar de solo una celda.
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Conecta la señal de cambio de selección de los elementos de la tabla al método fill_form_fields
        # para actualizar los campos del formulario cuando se selecciona una fila en la tabla.
        self.table.itemSelectionChanged.connect(self.fill_form_fields)
        self.table.horizontalHeader().setFixedHeight(35)
        self.table.setColumnWidth(0, 50)  
        self.table.setColumnWidth(1, 80)  
        self.table.setColumnWidth(2, 100)  
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 170)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 70)

        # Carga los datos en la tabla (probablemente desde una base de datos o archivo).
        self.load_table_data()


        # Filtros
        filter_layout = QHBoxLayout()
        self.filters = []
        for col in range(7):
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Filtrar {self.table.horizontalHeaderItem(col).text()}")
            line_edit.textChanged.connect(lambda text, col=col: self.filter_table(text, col))
            self.filters.append(line_edit)
            filter_layout.addWidget(line_edit)

        # Formulario
        form_layout = QHBoxLayout()
        self.inputs = {
            "ci": QLineEdit(),
            "ru": QLineEdit(),
            "nombre": QLineEdit(),
            "apellidos": QLineEdit(),
            "correo": QLineEdit(),
            "estado": QComboBox(),
            "modalidad": QComboBox()  # Agregamos ComboBox para modalidad
        }
        for label, widget in self.inputs.items():
            form_layout.addWidget(QLabel(label.capitalize()))
            form_layout.addWidget(widget)

        self.inputs["estado"].addItems(["Activo", "Inactivo"])  # Opciones de ejemplo
        self.inputs["modalidad"].addItems(self.get_modalidades())  # Opciones de modalidad

        # Botones
        button_layout = QHBoxLayout()
        add_button = QPushButton("Registrar")
        add_button.setStyleSheet(f"background-color: {self.color_primario}; color: {self.color_fondo}")
        add_button.clicked.connect(self.add_student)

        update_button = QPushButton("Actualizar")
        update_button.setStyleSheet(f"background-color: {self.color_secundario}; color: {self.color_fondo}")
        update_button.clicked.connect(self.update_student)

        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)

        # Construcción
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.central_widget.setLayout(main_layout)

    def load_table_data(self):
        """Carga los datos de la base de datos a la tabla."""
        self.table.setRowCount(0)
        estudiantes = self.crud.consultar_estudiantes()
        for estudiante in estudiantes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, data in enumerate(estudiante):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def filter_table(self, text, col):
        """Filtra los datos en la tabla según el texto ingresado en un filtro."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if item:
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def fill_form_fields(self):
        """Rellena los campos del formulario con los datos seleccionados en la tabla."""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self.inputs["ci"].setText(self.table.item(row, 0).text())
            self.inputs["ru"].setText(self.table.item(row, 1).text())
            self.inputs["nombre"].setText(self.table.item(row, 2).text())
            self.inputs["apellidos"].setText(self.table.item(row, 3).text())
            self.inputs["correo"].setText(self.table.item(row, 4).text())
            self.inputs["estado"].setCurrentText(self.table.item(row, 5).text())
            self.inputs["modalidad"].setCurrentText(self.table.item(row, 6).text())

    def add_student(self):
        """Registra un nuevo estudiante en la base de datos."""
        ci = self.inputs["ci"].text()
        ru = self.inputs["ru"].text()
        nombre = self.inputs["nombre"].text()
        apellidos = self.inputs["apellidos"].text()
        correo = self.inputs["correo"].text()
        estado = self.inputs["estado"].currentText()
        modalidad = self.inputs["modalidad"].currentText()

        estudiantes = self.crud.consultar_estudiantes()
        if any(str(ci) == str(est[0]) for est in estudiantes):
            QMessageBox.warning(self, "Error", "El estudiante ya existe.")
            return

        # Obtiene el ID de la modalidad seleccionada
        id_modalidad = self.get_modalidad_id(modalidad)
        
        self.crud.registrar_estudiante(ci, ru, nombre, apellidos, correo, estado, id_modalidad)
        QMessageBox.information(self, "Éxito", "Estudiante registrado exitosamente.")
        self.load_table_data()
        self.limpiar_campos()

    def update_student(self):
        """Actualiza los datos de un estudiante en la base de datos."""
        ci = self.inputs["ci"].text()
        ru = self.inputs["ru"].text()
        nombre = self.inputs["nombre"].text()
        apellidos = self.inputs["apellidos"].text()
        correo = self.inputs["correo"].text()
        estado = self.inputs["estado"].currentText()
        modalidad = self.inputs["modalidad"].currentText()

        if not ci:
            QMessageBox.warning(self, "Error", "Debe seleccionar un estudiante para actualizar.")
            return

        # Obtiene el ID de la modalidad seleccionada
        id_modalidad = self.get_modalidad_id(modalidad)
        
        self.crud.modificar_estudiante(ci, ru, nombre, apellidos, correo, estado, id_modalidad)
        QMessageBox.information(self, "Éxito", "Estudiante actualizado exitosamente.")
        self.load_table_data()
        self.limpiar_campos()

    def get_modalidades(self):
        """Devuelve las modalidades de graduación disponibles."""
        modalidades = self.crud.consultar_modalidades()
        return [modalidad[1] for modalidad in modalidades]  # Suponiendo que modalidad[1] contiene el nombre

    def get_modalidad_id(self, modalidad_name):
        """Obtiene el ID de la modalidad seleccionada."""
        modalidades = self.crud.consultar_modalidades()  
        for modalidad in modalidades:
            if modalidad[1] == modalidad_name:  # Suponiendo que modalidad[1] contiene el nombre
                return modalidad[0]  # Suponiendo que modalidad[0] contiene el ID
        return None

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        for key, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                widget.clear()  # Limpia el texto de los campos de texto
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)  # Restablece el índice del ComboBox

if __name__ == "__main__":
    app = QApplication([])
    ventana = EstudiantesApp()
    ventana.show()
    app.exec()

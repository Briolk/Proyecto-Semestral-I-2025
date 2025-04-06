import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from ConexionPM import ConexionPM
from crud_asignacion import CrudAsignacion
from PyQt6.QtGui import QIcon

class AsignacionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asignación de Tutor a Estudiante")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("sal.ico"))
        
        self.crud_asignacion = CrudAsignacion()

        # Interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Campo de búsqueda para estudiantes sin tutor
        self.search_input_sin_tutor = QLineEdit()
        self.search_input_sin_tutor.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input_sin_tutor.setPlaceholderText("Buscar estudiante sin tutor por RU...")
        self.search_input_sin_tutor.textChanged.connect(self.on_search_text_changed_sin_tutor)

        # Campo de búsqueda para estudiantes con tutor
        self.search_input_con_tutor = QLineEdit()
        self.search_input_con_tutor.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input_con_tutor.setPlaceholderText("Buscar estudiante con tutor por CI...")
        self.search_input_con_tutor.textChanged.connect(self.on_search_text_changed_con_tutor)

        # Añadir los campos de búsqueda al layout principal
        main_layout.addWidget(self.search_input_sin_tutor)
        main_layout.addWidget(self.search_input_con_tutor)

        # Layout de formulario de ingreso
        form_layout = QHBoxLayout()

        self.inputs = {
            "ru_estudiante": QLineEdit(),
            "tutor": QComboBox()
        }

        self.inputs["tutor"].setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        form_layout.addWidget(QLabel("Número de RU del Estudiante"))
        form_layout.addWidget(self.inputs["ru_estudiante"])
        form_layout.addWidget(QLabel("Seleccionar Tutor"))
        form_layout.addWidget(self.inputs["tutor"])

        main_layout.addLayout(form_layout)

        # Botón para asignar tutor
        self.asignar_button = QPushButton("Asignar Tutor")
        self.asignar_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.asignar_button.clicked.connect(self.asignar_tutor)
        main_layout.addWidget(self.asignar_button)

        # Tabla para mostrar los estudiantes sin tutor
        self.table_sin_tutor = QTableWidget()
        self.table_sin_tutor.setColumnCount(3)
        self.table_sin_tutor.setHorizontalHeaderLabels(["CI Estudiante", "Nombre", "Apellidos"])
        self.table_sin_tutor.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table_sin_tutor.selectionModel().selectionChanged.connect(self.on_row_selected_sin_tutor)
        self.table_sin_tutor.horizontalHeader().setFixedHeight(35)

        # Tabla para mostrar los estudiantes con tutor
        self.table_con_tutor = QTableWidget()
        self.table_con_tutor.setColumnCount(4)
        self.table_con_tutor.setHorizontalHeaderLabels(["CI Estudiante", "Nombre", "Apellidos", "Nombre Tutor"])
        self.table_con_tutor.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table_con_tutor.selectionModel().selectionChanged.connect(self.on_row_selected_con_tutor)
        self.table_con_tutor.horizontalHeader().setFixedHeight(35)

        # Añadir las tablas al layout
        main_layout.addWidget(self.table_sin_tutor)
        main_layout.addWidget(self.table_con_tutor)

        # Establecer el layout principal en la ventana
        self.setLayout(main_layout)

        # Listar los estudiantes sin tutor en la tabla
        self.listar_estudiantes_sin_tutor()
        self.listar_estudiantes_con_tutor()

    def listar_estudiantes_sin_tutor(self):
        """Lista los estudiantes sin tutor en la tabla."""
        estudiantes = self.crud_asignacion.obtener_estudiantes_sin_tutor()
        self.table_sin_tutor.setRowCount(len(estudiantes))

        for row, estudiante in enumerate(estudiantes):
            self.table_sin_tutor.setItem(row, 0, QTableWidgetItem(str(estudiante[0])))  # CI Estudiante
            self.table_sin_tutor.setItem(row, 1, QTableWidgetItem(estudiante[1]))  # Nombre
            self.table_sin_tutor.setItem(row, 2, QTableWidgetItem(estudiante[2]))  # Apellidos

        # Cargar los tutores en el combo box
        tutores = self.crud_asignacion.obtener_tutores()
        self.inputs["tutor"].clear()  # Limpiar combo box
        for tutor in tutores:
            self.inputs["tutor"].addItem(tutor[1], tutor[0])  # Agregar nombre de tutor y el id_tutor como dato adicional

    def listar_estudiantes_con_tutor(self):
        """Lista los estudiantes con tutor asignado en la tabla."""
        estudiantes_con_tutor = self.crud_asignacion.obtener_estudiantes_con_tutor()
        self.table_con_tutor.setRowCount(len(estudiantes_con_tutor))

        for row, estudiante in enumerate(estudiantes_con_tutor):
            self.table_con_tutor.setItem(row, 0, QTableWidgetItem(str(estudiante[0])))  # CI Estudiante
            self.table_con_tutor.setItem(row, 1, QTableWidgetItem(estudiante[1]))  # Nombre
            self.table_con_tutor.setItem(row, 2, QTableWidgetItem(estudiante[2]))  # Apellidos
            self.table_con_tutor.setItem(row, 3, QTableWidgetItem(estudiante[3]))  # Nombre Tutor

    def on_row_selected_sin_tutor(self):
        """Rellena el campo de número de RU con el CI del estudiante seleccionado en la tabla de estudiantes sin tutor."""
        selected_row = self.table_sin_tutor.currentRow()
        if selected_row >= 0:
            ci_estudiante = self.table_sin_tutor.item(selected_row, 0).text()
            self.inputs["ru_estudiante"].setText(ci_estudiante)

    def on_row_selected_con_tutor(self):
        """Rellena el campo de número de RU con el CI del estudiante seleccionado en la tabla de estudiantes con tutor."""
        selected_row = self.table_con_tutor.currentRow()
        if selected_row >= 0:
            ci_estudiante = self.table_con_tutor.item(selected_row, 0).text()
            self.inputs["ru_estudiante"].setText(ci_estudiante)

    def on_search_text_changed_sin_tutor(self):
        """Se llama cuando el texto de búsqueda cambia en la tabla de estudiantes sin tutor"""
        text = self.search_input_sin_tutor.text()
        self.listar_estudiantes_sin_tutor()  # Vuelve a cargar todos los estudiantes sin tutor
        self.filter_table(self.table_sin_tutor, text, 0)  # Aplica el filtro a la columna "CI Estudiante"

    def on_search_text_changed_con_tutor(self):
        """Se llama cuando el texto de búsqueda cambia en la tabla de estudiantes con tutor"""
        text = self.search_input_con_tutor.text()
        self.listar_estudiantes_con_tutor()  # Vuelve a cargar todos los estudiantes con tutor
        self.filter_table(self.table_con_tutor, text, 0)  # Aplica el filtro a la columna "CI Estudiante"
        
    def filter_table(self, table, text, col):
        """Filtra los datos en la tabla según el texto ingresado en un filtro."""
        for row in range(table.rowCount()):
            item = table.item(row, col)
            if item:
                # Se oculta la fila si el texto no está contenido en el valor de la celda
                table.setRowHidden(row, text.lower() not in item.text().lower())

    def asignar_tutor(self):
        """Asigna un tutor a un estudiante."""
        ru_estudiante = self.inputs["ru_estudiante"].text()
        id_tutor = self.inputs["tutor"].currentData()  # Obtener el ID del tutor seleccionado

        if ru_estudiante and id_tutor:
            success = self.crud_asignacion.asignar_tutor_a_estudiante(ru_estudiante, id_tutor)
            if success:
                self.limpiar_campos()
                self.listar_estudiantes_sin_tutor()
                self.listar_estudiantes_con_tutor()

    def limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.inputs["ru_estudiante"].clear()
        self.inputs["tutor"].setCurrentIndex(0)  # Restablecer el combo box

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AsignacionApp()
    window.show()
    sys.exit(app.exec())


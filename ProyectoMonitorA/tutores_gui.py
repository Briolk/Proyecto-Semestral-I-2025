import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from ConexionPM import ConexionPM
from tutores_crud import TutoresCRUD
from PyQt6.QtGui import QIcon

class TutoresApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Tutores")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("sal.ico"))
        self.tutores_crud = TutoresCRUD()
        
        # Interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input.setPlaceholderText("Buscar tutor...")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        # Añadir el campo de búsqueda al layout principal
        main_layout.addWidget(self.search_input)

        # Layout de formulario de ingreso
        form_layout = QHBoxLayout()

        self.inputs = {
            "id_tutor": QLineEdit(),
            "nombre_tutor": QLineEdit(),
            "especialidad": QLineEdit()
        }

        for label, widget in self.inputs.items():
            widget.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
            form_layout.addWidget(QLabel(label.replace("_", " ").capitalize()))
            form_layout.addWidget(widget)

        main_layout.addLayout(form_layout)

        # Botones para las operaciones CRUD
        button_layout = QHBoxLayout()

        self.registrar_button = QPushButton("Registrar Tutor")
        self.registrar_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.registrar_button.clicked.connect(self.registrar_tutor)
        button_layout.addWidget(self.registrar_button)

        self.modificar_button = QPushButton("Modificar Tutor")
        self.modificar_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        self.modificar_button.clicked.connect(self.modificar_tutor)
        button_layout.addWidget(self.modificar_button)

        self.eliminar_button = QPushButton("Eliminar Tutor")
        self.eliminar_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        self.eliminar_button.clicked.connect(self.eliminar_tutor)
        button_layout.addWidget(self.eliminar_button)

        main_layout.addLayout(button_layout)

        # Tabla para mostrar los tutores
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID Tutor", "Nombre", "Especialidad"])
        self.table.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table.selectionModel().selectionChanged.connect(self.on_row_selected)
        self.table.horizontalHeader().setFixedHeight(35)# ancho de la cabecera
        self.table.setColumnWidth(0, 50)  # Ancho de la columna ID Tutor
        self.table.setColumnWidth(1, 250)  # Ancho de la columna Nombre
        self.table.setColumnWidth(2, 200)  # Ancho de la columna Especialidad

        main_layout.addWidget(self.table)

        # Establecer el layout principal en la ventana
        self.setLayout(main_layout)

        # Listar tutores en la tabla
        self.listar_tutores()

    def listar_tutores(self):
        """
        Lista todos los tutores en la tabla.
        """
        tutores = self.tutores_crud.consultar_tutores()
        self.table.setRowCount(len(tutores))

        for row, tutor in enumerate(tutores):
            self.table.setItem(row, 0, QTableWidgetItem(str(tutor['id_tutor'])))  # ID Tutor
            self.table.setItem(row, 1, QTableWidgetItem(tutor['nombre_tutor']))
            self.table.setItem(row, 2, QTableWidgetItem(tutor['especialidad']))

    def on_row_selected(self):
        """
        Rellena los campos de entrada con los datos de la fila seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_tutor = self.table.item(selected_row, 0).text()
            nombre_tutor = self.table.item(selected_row, 1).text()
            especialidad = self.table.item(selected_row, 2).text()

            self.inputs["id_tutor"].setText(id_tutor)  # Rellenamos el campo id_tutor
            self.inputs["nombre_tutor"].setText(nombre_tutor)
            self.inputs["especialidad"].setText(especialidad)

    def on_search_text_changed(self):
        """Se llama cuando el texto de búsqueda cambia"""
        text = self.search_input.text()
        self.listar_tutores()  # Vuelve a cargar todos los tutores
        self.filter_table(text, 1)  # Aplica el filtro a la columna "nombre_tutor"
        
    def filter_table(self, text, col):
        """Filtra los datos en la tabla según el texto ingresado en un filtro."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if item:
                # Se oculta la fila si el texto no está contenido en el valor de la celda
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def registrar_tutor(self):
        """
        Registra un nuevo tutor en la base de datos.
        """
        nombre_tutor = self.inputs["nombre_tutor"].text()
        especialidad = self.inputs["especialidad"].text()

        if nombre_tutor and especialidad:
            self.tutores_crud.registrar_tutor(nombre_tutor, especialidad)
            self.limpiar_campos()
            self.listar_tutores()

    def modificar_tutor(self):
        """
        Modifica los datos de un tutor.
        """
        id_tutor = self.inputs["id_tutor"].text()  # Obtener el ID desde el campo
        nombre_tutor = self.inputs["nombre_tutor"].text()
        especialidad = self.inputs["especialidad"].text()

        if nombre_tutor and especialidad and id_tutor:
            self.tutores_crud.modificar_tutor(id_tutor, nombre_tutor, especialidad)
            self.limpiar_campos()
            self.listar_tutores()

    def eliminar_tutor(self):
        """
        Elimina un tutor de la base de datos.
        """
        id_tutor = self.inputs["id_tutor"].text()  # Obtener el ID desde el campo

        if id_tutor:
            self.tutores_crud.eliminar_tutor(id_tutor)
            self.listar_tutores()

    def limpiar_campos(self):
        """
        Limpia los campos de entrada.
        """
        self.inputs["id_tutor"].clear()
        self.inputs["nombre_tutor"].clear()
        self.inputs["especialidad"].clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TutoresApp()
    ventana.show()
    sys.exit(app.exec())

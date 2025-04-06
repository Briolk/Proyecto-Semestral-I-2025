import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt6.QtGui import QIcon
from ConexionPM import ConexionPM
from modalidades_crud import ModalidadesCRUD

class ModalidadesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Modalidades de Graduación")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("sal.ico"))
        
        self.modalidades_crud = ModalidadesCRUD()

        # Interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input.setPlaceholderText("Buscar modalidad...")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        # Añadir el campo de búsqueda al layout principal
        main_layout.addWidget(self.search_input)

        # Layout de formulario de ingreso
        form_layout = QHBoxLayout()

        self.inputs = {
            "id_modalidad": QLineEdit(),
            "nombre_modalidad": QLineEdit(),
            "descripcion": QLineEdit()
        }

        for label, widget in self.inputs.items():
            widget.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
            form_layout.addWidget(QLabel(label.replace("_", " ").capitalize()))
            form_layout.addWidget(widget)

        main_layout.addLayout(form_layout)

        # Botones para las operaciones CRUD
        button_layout = QHBoxLayout()

        self.registrar_button = QPushButton("Registrar Modalidad")
        self.registrar_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.registrar_button.clicked.connect(self.registrar_modalidad)
        button_layout.addWidget(self.registrar_button)

        self.modificar_button = QPushButton("Modificar Modalidad")
        self.modificar_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        self.modificar_button.clicked.connect(self.modificar_modalidad)
        button_layout.addWidget(self.modificar_button)

        self.eliminar_button = QPushButton("Eliminar Modalidad")
        self.eliminar_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        self.eliminar_button.clicked.connect(self.eliminar_modalidad)
        button_layout.addWidget(self.eliminar_button)

        main_layout.addLayout(button_layout)

        # Tabla para mostrar las modalidades
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID Modalidad", "Nombre", "Descripción"])
        self.table.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table.horizontalHeader().setFixedHeight(35)
        self.table.setColumnWidth(0, 50)  
        self.table.setColumnWidth(1, 250)  
        self.table.setColumnWidth(2, 200)  

        self.table.selectionModel().selectionChanged.connect(self.on_row_selected)
        main_layout.addWidget(self.table)

        # Establecer el layout principal en la ventana
        self.setLayout(main_layout)

        # Listar modalidades en la tabla
        self.listar_modalidades()

    def listar_modalidades(self):
        """
        Lista todas las modalidades en la tabla.
        """
        modalidades = self.modalidades_crud.consultar_modalidades()  # Obtener datos de la base de datos
        self.table.setRowCount(len(modalidades))

        for row, modalidad in enumerate(modalidades):
            # Accediendo a la tupla por índice en lugar de por claves
            self.table.setItem(row, 0, QTableWidgetItem(str(modalidad[0])))  # ID Modalidad (índice 0)
            self.table.setItem(row, 1, QTableWidgetItem(modalidad[1]))  # Nombre Modalidad (índice 1)
            self.table.setItem(row, 2, QTableWidgetItem(modalidad[2]))  # Descripción (índice 2)

    def on_row_selected(self):
        """
        Rellena los campos de entrada con los datos de la fila seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_modalidad = self.table.item(selected_row, 0).text()
            nombre_modalidad = self.table.item(selected_row, 1).text()
            descripcion = self.table.item(selected_row, 2).text()

            self.inputs["id_modalidad"].setText(id_modalidad)
            self.inputs["nombre_modalidad"].setText(nombre_modalidad)
            self.inputs["descripcion"].setText(descripcion)

    def on_search_text_changed(self):
        """Se llama cuando el texto de búsqueda cambia"""
        text = self.search_input.text()
        self.listar_modalidades()  # Vuelve a cargar todas las modalidades
        self.filter_table(text, 1)  # Aplica el filtro a la columna "nombre_modalidad"
        
    def filter_table(self, text, col):
        """Filtra los datos en la tabla según el texto ingresado en un filtro."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if item:
                # Se oculta la fila si el texto no está contenido en el valor de la celda
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def registrar_modalidad(self):
        """
        Registra una nueva modalidad en la base de datos.
        """
        nombre_modalidad = self.inputs["nombre_modalidad"].text()
        descripcion = self.inputs["descripcion"].text()

        if nombre_modalidad and descripcion:
            self.modalidades_crud.registrar_modalidad(nombre_modalidad, descripcion)
            self.limpiar_campos()
            self.listar_modalidades()

    def modificar_modalidad(self):
        """
        Modifica los datos de una modalidad.
        """
        id_modalidad = self.inputs["id_modalidad"].text()
        nombre_modalidad = self.inputs["nombre_modalidad"].text()
        descripcion = self.inputs["descripcion"].text()

        if nombre_modalidad and descripcion and id_modalidad:
            self.modalidades_crud.modificar_modalidad(id_modalidad, nombre_modalidad, descripcion)
            self.limpiar_campos()
            self.listar_modalidades()

    def eliminar_modalidad(self):
        """
        Elimina una modalidad de la base de datos.
        """
        id_modalidad = self.inputs["id_modalidad"].text()

        if id_modalidad:
            self.modalidades_crud.eliminar_modalidad(id_modalidad)
            self.listar_modalidades()

    def limpiar_campos(self):
        """
        Limpia los campos de entrada.
        """
        self.inputs["id_modalidad"].clear()
        self.inputs["nombre_modalidad"].clear()
        self.inputs["descripcion"].clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ModalidadesApp()
    ventana.show()
    sys.exit(app.exec())


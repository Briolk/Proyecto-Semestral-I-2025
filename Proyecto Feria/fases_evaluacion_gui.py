import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from ConexionPM import ConexionPM
from fases_evaluacion_crud import FasesEvaluacionCRUD
from PyQt6.QtGui import QIcon

class FasesEvaluacionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Fases de Evaluación")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("sal.ico"))
        
        self.fases_crud = FasesEvaluacionCRUD()
        
        # Interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input.setPlaceholderText("Buscar fase...")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        # Añadir el campo de búsqueda al layout principal
        main_layout.addWidget(self.search_input)

        # Layout de formulario de ingreso
        form_layout = QHBoxLayout()

        self.inputs = {
            "id_fase": QLineEdit(),
            "nombre_fase": QLineEdit(),
            "descripcion": QLineEdit(),
            "orden": QLineEdit()
        }

        for label, widget in self.inputs.items():
            widget.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
            form_layout.addWidget(QLabel(label.replace("_", " ").capitalize()))
            form_layout.addWidget(widget)

        main_layout.addLayout(form_layout)

        # Botones para las operaciones CRUD
        button_layout = QHBoxLayout()

        self.registrar_button = QPushButton("Registrar Fase")
        self.registrar_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.registrar_button.clicked.connect(self.registrar_fase)
        button_layout.addWidget(self.registrar_button)

        self.modificar_button = QPushButton("Modificar Fase")
        self.modificar_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        self.modificar_button.clicked.connect(self.modificar_fase)
        button_layout.addWidget(self.modificar_button)

        self.eliminar_button = QPushButton("Eliminar Fase")
        self.eliminar_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        self.eliminar_button.clicked.connect(self.eliminar_fase)
        button_layout.addWidget(self.eliminar_button)

        main_layout.addLayout(button_layout)

        # Tabla para mostrar las fases
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Fase", "Nombre", "Descripción", "Orden"])
        self.table.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table.selectionModel().selectionChanged.connect(self.on_row_selected)
        self.table.horizontalHeader().setFixedHeight(35)
        self.table.setColumnWidth(0, 50)  # Ancho de la columna ID Fase
        self.table.setColumnWidth(1, 150)  # Ancho de la columna Nombre
        self.table.setColumnWidth(2, 310)  # Ancho de la columna Descripción
        self.table.setColumnWidth(3, 50)  # Ancho de la columna Orden

        main_layout.addWidget(self.table)

        # Establecer el layout principal en la ventana
        self.setLayout(main_layout)

        # Listar fases en la tabla
        self.listar_fases()

    def listar_fases(self):
        """
        Lista todas las fases en la tabla.
        """
        fases = self.fases_crud.consultar_fases()
        self.table.setRowCount(len(fases))

        for row, fase in enumerate(fases):
            # Usar índices numéricos en lugar de claves de diccionario
            self.table.setItem(row, 0, QTableWidgetItem(str(fase[0]))) 
            self.table.setItem(row, 1, QTableWidgetItem(fase[1]))  
            self.table.setItem(row, 2, QTableWidgetItem(fase[2]))  
            self.table.setItem(row, 3, QTableWidgetItem(str(fase[3])))
            
    def on_row_selected(self):
        """
        Rellena los campos de entrada con los datos de la fila seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            id_fase = self.table.item(selected_row, 0).text()
            nombre_fase = self.table.item(selected_row, 1).text()
            descripcion = self.table.item(selected_row, 2).text()
            orden = self.table.item(selected_row, 3).text()

            self.inputs["id_fase"].setText(id_fase)  # Rellenamos el campo id_fase
            self.inputs["nombre_fase"].setText(nombre_fase)
            self.inputs["descripcion"].setText(descripcion)
            self.inputs["orden"].setText(orden)

    def on_search_text_changed(self):
        """Se llama cuando el texto de búsqueda cambia"""
        text = self.search_input.text()
        self.listar_fases()  # Vuelve a cargar todas las fases
        self.filter_table(text, 1)  # Aplica el filtro a la columna "nombre_fase"
        
    def filter_table(self, text, col):
        """Filtra los datos en la tabla según el texto ingresado en un filtro."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col)
            if item:
                # Se oculta la fila si el texto no está contenido en el valor de la celda
                self.table.setRowHidden(row, text.lower() not in item.text().lower())

    def registrar_fase(self):
        """
        Registra una nueva fase en la base de datos.
        """
        nombre_fase = self.inputs["nombre_fase"].text()
        descripcion = self.inputs["descripcion"].text()
        orden = self.inputs["orden"].text()

        if nombre_fase and descripcion and orden:
            self.fases_crud.registrar_fase(nombre_fase, descripcion, orden)
            self.limpiar_campos()
            self.listar_fases()

    def modificar_fase(self):
        """
        Modifica los datos de una fase.
        """
        id_fase = self.inputs["id_fase"].text()  # Obtener el ID desde el campo
        nombre_fase = self.inputs["nombre_fase"].text()
        descripcion = self.inputs["descripcion"].text()
        orden = self.inputs["orden"].text()

        if nombre_fase and descripcion and orden and id_fase:
            self.fases_crud.modificar_fase(id_fase, nombre_fase, descripcion, orden)
            self.limpiar_campos()
            self.listar_fases()

    def eliminar_fase(self):
        """
        Elimina una fase de la base de datos.
        """
        id_fase = self.inputs["id_fase"].text()  # Obtener el ID desde el campo

        if id_fase:
            self.fases_crud.eliminar_fase(id_fase)
            self.listar_fases()

    def limpiar_campos(self):
        """
        Limpia los campos de entrada.
        """
        self.inputs["id_fase"].clear()
        self.inputs["nombre_fase"].clear()
        self.inputs["descripcion"].clear()
        self.inputs["orden"].clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FasesEvaluacionApp()
    ventana.show()
    sys.exit(app.exec())


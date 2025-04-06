import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel
)
from PyQt6.QtGui import QIcon
from avanceEvaluacionCRUD import AvanceEvaluacionCRUD


class AvanceEvaluacionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Avances de Evaluación")
        self.setGeometry(100, 100, 800, 500)
        self.setWindowIcon(QIcon("sal.ico"))
        
        self.avance_evaluacion_crud = AvanceEvaluacionCRUD()
        
        # Interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
        self.search_input.setPlaceholderText("Buscar avance de evaluación...")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        main_layout.addWidget(self.search_input)

        # Layout de formulario de ingreso
        form_layout = QHBoxLayout()

        self.inputs = {
            "id_avance": QLineEdit(),
            "ci_estudiante": QLineEdit(),
            "id_fase": QLineEdit(),
            "fecha_aprobacion": QLineEdit(),
            "estado_fase": QLineEdit()
        }

        for label, widget in self.inputs.items():
            widget.setStyleSheet("background-color: #2A438C; color: white; padding: 5px;")
            if label == "id_avance":
                widget.setReadOnly(True)  # Campo de solo lectura
            form_layout.addWidget(QLabel(label.replace("_", " ").capitalize()))
            form_layout.addWidget(widget)

        main_layout.addLayout(form_layout)

        # Botones para las operaciones CRUD
        button_layout = QHBoxLayout()

        self.registrar_button = QPushButton("Registrar Avance")
        self.registrar_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.registrar_button.clicked.connect(self.registrar_avance)
        button_layout.addWidget(self.registrar_button)

        self.modificar_button = QPushButton("Modificar Avance")
        self.modificar_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        self.modificar_button.clicked.connect(self.modificar_avance)
        button_layout.addWidget(self.modificar_button)

        self.eliminar_button = QPushButton("Eliminar Avance")
        self.eliminar_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        self.eliminar_button.clicked.connect(self.eliminar_avance)
        button_layout.addWidget(self.eliminar_button)

        main_layout.addLayout(button_layout)

        # Tabla para mostrar los avances
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Avance", "CI Estudiante", "ID Fase", "Fecha Aprobación", "Estado Fase"])
        self.table.setStyleSheet("QTableWidget { background-color: #1C2833; color: white; }")
        self.table.selectionModel().selectionChanged.connect(self.on_row_selected)
        self.table.horizontalHeader().setFixedHeight(35)
        self.table.setColumnWidth(0, 100)  # ID Avance
        self.table.setColumnWidth(1, 150)  # CI Estudiante
        self.table.setColumnWidth(2, 100)  # ID Fase
        self.table.setColumnWidth(3, 150)  # Fecha Aprobación
        self.table.setColumnWidth(4, 150)  # Estado Fase

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.listar_avances()

    def listar_avances(self):
        """
        Lista todos los avances de evaluación en la tabla.
        """
        avances = self.avance_evaluacion_crud.consultar_avances()
        self.table.setRowCount(len(avances))

        for row, avance in enumerate(avances):
            for col, value in enumerate(avance):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
    
    def on_search_text_changed(self, text):
        """
        Filtra los avances mostrados en la tabla según el texto ingresado en el campo de búsqueda.
        """
        avances = self.avance_evaluacion_crud.consultar_avances()
        # Filtrar los avances según el texto de búsqueda (coincidencia parcial)
        resultados = [
            avance for avance in avances
            if any(text.lower() in str(valor).lower() for valor in avance)
        ]
        
        # Actualizar la tabla con los resultados filtrados
        self.table.setRowCount(len(resultados))
        for row, avance in enumerate(resultados):
            for col, value in enumerate(avance):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def on_row_selected(self):
        """
        Rellena los campos de entrada con los datos de la fila seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            for col, key in enumerate(self.inputs.keys()):
                item = self.table.item(selected_row, col)
                self.inputs[key].setText(item.text() if item else "")

    def registrar_avance(self):
        ci_estudiante = self.inputs["ci_estudiante"].text()
        id_fase = self.inputs["id_fase"].text()
        fecha_aprobacion = self.inputs["fecha_aprobacion"].text()
        estado_fase = self.inputs["estado_fase"].text()

        if ci_estudiante and id_fase and fecha_aprobacion:
            self.avance_evaluacion_crud.registrar_avance(ci_estudiante, id_fase, fecha_aprobacion, estado_fase)
            self.limpiar_campos()
            self.listar_avances()

    def modificar_avance(self):
        id_avance = self.inputs["id_avance"].text()
        ci_estudiante = self.inputs["ci_estudiante"].text()
        id_fase = self.inputs["id_fase"].text()
        fecha_aprobacion = self.inputs["fecha_aprobacion"].text()
        estado_fase = self.inputs["estado_fase"].text()

        if id_avance and ci_estudiante and id_fase and fecha_aprobacion:
            self.avance_evaluacion_crud.modificar_avance(id_avance, ci_estudiante, id_fase, fecha_aprobacion, estado_fase)
            self.limpiar_campos()
            self.listar_avances()

    def eliminar_avance(self):
        id_avance = self.inputs["id_avance"].text()
        if id_avance:
            self.avance_evaluacion_crud.eliminar_avance(id_avance)
            self.limpiar_campos()
            self.listar_avances()

    def limpiar_campos(self):
        """
        Limpia los campos de entrada.
        """
        for widget in self.inputs.values():
            widget.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AvanceEvaluacionApp()
    ventana.show()
    sys.exit(app.exec())

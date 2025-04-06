import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)

from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt
from estudiantes_gui import EstudiantesApp
from tutores_gui import TutoresApp
from asignacion_tutor_gui import AsignacionApp
from modalidades_gui import ModalidadesApp
from pagosTitulacion_gui import PagosTitulacionApp
from avanceEvaluacionApp_gui import AvanceEvaluacionApp
from fases_evaluacion_gui import FasesEvaluacionApp



class Menu(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("APLICACIÓN DE GESTIÓN DE ESTUDIANTES")

        # Set window icon
        self.setWindowIcon(QIcon("sal.ico"))
        
        self.setStyleSheet("background-color: #F29829;")

        # Create main layout
        main_layout = QHBoxLayout()

        # Create left menu layout
        left_menu_layout = QVBoxLayout()
        left_menu_layout.setSpacing(10)

        # Create menu buttons
        students_button = QPushButton("ESTUDIANTES")
        tutors_button = QPushButton("TUTORES")
        modalities_button = QPushButton("MODALIDADES")
        assign_button = QPushButton("ASIGNACIÓN TUTOR")
        payment_button = QPushButton("PAGOS")
        evaluation_button = QPushButton("AVANCE EVALUACIÓN")
        phases_button = QPushButton("FASES EVALUACIÓN")


        # Style menu buttons
        for button in [students_button, tutors_button, modalities_button, assign_button, payment_button, evaluation_button, phases_button]:
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #104573; /* Color de fondo */
                    border: 2px solid #D9A73C; /* Borde */
                    border-radius: 10px; /* Esquinas redondeadas */
                    font-weight: bold; /* Texto en negrita */
                    font-size: 16px; /* Tamaño de letra */
                    color: #FFFFFF; /* Color del texto (blanco en este caso) */
                    padding: 10px; /* Espaciado interno */
                    transition: background-color 0.3s; /* Efecto de transición al cambiar el color de fondo */
                }

                QPushButton:hover {
                    background-color: #D90718; /* Cambia el color de fondo al pasar el cursor */
                    cursor: pointer; /* Cambia el cursor a una mano */
                }
                """
            )

        # Add menu buttons to left menu layout
        left_menu_layout.addWidget(students_button)
        left_menu_layout.addWidget(tutors_button)
        left_menu_layout.addWidget(modalities_button)
        left_menu_layout.addWidget(assign_button)
        left_menu_layout.addWidget(payment_button)
        left_menu_layout.addWidget(evaluation_button)
        left_menu_layout.addWidget(phases_button)

        # Create right menu layout
        right_menu_layout = QVBoxLayout()
        right_menu_layout.setSpacing(10)
        
        # Title label
        title_label = QLabel("APLICACIÓN DE\nGESTIÓN DE TITULACIÓN")
        title_label.setFont(QFont("Arial", 30))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
            QLabel {
                color: #104573;
                font-weight: bold;
                background-color: #F29829;
                padding: 15px;
                border-radius: 10px;
            }
            """
        )

        # Add image
        image_label = QLabel()
        pixmap = QPixmap("L1.png")  # Ruta de la imagen
        pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Redimensionar la imagen
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_menu_layout.addWidget(title_label)
        right_menu_layout.addWidget(image_label)

        # Add layouts to main layout
        main_layout.addLayout(left_menu_layout)
        main_layout.addLayout(right_menu_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        # Connect buttons to actions
        students_button.clicked.connect(self.open_estudiantes_window)
        tutors_button.clicked.connect(self.open_tutores_window)
        modalities_button.clicked.connect(self.open_modalidades_window)
        assign_button.clicked.connect(self.open_asignacion_tutor_window)
        payment_button.clicked.connect(self.open_pagos_window)
        evaluation_button.clicked.connect(self.open_avance_evaluacion_window)
        phases_button.clicked.connect(self.open_fases_evaluacion_window)
        

    def open_estudiantes_window(self):
        self.estudiantes_window = EstudiantesApp()
        self.estudiantes_window.show()

    def open_tutores_window(self):
        self.tutores_window = TutoresApp()
        self.tutores_window.show()

    def open_modalidades_window(self):
        self.modalidades_window = ModalidadesApp()
        self.modalidades_window.show()

    def open_asignacion_tutor_window(self):
        self.asignacion_tutor_window = AsignacionApp()
        self.asignacion_tutor_window.show()

    def open_pagos_window(self):
        self.pagos_window = PagosTitulacionApp()
        self.pagos_window.show()

    def open_avance_evaluacion_window(self):
        self.avance_evaluacion_window = AvanceEvaluacionApp()
        self.avance_evaluacion_window.show()

    def open_fases_evaluacion_window(self):
        self.fases_evaluacion_window = FasesEvaluacionApp()
        self.fases_evaluacion_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.resize(600, 400)  # Ajustar tamaño de la ventana principal
    menu.show()
    sys.exit(app.exec())

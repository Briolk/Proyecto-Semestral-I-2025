from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QLabel, QWidget, QMessageBox)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from menu import Menu


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión")
        self.resize(400, 300)
        self.setWindowIcon(QIcon("sal.ico"))

        # Colores
        self.color_primario = "#D90718"
        self.color_secundario = "#2A438C"
        self.color_fondo = "#F2F2F2"
        self.color_texto = "#0D0D0D"

        # Widgets
        self.init_ui()

    def init_ui(self):
        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Imagen del logo (opcional)
        logo_label = QLabel()
        pixmap = QPixmap("L1.png")  # Reemplaza con el nombre de tu imagen
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Campos de texto para usuario y contraseña
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setStyleSheet(f"background-color: {self.color_fondo}; color: {self.color_texto}; padding: 10px; border-radius: 5px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(f"background-color: {self.color_fondo}; color: {self.color_texto}; padding: 10px; border-radius: 5px;")

        # Botón de iniciar sesión
        login_button = QPushButton("Iniciar Sesión")
        login_button.setStyleSheet(f"background-color: {self.color_primario}; color: {self.color_fondo}; padding: 10px; border-radius: 5px; font-size: 14px;")
        login_button.clicked.connect(self.check_login)

        # Agregar widgets al layout
        main_layout.addWidget(logo_label)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(login_button)

        # Establecer el layout central
        self.central_widget.setLayout(main_layout)

    def check_login(self):
        """Verifica si las credenciales son correctas."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Lógica de validación (aquí podrías usar una base de datos o archivo para validar)
        if username == "admin" and password == "1234":
            QMessageBox.information(self, "Éxito", "Bienvenido, has iniciado sesión correctamente.")
            self.open_menu()  # Abre el menú después de login exitoso
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos. Intenta nuevamente.")

    def open_menu(self):
        """Abre el menú principal después del inicio de sesión exitoso."""
        self.menu_window = Menu()
        self.menu_window.show()
        self.close()  # Cierra la ventana de login


if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout,
    QVBoxLayout, QFormLayout, QMessageBox, QDialog
)
from entities.User import User
from PySide6.QtGui import QPixmap, QFont, QCursor
from PySide6.QtCore import Qt
from pathlib import Path
import sys


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Flow - Inicio de sesión")
        self.valid_login = False
        self.setFixedSize(800, 500)
        self.setStyleSheet("background-color: #2D2D30;")
        
        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # === LADO IZQUIERDO ===
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #1c1c1e")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)

        # Imagen o ícono de cajas
        BASE_DIR = Path(__file__).resolve().parent
        logo_path = BASE_DIR / "utils" / "logo_white_letters.svg"
        image_label = QLabel()
        pixmap = QPixmap(str(logo_path))  # Coloca aquí tu imagen
        pixmap = pixmap.scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

    
        left_layout.addWidget(image_label)

        # === LADO DERECHO ===
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #2D2D30;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(60, 60, 60, 80)
        right_layout.setSpacing(20)

        # Título
        login_label = QLabel("Bienvenido")
        login_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        login_label.setStyleSheet("margin-bottom: 70px;")
        login_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(login_label)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo")
        self.email_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #000;
                background: transparent;
                padding: 5px;
                font-size: 14px;
                margin-bottom: 15px;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #000;
                background: transparent;
                padding: 5px;
                font-size: 14px;
            }
        """)

        form_layout.addRow("👤", self.email_input)
        form_layout.addRow("🔒", self.password_input)
        right_layout.addLayout(form_layout)

        # Enlace de recuperación
        forgot_label = QLabel('<a href="#">¿Olvidaste tu contraseña?</a>')
        forgot_label.setAlignment(Qt.AlignRight)
        forgot_label.setStyleSheet("color: black; font-weight: bold;")
        forgot_label.setOpenExternalLinks(False)
        forgot_label.linkActivated.connect(self.show_forgot_warning)
        right_layout.addWidget(forgot_label)

        
        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #f8cc87;
                color: #1c1c1e;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #fadfbc;
            }
        """)
        right_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        self.login_button.clicked.connect(self.check_login)
        
        # Añadir widgets al layout principal
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 2)

    def check_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Stockflow", "Por favor ingrese correo y contraseña")
            return

            # LLAMADA A LA BASE DE DATOS
        user_logged_in = User.authenticate(email, password)

        if user_logged_in:
            self.valid_login = True
            self.accept()  # Cierra el diálogo con resultado positivo
        else:
            self.valid_login = False
            QMessageBox.warning(self, "Stockflow", "Usuario o contraseña incorrectos")
            
    def show_forgot_warning(self):
            QMessageBox.warning(self, "Stockflow", "Contacta al administrador")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

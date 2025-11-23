from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout,
    QVBoxLayout, QFormLayout, QMessageBox, QDialog, QFrame
)
from entities.User import User
from PySide6.QtGui import QPixmap, QFont, QCursor
from PySide6.QtCore import Qt, QSize
from pathlib import Path
import sys
import random
import qtawesome as qta
from ui.utils.common_widgets import GlowLabel

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Flow - Inicio de sesión")
        self.valid_login = False
        self.setFixedSize(850, 550)
        self.setStyleSheet("background-color: #2D2D30;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #1c1c1e")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignCenter)

        BASE_DIR = Path(__file__).resolve().parent
        logo_path = BASE_DIR / "utils" / "logo_white_letters.svg"
        image_label = QLabel()
        pixmap = QPixmap(str(logo_path))
        pixmap = pixmap.scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(image_label)


        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #2D2D30;")
        right_layout = QVBoxLayout(right_widget)

        right_layout.setContentsMargins(50, 40, 50, 40) 
        right_layout.setSpacing(20)

        welcome = ["Iniciar sesión"]
        welcome_random = random.choice(welcome)

        login_label = GlowLabel(welcome_random, font_size=30)
        login_label.setFont(QFont("Segoe UI", 40, QFont.Bold))
        login_label.setStyleSheet("color: #f7a51b; margin-bottom: 20px;")
        login_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(login_label)


        self.form_container = QFrame()
        self.form_container.setObjectName("FormContainer")

        self.form_container.setStyleSheet("""
            #FormContainer {
                border: 2px solid #f7a51b;
                border-radius: 15px;
                background-color: transparent;
            }
        """)

        container_layout = QVBoxLayout(self.form_container)
        container_layout.setContentsMargins(25, 30, 25, 30)
        container_layout.setSpacing(20)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setVerticalSpacing(15)

        input_style = """
            QLineEdit {
                border: none;
                border-bottom: 2px solid #555;
                background: transparent;
                padding: 5px;
                font-size: 14px;
                color: white;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #f7a51b;
            }
        """

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo")
        self.email_input.setStyleSheet(input_style)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setStyleSheet(input_style)

        lbl_user_icon = QLabel()
        lbl_user_icon.setPixmap(qta.icon('fa5s.user', color='#f7a51b').pixmap(QSize(20, 20)))
        lbl_user_icon.setStyleSheet("border: none;") 

        lbl_pass_icon = QLabel()
        lbl_pass_icon.setPixmap(qta.icon('fa5s.lock', color='#f7a51b').pixmap(QSize(20, 20)))
        lbl_pass_icon.setStyleSheet("border: none;")

        form_layout.addRow(lbl_user_icon, self.email_input)
        form_layout.addRow(lbl_pass_icon, self.password_input)
        
        container_layout.addLayout(form_layout)

        forgot_label = QLabel('<a href="#">¿Olvidaste tu contraseña?</a>')
        forgot_label.setOpenExternalLinks(False)
        forgot_label.setAlignment(Qt.AlignRight)
        forgot_label.setStyleSheet("""
                        QLabel {
                            color: #888;
                            font-weight: bold;
                            border: none;
                        }
                        QLabel:hover {
                            color: #3AA6FF;
                        }
                    """)
        forgot_label.setOpenExternalLinks(False)
        forgot_label.linkActivated.connect(self.show_forgot_warning)
        container_layout.addWidget(forgot_label)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #f7a51b;
                color: #1c1c1e;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f7c774;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        container_layout.addWidget(self.login_button)

        #Fin del marco
        
        right_layout.addWidget(self.form_container)
        right_layout.addStretch()

        self.separator = QFrame()
        self.separator.setFrameShadow(QFrame.Plain)
        self.separator.setFixedWidth(2) 
        self.separator.setStyleSheet("background-color: #f7a51b; border: none;")

        main_layout.addWidget(left_widget, 3.5)
        main_layout.addWidget(self.separator)
        main_layout.addWidget(right_widget, 6.5)

    def check_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            self.show_empty_warning()
            return

        user = User.authenticate(email, password)

        if user:
            self.valid_login = True
            self.user_session = user
            self.accept()
        else:
            self.valid_login = False
            self.user_session = None
            QMessageBox.warning(self, "Stockflow", "Usuario o contraseña incorrectos")
            
    def show_forgot_warning(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Stockflow")
        msg.setText("Si ha olvidado su contraseña o correo electrónico, póngase en contacto con el Administrador o con el departamento de Recursos Humanos.")
        msg.setStandardButtons(QMessageBox.Ok)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #f7a51b;
                color: #1c1c1e;
                padding: 6px 12px;
                border-radius: 8px;
            }
            QMessageBox QPushButton:hover {
                background-color: #f7c774;
            }
        """)

        msg.exec()
        
    def show_empty_warning(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Stockflow")
        msg.setText("Por favor ingrese correo y contraseña")
        msg.setStandardButtons(QMessageBox.Ok)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D30;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background-color: #f7a51b;
                color: #1c1c1e;
                padding: 6px 14px;
                border-radius: 6px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #f7c774;
            }
        """)

        msg.exec()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
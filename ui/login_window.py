from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QPushButton, QVBoxLayout, QLineEdit, QLabel, QWidget
import sys

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.valid_login = False

    def check_login(self):
        if self.user_input.text() == "admin" and self.pass_input.text() == "1234":
            self.valid_login = True
            self.accept()  # cierra el dialogo con resultado aceptado
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación")
        label = QLabel("Bienvenido a la aplicación principal")
        self.setCentralWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginDialog()
    if login.exec(): 
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

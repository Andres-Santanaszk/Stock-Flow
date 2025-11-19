import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon
import qdarktheme

from ui.login_window import LoginDialog
from ui.main_window import MainWindow

BASE_DIR = Path(__file__).resolve().parent

def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    icon_path = BASE_DIR / "ui" / "utils" / "icon.png" 

    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon) # para el login
    else:
        print(f"WARNING: No se encontró el icono en: {icon_path}")

    app.setFont(QFont("Segoe UI"))

    login_dialog = LoginDialog()
    if login_dialog.exec() == LoginDialog.Accepted and login_dialog.valid_login:
        main_window = MainWindow()
        main_window.show()
        app.main_window = main_window
        sys.exit(app.exec())
    else:
        print("INFO: Inicio de sesión cancelado o invalido.")
        sys.exit(0)

if __name__ == "__main__":
    main()
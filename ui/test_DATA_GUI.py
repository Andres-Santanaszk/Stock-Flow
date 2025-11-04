import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from db.connection import get_connection  # usa tu connection.py

def fetch_all_roles():
    """
    Devuelve una lista de tuplas [(name, description), ...] de la tabla roles,
    ordenada por id ascendente.
    """
    conn = None
    try:
        conn = get_connection()  # tal cual, sin setear client_encoding
        with conn, conn.cursor() as cur:
            cur.execute("SELECT name, description FROM roles ORDER BY id ASC;")
            rows = cur.fetchall()
            return rows or []
    except Exception as e:
        print("ERROR DB:", e)
        return []
    finally:
        if conn:
            conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prueba QLabel - Listado de Roles")
        self.resize(700, 400)

        roles = fetch_all_roles()

        if not roles:
            html = "<b>No se encontraron roles.</b>"
        else:
            # Armamos un HTML simple para QLabel
            items = []
            for name, desc in roles:
                safe_name = name or ""
                safe_desc = desc or ""
                items.append(f"<li><b>{safe_name}</b><br><span>{safe_desc}</span></li>")
            html = "<b>Roles en la base:</b><br><ul>" + "".join(items) + "</ul>"

        # QLabel centrado con word wrap
        label = QLabel(html)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop)  # arriba para listas largas
        label.setFont(QFont("Segoe UI", 11))
        label.setTextFormat(Qt.RichText)

        # Contenedor básico
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(label)
        self.setCentralWidget(central)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

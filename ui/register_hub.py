# ui/register_hub.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from pathlib import Path

from ui.item_form import ItemFormWidget
from ui.simple_forms import BrandFormWidget, CategoryFormWidget

# Definimos la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
# 1. ----> [AÑADIDO PARA DEBUG]
print(f"DEBUG: BASE_DIR de register_hub.py es: {BASE_DIR}")

class RegisterHubWidget(QWidget):
    """
    Pantalla con 3 botones grandes (con iconos) que abren diálogos 
    para registrar: Item, Marca y Categoría.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Título (sin cambios)
        self.lbl_title = QLabel("Gestor de Registros")
        self.lbl_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("HubTitle") 

        # 2. Botones (sin cambios)
        self.btn_item = QPushButton("   Registrar Ítem")
        self.btn_brand = QPushButton("   Registrar Marca")
        self.btn_category = QPushButton("   Registrar Categoría")

        # 3. Configuración de botones (sin cambios)
        self._setup_hub_button(self.btn_item, "add_item.svg", "list-add")
        self._setup_hub_button(self.btn_brand, "brands.svg", "bookmark-new")
        self._setup_hub_button(self.btn_category, "add_category.svg", "folder-new")

        # 4. Layout (sin cambios)
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignTop | Qt.AlignHCenter) 
        lay.setContentsMargins(20, 20, 20, 20) 
        lay.setSpacing(15) 
        lay.addWidget(self.lbl_title)
        lay.addSpacing(25) 
        lay.addWidget(self.btn_item)
        lay.addWidget(self.btn_brand)
        lay.addWidget(self.btn_category)
        lay.addStretch()

        # 5. Estilos QSS (sin cambios)
        self.setStyleSheet("""
            #HubTitle {
                color: #f7a51b; 
                margin-bottom: 10px;
            }
            QPushButton {
                min-height: 90px;
                max-width: 450px;
                font-size: 19px;
                font-weight: bold;
                text-align: left;
                padding-left: 25px;
                border-radius: 8px;
                background-color: #3C3F41;
                border: 1px solid #555555;
            }
            QPushButton:hover {
                background-color: #f7c774;
                color: black;
                border: 1px solid #f7a51b;
            }
        """)

        # 6. Conexiones (sin cambios)
        self.btn_item.clicked.connect(self._open_item_dialog)
        self.btn_brand.clicked.connect(self._open_brand_dialog)
        self.btn_category.clicked.connect(self._open_category_dialog)

    def _setup_hub_button(self, button: QPushButton, icon_name: str, fallback_theme_icon: str):
        """
        Helper para configurar los iconos de los botones del Hub.
        """
        icon_path = BASE_DIR / "utils" / icon_name
        
        # 2. ----> [AÑADIDO PARA DEBUG]
        print(f"DEBUG: Buscando ícono en: {icon_path}")
        
        icon = QIcon()
        if icon_path.exists():
            icon.addFile(str(icon_path))
        else:
            # 3. ----> [MODIFICADO PARA DEBUG]
            print(f"ADVERTENCIA: ¡No se encontró el ícono! {icon_path}. Usando fallback.")
            icon = QIcon.fromTheme(fallback_theme_icon)
            
        button.setIcon(icon)
        button.setIconSize(QSize(52, 52))

    # --- Métodos de Diálogo (sin cambios) ---
    
    def _open_item_dialog(self):
        # (código sin cambios)
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar ítem")
        form = ItemFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(520, 500)
        dlg.exec()

    def _open_brand_dialog(self):
        # (código sin cambios)
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar marca")
        form = BrandFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(480, 320)
        dlg.exec()

    def _open_category_dialog(self):
        # (código sin cambios)
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar categoría")
        form = CategoryFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(520, 380)
        dlg.exec()
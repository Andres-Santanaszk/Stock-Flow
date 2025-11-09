from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDialog, 
    QLabel, QToolButton  
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve  
from PySide6.QtGui import QIcon, QFont
from pathlib import Path

from ui.item_form import ItemFormWidget
from ui.brand_form import BrandFormWidget
from ui.category_form import CategoryFormWidget

# Ruta base que apunta a la carpeta 'ui'
BASE_DIR = Path(__file__).resolve().parent

class AnimatedHubButton(QToolButton):
    def __init__(self, text, icon_path, fallback_name, parent=None):
        super().__init__(parent)
        self.setText(text)
        
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        icon = QIcon()
        if icon_path.exists():
            icon.addFile(str(icon_path))
        else:
            icon = QIcon.fromTheme(fallback_name)
        self.setIcon(icon)

        self.small_icon_size = QSize(48, 48)
        self.large_icon_size = QSize(60, 60) # Tamaño al hacer hover
        self.setIconSize(self.small_icon_size)

        self.grow_animation = QPropertyAnimation(self, b"iconSize")
        self.grow_animation.setEndValue(self.large_icon_size)
        self.grow_animation.setDuration(150) # milisegundos
        self.grow_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Animación para "encoger" (Leave)
        self.shrink_animation = QPropertyAnimation(self, b"iconSize")
        self.shrink_animation.setEndValue(self.small_icon_size)
        self.shrink_animation.setDuration(150)
        self.shrink_animation.setEasingCurve(QEasingCurve.OutQuad)

    def enterEvent(self, event):
        self.shrink_animation.stop()
        self.grow_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.grow_animation.stop()
        self.shrink_animation.start()
        super().leaveEvent(event)

class RegisterHubWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lbl_title = QLabel("Gestor de Registros")
        self.lbl_title.setFont(QFont("Segoe UI", 30, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("HubTitle") 

        self.btn_item = AnimatedHubButton(
            "Registrar Ítem", 
            BASE_DIR / "utils" / "add_item.svg", 
            "list-add"
        )
        self.btn_brand = AnimatedHubButton(
            "Registrar Marca", 
            BASE_DIR / "utils" / "brands.svg", 
            "bookmark-new"
        )
        self.btn_category = AnimatedHubButton(
            "Registrar Categoría", 
            BASE_DIR / "utils" / "add_category.svg", 
            "folder-new"
        )

        # 3. Layout (MODIFICADO para centrar y poner en horizontal)
        
        # Layout para los botones (Horizontal)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(25) # Espacio entre botones
        button_layout.addWidget(self.btn_item)
        button_layout.addWidget(self.btn_brand)
        button_layout.addWidget(self.btn_category)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter) 
        main_layout.setContentsMargins(20, 20, 20, 20) 
        main_layout.setSpacing(30) 

        main_layout.addWidget(self.lbl_title)
        main_layout.addLayout(button_layout) # <-- Añade el layout horizontal

        # 4. Estilos QSS (MODIFICADO para QToolButton)
        self.setStyleSheet("""
            #HubTitle {
                color: #f7a51b; 
                margin-bottom: 10px;
            }
            
            QToolButton {
                /* Quitamos text-align y padding-left, QToolButton lo maneja */
                min-height: 140px;    /* <-- Alto del botón */
                min-width: 160px;     /* <-- Ancho del botón */
                font-size: 16px;      /* <-- Tamaño de texto */
                font-weight: bold;
                padding: 15px;        /* Padding interno */
                border-radius: 8px;
                
                background-color: #3C3F41;
                border: 1px solid #555555;
            }
            QToolButton:hover {
                background-color: #f7c774;
                color: black;
                border: 1px solid #f7a51b;
            }
        """)

        self.btn_item.clicked.connect(self._open_item_dialog)
        self.btn_brand.clicked.connect(self._open_brand_dialog)
        self.btn_category.clicked.connect(self._open_category_dialog)

    def _open_item_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar ítem")
        form = ItemFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(850, 620)
        dlg.exec()

    def _open_brand_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar marca")
        form = BrandFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(600, 500)
        dlg.exec()

    def _open_category_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar categoría")
        form = CategoryFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(600, 500)
        dlg.exec()
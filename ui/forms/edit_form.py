from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, 
    QDialog, QToolButton, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from ui.utils.common_widgets import IconHoverAnimationMixin

from ui.forms.update_item_form import UpdateItemForm
from ui.forms.update_brand_form import UpdateBrandForm
from ui.forms.update_category_form import UpdateCategoryForm
from ui.forms.update_location_form import UpdateLocationForm

BASE_DIR = Path(__file__).resolve().parents[1]

class AnimatedHubButton(IconHoverAnimationMixin, QToolButton):
    def __init__(
        self,
        text,
        icon_path,
        fallback_name,
        parent=None,
        base_icon_size=QSize(150, 150),
        hover_icon_size=QSize(170, 170),
    ):
        super().__init__(parent)

        self.setText(text)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        icon = QIcon()
        if icon_path.exists():
            icon.addFile(str(icon_path))
        else:
            icon = QIcon.fromTheme(fallback_name)
        self.setIcon(icon)

        self.ratio_base = base_icon_size
        self.ratio_hover = hover_icon_size

        self._setup_icon_hover_animation(
            base_icon_size=base_icon_size,
            hover_icon_size=hover_icon_size,
        )


class SmartSquareButton(AnimatedHubButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumSize(160, 160)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return width

    def resizeEvent(self, event):
        new_width = event.size().width()
        dynamic_size = int(new_width * 0.5)
        
        self.small_icon_size = QSize(dynamic_size, dynamic_size)
        self.large_icon_size = QSize(dynamic_size + 20, dynamic_size + 20)
        
        if not self.underMouse():
            self.setIconSize(self.small_icon_size)
            
        super().resizeEvent(event)


class UpdateHubWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lbl_title = QLabel("Gestor de Actualizaciones")
        self.lbl_title.setFont(QFont("Segoe UI", 48, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("HubTitle")

        self.lbl_subtitle = QLabel("Selecciona qué deseas modificar")
        self.lbl_subtitle.setFont(QFont("Segoe UI", 18))
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.setObjectName("HubSubtitle")

        self.btn_register_link = QPushButton(
            "¿Necesitas crear un registro nuevo? Hazlo aquí"
        )
        self.btn_register_link.setObjectName("LinkButton")
        self.btn_register_link.setCursor(Qt.PointingHandCursor)

        # Usamos SmartSquareButton igual que en el archivo que funciona
        self.btn_item = SmartSquareButton(
            "Modificar Ítem",
            BASE_DIR / "utils" / "add_item.svg",
            "document-edit"
        )
        self.btn_brand = SmartSquareButton(
            "Modificar Marca",
            BASE_DIR / "utils" / "brands.svg",
            "document-edit"
        )
        self.btn_category = SmartSquareButton(
            "Modificar Categoría",
            BASE_DIR / "utils" / "add_category.svg",
            "document-edit"
        )
        self.btn_location = SmartSquareButton(
            "Modificar Ubicación",
            BASE_DIR / "utils" / "add_location.svg",
            "document-edit"
        )

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        grid_layout.addWidget(self.btn_item, 0, 0)
        grid_layout.addWidget(self.btn_brand, 0, 1)
        grid_layout.addWidget(self.btn_category, 1, 0)
        grid_layout.addWidget(self.btn_location, 1, 1)

        # --- AQUÍ ESTÁ LA LÓGICA DEL CONTAINER QUE FALTABA ---
        center_container = QWidget()
        center_lay = QVBoxLayout(center_container)
        center_lay.addLayout(grid_layout)
        center_container.setMaximumWidth(900) 
        # -----------------------------------------------------

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        main_layout.addWidget(self.lbl_title)
        main_layout.addWidget(self.lbl_subtitle)
        main_layout.addStretch(1)
        
        # Agregamos el container centrado, igual que en RegisterHub
        main_layout.addWidget(center_container, 0, Qt.AlignCenter)
        
        main_layout.addStretch(1)
        main_layout.addWidget(self.btn_register_link)

        self.setStyleSheet("""
            #HubTitle { 
                color: #f7a51b; 
                margin-bottom: 10px; 
            }
            #HubSubtitle { 
                color: #FFFFFF; 
                margin-bottom: 20px; 
            }
            QToolButton {
                font: Segoe UI;
                font-size: 18px; 
                font-weight: bold; 
                padding: 10px;
                border-radius: 12px; 
                background-color: #3C3F41; 
                border: 1px solid #555555;
            }
            QToolButton:hover {
                background-color: #f7c774; 
                color: black; 
                border: 1px solid #f7a51b;
            }
            #LinkButton {
                background-color: transparent; 
                border: none; 
                color: #AAAAAA;
                font-size: 16px; 
                font-weight: bold; 
                padding: 15px; 
                text-align: center;
            }
            #LinkButton:hover { 
                text-decoration: underline; 
                color: #f7a51b; 
            }
        """)

        self.btn_item.clicked.connect(self._open_item_dialog)
        self.btn_brand.clicked.connect(self._open_brand_dialog)
        self.btn_category.clicked.connect(self._open_category_dialog)
        self.btn_location.clicked.connect(self._open_location_dialog)
        self.btn_register_link.clicked.connect(self._open_update_view)

    def _open_item_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Modificar Ítem")
        form = UpdateItemForm(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(850, 620)
        dlg.exec()

    def _open_brand_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Modificar Marca")
        form = UpdateBrandForm(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(600, 500)
        dlg.exec()
        
    def _open_category_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Modificar Categoria")
        form = UpdateCategoryForm(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(600, 500)
        dlg.exec()
        
    def _open_location_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Modificar Ubicación")
        form = UpdateLocationForm(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(600, 500)
        dlg.exec()

    def _open_update_view(self):
        print("Botón de 'Ir a Registro' presionado. Abriendo otra vista...")
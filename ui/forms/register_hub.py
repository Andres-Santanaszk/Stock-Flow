from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDialog,
    QLabel, QToolButton, QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from pathlib import Path

from ui.forms.item_form import ItemFormWidget
from ui.forms.brand_form import BrandFormWidget
from ui.forms.category_form import CategoryFormWidget
from ui.forms.location_form import LocationFormWidget
from ui.utils.common_widgets import IconHoverAnimationMixin

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

        self._setup_icon_hover_animation(
            base_icon_size=base_icon_size,
            hover_icon_size=hover_icon_size,
        )


class RegisterHubWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lbl_title = QLabel("Gestor de Registros")
        self.lbl_title.setFont(QFont("Segoe UI", 48, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("HubTitle")

        self.lbl_subtitle = QLabel("Selecciona una opción para comenzar")
        self.lbl_subtitle.setFont(QFont("Segoe UI", 18))
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.setObjectName("HubSubtitle")

        self.btn_update_link = QPushButton(
            "¿Ya has registrado tu ítem? Actualízalo aquí"
        )
        self.btn_update_link.setObjectName("LinkButton")
        self.btn_update_link.setCursor(Qt.PointingHandCursor)

        self.btn_item = AnimatedHubButton(
            "Registrar Ítem",
            BASE_DIR / "utils" / "add_item.svg",
            "list-add",
        )
        self.btn_brand = AnimatedHubButton(
            "Registrar Marca",
            BASE_DIR / "utils" / "brands.svg",
            "bookmark-new",
        )
        self.btn_category = AnimatedHubButton(
            "Registrar Categoría",
            BASE_DIR / "utils" / "add_category.svg",
            "folder-new",
        )

        self.btn_location = AnimatedHubButton(
            "Registrar ubicacion",
            BASE_DIR / "utils" / "add_location.svg",
            "folder-new",
        )

        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(40)
        top_row_layout.addWidget(self.btn_item)
        top_row_layout.addWidget(self.btn_brand)
        top_row_layout.setAlignment(Qt.AlignCenter)

        bottom_row_layout = QHBoxLayout()
        bottom_row_layout.setSpacing(40)
        bottom_row_layout.addWidget(self.btn_category)
        bottom_row_layout.addWidget(self.btn_location)
        bottom_row_layout.setAlignment(Qt.AlignCenter)

        buttons_container_layout = QVBoxLayout()
        buttons_container_layout.addLayout(top_row_layout)
        buttons_container_layout.addSpacing(30)
        buttons_container_layout.addLayout(bottom_row_layout)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        main_layout.addWidget(self.lbl_title)
        main_layout.addWidget(self.lbl_subtitle)
        main_layout.addStretch(1)
        main_layout.addLayout(buttons_container_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.btn_update_link)

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
                min-height: 250px;
                min-width: 250px;
                font: Segoe UI;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
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
                padding: 10px;
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
        self.btn_update_link.clicked.connect(self._open_update_view)
        self.btn_location.clicked.connect(self._open_location_dialog)

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

    def _open_location_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Registrar ubicacion")
        form = LocationFormWidget(dlg)
        lay = QVBoxLayout(dlg)
        lay.addWidget(form)
        dlg.resize(600, 500)
        dlg.exec()

    def _open_update_view(self):
        print("Botón de 'Actualizar' presionado. Abriendo otra vista...")

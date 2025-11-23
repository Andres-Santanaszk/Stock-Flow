from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QPushButton, QDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from pathlib import Path

from ui.utils.common_widgets import IconHoverAnimationMixin


from ui.forms.update_item_form import UpdateItemForm
from ui.forms.update_brand_form import UpdateBrandForm
from ui.forms.update_category_form import UpdateCategoryForm
from ui.forms.update_location_form import UpdateLocationForm

BASE_DIR = Path(__file__).resolve().parents[1]

class AnimatedHubButton(IconHoverAnimationMixin, QToolButton):
    # (Tu código del botón se queda EXACTAMENTE IGUAL, no lo toqué)
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


class UpdateHubWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # --- INTERFAZ VISUAL (SE QUEDA IGUAL) ---
        
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

        # Botones
        self.btn_item = AnimatedHubButton(
            "Modificar Ítem",
            BASE_DIR / "utils" / "add_item.svg",
            "document-edit",
        )
        self.btn_brand = AnimatedHubButton(
            "Modificar Marca",
            BASE_DIR / "utils" / "brands.svg",
            "document-edit",
        )
        self.btn_category = AnimatedHubButton(
            "Modificar Categoría",
            BASE_DIR / "utils" / "add_category.svg",
            "document-edit",
        )
        self.btn_location = AnimatedHubButton(
            "Modificar Ubicación",
            BASE_DIR / "utils" / "add_location.svg",
            "document-edit",
        )

        # Layouts
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
        main_layout.addWidget(self.btn_register_link)

        # Estilos
        self.setStyleSheet("""
            #HubTitle { color: #f7a51b; margin-bottom: 10px; }
            #HubSubtitle { color: #FFFFFF; margin-bottom: 20px; }
            QToolButton {
                min-height: 260px; min-width: 300px; font: Segoe UI;
                font-size: 18px; font-weight: bold; padding: 15px;
                border-radius: 8px; background-color: #3C3F41; border: 1px solid #555555;
            }
            QToolButton:hover {
                background-color: #f7c774; color: black; border: 1px solid #f7a51b;
            }
            #LinkButton {
                background-color: transparent; border: none; color: #AAAAAA;
                font-size: 16px; font-weight: bold; padding: 10px; text-align: center;
            }
            #LinkButton:hover { text-decoration: underline; color: #f7a51b; }
        """)

        # --- CAMBIO 2: CONEXIONES A LOS MÉTODOS ACTUALIZADOS ---
        self.btn_item.clicked.connect(self._open_item_dialog)
        self.btn_brand.clicked.connect(self._open_brand_dialog)
        self.btn_category.clicked.connect(self._open_category_dialog)
        self.btn_register_link.clicked.connect(self._open_update_view)
        self.btn_location.clicked.connect(self._open_location_dialog)
        
        

    # --- CAMBIO 3: MÉTODOS SIMPLIFICADOS ---
    # Ya no configuramos el diálogo aquí. Simplemente abrimos la clase "Gestora"
    # que contiene la lista y la lógica.
    
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
        print("Botón de 'Actualizar' presionado. Abriendo otra vista...")
        # Aquí tu lógica para cambiar de pantalla en el MainWindow
        
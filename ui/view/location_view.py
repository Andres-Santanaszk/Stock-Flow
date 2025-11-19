from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDialog,
    QLabel, QToolButton, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from pathlib import Path

from ui.forms.item_form import ItemFormWidget
from ui.forms.brand_form import BrandFormWidget
from ui.forms.category_form import CategoryFormWidget
from ui.forms.location_form import LocationFormWidget
from ui.utils.common_widgets import IconHoverAnimationMixin
from entities.Location import Location

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


class view_location(QWidget):
    TYPE_INDEX = 1
    CODE_INDEX = 2

    def __init__(self, parent=None):
        super().__init__(parent)

        try:
            self.all_locations_data = Location.get_all_locations_data()
        except Exception as e:
            print(
                f"ERROR: No se pudieron cargar datos iniciales de Location: {e}")
            self.all_locations_data = []

        self.lbl_title = QLabel("Localizaciones")
        self.lbl_title.setFont(QFont("Segoe UI", 48, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("HubTitle")

        self.lbl_subtitle = QLabel("Estado de las localizaciones")
        self.lbl_subtitle.setFont(QFont("Segoe UI", 18))
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.setObjectName("HubSubtitle")

        self.btn_update_link = QPushButton("actualizar tabla")
        self.btn_update_link.setObjectName("LinkButton")
        self.btn_update_link.setCursor(Qt.PointingHandCursor)
        self.btn_update_link.clicked.connect(self.load_locations_data)

        self.cmb_filter_field = QComboBox()
        self.cmb_filter_field.addItem("Tipo", userData=self.TYPE_INDEX)
        self.cmb_filter_field.addItem("Código", userData=self.CODE_INDEX)
        self.cmb_filter_field.setFixedWidth(120)
        self.cmb_filter_field.currentIndexChanged.connect(
            self._update_filter_values)

        self.cmb_filter_value = QComboBox()
        self.cmb_filter_value.setFixedWidth(200)
        self.cmb_filter_value.currentIndexChanged.connect(
            self.load_locations_data)

        self.table_locations = QTableWidget()
        self._setup_table()

        main_layout = QVBoxLayout()
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Filtrar por:"))
        filter_layout.addWidget(self.cmb_filter_field)
        filter_layout.addWidget(self.cmb_filter_value)
        filter_layout.addStretch(1)

        main_layout.addWidget(self.lbl_title)
        main_layout.addWidget(self.lbl_subtitle)

        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table_locations)

        main_layout.addStretch(1)
        main_layout.addWidget(self.btn_update_link)

        self.setLayout(main_layout)
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
                min-height: 260px;
                min-width: 300px;
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
        self._update_filter_values()

    def _setup_table(self):
        headers = ["Tipo", "Codigo", "Descripciòn", "Estado"]
        self.table_locations.setColumnCount(len(headers))
        self.table_locations.setHorizontalHeaderLabels(headers)
        header = self.table_locations.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table_locations.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_locations.setSelectionBehavior(QTableWidget.SelectRows)

    def _update_filter_values(self):
        """Actualiza cmb_filter_value basándose en la selección de cmb_filter_field."""

        filter_index = self.cmb_filter_field.currentData()
        field_name = self.cmb_filter_field.currentText()
        unique_values = sorted(
            list(set(item[filter_index] for item in self.all_locations_data)))
        self.cmb_filter_value.blockSignals(True)
        self.cmb_filter_value.clear()
        self.cmb_filter_value.addItem(f"Todos los {field_name}s")
        self.cmb_filter_value.addItems(unique_values)
        self.cmb_filter_value.blockSignals(False)
        self.load_locations_data()

    def load_locations_data(self):
        try:
            filter_index = self.cmb_filter_field.currentData()
            selected_value = self.cmb_filter_value.currentText()

            locations_data_to_display = self.all_locations_data
            if self.cmb_filter_value.currentIndex() != 0:
                locations_data_to_display = [
                    row for row in self.all_locations_data if row[filter_index] == selected_value
                ]

            self.table_locations.setRowCount(0)
            self.location_ids = []

            if not locations_data_to_display:
                return

            self.table_locations.setRowCount(len(locations_data_to_display))

            for row_idx, row_data in enumerate(locations_data_to_display):
                id_location, type_val, code_val, desc_val, active_val = row_data
                self.location_ids.append(id_location)
                self.table_locations.setItem(
                    row_idx, 0, QTableWidgetItem(type_val))
                item_code = QTableWidgetItem(code_val)
                item_code.setTextAlignment(Qt.AlignCenter)
                self.table_locations.setItem(row_idx, 1, item_code)
                self.table_locations.setItem(
                    row_idx, 2, QTableWidgetItem(desc_val))
                active_text = "Activo" if active_val else "Inactivo"
                item_active = QTableWidgetItem(active_text)
                item_active.setTextAlignment(Qt.AlignCenter)
                self.table_locations.setItem(row_idx, 3, item_active)

        except Exception as e:
            print(f"Error al cargar datos de localizaciones: {e}")
            self.lbl_subtitle.setText(f"ERROR al cargar datos: {e}")
            self.lbl_subtitle.setStyleSheet("#HubSubtitle { color: red; }")

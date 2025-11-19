from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QDialog,
    QLabel, QToolButton, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox,)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from pathlib import Path

from ui.forms.item_form import ItemFormWidget
from ui.forms.brand_form import BrandFormWidget
from ui.forms.category_form import CategoryFormWidget
from ui.forms.location_form import LocationFormWidget
from ui.utils.common_widgets import IconHoverAnimationMixin
from entities.Item import Item
from entities.Brand import Brand
from entities.Category import Category
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


class view_item(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._load_metadata()

        self.lbl_title = QLabel("Inventario de Ítems")
        self.lbl_title.setFont(QFont("Segoe UI", 48, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setObjectName("HubTitle")

        self.lbl_subtitle = QLabel("Catálogo de productos")
        self.lbl_subtitle.setFont(QFont("Segoe UI", 18))
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.setObjectName("HubSubtitle")

        self.btn_update_link = QPushButton(
            "actualizar tabla"
        )
        self.btn_update_link.setObjectName("LinkButton")
        self.btn_update_link.setCursor(Qt.PointingHandCursor)
        self.btn_update_link.clicked.connect(self.load_items_data)

        self.cmb_brand = QComboBox()
        self.cmb_brand.setFixedWidth(200)

        self.cmb_brand.currentIndexChanged.connect(self.load_items_data)

        self.cmb_category = QComboBox()
        self.cmb_category.setFixedWidth(200)
        self.cmb_category.currentIndexChanged.connect(self.load_items_data)

        self.table_items = QTableWidget()
        self._setup_table()

        main_layout = QVBoxLayout()
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Marca:"))
        filter_layout.addWidget(self.cmb_brand)
        filter_layout.addWidget(QLabel("Categoría:"))
        filter_layout.addWidget(self.cmb_category)
        filter_layout.addStretch(1)

        main_layout.addWidget(self.lbl_title)
        main_layout.addWidget(self.lbl_subtitle)

        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table_items)

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
            QComboBox {
                padding: 5px;
                border-radius: 4px;
                background-color: #3C3F41;
                border: 1px solid #555555;
                color: white;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
            }
        """)
        self.load_items_data(initial_load=True)

    def _load_metadata(self):
        try:
            self.brands_map = {id_: name for id_,
                               name in Brand.get_all_brands()}
            self.categories_map = {id_: name for id_,
                                   name in Category.get_all_categories()}
            self.brands_name_map = {name: id_ for id_,
                                    name in Brand.get_all_brands()}
            self.categories_name_map = {
                name: id_ for id_, name in Category.get_all_categories()}
        except Exception as e:
            print(
                f"Advertencia: No se pudo cargar metadatos (Marcas/Categorías): {e}")
            self.brands_map = {}
            self.categories_map = {}
            self.brands_name_map = {}
            self.categories_name_map = {}

    def _populate_comboboxes(self):

        current_brand = self.cmb_brand.currentText()
        self.cmb_brand.blockSignals(True)
        self.cmb_brand.clear()
        self.cmb_brand.addItem("Todas las Marcas", userData=None)

        brand_names = sorted(self.brands_name_map.keys())
        for name in brand_names:
            self.cmb_brand.addItem(name, userData=self.brands_name_map[name])

        index = self.cmb_brand.findText(current_brand)
        if index != -1:
            self.cmb_brand.setCurrentIndex(index)
        self.cmb_brand.blockSignals(False)

        current_category = self.cmb_category.currentText()
        self.cmb_category.blockSignals(True)
        self.cmb_category.clear()
        self.cmb_category.addItem("Todas las Categorías", userData=None)

        category_names = sorted(self.categories_name_map.keys())
        for name in category_names:
            self.cmb_category.addItem(
                name, userData=self.categories_name_map[name])

        index = self.cmb_category.findText(current_category)
        if index != -1:
            self.cmb_category.setCurrentIndex(index)
        self.cmb_category.blockSignals(False)

    def _setup_table(self):
        headers = ["Nombre", "SKU", "Marca", "Categoría",
                   "Tipo Empaque", "Mínimo", "Estado"]
        self.table_items.setColumnCount(len(headers))
        self.table_items.setHorizontalHeaderLabels(headers)

        header = self.table_items.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.table_items.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_items.setSelectionBehavior(QTableWidget.SelectRows)

    def load_items_data(self, initial_load=False):
        try:
            all_items_data = Item.get_all_items_data()

            if initial_load:
                self._populate_comboboxes()

            selected_brand_id = self.cmb_brand.currentData()
            selected_category_id = self.cmb_category.currentData()

            items_data_to_display = all_items_data

            if selected_brand_id is not None:
                items_data_to_display = [
                    row for row in items_data_to_display if row[4] == selected_brand_id
                ]

            if selected_category_id is not None:
                items_data_to_display = [
                    row for row in items_data_to_display if row[6] == selected_category_id
                ]

            self.table_items.setRowCount(0)
            self.item_ids = []

            if not items_data_to_display:
                return

            self.table_items.setRowCount(len(items_data_to_display))

            for row_idx, row_data in enumerate(items_data_to_display):
                (
                    id_item, name, sku, barcode, brand_id,
                    description, category_id, pack_type, min_qty,
                    active, created_at, updated_at
                ) = row_data

                self.item_ids.append(id_item)

                brand_name = self.brands_map.get(brand_id, f"ID: {brand_id}")
                category_name = self.categories_map.get(
                    category_id, f"ID: {category_id}")
                active_text = "Activo" if active else "Inactivo"

                self.table_items.setItem(row_idx, 0, QTableWidgetItem(name))

                item_sku = QTableWidgetItem(sku)
                item_sku.setTextAlignment(Qt.AlignCenter)
                self.table_items.setItem(row_idx, 1, item_sku)

                self.table_items.setItem(
                    row_idx, 2, QTableWidgetItem(brand_name))

                self.table_items.setItem(
                    row_idx, 3, QTableWidgetItem(category_name))

                item_pack = QTableWidgetItem(pack_type)
                item_pack.setTextAlignment(Qt.AlignCenter)
                self.table_items.setItem(row_idx, 4, item_pack)

                item_min_qty = QTableWidgetItem(str(min_qty))
                item_min_qty.setTextAlignment(Qt.AlignCenter)
                self.table_items.setItem(row_idx, 5, item_min_qty)

                item_active = QTableWidgetItem(active_text)
                item_active.setTextAlignment(Qt.AlignCenter)
                self.table_items.setItem(row_idx, 6, item_active)

        except Exception as e:
            print(f"Error al cargar datos de ítems: {e}")
            self.lbl_subtitle.setText(f"ERROR al cargar datos: {e}")
            self.lbl_subtitle.setStyleSheet("#HubSubtitle { color: red; }")

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFrame, QStyledItemDelegate, QStyle, QFormLayout, QLineEdit, QComboBox,
    QScrollArea
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QIcon, QColor
from pathlib import Path
import qtawesome as qta

from entities.Item import Item
from entities.ItemLocation import ItemLocation
from entities.Movement import Movement
from ui.translations import MOV_TYPE_ES, MOV_REASON_ES


class IDHighlighterDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        target_col = 1
        if (option.state & QStyle.State_Selected) and index.column() == target_col:
            painter.save()
            color = QColor("#f7a51b")
            width = 6
            rect = option.rect
            bar_rect = QRect(rect.left(), rect.top(), width, rect.height())
            painter.fillRect(bar_rect, color)
            painter.restore()


class ItemDetailPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DetailPanel")
        self.setFixedWidth(380)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")

        self.content_widget = QWidget()
        self.layout = QVBoxLayout(self.content_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        lbl_header = QLabel("Detalles del Ítem")
        lbl_header.setObjectName("PanelHeader")
        self.layout.addWidget(lbl_header)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setObjectName("PanelLine")
        self.layout.addWidget(line)

        self.lbl_name = QLabel()
        self.lbl_name.setObjectName("PanelName")
        self.lbl_name.setWordWrap(True)
        self.layout.addWidget(self.lbl_name)

        self.lbl_sku = QLabel()
        self.lbl_sku.setObjectName("PanelEmail")
        self.layout.addWidget(self.lbl_sku)

        self.layout.addSpacing(10)

        info_layout = QFormLayout()
        info_layout.setHorizontalSpacing(15)
        info_layout.setVerticalSpacing(5)

        self.lbl_brand = QLabel("-")
        self.lbl_category = QLabel("-")
        self.lbl_min = QLabel("-")

        for lbl in [self.lbl_brand, self.lbl_category, self.lbl_min]:
            lbl.setObjectName("PanelValue")
            lbl.setAlignment(Qt.AlignRight)

        def create_row(label, widget):
            l = QLabel(label)
            l.setObjectName("PanelLabel")
            info_layout.addRow(l, widget)

        create_row("Marca:", self.lbl_brand)
        create_row("Categoría:", self.lbl_category)
        create_row("Min. Stock:", self.lbl_min)

        self.layout.addLayout(info_layout)
        self.layout.addSpacing(15)

        self.lbl_stock_total = QLabel("Total: -")
        self.lbl_stock_total.setObjectName("PanelStatus")
        self.lbl_stock_total.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_stock_total)

        self.layout.addSpacing(15)

        lbl_locs = QLabel("📍 Ubicaciones Actuales")
        lbl_locs.setStyleSheet(
            "color: #f7a51b; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.layout.addWidget(lbl_locs)

        self.lbl_locations_detail = QLabel("Sin datos.")
        self.lbl_locations_detail.setWordWrap(True)
        self.lbl_locations_detail.setStyleSheet(
            "color: #ddd; font-size: 13px; margin-left: 10px;")
        self.layout.addWidget(self.lbl_locations_detail)

        self.layout.addSpacing(10)
        lbl_movs = QLabel("🕒 Últimos 2 Movimientos")
        lbl_movs.setStyleSheet(
            "color: #f7a51b; font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.layout.addWidget(lbl_movs)

        self.lbl_last_moves = QLabel("Sin movimientos recientes.")
        self.lbl_last_moves.setWordWrap(True)
        self.lbl_last_moves.setStyleSheet(
            "color: #ddd; font-size: 13px; margin-left: 10px;")
        self.layout.addWidget(self.lbl_last_moves)

        self.layout.addStretch()

        self.scroll_area.setWidget(self.content_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)

        self.reset_panel()

    def reset_panel(self):
        self.lbl_name.setText("Seleccione un ítem...")
        self.lbl_name.setStyleSheet("color: #777;")
        self.lbl_sku.setText("")
        self.lbl_brand.setText("-")
        self.lbl_category.setText("-")
        self.lbl_min.setText("-")
        self.lbl_stock_total.setText("")
        self.lbl_locations_detail.setText("-")
        self.lbl_last_moves.setText("-")

    def update_data(self, item_id):
        details = Item.get_details_for_panel(item_id)
        total_stock = Item.get_total_stock(item_id)

        if details:
            self.lbl_name.setText(details['name'])
            self.lbl_name.setStyleSheet("color: #f7a51b;")
            self.lbl_sku.setText(f"SKU: {details['sku']}")
            self.lbl_brand.setText(details['brand_name'])
            self.lbl_category.setText(details['category_name'])
            self.lbl_min.setText(str(details['min']))

            self.lbl_stock_total.setText(f"{total_stock} unidades.")
            if total_stock <= details['min']:
                self.lbl_stock_total.setStyleSheet(
                    "color: #EF5350; font-size: 22px; font-weight: bold;")
            else:
                self.lbl_stock_total.setStyleSheet(
                    "color: #28a745; font-size: 22px; font-weight: bold;")

        locs = ItemLocation.list_by_item(item_id)
        if locs:
            html_locs = ""
            for l in locs:
                html_locs += f"• <b>{l['code']}</b>: <span style='color:#fff'>{l['qty']}</span> <i style='color:#aaa'>({l['type']})</i><br>"
            self.lbl_locations_detail.setText(html_locs)
            self.lbl_locations_detail.setTextFormat(Qt.RichText)
        else:
            self.lbl_locations_detail.setText("No hay stock asignado.")

        moves = Movement.get_last_movements_by_item(item_id, limit=2)
        if moves:
            html_movs = ""
            for m in moves:
                m_type = MOV_TYPE_ES.get(m[0], m[0])
                m_reason = MOV_REASON_ES.get(m[1], m[1])
                qty = m[2]
                date_str = m[3].strftime("%d/%m %H:%M")
                from_c = m[4]
                to_c = m[5]

                color = "#28a745" if m[0] == "IN" else "#EF5350"

                route = ""
                if m[0] == "IN":
                    route = f"➜ {to_c}"
                elif m[0] == "OUT":
                    route = f"De {from_c} ➜ Fuera"
                elif m[0] == "ADJUST":
                    route = f"En {from_c or to_c}"
                else:
                    route = f"{from_c} ➜ {to_c}"

                html_movs += f"""
                <div style='margin-bottom: 8px;'>
                    <span style='color:{color}; font-weight:bold;'>{m_type} ({m_reason})</span>
                    <span style='color:#fff; float:right;'>Cant: {qty}</span><br>
                    <span style='color:#aaa; font-size:11px;'>{date_str} | {route}</span>
                </div>
                """
            self.lbl_last_moves.setText(html_movs)
            self.lbl_last_moves.setTextFormat(Qt.RichText)
        else:
            self.lbl_last_moves.setText("Sin historial reciente.")


class view_item(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lbl_title = QLabel("Inventario")
        self.lbl_title.setObjectName("MainTitle")

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Buscar por Nombre o SKU...")
        self.txt_search.setObjectName("SearchInput")
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.addAction(
            qta.icon('fa5s.search', color='#aaaaaa'), QLineEdit.LeadingPosition)
        self.txt_search.textChanged.connect(self.load_items_data)

        self.cmb_brand_filter = QComboBox()
        self.cmb_brand_filter.setPlaceholderText("Todas las marcas")
        self.cmb_brand_filter.addItem("Todas las marcas", userData=None)
        self._load_brands()
        self.cmb_brand_filter.currentIndexChanged.connect(self.load_items_data)

        self.cmb_cat_filter = QComboBox()
        self.cmb_cat_filter.setPlaceholderText("Todas las categorías")
        self.cmb_cat_filter.addItem("Todas las categorías", userData=None)
        self._load_categories()
        self.cmb_cat_filter.currentIndexChanged.connect(self.load_items_data)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.txt_search, 2)
        controls_layout.addWidget(self.cmb_brand_filter, 1)
        controls_layout.addWidget(self.cmb_cat_filter, 1)
        controls_layout.addStretch()

        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        self.table_frame = QFrame()
        self.table_frame.setObjectName("TableContainer")

        self.table_items = QTableWidget()
        self.table_items.setColumnCount(5)
        self.table_items.setHorizontalHeaderLabels(
            ["ID", "NOMBRE", "SKU", "MARCA", "STOCK"])

        header = self.table_items.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.table_items.verticalHeader().setDefaultSectionSize(45)
        self.table_items.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_items.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_items.setFocusPolicy(Qt.NoFocus)
        self.table_items.setShowGrid(False)
        self.table_items.verticalHeader().setVisible(False)
        self.table_items.setColumnHidden(0, True)

        self.delegate = IDHighlighterDelegate(self.table_items)
        self.table_items.setItemDelegate(self.delegate)
        self.table_items.itemSelectionChanged.connect(
            self._on_selection_changed)

        t_lay = QVBoxLayout(self.table_frame)
        t_lay.setContentsMargins(2, 2, 2, 2)
        t_lay.addWidget(self.table_items)

        self.detail_panel = ItemDetailPanel()

        body_layout.addWidget(self.table_frame, stretch=1)
        body_layout.addWidget(self.detail_panel)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 10, 40, 40)

        main_layout.addWidget(self.lbl_title)
        main_layout.addSpacing(20)
        main_layout.addLayout(controls_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(body_layout)

        self._apply_styles()

    def showEvent(self, event):
        """Se ejecuta automáticamente al mostrar la pestaña, actualizando la tabla."""
        super().showEvent(event)
        self.load_items_data()

    def _load_brands(self):
        try:
            brands = Item.get_all_brands_for_combo()
            for b_id, name in brands:
                self.cmb_brand_filter.addItem(name, userData=name)
        except:
            pass

    def _load_categories(self):
        try:
            cats = Item.get_all_categories_for_combo()
            for c_id, name in cats:
                self.cmb_cat_filter.addItem(name, userData=name)
        except:
            pass

    def load_items_data(self):
        try:
            search = self.txt_search.text().strip()
            brand_val = self.cmb_brand_filter.currentData()
            cat_val = self.cmb_cat_filter.currentData()

            filter_f = None
            filter_v = None
            if brand_val:
                filter_f = 'brand'
                filter_v = brand_val
            elif cat_val:
                filter_f = 'category'
                filter_v = cat_val

            items = Item.get_items_for_display(
                filter_field=filter_f,
                filter_value=filter_v,
                search_term=search
            )

            current_row = self.table_items.currentRow()
            selected_id = None
            if current_row >= 0:
                selected_id = self.table_items.item(current_row, 0).text()

            self.table_items.setRowCount(0)
            self.detail_panel.reset_panel()

            for row_idx, row_data in enumerate(items):
                (id_item, name, sku, _, _, _, brand_name, _, stock) = row_data

                self.table_items.insertRow(row_idx)

                item_id = QTableWidgetItem(str(id_item))
                item_id.setTextAlignment(Qt.AlignCenter)
                self.table_items.setItem(row_idx, 0, item_id)

                self.table_items.setItem(row_idx, 1, QTableWidgetItem(name))
                self.table_items.setItem(row_idx, 2, QTableWidgetItem(sku))
                self.table_items.setItem(
                    row_idx, 3, QTableWidgetItem(brand_name))

                item_stock = QTableWidgetItem(str(stock))
                item_stock.setTextAlignment(Qt.AlignCenter)
                self.table_items.setItem(row_idx, 4, item_stock)

                if selected_id and str(id_item) == selected_id:
                    self.table_items.selectRow(row_idx)

        except Exception as e:
            print(f"Error loading items: {e}")

    def _on_selection_changed(self):
        selected = self.table_items.selectedItems()
        if not selected:
            self.detail_panel.reset_panel()
            return

        row = selected[0].row()
        id_item = int(self.table_items.item(row, 0).text())
        self.detail_panel.update_data(id_item)

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: "Segoe UI"; }
            
            #MainTitle { color: #f7a51b; font-size: 54px; font-weight: 800; margin-left: -15px; }
            #SubTitle { color: #FFFFFF; font-size: 24px; font-weight: 600; }
            
            #SearchInput, QComboBox {
                background-color: #3c3f41;
                border: 2px solid #444444;
                border-radius: 8px;
                padding: 5px 15px; 
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                height: 35px;
            }
            #SearchInput:focus, QComboBox:focus { border: 2px solid #f7a51b; }

            #TableContainer { background-color: #3c3f41; border: 1px solid #555; border-radius: 10px; }
            QTableWidget { background-color: #3c3f41; border: none; color: #ffffff; font-size: 15px; font-weight: 500; }
            QHeaderView::section {
                background-color: #3c3f41; color: #f7a51b; font-weight: 800;
                font-size: 13px; text-transform: uppercase; border: none;
                border-bottom: 2px solid #555; padding: 8px;
            }
            QTableWidget::item { padding-left: 10px; border-bottom: 1px solid #444; }
            QTableWidget::item:selected { background-color: #454545; color: #f7a51b; }

            #DetailPanel { background-color: #3c3f41; border: 1px solid #555555; border-radius: 8px; }
            #DetailPanel QLabel { background-color: transparent; }
            #PanelHeader { color: #FFFFFF; font-size: 18px; font-weight: bold; }
            #PanelLine { border: none; background-color: #FFFFFF; max-height: 1px; height: 1px; }
            #PanelName { font-size: 22px; font-weight: 800; color: #f7a51b; }
            #PanelEmail { color: #ccc; font-size: 14px; font-weight: 600; }
            #PanelLabel { color: #FFFFFF; font-size: 14px; font-weight: bold; }
            #PanelValue { color: #ffffff; font-size: 14px; }
            #PanelStatus { font-size: 20px; font-weight: bold; }
            
            QScrollBar:vertical { border: none; background: #2b2b2b; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #555; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #f7a51b; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

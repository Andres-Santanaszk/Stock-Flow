from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFrame, QStyledItemDelegate, QStyle, QFormLayout, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QIcon, QColor
from pathlib import Path
import qtawesome as qta

from entities.Location import Location
from ui.translations import LOCATION_TYPE_ES


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


class ActionButton(QToolButton):
    def __init__(self, text, icon_name, parent=None):
        super().__init__(parent)
        self.setText(text.upper())
        self.setCursor(Qt.PointingHandCursor)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIcon(qta.icon(icon_name, color="white"))
        self.base_size = QSize(20, 20)
        self.hover_size = QSize(26, 26)
        self.setIconSize(self.base_size)
        self.anim_grow = QPropertyAnimation(self, b"iconSize")
        self.anim_grow.setDuration(150)
        self.anim_grow.setEndValue(self.hover_size)
        self.anim_shrink = QPropertyAnimation(self, b"iconSize")
        self.anim_shrink.setDuration(150)
        self.anim_shrink.setEndValue(self.base_size)

    def enterEvent(self, event):
        self.anim_shrink.stop()
        self.anim_grow.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim_grow.stop()
        self.anim_shrink.start()
        super().leaveEvent(event)


class LocationDetailPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DetailPanel")
        self.setFixedWidth(350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        lbl_header = QLabel("Detalle de Ubicación")
        lbl_header.setObjectName("PanelHeader")
        layout.addWidget(lbl_header)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setObjectName("PanelLine")
        layout.addWidget(line)

        self.lbl_code = QLabel()
        self.lbl_code.setObjectName("PanelName")
        layout.addWidget(self.lbl_code)

        layout.addSpacing(20)

        info_layout = QFormLayout()
        info_layout.setHorizontalSpacing(20)
        info_layout.setVerticalSpacing(15)

        self.lbl_id = QLabel("-")
        self.lbl_type = QLabel("-")
        self.lbl_desc = QLabel("-")
        self.lbl_status = QLabel("-")

        for lbl in [self.lbl_id, self.lbl_type, self.lbl_desc, self.lbl_status]:
            lbl.setObjectName("PanelValue")
            lbl.setAlignment(Qt.AlignRight)
            lbl.setWordWrap(True)

        def create_row(label, widget):
            l = QLabel(label)
            l.setObjectName("PanelLabel")
            info_layout.addRow(l, widget)

        create_row("ID Interno:", self.lbl_id)
        create_row("Tipo:", self.lbl_type)
        create_row("Descripción:", self.lbl_desc)
        create_row("Estado:", self.lbl_status)

        layout.addLayout(info_layout)
        layout.addStretch()
        self.reset_panel()

    def reset_panel(self):
        self.lbl_code.setText("Seleccione ubicación...")
        self.lbl_code.setStyleSheet("color: #777;")
        self.lbl_id.setText("-")
        self.lbl_type.setText("-")
        self.lbl_desc.setText("-")
        self.lbl_status.setText("")

    def update_data(self, id_loc, code, type_, desc, active):
        self.lbl_code.setText(code)
        self.lbl_code.setStyleSheet("color: #f7a51b;")
        self.lbl_id.setText(str(id_loc))

        translated_type = LOCATION_TYPE_ES.get(type_, type_)
        self.lbl_type.setText(translated_type)

        self.lbl_desc.setText(desc if desc else "Sin descripción")

        if active:
            self.lbl_status.setText("ACTIVO")
            self.lbl_status.setStyleSheet("color: #28a745; font-weight: bold;")
        else:
            self.lbl_status.setText("INACTIVO")
            self.lbl_status.setStyleSheet("color: #EF5350; font-weight: bold;")


class view_location(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lbl_title = QLabel("Ubicaciones")
        self.lbl_title.setObjectName("MainTitle")

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Buscar por Tipo o Código...")
        self.txt_search.setObjectName("SearchInput")
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.addAction(
            qta.icon('fa5s.search', color='#aaa'), QLineEdit.LeadingPosition)
        self.txt_search.textChanged.connect(self.load_locations_data)

        self.cmb_type_filter = QComboBox()
        self.cmb_type_filter.addItem("Todos los tipos", userData=None)
        self._load_types()
        self.cmb_type_filter.currentIndexChanged.connect(
            self.load_locations_data)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.txt_search, 2)
        controls_layout.addWidget(self.cmb_type_filter, 1)
        controls_layout.addStretch()

        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        self.table_frame = QFrame()
        self.table_frame.setObjectName("TableContainer")

        self.table_locs = QTableWidget()
        self.table_locs.setColumnCount(3)
        self.table_locs.setHorizontalHeaderLabels(["ID", "TIPO", "CÓDIGO"])

        header = self.table_locs.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_locs.verticalHeader().setVisible(False)
        self.table_locs.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_locs.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_locs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_locs.setShowGrid(False)
        self.table_locs.setFocusPolicy(Qt.NoFocus)

        self.table_locs.setColumnHidden(0, True)

        self.delegate = IDHighlighterDelegate(self.table_locs)
        self.table_locs.setItemDelegate(self.delegate)
        self.table_locs.itemSelectionChanged.connect(
            self._on_selection_changed)

        t_lay = QVBoxLayout(self.table_frame)
        t_lay.setContentsMargins(2, 2, 2, 2)
        t_lay.addWidget(self.table_locs)

        self.detail_panel = LocationDetailPanel()

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
        """Actualización automática"""
        super().showEvent(event)
        self.load_locations_data()

    def _load_types(self):
        try:
            types = Location.get_unique_values_for_field("type")
            for t in types:
                translated_text = LOCATION_TYPE_ES.get(t, t)
                self.cmb_type_filter.addItem(translated_text, userData=t)
        except:
            pass

    def load_locations_data(self):
        search = self.txt_search.text().strip()
        type_filter = self.cmb_type_filter.currentData()

        filter_field = "type" if type_filter else None
        filter_val = type_filter

        try:
            data = Location.get_all_locations_data(
                filter_field=filter_field,
                filter_value=filter_val,
                search_term=search
            )

            self.table_locs.setRowCount(0)
            self.detail_panel.reset_panel()

            self.current_data_map = {}

            for row_idx, row_data in enumerate(data):
                self.table_locs.insertRow(row_idx)
                self.current_data_map[row_idx] = row_data

                item_id = QTableWidgetItem(str(row_data[0]))
                item_id.setTextAlignment(Qt.AlignCenter)
                self.table_locs.setItem(row_idx, 0, item_id)
                raw_type = row_data[1]
                translated_type = LOCATION_TYPE_ES.get(raw_type, raw_type)

                self.table_locs.setItem(
                    row_idx, 1, QTableWidgetItem(translated_type))

                # Código
                self.table_locs.setItem(
                    row_idx, 2, QTableWidgetItem(row_data[2]))

        except Exception as e:
            print(e)

    def _on_selection_changed(self):
        selected = self.table_locs.selectedItems()
        if not selected:
            self.detail_panel.reset_panel()
            return

        row = selected[0].row()
        if row in self.current_data_map:
            d = self.current_data_map[row]
            self.detail_panel.update_data(d[0], d[2], d[1], d[3], d[4])

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: "Segoe UI"; }
           
            #MainTitle { color: #f7a51b; font-size: 54px; font-weight: 800; margin-left: -15px; }
            #SubTitle { color: #FFFFFF; font-size: 24px; font-weight: 600; }
           
            #SearchInput, QComboBox {
                background-color: #3c3f41; border: 2px solid #444; border-radius: 8px;
                padding: 5px 15px; color: #fff; font-size: 14px; font-weight: bold; height: 35px;
            }
            #SearchInput:focus, QComboBox:focus { border: 2px solid #f7a51b; }
           
            #BigBtn {
                background-color: #3c3f41; color: #fff; border: 2px solid #444;
                border-radius: 20px; padding: 8px 20px; font-weight: bold; font-size: 14px;
            }
            #BigBtn:hover { background-color: #f7c774; color: black; border: 2px solid #f7a51b; }

            #TableContainer { background-color: #3c3f41; border: 1px solid #555; border-radius: 10px; }
            QTableWidget { background-color: #3c3f41; border: none; color: #fff; font-size: 15px; font-weight: 500; }
            QHeaderView::section {
                background-color: #3c3f41; color: #f7a51b; font-weight: 800;
                font-size: 13px; text-transform: uppercase; border: none;
                border-bottom: 2px solid #555; padding: 8px;
            }
            QTableWidget::item { padding-left: 10px; border-bottom: 1px solid #444; }
            QTableWidget::item:selected { background-color: #454545; color: #f7a51b; }

            #DetailPanel { background-color: #3c3f41; border: 1px solid #555; border-radius: 8px; }
            #DetailPanel QLabel { background-color: transparent; }
            #PanelHeader { color: #fff; font-size: 18px; font-weight: bold; }
            #PanelLine { border: none; background-color: #fff; max-height: 1px; height: 1px; }
            #PanelName { font-size: 22px; font-weight: 800; color: #f7a51b; }
            #PanelLabel { color: #fff; font-size: 14px; font-weight: bold; }
            #PanelValue { color: #fff; font-size: 14px; }
        """)

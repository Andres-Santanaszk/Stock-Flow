from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFrame, QStyledItemDelegate, QStyle, QFormLayout, QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QDate
from PySide6.QtGui import QIcon, QColor
from pathlib import Path
import qtawesome as qta

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


class MovementDetailPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DetailPanel")
        self.setFixedWidth(350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        lbl_header = QLabel("Detalle del Movimiento")
        lbl_header.setObjectName("PanelHeader")
        layout.addWidget(lbl_header)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setObjectName("PanelLine")
        layout.addWidget(line)

        self.lbl_date = QLabel()
        self.lbl_date.setObjectName("PanelName")
        layout.addWidget(self.lbl_date)

        self.lbl_type_main = QLabel()
        self.lbl_type_main.setObjectName("PanelEmail")
        layout.addWidget(self.lbl_type_main)

        layout.addSpacing(20)

        info_layout = QFormLayout()
        info_layout.setHorizontalSpacing(20)
        info_layout.setVerticalSpacing(15)

        self.lbl_item = QLabel("-")
        self.lbl_qty = QLabel("-")
        self.lbl_reason = QLabel("-")
        self.lbl_user = QLabel("-")
        self.lbl_route = QLabel("-")

        for lbl in [self.lbl_item, self.lbl_qty, self.lbl_reason, self.lbl_user, self.lbl_route]:
            lbl.setObjectName("PanelValue")
            lbl.setAlignment(Qt.AlignRight)
            lbl.setWordWrap(True)

        def create_row(label, widget):
            l = QLabel(label)
            l.setObjectName("PanelLabel")
            info_layout.addRow(l, widget)

        create_row("Ítem:", self.lbl_item)
        create_row("Cantidad:", self.lbl_qty)
        create_row("Motivo:", self.lbl_reason)
        create_row("Usuario:", self.lbl_user)
        create_row("Ruta:", self.lbl_route)

        layout.addLayout(info_layout)
        layout.addStretch()
        self.reset_panel()

    def reset_panel(self):
        self.lbl_date.setText("Seleccione un movimiento...")
        self.lbl_date.setStyleSheet("color: #777;")
        self.lbl_type_main.setText("")
        self.lbl_item.setText("-")
        self.lbl_qty.setText("-")
        self.lbl_reason.setText("-")
        self.lbl_user.setText("-")
        self.lbl_route.setText("-")

    def update_data(self, data_tuple):
        dt = data_tuple[1]
        date_str = dt.strftime("%d/%m/%Y %H:%M")

        raw_type = data_tuple[4]
        raw_reason = data_tuple[5]

        t_type = MOV_TYPE_ES.get(raw_type, raw_type)
        t_reason = MOV_REASON_ES.get(raw_reason, raw_reason)

        color = "#ffffff"
        if raw_type == "IN":
            color = "#28a745"
        elif raw_type == "OUT":
            color = "#EF5350"
        elif raw_type == "ADJUST":
            color = "#f7a51b"

        self.lbl_date.setText(date_str)
        self.lbl_date.setStyleSheet("color: #f7a51b;")

        self.lbl_type_main.setText(t_type.upper())
        self.lbl_type_main.setStyleSheet(
            f"color: {color}; font-weight: bold; font-size: 16px;")

        self.lbl_item.setText(f"{data_tuple[2]}\n({data_tuple[3]})")
        self.lbl_qty.setText(str(data_tuple[6]))
        self.lbl_reason.setText(t_reason)
        self.lbl_user.setText(data_tuple[7])

        route = ""
        if raw_type == "IN":
            route = f"Hacia {data_tuple[9]}"
        elif raw_type == "OUT":
            route = f"Desde {data_tuple[8]}"
        else:
            route = f"{data_tuple[8]} ➜ {data_tuple[9]}"
        self.lbl_route.setText(route)


class view_movement(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lbl_title = QLabel("Historial de Movimientos")
        self.lbl_title.setObjectName("MainTitle")
        self.lbl_subtitle = QLabel("Historial completo de transacciones.")
        self.lbl_subtitle.setObjectName("SubTitle")

        self.cmb_type = QComboBox()
        self.cmb_type.addItem("Todos", userData=None)
        for key, val in MOV_TYPE_ES.items():
            self.cmb_type.addItem(val, userData=key)

        self.cmb_type.currentIndexChanged.connect(self.load_data)

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.dateChanged.connect(self.load_data)

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.dateChanged.connect(self.load_data)

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        lbl_t = QLabel("Tipo:")
        lbl_t.setStyleSheet("color:#aaa; font-weight:bold;")
        lbl_d1 = QLabel("Desde:")
        lbl_d1.setStyleSheet("color:#aaa; font-weight:bold;")
        lbl_d2 = QLabel("Hasta:")
        lbl_d2.setStyleSheet("color:#aaa; font-weight:bold;")

        filter_layout.addWidget(lbl_t)
        filter_layout.addWidget(self.cmb_type)
        filter_layout.addSpacing(15)
        filter_layout.addWidget(lbl_d1)
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(lbl_d2)
        filter_layout.addWidget(self.date_to)

        filter_layout.addStretch()

        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)

        self.table_frame = QFrame()
        self.table_frame.setObjectName("TableContainer")

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "FECHA", "ÍTEM", "TIPO", "CANT."])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)

        self.table.setColumnHidden(0, True)

        self.delegate = IDHighlighterDelegate(self.table)
        self.table.setItemDelegate(self.delegate)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)

        t_lay = QVBoxLayout(self.table_frame)
        t_lay.setContentsMargins(2, 2, 2, 2)
        t_lay.addWidget(self.table)

        self.detail_panel = MovementDetailPanel()

        body_layout.addWidget(self.table_frame, stretch=1)
        body_layout.addWidget(self.detail_panel)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 10, 40, 40)

        main_layout.addWidget(self.lbl_title)
        main_layout.addSpacing(5)
        main_layout.addWidget(self.lbl_subtitle)
        main_layout.addSpacing(20)
        main_layout.addLayout(filter_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(body_layout)

        self._apply_styles()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_data()

    def load_data(self):
        type_param = self.cmb_type.currentData()
        d_from = self.date_from.date().toString("yyyy-MM-dd")
        d_to = self.date_to.date().toString("yyyy-MM-dd")

        try:
            data = Movement.get_history_data(
                filter_type=type_param,
                date_from=d_from,
                date_to=d_to
            )

            self.table.setRowCount(0)
            self.detail_panel.reset_panel()
            self.current_data_map = {}

            for row_idx, row_data in enumerate(data):
                self.table.insertRow(row_idx)
                self.current_data_map[row_idx] = row_data

                item_id = QTableWidgetItem(str(row_data[0]))
                self.table.setItem(row_idx, 0, item_id)

                date_short = row_data[1].strftime("%d/%m %H:%M")
                self.table.setItem(row_idx, 1, QTableWidgetItem(date_short))

                self.table.setItem(row_idx, 2, QTableWidgetItem(row_data[2]))

                raw_type = row_data[4]
                t_type = MOV_TYPE_ES.get(raw_type, raw_type)
                item_type = QTableWidgetItem(t_type)
                item_type.setTextAlignment(Qt.AlignCenter)

                if raw_type == "IN":
                    item_type.setForeground(QColor("#28a745"))
                elif raw_type == "OUT":
                    item_type.setForeground(QColor("#EF5350"))
                elif raw_type == "ADJUST":
                    item_type.setForeground(QColor("#f7a51b"))

                self.table.setItem(row_idx, 3, item_type)

                item_qty = QTableWidgetItem(str(row_data[6]))
                item_qty.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, 4, item_qty)

        except Exception as e:
            print(f"Error loading movements: {e}")

    def _on_selection_changed(self):
        selected = self.table.selectedItems()
        if not selected:
            self.detail_panel.reset_panel()
            return

        row = selected[0].row()
        if row in self.current_data_map:
            self.detail_panel.update_data(self.current_data_map[row])

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: "Segoe UI"; }
            
            #MainTitle { color: #f7a51b; font-size: 54px; font-weight: 800; margin-left: -15px; }
            #SubTitle { color: #FFFFFF; font-size: 24px; font-weight: 600; }
            
            /* Estilo IDENTICO a inventory_view (sin hacks de flecha) */
            QComboBox, QDateEdit {
                background-color: #3c3f41;
                border: 2px solid #444444;
                border-radius: 8px;
                padding: 5px 10px; 
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                height: 30px;
                min-width: 120px;
            }
            QComboBox:focus, QDateEdit:focus { border: 2px solid #f7a51b; }

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
        """)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QSpinBox, QLineEdit, QPushButton, 
    QFrame, QGridLayout, QSpacerItem, QSizePolicy,
    QTextEdit
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
import qtawesome as qta
from ui.utils.common_widgets import AnimatedButton

class MovementsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_styles()
        
        # Set default state
        self.set_movement_type("IN")

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.form_frame = QFrame()
        self.form_frame.setObjectName("FormFrame")
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setSpacing(15)

        # 1. Header Title
        title = QLabel("Registro de Movimientos")
        title.setFont(QFont("Segoe UI", 70, QFont.Bold))
        title.setStyleSheet("color: #f7a51b; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)

        # 2. Movement Type Selectors (Toggle Buttons)
        type_layout = QHBoxLayout()
        self.btn_in = self.create_type_button("ENTRADA", "mdi.import", "#4CAF50", "#66BB6A")
        self.btn_out = self.create_type_button("SALIDA", "mdi.export", "#E91511", "#EF5350")
        self.btn_adjust = self.create_type_button("AJUSTE", "mdi.swap-horizontal", "#f7a51b", "#f7c774")
        
        type_layout.addWidget(self.btn_in)
        type_layout.addWidget(self.btn_out)
        type_layout.addWidget(self.btn_adjust)
        form_layout.addLayout(type_layout)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #555555;")
        form_layout.addWidget(line)

        # 3. Form Fields (Grid Layout)
        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)

        # Row 1: SKU/Item Selection
        lbl_item = QLabel("Item / SKU:")
        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText("Escanear código o buscar nombre...")
        self.btn_search_item = QPushButton(qta.icon("mdi.magnify", color="white"), "")
        self.btn_search_item.setFixedWidth(40)
        
        item_layout = QHBoxLayout()
        item_layout.addWidget(self.input_item)
        item_layout.addWidget(self.btn_search_item)
        item_layout.setContentsMargins(0,0,0,0)

        grid.addWidget(lbl_item, 0, 0)
        grid.addLayout(item_layout, 0, 1)

        # Row 2: Quantity
        lbl_qty = QLabel("Cantidad:")
        self.spin_qty = QSpinBox()
        self.spin_qty.setRange(1, 999999)
        self.spin_qty.setFixedHeight(35)
        grid.addWidget(lbl_qty, 1, 0)
        grid.addWidget(self.spin_qty, 1, 1)

        # Row 3: Locations (Dynamic)
        # Based on your SQL: from_location_id vs to_location_id
        lbl_origin = QLabel("Ubicación Origen:")
        self.combo_origin = QComboBox()
        self.combo_origin.addItems(["--- Seleccionar Origen ---", "Bodega A", "Estante 1", "Zona Recepción"])
        
        lbl_dest = QLabel("Ubicación Destino:")
        self.combo_dest = QComboBox()
        self.combo_dest.addItems(["--- Seleccionar Destino ---", "Bodega A", "Estante 1", "Zona Despacho"])

        grid.addWidget(lbl_origin, 2, 0)
        grid.addWidget(self.combo_origin, 2, 1)
        grid.addWidget(lbl_dest, 3, 0)
        grid.addWidget(self.combo_dest, 3, 1)

        # Row 4: Reason (Enum from SQL)
        lbl_reason = QLabel("Motivo:")
        self.combo_reason = QComboBox()
        # Populate with SQL enums placeholders
        self.combo_reason.addItems(["Purchase", "Return In", "Transfer In", "Manufacture Produce"])
        grid.addWidget(lbl_reason, 4, 0)
        grid.addWidget(self.combo_reason, 4, 1)

        form_layout.addLayout(grid)

        # Notes Area
        lbl_notes = QLabel("Comentarios:")
        lbl_notes.setStyleSheet("margin-top: 10px;")
        self.text_notes = QTextEdit()
        self.text_notes.setMaximumHeight(80)
        self.text_notes.setPlaceholderText("Detalles adicionales del movimiento...")
        
        form_layout.addWidget(lbl_notes)
        form_layout.addWidget(self.text_notes)

        form_layout.addStretch()

        # Submit Button
        self.btn_submit = QPushButton("REGISTRAR MOVIMIENTO")
        self.btn_submit.setObjectName("SubmitButton")
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        self.btn_submit.setIcon(qta.icon("mdi.content-save", color="white"))
        self.btn_submit.setIconSize(QSize(20, 20))
        form_layout.addWidget(self.btn_submit)

        # --- Right Panel: Preview / Info (Optional visual aid) ---
        # This helps fill the wide screen and gives feedback to the user
        self.info_frame = QFrame()
        self.info_frame.setObjectName("InfoFrame")
        self.info_frame.setFixedWidth(300)
        info_layout = QVBoxLayout(self.info_frame)
        
        info_title = QLabel("Detalles del Item")
        info_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info_layout.addWidget(info_title)
        
        # Placeholder for item info
        self.lbl_item_name = QLabel("Seleccione un item...")
        self.lbl_item_name.setWordWrap(True)
        self.lbl_item_name.setStyleSheet("color: #B0BEC5; font-size: 14px;")
        
        self.lbl_current_stock = QLabel("Stock Actual: -")
        self.lbl_current_stock.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")

        info_layout.addWidget(self.lbl_item_name)
        info_layout.addWidget(self.lbl_current_stock)
        info_layout.addStretch()
        
        # Add frames to main layout
        main_layout.addWidget(self.form_frame, 70) # 70% width
        main_layout.addWidget(self.info_frame, 30) # 30% width

        # Connect signals
        self.btn_in.clicked.connect(lambda: self.set_movement_type("IN"))
        self.btn_out.clicked.connect(lambda: self.set_movement_type("OUT"))
        self.btn_adjust.clicked.connect(lambda: self.set_movement_type("ADJUST"))

    def create_type_button(self, text, icon_name, accent_color, hover_color):
        btn = AnimatedButton(
            text,
            self,
            base_icon_size=QSize(34, 34),
            hover_icon_size=QSize(44, 44),  # un poco más grande al hacer hover
        )
        btn.setIcon(qta.icon(icon_name, color="white"))
        btn.setCheckable(True)
        btn.setFixedHeight(50)
        btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn.setProperty("accent_color", accent_color)
        btn.setProperty("hover_color", hover_color)
        return btn


    def set_movement_type(self, mov_type):
        """
        Changes visual state based on SQL constraints:
        IN:     To Location (Required), From Location (Null)
        OUT:    From Location (Required), To Location (Null)
        ADJUST: Flexible (Usually From Location -> Null for Scrap)
        """
        # Reset Buttons con Hover Dinámico
        for btn in [self.btn_in, self.btn_out, self.btn_adjust]:
            btn.setChecked(False)
            
            # 1. Recuperamos el color hover específico de este botón
            h_col = btn.property("hover_color")
            
            # 2. Lo aplicamos al estilo inactivo usando f-string
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #2D2D30;
                    border: 1px solid #555;
                    border-radius: 5px;
                    color: #AAA;
                }}
                QPushButton:hover {{ 
                    background-color: {h_col}; 
                    color: white;
                    border: 1px solid {h_col};
                }}
            """)
        # Activate selected button
        if mov_type == "IN":
            active_btn = self.btn_in
            self.combo_origin.setEnabled(False)
            self.combo_dest.setEnabled(True)
            self.combo_origin.setCurrentText("--- N/A (Externo) ---")
            # Populate Reasons for IN
            self.update_reasons(["Purchase", "Return In", "Transfer In", "Manufacture Produce"])

        elif mov_type == "OUT":
            active_btn = self.btn_out
            self.combo_origin.setEnabled(True)
            self.combo_dest.setEnabled(False)
            self.combo_dest.setCurrentText("--- N/A (Externo) ---")
            # Populate Reasons for OUT
            self.update_reasons(["Sale", "Shipping", "Return Out", "Transfer Out", "Manufacture Consume"])

        elif mov_type == "ADJUST":
            active_btn = self.btn_adjust
            self.combo_origin.setEnabled(True)
            self.combo_dest.setEnabled(True) # Usually Adjust implies removing stock or changing qty
            # Populate Reasons for ADJUST
            self.update_reasons(["Scrap", "Damage", "Relocation"])

        active_btn.setChecked(True)
        accent = active_btn.property("accent_color")
        hover = active_btn.property("hover_color")
        active_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent};
                color: white;
                border: 1px solid {accent};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {hover};
                border: 1px solid {hover};
            }}
        """)

    def update_reasons(self, reasons):
        self.combo_reason.clear()
        self.combo_reason.addItems(reasons)

    def setup_styles(self):
        self.setStyleSheet("""
            #FormFrame, #InfoFrame {
                background-color: #3C3F41;
                border-radius: 10px;
                border: 1px solid #555555;
            }
            QLabel {
                font-size: 20px;
                color: #ECEFF1;
            }
            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                background-color: #2D2D30;
                border: 1px solid #555555;
                border-radius: 4px;
                color: white;
                padding: 5px;
                font-size: 18px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #f7c774;
            }
            #SubmitButton {
                background-color: "#f7a51b";
                font-weight: bold;
                padding: 20px;
                border-radius: 5px;
                margin-top: 10px;
            }
            #SubmitButton:hover {
                background-color: #f7c774;
            }
            #SubmitButton:pressed {
                background-color: #f7a51b;
            }
        """)
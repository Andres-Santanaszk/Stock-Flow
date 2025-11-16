from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QCheckBox, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont 
from entities.Item import Item
from ui.translations import ITEM_PACK_TYPE_ES

class ItemFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        title_label = QLabel("Registrar Ítem")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        info_layout = QFormLayout()
        info_layout.setLabelAlignment(Qt.AlignRight)
        
        stock_layout = QFormLayout()
        stock_layout.setLabelAlignment(Qt.AlignRight)

        self.txtName = QLineEdit()
        self.txtSKU = QLineEdit()
        self.txtBarcode = QLineEdit()
        
        self.cmbBrand = QComboBox()
        self.cmbCategory = QComboBox()
        
        self.cmbPack = QComboBox()
        for enum_val, es_val in ITEM_PACK_TYPE_ES.items():
            self.cmbPack.addItem(es_val, userData=enum_val)

        self.spnMinQty = QSpinBox()
        self.spnMinQty.setRange(0, 100)
        self.spnMinQty.setValue(0)
        
        self.txtDesc = QTextEdit()
        self.txtDesc.setMinimumHeight(80)

        info_layout.addRow("Nombre:", self.txtName)
        info_layout.addRow("SKU:", self.txtSKU)
        info_layout.addRow("Código de barras:", self.txtBarcode)

        stock_layout.addRow("Marca:", self.cmbBrand)
        stock_layout.addRow("Categoría:", self.cmbCategory)
        stock_layout.addRow("Tipo de empaque:", self.cmbPack)
        stock_layout.addRow("Cantidad mínima: ", self.spnMinQty)

        card_info = QFrame()
        card_info.setObjectName("CardFrame")
        card_info_layout = QVBoxLayout(card_info)
        card_title_info = QLabel("Información Principal")
        card_title_info.setObjectName("SectionTitle")
        card_info_layout.addWidget(card_title_info)
        card_info_layout.addLayout(info_layout)
        card_info_layout.addStretch()

        card_stock = QFrame()
        card_stock.setObjectName("CardFrame")
        card_stock_layout = QVBoxLayout(card_stock)
        card_title_stock = QLabel("Clasificación")
        card_title_stock.setObjectName("SectionTitle")
        card_stock_layout.addWidget(card_title_stock)
        card_stock_layout.addLayout(stock_layout)
        card_stock_layout.addStretch()
        
        card_desc = QFrame()
        card_desc.setObjectName("CardFrame")
        card_desc_layout = QVBoxLayout(card_desc)
        card_title_desc = QLabel("Descripción")
        card_title_desc.setObjectName("SectionTitle")
        card_desc_layout.addWidget(card_title_desc)
        card_desc_layout.addWidget(self.txtDesc)
        
        self.btnSave = QPushButton("Guardar Ítem")
        self.btnSave.setObjectName("BtnSave")
        
        self.btnClear = QPushButton("Limpiar")
        self.btnClear.setObjectName("BtnClear")


        
        top_cards_layout = QHBoxLayout()
        top_cards_layout.addWidget(card_info, 1)  
        top_cards_layout.addWidget(card_stock, 1) 

        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnClear, 1)
        btns_layout.addWidget(self.btnSave, 1) 
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20) 
        root_layout.setSpacing(15)
        
        root_layout.addWidget(title_label)
        root_layout.addLayout(top_cards_layout)
        root_layout.addWidget(card_desc)
        root_layout.addStretch(1) 
        root_layout.addLayout(btns_layout)

        self._apply_styles()

        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._on_clear)
        self._load_combos()

    def _apply_styles(self):
        """ Aplica los QSS para el estilo de tarjetas """
        self.setStyleSheet("""
            /* Título principal del formulario */
            #FormTitle {
                color: #f7a51b; /* Color de acento */
                margin-bottom: 10px;
            }

            /* Contenedor de cada tarjeta */
            #CardFrame {
                background-color: #3C3F41; /* Fondo de tarjeta (del Placeholder) */
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 15px;
            }

            /* Título dentro de cada tarjeta */
            #SectionTitle {
                font-size: 14px;
                font-weight: bold;
                color: #ECEFF1; /* Texto claro */
                margin-bottom: 10px;
                border-bottom: 1px solid #555555; /* Separador ligero */
                padding-bottom: 5px;
            }

            /* Widgets de formulario (QLineEdit, QComboBox, etc.) */
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 11px; /* <-- Aumentado de 8px a 11px */
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                background-color: #424242;
                font-size: 14px; /* <-- Añadido para que el texto sea más legible */
            }
            
            /* Botón Principal (Guardar) */
            #BtnSave {
                background-color: #f7a51b; /* Color de acento */
                color: #000000;
                font-weight: bold;
                font-size: 15px;
                padding: 10px 15px;
                border-radius: 5px;
            }
            #BtnSave:hover {
                background-color: #f7c774;
            }
            
            /* Botón Secundario (Limpiar) */
            #BtnClear {
                background-color: #555555; /* Color gris */
                color: #ECEFF1;
                font-size: 15px;
                padding: 10px 15px;
                border-radius: 5px;
            }
            #BtnClear:hover {
                background-color: #6A6A6A;
            }
        """)

    def _load_combos(self):
        try:
            self.cmbBrand.addItem("(Opcional)", userData=None)
            self.cmbCategory.addItem("(Opcional)", userData=None)

            brands = Item.get_all_brands_for_combo()
            for brand_id, name in brands:
                self.cmbBrand.addItem(name, userData=brand_id)

            categories = Item.get_all_categories_for_combo()
            for cat_id, name in categories:
                self.cmbCategory.addItem(name, userData=cat_id)

        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error de Carga", 
                f"No se pudieron cargar marcas y categorías:\n{e}"
            )

    def _on_save(self):
        name = self.txtName.text().strip()
        sku = self.txtSKU.text().strip()
        barcode = self.txtBarcode.text().strip() or None
        
        brand_id = self.cmbBrand.currentData()
        category_id = self.cmbCategory.currentData()
        
        desc = self.txtDesc.toPlainText().strip()
        pack_enum = self.cmbPack.currentData()
        min_qty = int(self.spnMinQty.value())

        if not name or not sku:
            QMessageBox.warning(self, "Faltan datos", "Nombre y SKU son obligatorios.")
            return

        try:
            if Item.exists_sku(sku):
                QMessageBox.warning(self, "Duplicado", f"El SKU '{sku}' ya existe.")
                return

            item = Item(
                name=name, 
                sku=sku, 
                description=desc, 
                pack_type=pack_enum,
                min_qty=min_qty, 
                barcode=barcode,
                brand_id=brand_id,
                category_id=category_id
            )
            
            new_id = item.add_item()
            QMessageBox.information(self, "Éxito", f"Item creado con ID {new_id}")
            self._on_clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{e}")

    def _on_clear(self):
        self.txtName.clear()
        self.txtSKU.clear()
        self.txtBarcode.clear()
        
        self.cmbBrand.setCurrentIndex(0)
        self.cmbCategory.setCurrentIndex(0)
        
        self.txtDesc.clear()
        self.cmbPack.setCurrentIndex(0)
        self.spnMinQty.setValue(0)
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame, QCompleter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from entities.ItemLocation import ItemLocation
from entities.Item import Item
from ui.translations import ITEM_PACK_TYPE_ES
from ui.utils.common_widgets import SwitchButton

class UpdateItemForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentid_item = None
        self.original_sku = None

        title_label = QLabel("Modificar Ítem ")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")


        info_layout = QFormLayout()
        info_layout.setLabelAlignment(Qt.AlignRight)

        stock_layout = QFormLayout()
        stock_layout.setLabelAlignment(Qt.AlignRight)

        # CAMPOS
        self.combo_item = QComboBox()
        self.combo_item.setEditable(True)
        self.combo_item.setInsertPolicy(QComboBox.NoInsert)
        self.combo_item.setPlaceholderText("Buscar por nombre o SKU...")

        completer = self.combo_item.completer()

        completer.setFilterMode(Qt.MatchContains) 
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        

        completer.activated.connect(self._on_completer_activated)


        self.txtName = QLineEdit()
        self.txtSKU = QLineEdit()
        self.txtBarcode = QLineEdit()

        self.txtDesc = QTextEdit()
        self.txtDesc.setMinimumHeight(80)
        self.btnActive = SwitchButton() 
        self.btnActive.setToolTip("Activar o Desactivar este ítem")
        
        self.cmbBrand = QComboBox()
        self.cmbCategory = QComboBox()

        self.cmbPack = QComboBox()
        for enum_val, es_val in ITEM_PACK_TYPE_ES.items():
            self.cmbPack.addItem(es_val, userData=enum_val)

        self.spnMinQty = QSpinBox()
        self.spnMinQty.setRange(0, 10000)
        self.spnMinQty.setValue(0)

        self.txtDesc = QTextEdit()
        self.txtDesc.setMinimumHeight(80)

        info_layout.addRow("Nombre:", self.txtName)
        info_layout.addRow("SKU:", self.txtSKU)
        info_layout.addRow("Código de barras:", self.txtBarcode)
        info_layout.addRow("Estado Activo:", self.btnActive)
        
        stock_layout.addRow("Marca:", self.cmbBrand)
        stock_layout.addRow("Categoría:", self.cmbCategory)
        stock_layout.addRow("Tipo de empaque:", self.cmbPack)
        stock_layout.addRow("Cantidad mínima:", self.spnMinQty)

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

        card_desc = QFrame()
        card_desc.setObjectName("CardFrame")
        card_desc_layout = QVBoxLayout(card_desc)
        card_title_desc = QLabel("Descripción")
        card_title_desc.setObjectName("SectionTitle")
        card_desc_layout.addWidget(card_title_desc)
        card_desc_layout.addWidget(self.txtDesc)

        self.btnSave = QPushButton("Actualizar Ítem")
        self.btnSave.setObjectName("BtnSave")

        self.btnClear = QPushButton("Restablecer")
        self.btnClear.setObjectName("BtnClear")
        
        # LAYOUTS ORGANIZADOS
        top_cards_layout = QHBoxLayout()
        top_cards_layout.addWidget(card_info, 1)
        top_cards_layout.addWidget(card_stock, 1)

        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnClear, 1)
        btns_layout.addWidget(self.btnSave, 2)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)

        root_layout.addWidget(title_label)
        root_layout.addWidget(self.combo_item)
        root_layout.addLayout(top_cards_layout)
        root_layout.addWidget(card_desc)
        root_layout.addStretch(1)
        root_layout.addLayout(btns_layout)

        self._apply_styles()

        self.combo_item.currentIndexChanged.connect(self._on_item_selected)
        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._restore_selected_item)

        # CARGAR DATOS
        self._load_combos()
        self.load_items_for_search()


    def _apply_styles(self):
        self.setStyleSheet("""
            #FormTitle {
                color: #f7a51b;
                margin-bottom: 10px;
            }
            #CardFrame {
                background-color: #3C3F41;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 15px;
            }
            #SectionTitle {
                font-size: 14px;
                font-weight: bold;
                color: #ECEFF1;
                margin-bottom: 10px;
                border-bottom: 1px solid #555555;
                padding-bottom: 5px;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 11px;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                background-color: #424242;
                font-size: 14px;
                color: white;
            }
            QComboBox QAbstractItemView {
                background-color: #424242;
                selection-background-color: #f7a51b;
                selection-color: #000;
                border: 1px solid #5A5A5A;
                color: white;
            }
            #BtnSave {
                background-color: #f7a51b;
                color: #000000;
                font-weight: bold;
                font-size: 15px;
                padding: 10px 15px;
                border-radius: 5px;
            }
            #BtnSave:hover {
                background-color: #f7c774;
            }
            #BtnClear {
                background-color: #555555;
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
            self.cmbBrand.clear()
            self.cmbCategory.clear()
            self.cmbBrand.addItem("(Opcional)", userData=None)
            self.cmbCategory.addItem("(Opcional)", userData=None)

            for brand_id, name in Item.get_all_brands_for_combo():
                self.cmbBrand.addItem(name, userData=brand_id)

            for cat_id, name in Item.get_all_categories_for_combo():
                self.cmbCategory.addItem(name, userData=cat_id)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar combos:\n{e}")


    def load_items_for_search(self):
        items = Item.search_items_for_display("", limit=1000)

        self.combo_item.blockSignals(True)
        self.combo_item.clear()
        self.combo_item.addItem("Buscar o seleccionar ítem…", userData=None)

        for row in items:
            id_item = row[0]
            name = row[1]
            sku = row[2]
            display = f"{name} | SKU: {sku}"
            self.combo_item.addItem(display, userData=id_item)

        self.combo_item.blockSignals(False)


    def _on_completer_activated(self, text):
        """Maneja la selección desde el menú desplegable del autocompletado"""
        if not text:
            return

        index = self.combo_item.findText(text)
        if index >= 0:
            self.combo_item.setCurrentIndex(index)

    def _on_item_selected(self, index):
        id_item = self.combo_item.itemData(index)
        if not id_item:
            return

        self.currentid_item = id_item
        self._load_item_data()


    def _load_item_data(self):
        try:
            if not self.currentid_item:
                return

            item = Item.get_by_id(self.currentid_item)
            if not item:
                return

            self.txtName.setText(item.name)
            self.txtSKU.setText(item.sku)
            self.txtBarcode.setText(item.barcode or "")
            self.txtDesc.setText(item.description or "")
            self.spnMinQty.setValue(item.min_qty or 0)

            self.original_sku = item.sku
            is_active = bool(item.active) 
            self.btnActive.setChecked(is_active)

            self._set_combo(self.cmbBrand, item.brand_id)
            self._set_combo(self.cmbCategory, item.category_id)
            self._set_combo(self.cmbPack, item.pack_type)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar datos:\n{e}")

    def _set_combo(self, combo, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                return
        combo.setCurrentIndex(0)

    def _on_save(self):
        # Validación extra por si escribieron texto pero no seleccionaron del combo
        if not self.currentid_item:
            # Intentamos resolverlo por texto
            current_text = self.combo_item.currentText()
            index = self.combo_item.findText(current_text)
            if index >= 0:
                 self.currentid_item = self.combo_item.itemData(index)

        if not self.currentid_item:
            QMessageBox.warning(self, "Error", "Selecciona un ítem válido de la lista.")
            return

        name = self.txtName.text().strip()
        sku = self.txtSKU.text().strip()

        if not name or not sku:
            QMessageBox.warning(self, "Error", "Nombre y SKU son obligatorios.")
            return

        if sku != self.original_sku and Item.exists_sku(sku):
            QMessageBox.warning(self, "Duplicado", f"El SKU '{sku}' ya existe.")
            return

        if not self.btnActive.isChecked():
            # Consultamos solo el número total
            total_stock = ItemLocation.get_total_stock(self.currentid_item)
            
            if total_stock > 0:
                QMessageBox.warning(
                    self,
                    "No permitido",
                    f"No puedes desactivar este ítem. Hay un total de {total_stock} unidades en inventario."
                )
                self._clear_form()
                self.load_items_for_search()
                return    

        try:
            item = Item(
                id_item=self.currentid_item,
                name=name,
                sku=sku,
                barcode=self.txtBarcode.text().strip() or None,
                description=self.txtDesc.toPlainText().strip() or None,
                brand_id=self.cmbBrand.currentData(),
                category_id=self.cmbCategory.currentData(),
                pack_type=self.cmbPack.currentData(),
                min_qty=self.spnMinQty.value(),
                active=self.btnActive.isChecked()
            )

            item.update()
            self.original_sku = sku
            
            QMessageBox.information(self, "Éxito", "Ítem actualizado correctamente.")
            self._clear_form()

            self.load_items_for_search()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
            
    def _clear_form(self):
        self.currentid_item = None
        self.original_sku = None

        self.combo_item.setCurrentIndex(0)

        self.txtName.clear()
        self.txtSKU.clear()
        self.txtBarcode.clear()
        self.txtDesc.clear()

        self.spnMinQty.setValue(0)
        self.btnActive.setChecked(False)

        self.cmbBrand.setCurrentIndex(0)
        self.cmbCategory.setCurrentIndex(0)
        self.cmbPack.setCurrentIndex(0)


    # -------------------------------
    # RESTAURAR DATOS ORIGINALES
    # -------------------------------
    def _restore_selected_item(self):
        self._load_item_data()
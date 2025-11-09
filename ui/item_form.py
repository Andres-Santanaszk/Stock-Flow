from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QCheckBox, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt
from entities.Item import Item
from ui.translations import ITEM_PACK_TYPE_ES

class ItemFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.txtName = QLineEdit()
        self.txtSKU = QLineEdit()
        self.txtBarcode = QLineEdit()
        self.txtDesc = QTextEdit()
        self.txtDesc.setFixedHeight(80)

        self.cmbPack = QComboBox()
        for enum_val, es_val in ITEM_PACK_TYPE_ES.items():
            self.cmbPack.addItem(es_val, userData=enum_val)

        self.spnMinQty = QSpinBox()
        self.spnMinQty.setRange(0, 10_000)
        self.spnMinQty.setValue(0)

        self.chkActive = QCheckBox("Activo")
        self.chkActive.setChecked(True)

        self.btnSave = QPushButton("Guardar item")
        self.btnClear = QPushButton("Limpiar")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addRow("Nombre:", self.txtName)
        form.addRow("SKU:", self.txtSKU)
        form.addRow("Código de barras:", self.txtBarcode)
        form.addRow("Descripción:", self.txtDesc)
        form.addRow("Tipo de empaque:", self.cmbPack)
        form.addRow("Stock mínimo:", self.spnMinQty)
        form.addRow("", self.chkActive)

        btns = QHBoxLayout()
        btns.addWidget(self.btnSave)
        btns.addWidget(self.btnClear)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addLayout(btns)
        root.addStretch()

        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._on_clear)

    def _on_save(self):
        name = self.txtName.text().strip()
        sku = self.txtSKU.text().strip()
        barcode = self.txtBarcode.text().strip() or None
        desc = self.txtDesc.toPlainText().strip()
        pack_enum = self.cmbPack.currentData()
        min_qty = int(self.spnMinQty.value())
        active = self.chkActive.isChecked()

        if not name or not sku:
            QMessageBox.warning(self, "Faltan datos", "Nombre y SKU son obligatorios.")
            return

        try:
            # Validación rápida de duplicado
            if Item.exists_sku(sku):
                QMessageBox.warning(self, "Duplicado", f"El SKU '{sku}' ya existe.")
                return

            item = Item(
                name=name, sku=sku, description=desc, pack_type=pack_enum,
                min_qty=min_qty, active=active, barcode=barcode
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
        self.txtDesc.clear()
        self.cmbPack.setCurrentIndex(0)
        self.spnMinQty.setValue(0)
        self.chkActive.setChecked(True)

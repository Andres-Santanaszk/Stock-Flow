# ui/simple_forms.py
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox, QCheckBox, QSpinBox
)
from PySide6.QtCore import Qt

from db.connection import get_connection
from ui.translations import ITEM_CLASS_ES  # para el enum de categorías

# ---------- Formulario Marca ----------
class BrandFormWidget(QWidget):
    """
    Inserta en brands (name UNIQUE, description, website, contact_email)
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.txtName = QLineEdit()
        self.txtDesc = QTextEdit(); self.txtDesc.setFixedHeight(70)
        self.txtWebsite = QLineEdit()
        self.txtEmail = QLineEdit()

        self.btnSave = QPushButton("Guardar marca")
        self.btnClear = QPushButton("Limpiar")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addRow("Nombre:", self.txtName)
        form.addRow("Descripción:", self.txtDesc)
        form.addRow("Sitio web:", self.txtWebsite)
        form.addRow("Email contacto:", self.txtEmail)

        btns = QHBoxLayout()
        btns.addWidget(self.btnSave); btns.addWidget(self.btnClear)

        root = QVBoxLayout(self)
        root.addLayout(form); root.addLayout(btns); root.addStretch()

        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._on_clear)

    def _on_save(self):
        name = self.txtName.text().strip()
        desc = self.txtDesc.toPlainText().strip() or None
        web  = self.txtWebsite.text().strip() or None
        mail = self.txtEmail.text().strip() or None

        if not name:
            QMessageBox.warning(self, "Faltan datos", "El nombre de la marca es obligatorio.")
            return

        sql = """
        INSERT INTO brands (name, description, website, contact_email)
        VALUES (%s, %s, %s, %s)
        RETURNING id_brand;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (name, desc, web, mail))
            new_id = cur.fetchone()[0]
            conn.commit()
            QMessageBox.information(self, "Éxito", f"Marca creada con ID {new_id}")
            self._on_clear()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo guardar la marca:\n{e}")
        finally:
            cur.close(); conn.close()

    def _on_clear(self):
        self.txtName.clear(); self.txtDesc.clear(); self.txtWebsite.clear(); self.txtEmail.clear()

# ---------- Formulario Categoría ----------
class CategoryFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.txtName = QLineEdit()
        self.cmbClass = QComboBox()
        for en, es in ITEM_CLASS_ES.items():
            self.cmbClass.addItem(es, userData=en)

        self.txtDesc = QTextEdit(); self.txtDesc.setFixedHeight(70)
        self.chkActive = QCheckBox("Activa"); self.chkActive.setChecked(True)

        self.btnSave = QPushButton("Guardar categoría")
        self.btnClear = QPushButton("Limpiar")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addRow("Nombre:", self.txtName)
        form.addRow("Clase:", self.cmbClass)
        form.addRow("Descripción:", self.txtDesc)
        form.addRow("", self.chkActive)

        btns = QHBoxLayout()
        btns.addWidget(self.btnSave); btns.addWidget(self.btnClear)

        root = QVBoxLayout(self)
        root.addLayout(form); root.addLayout(btns); root.addStretch()

        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._on_clear)

    def _on_save(self):
        name = self.txtName.text().strip()
        cls  = self.cmbClass.currentData() 
        desc = self.txtDesc.toPlainText().strip() or None
        active = self.chkActive.isChecked()

        if not name:
            QMessageBox.warning(self, "Faltan datos", "El nombre de la categoría es obligatorio.")
            return

        sql = """
        INSERT INTO categories (name, class, description, active)
        VALUES (%s, %s, %s, %s)
        RETURNING id_category;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (name, cls, desc, active))
            new_id = cur.fetchone()[0]
            conn.commit()
            QMessageBox.information(self, "Éxito", f"Categoría creada con ID {new_id}")
            self._on_clear()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"No se pudo guardar la categoría:\n{e}")
        finally:
            cur.close(); conn.close()

    def _on_clear(self):
        self.txtName.clear(); self.txtDesc.clear()
        if self.cmbClass.count() > 0: self.cmbClass.setCurrentIndex(0)
        self.chkActive.setChecked(True)

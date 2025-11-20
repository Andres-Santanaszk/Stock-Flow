from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QComboBox, QCheckBox,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from entities.Category import Category
from ui.translations import ITEM_CLASS_ES 

class CategoryFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        title_label = QLabel("Registrar Categoría")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.txtName = QLineEdit()
        
        self.cmbClass = QComboBox()
        for en, es in ITEM_CLASS_ES.items():
            self.cmbClass.addItem(es, userData=en)

        self.txtDesc = QTextEdit(); self.txtDesc.setFixedHeight(70)

        form_layout.addRow("Nombre:", self.txtName)
        form_layout.addRow("Tipo:", self.cmbClass)
        form_layout.addRow("Descripción:", self.txtDesc)

        card_form = QFrame()
        card_form.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card_form)
        
        card_title = QLabel("Datos de la Categoría")
        card_title.setObjectName("SectionTitle")
        
        card_layout.addWidget(card_title)
        card_layout.addLayout(form_layout)
        card_layout.addStretch()

        self.btnSave = QPushButton("Guardar Categoría")
        self.btnSave.setObjectName("BtnSave")
        
        self.btnClear = QPushButton("Limpiar")
        self.btnClear.setObjectName("BtnClear")

        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnClear, 1)
        btns_layout.addWidget(self.btnSave, 2)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)
        
        root_layout.addWidget(title_label)
        root_layout.addWidget(card_form)
        root_layout.addStretch(1)
        root_layout.addLayout(btns_layout)

        self._apply_styles()
        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._on_clear)

    def _apply_styles(self):
        """ Aplica los QSS para el estilo de tarjetas """

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


    def _on_save(self):
        name = self.txtName.text().strip()
        cls_ = self.cmbClass.currentData()
        desc = self.txtDesc.toPlainText().strip() or None

        if not name or not cls_:
            QMessageBox.warning(self, "Faltan datos", "Nombre y Clase son obligatorios.")
            return
        cat_id = getattr(self, "current_id", None)
        try:
            new_category = Category(
                id_category=cat_id,
                name=name,
                class_=cls_, 
                description=desc,
            )
            new_id = new_category.add_category()

            QMessageBox.information(self, "Éxito", f"Categoría creada con ID {new_id}")
            self._on_clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la categoría:\n{e}")

    def _on_clear(self):
        self.txtName.clear(); self.txtDesc.clear()
        if self.cmbClass.count() > 0: self.cmbClass.setCurrentIndex(0)
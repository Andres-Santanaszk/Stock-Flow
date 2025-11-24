from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from entities.Location import Location
from ui.translations import LOCATION_TYPE_ES


class LocationFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        title_label = QLabel("Registrar Localizacion")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.txtCode = QLineEdit()

        self.txtDescription = QTextEdit()
        self.txtDescription.setMinimumHeight(80)

        self.cmbType = QComboBox()

        for enum_val, es_val in LOCATION_TYPE_ES.items():
            self.cmbType.addItem(es_val, userData=enum_val)

        form_layout.addRow("Código:", self.txtCode)
        form_layout.addRow("Tipo:", self.cmbType)
        form_layout.addRow("Descripción:", self.txtDescription)

        card_form = QFrame()
        card_form.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card_form)

        card_tittle = QLabel("Datos de la Localizacion")
        card_tittle.setObjectName("SectionTitle")

        card_layout.addWidget(card_tittle)
        card_layout.addLayout(form_layout)
        card_layout.addStretch()

        self.btnSave = QPushButton("Guardar Localizacion")
        self.btnSave.setObjectName("BtnSave")

        self.btnClear = QPushButton("Limpiar")
        self.btnClear.setObjectName("BtnClear")

        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnClear, 1)
        btns_layout.addWidget(self.btnSave, 2)

        root_layout = QVBoxLayout(self)
        root_layout.addWidget(title_label)
        root_layout.addWidget(card_form)
        root_layout.addStretch(1)
        root_layout.addLayout(btns_layout)

        self._apply_styles()
        self.btnSave.clicked.connect(self._on_save)
        self.btnClear.clicked.connect(self._on_clear)

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
        code = self.txtCode.text().strip()
        tipe = self.cmbType.currentData()
        desc = self.txtDescription.toPlainText().strip() or None

        if not code or not tipe:
            QMessageBox.warning(self, "Faltan datos",
                                "El Código y el Tipo de locación son obligatorios.")
            return
        loc_id = getattr(self, "current_id", None)
        try:
            new_location = Location(
                code,
                tipe,
                desc,
                True
            )
            new_id = new_location.add_location()
            QMessageBox.information(
                self, "Éxito", f"Localización creada con el ID {new_id}")
            self._on_clear()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"No se pudo guardar la localización:\n{e}")

    def _on_clear(self):
        self.txtCode.clear()
        self.txtDescription.clear()

        if self.cmbType.count() > 0:
            self.cmbType.setCurrentIndex(0)

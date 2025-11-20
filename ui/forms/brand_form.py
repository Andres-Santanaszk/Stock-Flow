from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from entities.Brand import Brand

class BrandFormWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        title_label = QLabel("Registrar Marca")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.txtName = QLineEdit()
        self.txtDesc = QTextEdit(); self.txtDesc.setFixedHeight(70)
        self.txtWebsite = QLineEdit()
        self.txtEmail = QLineEdit()
        
        form_layout.addRow("Nombre:", self.txtName)
        form_layout.addRow("Descripción:", self.txtDesc)
        form_layout.addRow("Sitio web:", self.txtWebsite)
        form_layout.addRow("Email contacto:", self.txtEmail)

        card_form = QFrame()
        card_form.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card_form)
        
        card_title = QLabel("Datos de la Marca")
        card_title.setObjectName("SectionTitle")
        
        card_layout.addWidget(card_title)
        card_layout.addLayout(form_layout)
        card_layout.addStretch()

        # botnes
        self.btnSave = QPushButton("Guardar Marca")
        self.btnSave.setObjectName("BtnSave")
        
        self.btnClear = QPushButton("Limpiar")
        self.btnClear.setObjectName("BtnClear")

        # layout botones
        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnClear, 1)
        btns_layout.addWidget(self.btnSave, 2)

        # layout vertical
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)
        
        root_layout.addWidget(title_label)
        root_layout.addWidget(card_form)
        root_layout.addStretch(1) 
        root_layout.addLayout(btns_layout)

        # aplicando estilos y conectar boton
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

    # logica
    def _on_save(self):
        name = self.txtName.text().strip()
        desc = self.txtDesc.toPlainText().strip() or None
        web  = self.txtWebsite.text().strip() or None
        mail = self.txtEmail.text().strip() or None

        if not name:
            QMessageBox.warning(self, "Faltan datos", "El nombre de la marca es obligatorio.")
            return

        brand_id = getattr(self, "current_id", None)
        try:
            new_brand = Brand(
                id_brand=brand_id,
                name=name,
                description=desc,
                website=web,
                contact_email=mail
            )
            new_id = new_brand.add_brand()
            
            QMessageBox.information(self, "Éxito", f"Marca creada con ID {new_id}")
            self._on_clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la marca:\n{e}")

    def _on_clear(self):
        self.txtName.clear(); self.txtDesc.clear(); self.txtWebsite.clear(); self.txtEmail.clear()
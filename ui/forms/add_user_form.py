from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QCheckBox, 
    QFrame, QMessageBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt

from security.hashing import hash_password 
from entities.User import User

class AddUserForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Usuario - Stock Flow")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        # --- UI LAYOUT ---
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # Header
        lbl_title = QLabel("REGISTRAR USUARIO")
        lbl_title.setObjectName("DialogTitle")
        lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl_title)

        line = QFrame()
        line.setObjectName("Separator")
        line.setFrameShape(QFrame.HLine)
        self.layout.addWidget(line)

        # Formulario
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(15)
        self.form_layout.setHorizontalSpacing(20)

        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Nombre completo")
        
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("correo@ejemplo.com")

        self.cmb_role = QComboBox()
        self.cmb_role.setPlaceholderText("Seleccione un rol")
        # Data Dummy para roles
        self.cmb_role.addItem("Administrador", 1)
        self.cmb_role.addItem("Almacenista", 2)
        self.cmb_role.addItem("Vendedor", 3)

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Contraseña")
        self.txt_pass.setEchoMode(QLineEdit.Password)

        self.txt_confirm = QLineEdit()
        self.txt_confirm.setPlaceholderText("Confirmar contraseña")
        self.txt_confirm.setEchoMode(QLineEdit.Password)

        def add_row(label, widget):
            lbl = QLabel(label)
            lbl.setObjectName("FormLabel")
            self.form_layout.addRow(lbl, widget)

        add_row("Nombre:", self.txt_name)
        add_row("Email:", self.txt_email)
        add_row("Rol:", self.cmb_role)
        add_row("Contraseña:", self.txt_pass)
        add_row("Confirmar:", self.txt_confirm)

        self.layout.addLayout(self.form_layout)
        self.layout.addSpacing(20)

        # Botones
        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setObjectName("BtnCancel")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Guardar Usuario")
        self.btn_save.setObjectName("BtnSave")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self._on_save)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.btn_save)
        self.layout.addLayout(btn_layout)

        self.apply_styles()

    def apply_styles(self):
        # Mismos estilos definidos anteriormente...
        self.setStyleSheet("""
            QDialog { background-color: #3c3f41; }
            #DialogTitle { color: #f7a51b; font-size: 24px; font-weight: 800; font-family: "Segoe UI"; }
            #Separator { color: #555555; border-top: 1px solid #555555; }
            #FormLabel { color: #ffffff; font-size: 14px; font-weight: bold; font-family: "Segoe UI"; }
            QLineEdit, QComboBox {
                background-color: #2b2b2b; border: 2px solid #444444;
                border-radius: 6px; padding: 5px 10px; color: #ffffff; font-size: 14px; height: 30px;
            }
            QLineEdit:focus, QComboBox:focus { border: 2px solid #f7a51b; }
            QComboBox::drop-down { border: none; }
            QCheckBox { color: #ffffff; font-size: 14px; spacing: 10px; }
            QCheckBox::indicator { width: 18px; height: 18px; border: 2px solid #444444; border-radius: 4px; background: #2b2b2b; }
            QPushButton { font-weight: bold; font-size: 14px; border-radius: 8px; padding: 10px 20px; }
            #BtnCancel { background-color: #555555; color: #ffffff; border: none; }
            #BtnCancel:hover { background-color: #777777; }
            #BtnSave { background-color: #f7a51b; color: #000000; border: none; }
            #BtnSave:hover { background-color: #f7c774; }
            #BtnSave:pressed { background-color: #d48806; }
        """)
        
    def _on_save(self):
        # 1. Extracción directa de variables
        name = self.txt_name.text().strip()
        email = self.txt_email.text().strip().lower()
        raw_pass = self.txt_pass.text()
        confirm_pass = self.txt_confirm.text()
        
        role_id = self.cmb_role.currentData()

        # 2. Validaciones de UI
        if not name or not email or not raw_pass:
            QMessageBox.warning(self, "Faltan datos", "Nombre, email y contraseña son obligatorios.")
            return

        if raw_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return

        try:
            # 3. Lógica de Negocio (Duplicados)
            # Asumo que crearás este método estático igual que en Item.exists_sku(sku)
            if User.exists_email(email): 
                QMessageBox.warning(self, "Duplicado", f"El correo '{email}' ya existe.")
                return

            # 4. Hashing
            hashed_pw = hash_password(raw_pass)

            new_user = User(
                full_name=name,
                email=email,
                password_hash=hashed_pw,
                role_id=role_id
            )
            
            new_id = new_user.add_user()
            
            QMessageBox.information(self, "Éxito", f"Usuario creado con ID {new_id}")
            
            # 7. Cerrar indicando éxito (Accepted)
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{e}")
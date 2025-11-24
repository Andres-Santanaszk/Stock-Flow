from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, 
    QFrame, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt

from security.hashing import hash_password 
from entities.User import User
from ui.utils.common_widgets import SwitchButton
from entities.Role import Role

class EditUserForm(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Flow - Editar Usuario")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        self.current_user = User.get_by_id(user_id)
        
        if not self.current_user:
            QMessageBox.critical(self, "Error", "No se encontró el usuario en la base de datos.")
            self.reject()
            return

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        lbl_title = QLabel("EDITAR USUARIO") 
        lbl_title.setObjectName("DialogTitle")
        lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl_title)

        line = QFrame()
        line.setObjectName("Separator")
        line.setFrameShape(QFrame.HLine)
        self.layout.addWidget(line)

        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(15)
        self.form_layout.setHorizontalSpacing(20)

        self.txt_name = QLineEdit()
        self.txt_name.setText(self.current_user.full_name)
        
        self.txt_email = QLineEdit()
        self.txt_email.setText(self.current_user.email) 

        self.cmb_role = QComboBox()
        self.cmb_role.setPlaceholderText("")
        roles_data = Role.get_all()

        for role_id, role_name in roles_data:
            self.cmb_role.addItem(role_name, role_id)

        index = self.cmb_role.findData(self.current_user.role_id)
        if index >= 0:
            self.cmb_role.setCurrentIndex(index)

        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Dejar vacío para mantener actual")
        self.txt_pass.setEchoMode(QLineEdit.Password)

        self.txt_confirm = QLineEdit()
        self.txt_confirm.setPlaceholderText("Confirmar nueva contraseña")
        self.txt_confirm.setEchoMode(QLineEdit.Password)

        self.chk_active = SwitchButton()
        self.chk_active.setChecked(self.current_user.active)
        
        def add_row(label, widget):
            lbl = QLabel(label)
            lbl.setObjectName("FormLabel")
            self.form_layout.addRow(lbl, widget)

        add_row("Nombre:", self.txt_name)
        add_row("Email:", self.txt_email)
        add_row("Rol:", self.cmb_role)
        add_row("Contraseña:", self.txt_pass)
        add_row("Confirmar:", self.txt_confirm)
        add_row("Activo / Inactivo", self.chk_active)

        self.layout.addLayout(self.form_layout)
        self.layout.addSpacing(20)

        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setObjectName("BtnCancel")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setAutoDefault(False) 
        self.btn_cancel.setDefault(False)
        self.btn_cancel.clicked.connect(self.reject)
        

        self.btn_save = QPushButton("Actualizar Usuario")
        self.btn_save.setObjectName("BtnSave")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.setDefault(True) 
        self.btn_save.setAutoDefault(True)
        self.btn_save.clicked.connect(self._on_update)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.btn_save)
        self.layout.addLayout(btn_layout)

        self.apply_styles()

    def apply_styles(self):
        # Mismo estilo exacto para mantener consistencia
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

    def _on_update(self):
        # 1. Extracción
        name = self.txt_name.text().strip()
        email = self.txt_email.text().strip().lower()
        new_pass = self.txt_pass.text()
        confirm_pass = self.txt_confirm.text()
        role_id = self.cmb_role.currentData()
        is_active = self.chk_active.isChecked()

        # 2. Validaciones Básicas
        if not name or not email:
            QMessageBox.warning(self, "Faltan datos", "El nombre y el email no pueden estar vacíos.")
            return

        # 3. Lógica de Contraseña (Opcional)
        final_hash = self.current_user.password_hash # Por defecto, mantenemos la anterior
        
        if new_pass: # Solo si el usuario escribió algo
            if new_pass != confirm_pass:
                QMessageBox.warning(self, "Error", "Las nuevas contraseñas no coinciden.")
                return
            final_hash = hash_password(new_pass) # Hasheamos la nueva

        try:
            if email != self.current_user.email and User.exists_email(email):
                QMessageBox.warning(self, "Duplicado", f"El correo '{email}' ya está en uso por otro usuario.")
                return

            user_to_update = User(
                id_user=self.current_user.id_user, 
                full_name=name,
                email=email,
                password_hash=final_hash,
                active=is_active,
                role_id=role_id
            )
            
            # 6. Llamada a Update
            user_to_update.update()
            
            QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
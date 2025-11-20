from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, 
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

# Asumimos que tienes tu lógica y el formulario de edición original
from entities.Brand import Brand
from ui.forms.brand_form import BrandFormWidget

class UpdateBrandForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de Marcas")
        self.resize(450, 600)
        
        # Datos en memoria
        self.all_brands = []

        # --- UI SETUP ---
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Título
        self.lbl_title = QLabel("Actualizar Marca")
        self.lbl_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        # Buscador
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Buscar marca por nombre...")
        self.txt_search.setClearButtonEnabled(True)
        self.txt_search.textChanged.connect(self.filter_list)
        self.layout.addWidget(self.txt_search)

        # Lista
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_edit = QPushButton("Editar Seleccionada")
        
        # Estilo especial al botón editar
        self.btn_edit.setObjectName("BtnAction")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_edit)
        self.layout.addLayout(btn_layout)

        # --- ESTILOS (Dark Theme) ---
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; color: white; }
            QLabel { color: #f7a51b; }
            QLineEdit { 
                padding: 10px; border-radius: 5px; border: 1px solid #555; 
                background-color: #3c3f41; color: white; font-size: 14px;
            }
            QListWidget { 
                background-color: #3c3f41; border: 1px solid #555; 
                color: white; font-size: 14px; border-radius: 5px; outline: none;
            }
            QListWidget::item { padding: 10px; }
            QListWidget::item:selected { background-color: #3498db; color: white; }
            QPushButton { 
                padding: 10px 20px; border-radius: 5px; 
                background-color: #555; color: white; font-weight: bold; border: none;
            }
            QPushButton:hover { background-color: #666; }
            QPushButton#BtnAction { background-color: #f7a51b; color: black; }
            QPushButton#BtnAction:hover { background-color: #ffb84d; }
        """)

        # --- CONEXIONES ---
        self.btn_cancel.clicked.connect(self.close)
        self.btn_edit.clicked.connect(self.open_editor)
        self.list_widget.itemDoubleClicked.connect(self.open_editor)

        # Cargar datos iniciales
        self.load_data()

    def load_data(self):
        self.list_widget.clear()
        try:
            self.all_brands = Brand.get_all()
            for brand in self.all_brands:
                self.list_widget.addItem(brand.name)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las marcas: {e}")

    def filter_list(self, text):
        self.list_widget.clear()
        text = text.lower()
        for brand in self.all_brands:
            if text in brand.name.lower():
                self.list_widget.addItem(brand.name)

    def open_editor(self):
        row = self.list_widget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atención", "Debes seleccionar una marca de la lista.")
            return

        # Buscar el objeto original basado en el texto seleccionado
        selected_text = self.list_widget.currentItem().text()
        brand_obj = next((b for b in self.all_brands if b.name == selected_text), None)

        if brand_obj:
            # Abrir formulario existente
            dlg = QDialog(self)
            form = BrandFormWidget(dlg)
            
            # RELLENAR DATOS (Ajusta según tus inputs reales)
            # Asumo que tu form tiene inputs llamados line_name, etc.
            if hasattr(form, 'line_name'): form.line_name.setText(brand_obj.name)
            if hasattr(form, 'line_desc'): form.line_desc.setText(brand_obj.description or "")
            if hasattr(form, 'line_web'): form.line_web.setText(brand_obj.website or "")
            if hasattr(form, 'line_email'): form.line_email.setText(brand_obj.contact_email or "")

            # INYECTAR ID (Crucial para el UPDATE)
            form.current_id = brand_obj.id_brand
            
            lay = QVBoxLayout(dlg)
            lay.addWidget(form)
            dlg.setWindowTitle(f"Editando: {brand_obj.name}")
            
            if dlg.exec():
                self.load_data() # Recargar lista al volver
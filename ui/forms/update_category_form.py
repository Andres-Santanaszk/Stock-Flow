from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, 
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from entities.Category import Category
from ui.forms.category_form import CategoryFormWidget

class UpdateCategoryForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de Categorías")
        self.resize(450, 500)
        self.all_cats = []

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Header
        self.lbl_title = QLabel("Actualizar Categoría")
        self.lbl_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        # Search
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Buscar categoría...")
        self.txt_search.textChanged.connect(self.filter_list)
        self.layout.addWidget(self.txt_search)

        # List
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Editar")
        self.btn_edit.setObjectName("BtnAction")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_edit)
        self.layout.addLayout(btn_layout)

        # Estilos (Reutilizamos el estilo Dark)
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; color: white; }
            QLabel { color: #f7a51b; }
            QLineEdit, QListWidget { 
                background-color: #3c3f41; border: 1px solid #555; 
                color: white; padding: 8px; border-radius: 4px;
            }
            QListWidget::item:selected { background-color: #3498db; }
            QPushButton { padding: 10px 25px; border-radius: 5px; background-color: #555; color: white; }
            QPushButton#BtnAction { background-color: #f7a51b; color: black; font-weight: bold; }
        """)

        self.btn_edit.clicked.connect(self.open_editor)
        self.list_widget.itemDoubleClicked.connect(self.open_editor)
        self.load_data()

    def load_data(self):
        self.list_widget.clear()
        try:
            self.all_cats = Category.get_all()
            for c in self.all_cats:
                self.list_widget.addItem(c.name)
        except:
            pass # Manejo de error silencioso o agregar print

    def filter_list(self, text):
        self.list_widget.clear()
        text = text.lower()
        for c in self.all_cats:
            if text in c.name.lower():
                self.list_widget.addItem(c.name)

    def open_editor(self):
        row = self.list_widget.currentRow()
        if row < 0: return

        selected_text = self.list_widget.currentItem().text()
        obj = next((c for c in self.all_cats if c.name == selected_text), None)

        if obj:
            dlg = QDialog(self)
            form = CategoryFormWidget(dlg)
            
            # Rellenar
            if hasattr(form, 'line_name'): form.line_name.setText(obj.name)
            form.current_id = obj.id_category
            
            lay = QVBoxLayout(dlg)
            lay.addWidget(form)
            dlg.setWindowTitle("Editar Categoría")
            if dlg.exec():
                self.load_data()
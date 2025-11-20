from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, 
    QLineEdit, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from entities.Location import Location
from ui.forms.location_form import LocationFormWidget

class UpdateLocationForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de Locaciones")
        self.resize(500, 550)
        self.all_locs = []

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        
        # Header
        self.lbl_title = QLabel("Actualizar Locación")
        self.lbl_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Buscar por nombre o dirección...")
        self.txt_search.textChanged.connect(self.filter_list)
        self.layout.addWidget(self.txt_search)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.btn_edit = QPushButton("Editar Locación")
        self.btn_edit.setObjectName("BtnAction")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.layout.addWidget(self.btn_edit)

        # Estilos
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; }
            QLabel { color: #f7a51b; }
            QLineEdit, QListWidget { 
                background-color: #3c3f41; border: 1px solid #555; color: white; padding: 5px; 
            }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #444; }
            QListWidget::item:selected { background-color: #3498db; }
            QPushButton#BtnAction { 
                background-color: #f7a51b; color: black; font-weight: bold; 
                padding: 12px; border-radius: 6px;
            }
        """)

        self.btn_edit.clicked.connect(self.open_editor)
        self.load_data()

    def load_data(self):
        self.list_widget.clear()
        try:
            self.all_locs = Location.get_all()
            for l in self.all_locs:
                # Mostramos info extra en la lista
                display_text = f"{l.code}  |  {l.type}"
                self.list_widget.addItem(display_text)
        except: pass

    def filter_list(self, text):
        self.list_widget.clear()
        text = text.lower()
        for l in self.all_locs:
            full_text = f"{l.code} {l.type}".lower()
            if text in full_text:
                self.list_widget.addItem(f"{l.code}  |  {l.type}")

    def open_editor(self):
        row = self.list_widget.currentRow()
        if row < 0: return

        # Truco: Como filtramos, necesitamos encontrar el objeto correcto en la lista original
        # Lo ideal es usar item.data() pero por simplicidad buscamos por índice filtrado
        # NOTA: Si filtras, el indice cambia. Mejor buscamos por nombre parseando el string
        selected_str = self.list_widget.currentItem().text()
        name_part = selected_str.split("  |")[0].strip()
        
        obj = next((l for l in self.all_locs if l.name == name_part), None)

        if obj:
            dlg = QDialog(self)
            form = LocationFormWidget(dlg)
            if hasattr(form, 'line_name'): form.line_name.setText(obj.name)
            if hasattr(form, 'line_address'): form.line_address.setText(obj.address)
            form.current_id = obj.id_location
            
            lay = QVBoxLayout(dlg)
            lay.addWidget(form)
            if dlg.exec():
                self.load_data()
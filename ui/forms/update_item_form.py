from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, 
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Asegúrate de que el import coincida con tu estructura
from entities.Item import Item
from ui.forms.item_form import ItemFormWidget

class UpdateItemForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de Inventario (Ítems)")
        self.resize(600, 700)
        self.all_items = []

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(25, 25, 25, 25)

        # Título
        self.lbl_title = QLabel("Buscar y Actualizar Ítem")
        self.lbl_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_title)

        # Buscador (Texto actualizado)
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Buscar por Nombre o SKU...")
        self.txt_search.textChanged.connect(self.filter_list)
        self.layout.addWidget(self.txt_search)

        # Lista
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cerrar")
        self.btn_edit = QPushButton("✏️ Editar Ítem Seleccionado")
        
        self.btn_edit.setObjectName("BtnPrimary")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_edit)
        self.layout.addLayout(btn_layout)

        # Estilos
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; color: white; }
            QLabel { color: #f7a51b; margin-bottom: 10px; }
            QLineEdit { 
                background-color: #3c3f41; border: 2px solid #555; 
                color: white; padding: 12px; border-radius: 6px; font-size: 15px;
            }
            QLineEdit:focus { border: 2px solid #f7a51b; }
            QListWidget { 
                background-color: #323232; border: none; color: #DDD; 
                font-size: 14px; border-radius: 6px;
            }
            QListWidget::item { 
                padding: 12px; border-bottom: 1px solid #444; 
            }
            QListWidget::item:selected { 
                background-color: #3498db; color: white; border-radius: 4px;
            }
            QPushButton { 
                padding: 12px; background-color: #444; color: white; border-radius: 6px; border: none; 
            }
            QPushButton#BtnPrimary { 
                background-color: #f7a51b; color: #222; font-weight: bold; font-size: 15px; 
            }
            QPushButton#BtnPrimary:hover { background-color: #ffc04d; }
        """)

        self.btn_cancel.clicked.connect(self.close)
        self.btn_edit.clicked.connect(self.open_editor)
        self.list_widget.itemDoubleClicked.connect(self.open_editor)
        
        self.load_data()

    def load_data(self):
        """Carga todos los ítems al inicio mostrando NOMBRE | SKU"""
        self.list_widget.clear()
        try:
            self.all_items = Item.get_all()
            for item in self.all_items:
                # IMPORTANTE: Aquí definimos cómo se ve en la lista
                text = f"{item.name} | SKU: {item.sku}"
                self.list_widget.addItem(text)
        except Exception as e:
            print(f"Error loading items: {e}")

    def filter_list(self, text):
        """Filtra la lista buscando coincidencias en Nombre O en SKU"""
        self.list_widget.clear()
        text = text.lower().strip()
        
        for item in self.all_items:
            # Convertimos a string y minúsculas para comparar sin errores
            name = str(item.name).lower()
            sku = str(item.sku).lower()
            
            # LÓGICA DE BÚSQUEDA:
            if text in name or text in sku:
                display = f"{item.name} | SKU: {item.sku}"
                self.list_widget.addItem(display)

    def open_editor(self):
        """Abre el editor recuperando el objeto correcto"""
        row = self.list_widget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor selecciona un ítem de la lista.")
            return

        # Obtenemos el texto de la fila seleccionada
        # Formato esperado: "Nombre del producto | SKU: SKU-123"
        sel_text = self.list_widget.currentItem().text()
        
        # Truco para sacar el SKU: dividimos el texto por el separador " | SKU: "
        # y tomamos la segunda parte (el final)
        try:
            sku_part = sel_text.split(" | SKU: ")[1]
        except IndexError:
            QMessageBox.warning(self, "Error", "No se pudo identificar el SKU del ítem.")
            return
        
        # Buscamos en la lista de objetos cuál tiene ese SKU
        obj = next((i for i in self.all_items if i.sku == sku_part), None)

        if obj:
            dlg = QDialog(self)
            # Aquí asumimos que tu ItemFormWidget está listo para recibir datos
            form = ItemFormWidget(dlg)
            
            # Rellenar campos (Asegúrate que estos nombres coincidan con tu Formulario UI)
            if hasattr(form, 'line_name'): form.line_name.setText(obj.name)
            if hasattr(form, 'line_sku'): form.line_sku.setText(obj.sku)
            if hasattr(form, 'line_barcode'): form.line_barcode.setText(obj.barcode)
            if hasattr(form, 'text_desc'): form.text_desc.setPlainText(obj.description or "")

            # INYECTAR ID (Vital para que el update funcione)
            form.current_id = obj.id_item
            
            lay = QVBoxLayout(dlg)
            lay.addWidget(form)
            dlg.setWindowTitle(f"Editando: {obj.name}")
            
            if dlg.exec():
                # Si guardó cambios, recargamos la lista
                self.load_data()
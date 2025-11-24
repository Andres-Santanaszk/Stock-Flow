from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QFrame,
    QComboBox, QCompleter
)
from ui.utils.common_widgets import SwitchButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from entities.Category import Category
from ui.translations import ITEM_CLASS_ES

class UpdateCategoryForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_id_category = None

        # -------------------------------
        # TÍTULO
        # -------------------------------
        title_label = QLabel("Modificar Categoría")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        # -------------------------------
        # FORMULARIO
        # -------------------------------
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        # --- BUSCADOR INTELIGENTE ---
        self.combo_search = QComboBox()
        self.combo_search.setEditable(True)
        self.combo_search.setInsertPolicy(QComboBox.NoInsert)
        self.combo_search.setPlaceholderText("Buscar categoría...")
        
        # Configuración del autocompletado
        completer = self.combo_search.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self._on_completer_activated)

        # --- CAMPOS DE DATOS ---
        self.txtName = QLineEdit()
        
        # Combo para Tipo/Clase (Misma lógica que en el Create)
        self.cmbClass = QComboBox()
        for en, es in ITEM_CLASS_ES.items():
            self.cmbClass.addItem(es, userData=en)

        self.txtDesc = QTextEdit()
        self.txtDesc.setMinimumHeight(80)
        #boton
        self.btnActive = SwitchButton() 
        self.btnActive.setToolTip("Activar o Desactivar este categoria")
        
        # Agregar filas
        form_layout.addRow("<b>Buscar:</b>", self.combo_search)
        form_layout.addRow("Nombre:", self.txtName)
        form_layout.addRow("Tipo:", self.cmbClass)
        form_layout.addRow("Estado Activo:", self.btnActive)
        form_layout.addRow("Descripción:", self.txtDesc)

        # -------------------------------
        # TARJETA (CARD)
        # -------------------------------
        card_form = QFrame()
        card_form.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card_form)
        
        card_title = QLabel("Datos de la Categoría")
        card_title.setObjectName("SectionTitle")
        
        card_layout.addWidget(card_title)
        card_layout.addLayout(form_layout)
        card_layout.addStretch()

        # -------------------------------
        # BOTONES
        # -------------------------------
        self.btnSave = QPushButton("Actualizar Categoría")
        self.btnSave.setObjectName("BtnSave")
        
        self.btnRestore = QPushButton("Restablecer")
        self.btnRestore.setObjectName("BtnClear")

        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnRestore, 1)
        btns_layout.addWidget(self.btnSave, 2)

        # -------------------------------
        # LAYOUT PRINCIPAL
        # -------------------------------
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)
        
        root_layout.addWidget(title_label)
        root_layout.addWidget(card_form)
        root_layout.addStretch(1)
        root_layout.addLayout(btns_layout)

        # ESTILOS Y CONEXIONES
        self._apply_styles()
        
        self.combo_search.currentIndexChanged.connect(self._on_category_selected)
        self.btnSave.clicked.connect(self._on_save)
        self.btnRestore.clicked.connect(self._restore_data)

        # Cargar datos iniciales
        self.load_categories_list()

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
            QLineEdit, QTextEdit, QComboBox {
                padding: 11px;
                border: 1px solid #5A5A5A;
                border-radius: 5px;
                background-color: #424242;
                font-size: 14px;
                color: white;
            }
            QComboBox QAbstractItemView {
                background-color: #424242;
                selection-background-color: #f7a51b;
                selection-color: #000;
                border: 1px solid #5A5A5A;
                color: white;
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

    # -------------------------------
    # LÓGICA DE CARGA
    # -------------------------------
    def load_categories_list(self):
        try:
            # Necesitas este método en tu clase Category
            categories = Category.get_all_categories()
            
            self.combo_search.blockSignals(True)
            self.combo_search.clear()
            self.combo_search.addItem("Buscar categoría...", userData=None)
            
            for row in categories:
                # row = (id_category, name)
                self.combo_search.addItem(row[1], userData=row[0])
                
            self.combo_search.blockSignals(False)
        except Exception as e:
            print(f"Error cargando categorías: {e}")

    def _on_completer_activated(self, text):
        if not text: return
        index = self.combo_search.findText(text)
        if index >= 0:
            self.combo_search.setCurrentIndex(index)

    def _on_category_selected(self, index):
        cat_id = self.combo_search.itemData(index)
        if not cat_id:
            return
        self.current_id_category = cat_id
        self._load_category_data()

    def _load_category_data(self):
        if not self.current_id_category:
            return
        try:
            # Necesitas este método en tu clase Category
            cat = Category.get_by_id(self.current_id_category)
            if cat:
                self.txtName.setText(cat.name)
                self.txtDesc.setText(cat.description or "")
                is_active = bool(cat.active) 
                self.btnActive.setChecked(is_active)
                #Selecionar tipo
                index = self.cmbClass.findData(cat.class_)
                if index >= 0:
                    self.cmbClass.setCurrentIndex(index)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar datos:\n{e}")

    def _set_combo(self, combo, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                return
        combo.setCurrentIndex(0)
    
    def _restore_data(self):
        self._load_category_data()

    # -------------------------------
    # GUARDAR
    # -------------------------------
    def _on_save(self):
        if not self.current_id_category:
            QMessageBox.warning(self, "Atención", "Selecciona una categoría primero.")
            return

        name = self.txtName.text().strip()
        cls_ = self.cmbClass.currentData()
        desc = self.txtDesc.toPlainText().strip() or None
        
        if not name or not cls_:
            QMessageBox.warning(self, "Faltan datos", "Nombre y Tipo son obligatorios.")
            return

        # --- INICIO DE LA NUEVA VALIDACIÓN ---
        # Si el usuario está intentando desactivar la categoría (el botón NO está checkeado)
        if not self.btnActive.isChecked():
            # Verificamos si hay productos dentro
            if Category.has_associated_items(self.current_id_category):
                QMessageBox.warning(
                    self, 
                    "No permitido", 
                    "No puedes desactivar esta categoría porque tiene productos asociados.\n"
                    "Debes mover o eliminar los productos antes de desactivar la categoría."
                )
                # Opcional: Volver a activar el botón visualmente para que el usuario entienda
                self.btnActive.setChecked(True) 
                self._clear_form()
                self.load_categories_list()
                return
        
        try:
            category = Category(
                id_category=self.current_id_category,
                name=name,
                class_=cls_,
                description=desc,
                active=self.btnActive.isChecked()
            )
            
            # Necesitas este método en tu clase Category
            category.update()
            
            QMessageBox.information(self, "Éxito", "Categoría actualizada correctamente.")
            self._clear_form()
            # Recargar lista para refrescar nombres
            self.combo_search.blockSignals(True)
            self._clear_form()
            self.load_categories_list()
            self.combo_search.blockSignals(False)
            
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
            
    def _clear_form(self):
        self.current_id_category = None
        self.combo_search.blockSignals(True)
        self.combo_search.setCurrentIndex(0)
        self.combo_search.blockSignals(False)
        
        self.txtName.clear()
        self.cmbClass.setCurrentIndex(0)
        self.txtDesc.clear() 
        self.btnActive.setChecked(False)
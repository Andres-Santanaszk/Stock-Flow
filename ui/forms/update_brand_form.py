from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QFrame,
    QComboBox, QCompleter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.utils.common_widgets import SwitchButton
from entities.Brand import Brand  # Asegúrate de tener esta clase

class UpdateBrandForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_id_brand = None

        # -------------------------------
        # TÍTULO
        # -------------------------------
        title_label = QLabel("Modificar Marca")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        # -------------------------------
        # FORMULARIO
        # -------------------------------
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        # --- BUSCADOR DE MARCA (Estilo QCompleter avanzado) ---
        self.combo_search = QComboBox()
        self.combo_search.setEditable(True)
        self.combo_search.setInsertPolicy(QComboBox.NoInsert)
        self.combo_search.setPlaceholderText("Buscar marca por nombre...")
        
        # Configuración del autocompletado "MatchContains"
        completer = self.combo_search.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self._on_completer_activated)

        # CAMPOS DE DATOS
        self.txtName = QLineEdit()
        self.txtWebsite = QLineEdit()
        self.txtEmail = QLineEdit()
        self.txtDesc = QTextEdit()
        self.txtDesc.setFixedHeight(80)
        self.btnActive = SwitchButton() 
        self.btnActive.setToolTip("Activar o Desactivar esta marca")
        
        
        # AGREGAR AL LAYOUT
        # (Opcional: Poner el buscador fuera de la tarjeta o dentro, aquí lo pongo primero)
        form_layout.addRow("<b>Buscar Marca:</b>", self.combo_search)
        form_layout.addRow("Nombre:", self.txtName)
        form_layout.addRow("Sitio web:", self.txtWebsite)
        form_layout.addRow("Email contacto:", self.txtEmail)
        form_layout.addRow("Estado Activo:", self.btnActive)
        form_layout.addRow("Descripción:", self.txtDesc)
        

        # -------------------------------
        # TARJETA (CARD)
        # -------------------------------
        card_form = QFrame()
        card_form.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card_form)
        
        card_title = QLabel("Datos de la Marca")
        card_title.setObjectName("SectionTitle")
        
        card_layout.addWidget(card_title)
        card_layout.addLayout(form_layout)
        card_layout.addStretch()

        # -------------------------------
        # BOTONES
        # -------------------------------
        self.btnSave = QPushButton("Actualizar Marca")
        self.btnSave.setObjectName("BtnSave")
        
        self.btnRestore = QPushButton("Restablecer")
        self.btnRestore.setObjectName("BtnClear") # Usamos el mismo estilo gris

        # LAYOUT BOTONES
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
        
        self.combo_search.currentIndexChanged.connect(self._on_brand_selected)
        self.btnSave.clicked.connect(self._on_save)
        self.btnRestore.clicked.connect(self._restore_data)

        # Cargar lista inicial
        self.load_brands_list()

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
    # CARGA DE LISTA DE MARCAS
    # -------------------------------
    def load_brands_list(self):
        """ Carga todas las marcas en el combo para buscar """
        try:
            # Asumo que tienes un método estático similar en tu clase Brand
            # Si no, usa Brand.get_all() y itera
            brands = Brand.get_all_brands() 
            
            self.combo_search.blockSignals(True)
            self.combo_search.clear()
            self.combo_search.addItem("Buscar marca...", userData=None)
            
            for row in brands:
                # row suele ser (id_brand, name)
                id_brand = row[0]
                name = row[1]
                self.combo_search.addItem(name, userData=id_brand)
                
            self.combo_search.blockSignals(False)
            
        except Exception as e:
            # Si falla porque no existe el método, intenta manejarlo o crea el método en Brand
            print(f"Error cargando marcas: {e}")

    # -------------------------------
    # LÓGICA DE SELECCIÓN
    # -------------------------------
    def _on_completer_activated(self, text):
        if not text: return
        index = self.combo_search.findText(text)
        if index >= 0:
            self.combo_search.setCurrentIndex(index)

    def _on_brand_selected(self, index):
        brand_id = self.combo_search.itemData(index)
        if not brand_id:
            return
        
        self.current_id_brand = brand_id
        self._load_brand_data()

    def _load_brand_data(self):
        if not self.current_id_brand:
            return
            
        try:
            # Asumimos método get_by_id en Brand
            brand = Brand.get_by_id(self.current_id_brand)
            if brand:
                self.txtName.setText(brand.name)
                self.txtDesc.setText(brand.description or "")
                self.txtWebsite.setText(brand.website or "")
                self.txtEmail.setText(brand.contact_email or "")
                is_active = bool(brand.active) 
                self.btnActive.setChecked(is_active)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la marca:\n{e}")

    def _restore_data(self):
        """ Vuelve a cargar los datos de la base de datos para la marca seleccionada """
        self._load_brand_data()

    # -------------------------------
    # GUARDAR / ACTUALIZAR
    # -------------------------------
    def _on_save(self):
        if not self.current_id_brand:
            QMessageBox.warning(self, "Atención", "Primero debes buscar y seleccionar una marca.")
            return

        name = self.txtName.text().strip()
        desc = self.txtDesc.toPlainText().strip() or None
        web  = self.txtWebsite.text().strip() or None
        mail = self.txtEmail.text().strip() or None

        if not name:
            QMessageBox.warning(self, "Faltan datos", "El nombre de la marca es obligatorio.")
            return

        # --- VALIDACIÓN DE SEGURIDAD ---
        # Si el usuario quiere desactivar la marca...
        if not self.btnActive.isChecked():
            # ...verificamos si hay items usándola
            if Brand.has_associated_items(self.current_id_brand):
                QMessageBox.warning(
                    self, 
                    "No permitido", 
                    "No puedes desactivar esta marca porque hay productos asociados a ella.\n"
                    "Elimina o cambia la marca de esos productos antes de continuar."
                )
                self._clear_form()
                self.load_brands_list
                return
        
        try:
            # Creamos objeto Brand con el ID existente
            brand = Brand(
                id_brand=self.current_id_brand,
                name=name,
                description=desc,
                website=web,
                contact_email=mail,
                active=self.btnActive.isChecked()
            )
            
            # LLAMADA A UPDATE (Asegúrate de tener este método en tu clase Brand)
            brand.update() 
            
            QMessageBox.information(self, "Éxito", "Marca actualizada correctamente.")
            self._clear_form()
            # Opcional: Recargar la lista por si cambió el nombre
            self.combo_search.blockSignals(True)
            self._clear_form()
            self.load_brands_list()
            self.combo_search.blockSignals(False)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar la marca:\n{e}")
            
    def _clear_form(self):
        self.current_id_brand = None
        self.combo_search.blockSignals(True)
        self.combo_search.setCurrentIndex(0)
        self.combo_search.blockSignals(False)
        
        self.txtName.clear()
        self.txtWebsite.clear()
        self.txtEmail.clear()
        self.txtDesc.clear()
        self.btnActive.setChecked(False)
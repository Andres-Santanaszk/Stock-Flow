from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, QComboBox, 
    QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout,
    QLabel, QFrame, QCompleter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.utils.common_widgets import SwitchButton
from entities.ItemLocation import ItemLocation
from entities.Location import Location
from ui.translations import LOCATION_TYPE_ES

class UpdateLocationForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_id_location = None

        title_label = QLabel("Modificar Ubicación")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("FormTitle")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.combo_search = QComboBox()
        self.combo_search.setEditable(True)
        self.combo_search.setInsertPolicy(QComboBox.NoInsert)
        self.combo_search.setPlaceholderText("Buscar por código...")

        completer = self.combo_search.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self._on_completer_activated)

        self.txtCode = QLineEdit()
        
        self.cmbType = QComboBox()
        for enum_val, es_val in LOCATION_TYPE_ES.items():
            self.cmbType.addItem(es_val, userData=enum_val)

        self.txtDescription = QTextEdit()
        self.txtDescription.setMinimumHeight(80)
        #boton
        self.btnActive = SwitchButton() 
        self.btnActive.setToolTip("Activar o Desactivar esta ubicacion")
        

        form_layout.addRow("<b>Buscar:</b>", self.combo_search)
        form_layout.addRow("Código:", self.txtCode)
        form_layout.addRow("Tipo:", self.cmbType)
        form_layout.addRow("Estado Activo:", self.btnActive)
        form_layout.addRow("Descripción:", self.txtDescription)

        card_form = QFrame()
        card_form.setObjectName("CardFrame")
        card_layout = QVBoxLayout(card_form)

        card_title = QLabel("Datos de la Localización")
        card_title.setObjectName("SectionTitle")

        card_layout.addWidget(card_title)
        card_layout.addLayout(form_layout)
        card_layout.addStretch()

        self.btnSave = QPushButton("Actualizar Localización")
        self.btnSave.setObjectName("BtnSave")

        self.btnRestore = QPushButton("Restablecer")
        self.btnRestore.setObjectName("BtnClear")

        btns_layout = QHBoxLayout()
        btns_layout.addStretch(1)
        btns_layout.addWidget(self.btnRestore, 1)
        btns_layout.addWidget(self.btnSave, 2)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(15)

        root_layout.addWidget(title_label)
        root_layout.addWidget(card_form)
        root_layout.addStretch(1)
        root_layout.addLayout(btns_layout)

        self._apply_styles()

        self.combo_search.currentIndexChanged.connect(self._on_location_selected)
        self.btnSave.clicked.connect(self._on_save)
        self.btnRestore.clicked.connect(self._restore_data)

        self.load_locations_list()
        
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


    def load_locations_list(self):
        try:

            locations = Location.get_all_locations_for_combo()

            self.combo_search.blockSignals(True)
            self.combo_search.clear()
            self.combo_search.addItem("Buscar código...", userData=None)

            for row in locations:

                self.combo_search.addItem(row[1], userData=row[0])

            self.combo_search.blockSignals(False)
        except Exception as e:
            print(f"Error cargando localizaciones: {e}")

    def _on_completer_activated(self, text):
        if not text: return
        index = self.combo_search.findText(text)
        if index >= 0:
            self.combo_search.setCurrentIndex(index)

    def _on_location_selected(self, index):
        loc_id = self.combo_search.itemData(index)
        if not loc_id:
            return
        self.current_id_location = loc_id
        self._load_location_data()

    def _load_location_data(self):
        if not self.current_id_location:
            return
        try:

            loc = Location.get_by_id(self.current_id_location)
            if loc:
                self.txtCode.setText(loc.code)
                self.txtDescription.setText(loc.description or "")
                is_active = bool(loc.active) 
                self.btnActive.setChecked(is_active)

            index = self.cmbType.findData(loc.type)
            if index >= 0:
                self.cmbType.setCurrentIndex(index)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar datos:\n{e}")

    def _restore_data(self):
        self._load_location_data()

    def _on_save(self):
        if not self.current_id_location:
            QMessageBox.warning(self, "Atención", "Selecciona una localización primero.")
            return

        code = self.txtCode.text().strip()
        tipe = self.cmbType.currentData()
        desc = self.txtDescription.toPlainText().strip() or None

        if not code or not tipe:
            QMessageBox.warning(self, "Faltan datos", "El Código y el Tipo son obligatorios.")
            return

        if not self.btnActive.isChecked():

            if ItemLocation.has_stock_in_location(self.current_id_location):
                QMessageBox.warning(
                    self, 
                    "No permitido", 
                    "No puedes desactivar esta ubicación porque contiene stock físico.\n"
                    "Debes mover los productos a otra ubicación antes de desactivarla."
                )
                self._clear_form()
                self.load_locations_list()
                return

        try:

            location = Location(
                id_location=self.current_id_location,
                code=code,
                type=tipe,
                description=desc,
                active=self.btnActive.isChecked()
            )

            location.update()

            QMessageBox.information(self, "Éxito", "Localización actualizada correctamente.")
            self._clear_form()
            self.combo_search.blockSignals(True)
            self._clear_form()
            self.load_locations_list()
            self.combo_search.blockSignals(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar:\n{e}")
            
    def _clear_form(self):
        self.current_id_location = None
        self.combo_search.blockSignals(True)
        self.combo_search.setCurrentIndex(0)
        self.combo_search.blockSignals(False)
            
        self.txtCode.clear()
        self.cmbType.setCurrentIndex(0)
        self.txtDescription.clear()
        self.btnActive.setChecked(False)
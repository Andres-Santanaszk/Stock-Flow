from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, 
    QFrame, QStyledItemDelegate, QStyle, QFormLayout, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QIcon, QColor
from pathlib import Path
import qtawesome as qta

from entities.User import User
from ui.forms.add_user_form import AddUserForm 
from ui.forms.edit_user_form import EditUserForm

BASE_DIR = Path(__file__).resolve().parents[1]

class IDHighlighterDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if (option.state & QStyle.State_Selected) and index.column() == 0:
            painter.save()
            color = QColor("#f7a51b")
            width = 6
            rect = option.rect
            bar_rect = QRect(rect.left(), rect.top(), width, rect.height())
            painter.fillRect(bar_rect, color)
            painter.restore()

class BigAnimatedButton(QToolButton):
    def __init__(self, text, icon_path, fallback_name, parent=None):
        super().__init__(parent)
        self.setText(text.upper())
        self.setCursor(Qt.PointingHandCursor)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon) 

        icon = QIcon()
        if icon_path.exists():
            icon.addFile(str(icon_path))
        else:
            icon = QIcon.fromTheme(fallback_name)
        self.setIcon(icon)

        # TAMAÑOS
        self.base_size = QSize(50, 50)
        self.hover_size = QSize(60, 60)

        self.setIconSize(self.base_size)

        # ANIMACIONES
        self.anim_grow = QPropertyAnimation(self, b"iconSize")
        self.anim_grow.setDuration(150)
        self.anim_grow.setEasingCurve(QEasingCurve.OutQuad)
        self.anim_grow.setEndValue(self.hover_size)

        self.anim_shrink = QPropertyAnimation(self, b"iconSize")
        self.anim_shrink.setDuration(150)
        self.anim_shrink.setEasingCurve(QEasingCurve.OutQuad)
        self.anim_shrink.setEndValue(self.base_size)

    def enterEvent(self, event):
        self.anim_shrink.stop()
        self.anim_grow.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim_grow.stop()
        self.anim_shrink.start()
        super().leaveEvent(event)

class UserInfoPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DetailPanel")
        self.setFixedWidth(350) 

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        lbl_header = QLabel("Detalles del Usuario")
        lbl_header.setObjectName("PanelHeader")
        layout.addWidget(lbl_header)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setObjectName("PanelLine")
        layout.addWidget(line)

        self.lbl_name = QLabel()
        self.lbl_name.setObjectName("PanelName")
        self.lbl_name.setWordWrap(True)
        layout.addWidget(self.lbl_name)

        self.lbl_email = QLabel()
        self.lbl_email.setObjectName("PanelEmail")
        layout.addWidget(self.lbl_email)

        layout.addSpacing(10)

        info_layout = QFormLayout()
        info_layout.setHorizontalSpacing(20)
        info_layout.setVerticalSpacing(10)
        
        def create_row(label_text, value_widget):
            lbl = QLabel(label_text)
            lbl.setObjectName("PanelLabel")
            info_layout.addRow(lbl, value_widget)

        self.lbl_id = QLabel()
        self.lbl_id.setObjectName("PanelValue")
        self.lbl_id.setAlignment(Qt.AlignRight)
        
        self.lbl_role = QLabel()
        self.lbl_role.setObjectName("PanelValue")
        self.lbl_role.setAlignment(Qt.AlignRight)

        create_row("ID", self.lbl_id)
        create_row("Rol Asignado:", self.lbl_role)

        layout.addLayout(info_layout)
        layout.addSpacing(15)

        self.lbl_status = QLabel()
        self.lbl_status.setObjectName("PanelStatus")
        layout.addWidget(self.lbl_status)

        layout.addStretch()

        self.reset_panel()

    def reset_panel(self):
        self.lbl_name.setText("Seleccione un usuario...")
        self.lbl_name.setStyleSheet("color: #777;") 
        self.lbl_email.setText("")
        self.lbl_id.setText("-")
        self.lbl_role.setText("-")
        self.lbl_status.setText("") 
        self.lbl_status.setStyleSheet("") 

    def update_data(self, user_id, name, email, role, is_active):
        self.lbl_name.setText(name)
        self.lbl_name.setStyleSheet("color: #f7a51b;") 
        self.lbl_email.setText(email)
        self.lbl_id.setText(str(user_id))
        self.lbl_role.setText(role)
        
        if is_active:
            self.lbl_status.setText("Usuario activo.")
            self.lbl_status.setStyleSheet("color: #28a745;")
        else:
            self.lbl_status.setText("Usuario inactivo.")
            self.lbl_status.setStyleSheet("color: #e74c3c;")

class UserHubWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.lbl_title = QLabel("Administrar Usuarios")
        self.lbl_title.setObjectName("MainTitle")
        
        self.lbl_subtitle = QLabel("Seleccione un usuario para comenzar. ")
        self.lbl_subtitle.setObjectName("SubTitle")
        
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Buscar usuario por nombre...")
        self.txt_search.setObjectName("SearchInput")
        self.txt_search.setClearButtonEnabled(True)
        search_icon = qta.icon('fa5s.search', color='#aaaaaa')
        self.txt_search.addAction(search_icon, QLineEdit.LeadingPosition)
        self.txt_search.textChanged.connect(self.filter_user_list)
        
        self.btn_add = BigAnimatedButton("Nuevo Usuario", BASE_DIR / "utils" / "add_user.svg", "contact-new")
        self.btn_edit = BigAnimatedButton("Editar usuario", BASE_DIR / "utils" / "edit_user.svg", "user-properties")
        self.btn_add.setObjectName("BigBtn")
        self.btn_edit.setObjectName("BigBtn")

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.txt_search) 
        controls_layout.addStretch()               
        controls_layout.addWidget(self.btn_add)    
        controls_layout.addWidget(self.btn_edit)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(20) 

        #Tabla
        self.table_frame = QFrame()
        self.table_frame.setObjectName("TableContainer")
        self.table_users = QTableWidget()
        self.table_users.setColumnCount(5) 
        self.table_users.setHorizontalHeaderLabels(["ID", "USUARIO", "EMAIL", "ROL", "active_hidden"])
        
        self.table_users.setColumnHidden(4, True)
        header = self.table_users.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.table_users.verticalHeader().setDefaultSectionSize(50)
        self.table_users.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_users.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_users.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_users.setFocusPolicy(Qt.NoFocus)
        self.table_users.setShowGrid(False) 
        self.table_users.verticalHeader().setVisible(False)
        
        self.delegate = IDHighlighterDelegate(self.table_users)
        self.table_users.setItemDelegate(self.delegate)

        t_lay = QVBoxLayout(self.table_frame)
        t_lay.setContentsMargins(2,2,2,2)
        t_lay.addWidget(self.table_users)

        # Panel Derecho
        self.detail_panel = UserInfoPanel()

        body_layout.addWidget(self.table_frame, stretch=1)
        body_layout.addWidget(self.detail_panel)          

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(40, 10, 40, 40) 

        main_layout.addWidget(self.lbl_title)

        main_layout.addSpacing(15) 
        
        main_layout.addWidget(self.lbl_subtitle)
        main_layout.addSpacing(10)

        main_layout.addLayout(controls_layout)
        
        main_layout.addSpacing(15) 

        main_layout.addLayout(body_layout)

        self.setStyleSheet("""
            QWidget {
                font-family: "Segoe UI";
            }
            #MainTitle { 
                color: #f7a51b; 
                font-size: 54px; 
                font-weight: 800;

                margin-left: -15px;
            }
            
            #SubTitle {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: 600;

                margin-left: 0px; 
            }
            
            #SearchInput {
                background-color: #3c3f41;
                border: 2px solid #444444;
                border-radius: 8px;
                padding: 5px 15px 5px 5px; 
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                min-width: 300px;
                max-width: 400px;
                height: 35px;
            }
            #SearchInput:focus {
                border: 2px solid #f7a51b;
            }
            #BigBtn {
                background-color: #3c3f41;
                color: #ffffff;
                border: 2px solid #444444;
                border-radius: 25px;
                padding: 10px 25px; 
                font-weight: bold;
                font-size: 16px;
                
                min-width: 200px;  
                max-width: 200px;
                min-height: 75px;
                max-height: 75px;
            }
            #BigBtn:hover { 
                background-color: #f7c774; 
                color: black;
                border: 2px solid #f7a51b; 
            }
            #BigBtn:pressed { background-color: #f7a51b; color: black; }


            #TableContainer {
                background-color: #3c3f41;
                border: 1px solid #555;
                border-radius: 10px;
            }
            QTableWidget {
                background-color: #3c3f41;
                border: none;
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                padding: 10px;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #3c3f41;
                color: #f7a51b;
                font-weight: 800;
                font-size: 14px;
                text-transform: uppercase;
                border: none;
                border-bottom: 2px solid #555;
                padding: 5px 15px;
            }
            QTableWidget::item { padding-left: 15px; border-bottom: 1px solid #444; }
            QTableWidget::item:selected { background-color: #454545; color: #f7a51b; }

            #DetailPanel {
                background-color: #3c3f41;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            #DetailPanel QLabel { background-color: transparent; }
            #PanelHeader { color: #FFFFFF; font-size: 18px; font-weight: bold; }
            #PanelLine {
                border: none;
                background-color: #FFFFFF;
                max-height: 1px; height: 1px;
            }
            #PanelName { font-size: 22px; font-weight: 800; font-weight: bold; }
            #PanelEmail { color: #ffffff; font-size: 14px; font-weight: bold; }
            #PanelLabel { color: #FFFFFF; font-size: 14px; font-weight: bold; }
            #PanelValue { color: #ffffff; font-size: 14px; font-weight: bold; }
            #PanelStatus { font-size: 20px; font-weight: bold; font-weight: bold; }

            QScrollBar:vertical { border: none; background: #2b2b2b; width: 10px; margin: 0px; }
            QScrollBar::handle:vertical { background: #555555; min-height: 20px; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #f7a51b; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.btn_add.clicked.connect(self._open_add_user_dialog)
        self.btn_edit.clicked.connect(self._open_edit_user_dialog)
        self.table_users.itemSelectionChanged.connect(self._on_selection_changed)
        
        self.refresh_user_list()

    def _on_selection_changed(self):
        selected = self.table_users.selectedItems()
        if not selected:
            self.detail_panel.reset_panel()
            return
        
        row = selected[0].row()

        user_id = self.table_users.item(row, 0).text()
        name = self.table_users.item(row, 1).text()
        email = self.table_users.item(row, 2).text()
        role = self.table_users.item(row, 3).text()

        active_text = self.table_users.item(row, 4).text()

        is_active = active_text == "True"

        self.detail_panel.update_data(user_id, name, email, role, is_active)

    def filter_user_list(self, text):
        self.table_users.setRowCount(0)
        self.detail_panel.reset_panel()
        try:
            users = User.search_users_with_role(text) 
            
            for row_idx, user_data in enumerate(users):
                self.table_users.insertRow(row_idx)

                for col_idx, data in enumerate(user_data):
                    item = QTableWidgetItem(str(data))
                    if col_idx == 0:
                         item.setTextAlignment(Qt.AlignCenter)
                    else:
                         item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    
                    self.table_users.setItem(row_idx, col_idx, item)
        except Exception as e:
            print(f"Error filtering users: {e}")

    def refresh_user_list(self):
        self.filter_user_list("")

    def _open_add_user_dialog(self):
        dialog = AddUserForm(self)
        if dialog.exec(): 
            self.refresh_user_list()
            
        
    def _open_edit_user_dialog(self):
        selected_items = self.table_users.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error de selección", "Por favor, seleccione un usuario de la lista para continuar.")
            return

        row = selected_items[0].row()
        user_id = self.table_users.item(row, 0).text() 

        dialog = EditUserForm(int(user_id), self)
        
        if dialog.exec():
            self.refresh_user_list()
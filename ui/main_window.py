from pathlib import Path
import qtawesome as qta

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QStackedWidget,
    QFrame, QDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from PySide6.QtSvgWidgets import QSvgWidget

from ui.login_window import LoginWindow
from ui.forms.register_hub import RegisterHubWidget
from ui.forms.movement_form import MovementsWidget
from ui.utils.common_widgets import AnimatedButton
from ui.forms.user_hub import UserHubWidget
from entities.Role import Role
from entities.Permission import Permission


BASE_DIR = Path(__file__).resolve().parent

UTILS_DIR = BASE_DIR / "utils" 

logo_path = UTILS_DIR / "logo_white_letters.svg"
icon_path = UTILS_DIR / "icon.png"

class PlaceholderWidget(QFrame):
    def __init__(self, title, user_role, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(f"Módulo: {title}")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        role_label = QLabel(f"Acceso de Usuario Actual: <span style='color: #1E88E5;'>{user_role}</span>")
        role_label.setFont(QFont("Segoe UI", 14))
        role_label.setAlignment(Qt.AlignCenter)
        role_label.setStyleSheet("QLabel { margin-top: 15px; }")
        
        layout.addWidget(title_label)
        layout.addWidget(role_label)
        
        
        self.setStyleSheet("""
            QFrame {
                background-color: #3C3F41; /* Fondo ligeramente más oscuro que el fondo principal del tema */
                border: 1px solid #555555;
                border-radius: 10px;
                color: #ECEFF1; /* Asegura que el texto general sea claro */
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        
        self.current_user = user
        self.current_user_role = "Invitado"
        self.current_user_permissions = []

        self.setWindowTitle("Stock Flow")
        self.setWindowIcon(QIcon(str(icon_path)))
        self.setGeometry(100, 100, 1200, 800)
        
        self.current_user_role = "Invitado"
        
        if self.current_user:
            self.setWindowTitle(f"Stock Flow - {self.current_user_role}")
            self.current_user_role = Role.get_name_by_id(self.current_user.role_id)
            self.current_user_permissions = Permission.get_codes_by_role_id(self.current_user.role_id)
            
            print(f"DEBUG: Rol: {self.current_user_role}")
            print(f"DEBUG: Permisos: {self.current_user_permissions}")
        
        self._fade_anim = None
        
        self._setup_styles()
        self._setup_ui()
        self._apply_role_permissions()
    
        self.btn_dashboard.click()
        
        if self.btn_dashboard.isVisible():
            self.btn_dashboard.click()

    def _animate_transition_to_widget(self, new_widget):
            """Hace una transición de fade entre la vista actual y new_widget."""
            current_widget = self.stacked_widget.currentWidget()
            if current_widget is new_widget:
                return 

            
            if current_widget is not None:
                from PySide6.QtWidgets import QGraphicsOpacityEffect #si no los importo aquí no funciona wtf
                from PySide6.QtCore import QPropertyAnimation
                
                effect = QGraphicsOpacityEffect(current_widget)
                current_widget.setGraphicsEffect(effect)

                fade_out = QPropertyAnimation(effect, b"opacity", self)
                fade_out.setDuration(150)
                fade_out.setStartValue(1.0)
                fade_out.setEndValue(0.0)

                def on_fade_out_finished():
                    current_widget.setGraphicsEffect(None)

                    index = self.stacked_widget.indexOf(new_widget)
                    self.stacked_widget.setCurrentIndex(index)

                    effect_new = QGraphicsOpacityEffect(new_widget)
                    new_widget.setGraphicsEffect(effect_new)
                    effect_new.setOpacity(0.0)

                    fade_in = QPropertyAnimation(effect_new, b"opacity", self)
                    fade_in.setDuration(150)
                    fade_in.setStartValue(0.0)
                    fade_in.setEndValue(1.0)

                    def on_fade_in_finished():
                        new_widget.setGraphicsEffect(None)

                    fade_in.finished.connect(on_fade_in_finished)
                    fade_in.start()

                    self._fade_anim = fade_in

                fade_out.finished.connect(on_fade_out_finished)
                fade_out.start()

                self._fade_anim = fade_out

            else:
                from PySide6.QtWidgets import QGraphicsOpacityEffect
                from PySide6.QtCore import QPropertyAnimation

                index = self.stacked_widget.indexOf(new_widget)
                self.stacked_widget.setCurrentIndex(index)

                effect_new = QGraphicsOpacityEffect(new_widget)
                new_widget.setGraphicsEffect(effect_new)
                effect_new.setOpacity(0.0)

                fade_in = QPropertyAnimation(effect_new, b"opacity", self)
                fade_in.setDuration(250)
                fade_in.setStartValue(0.0)
                fade_in.setEndValue(1.0)

                def on_fade_in_finished():
                    new_widget.setGraphicsEffect(None)

                fade_in.finished.connect(on_fade_in_finished)
                fade_in.start()
                self._fade_anim = fade_in


    def _setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
            }
            QPushButton {
                /* Colores generales de botones manejados por qdarktheme, solo ajustamos padding y fuente */
                border: none;
                padding: 15px 10px;
                text-align: left;
                font-size: 18px;
                font-weight: 500;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover {
                background-color: #f7c774; 
                color: black;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #f7a51b; 
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            #SidebarFrame {
                background-color: #2D2D30; 
                border-right: 1px solid #555555;
            }
            #HeaderLabel {
                background-color: #2c2c30;
                padding: 15px;
                font-size: 18px;
                font-weight: 700;
                border-radius: 0;
            }
        """)

    def _setup_ui(self):
        """Configura el layout principal de la aplicación."""
        
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(central_widget)

        # sidebar
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarFrame")
        self.sidebar_frame.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 0, 10, 10)
        self.sidebar_layout.setSpacing(8)
        
        logo_widget = QSvgWidget(str(logo_path))
        logo_widget.setObjectName("HeaderLabel")
        logo_widget.setMaximumHeight(180)
        logo_widget.setMaximumWidth(180)
        self.sidebar_layout.addWidget(logo_widget)
        self.sidebar_layout.addWidget(logo_widget, alignment=Qt.AlignCenter)

        self._setup_sidebar_buttons()
        self.sidebar_layout.addLayout(self.buttons_layout)
        self.sidebar_layout.addStretch()
        
        
        self._setup_user_info()

        main_layout.addWidget(self.sidebar_frame)

        # central area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget { padding: 5px; }")
        
        self._setup_central_views()
        
        main_layout.addWidget(self.stacked_widget)
    
    def _setup_sidebar_buttons(self):
        """Define y conecta los botones de navegación."""
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(2)
        
        self.button_map = {
            "Dashboard": ("Inicio", "dashboard.view", "mdi.home"),
            "Registrar_Item": ("Registros", "items.write", "mdi.file-edit"),
            
            "Movimientos de inventario": ("Movimientos", "movements.post", "mdi.swap-horizontal"),
            
            "Inventory On Hand": ("Inventario", "items.read", "mdi.cube-scan"),
            "Localización": ("Ubicaciones", "locations.view", "mdi.map-marker"),

            "Gestión de Roles": ("Administrar usuarios", "users.manage", "mdi.account-cog"),
            
            "Historial de Movimientos": ("Historial transacciones", "reports.view", "mdi.history"),
            
            "Administrar inventario": ("Catálogos", "catalogs.manage", "mdi.tag-outline")
        }

        self.buttons = {}
        for key, (text, permission_id, icon_name) in self.button_map.items():
            btn = AnimatedButton(text, self,
                                base_icon_size=QSize(24, 24),
                                hover_icon_size=QSize(32, 32))
            btn.setIcon(qta.icon(icon_name, color="white"))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._switch_view(k, checked))

            btn.setProperty("permission_id", permission_id) 
            
            self.buttons[key] = btn
            self.buttons_layout.addWidget(btn)
            
        self.btn_dashboard = self.buttons["Dashboard"]
    
    def _setup_user_info(self):
        """Configura la etiqueta de usuario y el botón de Logout."""
        user_info_frame = QFrame()
        user_info_frame.setStyleSheet("""
            QFrame {
                border-top: 5px; 
                padding-top: 1px;
            }
            QLabel {
                color: #ECEFF1; 
            }
        """)
        user_info_layout = QVBoxLayout(user_info_frame)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        
        first_name = self.current_user.full_name.split(" ")[0]
        
        role_label = QLabel(f"Bienvenido, <b>{first_name}</b>")
        role_label.setFont(QFont("Segoe UI", 13))
        user_info_layout.addWidget(role_label)
        
        btn_logout = QPushButton("Cerrar Sesión / Logout")
        btn_logout.clicked.connect(self._handle_logout)
        btn_logout.setStyleSheet("QPushButton { background-color: #D32F2F; color: white; } QPushButton:hover { background-color: #EF5350; }")
        
        user_info_layout.addWidget(btn_logout)
        self.sidebar_layout.addWidget(user_info_frame)

    def _setup_central_views(self):
        """Crea y añade los widgets al QStackedWidget."""
        self.view_widgets = {}
        for key, (title, permission_id, icon_name) in self.button_map.items():
            if key == "Registrar_Item":  
                widget = RegisterHubWidget(self)
            elif key == "Movimientos de inventario": 
                widget = MovementsWidget(self, self.current_user)
            elif key == "Gestión de Roles":
                widget = UserHubWidget(self)
            else:
                widget = PlaceholderWidget(title, self.current_user_role)
            self.view_widgets[key] = widget
            self.stacked_widget.addWidget(widget)


    def _switch_view(self, key, checked):
            """Maneja el cambio de vista en el QStackedWidget."""
            if not checked:
                return

            #desactivar todos los demas botones
            for other_key, btn in self.buttons.items():
                if other_key != key:
                    btn.setChecked(False)

            widget = self.view_widgets.get(key)
            if widget:
                print(f"DEBUG: Cambiando a la vista: {key}")
                self._animate_transition_to_widget(widget)        


    def _apply_role_permissions(self):
        """
        Habilita/deshabilita botones comparando el código del botón
        con la lista de permisos cargada desde la Base de Datos.
        """
        user_perms = self.current_user_permissions if self.current_user_permissions else []

        for key, btn in self.buttons.items():
            required_code = btn.property("permission_id")
            if required_code in user_perms:
                btn.show()
            else:
                btn.hide()

    def _handle_logout(self):
        self.close()

        login_dialog = LoginWindow()
        if login_dialog.exec() == QDialog.Accepted and login_dialog.valid_login:

            new_user = login_dialog.user_session

            main_window = MainWindow(user=new_user)
            main_window.show()
            
            app = QApplication.instance()
            if app is not None:
                app.main_window = main_window
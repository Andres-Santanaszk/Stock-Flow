import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QStackedWidget,
    QFrame, QDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from pathlib import Path
import qdarktheme
from ui.login_window import LoginDialog
from ui.item_form import ItemFormWidget
from ui.register_hub import RegisterHubWidget



# Diccionario de roles y sus permisos (simulación)
ROLES_PERMISSIONS = {
    "Administrador": ["Management", "Inventory", "Requests", "Visibility", "Dashboard", "management", "history", "administration", "register_item"],
    "Líder": ["Inventory", "Requests", "Visibility", "Dashboard"],
    "Operador de Almacén": ["Inventory", "Requests", "Dashboard"],
    "Líder de Producción / Otro": ["Requests", "Visibility", "Dashboard"]
}
BASE_DIR = Path(__file__).resolve().parent
logo_path = BASE_DIR / "utils" / "logo_white_letters.svg"

class PlaceholderWidget(QFrame):
    """
    Widget de marcador de posición para cada módulo.
    Muestra el nombre del módulo y el rol del usuario actual.
    """
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

        # Mensaje específico para las vistas de solo lectura (Módulo 4)
        
        layout.addWidget(title_label)
        layout.addWidget(role_label)
        
        # Adaptación ligera del frame para que sea menos brillante en Dark Mode
        self.setStyleSheet("""
            QFrame {
                background-color: #3C3F41; /* Fondo ligeramente más oscuro que el fondo principal del tema */
                border: 1px solid #555555;
                border-radius: 10px;
                color: #ECEFF1; /* Asegura que el texto general sea claro */
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Flow")
        self.setGeometry(100, 100, 1200, 800)
        
        # Simulamos un usuario logueado
        self.current_user_role = "Administrador" 
        
        self._setup_styles()
        self._setup_ui()
        self._apply_role_permissions()
        
        # Conexión inicial para mostrar la vista por defecto
        self.btn_dashboard.click()

    def _setup_styles(self):
        """Estilos generales para la ventana principal y la barra lateral, ajustados para Dark Theme."""
        
        # Los colores de la barra lateral se ajustan para tener mejor contraste en el tema oscuro.
        self.setStyleSheet("""
            QMainWindow {
                /* Fondo de QMainWindow será manejado por qdarktheme */
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
                background-color: #f7c774; /* Color de acento para botón seleccionado */
                color: black;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #f7a51b; /* Color de acento para botón seleccionado */
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            #SidebarFrame {
                background-color: #2D2D30; /* Fondo oscuro específico para la barra lateral */
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

        # 1. Barra Lateral (Sidebar)
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarFrame")
        self.sidebar_frame.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 0, 10, 10)
        self.sidebar_layout.setSpacing(8)
        
        logo_widget = QSvgWidget(str(logo_path))
        logo_widget.setObjectName("HeaderLabel")
        logo_widget.setMaximumHeight(180)
        self.sidebar_layout.addWidget(logo_widget)

        self._setup_sidebar_buttons()
        self.sidebar_layout.addLayout(self.buttons_layout)
        self.sidebar_layout.addStretch()
        
        # Etiqueta de usuario y botón de Logout
        self._setup_user_info()

        main_layout.addWidget(self.sidebar_frame)

        # 2. Área Central (Central Area)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget { padding: 5px; }")
        
        self._setup_central_views()
        
        main_layout.addWidget(self.stacked_widget)
    
    def _setup_sidebar_buttons(self):
        """Define y conecta los botones de navegación."""
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(2)
        
        # Mapeo de botones a sus títulos y IDs de permiso
        self.button_map = {
            "Dashboard": ("🏠 Inicio", "Dashboard"),
            "Registrar_Item": ("📝 Registro", "register_item"),
            # Módulo 2: Operaciones de Inventario
            "Movimientos de inventario": ("📦 Movimientos", "Inventory"),
            # Módulo 4: Visualización de Inventario
            "Inventory On Hand": ("📊 Inventario", "Visibility"),
            "Localización": ("📌 Ubicaciones", "Visibility"),
            # Módulo 1: Gestión de Usuarios y Roles
            "Gestión de Roles": ("👥 Administrar usuarios", "management"),
            "Historial de Movimientos": ("📜 Historial transacciones", "history"),
            "Administrar inventario": ("🛠️ Catálogos", "administration")
        }
        
        self.buttons = {}
        for key, (text, permission_id) in self.button_map.items():
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._switch_view(k, checked))
            btn.setProperty("permission_id", permission_id) # Usado para restricción de roles
            self.buttons[key] = btn
            self.buttons_layout.addWidget(btn)
        
        # Botón Dashboard/Inicio (Siempre debe estar visible y es el primero)
        self.btn_dashboard = self.buttons["Dashboard"]
    
    def _setup_user_info(self):
        """Configura la etiqueta de usuario y el botón de Logout."""
        user_info_frame = QFrame()
        user_info_frame.setStyleSheet("""
            QFrame {
                border-top: 1px solid #555555; 
                padding-top: 10px;
            }
            QLabel {
                color: #ECEFF1; 
            }
        """)
        user_info_layout = QVBoxLayout(user_info_frame)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        
        role_label = QLabel(f"Rol: <b>{self.current_user_role}</b>")
        role_label.setFont(QFont("Segoe UI", 10))
        user_info_layout.addWidget(role_label)
        
        #Logout
        btn_logout = QPushButton("Cerrar Sesión / Logout")
        btn_logout.clicked.connect(self._handle_logout)
        btn_logout.setStyleSheet("QPushButton { background-color: #D32F2F; color: white; } QPushButton:hover { background-color: #EF5350; }")
        
        user_info_layout.addWidget(btn_logout)
        self.sidebar_layout.addWidget(user_info_frame)

    def _setup_central_views(self):
        """Crea y añade los widgets al QStackedWidget."""
        self.view_widgets = {}
        for key, (title, _) in self.button_map.items():
            if key == "Registrar_Item":  # 👈 clave que ya tienes en el sidebar
                widget = RegisterHubWidget(self)   # ← aquí va el hub con 3 botones
            else:
                widget = PlaceholderWidget(title, self.current_user_role)
            self.view_widgets[key] = widget
            self.stacked_widget.addWidget(widget)


    def _switch_view(self, key, checked):
        """Maneja el cambio de vista en el QStackedWidget."""
        if not checked:
            return

        # Desactivar todos los demás botones
        for other_key, btn in self.buttons.items():
            if other_key != key:
                btn.setChecked(False)
        
        # Cambiar el widget en el stack
        widget = self.view_widgets.get(key)
        if widget:
            index = self.stacked_widget.indexOf(widget)
            self.stacked_widget.setCurrentIndex(index)
            print(f"DEBUG: Cambiando a la vista: {key}")

    def _apply_role_permissions(self):
        """Habilita/deshabilita botones según el rol del usuario."""
        required_permissions = ROLES_PERMISSIONS.get(self.current_user_role, [])
        
        for key, btn in self.buttons.items():
            permission_id = btn.property("permission_id")
            
            # El Dashboard siempre está visible si tiene el permiso "Dashboard"
            if permission_id == "Dashboard" and permission_id in required_permissions:
                btn.setEnabled(True)
                continue

            if permission_id in required_permissions:
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)
                # Estilo de botón deshabilitado que se ve bien en Dark Mode
                disabled_style = "QPushButton { color: #888888; background-color: #38383a; }"
                btn.setStyleSheet(btn.styleSheet() + disabled_style)
                btn.setText(f"{self.button_map[key][0]} (Acceso Denegado)")
                print(f"INFO: Botón '{key}' deshabilitado para rol '{self.current_user_role}'.")

    def _handle_logout(self):
        """Simulación de la acción de cerrar sesión."""
        print("INFO: Usuario cerró sesión (Logout).")
        # En una aplicación real, aquí se cerraría la ventana de la App y se abriría la de Login.
        self.close()
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.Accepted and login_dialog.valid_login:
            # Si el login fue correcto, reabrir la ventana principal
            main_window = MainWindow()
            main_window.show()
            # Mantener la app viva: pasamos la referencia al QApplication
            app.main_window = main_window
        

if __name__ == "__main__":
    # La aplicación de PySide6
    app = QApplication(sys.argv)
    
    # 1. Aplicar el tema oscuro (Dark Theme)
    # Se usa 'light' para el modo claro o 'dark' para el modo oscuro.
    # qdarktheme.setup_theme(theme='dark', corner_radius=5) 
    
    qdarktheme.setup_theme()
    
    icon_path = BASE_DIR / "utils" / "icon.png"
    app_icon = QIcon(str(icon_path))
    app.setWindowIcon(app_icon)
    app.setFont(QFont("Segoe UI"))
    
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.Accepted and login_dialog.valid_login:
        main_window = MainWindow()
        main_window.show()
        app.main_window = main_window  # mantener referencia
        sys.exit(app.exec())
    else:
        # Si el login se cancela o es incorrecto → cerrar app
        print("INFO: Inicio de sesión cancelado o inválido.")
        sys.exit(0)

    
    sys.exit(app.exec())

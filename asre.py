import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                               QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor
import qtawesome as qta  # Librería para íconos (FontAwesome)

class ModernInventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inventarios - Stock Flow")
        self.resize(1000, 700)

        # Estilos generales (CSS-like)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f7f6; /* Background general claro */
            }
            /* Estilo del Sidebar */
            QFrame#sidebar {
                background-color: #2c3e50; /* Dark Slate Blue */
                border-radius: 0px;
            }
            QLabel#app_title {
                color: #ecf0f1;
                font-weight: bold;
                font-size: 18px;
                padding: 20px;
            }
            QLabel#section_label {
                color: #95a5a6;
                font-size: 12px;
                font-weight: bold;
                padding-left: 20px;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            /* Botones del menú */
            QPushButton {
                background-color: transparent;
                color: #bdc3c7;
                text-align: left;
                padding: 12px 20px;
                border: none;
                font-size: 14px;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #34495e;
                color: #ffffff;
            }
            QPushButton:checked {
                background-color: #34495e;
                color: #ffffff;
                border-left: 4px solid #3498db; /* Acento azul al estar activo */
            }
            /* Content Area */
            QFrame#content_frame {
                background-color: #ffffff;
                border-top-left-radius: 20px; /* Borde redondeado moderno */
            }
        """)

        # --- Main Layout Container ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. Sidebar (Izquierda) ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 20)
        sidebar_layout.setSpacing(0)

        # Título de la App
        title_label = QLabel("📦 Stock Flow")
        title_label.setObjectName("app_title")
        sidebar_layout.addWidget(title_label)

        # Navegación
        # --- Sección Dashboard ---
        self.btn_dashboard = self.create_nav_button("Dashboard", "fa5s.chart-line")
        sidebar_layout.addWidget(self.btn_dashboard)

        # --- Sección Transacciones (Transactions) ---
        sidebar_layout.addWidget(self.create_section_label("MOVIMIENTOS"))
        
        self.btn_entry = self.create_nav_button("Entrada de Insumos", "fa5s.dolly")
        sidebar_layout.addWidget(self.btn_entry)
        
        self.btn_exit = self.create_nav_button("Salida de Insumos", "fa5s.shipping-fast")
        sidebar_layout.addWidget(self.btn_exit)
        
        self.btn_adjust = self.create_nav_button("Ajuste de Inventario", "fa5s.balance-scale")
        sidebar_layout.addWidget(self.btn_adjust)

        # --- Sección Catálogos (Master Data) ---
        sidebar_layout.addWidget(self.create_section_label("CATÁLOGOS"))
        
        self.btn_items = self.create_nav_button("Items / Productos", "fa5s.boxes")
        sidebar_layout.addWidget(self.btn_items)
        
        self.btn_brands = self.create_nav_button("Marcas", "fa5s.tag")
        sidebar_layout.addWidget(self.btn_brands)

        # Spacer para empujar todo hacia arriba
        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Footer del sidebar (Settings/Logout)
        self.btn_settings = self.create_nav_button("Configuración", "fa5s.cog")
        sidebar_layout.addWidget(self.btn_settings)

        # --- 2. Content Area (Derecha) ---
        self.content_area = QFrame()
        self.content_area.setObjectName("content_frame")
        content_layout = QVBoxLayout(self.content_area)

        # Stacked Widget para cambiar vistas
        self.pages = QStackedWidget()
        content_layout.addWidget(self.pages)

        # Agregamos páginas dummy para probar la navegación
        self.pages.addWidget(self.create_dummy_page("Dashboard - Resumen General"))
        self.pages.addWidget(self.create_dummy_page("Entrada de Insumos (Stock In)"))
        self.pages.addWidget(self.create_dummy_page("Salida de Insumos (Stock Out)"))
        self.pages.addWidget(self.create_dummy_page("Ajustes (Adjustments)"))
        self.pages.addWidget(self.create_dummy_page("Gestión de Items"))
        self.pages.addWidget(self.create_dummy_page("Gestión de Marcas"))
        self.pages.addWidget(self.create_dummy_page("Configuración"))

        # Conectar botones a las páginas
        # Usamos lambda para pasar el índice
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard))
        self.btn_entry.clicked.connect(lambda: self.switch_page(1, self.btn_entry))
        self.btn_exit.clicked.connect(lambda: self.switch_page(2, self.btn_exit))
        self.btn_adjust.clicked.connect(lambda: self.switch_page(3, self.btn_adjust))
        self.btn_items.clicked.connect(lambda: self.switch_page(4, self.btn_items))
        self.btn_brands.clicked.connect(lambda: self.switch_page(5, self.btn_brands))
        self.btn_settings.clicked.connect(lambda: self.switch_page(6, self.btn_settings))

        # Inicializar en Dashboard
        self.btn_dashboard.click()

        # Agregar widgets al layout principal
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)

    def create_nav_button(self, text, icon_name):
        """Helper to create styled buttons with icons"""
        btn = QPushButton(text)
        # Usamos qtawesome para iconos vectoriales modernos
        icon = qta.icon(icon_name, color="#bdc3c7")
        btn.setIcon(icon)
        btn.setIconSize(QSize(20, 20))
        btn.setCheckable(True)
        btn.setAutoExclusive(True) # Solo uno puede estar activo a la vez
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def create_section_label(self, text):
        """Helper for section headers in sidebar"""
        lbl = QLabel(text)
        lbl.setObjectName("section_label")
        return lbl

    def create_dummy_page(self, title_text):
        """Creates a placeholder page for content"""
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        return page

    def switch_page(self, index, button_sender):
        """Logic to switch stacked widget index and handle icon colors"""
        self.pages.setCurrentIndex(index)
        
        # Opcional: Cambiar color del icono activo (Visual Feedback)
        # Restaurar todos los iconos a gris primero si deseas lógica compleja, 
        # pero el stylesheet QSS maneja la mayoría del estado visual.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernInventoryApp()
    window.show()
    sys.exit(app.exec())
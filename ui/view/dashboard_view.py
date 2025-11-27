import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

# --- Matplotlib Integration ---
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# IMPORTACIÓN SOLICITADA
from entities.Dashboard import DashboardService

# --- CONFIGURACIÓN DE TEMA Y COLORES ---
THEME = {
    "bg_app": "#181820",
    "bg_card": "#3c3f41",
    "text_white": "#ffffff",
    "text_gray": "#ffffff",
    "font_family": "Segoe UI"
}

COLORS = {
    "donut": ["#00d4ff", "#ffae00", "#ff4d4d", "#ae00ff", "#00ff88"],
    "user_bar": "#f7a51b",
    "critical_min": "#ff4d4d", # Rojo
    "critical_curr": "#00ff88" # Verde
}

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_alpha(0)
        self.axes = self.fig.add_subplot(111)
        self.axes.patch.set_alpha(0)
        super().__init__(self.fig)
        self.setStyleSheet("background: transparent;")

class ChartCard(QFrame):
    def __init__(self, title, subtitle, widget, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME['bg_card']};
                border-radius: 16px;
                border: 1px solid #4a4d50;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"""
            color: #ffae00; 
            font-family: "{THEME['font_family']}"; 
            font-size: 16px; 
            font-weight: bold;
            background: transparent; border: none;
        """)
        
        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet(f"""
            color: {THEME['text_gray']}; 
            font-family: "{THEME['font_family']}"; 
            font-size: 12px;
            background: transparent; border: none;
        """)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_sub)
        layout.addSpacing(10)
        
        widget.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(widget)

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = DashboardService()
        
        self.setStyleSheet(f"background-color: {THEME['bg_app']};")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 1. Header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #202124; /* Este es el 'azul' oscuro de fondo */
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 5, 0, 5)

        lbl_dash = QLabel("Dashboard de Stock Flow")
        lbl_dash.setAlignment(Qt.AlignCenter)
        lbl_dash.setStyleSheet(f"""
            color: #ffae00; 
            font-size: 48px; 
            font-weight: 800; 
            font-family: {THEME['font_family']};
            background: transparent; /* Importante para que tome el color del frame */
            border: none;
        """)
        
        header_layout.addWidget(lbl_dash)
        main_layout.addWidget(header_frame)
        main_layout.addSpacing(20)

        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(content)
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(0,0,0,0)

        # --- AJUSTE DE TAMAÑOS (Stretch Factors) ---
        # Columna 0 (Donut): Peso 1 (Pequeño)
        self.grid.setColumnStretch(0, 1)
        # Columna 1 (Alertas): Peso 2 (Grande - Doble de ancho)
        self.grid.setColumnStretch(1, 2)

        # 3. Inicializar Gráficos
        self.init_donut_chart()      
        self.init_critical_chart()   
        self.init_user_chart()       

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    # ---------------------------------------------------------
    # GRÁFICO 1: DONA (Pequeño)
    # ---------------------------------------------------------
    def init_donut_chart(self):
        data = self.service.get_category_distribution()
        # Reducimos el ancho físico del canvas (width=4)
        canvas = MplCanvas(self, width=4, height=4, dpi=90)
        ax = canvas.axes

        if data:
            labels = [row[0] for row in data]
            values = [row[1] for row in data]
            total_stock = sum(values)

            wedges, texts = ax.pie(
                values, 
                startangle=90, 
                colors=COLORS['donut'], 
                wedgeprops=dict(width=0.35, edgecolor=THEME['bg_card'])
            )
            
            # Ajuste leyenda para espacio reducido
            ax.legend(wedges, labels, 
                      loc="center left", 
                      bbox_to_anchor=(0.85, 0, 0.5, 1), # Ajustado ligeramente
                      frameon=False, 
                      labelcolor="white",
                      fontsize=8) # Fuente más pequeña
            
            ax.text(0, 0.1, f"{total_stock}", ha='center', va='center', 
                    color='white', fontsize=20, fontweight='bold', fontfamily=THEME['font_family'])
            
            ax.text(0, -0.2, "Unidades\nTotales", ha='center', va='center', 
                    color=THEME['text_gray'], fontsize=8, fontfamily=THEME['font_family'])
        else:
            ax.text(0, 0, "Sin Datos", color="white", ha='center')

        card = ChartCard("Informe de Stock", "Por Categoría", canvas)
        self.grid.addWidget(card, 0, 0)

    # ---------------------------------------------------------
    # GRÁFICO 2: BARRAS VERTICALES (Alertas Stock) - CORREGIDO
    # ---------------------------------------------------------
    def init_critical_chart(self):
        data = self.service.get_critical_stock()
        
        # Mantenemos el ancho, pero el margen interno hará el gráfico "útil" más pequeño
        canvas = MplCanvas(self, width=8, height=4, dpi=90)
        ax = canvas.axes

        if data:
            names = [row[0] for row in data] 
            min_vals = [row[1] for row in data]
            curr_vals = [row[2] for row in data]
            x = np.arange(len(names))
            
            # --- AJUSTE CLAVE DE MÁRGENES ---
            # 'bottom=0.40' reserva el 40% de la altura del gráfico PARA EL TEXTO.
            # Esto evita que se corten los nombres.
            canvas.fig.subplots_adjust(bottom=0.40, top=0.90, left=0.10, right=0.95)

            # Barras
            ax.bar(x - 0.2, min_vals, 0.4, label='Mínimo', color=COLORS['critical_min'])
            ax.bar(x + 0.2, curr_vals, 0.4, label='Actual', color=COLORS['critical_curr'])

            # Estilo Ejes
            ax.set_xticks(x)
            
            # Rotación aumentada a 30 grados y alineación derecha (ha='right')
            # para que el texto termine justo debajo de la barra, no centrado
            ax.set_xticklabels(names, color=THEME['text_white'], fontsize=9, rotation=30, ha='right')
            
            ax.legend(frameon=False, labelcolor="white", loc='upper right', fontsize=8)
            
            for spine in ax.spines.values(): 
                spine.set_visible(False)
            
            ax.tick_params(left=False, bottom=False)
            ax.tick_params(axis='y', colors=THEME['text_white'])
            ax.grid(axis='y', color='#444444', linestyle='--', alpha=0.3)
            
        else:
            ax.text(0.5, 0.5, "Todo el stock saludable", color="white", ha='center')

        card = ChartCard("Alertas de Stock", "Mínimo (Rojo) vs Actual (Verde)", canvas)
        self.grid.addWidget(card, 0, 1)

    # ---------------------------------------------------------
    # GRÁFICO 3: BARRAS HORIZONTALES (Top Usuarios)
    # ---------------------------------------------------------
    def init_user_chart(self):
        data = self.service.get_top_users_movements()
        canvas = MplCanvas(self, width=10, height=3.5, dpi=90)
        ax = canvas.axes

        if data:
            data.reverse()
            users = [row[0] for row in data]
            counts = [row[1] for row in data]
            y_pos = np.arange(len(users))

            canvas.fig.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.1)

            bars = ax.barh(y_pos, counts, color=COLORS['user_bar'], height=0.6)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(users, color="white", fontsize=10, fontweight='bold', ha='right')
            ax.set_xticks([]) 

            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, 
                        f'{int(width)}', 
                        ha='left', va='center', color='white', fontweight='bold')

            for spine in ax.spines.values(): 
                spine.set_visible(False)
            ax.tick_params(left=False, bottom=False)

        else:
             ax.text(0.5, 0.5, "Sin actividad de usuarios reciente", color="white", ha='center')

        card = ChartCard("Actividad por Usuario", "Personal con mayor número de movimientos registrados", canvas)
        self.grid.addWidget(card, 1, 0, 1, 2)
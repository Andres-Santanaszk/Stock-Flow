from PySide6.QtCore import QSize, QEasingCurve, QPropertyAnimation, QRectF, QPoint, Qt, Property
from PySide6.QtWidgets import QPushButton, QCheckBox
from PySide6.QtGui import QPainter, QColor, QBrush

class IconHoverAnimationMixin:
    """
    Mixin que agrega animación de tamaño de ícono al hacer hover.
    Se puede combinar con QPushButton, QToolButton, etc.
    """

    def _setup_icon_hover_animation(
        self,
        base_icon_size=QSize(24, 24),
        hover_icon_size=QSize(32, 32),
        duration_ms=150,
    ):
        self._base_icon_size = base_icon_size
        self._hover_icon_size = hover_icon_size

        # Tamaño inicial
        self.setIconSize(self._base_icon_size)

        # Una sola animación, cambiando endValue según el caso
        self._icon_anim = QPropertyAnimation(self, b"iconSize")
        self._icon_anim.setDuration(duration_ms)
        self._icon_anim.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        # Cuando el mouse entra, agrandamos el ícono
        if hasattr(self, "_icon_anim"):
            self._icon_anim.stop()
            self._icon_anim.setStartValue(self.iconSize())
            self._icon_anim.setEndValue(self._hover_icon_size)
            self._icon_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Cuando el mouse sale, lo regresamos al tamaño base
        if hasattr(self, "_icon_anim"):
            self._icon_anim.stop()
            self._icon_anim.setStartValue(self.iconSize())
            self._icon_anim.setEndValue(self._base_icon_size)
            self._icon_anim.start()
        super().leaveEvent(event)


class AnimatedButton(IconHoverAnimationMixin, QPushButton):
    def __init__(
        self,
        text="",
        parent=None,
        base_icon_size=QSize(24, 24),
        hover_icon_size=QSize(32, 32),
    ):
        super().__init__(text, parent)

        self._setup_icon_hover_animation(
            base_icon_size=base_icon_size,
            hover_icon_size=hover_icon_size,
        )

class SwitchButton(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. CONFIGURACIÓN BÁSICA
        self.setFixedSize(60, 30)  # Definimos el tamaño fijo del switch
        self.setCursor(Qt.PointingHandCursor)  # Cambiamos el cursor a "manita"

        # Colores (Estilo "Flat")
        self._track_color_off = QColor("#BDC3C7")  # Gris
        self._track_color_on = QColor("#2ECC71")  # Verde
        self._thumb_color = QColor("#FFFFFF")  # Blanco

        # 2. PREPARAR LA ANIMACIÓN
        # Esta variable '_thumb_x' guardará la posición X del círculo blanco.
        # Empieza en 3 píxeles (izquierda).
        self._thumb_x = 3

        self._animation = QPropertyAnimation(self, b"thumb_pos", self)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)  # Aceleración suave
        self._animation.setDuration(250)  # Duración: 250 milisegundos

        # Conectamos el cambio de estado (click) con la función de animación
        self.stateChanged.connect(self.start_transition)

    # 3. DEFINIR LA PROPIEDAD ANIMABLE
    # PySide necesita métodos get/set para que la animación sepa qué modificar
    @Property(float)
    def thumb_pos(self):
        return self._thumb_x

    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_x = pos
        self.update()  # ¡IMPORTANTE! Pide redibujar el widget cada vez que se mueve un milímetro

    # 4. LÓGICA DE TRANSICIÓN
    def start_transition(self, state):
        self._animation.stop()  # Detener cualquier animación en curso
        if state:
            # Si está ACTIVO (checked), movemos el círculo a la derecha
            # (Ancho total - Ancho círculo - Margen)
            target = self.width() - 26 - 3
            self._animation.setEndValue(target)
        else:
            # Si está INACTIVO, movemos a la izquierda
            self._animation.setEndValue(3)

        self._animation.start()

    # 5. ÁREA DE CLIC (HITBOX)
    def hitButton(self, pos: QPoint):
        # Le decimos a Qt que CUALQUIER clic dentro del widget es válido.
        return self.contentsRect().contains(pos)

    # 6. EL PINTOR (La parte visual)
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)  # Suavizar bordes (antidentado)
        p.setPen(Qt.NoPen)  # Sin bordes negros feos

        # A. Dibujar el FONDO (Track)
        rect = QRectF(0, 0, self.width(), self.height())

        if self.isChecked():
            p.setBrush(QBrush(self._track_color_on))
        else:
            p.setBrush(QBrush(self._track_color_off))

        # Dibujamos rectángulo redondeado (x, y, w, h, radioX, radioY)
        p.drawRoundedRect(rect, 15, 15)

        # B. Dibujar el CÍRCULO (Thumb)
        p.setBrush(QBrush(self._thumb_color))
        # Usamos la variable self._thumb_x que la animación está actualizando
        p.drawEllipse(self._thumb_x, 3, 24, 24)

        p.end()
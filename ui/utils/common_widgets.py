from PySide6.QtCore import QSize, QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QPushButton, QToolButton

class IconHoverAnimationMixin:
    def _setup_icon_hover_animation(
        self,
        base_icon_size=QSize(24, 24),
        hover_icon_size=QSize(32, 32),
        duration_ms=150,
    ):
        self._base_icon_size = base_icon_size
        self._hover_icon_size = hover_icon_size

        self.setIconSize(self._base_icon_size)

        self._icon_anim = QPropertyAnimation(self, b"iconSize")
        self._icon_anim.setDuration(duration_ms)
        self._icon_anim.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        if hasattr(self, "_icon_anim"):
            self._icon_anim.stop()
            self._icon_anim.setStartValue(self.iconSize())
            self._icon_anim.setEndValue(self._hover_icon_size)
            self._icon_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
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

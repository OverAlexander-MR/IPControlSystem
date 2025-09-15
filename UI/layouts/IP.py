from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QPointF

from math import sin, cos

# Dracula palette
DRACULA = {
    "bg": "#282a36",
    "panel": "#21222c",
    "current_line": "#44475a",
    "fg": "#f8f8f2",
    "muted": "#6272a4",
    "accent": "#bd93f9",
    "green": "#50fa7b",
    "red": "#ff5555",
    "orange": "#ffb86c",
}


class PendulumWidget(QWidget):
    """Widget que dibuja un carrito (cart), una varilla (rod) y una masa (bob).

    La función `set_state(cart_pos, cart_vel, theta, theta_dot)` actualiza el estado
    visual y provoca un repintado. `cart_pos` se interpreta como valor normalizado en
    el rango [-1, 1] (izquierda a derecha). Si tus datos vienen en metros, normalízalos
    antes de pasarlos al widget o ajusta `pos_scale`.

    Parámetros visuales:
        - cart_width, cart_height: tamaño del carrito en píxeles
        - rod_length_ratio: fracción de la altura del widget que ocupa la varilla
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Estado (valores por defecto)
        self.cart_pos = 0.0  # normalizado -1..1
        self.cart_vel = 0.0
        self.theta = 0.0  # radians, 0 = vertical up
        self.theta_dot = 0.0

        # Visual tuning
        self.cart_width = 120
        self.cart_height = 36
        self.rod_length_ratio = 0.35  # fraction of widget height
        self.pivot_offset_y = 6  # pixels above cart top where pivot is

        # Mapping: si tus datos provienen en metros, ajusta pos_scale
        self.pos_scale = 1.0

        # Make sure widget repaints smoothly
        self.setMinimumHeight(220)

    def set_state(
        self, cart_pos: float, cart_vel: float, theta: float, theta_dot: float
    ):
        """Actualiza el estado y repinta.

        - cart_pos: normalizado en [-1,1] (izquierda a derecha)
        - cart_vel: velocidad del carrito (no usada para dibujo actualmente)
        - theta: ángulo en radianes, 0 apunta hacia arriba, positivo hacia la derecha
        - theta_dot: velocidad angular
        """
        self.cart_pos = max(-1.0, min(1.0, float(cart_pos)))
        self.cart_vel = float(cart_vel)
        self.theta = float(theta)
        self.theta_dot = float(theta_dot)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Background (transparent assumed; parent frame draws border)
        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.transparent))

        # Compute mapping for cart x: map [-1,1] to available track width
        margin = 24
        track_left = margin
        track_right = w - margin
        track_width = max(1, track_right - track_left)

        # position in pixels
        x_pix = track_left + (self.cart_pos + 1.0) / 2.0 * track_width

        # Cart rectangle
        cart_w = min(self.cart_width, track_width * 0.35)
        cart_h = self.cart_height
        cart_x = x_pix - cart_w / 2
        cart_y = h * 0.55  # baseline vertical position (will scale with widget)

        # Draw track line
        pen = QPen(DRACULA["muted"])
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(
            int(track_left),
            int(cart_y + cart_h / 2 + 10),
            int(track_right),
            int(cart_y + cart_h / 2 + 10),
        )

        # Draw cart body
        cart_rect_brush = QBrush(DRACULA["panel"])  # darker body
        cart_border = QPen(DRACULA["current_line"])  # border
        cart_border.setWidth(2)
        painter.setPen(cart_border)
        painter.setBrush(cart_rect_brush)
        painter.drawRoundedRect(
            int(cart_x), int(cart_y), int(cart_w), int(cart_h), 6, 6
        )

        # Wheels
        wheel_radius = 8
        wheel_pen = QPen(DRACULA["current_line"])
        wheel_pen.setWidth(2)
        painter.setPen(wheel_pen)
        painter.setBrush(QBrush(DRACULA["muted"]))
        left_wheel_c = QPointF(cart_x + cart_w * 0.22, cart_y + cart_h + wheel_radius)
        right_wheel_c = QPointF(cart_x + cart_w * 0.78, cart_y + cart_h + wheel_radius)
        painter.drawEllipse(left_wheel_c, wheel_radius, wheel_radius)
        painter.drawEllipse(right_wheel_c, wheel_radius, wheel_radius)

        # Pivot point (top center of cart)
        pivot_x = x_pix
        pivot_y = cart_y - self.pivot_offset_y

        # Rod length
        rod_length = h * self.rod_length_ratio

        # Bob position (theta: 0 = up)
        # Convert theta so that 0 rad => up (negative y direction)
        bob_x = pivot_x + rod_length * sin(self.theta)
        bob_y = pivot_y - rod_length * cos(self.theta)

        # Draw rod
        rod_pen = QPen(DRACULA["fg"])  # bright rod
        rod_pen.setWidth(3)
        painter.setPen(rod_pen)
        painter.drawLine(int(pivot_x), int(pivot_y), int(bob_x), int(bob_y))

        # Draw pivot
        pivot_brush = QBrush(DRACULA["accent"])
        painter.setBrush(pivot_brush)
        painter.setPen(QPen(DRACULA["accent"]))
        painter.drawEllipse(QPointF(pivot_x, pivot_y), 4, 4)

        # Draw bob (mass)
        bob_radius = max(10, int(min(28, h * 0.05)))
        painter.setPen(QPen(DRACULA["current_line"]))
        painter.setBrush(QBrush(DRACULA["orange"]))
        painter.drawEllipse(QPointF(bob_x, bob_y), bob_radius, bob_radius)

        painter.end()


# Small test when se ejecuta directamente
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer
    import random

    app = QApplication(sys.argv)
    w = PendulumWidget()
    w.resize(600, 440)
    w.show()

    def random_update():
        t = random.random() * 2 - 1
        theta = (random.random() - 0.5) * 0.6
        w.set_state(t, random.random(), theta, random.random() - 0.5)

    timer = QTimer()
    timer.timeout.connect(random_update)
    timer.start(200)

    sys.exit(app.exec())

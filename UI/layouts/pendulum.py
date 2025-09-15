from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QSizePolicy,
    QFrame,
    QSpacerItem,
)
from PySide6.QtCore import Qt, QTimer

from .IP import PendulumWidget


class PendulumPage(QWidget):
    """Página del péndulo: diseño con dos menús desplegables y botones Ejecutar/Parar.

    Ahora integra `PendulumWidget` en la zona de visualización y expone el método
    `update_pendulum_state(cart_pos, cart_vel, theta, theta_dot)` para actualizar
    su estado desde fuera (por ejemplo, desde un hilo, un QTimer o una rutina de lectura serial).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("page_pendulum_custom")
        self._build_ui()

        # Timer de prueba (si quieres alimentar datos de prueba desde aquí, puedes conectar)
        self._test_timer = None
        self.control = True

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Título y subtítulo
        title = QLabel("Pendulum")
        title.setObjectName("page_title")
        subtitle = QLabel("Visualización y controles del péndulo")
        subtitle.setObjectName("page_subtitle")
        subtitle.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Marco para el área de controles con borde
        control_frame = QFrame()
        control_frame.setFrameStyle(QFrame.Shape.Box)
        control_frame.setLineWidth(1)
        control_frame.setStyleSheet("QFrame { border-color: #6272a4; }")

        control_layout = QVBoxLayout(control_frame)
        control_layout.setContentsMargins(12, 12, 12, 12)

        # Fila superior con los menús y botones
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        # Tipo de control
        lbl_control = QLabel("Tipo de control:")
        lbl_control.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        self.combo_control = QComboBox()
        self.combo_control.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.combo_control.addItems(["LQR", "LQR + Swim up", "SAC", "DDPG"])
        self.combo_control.currentTextChanged.connect(self._on_control_changed)

        top_row.addWidget(lbl_control)
        top_row.addWidget(self.combo_control)

        # Espacio separador
        top_row.addSpacing(16)

        # Puertos COM (intenta listar puertos si pyserial está disponible)
        lbl_com = QLabel("Puertos COM:")
        lbl_com.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.combo_com = QComboBox()
        self.combo_com.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._populate_com_ports()
        self.combo_com.currentTextChanged.connect(self._on_com_changed)

        top_row.addWidget(lbl_com)
        top_row.addWidget(self.combo_com)

        # Espacio separador
        top_row.addStretch(1)

        # Botones Ejecutar / Parar
        self.btn_run = QPushButton("▶️")
        self.btn_run.setFixedSize(44, 36)
        self.btn_run.clicked.connect(self._on_run)

        self.btn_stop = QPushButton("⏸️")
        self.btn_stop.setFixedSize(44, 36)
        self.btn_stop.clicked.connect(self._on_stop)

        top_row.addWidget(self.btn_run)
        top_row.addWidget(self.btn_stop)

        control_layout.addLayout(top_row)
        main_layout.addWidget(control_frame)

        # Marco para la visualización con borde
        visualization_frame = QFrame()
        visualization_frame.setFrameStyle(QFrame.Shape.Box)
        visualization_frame.setLineWidth(1)
        visualization_frame.setStyleSheet("QFrame { border-color: #6272a4; }")
        visualization_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        visualization_layout = QVBoxLayout(visualization_frame)
        visualization_layout.setContentsMargins(12, 12, 12, 12)

        # PendulumWidget
        self.pendulum_widget = PendulumWidget()
        self.pendulum_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        visualization_layout.addWidget(self.pendulum_widget)

        # Añadir el marco de visualización con un factor de estiramiento
        main_layout.addWidget(visualization_frame, 1)  # El factor 1 hace que se expanda

        # Añadir un espaciador en la parte inferior para mantener un margen fijo
        bottom_spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Fixed
        )
        main_layout.addItem(bottom_spacer)

    def _populate_com_ports(self):
        """Intenta obtener puertos serie con pyserial; si falla, agrega valores por defecto."""
        ports = []
        try:
            import serial.tools.list_ports as list_ports

            ports = [p.device for p in list_ports.comports()]
        except Exception:
            # pyserial no disponible o no se pudo listar
            ports = []

        if not ports:
            ports = ["COM3", "COM4", "COM5", "/dev/ttyUSB0", "/dev/ttyACM0"]

        self.combo_com.clear()
        self.combo_com.addItems(ports)

    # callbacks (solo prints para prueba)
    def _on_control_changed(self, text: str):
        print(f"[Pendulum] Tipo de control seleccionado: {text}")

    def _on_com_changed(self, text: str):
        print(f"[Pendulum] Puerto COM seleccionado: {text}")

    def _on_run(self):
        control = self.combo_control.currentText()
        com = self.combo_com.currentText()
        print(f"[Pendulum] Ejecutar -> Control: {control} | COM: {com}")

    def _on_stop(self):
        print("[Pendulum] Parar -> Stop pressed")

    # ----------------- Interfaz para actualizar el péndulo -----------------
    def update_pendulum_state(self, cart_pos, cart_vel, theta, theta_dot):
        """Recibe las variables y las pasa al widget para su representación visual.

        cart_pos se interpreta como valor normalizado en [-1,1].
        """
        self.pendulum_widget.set_state(cart_pos, cart_vel, theta, theta_dot)


# # Si se ejecuta este archivo como script, hacemos una demo con datos aleatorios
# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication
#     from utils.random_pendulum_data import RandomPendulumData

#     app = QApplication(sys.argv)
#     page = PendulumPage()
#     page.resize(900, 640)
#     page.show()

#     # Demo: alimentar el widget con datos de prueba
#     rnd = RandomPendulumData()

#     def tick():
#         cart_pos, cart_vel, theta, theta_dot = rnd.next(0.05)
#         page.update_pendulum_state(cart_pos, cart_vel, theta, theta_dot)

#     timer = QTimer()
#     timer.timeout.connect(tick)
#     timer.start(60)  # ~16-17 FPS

#     sys.exit(app.exec())

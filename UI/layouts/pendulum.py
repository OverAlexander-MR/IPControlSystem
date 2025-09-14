# from PySide6.QtWidgets import (
#     QWidget,
#     QVBoxLayout,
#     QHBoxLayout,
#     QLabel,
#     QComboBox,
#     QPushButton,
#     QFrame,
#     QSizePolicy,
# )
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon


# class PendulumPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         # Layout principal
#         main_layout = QVBoxLayout()
#         main_layout.setContentsMargins(20, 20, 20, 20)
#         main_layout.setSpacing(15)

#         # Título de la página
#         title_label = QLabel("Control del Péndulo Invertido")
#         title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         title_label.setStyleSheet(
#             """
#             QLabel {
#                 font-size: 24px;
#                 font-weight: bold;
#                 color: #bd93f9;
#                 padding: 10px;
#             }
#         """
#         )
#         main_layout.addWidget(title_label)

#         # Sección de controles
#         control_frame = QFrame()
#         control_frame.setStyleSheet(
#             """
#             QFrame {
#                 background-color: #44475a;
#                 border-radius: 8px;
#                 padding: 15px;
#             }
#         """
#         )

#         control_layout = QVBoxLayout(control_frame)

#         # Fila de selección de control
#         selection_layout = QHBoxLayout()

#         # Label y combo para tipo de control
#         control_label = QLabel("Tipo de Control:")
#         control_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
#         selection_layout.addWidget(control_label)

#         self.control_combo = QComboBox()
#         self.control_combo.addItems(["LQR", "LQR + Swim up", "SAC", "DDPG"])
#         self.control_combo.setStyleSheet(
#             """
#             QComboBox {
#                 background-color: #6272a4;
#                 color: #f8f8f2;
#                 border: 1px solid #bd93f9;
#                 border-radius: 4px;
#                 padding: 5px;
#                 min-width: 150px;
#             }
#             QComboBox::drop-down {
#                 border: none;
#             }
#             QComboBox QAbstractItemView {
#                 background-color: #6272a4;
#                 color: #f8f8f2;
#                 selection-background-color: #bd93f9;
#             }
#         """
#         )
#         self.control_combo.currentIndexChanged.connect(self.on_control_changed)
#         selection_layout.addWidget(self.control_combo)

#         # Espaciador
#         selection_layout.addStretch()

#         # Label y combo para puertos COM
#         port_label = QLabel("Puertos COM:")
#         port_label.setStyleSheet("color: #f8f8f2; font-weight: bold;")
#         selection_layout.addWidget(port_label)

#         self.port_combo = QComboBox()
#         # Simulamos algunos puertos COM
#         self.port_combo.addItems(["COM3", "COM4", "COM5", "COM6"])
#         self.port_combo.setStyleSheet(
#             """
#             QComboBox {
#                 background-color: #6272a4;
#                 color: #f8f8f2;
#                 border: 1px solid #bd93f9;
#                 border-radius: 4px;
#                 padding: 5px;
#                 min-width: 100px;
#             }
#             QComboBox::drop-down {
#                 border: none;
#             }
#             QComboBox QAbstractItemView {
#                 background-color: #6272a4;
#                 color: #f8f8f2;
#                 selection-background-color: #bd93f9;
#             }
#         """
#         )
#         self.port_combo.currentIndexChanged.connect(self.on_port_changed)
#         selection_layout.addWidget(self.port_combo)

#         control_layout.addLayout(selection_layout)

#         # Fila de botones de control
#         button_layout = QHBoxLayout()
#         button_layout.addStretch()

#         # Botón de ejecutar
#         self.run_button = QPushButton("▶️ Ejecutar")
#         self.run_button.setStyleSheet(
#             """
#             QPushButton {
#                 background-color: #50fa7b;
#                 color: #282a36;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 8px 16px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #69ff93;
#             }
#             QPushButton:pressed {
#                 background-color: #40c965;
#             }
#         """
#         )
#         self.run_button.clicked.connect(self.on_run_clicked)
#         button_layout.addWidget(self.run_button)

#         # Botón de pausa
#         self.pause_button = QPushButton("⏸️ Pausar")
#         self.pause_button.setStyleSheet(
#             """
#             QPushButton {
#                 background-color: #ffb86c;
#                 color: #282a36;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 8px 16px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #ffcc99;
#             }
#             QPushButton:pressed {
#                 background-color: #e6a056;
#             }
#         """
#         )
#         self.pause_button.clicked.connect(self.on_pause_clicked)
#         button_layout.addWidget(self.pause_button)

#         # Botón de detener
#         self.stop_button = QPushButton("⏹️ Detener")
#         self.stop_button.setStyleSheet(
#             """
#             QPushButton {
#                 background-color: #ff5555;
#                 color: #f8f8f2;
#                 border: none;
#                 border-radius: 6px;
#                 padding: 8px 16px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #ff7979;
#             }
#             QPushButton:pressed {
#                 background-color: #e64040;
#             }
#         """
#         )
#         self.stop_button.clicked.connect(self.on_stop_clicked)
#         button_layout.addWidget(self.stop_button)

#         button_layout.addStretch()
#         control_layout.addLayout(button_layout)

#         main_layout.addWidget(control_frame)

#         # Área para visualización del péndulo (placeholder)
#         visualization_label = QLabel(
#             "Visualización del Péndulo\n(Área para gráficos o simulación)"
#         )
#         visualization_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         visualization_label.setStyleSheet(
#             """
#             QLabel {
#                 background-color: #44475a;
#                 color: #f8f8f2;
#                 border-radius: 8px;
#                 padding: 40px;
#                 font-size: 16px;
#             }
#         """
#         )
#         visualization_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         main_layout.addWidget(visualization_label)

#         self.setLayout(main_layout)

#     def on_control_changed(self, index):
#         control_type = self.control_combo.currentText()
#         print(f"Tipo de control seleccionado: {control_type}")

#     def on_port_changed(self, index):
#         port = self.port_combo.currentText()
#         print(f"Puerto COM seleccionado: {port}")

#     def on_run_clicked(self):
#         control_type = self.control_combo.currentText()
#         port = self.port_combo.currentText()
#         print(f"Ejecutando control {control_type} en puerto {port}")

#     def on_pause_clicked(self):
#         print("Pausando ejecución")

#     def on_stop_clicked(self):
#         print("Deteniendo ejecución")


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class PendulumPage(QWidget):
    """Página del péndulo: diseño con dos menús desplegables y botones Ejecutar/Parar.

    Diseño (horizontal superior):
        Tipo de control: [QComboBox]  ---  Puertos COM: [QComboBox]  ---  ▶️ ⏸️

    Las acciones solo imprimen mensajes en consola para prueba.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("page_pendulum_custom")
        self._build_ui()

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

        # Puertos COM
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

        main_layout.addLayout(top_row)

        # Espacio reservado para la visualización (placeholder)
        placeholder = QLabel(
            "\nAquí irá la visualización del péndulo (canvas / plots / live data)\n"
        )
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setObjectName("pendulum_placeholder")
        placeholder.setMinimumHeight(300)
        main_layout.addWidget(placeholder)

        # Estirar para ocupar espacio restante
        main_layout.addStretch(1)

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

        # Limpiar y poblar el combo
        self.combo_com.clear()
        self.combo_com.addItems(ports)

    # --------- Slots / callbacks (solo prints para prueba) ----------
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


# # Test: ejecutar esta página sola
# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     w = PendulumPage()
#     w.resize(700, 480)
#     w.show()
#     sys.exit(app.exec())

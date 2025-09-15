from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
    QSizePolicy,
)

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
import sys

# ---------------- Dracula palette ----------------
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

from layouts import PendulumPage, RandomPendulumData


class SidebarButton(QPushButton):
    def __init__(self, emoji: str, text: str, parent=None):
        super().__init__(parent)
        self.emoji = emoji
        self.label_text = text
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self.setExpanded(True)
        self.setFixedHeight(44)
        self.setFlat(True)

    def setExpanded(self, expanded: bool):
        if expanded:
            self.setText(f"{self.emoji}  {self.label_text}")
        else:
            self.setText(self.emoji)
        self.adjustSize()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inverted Pendulum Control System")
        self.resize(1000, 640)

        # Sidebar sizes
        self.sidebar_expanded_width = 220
        self.sidebar_collapsed_width = 50
        self.sidebar_is_expanded = True

        # Central widget and layout
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar frame
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(self.sidebar_expanded_width)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(8, 8, 8, 8)
        self.sidebar_layout.setSpacing(6)

        # Toggle button (top)
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedHeight(36)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.toggle_btn.setObjectName("toggle_btn")
        self.sidebar_layout.addWidget(self.toggle_btn)

        # Navigation buttons
        self.nav_buttons = []
        nav_info = [
            ("🏠", "Home"),
            ("🕰️", "Pendulum"),
            ("🤖", "Train"),
            ("📈", "Gráficas"),
        ]

        for emoji, label in nav_info:
            btn = SidebarButton(emoji, label)
            btn.clicked.connect(self.on_nav_clicked)
            btn.setObjectName("nav_button")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        self.sidebar_layout.addStretch(1)

        # Exit button (bottom)
        self.exit_button = SidebarButton("⏻", "Exit")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setObjectName("exit_button")
        self.sidebar_layout.addWidget(self.exit_button)

        # Content area (stacked pages)
        self.stack = QStackedWidget()
        self.stack.setObjectName("content_stack")

        # Pages
        self.page_home = self._make_page("Home", "Bienvenido — Péndulo Invertido")
        self.page_pendulum = PendulumPage()
        self.page_train = self._make_page("Train", "Entrenamiento / Simulación")
        self.page_graphs = self._make_page(
            "Gráficas", "Gráficas de respuesta / pérdida"
        )

        for p in (
            self.page_home,
            self.page_pendulum,
            self.page_train,
            self.page_graphs,
        ):
            self.stack.addWidget(p)

        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.stack, 1)

        self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)
        self.apply_stylesheet()

        # Simulation setup
        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self.update_simulation)
        self.simulator = RandomPendulumData()

        # Connect pendulum page signals
        self.page_pendulum.btn_run.clicked.connect(self.start_simulation)
        self.page_pendulum.btn_stop.clicked.connect(self.stop_simulation)

    def _make_page(self, title: str, subtitle: str) -> QWidget:
        w = QWidget()
        w.setObjectName(f"page_{title.lower()}")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        title_lbl = QLabel(title)
        title_lbl.setObjectName("page_title")
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setObjectName("page_subtitle")
        subtitle_lbl.setWordWrap(True)
        subtitle_lbl.setMaximumHeight(60)
        center_lbl = QLabel("Contenido de la página\n(agrega tus widgets aquí)")
        center_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_lbl.setObjectName("page_center")
        layout.addWidget(title_lbl)
        layout.addWidget(subtitle_lbl)
        layout.addStretch(1)
        layout.addWidget(center_lbl, 2)
        layout.addStretch(3)
        return w

    def on_nav_clicked(self):
        sender = self.sender()
        for i, btn in enumerate(self.nav_buttons):
            if btn is sender:
                btn.setChecked(True)
                self.stack.setCurrentIndex(i)
            else:
                btn.setChecked(False)

    def toggle_sidebar(self):
        start = self.sidebar.width()
        if self.sidebar_is_expanded:
            end = self.sidebar_collapsed_width
        else:
            end = self.sidebar_expanded_width

        # Animación para el ancho mínimo y máximo
        anim_min = QPropertyAnimation(self.sidebar, b"minimumWidth")
        anim_min.setDuration(180)
        anim_min.setStartValue(start)
        anim_min.setEndValue(end)
        anim_min.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim_max = QPropertyAnimation(self.sidebar, b"maximumWidth")
        anim_max.setDuration(180)
        anim_max.setStartValue(start)
        anim_max.setEndValue(end)
        anim_max.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Actualizar estado y textos de botones
        self.sidebar_is_expanded = not self.sidebar_is_expanded
        for btn in self.nav_buttons + [self.exit_button]:
            btn.setExpanded(self.sidebar_is_expanded)

        # Iniciar animaciones
        anim_min.start()
        anim_max.start()

        # Mantener referencias
        self._anim_min = anim_min
        self._anim_max = anim_max

    def apply_stylesheet(self):
        s = f"""
        QWidget{{
            background-color: {DRACULA['bg']};
            color: {DRACULA['fg']};
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            font-size: 13px;
        }}
        #sidebar{{
            background-color: {DRACULA['panel']};
            border-right: 1px solid {DRACULA['current_line']};
        }}
        QPushButton#toggle_btn{{
            background: transparent;
            color: {DRACULA['muted']};
            border: none;
            font-size: 16px;
            text-align: left;
            padding-left: 6px;
        }}
        QPushButton#toggle_btn:hover{{ color: {DRACULA['fg']}; }}

        QPushButton#nav_button, QPushButton#exit_button{{
            background: transparent;
            color: {DRACULA['fg']};
            border: none;
            text-align: left;
            padding-left: 6px;
            border-radius: 6px;
            margin-top: 6px;
        }}
        QPushButton#nav_button:checked{{
            background: {DRACULA['current_line']};
            color: {DRACULA['accent']};
        }}
        QPushButton#nav_button:hover{{
            background: {DRACULA['current_line']};
        }}

        QStackedWidget#content_stack{{
            background-color: transparent;
        }}
        QWidget#page_home, QWidget#page_pendulum, QWidget#page_train, QWidget#page_graphs {{
            background: transparent;
        }}
        QLabel#page_title{{
            font-size: 20px;
            font-weight: 600;
            color: {DRACULA['fg']};
        }}
        QLabel#page_subtitle{{
            color: {DRACULA['muted']};
            margin-bottom: 8px;
        }}
        QLabel#page_center{{
            color: {DRACULA['muted']};
            font-size: 15px;
        }}
        """
        self.setStyleSheet(s)

    def start_simulation(self):
        """Inicia la simulación del péndulo"""
        print("Iniciando simulación del péndulo")
        self.sim_timer.start(30)  # ~33 FPS

    def stop_simulation(self):
        """Detiene la simulación del péndulo"""
        print("Deteniendo simulación del péndulo")
        self.sim_timer.stop()

    def update_simulation(self):
        """Actualiza el estado del péndulo con nuevos datos de simulación"""
        cart_pos, cart_vel, theta, theta_dot = self.simulator.next(0.05)
        self.page_pendulum.update_pendulum_state(cart_pos, cart_vel, 0, theta_dot)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

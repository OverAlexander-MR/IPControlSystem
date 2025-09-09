import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QStackedLayout,
)


from PySide6.QtGui import QPalette, QColor


# Subclase para customizar mi app
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inverted Pendulum")
        self.setFixedSize(QSize(1300, 800))

        # layout = QHBoxLayout()
        layout = QHBoxLayout()
        layout_h = QHBoxLayout()

        # Pestañas
        self.stack = QStackedLayout()
        pagelayout = QVBoxLayout()

        # Check Variables
        self.checked_IA = False
        self.checked_lqr = False
        self.checked_lqrUp = False

        # Buttoms
        LQR = QPushButton("LQR!")
        LQR_UP = QPushButton("LQR With Swing Up")
        IA = QPushButton("IA Methods")

        # Ms
        authors = QLabel("Hola Mundo")
        font = authors.font()
        font.setPointSize(16)
        authors.setFont(font)
        authors.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        # Agregrar al Stack layout

        pagelayout.addLayout(layout_h)
        pagelayout.addChildLayout(self.stack)

        IA.setCheckable(True)
        IA.clicked.connect(self._IA_clicked)
        IA.setChecked(self.checked_IA)

        LQR.setCheckable(True)
        LQR.clicked.connect(self._lqr_clicked)
        LQR.setChecked(self.checked_lqr)

        LQR_UP.setCheckable(True)
        LQR_UP.clicked.connect(self._lqrUp_clicked)
        LQR_UP.setChecked(self.checked_lqrUp)

        # Second Layout
        layout.setContentsMargins(100, 0, 100, 0)
        layout.setSpacing(5)

        layout.addWidget(authors)
        layout.addWidget(LQR_UP)
        layout.addWidget(LQR)

        layout_h.addLayout(layout)
        layout_h.setContentsMargins(50, 0, 50, 12)
        layout_h.setSpacing(15)

        layout_h.addWidget(IA)

        widget = QWidget()
        widget.setLayout(pagelayout)

        self.setCentralWidget(widget)

    def _IA_clicked(self, checked):
        self.checked_IA = checked
        self.stack.setCurrentIndex(0)  # Pestaña
        print("LQR clicked", self.checked_lqr)

    def _lqr_clicked(self, checked):
        self.checked_lqr = checked
        print("LQR clicked", self.checked_lqr)

    def _lqrUp_clicked(self, checked):
        self.checked_lqrUp = checked
        print("LQR Swing Up clicked", self.checked_lqrUp)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

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
        layout_buttons = QHBoxLayout()

        # Pestañas
        self.stack = QStackedLayout()
        pagelayout = QVBoxLayout()

        pagelayout.addLayout(layout_buttons)
        pagelayout.addLayout(self.stack)

        # Buttoms
        self.LQR = QPushButton("LQR!")
        self.LQR_UP = QPushButton("LQR With Swing Up")
        self.IA = QPushButton("IA Methods")

        # Ms
        authors = QLabel("Hola Mundo")
        font = authors.font()
        font.setPointSize(16)
        authors.setFont(font)
        authors.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        # Agregrar al Stack layout
        # pagelayout.addChildLayout(self.stack)

        self.IA.setCheckable(True)
        self.IA.clicked.connect(self._IA_clicked)

        self.LQR.setCheckable(True)
        self.LQR.clicked.connect(self._lqr_clicked)

        self.LQR_UP.setCheckable(True)
        self.LQR_UP.clicked.connect(self._lqrUp_clicked)

        
        layout_buttons.addWidget(self.IA)
        self.stack.addWidget(self.message("IA Layout"))
        
        layout_buttons.addWidget(self.LQR)
        self.stack.addWidget(self.message("LQR Layout"))

        layout_buttons.addWidget(self.LQR_UP)
        self.stack.addWidget(self.message("LQR Swin Layout"))


        # Dimensions layout
        layout_buttons.setContentsMargins(50, 0, 50, 12)
        layout_buttons.setSpacing(15)

        widget = QWidget()
        widget.setLayout(pagelayout)

        self.setCentralWidget(widget)

    @staticmethod
    def message(mss):
        welcome = QLabel(mss)
        font = welcome.font()
        font.setPointSize(16)
        welcome.setFont(font)
        welcome.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        return welcome

    def _IA_clicked(self):
        # Disable buttons
        self.LQR.setCheckable(False)
        self.LQR_UP.setCheckable(False)

        self.stack.setCurrentIndex(0)
        print("IA clicked")

        # Enable buttons
        self.LQR.setCheckable(True)
        self.LQR_UP.setCheckable(True)

    def _lqr_clicked(self):
        # Disable buttons
        self.IA.setCheckable(False)
        self.LQR_UP.setCheckable(False)

        print("LQR clicked")
        self.stack.setCurrentIndex(1)

        # Repouse buttons
        self.IA.setCheckable(True)
        self.LQR_UP.setCheckable(True)

    def _lqrUp_clicked(self):
        # Disable buttons
        self.IA.setCheckable(False)
        self.LQR.setCheckable(False)

        print("LQR Swing Up clicked")
        self.stack.setCurrentIndex(2)

        # Enable buttons
        self.IA.setCheckable(True)
        self.LQR.setCheckable(True)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

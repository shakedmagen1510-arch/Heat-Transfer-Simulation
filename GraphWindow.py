from PySide6.QtWidgets import QWidget, QComboBox, QPushButton, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Graph Window - Temperature vs Time")
        self.setFixedSize(680, 440)
        self.setStyleSheet("background-color: whitesmoke; font-size: 14px;")

        # הגדרת משטח הגרף של Matplotlib
        self.figure = Figure(figsize=(4.5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.figure.tight_layout()

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 20, 450, 400)

        # תווית ותיבת בחירה לגוף המבוקש
        self.select_lbl = QLabel("Select Body:", self)
        self.select_lbl.setGeometry(495, 30, 160, 25)
        self.select_lbl.setStyleSheet("font-weight: bold; color: black;")

        self.body_combo = QComboBox(self)
        self.body_combo.setGeometry(495, 60, 160, 38)
        self.body_combo.addItems(["Body 1", "Body 2"])
        self.body_combo.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 5px; padding: 4px;")

        # כפתורי פעולה (יחוברו בשלב 4)
        self.draw_btn = QPushButton("Draw", self)
        self.draw_btn.setGeometry(495, 115, 160, 42)
        self.draw_btn.setStyleSheet("background-color: royalblue; color: white; font-weight: bold; border-radius: 6px;")

        self.clear_btn = QPushButton("Clear", self)
        self.clear_btn.setGeometry(495, 172, 160, 42)
        self.clear_btn.setStyleSheet("background-color: slategray; color: white; font-weight: bold; border-radius: 6px;")

        self.export_btn = QPushButton("Export to CSV", self)
        self.export_btn.setGeometry(495, 229, 160, 42)
        self.export_btn.setStyleSheet("background-color: seagreen; color: white; font-weight: bold; border-radius: 6px;")
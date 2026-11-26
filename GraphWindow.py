import os
import csv
from pathlib import Path
from PySide6.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QMessageBox
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
        self.format_axes()

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 20, 450, 400)

        # תווית ותיבת בחירה לגוף המבוקש
        self.select_lbl = QLabel("Select Body:", self)
        self.select_lbl.setGeometry(495, 30, 160, 25)
        self.select_lbl.setStyleSheet("font-weight: bold; color: black;")

        self.body_combo = QComboBox(self)
        self.body_combo.setGeometry(495, 60, 160, 38)
        self.body_combo.addItems(["Both", "Body 1", "Body 2"])
        self.body_combo.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 5px; padding: 4px;")

        # כפתורי פעולה מחוברים למתודות
        self.draw_btn = QPushButton("Draw", self)
        self.draw_btn.setGeometry(495, 115, 160, 42)
        self.draw_btn.setStyleSheet("background-color: royalblue; color: white; font-weight: bold; border-radius: 6px;")
        self.draw_btn.clicked.connect(self.draw_graph)

        self.clear_btn = QPushButton("Clear", self)
        self.clear_btn.setGeometry(495, 172, 160, 42)
        self.clear_btn.setStyleSheet("background-color: slategray; color: white; font-weight: bold; border-radius: 6px;")
        self.clear_btn.clicked.connect(self.clear_graph)

        self.export_btn = QPushButton("Export to CSV", self)
        self.export_btn.setGeometry(495, 229, 160, 42)
        self.export_btn.setStyleSheet("background-color: seagreen; color: white; font-weight: bold; border-radius: 6px;")
        self.export_btn.clicked.connect(self.export_csv)

    def format_axes(self):
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.figure.tight_layout()

    def draw_graph(self):
        times = self.main_window.time_history
        if not times:
            QMessageBox.warning(self, "No Data", "Run the simulation first before drawing a graph.")
            return

        selected = self.body_combo.currentText()
        if selected == "Both":
            self.ax.plot(times, self.main_window.body1_temp_history, color="crimson", linewidth=2, label="Body 1")
            self.ax.plot(times, self.main_window.body2_temp_history, color="mediumblue", linewidth=2, label="Body 2")
        elif selected == "Body 1":
            self.ax.plot(times, self.main_window.body1_temp_history, color="crimson", linewidth=2, label="Body 1")
        else:
            self.ax.plot(times, self.main_window.body2_temp_history, color="mediumblue", linewidth=2, label="Body 2")

        self.ax.legend()
        self.format_axes()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.format_axes()
        self.canvas.draw()

    def export_csv(self):
        times = self.main_window.time_history
        t1_list = self.main_window.body1_temp_history
        t2_list = self.main_window.body2_temp_history

        if not times:
            QMessageBox.warning(self, "No Data", "Run the simulation first before exporting to CSV.")
            return

        csv_path = Path(__file__).resolve().parent / "heat_transfer_results.csv"
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Time (s)", "Body 1 Temp (°C)", "Body 2 Temp (°C)"])
            for t, temp1, temp2 in zip(times, t1_list, t2_list):
                writer.writerow([t, round(temp1, 3), round(temp2, 3)])

        os.startfile(csv_path)
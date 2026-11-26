from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider,
    QDoubleSpinBox, QPushButton
)
from PySide6.QtCore import Qt, QTimer
from Body import Body
from About import AboutWindow
from GraphWindow import GraphWindow


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.about_win = AboutWindow()
        self.graph_win = GraphWindow(self)

        # משתני סימולציה והיסטוריית נתונים
        self.body1 = None
        self.body2 = None
        self.dt = 0.1
        self.current_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        # הגדרת הטיימר
        self.timer = QTimer(self)
        self.timer.setInterval(int(self.dt * 1000))
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.setFixedSize(640, 460)
        self.setStyleSheet("background-color: whitesmoke; font-size: 14px; color: black;")

        # --- גשר המוליכות במרכז ---
        self.bridge_box = QLabel(self)
        self.bridge_box.setGeometry(235, 115, 170, 35)
        self.bridge_box.setStyleSheet("background-color: darkgray; border-radius: 4px;")

        self.cond_lbl = QLabel("Conductivity", self)
        self.cond_lbl.setGeometry(255, 45, 130, 25)
        self.cond_lbl.setAlignment(Qt.AlignCenter)
        self.cond_lbl.setStyleSheet("font-weight: bold;")

        self.cond_spin = QDoubleSpinBox(self)
        self.cond_spin.setGeometry(250, 72, 140, 32)
        self.cond_spin.setRange(0.01, 500.0)
        self.cond_spin.setValue(1.00)
        self.cond_spin.setSuffix(" J/s°C")
        self.cond_spin.setAlignment(Qt.AlignCenter)
        self.cond_spin.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 4px;")

        # --- גוף שמאלי (Body 1) ---
        self.left_slider = QSlider(Qt.Vertical, self)
        self.left_slider.setGeometry(50, 50, 30, 170)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_box = QLabel(self)
        self.left_body_box.setGeometry(100, 50, 135, 170)
        self.left_body_box.setStyleSheet("background-color: rgb(255, 0, 0); border-radius: 8px; border: 2px solid darkslategray;")

        self.left_temp_title = QLabel("Temp.", self)
        self.left_temp_title.setGeometry(40, 245, 55, 30)

        self.left_temp_display = QLabel("200.0 °C", self)
        self.left_temp_display.setGeometry(100, 245, 135, 30)
        self.left_temp_display.setAlignment(Qt.AlignCenter)
        self.left_temp_display.setStyleSheet("background-color: gainsboro; border: 1px solid darkgray; border-radius: 4px; font-weight: bold;")

        self.left_mass_title = QLabel("Mass", self)
        self.left_mass_title.setGeometry(40, 290, 55, 30)

        self.left_mass_spin = QDoubleSpinBox(self)
        self.left_mass_spin.setGeometry(100, 290, 135, 30)
        self.left_mass_spin.setRange(0.1, 10000.0)
        self.left_mass_spin.setValue(10.00)
        self.left_mass_spin.setSuffix(" kg")
        self.left_mass_spin.setAlignment(Qt.AlignCenter)
        self.left_mass_spin.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 4px;")

        self.left_cap_title = QLabel("H. Cap.", self)
        self.left_cap_title.setGeometry(40, 335, 55, 30)

        self.left_cap_spin = QDoubleSpinBox(self)
        self.left_cap_spin.setGeometry(100, 335, 135, 30)
        self.left_cap_spin.setRange(0.01, 50.0)
        self.left_cap_spin.setValue(0.40)
        self.left_cap_spin.setSuffix(" J/kg°C")
        self.left_cap_spin.setAlignment(Qt.AlignCenter)
        self.left_cap_spin.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 4px;")

        # --- גוף ימני (Body 2) ---
        self.right_body_box = QLabel(self)
        self.right_body_box.setGeometry(405, 50, 135, 170)
        self.right_body_box.setStyleSheet("background-color: rgb(0, 0, 0); border-radius: 8px; border: 2px solid darkslategray;")

        self.right_slider = QSlider(Qt.Vertical, self)
        self.right_slider.setGeometry(560, 50, 30, 170)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        self.right_temp_display = QLabel("0.0 °C", self)
        self.right_temp_display.setGeometry(405, 245, 135, 30)
        self.right_temp_display.setAlignment(Qt.AlignCenter)
        self.right_temp_display.setStyleSheet("background-color: gainsboro; border: 1px solid darkgray; border-radius: 4px; font-weight: bold;")

        self.right_temp_title = QLabel("Temp.", self)
        self.right_temp_title.setGeometry(550, 245, 55, 30)

        self.right_mass_spin = QDoubleSpinBox(self)
        self.right_mass_spin.setGeometry(405, 290, 135, 30)
        self.right_mass_spin.setRange(0.1, 10000.0)
        self.right_mass_spin.setValue(10.00)
        self.right_mass_spin.setSuffix(" kg")
        self.right_mass_spin.setAlignment(Qt.AlignCenter)
        self.right_mass_spin.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 4px;")

        self.right_mass_title = QLabel("Mass", self)
        self.right_mass_title.setGeometry(550, 290, 55, 30)

        self.right_cap_spin = QDoubleSpinBox(self)
        self.right_cap_spin.setGeometry(405, 335, 135, 30)
        self.right_cap_spin.setRange(0.01, 50.0)
        self.right_cap_spin.setValue(0.40)
        self.right_cap_spin.setSuffix(" J/kg°C")
        self.right_cap_spin.setAlignment(Qt.AlignCenter)
        self.right_cap_spin.setStyleSheet("background-color: white; border: 1px solid silver; border-radius: 4px;")

        self.right_cap_title = QLabel("H. Cap.", self)
        self.right_cap_title.setGeometry(550, 335, 55, 30)

        # --- כפתורי הפעלה וניווט במרכז למטה ---
        self.start_btn = QPushButton("Start", self)
        self.start_btn.setGeometry(260, 245, 120, 42)
        self.start_btn.setCheckable(True)
        self.start_btn.setStyleSheet("font-size: 16px; font-weight: bold; color: forestgreen; background-color: white; border: 2px solid silver; border-radius: 6px;")
        self.start_btn.clicked.connect(self.start_stop_button_method)

        self.graphs_btn = QPushButton("Graphs", self)
        self.graphs_btn.setGeometry(260, 300, 120, 40)
        self.graphs_btn.setStyleSheet("font-size: 15px; background-color: white; border: 1px solid silver; border-radius: 6px;")
        self.graphs_btn.clicked.connect(self.open_graphs)

        self.about_btn = QPushButton("About", self)
        self.about_btn.setGeometry(260, 352, 120, 40)
        self.about_btn.setStyleSheet("font-size: 15px; background-color: gainsboro; border: 1px solid darkgray; border-radius: 6px;")
        self.about_btn.clicked.connect(self.open_about)

    def update_body_visual(self, temp, display_lbl, box_lbl):
        display_lbl.setText(f"{temp:.1f} °C")
        red_val = int((temp / 200.0) * 255)
        red_val = max(0, min(255, red_val))
        box_lbl.setStyleSheet(
            f"background-color: rgb({red_val}, 0, 0); border-radius: 8px; border: 2px solid darkslategray;"
        )

    def left_temperature_changed(self):
        temp = self.left_slider.value()
        self.update_body_visual(temp, self.left_temp_display, self.left_body_box)

    def right_temperature_changed(self):
        temp = self.right_slider.value()
        self.update_body_visual(temp, self.right_temp_display, self.right_body_box)

    def start_stop_button_method(self):
        if self.start_btn.isChecked():
            # יצירת אובייקטי הגופים לפי הערכים שעל המסך
            self.body1 = Body(
                self.left_mass_spin.value(),
                self.left_cap_spin.value(),
                float(self.left_slider.value())
            )
            self.body2 = Body(
                self.right_mass_spin.value(),
                self.right_cap_spin.value(),
                float(self.right_slider.value())
            )

            # אתחול זמן ורשימות היסטוריה לניסוי חדש
            self.current_time = 0.0
            self.time_history = [0.0]
            self.body1_temp_history = [self.body1.temperature]
            self.body2_temp_history = [self.body2.temperature]

            self.start_btn.setText("Stop")
            self.start_btn.setStyleSheet("font-size: 16px; font-weight: bold; color: crimson; background-color: white; border: 2px solid crimson; border-radius: 6px;")
            self.timer.start()
        else:
            self.timer.stop()
            self.start_btn.setText("Start")
            self.start_btn.setStyleSheet("font-size: 16px; font-weight: bold; color: forestgreen; background-color: white; border: 2px solid silver; border-radius: 6px;")

    def timer_method(self):
        sigma = self.cond_spin.value()
        t1 = self.body1.temperature
        t2 = self.body2.temperature

        # חישוב שטף החום וכמות החום העוברת בצעד הזמן dt
        i1 = sigma * (t2 - t1)
        i2 = sigma * (t1 - t2)
        dq1 = i1 * self.dt
        dq2 = i2 * self.dt

        # עדכון הטמפרטורה בכל גוף
        new_t1 = self.body1.add_heat(dq1)
        new_t2 = self.body2.add_heat(dq2)

        # שמירת הנתונים לרשימות עבור הגרף וה-CSV
        self.current_time = round(self.current_time + self.dt, 2)
        self.time_history.append(self.current_time)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        # עדכון התצוגה על המסך (מספרים, צבעים וסליידרים)
        self.left_slider.blockSignals(True)
        self.left_slider.setValue(round(new_t1))
        self.left_slider.blockSignals(False)
        self.update_body_visual(new_t1, self.left_temp_display, self.left_body_box)

        self.right_slider.blockSignals(True)
        self.right_slider.setValue(round(new_t2))
        self.right_slider.blockSignals(False)
        self.update_body_visual(new_t2, self.right_temp_display, self.right_body_box)

    def open_graphs(self):
        self.graph_win.show()

    def open_about(self):
        self.about_win.show()


if __name__ == "__main__":
    app = QApplication([])
    window = HeatTransfer()
    window.show()
    app.exec()
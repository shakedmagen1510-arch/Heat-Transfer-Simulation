from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

PIC_PATH = Path(__file__).resolve().parent / "AMXN3200.JPEG"


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About - Heat Transfer Simulation")
        self.setFixedSize(400, 440)
        self.setStyleSheet("background-color: whitesmoke;")

        # מסגרת והצגת תמונת פרופיל
        self.pic_label = QLabel(self)
        self.pic_label.setGeometry(125, 25, 150, 150)
        self.pic_label.setAlignment(Qt.AlignCenter)
        self.pic_label.setStyleSheet("border: 2px solid darkblue; border-radius: 10px; background-color: white;")

        if PIC_PATH.exists():
            pixmap = QPixmap(str(PIC_PATH))
            self.pic_label.setPixmap(pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.pic_label.setText("Image Not Found")

        # שם הסטודנט
        self.name_lbl = QLabel("Shaked Magen", self)
        self.name_lbl.setGeometry(50, 190, 300, 35)
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.name_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")

        # מחלקה ומכללה
        self.dept_lbl = QLabel("Mechanical Engineering | Afeka College", self)
        self.dept_lbl.setGeometry(30, 228, 340, 25)
        self.dept_lbl.setAlignment(Qt.AlignCenter)
        self.dept_lbl.setStyleSheet("font-size: 14px; color: dimgray;")

        # שם הקורס
        self.course_lbl = QLabel("Physics on Computer - Heat Conduction", self)
        self.course_lbl.setGeometry(30, 258, 340, 25)
        self.course_lbl.setAlignment(Qt.AlignCenter)
        self.course_lbl.setStyleSheet("font-size: 13px; color: gray;")

        # כתובת מייל
        self.mail_lbl = QLabel("shakedmagen1510@gmail.com", self)
        self.mail_lbl.setGeometry(50, 295, 300, 25)
        self.mail_lbl.setAlignment(Qt.AlignCenter)
        self.mail_lbl.setStyleSheet("font-size: 14px; color: black;")

        # קישור לחיץ למאגר ב-GitHub
        self.github_lbl = QLabel(
            '<a href="https://github.com/shakedmagen1510-arch/Heat-Transfer-Simulation" '
            'style="color: blue; text-decoration: none; font-weight: bold;">'
            'Project GitHub Repository</a>',
            self
        )
        self.github_lbl.setGeometry(40, 340, 320, 40)
        self.github_lbl.setAlignment(Qt.AlignCenter)
        self.github_lbl.setOpenExternalLinks(True)
        self.github_lbl.setStyleSheet(
            "font-size: 16px; background-color: lightblue; border-radius: 8px; border: 1px solid steelblue;"
        )
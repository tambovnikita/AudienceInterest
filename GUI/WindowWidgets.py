
from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt


# Кнопки
class NavigationBtn(QPushButton):
    def __init__(self, parent, name):
        QPushButton.__init__(self, parent)
        self.setObjectName(name)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QPushButton {background: white; border-radius: 15px;}
            QPushButton:hover {background:rgb(230, 230, 230); border-radius: 15px;}
            QPushButton:pressed {background:rgb(200, 200, 200); border-radius: 15px;}
        """)

        VLayout_lbl = QVBoxLayout()
        self.lbl_name = QLabel(self)
        self.lbl_name.setFont(QtGui.QFont('Helvetica', 18, weight=700))
        self.lbl_name.setFixedHeight(35)

        if name == "import":
            self.lbl_name.setText("Выбрать видео")
            self.setFixedWidth(240)
            self.lbl_name.setFixedWidth(140)

        elif name == "start_recognition":
            self.lbl_name.setText("Начать распознавание")
            self.setFixedWidth(270)
            self.lbl_name.setFixedWidth(220)

        elif name == "back":
            self.lbl_name.setText("Назад")
            self.setFixedWidth(120)
            self.lbl_name.setFixedWidth(70)

        elif name == "stop":
            self.lbl_name.setText("Остановить")
            self.setFixedWidth(160)
            self.lbl_name.setFixedWidth(110)

        elif name == "save_results":
            self.lbl_name.setText("Сохранить результаты")
            self.setFixedWidth(270)
            self.lbl_name.setFixedWidth(220)

        elif name == "save_video":
            self.lbl_name.setText("Сохранить видео")
            self.setFixedWidth(210)
            self.lbl_name.setFixedWidth(160)

        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setStyleSheet("background: 0; color: black;")
        VLayout_lbl.addWidget(self.lbl_name)

        VLayout_lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)  # выравнивание (центр)
        VLayout_lbl.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        self.setLayout(VLayout_lbl)

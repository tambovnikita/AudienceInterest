
from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt


# Подблок с результатами
class ResultBlock(QFrame):
    def __init__(self, parent, title, value):
        QFrame.__init__(self, parent)
        self.setFixedHeight(80)

        VLayout = QVBoxLayout()

        self.lbl_title = QLabel(self)
        self.lbl_title.setFont(QtGui.QFont('Helvetica', 16, weight=400))
        self.lbl_title.setFixedHeight(20)
        self.lbl_title.setText(title)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
        VLayout.addWidget(self.lbl_title)

        self.lbl_value = QLabel(self)
        self.lbl_value.setFont(QtGui.QFont('Helvetica', 14, weight=400))
        self.lbl_value.setFixedHeight(40)
        self.lbl_value.setText(value)
        self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_value.setStyleSheet("background: rgb(30, 30, 30); color: rgb(135, 135, 135); padding: 0 10px;")
        VLayout.addWidget(self.lbl_value)

        VLayout.setAlignment(Qt.AlignmentFlag.AlignTop)  # выравнивание
        VLayout.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        self.setLayout(VLayout)


# Сетка с результатами
class ResultGrid(QFrame):
    def __init__(self, parent, columns_title, rows_title, values):
        QFrame.__init__(self, parent)

        self.gridLayout = QGridLayout()

        for i in range(len(columns_title)):
            self.lbl_title = QLabel(self)
            self.lbl_title.setFont(QtGui.QFont('Helvetica', 16, weight=400))
            self.lbl_title.setFixedHeight(20)
            self.lbl_title.setText(columns_title[i])
            self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.lbl_title.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
            self.gridLayout.addWidget(self.lbl_title, 0, i+1)

        for i in range(len(rows_title)):
            self.lbl_title = QLabel(self)
            self.lbl_title.setFont(QtGui.QFont('Helvetica', 14, weight=400))
            self.lbl_title.setFixedHeight(20)
            self.lbl_title.setText(rows_title[i])
            self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.lbl_title.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
            self.gridLayout.addWidget(self.lbl_title, i+1, 0)

        for i in range(len(values)):
            for j in range(len(values[i])):
                self.lbl_value = QLabel(self)
                self.lbl_value.setFont(QtGui.QFont('Helvetica', 12, weight=400))
                self.lbl_value.setFixedHeight(30)
                self.lbl_value.setText(values[i][j])
                self.lbl_value.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.lbl_value.setStyleSheet("background: rgb(30, 30, 30); color: rgb(135, 135, 135); padding: 0 10px;")
                self.gridLayout.addWidget(self.lbl_value, i+1, j+1)

        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # выравнивание
        self.gridLayout.setContentsMargins(20, 0, 20, 0)  # внешние отступы
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setHorizontalSpacing(20)
        self.setLayout(self.gridLayout)


# Цветной блок
class ColorBlock(QFrame):
    def __init__(self, parent, title, color):
        QFrame.__init__(self, parent)
        self.setFixedHeight(30)

        HLayout = QHBoxLayout()

        self.color = QLabel(self)
        self.color.setFixedHeight(20)
        self.color.setFixedWidth(20)
        self.color.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.color.setStyleSheet(f"background: {color}; padding: 0 10px;")
        HLayout.addWidget(self.color)

        self.lbl_title = QLabel(self)
        self.lbl_title.setFont(QtGui.QFont('Helvetica', 14, weight=400))
        self.lbl_title.setFixedHeight(20)
        self.lbl_title.setText(title)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title.setStyleSheet(f"background: 0; color: {color}; padding: 0;")
        HLayout.addWidget(self.lbl_title)

        HLayout.setAlignment(Qt.AlignmentFlag.AlignTop)  # выравнивание
        HLayout.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        self.setLayout(HLayout)

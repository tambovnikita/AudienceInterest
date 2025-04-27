
import os
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt6.QtCore import Qt

from GUI.WindowWidgets import NavigationBtn
from GUI.ImportWindow import ImportWindow

basedir = (os.path.dirname(os.path.dirname(__file__)))  # путь к базовой папке
print(basedir)

class MainWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.import_window_create = False     # переменная, проверяющая создан ли объект ImportWindow

        # Расстановка элементов
        VLayout_main = QVBoxLayout()
        VLayout_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VLayout_main.setSpacing(50)     # расстояние между элементами
        VLayout_main.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.lbl_title = QLabel(self)  # заголовок
        self.lbl_title.setFont(QtGui.QFont('Helvetica', 72, weight=700))  # изменяем шрифт
        self.lbl_title.setFixedWidth(1400)
        self.lbl_title.setFixedHeight(300)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.lbl_title.setWordWrap(True)  # перенос текста
        self.lbl_title.setText("Заинтересованность слушателей")  # меняем текст
        self.lbl_title.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        VLayout_main.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel(self)  # заголовок
        self.lbl_subtitle.setFont(QtGui.QFont('Helvetica', 26, weight=400))  # изменяем шрифт
        self.lbl_subtitle.setFixedWidth(1400)
        self.lbl_subtitle.setFixedHeight(250)
        self.lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.lbl_subtitle.setText("Нажмите “Выбрать видео”, чтобы запись появилась в программе")  # меняем текст
        self.lbl_subtitle.setStyleSheet("color: black;")  # меняем цвет текста
        VLayout_main.addWidget(self.lbl_subtitle)

        HLayout_btns = QHBoxLayout()
        HLayout_btns.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Кнопка "Выбрать видео"
        self.btn_import = NavigationBtn(self, name="import")    # кнопка "Выбрать видео"
        self.btn_import.clicked.connect(self.btnImportClick)  # при клике на кнопку
        HLayout_btns.addWidget(self.btn_import)

        VLayout_main.addLayout(HLayout_btns)
        self.setLayout(VLayout_main)

    # При клике на кнопку "Выбрать видео"
    def btnImportClick(self):
        file_name_video, _ = QFileDialog.getOpenFileName(self, "Select Media", ".",
                                                         "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.mov)")

        if file_name_video != '':
            self.openImportWindow(file_name_video)

    # Следующий экран
    def openImportWindow(self, file_name_video):
        self.import_window = ImportWindow(self, file_name_video)
        self.import_window_create = True
        self.parent.setCentralWidget(self.import_window)     # меняем экран

    def __del__(self):
        if self.import_window_create == True:
            del self.import_window


class StartWindow(QMainWindow):
    def __init__(self):
        super(StartWindow, self).__init__()
        self.setGeometry(50, 50, 1920, 1080)
        self.setWindowTitle("Заинтересованность слушателей")   # название окна
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "other", "imgs", "icon.ico")))    # иконка окна
        self.setStyleSheet("background:rgb(80, 80, 80);")  # фон окна
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)     # устанавливаем главный виджет

    # Завершаем отдельный поток, если окно хотят закрыть
    def closeEvent(self, event):
        del self.main_widget
        os._exit(0)

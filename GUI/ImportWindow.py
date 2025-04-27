
import os
import time
import cv2
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLineEdit, QCheckBox, QFileDialog, QStackedWidget
from PyQt6.QtCore import Qt, QUrl

from GUI.WindowWidgets import NavigationBtn
from GUI.ImportWindowWidgets import VideoBlock, InfoBlock, CharacteristicBlock
from GUI.MainWindow import MainWindow


class MainWidget(QWidget):
    def __init__(self, parent=None, file_name_video=''):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.file_name_video = file_name_video
        self.main_window_create = False     # переменная, проверяющая создан ли объект MainWindow

        self.video_fps = None

        # Расстановка элементов
        HLayout_main = QHBoxLayout()
        HLayout_main.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        HLayout_main.setSpacing(20)  # расстояние между элементами
        HLayout_main.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        # Левая область

        VLayout_left = QVBoxLayout()
        VLayout_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VLayout_left.setSpacing(30)  # расстояние между элементами
        VLayout_left.setContentsMargins(20, 0, 0, 0)  # внешние отступы

        # Блок с видео
        self.video_block = VideoBlock(self)
        VLayout_left.addWidget(self.video_block)

        # Кнопка "Выбрать видео" и Отображаемые характеристики
        HLayout_btn_and_characteristics = QHBoxLayout()
        HLayout_btn_and_characteristics.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_btn_and_characteristics.setSpacing(130)  # расстояние между элементами
        HLayout_btn_and_characteristics.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.btn_import = NavigationBtn(self, name="import")  # кнопка "Выбрать видео"
        self.btn_import.clicked.connect(self.btnImportClick)  # при клике на кнопку
        HLayout_btn_and_characteristics.addWidget(self.btn_import)

        VLayout_characteristics = QVBoxLayout()
        VLayout_characteristics.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VLayout_characteristics.setSpacing(20)  # расстояние между элементами
        VLayout_characteristics.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.lbl_characteristics = QLabel(self)  # заголовок
        self.lbl_characteristics.setFont(QtGui.QFont('Helvetica', 26, weight=400))  # изменяем шрифт
        self.lbl_characteristics.setFixedWidth(500)
        self.lbl_characteristics.setFixedHeight(45)
        self.lbl_characteristics.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.lbl_characteristics.setText("ОТОБРАЖАЕМЫЕ ХАРАКТЕРИСТИКИ")  # меняем текст
        self.lbl_characteristics.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        VLayout_characteristics.addWidget(self.lbl_characteristics)

        gridlayout = QGridLayout()
        gridlayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        gridlayout.setHorizontalSpacing(80)
        gridlayout.setVerticalSpacing(10)

        self.characteristic_student = CharacteristicBlock(self, "student", "Силуэт слушателя")
        gridlayout.addWidget(self.characteristic_student, 0, 0)

        self.characteristic_eyes = CharacteristicBlock(self, "eyes", "Глаза слушателя")
        gridlayout.addWidget(self.characteristic_eyes, 0, 1)

        self.characteristic_face = CharacteristicBlock(self, "face", "Лицо слушателя")
        gridlayout.addWidget(self.characteristic_face, 1, 0)

        self.characteristic_cell_phone = CharacteristicBlock(self, "cell_phone", "Мобильный телефон")
        gridlayout.addWidget(self.characteristic_cell_phone, 1, 1)

        VLayout_characteristics.addLayout(gridlayout)
        HLayout_btn_and_characteristics.addLayout(VLayout_characteristics)

        VLayout_left.addLayout(HLayout_btn_and_characteristics)

        HLayout_main.addLayout(VLayout_left)

        # Правая область

        VLayout_right = QVBoxLayout()
        VLayout_right.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignTop)
        VLayout_right.setSpacing(20)  # расстояние между элементами
        VLayout_right.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.frame_info = QFrame(self)  # блок с информацией о видео
        self.frame_info.setFixedWidth(500)
        self.frame_info.setStyleSheet("background: black;")

        VLayout_frame_info = QVBoxLayout()
        VLayout_frame_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        VLayout_frame_info.setSpacing(0)  # расстояние между элементами
        VLayout_frame_info.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.lbl_frame_info_title = QLabel(self)  # заголовок
        self.lbl_frame_info_title.setFont(QtGui.QFont('Helvetica', 26, weight=400))  # изменяем шрифт
        self.lbl_frame_info_title.setFixedWidth(500)
        self.lbl_frame_info_title.setFixedHeight(90)
        self.lbl_frame_info_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.lbl_frame_info_title.setText("ИНФОРМАЦИЯ О ВИДЕО")  # меняем текст
        self.lbl_frame_info_title.setStyleSheet("color: rgb(200, 200, 200); padding-top: 30px;")  # меняем цвет текста
        VLayout_frame_info.addWidget(self.lbl_frame_info_title)

        self.name_frame_info = InfoBlock(self, "name", "Название", "...")  # информационный блок
        VLayout_frame_info.addWidget(self.name_frame_info)

        self.duration_frame_info = InfoBlock(self, "duration", "Продолжительность", "...")  # информационный блок
        VLayout_frame_info.addWidget(self.duration_frame_info)

        self.size_frame_info = InfoBlock(self, "size", "Размеры", "...")  # информационный блок
        VLayout_frame_info.addWidget(self.size_frame_info)

        self.fps_frame_info = InfoBlock(self, "fps", "FPS", "...")  # информационный блок
        VLayout_frame_info.addWidget(self.fps_frame_info)

        self.memory_frame_info = InfoBlock(self, "memory", "Занимает памяти", "...")  # информационный блок
        VLayout_frame_info.addWidget(self.memory_frame_info)

        self.frame_info.setLayout(VLayout_frame_info)

        VLayout_right.addWidget(self.frame_info)

        # Интервал выборки
        HLayout_interval = QHBoxLayout()
        HLayout_interval.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_interval.setSpacing(10)  # расстояние между элементами
        HLayout_interval.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.lbl_interval = QLabel(self)
        self.lbl_interval.setFont(QtGui.QFont('Helvetica', 20, weight=400))  # изменяем шрифт
        self.lbl_interval.setFixedWidth(190)
        self.lbl_interval.setFixedHeight(45)
        self.lbl_interval.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lbl_interval.setText("Интервал выборки:")  # меняем текст
        self.lbl_interval.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        HLayout_interval.addWidget(self.lbl_interval)

        self.lineedit_interval_sec = QLineEdit(self)
        self.lineedit_interval_sec.setFont(QtGui.QFont('Helvetica', 20, weight=400))  # изменяем шрифт
        self.lineedit_interval_sec.setFixedWidth(70)
        self.lineedit_interval_sec.setFixedHeight(28)
        self.lineedit_interval_sec.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lineedit_interval_sec.setText("30")  # меняем текст
        self.lineedit_interval_sec.setStyleSheet("background: rgb(200, 200, 200); color: rgb(80, 80, 80); border: 0; padding: 0 10px;")  # меняем цвет текста
        HLayout_interval.addWidget(self.lineedit_interval_sec)

        self.lbl_interval_sec = QLabel(self)
        self.lbl_interval_sec.setFont(QtGui.QFont('Helvetica', 20, weight=400))  # изменяем шрифт
        self.lbl_interval_sec.setFixedWidth(50)
        self.lbl_interval_sec.setFixedHeight(45)
        self.lbl_interval_sec.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lbl_interval_sec.setText("сек")  # меняем текст
        self.lbl_interval_sec.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        HLayout_interval.addWidget(self.lbl_interval_sec)

        VLayout_right.addLayout(HLayout_interval)

        # Сохранять отдельно кадры с мобильным телефоном
        HLayout_save_cell_phone = QHBoxLayout()
        HLayout_save_cell_phone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_save_cell_phone.setSpacing(30)  # расстояние между элементами
        HLayout_save_cell_phone.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        self.lbl_save_cell_phone = QLabel(self)
        self.lbl_save_cell_phone.setFont(QtGui.QFont('Helvetica', 20, weight=400))  # изменяем шрифт
        self.lbl_save_cell_phone.setWordWrap(True)  # перенос текста
        self.lbl_save_cell_phone.setFixedWidth(260)
        self.lbl_save_cell_phone.setFixedHeight(55)
        self.lbl_save_cell_phone.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lbl_save_cell_phone.setText("Сохранять отдельно кадры с мобильным телефоном")  # меняем текст
        self.lbl_save_cell_phone.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        HLayout_save_cell_phone.addWidget(self.lbl_save_cell_phone)

        self.checkbox_save_cell_phone = QCheckBox(self)
        self.checkbox_save_cell_phone.setStyleSheet("QCheckBox {background: rgb(200, 200, 200);}")
        self.checkbox_save_cell_phone.setChecked(True)
        HLayout_save_cell_phone.addWidget(self.checkbox_save_cell_phone)

        VLayout_right.addLayout(HLayout_save_cell_phone)

        HLayout_btn_start_recognition = QHBoxLayout()
        HLayout_btn_start_recognition.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_btn_start_recognition.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        self.btn_start_recognition = NavigationBtn(self, name="start_recognition")  # кнопка "Начать распознавание"
        self.btn_start_recognition.clicked.connect(self.btnStartRecognitionClick)  # при клике на кнопку
        HLayout_btn_start_recognition.addWidget(self.btn_start_recognition)
        VLayout_right.addLayout(HLayout_btn_start_recognition)

        HLayout_main.addLayout(VLayout_right)

        self.setLayout(HLayout_main)
        self.showVideo()

    # При клике на кнопку "Выбрать видео"
    def btnImportClick(self):
        self.file_name_video, _ = QFileDialog.getOpenFileName(self, "Select Media", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.mov)")
        self.showVideo()

    # Если имеется путь к видео, то показываем картинку
    def showVideo(self):
        if self.file_name_video != '':
            self.video_block.media_player.setSource(QUrl.fromLocalFile(self.file_name_video))
            self.video_block.btn_play_video.setEnabled(True)
            self.video_block.playVideo()    # запускаем воспроизведение, чтобы появился первый кадр
            time.sleep(0.5)
            self.video_block.playVideo()    # останавливаем воспроизведение

            # Название
            self.name_frame_info.lbl_value.setText(self.file_name_video[self.file_name_video.rindex("/")+1:])

            cap = cv2.VideoCapture(self.file_name_video)

            # Продолжительность
            self.video_fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = int(frame_count / self.video_fps)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = (duration % 3600) % 60
            self.duration_frame_info.lbl_value.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Размеры
            self.size_frame_info.lbl_value.setText(f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))} x {int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

            # FPS
            self.fps_frame_info.lbl_value.setText(str(self.video_fps))

            cap.release()

            # Занимает памяти
            video_memory = os.path.getsize(self.file_name_video)    # байты
            if video_memory > 1024 * 1024 * 1024:
                self.memory_frame_info.lbl_value.setText(f"{round(video_memory / (1024 * 1024 * 1024), 3)} Гб")
            elif video_memory > 1024 * 1024:
                self.memory_frame_info.lbl_value.setText(f"{round(video_memory / (1024 * 1024), 3)} Мб")
            else:
                self.memory_frame_info.lbl_value.setText(f"{round(video_memory / 1024, 3)} Кб")

    # При клике на кнопку "Начать распознавание"
    def btnStartRecognitionClick(self):
        self.main_window = MainWindow(
            self,
            file_name_video=self.file_name_video,
            need_fps=int(self.video_fps * int(self.lineedit_interval_sec.text())),
            parameters_recognition={
                "show_students": self.characteristic_student.checkbox.isChecked(),
                "show_face": self.characteristic_face.checkbox.isChecked(),
                "show_eyes": self.characteristic_eyes.checkbox.isChecked(),
                "show_cell_phone": self.characteristic_cell_phone.checkbox.isChecked(),
                "save_cell_phone": self.checkbox_save_cell_phone.isChecked(),
                "time_interval_sec": int(self.lineedit_interval_sec.text())
            }
        )
        self.main_window_create = True
        if self.parent.stacked_widget.count() == 2:   # если в наборе виджетов уже находятся два виджета, то
            self.parent.stacked_widget.removeWidget(self.parent.stacked_widget.widget(1))   # удаляем второй виджет

        self.parent.stacked_widget.addWidget(self.main_window)  # добавляем в набор новый виджет
        self.parent.stacked_widget.setCurrentIndex(1)   # показываем второй виджет, то есть MainWidget (MainWindow)

    def __del__(self):
        if self.main_window_create == True:
            del self.main_window


class ImportWindow(QMainWindow):
    def __init__(self, parent=None, file_name_video=''):
        super(ImportWindow, self).__init__()
        self.setGeometry(50, 50, 1920, 1080)
        self.setWindowTitle("Заинтересованность слушателей")   # название окна
        # self.setWindowIcon(QtGui.QIcon('GUI/other/imgs/icon.png'))    # иконка окна
        self.setStyleSheet("background:rgb(80, 80, 80);")  # фон окна

        self.stacked_widget = QStackedWidget(self)  # набор виджетов - MainWidget (ImportWindow) и MainWidget (MainWindow)

        self.main_widget = MainWidget(self, file_name_video)
        self.stacked_widget.addWidget(self.main_widget)
        self.setCentralWidget(self.stacked_widget)     # устанавливаем главный виджет
        self.stacked_widget.show()

    # Завершаем отдельный поток, если окно хотят закрыть
    def closeEvent(self, event):
        del self.main_widget


import cv2
import numpy
from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QHBoxLayout, \
    QVBoxLayout, QFrame, QFileDialog, QPushButton, QSlider
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from GUI.WindowWidgets import NavigationBtn
from GUI.MainWindowWidgets import ResultBlock, ResultGrid, ColorBlock

from methods.students_and_cell_phone_methods import start_recognition
from methods.video_methods import get_video


# Поток, отвечающий за процесс распознавания
class ThreadClass(QThread):
    add_frame_signal = pyqtSignal(numpy.ndarray)    # сигнал, возвращающий распознанный кадр
    update_progress_signal = pyqtSignal(int, int)   # сигнал, отвечающий за отображение прогресса распознавания
    add_results_signal = pyqtSignal(int, int, int, int)     # сигнал, возвращающий результы распознавания

    def __init__(self, input_video_path, need_fps, parameters_recognition):
        super().__init__()
        self.input_video_path = input_video_path
        self.need_fps = need_fps
        self.parameters_recognition = parameters_recognition
        self.is_active = True

    def run(self):
        print('Начинаем распознавание')
        start_recognition(
            input_video_path=self.input_video_path,
            need_fps=self.need_fps,
            GUI_signals={
                "add_frame_signal": self.add_frame_signal,
                "update_progress_signal": self.update_progress_signal,
                "add_results_signal": self.add_results_signal
            },
            parameters_recognition=self.parameters_recognition
        )
        self.stop()     # завершаем поток, если распознавание закончилось

    def stop(self):
        print('Останавливаем распознавание')
        self.is_active = False
        self.terminate()


class MainWidget(QWidget):
    def __init__(self, parent=None, file_name_video=None, need_fps=None, parameters_recognition=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.file_name_video = file_name_video
        self.need_fps = need_fps
        self.parameters_recognition = parameters_recognition

        # Расстановка элементов
        HLayout_main = QHBoxLayout()
        HLayout_main.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        HLayout_main.setSpacing(20)  # расстояние между элементами
        HLayout_main.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        # Левая область

        VLayout_left = QVBoxLayout()
        VLayout_left.setAlignment(Qt.AlignmentFlag.AlignTop)
        VLayout_left.setSpacing(30)  # расстояние между элементами
        VLayout_left.setContentsMargins(20, 40, 0, 0)  # внешние отступы

        # Блок с видео
        self.video_block = QLabel(self)
        self.video_block.setFixedWidth(950)
        self.video_block.setFixedHeight(550)
        self.video_block.setText("Загрузка...")
        self.video_block.setFont(QtGui.QFont('Helvetica', 26, weight=400))  # изменяем шрифт
        self.video_block.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_block.setStyleSheet("color: rgb(200, 200, 200); background: black;")  # меняем цвет текста
        VLayout_left.addWidget(self.video_block)

        # Навигация по видео
        HLayout_video_navigation = QHBoxLayout()
        HLayout_video_navigation.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_video_navigation.setSpacing(20)  # расстояние между элементами
        HLayout_video_navigation.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        # Кнопка "Предыдущий кадр"
        self.btn_back_frame = QPushButton(self)
        self.btn_back_frame.setStyleSheet("""
                            QPushButton {background: rgb(200, 200, 200); color: rgb(80, 80, 80); border-radius: 15px;}
                            QPushButton:hover {background:rgb(160, 160, 160); color: rgb(80, 80, 80); border-radius: 15px;}
                            QPushButton:pressed {background:rgb(120, 120, 120); color: rgb(80, 80, 80); border-radius: 15px;}
                        """)
        self.btn_back_frame.setFixedHeight(28)
        self.btn_back_frame.setFixedWidth(28)
        self.btn_back_frame.setText("◀")
        self.btn_back_frame.clicked.connect(self.btnBackFrameClick)  # при клике на кнопку
        HLayout_video_navigation.addWidget(self.btn_back_frame)

        # Ползунок отображения кадров
        self.slider_position_video = QSlider(Qt.Orientation.Horizontal)
        self.slider_position_video.setRange(0, 0)
        self.slider_position_video.sliderMoved.connect(self.setPositionVideo)
        HLayout_video_navigation.addWidget(self.slider_position_video)

        # Кнопка "Следующий кадр"
        self.btn_next_frame = QPushButton(self)
        self.btn_next_frame.setStyleSheet("""
                                    QPushButton {background: rgb(200, 200, 200); color: rgb(80, 80, 80); border-radius: 15px;}
                                    QPushButton:hover {background:rgb(160, 160, 160); color: rgb(80, 80, 80); border-radius: 15px;}
                                    QPushButton:pressed {background:rgb(120, 120, 120); color: rgb(80, 80, 80); border-radius: 15px;}
                                """)
        self.btn_next_frame.setFixedHeight(28)
        self.btn_next_frame.setFixedWidth(28)
        self.btn_next_frame.setText("▶")
        self.btn_next_frame.clicked.connect(self.btnNextFrameClick)  # при клике на кнопку
        HLayout_video_navigation.addWidget(self.btn_next_frame)

        VLayout_left.addLayout(HLayout_video_navigation)

        # Время текущего кадра
        HLayout_time_current_frame = QHBoxLayout()
        HLayout_time_current_frame.setAlignment(Qt.AlignmentFlag.AlignLeft)
        HLayout_time_current_frame.setSpacing(350)  # расстояние между элементами
        HLayout_time_current_frame.setContentsMargins(20, 0, 0, 20)  # внешние отступы
        self.lbl_time = QLabel(self)  # заголовок
        self.lbl_time.setFont(QtGui.QFont('Helvetica', 18, weight=400))  # изменяем шрифт
        self.lbl_time.setFixedWidth(100)
        self.lbl_time.setFixedHeight(22)
        self.lbl_time.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_time.setText("...")  # меняем текст
        self.lbl_time.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        HLayout_time_current_frame.addWidget(self.lbl_time)
        self.lbl_progress = QLabel(self)  # заголовок
        self.lbl_progress.setFont(QtGui.QFont('Helvetica', 18, weight=400))  # изменяем шрифт
        self.lbl_progress.setFixedWidth(500)
        self.lbl_progress.setFixedHeight(22)
        self.lbl_progress.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lbl_progress.setText("Загрузка...")  # меняем текст
        self.lbl_progress.setStyleSheet("color: rgb(200, 200, 200);")  # меняем цвет текста
        HLayout_time_current_frame.addWidget(self.lbl_progress)
        VLayout_left.addLayout(HLayout_time_current_frame)

        # Кнопки
        HLayout_btns_all = QHBoxLayout()
        HLayout_btns_all.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_btns_all.setSpacing(140)  # расстояние между элементами
        HLayout_btns_all.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        HLayout_btns_left = QHBoxLayout()
        HLayout_btns_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_btns_left.setSpacing(20)  # расстояние между элементами
        HLayout_btns_left.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        self.btn_back = NavigationBtn(self, name="back")  # кнопка "Назад"
        self.btn_back.clicked.connect(self.btnBackClick)  # при клике на кнопку
        HLayout_btns_left.addWidget(self.btn_back)
        self.btn_stop = NavigationBtn(self, name="stop")  # кнопка "Остановить"
        self.btn_stop.clicked.connect(self.btnStopClick)  # при клике на кнопку
        HLayout_btns_left.addWidget(self.btn_stop)
        HLayout_btns_all.addLayout(HLayout_btns_left)

        HLayout_btns_right = QHBoxLayout()
        HLayout_btns_right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        HLayout_btns_right.setSpacing(20)  # расстояние между элементами
        HLayout_btns_right.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        self.btn_save_results = NavigationBtn(self, name="save_results")  # кнопка "Сохранить результаты"
        self.btn_save_results.clicked.connect(self.btnSaveResultsClick)  # при клике на кнопку
        HLayout_btns_right.addWidget(self.btn_save_results)
        self.btn_save_video = NavigationBtn(self, name="save_video")  # кнопка "Сохранить видео"
        self.btn_save_video.clicked.connect(self.btnSaveVideoClick)  # при клике на кнопку
        HLayout_btns_right.addWidget(self.btn_save_video)
        HLayout_btns_all.addLayout(HLayout_btns_right)

        VLayout_left.addLayout(HLayout_btns_all)

        HLayout_main.addLayout(VLayout_left)

        # Правая область

        self.frame_results = QFrame(self)  # блок с результатами
        self.frame_results.setFixedWidth(500)
        self.frame_results.setStyleSheet("background: black;")

        VLayout_frame_results = QVBoxLayout()
        VLayout_frame_results.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        VLayout_frame_results.setSpacing(0)  # расстояние между элементами
        VLayout_frame_results.setContentsMargins(0, 0, 0, 0)  # внешние отступы

        # Результаты текущего кадра
        self.lbl_frame_results_title = QLabel(self)  # заголовок
        self.lbl_frame_results_title.setFont(QtGui.QFont('Helvetica', 26, weight=400))  # изменяем шрифт
        self.lbl_frame_results_title.setFixedWidth(500)
        self.lbl_frame_results_title.setFixedHeight(80)
        self.lbl_frame_results_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.lbl_frame_results_title.setText("РЕЗУЛЬТАТЫ ТЕКУЩЕГО КАДРА")  # меняем текст
        self.lbl_frame_results_title.setStyleSheet("color: rgb(200, 200, 200); padding-top: 30px;")  # меняем цвет текста
        VLayout_frame_results.addWidget(self.lbl_frame_results_title)

        # Кол-во обнаруженных студентов в текущем кадре
        HLayout_count_students_current_frame = QHBoxLayout()
        HLayout_count_students_current_frame.setSpacing(20)
        HLayout_count_students_current_frame.setContentsMargins(20, 0, 20, 20)
        self.lbl_title_count_students_current_frame = QLabel(self)
        self.lbl_title_count_students_current_frame.setFont(QtGui.QFont('Helvetica', 16, weight=400))
        self.lbl_title_count_students_current_frame.setWordWrap(True)
        self.lbl_title_count_students_current_frame.setFixedHeight(40)
        self.lbl_title_count_students_current_frame.setText("Кол-во обнаруженных слушателей")
        self.lbl_title_count_students_current_frame.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title_count_students_current_frame.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
        HLayout_count_students_current_frame.addWidget(self.lbl_title_count_students_current_frame)
        self.lbl_value_count_students_current_frame = QLabel(self)
        self.lbl_value_count_students_current_frame.setFont(QtGui.QFont('Helvetica', 14, weight=400))
        self.lbl_value_count_students_current_frame.setFixedHeight(40)
        self.lbl_value_count_students_current_frame.setText("...")
        self.lbl_value_count_students_current_frame.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_value_count_students_current_frame.setStyleSheet("background: rgb(30, 30, 30); color: rgb(135, 135, 135); padding: 0 10px;")
        HLayout_count_students_current_frame.addWidget(self.lbl_value_count_students_current_frame)
        VLayout_frame_results.addLayout(HLayout_count_students_current_frame)

        # Кол-во обнаруженных мобильных телефонов в текущем кадре
        HLayout_count_cell_phone_current_frame = QHBoxLayout()
        HLayout_count_cell_phone_current_frame.setSpacing(20)
        HLayout_count_cell_phone_current_frame.setContentsMargins(20, 0, 20, 30)
        self.lbl_title_count_cell_phone_current_frame = QLabel(self)
        self.lbl_title_count_cell_phone_current_frame.setFont(QtGui.QFont('Helvetica', 16, weight=400))
        self.lbl_title_count_cell_phone_current_frame.setWordWrap(True)
        self.lbl_title_count_cell_phone_current_frame.setFixedHeight(40)
        self.lbl_title_count_cell_phone_current_frame.setText("Кол-во обнаруженных мобильных телефонов")
        self.lbl_title_count_cell_phone_current_frame.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title_count_cell_phone_current_frame.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
        HLayout_count_cell_phone_current_frame.addWidget(self.lbl_title_count_cell_phone_current_frame)
        self.lbl_value_count_cell_phone_current_frame = QLabel(self)
        self.lbl_value_count_cell_phone_current_frame.setFont(QtGui.QFont('Helvetica', 14, weight=400))
        self.lbl_value_count_cell_phone_current_frame.setFixedHeight(40)
        self.lbl_value_count_cell_phone_current_frame.setText("...")
        self.lbl_value_count_cell_phone_current_frame.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_value_count_cell_phone_current_frame.setStyleSheet("background: rgb(30, 30, 30); color: rgb(135, 135, 135); padding: 0 10px;")
        HLayout_count_cell_phone_current_frame.addWidget(self.lbl_value_count_cell_phone_current_frame)
        VLayout_frame_results.addLayout(HLayout_count_cell_phone_current_frame)

        # Статус студентов на текущем кадре
        HLayout_status_students_current_frame = QHBoxLayout()
        HLayout_status_students_current_frame.setSpacing(30)
        HLayout_status_students_current_frame.setContentsMargins(20, 0, 20, 0)
        self.involve_current_frame = ResultBlock(self, "ВОВЛЕЧЕНЫ", "...")
        HLayout_status_students_current_frame.addWidget(self.involve_current_frame)
        self.distracte_current_frame = ResultBlock(self, "ОТВЛЕКАЮТСЯ", "...")
        HLayout_status_students_current_frame.addWidget(self.distracte_current_frame)
        self.ignore_current_frame = ResultBlock(self, "ИГНОРИРУЮТ", "...")
        HLayout_status_students_current_frame.addWidget(self.ignore_current_frame)
        VLayout_frame_results.addLayout(HLayout_status_students_current_frame)

        # Общие результаты
        self.lbl_frame_results_title = QLabel(self)  # заголовок
        self.lbl_frame_results_title.setFont(QtGui.QFont('Helvetica', 26, weight=400))  # изменяем шрифт
        self.lbl_frame_results_title.setFixedWidth(500)
        self.lbl_frame_results_title.setFixedHeight(80)
        self.lbl_frame_results_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.lbl_frame_results_title.setText("ОБЩИЕ РЕЗУЛЬТАТЫ")  # меняем текст
        self.lbl_frame_results_title.setStyleSheet("color: rgb(200, 200, 200); padding-top: 30px;")  # меняем цвет текста
        VLayout_frame_results.addWidget(self.lbl_frame_results_title)

        # Общее кол-во обнаруженных студентов
        HLayout_count_students_all = QHBoxLayout()
        HLayout_count_students_all.setSpacing(20)
        HLayout_count_students_all.setContentsMargins(20, 0, 20, 0)
        self.lbl_title_count_students_all = QLabel(self)
        self.lbl_title_count_students_all.setFont(QtGui.QFont('Helvetica', 16, weight=400))
        self.lbl_title_count_students_all.setWordWrap(True)
        self.lbl_title_count_students_all.setFixedHeight(50)
        self.lbl_title_count_students_all.setText("Кол-во обнаруженных слушателей")
        self.lbl_title_count_students_all.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title_count_students_all.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
        HLayout_count_students_all.addWidget(self.lbl_title_count_students_all)
        self.count_students_min = ResultBlock(self, "МИНИМУМ", "...")
        HLayout_count_students_all.addWidget(self.count_students_min)
        self.count_students_medium = ResultBlock(self, "В СРЕДНЕМ", "...")
        HLayout_count_students_all.addWidget(self.count_students_medium)
        self.count_students_max = ResultBlock(self, "МАКСИМУМ", "...")
        HLayout_count_students_all.addWidget(self.count_students_max)
        VLayout_frame_results.addLayout(HLayout_count_students_all)

        # Общее кол-во обнаруженных мобильных телефонов
        HLayout_count_cell_phone_all = QHBoxLayout()
        HLayout_count_cell_phone_all.setSpacing(20)
        HLayout_count_cell_phone_all.setContentsMargins(20, 10, 20, 0)
        self.lbl_title_count_cell_phone_all = QLabel(self)
        self.lbl_title_count_cell_phone_all.setFont(QtGui.QFont('Helvetica', 16, weight=400))
        self.lbl_title_count_cell_phone_all.setWordWrap(True)
        self.lbl_title_count_cell_phone_all.setFixedHeight(70)
        self.lbl_title_count_cell_phone_all.setText("Кол-во обнаруженных мобильных телефонов")
        self.lbl_title_count_cell_phone_all.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title_count_cell_phone_all.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
        HLayout_count_cell_phone_all.addWidget(self.lbl_title_count_cell_phone_all)
        self.count_cell_phone_min = ResultBlock(self, "МИНИМУМ", "...")
        HLayout_count_cell_phone_all.addWidget(self.count_cell_phone_min)
        self.count_cell_phone_medium = ResultBlock(self, "В СРЕДНЕМ", "...")
        HLayout_count_cell_phone_all.addWidget(self.count_cell_phone_medium)
        self.count_cell_phone_max = ResultBlock(self, "МАКСИМУМ", "...")
        HLayout_count_cell_phone_all.addWidget(self.count_cell_phone_max)
        VLayout_frame_results.addLayout(HLayout_count_cell_phone_all)

        self.status_students_all = ResultGrid(
            self,
            columns_title=["МИНИМУМ", "В СРЕДНЕМ", "МАКСИМУМ"],
            rows_title=["ВОВЛЕЧЕНЫ", "ОТВЛЕКАЮТСЯ", "ИГНОРИРУЮТ"],
            values=[["...", "...", "..."], ["...", "...", "..."], ["...", "...", "..."]]
        )
        VLayout_frame_results.addWidget(self.status_students_all)

        gridLayoutColor = QGridLayout()
        gridLayoutColor.setContentsMargins(40, 30, 40, 0)
        gridLayoutColor.addWidget(ColorBlock(self, "ВОВЛЕЧЁН", "rgb(0, 255, 0)"), 0, 0)
        gridLayoutColor.addWidget(ColorBlock(self, "ЛИЦО СЛУШАТЕЛЯ", "rgb(255, 255, 255)"), 0, 1)
        gridLayoutColor.addWidget(ColorBlock(self, "ОТВЛЕКАЕТСЯ", "rgb(255, 255, 0)"), 1, 0)
        gridLayoutColor.addWidget(ColorBlock(self, "ГЛАЗА СЛУШАТЕЛЯ", "rgb(255, 0, 255)"), 1, 1)
        gridLayoutColor.addWidget(ColorBlock(self, "ИГНОРИРУЕТ", "rgb(255, 0, 0)"), 2, 0)
        gridLayoutColor.addWidget(ColorBlock(self, "МОБИЛЬНЫЙ ТЕЛЕФОН", "rgb(0, 0, 255)"), 2, 1)
        VLayout_frame_results.addLayout(gridLayoutColor)

        self.frame_results.setLayout(VLayout_frame_results)
        HLayout_main.addWidget(self.frame_results)

        self.setLayout(HLayout_main)

        self.all_frames = []    # список со всеми полученными кадрами
        self.all_frames_with_cell_phone = []  # список со всеми полученными кадрами, на которых обнаружен мобильный телефон
        self.all_times = []     # список со всеми временными метками

        # Общие результаты
        self.all_results_count_students = []
        self.all_results_count_cell_phone = []
        self.all_results_count_involve_students = []
        self.all_results_count_distracte_students = []
        self.all_results_count_ignore_students = []

        # Создаём отдельный поток
        self.thread = ThreadClass(self.file_name_video, self.need_fps, self.parameters_recognition)
        self.thread.start()  # запускаем поток
        self.thread.add_frame_signal.connect(self.add_frame)  # при срабатывании сигнала, получившийся frame будет передаваться в функцию add_frame
        self.thread.update_progress_signal.connect(self.update_progress)  # при срабатывании сигнала обновляется прогресс (информация о кол-ве обработанных кадров)
        self.thread.add_results_signal.connect(self.add_results)  # при срабатывании сигнала обновляются результаты распознавания

    # При клике на кнопку "Предыдущий кадр"
    def btnBackFrameClick(self):
        if self.slider_position_video.sliderPosition() - 1 >= 0:
            self.slider_position_video.setSliderPosition(self.slider_position_video.sliderPosition() - 1)
            self.show_frame(self.slider_position_video.sliderPosition())

    # Установка позиции видео
    def setPositionVideo(self, position):
        self.show_frame(position)

    # При клике на кнопку "Следующий кадр"
    def btnNextFrameClick(self):
        if self.slider_position_video.sliderPosition() + 1 <= self.slider_position_video.maximum():
            self.slider_position_video.setSliderPosition(self.slider_position_video.sliderPosition() + 1)
            self.show_frame(self.slider_position_video.sliderPosition())

    # При клике на кнопку "Назад"
    def btnBackClick(self):
        if self.thread.is_active:   # если поток всё ещё активен
            self.thread.stop()  # останавливаем поток
        self.parent.parent.parent.stacked_widget.setCurrentIndex(0)     # переключаемся на Import Window

    # При клике на кнопку "Остановить"
    def btnStopClick(self):
        self.thread.stop()  # останавливаем поток

    # При клике на кнопку "Сохранить результаты"
    def btnSaveResultsClick(self):
        output_file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовый файл (*.txt)")
        if len(output_file_path) > 0:
            text = f"""ОБЩИЕ РЕЗУЛЬТАТЫ

КОЛ-ВО ОБНАРУЖЕННЫХ СЛУШАТЕЛЕЙ
Минимум: {min(self.all_results_count_students)}
В среднем: {int(sum(self.all_results_count_students)/len(self.all_results_count_students))}
Максимум: {max(self.all_results_count_students)}

КОЛ-ВО ОБНАРУЖЕННЫХ МОБИЛЬНЫХ ТЕЛЕФОНОВ
Минимум: {min(self.all_results_count_cell_phone)}
В среднем: {int(sum(self.all_results_count_cell_phone)/len(self.all_results_count_cell_phone))}
Максимум: {max(self.all_results_count_cell_phone)}

ВОВЛЕЧЕНЫ
Минимум: {min(self.all_results_count_involve_students)}
В среднем: {int(sum(self.all_results_count_involve_students)/len(self.all_results_count_involve_students))}
Максимум: {max(self.all_results_count_involve_students)}

ОТВЛЕКАЮТСЯ
Минимум: {min(self.all_results_count_distracte_students)}
В среднем: {int(sum(self.all_results_count_distracte_students)/len(self.all_results_count_distracte_students))}
Максимум: {max(self.all_results_count_distracte_students)}

ИГНОРИРУЮТ
Минимум: {min(self.all_results_count_ignore_students)}
В среднем: {int(sum(self.all_results_count_ignore_students)/len(self.all_results_count_ignore_students))}
Максимум: {max(self.all_results_count_ignore_students)}


РЕЗУЛЬТАТЫ ДЛЯ КАЖДОГО КАДРА

"""
            for i in range(len(self.all_results_count_students)):
                hours = self.all_times[i] // 3600
                minutes = (self.all_times[i] % 3600) // 60
                seconds = (self.all_times[i] % 3600) % 60
                text += f"""{i+1}) {hours:02d}:{minutes:02d}:{seconds:02d}
Кол-во обнаруженных слушателей: {self.all_results_count_students[i]}
Кол-во обнаруженных мобильных телефонов: {self.all_results_count_cell_phone[i]}
Вовлечены: {self.all_results_count_involve_students[i]}
Отвлекаются: {self.all_results_count_distracte_students[i]}
Игнорируют: {self.all_results_count_ignore_students[i]}

"""

            with open(output_file_path, 'w') as file:
                file.write(text)

    # При клике на кнопку "Сохранить видео"
    def btnSaveVideoClick(self):
        # Сохраняем все кадры
        if len(self.all_frames) == 0:
            print("Кадры, полученные после распознавания, не были найдены")
        else:
            output_file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Видео (*.mp4)")
            if len(output_file_path) > 0:
                get_video(frames=self.all_frames, fps=1, name_video=output_file_path[output_file_path.rindex("/")+1:], path_video=output_file_path[:output_file_path.rindex("/")+1])

        if self.parameters_recognition["save_cell_phone"]:
            # Сохраняем только кадры с мобильным телефоном
            for i in range(len(self.all_frames)):
                if self.all_results_count_cell_phone[i] > 0:
                    self.all_frames_with_cell_phone.append(self.all_frames[i])
            if len(self.all_frames_with_cell_phone) == 0:
                print("Кадры с мобильным телефоном не были найдены")
            else:
                if len(output_file_path) > 0:
                    get_video(frames=self.all_frames_with_cell_phone, fps=1, name_video=output_file_path[output_file_path.rindex("/") + 1:-4]+"_cell_phone.mp4",
                      path_video=output_file_path[:output_file_path.rindex("/") + 1])

    # Функция, добавляющая новый кадр
    def add_frame(self, frame):
        self.all_frames.append(frame)   # добавляем полученный кадр в список

        # Увеличиваем максимальное значение ползунка
        self.slider_position_video.setMaximum(self.slider_position_video.maximum()+1)

        # Передвигаем ползунок в самый конец, если он до этого был в конце
        if self.slider_position_video.sliderPosition() == self.slider_position_video.maximum() - 1:
            self.slider_position_video.setSliderPosition(self.slider_position_video.maximum())
            self.show_frame(self.slider_position_video.sliderPosition())   # показываем новый кадр

    # Функция, отображающая кадр
    def show_frame(self, position):
        # Если ползунок в самом начале, то отображаем чёрный экран
        if position == 0:
            pixmap = QtGui.QPixmap(self.video_block.size())
            pixmap.fill(QtGui.QColor("black"))
            self.video_block.setPixmap(pixmap)
        # Все полученные кадры начинаются с позиции 1 и заканчиваются maximun
        else:
            # Преобразуем кадр из формата BGR в RGB
            frame_rgb = cv2.cvtColor(self.all_frames[position-1], cv2.COLOR_BGR2RGB)

            # Создаем изображение QImage из кадра
            img = QtGui.QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QtGui.QImage.Format.Format_RGB888)

            # Создаем QPixmap из QImage для отображения на QLabel
            pixmap = QtGui.QPixmap.fromImage(img)

            # Масштабируем QPixmap под размер QLabel и отображаем его
            self.video_block.setPixmap(pixmap.scaled(self.video_block.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        self.show_current_results(position)     # показываем результаты выбранного кадра
        self.show_current_time(position)   # показываем временную метку выбранного кадра

    # Функция, которая обновляет прогресс обработки кадров
    def update_progress(self, current_num, all_num):
        self.lbl_progress.setText(f"Обработано {int((current_num/all_num)*100)}% кадров ({current_num}/{all_num})")

    # Функция, которая добавляет результаты распознавания
    def add_results(self, count_involve_students, count_distracte_students, count_ignore_students, count_cell_phone):
        # Добавляем результаты в списки
        self.all_results_count_students.append(count_involve_students+count_distracte_students+count_ignore_students)
        self.all_results_count_cell_phone.append(count_cell_phone)
        self.all_results_count_involve_students.append(count_involve_students)
        self.all_results_count_distracte_students.append(count_distracte_students)
        self.all_results_count_ignore_students.append(count_ignore_students)

        self.update_all_results()   # обновляем общие результаты распознавания

        # Добавляем временную метку в список
        if len(self.all_times) == 0:
            self.all_times.append(0)
        else:
            self.all_times.append(self.all_times[-1]+self.parameters_recognition["time_interval_sec"])

    # Функция, показывающая результаты распознавания выбранного кадра
    def show_current_results(self, position):
        if position == 0:
            self.lbl_value_count_students_current_frame.setText("...")
            self.lbl_value_count_cell_phone_current_frame.setText("...")
            self.involve_current_frame.lbl_value.setText("...")
            self.distracte_current_frame.lbl_value.setText("...")
            self.ignore_current_frame.lbl_value.setText("...")
        else:
            self.lbl_value_count_students_current_frame.setText(str(self.all_results_count_students[position-1]))
            self.lbl_value_count_cell_phone_current_frame.setText(str(self.all_results_count_cell_phone[position-1]))
            self.involve_current_frame.lbl_value.setText(str(self.all_results_count_involve_students[position-1]))
            self.distracte_current_frame.lbl_value.setText(str(self.all_results_count_distracte_students[position-1]))
            self.ignore_current_frame.lbl_value.setText(str(self.all_results_count_ignore_students[position-1]))

    # Функция, обновляющая общие результаты распознавания
    def update_all_results(self):
        self.count_students_min.lbl_value.setText(str(min(self.all_results_count_students)))
        self.count_students_medium.lbl_value.setText(str(int(sum(self.all_results_count_students)/len(self.all_results_count_students))))
        self.count_students_max.lbl_value.setText(str(max(self.all_results_count_students)))

        self.count_cell_phone_min.lbl_value.setText(str(min(self.all_results_count_cell_phone)))
        self.count_cell_phone_medium.lbl_value.setText(str(int(sum(self.all_results_count_cell_phone)/len(self.all_results_count_cell_phone))))
        self.count_cell_phone_max.lbl_value.setText(str(max(self.all_results_count_cell_phone)))

        self.status_students_all.gridLayout.itemAtPosition(1, 1).widget().setText(str(min(self.all_results_count_involve_students)))
        self.status_students_all.gridLayout.itemAtPosition(1, 2).widget().setText(str(int(sum(self.all_results_count_involve_students)/len(self.all_results_count_involve_students))))
        self.status_students_all.gridLayout.itemAtPosition(1, 3).widget().setText(str(max(self.all_results_count_involve_students)))
        self.status_students_all.gridLayout.itemAtPosition(2, 1).widget().setText(str(min(self.all_results_count_distracte_students)))
        self.status_students_all.gridLayout.itemAtPosition(2, 2).widget().setText(str(int(sum(self.all_results_count_distracte_students)/len(self.all_results_count_distracte_students))))
        self.status_students_all.gridLayout.itemAtPosition(2, 3).widget().setText(str(max(self.all_results_count_distracte_students)))
        self.status_students_all.gridLayout.itemAtPosition(3, 1).widget().setText(str(min(self.all_results_count_ignore_students)))
        self.status_students_all.gridLayout.itemAtPosition(3, 2).widget().setText(str(int(sum(self.all_results_count_ignore_students)/len(self.all_results_count_ignore_students))))
        self.status_students_all.gridLayout.itemAtPosition(3, 3).widget().setText(str(max(self.all_results_count_ignore_students)))

    # Функция, показывающая время выбранного кадра
    def show_current_time(self, position):
        if position == 0:
            self.lbl_time.setText("...")
        else:
            hours = self.all_times[position-1] // 3600
            minutes = (self.all_times[position-1] % 3600) // 60
            seconds = (self.all_times[position-1] % 3600) % 60
            self.lbl_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def __del__(self):
        if self.thread.is_active:  # если поток всё ещё активен
            self.thread.stop()  # останавливаем поток
        del self.parent.parent.parent.stacked_widget


class MainWindow(QMainWindow):
    def __init__(self, parent=None, file_name_video=None, need_fps=None, parameters_recognition=None):
        super(MainWindow, self).__init__()
        self.parent = parent
        self.setGeometry(50, 50, 1920, 1080)
        self.setWindowTitle("Заинтересованность слушателей")   # название окна
        # self.setWindowIcon(QtGui.QIcon('GUI/other/imgs/icon.png'))  # иконка окна
        self.setStyleSheet("background:rgb(80, 80, 80);")  # фон окна
        self.main_widget = MainWidget(self, file_name_video, need_fps, parameters_recognition)
        self.setCentralWidget(self.main_widget)     # устанавливаем главный виджет

    # Завершаем отдельный поток, если окно хотят закрыть
    def closeEvent(self, event):
        del self.main_widget

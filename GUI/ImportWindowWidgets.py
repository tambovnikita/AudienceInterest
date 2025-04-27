
from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QFrame, QCheckBox, QPushButton, QStyle, QSlider
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget


# Информационные подблоки
class InfoBlock(QFrame):
    def __init__(self, parent, name, title, value):
        QFrame.__init__(self, parent)
        self.setObjectName(name)
        self.setFixedHeight(100)
        self.setStyleSheet("padding: 0 30px;")

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


# Подблок характеристики
class CharacteristicBlock(QFrame):
    def __init__(self, parent, name, title):
        QFrame.__init__(self, parent)
        self.setObjectName(name)
        self.setFixedHeight(30)

        HLayout = QHBoxLayout()

        self.lbl_title = QLabel(self)
        self.lbl_title.setFont(QtGui.QFont('Helvetica', 18, weight=400))
        self.lbl_title.setFixedHeight(20)
        self.lbl_title.setText(title)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.lbl_title.setStyleSheet("background: 0; color: rgb(200, 200, 200); padding: 0;")
        HLayout.addWidget(self.lbl_title)

        self.checkbox = QCheckBox(self)
        self.checkbox.setStyleSheet("QCheckBox {background: rgb(200, 200, 200);}")
        self.checkbox.setChecked(True)
        HLayout.addWidget(self.checkbox)

        HLayout.setAlignment(Qt.AlignmentFlag.AlignRight)  # выравнивание
        HLayout.setContentsMargins(0, 0, 0, 0)  # внешние отступы
        HLayout.setSpacing(20)
        self.setLayout(HLayout)


# Блок с видео
class VideoBlock(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)

        VLayout = QVBoxLayout()

        # Виджеты для работы с видео
        self.media_player = QMediaPlayer()
        self.video = QVideoWidget()
        self.video.setFixedWidth(950)
        self.video.setFixedHeight(550)
        VLayout.addWidget(self.video)

        HLayout_video_navigation = QHBoxLayout()
        HLayout_video_navigation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Стоп" и "Продолжить" для видео
        self.btn_play_video = QPushButton(self)
        self.btn_play_video.setStyleSheet("""
                    QPushButton {background: rgb(200, 200, 200); border-radius: 15px;}
                    QPushButton:hover {background:rgb(160, 160, 160); border-radius: 15px;}
                    QPushButton:pressed {background:rgb(120, 120, 120); border-radius: 15px;}
                """)
        self.btn_play_video.setEnabled(False)
        self.btn_play_video.setFixedHeight(28)
        self.btn_play_video.setFixedWidth(28)
        self.btn_play_video.setIconSize(QSize(18, 18))
        self.btn_play_video.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.btn_play_video.clicked.connect(self.playVideo)  # при клике на кнопку
        HLayout_video_navigation.addWidget(self.btn_play_video)

        # Управление временной позицией видео
        self.slider_position_video = QSlider(Qt.Orientation.Horizontal)
        self.slider_position_video.setRange(0, 0)
        self.slider_position_video.sliderMoved.connect(self.setPositionVideo)
        HLayout_video_navigation.addWidget(self.slider_position_video)

        VLayout.addLayout(HLayout_video_navigation)

        self.media_player.setVideoOutput(self.video)
        self.media_player.playbackStateChanged.connect(self.mediaStateChanged)
        self.media_player.positionChanged.connect(self.positionChanged)
        self.media_player.durationChanged.connect(self.durationChanged)
        self.media_player.errorChanged.connect(self.handleError)

        self.setLayout(VLayout)

    def playVideo(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def mediaStateChanged(self, state):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.btn_play_video.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.btn_play_video.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def positionChanged(self, position):
        self.slider_position_video.setValue(position)

    def durationChanged(self, duration):
        self.slider_position_video.setRange(0, duration)

    def setPositionVideo(self, position):
        self.media_player.setPosition(position)

    def handleError(self):
        self.btn_play_video.setEnabled(False)

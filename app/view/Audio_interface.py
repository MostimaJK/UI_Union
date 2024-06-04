# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths, QUrl
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QWheelEvent, QMouseEvent, QDesktopServices
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QVBoxLayout, QFileDialog, QActionGroup, QLabel,
                             QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QGraphicsView,
                             QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QVBoxLayout)
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType, CheckableMenu,
                            MenuIndicatorType, AvatarWidget, isDarkTheme, BodyLabel, CaptionLabel, HyperlinkButton,
                            ComboBox, PrimaryPushButton, InfoBarIcon, LineEdit, FlyoutView)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from qfluentwidgets import FluentIcon as FIF

from pydub import AudioSegment

from time import sleep

from .gallery_interface import GalleryInterface
from ..common.translator import Translator



class AudioInterface(GalleryInterface):
    """ Audio interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.audio,
            subtitle='音频裁剪，音频拼接，音频速率调整，音频倒放',
            parent=parent
        )
        self.audiopath = None
        self.audiopathB = None
        self.setObjectName('audioInterface')

        # 创建控件空间
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距
        
        # 创建子布局
        self.h_layout = QHBoxLayout(self.widget)# 创建h_layout水平布局
        self.h_layout_setting = QHBoxLayout(self.widget)  # 创建参数水平布局
        self.h_layout_audio = QHBoxLayout(self.widget)# 创建音频水平布局

###### 创建控件区域 ######

        # 创建导入音频A按钮
        self.button_input = PushButton(self.tr("导入音频A"))
        self.button_input.setFixedWidth(100)  # 设置按钮大小
        self.button_input.clicked.connect(self.inputAudio)  # 连接按钮的点击信号导入图片并显示

        # 创建导入音频B按钮
        self.button_input_B = PushButton(self.tr("导入音频B"))
        self.button_input_B.setFixedWidth(100)  # 设置按钮大小
        self.button_input_B.clicked.connect(self.inputAudio_B)  # 连接按钮的点击信号导入图片并显示

        # 创建选项下拉框
        self.comboBox_filter = ComboBox()  # 创建下拉框
        self.comboBox_filter.setPlaceholderText("请选择音频处理方法")
        items = ['音频裁剪','音频拼接', '音频速率调整', '音频倒放', '音频转成mp3', '音频转成wav']  # 下拉框的选项
        self.comboBox_filter.addItems(items)  # 添加下拉框的选项
        self.comboBox_filter.setCurrentIndex(-1)  # 设置下拉框的默认选项
        self.comboBox_filter.setFixedWidth(170)  # 设置下拉框的宽度
        # self.comboBox_filter.setMaximumWidth(180)  # 设置下拉框的最大宽度
        self.comboBox_filter.currentIndexChanged.connect(self.GetcomboBox_value)  # 当下拉框的选项改变时，触发事件

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_Audio_process)  # 连接按钮的点击信号导入图片并显示

        # 创建打开文件夹按钮
        self.button_input_save = PrimaryPushButton(self.tr("打开文件夹"))
        self.button_input_save.setFixedWidth(120)  # 设置按钮大小
        self.button_input_save.clicked.connect(self.open_folder)  # 连接按钮的点击信号导入图片并显示

        # 创建查看音频信息按钮A
        self.Audio_informationButton_A = PushButton(self.tr('音频信息A'))
        self.Audio_informationButton_A.clicked.connect(self.is_inputAudio_A)
        # self.Audio_informationButton_A.clicked.connect(self.showComplexFlyout_A)

        # 创建查看音频信息按钮B
        self.Audio_informationButton_B = PushButton(self.tr('音频信息B'))
        self.Audio_informationButton_B.clicked.connect(self.is_inputAudio_B)
        # self.Audio_informationButton_B.clicked.connect(self.showComplexFlyout_B)

        # # 创建一个音频播放器
        # self.videoplayer = QMediaPlayer()
        # # 创建一个音频窗口
        # self.videoWidget = QVideoWidget()
        # # 将音频播放器的输出设置为音频窗口
        # self.videoplayer.setVideoOutput(self.videoWidget)
        # self.videoplayer.setMedia(QMediaContent(QUrl.fromLocalFile('Photos/resource/video/Video.mp4')))
        # # 设置音频窗口的大小
        # self.videoWidget.resize(500, 500)

        # 创建音频开始时间输入框
        self.lineEdit_start = LineEdit()
        self.lineEdit_start.setPlaceholderText("Start Time ms")
        self.lineEdit_start.setFixedWidth(115)  # 设置输入框的宽度
        self.lineEdit_start.setEnabled(False)

        # 创建音频结束时间输入框
        self.lineEdit_end = LineEdit()
        self.lineEdit_end.setPlaceholderText("End Time ms")
        self.lineEdit_end.setFixedWidth(110)  # 设置输入框的宽度
        self.lineEdit_end.setEnabled(False)

        # 创建音频速率值输入框
        self.lineEdit_speed = LineEdit()
        self.lineEdit_speed.setPlaceholderText("Speed")
        self.lineEdit_speed.setFixedWidth(100)  # 设置输入框的宽度
        self.lineEdit_speed.setEnabled(False)

###### 控件区域布局 ######

        #子布局参数设置
        self.h_layout.setSpacing(100)  # 设置水平布局的间距
        self.h_layout_setting.setSpacing(100)  # 设置水平布局的间距
        self.h_layout_audio.setSpacing(100)  # 设置水平布局的间距
        self.h_layout.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式
        self.h_layout_setting.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式
        self.h_layout_audio.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式

        # 添加控件
        self.h_layout.addWidget(self.button_input, 0, Qt.AlignCenter)     # 添加导入音频按钮
        self.h_layout.addWidget(self.comboBox_filter, 0, Qt.AlignCenter)  # 将下拉框添加到水平布局中
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignCenter)  # 将Apply添加到水平布局中
        self.h_layout.addWidget(self.button_input_save, 0, Qt.AlignCenter)  # 将打开文件夹添加到水平布局中
        self.h_layout_setting.addWidget(self.button_input_B, 0, Qt.AlignCenter)  # 将导入音频B添加到水平布局中
        self.h_layout_setting.addWidget(self.lineEdit_start, 0, Qt.AlignCenter)  # 将参数设置框添加到水平布局中
        self.h_layout_setting.addWidget(self.lineEdit_end, 0, Qt.AlignCenter)  # 将参数设置框添加到水平布局中
        self.h_layout_setting.addWidget(self.lineEdit_speed, 0, Qt.AlignCenter)  # 将参数设置框添加到水平布局中
        self.h_layout_audio.addWidget(self.Audio_informationButton_A, 0, Qt.AlignCenter)  # 将音频信息按钮添加到水平布局中
        self.h_layout_audio.addWidget(self.Audio_informationButton_B, 0, Qt.AlignCenter)  # 将音频信息按钮添加到水平布局中

        # 布局嵌套
        self.vBoxLayout.addLayout(self.h_layout)    # 将水平布局添加到垂直布局中
        self.vBoxLayout.addLayout(self.h_layout_setting)    # 将水平布局添加到垂直布局中
        self.vBoxLayout.addLayout(self.h_layout_audio)    # 将水平布局添加到垂直布局中
        self.widget.layout().addLayout(self.h_layout)  # 将水平布局添加到垂直布局中

###### 函数区域 ######

   # Apply函数
    def Apply_Audio_process(self):
        # 获取下拉框的选项
        enum = self.GetcomboBox_value()
        # 判断inputPhoto的图片路径
        if self.audiopath == None:
            self.showFlyout("WARNING", "灾难性错误： 请先导入音频！")
            return
        # 加载音频文件
        audio = AudioSegment.from_file(self.audiopath)
        # 获取音频的文件名字
        filename = self.audiopath.split('/')[-1].split('.')[0]
        if enum == 1:
            # 音频裁剪
            start_time = self.get_value(self.lineEdit_start)
            end_time = self.get_value(self.lineEdit_end)
            clipped_audio = audio[start_time:end_time]
            clipped_audio.export('output/Audio_Processing/' + filename + '_clipped.mp3', format='mp3')
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "音频裁剪成功！")
        if enum == 2:
            # 音频拼接
            if self.audiopathB == None:
                self.showFlyout("WARNING", "灾难性错误： 请先导入音频B！")
                return
            audio2 = AudioSegment.from_file(self.audiopathB)
            combined_audio = audio + audio2
            combined_audio.export('output/Audio_Processing/' + filename + '_combined.mp3', format='mp3')
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "音频拼接成功！")
        if enum == 3:
            # 音频速率调整
            if self.lineEdit_speed == None:
                self.showFlyout("WARNING", "灾难性错误： 请先输入速率！")
                return
            speed = self.get_value(self.lineEdit_speed)
            speed_audio = audio.speedup(playback_speed=speed)
            speed_audio.export('output/Audio_Processing/' + filename + '_speed.mp3', format='mp3')
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "音频速率调整成功！")
        if enum == 4:
            # 音频倒放
            reversed_audio = audio.reverse()
            reversed_audio.export('output/Audio_Processing/' + filename + '_reversed.mp3', format='mp3')
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "音频倒放成功！")
        if enum == 5:
            # 音频转成mp3
            audio.export('output/Audio_Processing/' + filename + '_trs.mp3', format='mp3')
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "mp3音频转换成功！")
        if enum == 6:
            # 音频转成wav
            audio.export('output/Audio_Processing/' + filename + '_trs.wav', format='wav')
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "wav音频转换成功！")
        else:
            return


    # 当下拉框的选项改变时，触发事件
    def GetcomboBox_value(self):
        # 获取下拉框的选项
        comboBox_value = self.comboBox_filter.currentText()
        print(comboBox_value)
        res = -1
        if comboBox_value == '音频裁剪':
            self.lineEdit_start.setEnabled(True)
            self.lineEdit_end.setEnabled(True)
            res = 1
        elif comboBox_value == '音频拼接':
            res = 2
        elif comboBox_value == '音频速率调整':
            self.lineEdit_speed.setEnabled(True)
            res = 3
        elif comboBox_value == '音频倒放':
            res = 4
        elif comboBox_value == '音频转成mp3':
            res = 5
        elif comboBox_value == '音频转成wav':
            res = 6
        else:
            res = -1
        return res


    # 导入音频的方法
    def inputAudio(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath, _ = QFileDialog.getOpenFileName()
        self.audio_info_A = None
        if filepath:
            self.audiopath = filepath
            audio = AudioSegment.from_file(self.audiopath)
            # 获取音频信息
            self.frame_rate_A = audio.frame_rate# 帧率
            self.channels_A = audio.channels# 声道数
            self.sample_width_A = audio.sample_width# 采样宽度
            self.duration_seconds_A = round(audio.duration_seconds, 3)  # 时长s
            self.audio_info_A = ("帧率：" + str(self.frame_rate_A) + "\n" +
                                 "声道数：" + str(self.channels_A) + "\n" +
                                 "采样宽度：" + str(self.sample_width_A) + "\n" +
                                 "时长：" + str(self.duration_seconds_A) + "秒")
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, "SUCCESS", "音频导入成功！", self.button_input)

    # 导入音频的方法
    def inputAudio_B(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath_B, _ = QFileDialog.getOpenFileName()
        self.audio_info_B = None
        if filepath_B:
            self.audiopathB = filepath_B
            audio = AudioSegment.from_file(self.audiopath)
            # 获取音频信息
            self.frame_rate_B = audio.frame_rate# 帧率
            self.channels_B = audio.channels# 声道数
            self.sample_width_B = audio.sample_width# 采样宽度
            self.duration_seconds_B = round(audio.duration_seconds, 3)  # 时长s
            self.audio_info_B = "帧率：" + str(self.frame_rate_B) + "\n" + "声道数：" + str(self.channels_B) + "\n" + "采样宽度：" + str(self.sample_width_B) + "\n" + "时长：" + str(self.duration_seconds_B) + "s"
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, "SUCCESS", "音频B导入成功！", self.button_input)


    # 判断是否导入音频A
    def is_inputAudio_A(self):
        if self.audiopath == None:
            self.showFlyout_Custom2(InfoBarIcon.WARNING, "WARNING", "灾难性错误： 请先导入音频！",self.button_input)
            return False
        else:
            self.Audio_informationButton_A.clicked.connect(self.showComplexFlyout_A)
            self.showComplexFlyout_A()
            return True

    # 判断是否导入音频B
    def is_inputAudio_B(self):
        if self.audiopathB == None:
            self.showFlyout_Custom2(InfoBarIcon.WARNING, "WARNING", "灾难性错误： 请先导入音频！",self.button_input_B)
            return False
        else:
            self.Audio_informationButton_B.clicked.connect(self.showComplexFlyout_B)
            self.showComplexFlyout_B()
            return True

    # 获取输入框的值
    def get_input_box(self):
        size_value = self.lineEdit_start.text()
        if size_value == '':
            return 0
        else:
            return int(size_value)

    # 获取输入框的值
    def get_value(self, lineEdit):
        size_value = lineEdit.text()
        if size_value == '':
            return -1
        else:
            return int(size_value)

    # 打开文件夹的方法
    def open_folder(self):
        path = 'output/Audio_Processing'
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    # 创建浮出警告窗口的方法
    def showFlyout(self, title, content):
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title= title,
            content= content,
            target=self.button_input_apply,
            parent=self,
            isClosable=True
        )

    # 创建浮出客制化窗口的方法
    def showFlyout_Custom(self, infobaricon, title, content):
        Flyout.create(
            icon=infobaricon,
            title= title,
            content= content,
            target=self.button_input_apply,
            parent=self,
            isClosable=True
        )

    # 创建浮出客制化窗口的方法
    def showFlyout_Custom2(self, infobaricon, title, content, target):
        Flyout.create(
            icon=infobaricon,
            title=title,
            content=content,
            target=target,
            parent=self,
            isClosable=True
        )

    # 带有图片和按钮的FlyoutA
    def showComplexFlyout_A(self):
        view = FlyoutView(
            title=self.tr('音频信息'),
            content=self.tr(self.audio_info_A),
            image='Photos/resource/header/three.jpg',
        )

        # add button to view
        button = PushButton('确定')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.insertSpacing(0, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        Flyout.make(view, self.Audio_informationButton_A, self.window(), FlyoutAnimationType.SLIDE_RIGHT)
        
    # 带有图片和按钮的FlyoutB
    def showComplexFlyout_B(self):
        view = FlyoutView(
            title=self.tr('音频信息'),
            content=self.tr(self.audio_info_B),
            image='Photos/resource/header/three.jpg',
        )

        # add button to view
        button = PushButton('确定')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.insertSpacing(0, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        Flyout.make(view, self.Audio_informationButton_B, self.window(), FlyoutAnimationType.SLIDE_RIGHT)


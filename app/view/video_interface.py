# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths, QUrl, QThread, pyqtSignal
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
from moviepy.editor import VideoFileClip
from time import sleep
import threading

from .gallery_interface import GalleryInterface
from ..common.translator import Translator

class VideoProcessThread(QThread):
    processFinished = pyqtSignal()

    def __init__(self, videopath, enum, parent=None):
        super(VideoProcessThread, self).__init__(parent)
        self.videopath = videopath
        self.enum = enum

    def run(self):
        # 用moviepy读取视频
        video = VideoFileClip(self.videopath)
        # 获取视频的文件名字
        filename = self.videopath.split('/')[-1].split('.')[0]
        if self.enum == 1:
            # 将视频转换成音频
            audio = video.audio
            audio.write_audiofile('output/Video_Processing/{}.mp3'.format(filename))
        elif self.enum == 2:
            # 将视频转换成gif
            if video.duration > 10:
                return
            else:
                duration = video.duration
                print("视频的时长为： " + str(duration) + "s")
                video.write_gif('output/Video_Processing/{}.gif'.format(filename))
        elif self.enum == 3:
            # 将视频转换成图片
            fps = video.fps
            total_frames = video.duration * fps
            print("视频的总帧数为： " + str(total_frames))
            video.write_images_sequence('output/Video_Processing/to_photos/Video%d.png')
        elif self.enum == 4:
            # 将mkv转换成mp4
            video.write_videofile('output/Video_Processing/{}.mp4'.format(filename))
        elif self.enum == 5:
            # 将批量图片转换成视频
            subprocess.call('ffmpeg -f image2 -i output/Video_Processing/to_photos/Video%d.png output/Video_Processing/Video.mp4')
        else:
            return
        self.processFinished.emit()

class VideoInterface(GalleryInterface):
    """ Video interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.video,
            subtitle='音频提取、视频转换gif、导出批量图片、视频裁剪',
            parent=parent
        )
        self.videopath = None
        self.setObjectName('videoInterface')

        # 创建控件空间
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建子布局
        self.h_layout = QHBoxLayout(self.widget)# 创建水平布局h_layout
        self.h_layout_photos = QHBoxLayout(self.widget)# 创建水平布局h_layout_photos
        self.h_layout2 = QHBoxLayout(self.widget)  # 创建水平布局h_layout2


###### 创建控件区域 ######

        # 创建导入视频按钮
        self.button_input = PushButton(self.tr("导入视频"))
        self.button_input.setFixedWidth(100)  # 设置按钮大小
        self.button_input.clicked.connect(self.inputVideo)  # 连接按钮的点击信号导入图片并显示

        # 创建下拉框
        self.comboBox_filter = ComboBox()  # 创建下拉框
        self.comboBox_filter.setPlaceholderText("请选择视频处理方法")
        items = ['视频音频提取','视频转换为gif', '视频转换批量图片', 'mkv转换mp4']  # 下拉框的选项
        self.comboBox_filter.addItems(items)  # 添加下拉框的选项
        self.comboBox_filter.setCurrentIndex(-1)  # 设置下拉框的默认选项
        self.comboBox_filter.setFixedWidth(120)  # 设置下拉框的宽度
        self.comboBox_filter.setMaximumWidth(180)  # 设置下拉框的最大宽度
        self.comboBox_filter.currentIndexChanged.connect(self.GetcomboBox_value)  # 当下拉框的选项改变时，触发事件

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.thread_Apply_Video_process)  # 连接按钮的点击信号导入图片并显示
        # self.button_input_apply.clicked.connect(self.Click_Apply)  # 连接按钮的点击信号导入图片并显示


        # 创建保存滤波图像按钮
        self.button_input_save = PrimaryPushButton(self.tr("打开文件夹"))
        self.button_input_save.setFixedWidth(120)  # 设置按钮大小
        self.button_input_save.clicked.connect(self.open_folder)  # 连接按钮的点击信号导入图片并显示
        label = QLabel(self.tr('The significance of human history lies in inheritance and accumulation！'))
        # self.imageLabel = ImageLabel('Photos/resource/interface_background/Vertin2k.jpg')

        # 创建查看视频信息的按钮
        self.video_imformation = PushButton(self.tr('视频信息'))
        self.video_imformation.clicked.connect(self.is_inputVideo)

        # 创建图像分割时的一个输入框
        self.lineEdit_K = LineEdit()  # 创建输入框分割块数
        self.lineEdit_K.setPlaceholderText("Segments")
        self.lineEdit_K.setFixedWidth(100)  # 设置输入框的宽度
        self.lineEdit_K.setEnabled(False)  # 设置输入框不可用


###### 控件区域布局 ######

        # 子布局参数设置
        self.h_layout.setSpacing(100)  # 设置水平布局的间距
        self.h_layout.setSpacing(10)# 设置水平布局的间距
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距
        self.h_layout2.setSpacing(10)  # 设置水平布局的间距

        # 添加控件
        self.h_layout.addWidget(self.button_input, 0, Qt.AlignLeft)# 将按钮添加到水平布局中
        self.h_layout.addWidget(self.comboBox_filter, 0, Qt.AlignLeft)  # 将下拉框添加到水平布局中
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.h_layout.addWidget(self.button_input_save, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.h_layout.addWidget(self.video_imformation, 0, Qt.AlignLeft)
        self.widget.layout().addWidget(label)  # 将标签添加到布局中


        # 布局嵌套
        self.h_layout.addLayout(self.h_layout2)  # 将水平布局添加到垂直布局中
        self.vBoxLayout.addLayout(self.h_layout)  # 将水平布局添加到垂直布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将图片水平布局添加到布局中

        # 添加一个示例卡片
        self.addExampleCard(
            self.tr('视频影像处理'),
            self.widget,
            ' ',
            stretch=1
        )

###### 函数区域 ######

    # 视频处理的方法
    def Apply_Video_process(self):
        # 获取下拉框的选项
        enum = self.GetcomboBox_value()
        # 判断inputPhoto的图片路径
        if self.videopath == None:
            self.showFlyout("WARNING", "灾难性错误： 请先导入视频！")
            return
        # 用moviepy读取视频
        video = VideoFileClip(self.videopath)
        # 获取视频的文件名字
        filename = self.videopath.split('/')[-1].split('.')[0]
        if enum == 1:
            # 将视频转换成音频
            audio = video.audio
            audio.write_audiofile('output/Video_Processing/{}.mp3'.format(filename))
        elif enum == 2:
            # 将视频转换成gif
            if video.duration > 10:
                self.showFlyout("WARNING", "灾难性错误： 视频时长过长，请选择时长小于10s的视频！")
                return
            else:
                duration = video.duration
                print("视频的时长为： " + str(duration) + "s")
                video.write_gif('output/Video_Processing/{}.gif'.format(filename))
                self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "视频转换成gif成功！")
        elif enum == 3:
            # 将视频转换成图片
            fps = video.fps
            total_frames = video.duration * fps
            self.showFlyout_Custom(InfoBarIcon.SUCCESS, "SUCCESS", "视频的总帧数为： " + str(total_frames))
            print("视频的总帧数为： " + str(total_frames))
            video.write_images_sequence('output/Video_Processing/to_photos/Video%d.png')
        elif enum == 4:
            # 将mkv转换成mp4
            video.write_videofile('output/Video_Processing/{}.mp4'.format(filename))
        else:
            return

    # 创建线程
    def thread_Apply_Video_process(self):
        thread = threading.Thread(target=self.Apply_Video_process).start()
        return True

    # 当下拉框的选项改变时，触发事件
    def GetcomboBox_value(self):
        # 获取下拉框的选项
        comboBox_value = self.comboBox_filter.currentText()
        print(comboBox_value)
        res = -1
        if comboBox_value == '视频音频提取':
            res = 1
        elif comboBox_value == '视频转换为gif':
            res = 2
        elif comboBox_value == '视频转换批量图片':
            res = 3
        elif comboBox_value == 'mkv转换mp4':
            res = 4
        else:
            res = -1
        return res

    # 按下Apply按钮后，触发进程
    def Click_Apply(self):
        self.videoProcessThread = VideoProcessThread(self.videopath, self.GetcomboBox_value(), self)
        self.videoProcessThread.processFinished.connect(self.showFlyout_Custom2(InfoBarIcon.SUCCESS, "SUCCESS", "视频处理成功！", self.button_input_apply))
        self.videoProcessThread.start()

    # 创建命令栏弹出窗口的方法
    def createCommandBarFlyout(self):
        view = CommandBarView(self)

        view.addAction(Action(FIF.SHARE, self.tr('Share')))
        view.addAction(Action(FIF.SAVE, self.tr('Save'), triggered=self.saveImage))
        view.addAction(Action(FIF.HEART, self.tr('Add to favorate')))
        view.addAction(Action(FIF.DELETE, self.tr('Delete')))

        view.addHiddenAction(Action(FIF.PRINT, self.tr('Print'), shortcut='Ctrl+P'))
        view.addHiddenAction(Action(FIF.SETTING, self.tr('Settings'), shortcut='Ctrl+S'))
        view.resizeToSuitableWidth()

        x = self.imageLabel.width()
        pos = self.imageLabel.mapToGlobal(QPoint(x, 0))
        Flyout.make(view, pos, self, FlyoutAnimationType.FADE_IN)

    # 保存图片的方法
    def saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('Save image'),
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='TIF (*.tif)'
        )
        if not ok:
            return

        self.imageLabel.image.save(path)

    # 导入视频的方法
    def inputVideo(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath, _ = QFileDialog.getOpenFileName()
        self.video_info = None
        if filepath:
            # 用moviepy读取视频
            self.videopath = filepath
            video = VideoFileClip(self.videopath)
            # 获取视频信息
            self.duration = video.duration  # 视频的持续时间，单位为秒
            self.fps = video.fps    # 视频帧率
            self.size = video.size  # 视频尺寸
            self.video_info = ("视频尺寸：" + str(self.size) + "\n" +
                               "视频时长：" + str(self.duration) + "s" + "\n" +
                               "视频帧率：" + str(self.fps) + "\n")
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, "SUCCESS", "视频导入成功！", self.button_input)


    def get_input_box(self):
        size_value = self.lineEdit_K.text()
        if size_value == '':
            return 0
        else:
            return int(size_value)



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

    # 保存滤波图片的方法
    def Filter_saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('保存图片'),
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='TIF (*.tif)'
        )
        if not ok:
            return

    def is_inputVideo(self):
        if self.videopath == None:
            self.showFlyout_Custom2(InfoBarIcon.WARNING,"WARNING",'灾难性错误：请先导入视频！',self.video_imformation)
            return False
        else:
            self.video_imformation.clicked.connect(self.showComplexFlyout_video)
            self.showComplexFlyout_video()
            return True

    def showComplexFlyout_video(self):
        view = FlyoutView(
            title=self.tr('视频信息'),
            content=self.tr(self.video_info),
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
        Flyout.make(view, self.video_imformation, self.window(), FlyoutAnimationType.SLIDE_RIGHT)

    # 打开文件夹的方法
    def open_folder(self):
        path = 'output/Video_Processing'
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))


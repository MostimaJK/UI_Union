# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QVBoxLayout, QFileDialog, QActionGroup, QLabel,
                             QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QGraphicsView,
                             QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QVBoxLayout, QTextEdit)
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType, CheckableMenu,
                            MenuIndicatorType, AvatarWidget, isDarkTheme, BodyLabel, CaptionLabel, HyperlinkButton,
                            ComboBox, PrimaryPushButton, InfoBarIcon, LineEdit, TextEdit)
from qfluentwidgets import FluentIcon as FIF
import cv2
import os
from datetime import datetime

from .gallery_interface import GalleryInterface
from ..common.translator import Translator



class TimeInterface(GalleryInterface):
    """ Time interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.time,
            subtitle='设置定时关机',
            parent=parent
        )
        self.imagePath = None
        self.setObjectName('TimeInterface')

        # 浮出命令栏
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建水平布局
        self.h_layout = QHBoxLayout(self.widget)  # 创建水平布局
        self.h_layout.setSpacing(70)  # 设置水平布局的间距
        self.h_layout.setAlignment(Qt.AlignCenter)  # 设置水平布局的对齐方式
        self.vBoxLayout.addLayout(self.h_layout)  # 将水平布局添加到垂直布局中


        label = QLabel(self.tr('羊咩咩的瑞士卷'))
        self.imageLabel = ImageLabel('Photos/resource/interface_background/aiyafla.jpg')

        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)  # 将图片A添加到水平布局中

        # 创建定时关机时的文字
        self.text_shutdown = QLabel() # 创建输入框
        self.text_shutdown.setText(self.tr('请输入关机时间：'))
        self.text_shutdown.setStyleSheet("font-size: 20px;")
        self.h_layout.addWidget(self.text_shutdown, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 创建定时关机时的三个输入框
        self.lineEdit_hour = LineEdit()  # 创建输入框
        self.lineEdit_min = LineEdit()  # 创建输入框
        self.lineEdit_sec = LineEdit()  # 创建输入框
        self.lineEdit_hour.setPlaceholderText("小时")
        self.lineEdit_min.setPlaceholderText("分钟")
        self.lineEdit_sec.setPlaceholderText("秒")
        self.lineEdit_hour.setFixedWidth(100)  # 设置输入框的宽度
        self.lineEdit_min.setFixedWidth(100)  # 设置输入框的宽度
        self.lineEdit_sec.setFixedWidth(100)  # 设置输入框的宽度
        self.h_layout2 = QHBoxLayout(self.widget)  # 创建水平布局
        self.h_layout2.addWidget(self.lineEdit_hour, 0, Qt.AlignLeft)  # 将输入框添加到水平布局中
        self.h_layout2.addWidget(self.lineEdit_min, 0, Qt.AlignLeft)  # 将输入框添加到水平布局中
        self.h_layout2.addWidget(self.lineEdit_sec, 0, Qt.AlignLeft)  # 将输入框添加到水平布局中
        self.h_layout2.setSpacing(10)  # 设置水平布局的间距
        self.h_layout.addLayout(self.h_layout2)  # 将水平布局添加到垂直布局中

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_Time)  # 连接按钮的点击信号导入图片并显示
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 创建导入Stop按钮
        self.button_input_apply = PushButton(self.tr("取消关机"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.stop_shutdown)  # 连接按钮的点击信号导入图片并显示
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 设置图片功能
        self.imageLabel.scaledToWidth(500)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(8, 8, 8, 8)  # 设置图片的圆角


        self.widget.layout().addWidget(label)  # 将标签添加到布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中

        # 添加一个示例卡片，包含了标签的翻译，标签对象，示例代码的链接，和拉伸值
        self.addExampleCard(
            self.tr('Picture'),
            self.widget,
            'https://www.bilibili.com/?spm_id_from=333.999.b_696e7465726e6174696f6e616c486561646572.1',
            stretch=1
        )

    # 定时关机的方法
    def Apply_Time(self):
        # 获取三个输入框的值
        hour_value = self.lineEdit_hour.text()
        min_value = self.lineEdit_min.text()
        sec_value = self.lineEdit_sec.text()

        if hour_value == '' and min_value == '' and sec_value == '':
            self.showFlyout("WARNING", "提示：请输入时间！")
            return

        # 如果有一个输入框不为为空，则默认其他两个输入框为0
        if hour_value == '':
            hour_value = '0'
        if min_value == '':
            min_value = '0'
        if sec_value == '':
            sec_value = '0'

        # 将输入的时间转换为秒
        total_time = int(hour_value) * 3600 + int(min_value) * 60 + int(sec_value)

        # 设置定时关机
        os.system(f"shutdown -s -t {total_time}")
        self.showFlyout_Success('SUCCESS','将在' + str(total_time) + '秒后关机')
        return 1

    def stop_shutdown(self):
        os.system(f"shutdown -a")

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

    # 创建浮出成功窗口的方法
    def showFlyout_Success(self, title, content):
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title= title,
            content= content,
            target=self.button_input_apply,
            parent=self,
            isClosable=True
        )

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


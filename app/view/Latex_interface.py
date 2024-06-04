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
from PIL import Image
from pix2tex.cli import LatexOCR
import pyperclip

from .gallery_interface import GalleryInterface
from ..common.translator import Translator



class LatexInterface(GalleryInterface):
    """ Latex interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title='Latex-OCR',
            subtitle='Latex-OCR图像识别',
            parent=parent
        )
        self.imagePath = None
        self.setObjectName('latexInterface')

        # 浮出命令栏
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建导入图片按钮
        self.button_input = PushButton(self.tr("导入图片"))
        self.button_input.setFixedWidth(100)  # 设置按钮大小
        self.h_layout = QHBoxLayout(self.widget)# 创建水平布局
        self.h_layout.setSpacing(10)# 设置水平布局的间距
        self.h_layout.addWidget(self.button_input, 0, Qt.AlignLeft)# 将按钮添加到水平布局中
        self.vBoxLayout.addLayout(self.h_layout)# 将水平布局添加到垂直布局中
        self.button_input.clicked.connect(self.inputPhoto)  # 连接按钮的点击信号导入图片并显示

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_Latex)  # 连接按钮的点击信号导入图片并显示
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 创建复制识别结果按钮
        self.button_save = PrimaryPushButton(self.tr("复制识别结果"))
        self.button_save.setFixedWidth(120)  # 设置按钮大小
        self.h_layout.addWidget(self.button_save, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.button_save.clicked.connect(self.copy_LatexOCR)  # 连接按钮的点击信号导入图片并显示

        label = QLabel()
        self.imageLabel = ImageLabel('Photos/resource/interface_background/magic.jpg')

        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)  # 将图片A添加到水平布局中


        # 设置图片的功能
        self.imageLabel.scaledToWidth(400)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(10, 10, 10, 10)  # 设置图片的圆角
        self.imageLabel.clicked.connect(self.createCommandBarFlyout)  # 连接图片的点击信号，打开命令栏


        self.widget.layout().addWidget(label)  # 将标签添加到布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中

        self.Latex_result = TextEdit()
        self.Latex_result.setFixedHeight(50)

        # 添加一个示例卡片，包含了标签的翻译，标签对象，示例代码的链接，和拉伸值
        self.addExampleCard(
            self.tr('Latex公式识别结果'),
            self.Latex_result,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
            stretch=1
        )

        # 添加一个示例卡片，包含了标签的翻译，标签对象，示例代码的链接，和拉伸值
        self.addExampleCard(
            self.tr('数学公式图片'),
            self.widget,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
            stretch=1
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

    # 导入图片的方法
    def inputPhoto(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath, _ = QFileDialog.getOpenFileName()
        if filepath:
            # 将用户选择的图片路径赋值给ImageLabel
            self.imageLabel.setPixmap(filepath)
            # 设置图片的最大宽度
            self.imageLabel.setMaximumWidth(800)
            self.imageLabel.scaledToWidth(500)  # 设置图片的宽度
            self.imagePath = filepath  # 保存图片路径
            self.src = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)  # 用opencv读取图片


    # 图像滤波的应用方法
    def Apply_Latex(self):
        # 判断inputPhoto的图片路径
        if self.imagePath == None:
            self.showFlyout("WARNING", "灾难性错误： 请先导入图片！")
            return
        # img = cv2.imread(self.imagePath)  # 用opencv读取图片
        math_img = Image.open(self.imagePath)# 用PIL读取图片
        self.result = None
        model = LatexOCR()
        self.result = model(math_img)
        # 将识别结果显示在界面上
        self.Latex_result.setPlainText(self.result)
        # 将识别结果复制到剪贴板
        pyperclip.copy(self.result)
        self.showFlyout_Success("SUCCESS", "成功识别公式并自动复制到剪贴板！")

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

    # 复制识别结果的方法
    def copy_LatexOCR(self):
        if self.imagePath == None:
            self.showFlyout("WARNING", "灾难性错误： 请先导入图片！")
        elif self.result != None:
            pyperclip.copy(self.result)
            self.showFlyout_Success_copy("SUCCESS", "成功识别公式并自动复制到剪贴板！")

    # 创建浮出成功窗口的方法
    def showFlyout_Success_copy(self, title, content):
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title= title,
            content= content,
            target=self.button_save,
            parent=self,
            isClosable=True
        )
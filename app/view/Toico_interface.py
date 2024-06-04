# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths, QUrl
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QWheelEvent, QMouseEvent, QDesktopServices
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QVBoxLayout, QFileDialog, QActionGroup, QLabel,
                             QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QGraphicsView,
                             QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QVBoxLayout)
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType, CheckableMenu,
                            MenuIndicatorType, AvatarWidget, isDarkTheme, BodyLabel, CaptionLabel, HyperlinkButton,
                            ComboBox, PrimaryPushButton, InfoBarIcon, LineEdit)
from qfluentwidgets import FluentIcon as FIF

import cv2
import os
import glob
from PIL import Image
from io import BytesIO

from .gallery_interface import GalleryInterface
from ..common.translator import Translator



class ToicoInterface(GalleryInterface):
    """ To ico interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.toico,
            subtitle='将图片转换成.ico格式',
            parent=parent
        )
        self.imagePath = None
        self.setObjectName('ToicoInterface')

        # 浮出命令栏
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建导入图片按钮A
        self.button_input_A = PushButton(self.tr("导入图片"))
        self.button_input_A.setFixedWidth(150)  # 设置按钮大小
        self.h_layout = QHBoxLayout(self.widget)  # 创建水平布局
        self.h_layout.addWidget(self.button_input_A, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.button_input_A.clicked.connect(self.inputPhoto)  # 连接按钮的点击信号导入图片并显示

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_toico)  # 连接按钮的点击信号导入图片并显示
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 创建保打开文件夹按钮
        self.button_open = PrimaryPushButton(self.tr("打开文件夹"))
        self.button_open.setFixedWidth(120)  # 设置按钮大小
        self.h_layout.addWidget(self.button_open, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.button_open.clicked.connect(self.open_folder)  # 连接按钮的点击信号导入图片并显示

        label = QLabel(self.tr('导入图片点击Apply后，图片自动转换成.ico格式并保存'))
        self.imageLabel = ImageLabel('Photos/resource/interface_background/aiyafla.jpg')

        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)  # 将图片A添加到水平布局中

        # 设置图片功能
        self.imageLabel.scaledToWidth(500)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(8, 8, 8, 8)  # 设置图片的圆角
        self.imageLabel.clicked.connect(self.createCommandBarFlyout)  # 连接图片的点击信号，打开命令栏

        self.widget.layout().addWidget(label)  # 将标签添加到布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中
        self.h_layout.setAlignment(Qt.AlignCenter)  # 设置水平布局的对齐方式
        self.h_layout.setSpacing(200)  # 设置水平布局的间距
        self.vBoxLayout.addLayout(self.h_layout)  # 将水平布局添加到垂直布局中

        # 添加一个示例卡片，包含了标签的翻译，标签对象，示例代码的链接，和拉伸值
        self.addExampleCard(
            self.tr('Picture'),
            self.widget,
            'https://www.bilibili.com/',
            stretch=1
        )

    # 保存图片的方法
    def saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('Save image'),
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='ICO (*.ico)'
        )
        if not ok:
            return

        self.imageLabel.image.save(path)

    # 导入图片A的方法
    def inputPhoto(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath, _ = QFileDialog.getOpenFileName()
        if filepath:
            # 将用户选择的图片路径赋值给ImageLabel
            self.imageLabel.setPixmap(filepath)
            # 设置图片的最大宽度
            self.imageLabel.setMaximumWidth(500)
            self.imageLabel.scaledToWidth(300)  # 设置图片的宽度
            self.imagePath = filepath  # 保存图片路径

    # 图像滤波的应用方法
    def Apply_toico(self):
        # 判断inputPhoto的图片路径
        if self.imagePath == None:
            self.showFlyout_warnning("WARNING", "灾难性错误： 请先导入图片！")
            return
        img = Image.open(self.imagePath)  # 用PIL读取图片
        base_name = os.path.basename(self.imagePath)
        file_name, _ = os.path.splitext(base_name)
        print(f'图像文件名: {base_name}')
        # 将图像保存为.ico文件，文件名与原始图像文件的文件名相同
        img.save(f'output/ico_Processing/{file_name}.ico', format='ICO', sizes=[(64, 64)])
        self.showFlyout_Success("SUCCESS", f"图像已成功保存为{file_name}.ico文件！")

    # 创建浮出警告窗口的方法
    def showFlyout_warnning(self, title, content):
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title= title,
            content= content,
            target=self.button_input_apply,
            parent=self,
            isClosable=True
        )

    def open_folder(self):
        # 定义你想要打开的文件夹的路径
        folder_path = 'output/ico_Processing'
        # 使用QDesktopServices打开文件夹
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

    # 创建浮出警告窗口的方法
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

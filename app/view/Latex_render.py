# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths, QUrl
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QWheelEvent, QMouseEvent, QDesktopServices
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QVBoxLayout, QFileDialog, QActionGroup, QLabel,
                             QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QGraphicsView,
                             QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QVBoxLayout, )
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType, CheckableMenu,
                            MenuIndicatorType, AvatarWidget, isDarkTheme, BodyLabel, CaptionLabel, HyperlinkButton,
                            ComboBox, PrimaryPushButton, InfoBarIcon, LineEdit, FlyoutView, TextEdit)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from qfluentwidgets import FluentIcon as FIF

from pydub import AudioSegment
import matplotlib.pyplot as plt
import threading

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class LatexRenderInterface(GalleryInterface):
    """ LatexRender interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.latex_render,
            subtitle='LeTeX公式实时渲染和图片导出',
            parent=parent
        )

        self.setObjectName('latexrenderInterface')

        # 创建控件空间
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建子布局
        self.h_layout = QHBoxLayout(self.widget)  # 创建h_layout水平布局
        self.h_layout_latex = QHBoxLayout(self.widget)  # 创建参数水平布局

        ###### 创建控件区域 ######

        # 创建dpi输入框
        self.lineEdit_dpi = LineEdit()
        self.lineEdit_dpi.setPlaceholderText("DPI默认为300")
        self.lineEdit_dpi.setFixedWidth(120)  # 设置输入框的宽度

        # 创建fontsize输入框
        self.lineEdit_fontsize = LineEdit()
        self.lineEdit_fontsize.setPlaceholderText("Font Size默认为25")
        self.lineEdit_fontsize.setFixedWidth(150)  # 设置输入框的宽度

        # 创建导入Apply按钮
        self.button_apply = PushButton(self.tr("Apply"))
        self.button_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_apply.clicked.connect(self.Apply_Latex_render)  # 连接按钮的点击信号导入图片并显示

        # 创建打开文件夹按钮
        self.button_input_save = PrimaryPushButton(self.tr("打开文件夹"))
        self.button_input_save.setFixedWidth(120)  # 设置按钮大小
        self.button_input_save.clicked.connect(self.open_folder)  # 连接按钮的点击信号导入图片并显示

        # 添加LaTeX公式输入框
        self.Latex_result = TextEdit()
        self.Latex_result.setFixedHeight(50)
        self.Latex_result.setPlaceholderText("请输入LaTeX公式")
        self.Latex_result.textChanged.connect(self.thread_realtimerender)  # 连接按钮的点击信号导入图片并显示

        ###### 控件区域布局 ######

        # 子布局参数设置
        self.h_layout.setSpacing(100)  # 设置水平布局的间距
        self.h_layout.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式
        self.h_layout_latex.setSpacing(100)  # 设置水平布局的间距
        self.h_layout_latex.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式

        # 添加控件
        self.h_layout.addWidget(self.lineEdit_dpi, 0, Qt.AlignCenter)  # 将dpi输入框添加到水平布局中
        self.h_layout.addWidget(self.lineEdit_fontsize, 0, Qt.AlignCenter)  # 将fontsize输入框添加到水平布局中
        self.h_layout.addWidget(self.button_apply, 0, Qt.AlignCenter)  # 将Apply添加到水平布局中
        self.h_layout.addWidget(self.button_input_save, 0, Qt.AlignCenter)  # 将打开文件夹添加到水平布局中

        # 布局嵌套
        self.vBoxLayout.addLayout(self.h_layout)  # 将水平布局添加到垂直布局中
        self.vBoxLayout.addLayout(self.h_layout_latex)  # 将水平布局添加到垂直布局中
        self.widget.layout().addLayout(self.h_layout)  # 将水平布局添加到垂直布局中

        # 图片显示区域
        label = QLabel()
        self.imageLabel = ImageLabel('Photos/resource/interface_background/magic.jpg')
        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)  # 将图片A添加到水平布局中
        # 设置图片的功能
        self.imageLabel.scaledToWidth(400)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(10, 10, 10, 10)  # 设置图片的圆角
        self.widget.layout().addWidget(label)  # 将标签添加到布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中

        self.addExampleCard(
            self.tr('LaTeX'),
            self.Latex_result,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
            stretch=1
        )

        # 添加LaTeX公式渲染结果卡片
        self.addExampleCard(
            self.tr('LaTex公式渲染'),
            self.widget,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
            stretch=1
        )

    ###### 函数区域 ######

    # Apply函数
    def Apply_Latex_render(self):
        # 变量
        self.fig = plt.figure()
        self.dpi_set = self.get_dpi_value(self.lineEdit_dpi)
        self.fontsize_set = self.get_fontsize_value(self.lineEdit_fontsize)
        self.latex_formula = self.Latex_result.toPlainText()
        # 创建一个新的图像
        if self.latex_formula == '':
            self.showFlyout_Custom(InfoBarIcon.WARNING, 'WARNING', '请输入LaTeX公式!')
            return None
        else:
            # 在图像中添加一个LaTeX公式
            plt.text(0.5, 0.5, fr'${self.latex_formula}$', fontsize=self.fontsize_set, ha='center')
            # 隐藏坐标轴
            plt.axis('off')
            # 保存图像为PNG文件
            plt.savefig('output/LaTex_Rendering/formula.png', bbox_inches='tight', pad_inches=0, dpi=self.dpi_set)
            self.imageLabel.setPixmap(QPixmap('output/LaTex_Rendering/formula.png'))
            self.imageLabel.setMaximumWidth(800)
            self.imageLabel.scaledToWidth(450)  # 设置图片的宽度
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', 'LaTeX公式渲染成功!', self.button_apply)
            return 1

    # 当Latex公式输入框的值改变时，实时渲染
    def realtime_render(self):
        # 在图像中添加一个LaTeX公式
        rendering_dpi = self.get_dpi_value(self.lineEdit_dpi)
        rendering_fontsize = self.get_fontsize_value(self.lineEdit_fontsize)
        rendering_latex = self.Latex_result.toPlainText()
        plt.figure()
        plt.text(0.5, 0.5, fr'${rendering_latex}$', fontsize=rendering_fontsize, ha='center')
        # 隐藏坐标轴
        plt.axis('off')
        # 保存图像为PNG文件
        plt.savefig('output/LaTex_Rendering/Temporarily/Rendering.png', bbox_inches='tight', pad_inches=0, dpi=rendering_dpi)
        # 读取图像并显示
        self.imageLabel.setPixmap(QPixmap('output/LaTex_Rendering/Temporarily/Rendering.png'))
        self.imageLabel.setMaximumWidth(800)
        self.imageLabel.scaledToWidth(450)  # 设置图片的宽度
        return 1

    def thread_realtimerender(self):
        threading.Thread(target=self.realtime_render).start()
        return 1

    # 获取dpi输入框的值
    def get_dpi_value(self, lineEdit, default_dpi=300):
        size_value = lineEdit.text()
        if size_value == '':
            return default_dpi
        else:
            return int(size_value)

    # 获取fontsize输入框的值
    def get_fontsize_value(self, lineEdit, default_fontsize=300):
        size_value = lineEdit.text()
        if size_value == '':
            return default_fontsize
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
        path = 'output/LaTeX_Rendering'
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    # 创建浮出警告窗口的方法
    def showFlyout(self, title, content):
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title=title,
            content=content,
            target=self.button_apply,
            parent=self,
            isClosable=True
        )

    # 创建浮出客制化窗口的方法
    def showFlyout_Custom(self, infobaricon, title, content):
        Flyout.create(
            icon=infobaricon,
            title=title,
            content=content,
            target=self.button_apply,
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
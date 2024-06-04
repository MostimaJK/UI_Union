# coding:utf-8
from PyQt5.QtCore import QPoint, Qt, QStandardPaths, QUrl
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QWheelEvent, QMouseEvent, QDesktopServices
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



class SortInterface(GalleryInterface):
    """ Sort interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title='编号文件',
            subtitle='为文件夹内的文件编号',
            parent=parent
        )
        self.imagePath = None
        self.setObjectName('sortInterface')

        # 浮出命令栏
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建子布局
        self.h_layout = QHBoxLayout(self.widget)# 创建水平布局

###### 创建控件区域 ######

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_Sort)  # 连接按钮的点击信号导入图片并显示
        # self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 创建重命名方式下拉框
        self.rename_method = ComboBox()
        self.rename_method.setPlaceholderText('请选择重命名方式')
        items = ['重命名所有文件','编号并保留文件名', '仅编号']  # 下拉框的选项
        self.rename_method.addItems(items)  # 添加下拉框的选项
        self.rename_method.setCurrentIndex(-1)
        self.rename_method.setFixedWidth(180)
        self.rename_method.clicked.connect(self.GetcomboBox_value)
        # self.h_layout.addWidget(self.rename_method, 0, Qt.AlignLeft)

        # 创建文件名输入框
        self.folder_new_name = LineEdit()
        self.folder_new_name.setFixedWidth(150)  # 设置按钮大小
        self.folder_new_name.setPlaceholderText('新的文件名')
        # self.h_layout.addWidget(self.folder_new_name, 0, Qt.AlignLeft)

        # 创建打开文件夹按钮
        self.button_open = PrimaryPushButton(self.tr("打开文件夹"))
        self.button_open.setFixedWidth(120)  # 设置按钮大小
        # self.h_layout.addWidget(self.button_open, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.button_open.clicked.connect(self.folder_open)  # 连接按钮的点击信号导入图片并显示

        # 创建一个文本输入框
        self.folder_path_edit = TextEdit()
        self.folder_path_edit.setFixedHeight(40)

        label = QLabel(self.tr('单击图片打开命令栏'))

        ###### 控件区域布局 ######

        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距

        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中
        self.h_layout.setAlignment(Qt.AlignCenter)# 设置水平布局的对齐方式
        self.h_layout.setSpacing(200)
        self.vBoxLayout.addLayout(self.h_layout)# 将水平布局添加到垂直布局中

        # 添加控件
        self.h_layout.addWidget(self.rename_method, 0, Qt.AlignLeft)
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.h_layout.addWidget(self.folder_new_name, 0, Qt.AlignLeft)
        self.h_layout.addWidget(self.button_open, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中


        # 添加一个示例卡片，包含了标签的翻译，标签对象，示例代码的链接，和拉伸值
        self.addExampleCard(
            self.tr('文件夹路径'),
            self.folder_path_edit,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/menu/menu/demo.py',
            stretch=1
        )




    # 重命名文件的方法
    def Apply_Sort(self):
        # 获取下拉框的选项
        enum = self.GetcomboBox_value()
        # 获取TextEdit的文本
        self.folder_path = self.folder_path_edit.toPlainText()
        # 判断文件路径是否为空
        if self.folder_path == None:
            self.showFlyout("WARNING", "灾难性错误： 请先输入文件夹路径！")
            return
        # 列出文件夹中的所有文件
        file_list = os.listdir(self.folder_path)
        # 遍历文件列表并输出每个文件的名称
        for file_name in file_list:
            print(file_name)
        if enum == 1:
            # 重命名所有文件
            # 遍历文件列表并为文件添加序号
            for i, file_name in enumerate(file_list):
                # 生成新的文件名
                sub_name = self.get_input_box()
                # 获取文件扩展名
                file_extension = os.path.splitext(file_name)[1]
                new_file_name = '{:02d}_{}{}'.format(i + 1, sub_name, file_extension)
                # 重命名文件
                os.rename(os.path.join(self.folder_path, file_name), os.path.join(self.folder_path, new_file_name))
                print('文件{}已经重命名为{}'.format(file_name, new_file_name))
            # 输出修改之后的每个文件名称
            document_list = os.listdir(self.folder_path)
            for document_name in document_list:
                print(document_name)
            # 统计文件夹下文件数量
            number = len(file_list)
            print("文件总数量为：{} ".format(number))
            self.showFlyout_Success("SUCCESS", "文件已成功编号！")
        elif enum == 2:
            # 编号并保留文件名
            # 遍历文件列表并为没有序号的文件添加序号
            for i, file_name in enumerate(file_list):
                # 如何文件名中已经有序号，则跳过
                # [0:2]左闭右开，前两个字符
                if file_name[2] == '_' and file_name[0:2].isdigit():
                    continue
                else:
                    # 获取文件原名字
                    new_file_name = '{:02d}_{}'.format(i + 1, file_name)
                    # 重命名文件
                    os.rename(os.path.join(self.folder_path, file_name), os.path.join(self.folder_path, new_file_name))

            self.showFlyout_Success("SUCCESS", "文件已成功编号！")
        elif enum == 3:
            # 仅编号
            # 遍历文件列表并为没有序号的文件添加序号
            for i, file_name in enumerate(file_list):
                # 获取文件扩展名
                file_extension = os.path.splitext(file_name)[1]
                new_file_name = '{:02d}{}'.format(i + 1, file_extension)
                # 重命名文件
                os.rename(os.path.join(self.folder_path, file_name), os.path.join(self.folder_path, new_file_name))
            self.showFlyout_Success("SUCCESS", "文件已成功编号！")
        elif enum == -1:
            self.showFlyout("WARNING", "灾难性错误： 请先选择重命名方式！")

    # 当下拉框的选项改变时，触发事件
    def GetcomboBox_value(self):
        # 获取下拉框的选项
        comboBox_value = self.rename_method.currentText()
        print(comboBox_value)
        res = -1
        if comboBox_value == '重命名所有文件':
            res = 1
        elif comboBox_value == '编号并保留文件名':
            res = 2
        elif comboBox_value == '仅编号':
            res = 3
        else:
            res = -1
        return res

    # 获取输入框的值
    def get_input_box(self):
        size_value = self.folder_new_name.text()
        if size_value == '':
            return -1
        else:
            return str(size_value)

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

    def folder_open(self):
        # 打开的文件夹的路径
        folder_path = self.folder_path_edit.toPlainText()
        # 使用QDesktopServices打开文件夹
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

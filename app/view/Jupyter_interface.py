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
import nbconvert
import threading
import os
import subprocess
import shutil

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class JupyterInterface(GalleryInterface):
    """ Jupyter interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.jupyter,
            subtitle='Jupyter Notebook',
            parent=parent
        )
        self.Jupyter_path = None
        self.setObjectName('jupyterInterface')

        # 创建控件空间
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建子布局
        self.h_layout = QHBoxLayout(self.widget)  # 创建h_layout水平布局
        self.h_layout_Jupyter = QHBoxLayout(self.widget)  # 创建参数水平布局

        ###### 创建控件区域 ######

        # 创建导入Jupyter按钮
        self.button_input = PushButton(self.tr("导入Jupyter文件"))
        self.button_input.setFixedWidth(150)  # 设置按钮大小
        self.button_input.clicked.connect(self.inputJupyter)  # 连接按钮的点击信号导入图片并显示

        # 创建下拉框
        self.comboBox_jupyter = ComboBox()  # 创建下拉框
        self.comboBox_jupyter.setPlaceholderText("请选择Jupyter处理方法")
        items = ['转换为LaTeX格式', '转换为PDF', '转换为Markdown', '转换为HTML', '转换为Python脚本']  # 下拉框的选项
        self.comboBox_jupyter.addItems(items)  # 添加下拉框的选项
        self.comboBox_jupyter.setCurrentIndex(-1)  # 设置下拉框的默认选项
        self.comboBox_jupyter.setFixedWidth(180)  # 设置下拉框的宽度
        self.comboBox_jupyter.setMaximumWidth(200)  # 设置下拉框的最大宽度
        self.comboBox_jupyter.currentIndexChanged.connect(self.GetcomboBox_value)  # 当下拉框的选项改变时，触发事件

        # 创建导入Apply按钮
        self.button_apply = PushButton(self.tr("Apply"))
        self.button_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_apply.clicked.connect(self.thread_Apply_Jupyter)  # 连接按钮的点击信号导入图片并显示

        # 创建打开文件夹按钮
        self.button_open_folder = PrimaryPushButton(self.tr("打开文件夹"))
        self.button_open_folder.setFixedWidth(120)  # 设置按钮大小
        self.button_open_folder.clicked.connect(self.open_folder)  # 连接按钮的点击信号导入图片并显示

        # 创建清理文件按钮
        self.button_clear_files = PrimaryPushButton(self.tr("清理文件"))
        self.button_clear_files.setFixedWidth(120)  # 设置按钮大小
        self.button_clear_files.clicked.connect(self.clear_files)  # 连接按钮的点击信号导入图片并显示

        ###### 控件区域布局 ######

        # 图片显示区域
        label = QLabel()
        self.imageLabel = ImageLabel('Photos/resource/interface_background/JN.png')
        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)  # 将图片A添加到水平布局中
        # 设置图片的功能
        self.imageLabel.scaledToWidth(400)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(10, 10, 10, 10)  # 设置图片的圆角
        self.widget.layout().addWidget(label)  # 将标签添加到布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中
        # self.h_layout_Jupyter.addWidget(self.imageLabel, 0, Qt.AlignCenter)  # 将图片添加到水平布局中

        # 子布局参数设置
        self.h_layout.setSpacing(100)  # 设置水平布局的间距
        self.h_layout.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式
        self.h_layout_Jupyter.setSpacing(100)  # 设置水平布局的间距
        self.h_layout_Jupyter.setAlignment(Qt.AlignLeft)  # 设置水平布局的对齐方式

        # 添加控件
        self.h_layout.addWidget(self.button_input, 0, Qt.AlignCenter)  # 将导入Jupyter按钮添加到水平布局中
        self.h_layout.addWidget(self.comboBox_jupyter, 0, Qt.AlignCenter)  # 将下拉框添加到水平布局中
        self.h_layout.addWidget(self.button_apply, 0, Qt.AlignCenter)  # 将Apply添加到水平布局中
        self.h_layout.addWidget(self.button_open_folder, 0, Qt.AlignCenter)  # 将打开文件夹添加到水平布局中
        self.h_layout.addWidget(self.button_clear_files, 0, Qt.AlignCenter)  # 将清理文件添加到水平布局中

        # 布局嵌套
        self.vBoxLayout.addLayout(self.h_layout)  # 将水平布局添加到垂直布局中
        self.vBoxLayout.addLayout(self.h_layout_Jupyter)  # 将水平布局添加到垂直布局中
        self.widget.layout().addLayout(self.h_layout)  # 将水平布局添加到垂直布局中

        # 添加一个示例卡片
        self.addExampleCard(
            self.tr('Jupyter环境配置要求'),
            self.widget,
            ' ',
            stretch=1
        )

    ###### 函数区域 ######

    def Apply_Jupyter(self):
        latex_output_dir = "output/Jupyter_Processing/LaTeX"
        markdown_output_dir = "output/Jupyter_Processing/Markdown"
        html_output_dir = "output/Jupyter_Processing/HTML"
        python_output_dir = "output/Jupyter_Processing/Python"
        # 获取下拉框的选项
        enum = self.GetcomboBox_value()
        if self.Jupyter_path == None:
            self.showFlyout_Custom(InfoBarIcon.WARNING, 'WARNING', '请载入Jupyter文件!')
            return None
        elif enum == 1:
            # 转换为LaTeX格式
            subprocess.check_call(f'jupyter nbconvert --to latex --output-dir="{latex_output_dir}" "{self.Jupyter_path}"', shell=True)
            print('转换LaTeX格式成功！')
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '转换LaTeX格式成功！', self.button_apply)
        elif enum == 2:
            # 转换为PDF
            # 1.检测是否已经转换为LaTeX格式,如果没有转换为LaTeX格式，就先转换为LaTeX格式
            if not os.path.exists(f'{latex_output_dir}/{self.filename}.tex'):
                subprocess.check_call(f'jupyter nbconvert --to latex --output-dir="{latex_output_dir}" "{self.Jupyter_path}"', shell=True)
                print('转换LaTeX格式成功！')
            # 2.解决中文乱码问题，将LaTeX文件中的第三行到第五行插入以下代码
            tex_path = os.path.join(latex_output_dir, self.filename + '.tex')
            tex_path = tex_path.replace("\\", "/")
            with open(tex_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            lines.insert(3, '\t'+'\\usepackage{fontspec, xunicode, xltxtra}\n')
            lines.insert(4, '\t'+'\\setmainfont{Microsoft YaHei}\n')
            lines.insert(5, '\t'+'\\usepackage{ctex}\n')
            with open(tex_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            # 3.将LaTeX文件转换为PDF
            # 指定要在 PowerShell 中执行的命令
            command = f'xelatex {self.filename}.tex'
            # 获取latex_output文件夹的绝对路径
            self.absolute_latex_output_dir = os.path.abspath(latex_output_dir)
            # 在指定的文件夹中打开 PowerShell 并执行命令
            subprocess.Popen(['powershell.exe', 'cd {}; {}'.format(self.absolute_latex_output_dir, command)])
            print('转换为PDF成功！')
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '转换为PDF成功！', self.button_apply)
        elif enum == 3:
            # 转换为Markdown
            subprocess.check_call(f'jupyter nbconvert --to markdown --output-dir="{markdown_output_dir}" "{self.Jupyter_path}"', shell=True)
            print('转换为Markdown成功！')
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '转换为Markdown成功！', self.button_apply)
        elif enum == 4:
            # 转换为HTML
            subprocess.check_call(f'jupyter nbconvert --to html --output-dir="{html_output_dir}" "{self.Jupyter_path}"', shell=True)
            print('转换为HTML成功！')
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '转换为HTML成功！', self.button_apply)
        elif enum == 5:
            # 转换为Python脚本
            subprocess.check_call(f'jupyter nbconvert --to script --output-dir="{python_output_dir}" "{self.Jupyter_path}"', shell=True)
            print('转换为Python脚本成功！')
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '转换为Python脚本成功！', self.button_apply)
        elif enum == -1:
            self.showFlyout_Custom(InfoBarIcon.WARNING, 'WARNING', '请选择Jupyter处理方法！')
            return None

    # 创建线程
    def thread_Apply_Jupyter(self):
        thread = threading.Thread(target=self.Apply_Jupyter).start()
        return True

    # 当下拉框的选项改变时，触发事件
    def GetcomboBox_value(self):
        # 获取下拉框的选项
        comboBox_value = self.comboBox_jupyter.currentText()
        print(comboBox_value)
        res = -1
        if comboBox_value == '转换为LaTeX格式':
            res = 1
        elif comboBox_value == '转换为PDF':
            res = 2
        elif comboBox_value == '转换为Markdown':
            res = 3
        elif comboBox_value == '转换为HTML':
            res = 4
        elif comboBox_value == '转换为Python脚本':
            res = 5
        else:
            res = -1
        return res

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

    def inputJupyter(self):
        # 打开一个QFileDialog并获取用户选择的文件路径
        filepath, _ = QFileDialog.getOpenFileName(filter="Jupyter Notebook (*.ipynb)")
        if filepath:
            self.Jupyter_path = filepath
            # 获取文件全名
            self.basename = os.path.basename(filepath)
            # 获取文件名
            self.filename, _ = os.path.splitext(self.basename)
            # 删除扩展名前的点
            self.extension_name = '.ipynb'
            self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '导入Jupyter文件成功！', self.button_input)

    # 打开文件夹的方法
    def open_folder(self):
        path = 'output/Jupyter_Processing'
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    # 一键清理生成的文件
    def clear_files(self):
        folders = ['output/Jupyter_Processing/LaTeX/',
                   'output/Jupyter_Processing/PDF/',
                   'output/Jupyter_Processing/Markdown/',
                   'output/Jupyter_Processing/HTML/',
                   'output/Jupyter_Processing/Python/']
        for folder in folders:
            # 遍历文件夹中的所有文件和子文件夹
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                # 如果是文件，就删除文件
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # 如果是文件夹，就删除文件夹
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        self.showFlyout_Custom2(InfoBarIcon.SUCCESS, 'SUCCESS', '清理文件成功！', self.button_clear_files)

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
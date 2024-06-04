# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF


from .gallery_interface import GalleryInterface # 图库
from .home_interface import HomeInterface   # 主页-Home
from .Latex_interface import LatexInterface  # Latex公式识别
from .Latex_render import LatexRenderInterface  # Latex公式渲染
from .Time_interface import TimeInterface  # 设置关机时间
from .Jupyter_interface import JupyterInterface  # Jupyter Notebook
from .Toico_interface import ToicoInterface  # 图像转换.ico
from .sort_interface import SortInterface  # 排序文件
from .video_interface import VideoInterface  # 视频处理
from .Audio_interface import AudioInterface  # 音频处理

# from .date_time_interface import DateTimeInterface
# from .dialog_interface import DialogInterface
from .icon_interface import IconInterface
# from .navigation_view_interface import NavigationViewInterface
# from .scroll_interface import ScrollInterface   # 滚动
# from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface # 设置-Setting
# from .text_interface import TextInterface
# from .view_interface import ViewInterface

from ..common.config import SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource

from PyQt5.QtCore import QTimer

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        # 初始化窗口
        self.initWindow()

        # 创建子界面
        self.homeInterface = HomeInterface(self)# 主页-Home
        self.latexInterface = LatexInterface(self)# Latex图像识别
        self.latexrenderInterface = LatexRenderInterface(self)# Latex公式渲染
        self.timeInterface = TimeInterface(self)# 设置关机时间
        self.jupyterInterface = JupyterInterface(self)# Jupyter Notebook
        self.toicoInterface = ToicoInterface(self)# 图像转换.ico
        self.sortInterface = SortInterface(self)# 排序文件
        self.videoInterface = VideoInterface(self)# 视频处理
        self.audioInterface = AudioInterface(self)# 音频处理
        self.settingInterface = SettingInterface(self)
##################### 示例 ######################
        self.iconInterface = IconInterface(self)
        # self.dateTimeInterface = DateTimeInterface(self)
        # self.dialogInterface = DialogInterface(self)
        # self.navigationViewInterface = NavigationViewInterface(self)
        # self.scrollInterface = ScrollInterface(self)
        # self.statusInfoInterface = StatusInfoInterface(self)
        # self.textInterface = TextInterface(self)
        # self.viewInterface = ViewInterface(self)

        # 启用丙烯效果
        self.navigationInterface.setAcrylicEnabled(True)

        # 连接信号和槽
        self.connectSignalToSlot()

        # 添加项目到导航界面
        self.initNavigation()
        # 结束启动屏幕
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        # 连接信号和槽
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # 添加导航项目
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))# 主页-Home
        self.addSubInterface(self.iconInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)# 图标
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.latexInterface, FIF.ALBUM, t.latex, pos)  # Latex图像识别
        self.addSubInterface(self.latexrenderInterface, FIF.QUICK_NOTE, t.latex_render, pos)  # Latex公式渲染
        self.addSubInterface(self.timeInterface, FIF.STOP_WATCH, t.time, pos)  # 设置关机时间
        self.addSubInterface(self.jupyterInterface, FIF.COMMAND_PROMPT, t.jupyter, pos)  # Jupyter Notebook
        self.addSubInterface(self.toicoInterface, FIF.CLEAR_SELECTION, t.toico, pos)  # 图像转换.ico
        self.addSubInterface(self.sortInterface, FIF.MENU, t.sort, pos)  # 排序文件
        self.addSubInterface(self.videoInterface,FIF.VIDEO, t.video, pos) # 视频处理
        self.addSubInterface(self.audioInterface, FIF.MUSIC, t.audio, pos)  # 音频处理

        # self.addSubInterface(self.dateTimeInterface, FIF.DATE_TIME, t.dateTime, pos)    # 日期时间
        # self.addSubInterface(self.dialogInterface, FIF.MESSAGE, t.dialogs, pos)     # 对话框
        # self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos) # 导航视图
        # self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)   # 滚动
        # self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos) # 状态信息
        # self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)    # 文本
        # self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)    # 视图

        # 在底部添加自定义小部件
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Jacky', 'Photos/resource/header/three.png'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 初始化窗口
        ## 设置窗口大小
        ## 1600*900 1120*630 1120*700 1300*800
        self.resize(1300, 800)
        self.setMinimumWidth(760)
        # self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowIcon(QIcon('Photos/resource/header/SZU.png'))  # 设置窗口图标
        self.setWindowTitle('UI_Union')# 设置窗口标题

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))# 设置丙烯效果

        # 创建启动屏幕
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(200, 200))
        self.splashScreen.raise_()

        # 设置延时，单位为毫秒，例如这里设置为 5000 毫秒，即 5 秒
        QTimer.singleShot(800, self.splashScreen.close)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    # 重写关闭事件
    def onSupport(self):
        w = MessageBox(
            '作者：Jacky Ngai',
            'Ciallo！！٩(^ω^*)و',
            self
        )
        w.yesButton.setText('幸福美满！')
        w.cancelButton.setText('恭喜发财!')
        if w.exec():
            SUPPORT_URL2 = 'https://blog.csdn.net/RosmontisJK?spm=1000.2115.3001.5343'
            QDesktopServices.openUrl(QUrl(SUPPORT_URL2))

    # SUPPORT_URL
    # 重写窗口大小改变事件
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ 切换到sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)

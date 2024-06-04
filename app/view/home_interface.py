# coding:utf-8
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLabel, QHBoxLayout

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon, ImageLabel
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet


class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        font = QFont()
        font.setFamily('Comic Sans MS')


        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('Best wishes, my friend', self)
        self.galleryLabel.setAlignment(Qt.AlignLeft)
        self.galleryLabel.setStyleSheet("color: white;")
        self.galleryLabel.setFont(font)
        # self.banner = QPixmap(':/gallery/images/header1.png')
        self.banner = QPixmap('Photos/resource/interface_background/blue.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        CSDN_URL_ngai = "https://blog.csdn.net/RosmontisJK?spm=1000.2115.3001.5343"

        # Top图标1
        self.linkCardView.addCard(
            'photos/resource/header/shake.png',
            self.tr('Jacky'),
            self.tr(
                'The significance of human history lies in inheritance and accumulation.'),
            CSDN_URL_ngai
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # 绘制背景颜色
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        # self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        # 创建首页图片标签
        # self.imageLabel_label = ImageLabel('Photos/interface_background/Vertin2k.jpg')
        self.imageLabel_label = ImageLabel('Photos/resource/header/Alona.jpg')
        self.imageLabel_label.scaledToWidth(300)  # 设置图片的宽度
        self.imageLabel_label.setBorderRadius(5, 5, 5, 5)  # 设置图片的圆角
        self.imageLabel_label.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.imageLabel_label)
        # 让图片居中显示
        self.h_layout_photo = QHBoxLayout()
        self.h_layout_photo.setAlignment(Qt.AlignCenter)
        self.h_layout_photo.addWidget(self.imageLabel_label)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addLayout(self.h_layout_photo)

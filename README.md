# UI_Union开发文档

本项目原作者为Jacky Ngai基于Python-PyQt5-Fluent框架进行创作。


UI_Union是作者本人在本科学习过程中 ，发现很多重复性工作要频繁的写代码解决，于是希望可以将一些功能集成到一个软件中。例如写论文时，有些简单却冗长的LaTex公式，我希望快速的打出来，于是把LaTexOCR放进这个UI中;宿舍断电或出门上课，我想电脑在某个时间自动关机；还有交作业时要把Jupyter文件转成pdf(VScode等自动转换识别不了中文，我解决了这个问题)......

希望你能喜欢这个小软件！本项目不参与任何商业活动，开源免费，如有侵权，我会删除。本人程序开发仍有很大进步空间，请多多包涵！！

目前项目仍在开发中！作者还是本科大学生，程序还不成熟，请多多包涵！！

Github原项目地址：https://github.com/MostimaJK/UI_Union

## 环境配置

### Python Pyqt5-Fluent库安装

```cmd
pip install Pyqt5
pip install "PyQt-Fluent-Widgets[full]"
pip install PyQt5-tools
```

### 第三方库的安装

```
pip install opencv-python
pip install pyperclip
pip install PIL
pip install "pix2tex[gui]"
pip install os
pip install datetime
pip install moviepy
pip install time
pip install pydub
pip install matplotlib
pip install threading
pip install pydub
pip install nbconvert
pip install subprocess
pip install shutil
```

### Latex-OCR模型选择与安装

Latex-OCR的使用依靠神经网络，需要用到两个权重模型，总计115MB。

- weights.pth

- image_resizer.pth

```
pip install "pix2tex[gui]"
```

## 运行程序

安装完上面相关库就可以用python运行`UI_Union.py`文件啦！也可以用`启动UI.bat`运行。

同时，我也提供了`UI_Union.exe`文件位于`Releases`文件夹中，可以直接运行，不需要配置环境。

## 功能介绍

### Latex-OCR数学公式识别

实现将输入的数学公式图片进行Latex识别，将数学公式转换成Latex语言。

![Home](/Photos/sample/Home.png)

### Latex公式渲染

实现实时渲染LaTeX公式，并提供将渲染结果导出为图片的功能。

![LaTexOCR](/Photos/sample/LaTexOCR.png)

### 设置关机时间

实现关机时间的设置和取消关机的指令

![设置关机时间](/Photos/sample/设置关机时间.png)

### Jupyter Notebook

- 将Jupyter转换为LaTeX格式
- 将Jupyter转换为PDF格式
- 将Jupyter转换为Markdown格式
- 将Jupyter转换为HTML
- 将Jupyter转换为Python

![Jupyter转换](/Photos/sample/Jupyter转换.png)

### ico图像格式转换

将任意图像格式转换成.ico文件，用于作为系统程序的图标

![ico图像格式转换](/Photos/sample/ico图像格式转换.png)

### 编号文件

- 重命名文件：编号规律为 01_+自定义文件名，适合对同一系列不同特征的文件进行编号
- 编号并保留文件名：仅在原有文件名最前面家加上编号01_ 、02_、 ……适合对课件、番剧等有主题的文件进行编号
- 仅编号：不保留原有文件名，将所有文件进行编号。

![编号文件](/Photos/sample/编号文件.png)

### 视频处理

- 视频音频提取
- 视频转换成gif
- 视频转换为批量图片
- mkv转换MP4

![视频转换](/Photos/sample/视频转换.png)

### 音频处理

- 音频裁剪
- 音频拼接
- 音频速率调整
- 音频倒放
- 音频转成mp3
- 音频转成wav

![音频转换](/Photos/sample/音频转换.png)

## 打包项目

### Pyinstaller

```
pipenv --python 3.11
pipenv shell
pipenv install pyinstaller
pipenv install opencv-python
pipenv install PIL
pipenv install io
pipenv install os
pipenv install moviepy
pipenv install pix2tex
pipenv install pyperclip
pipenv install pydub

pipenv install Pyqt5
pipenv install "PyQt-Fluent-Widgets[full]"
pipenv install PyQt5-tools

pyinstaller  -D "UI_Union.py" -i "UI.ico" --noconsole --clean
```

## 项目开发板块

### Audio音频处理

**初始化区域**

- 标题、副标题的定义
- 创建控件空间widget设置垂直布局以及参数设置（垂直布局）
- 创建子布局h_layout（水平布局）
- 创建参数子布局h_layout_setting
- 创建音频子布局h_layout_audio

**创建控件区域**

- 导入音频音频A按钮
- 导入音频音频B按钮
- 创建选项下拉框
- 创建导入Apply按钮
- 创建打开文件夹按钮
- 创建查看音频信息按钮A
- 创建查看音频信息按钮B
- 创建音频开始时间输入框
- 创建音频结束时间输入框
- 创建音频速率值输入框

**控件区域布局**

子布局参数设置

将控件添加到相应的布局

各个布局的嵌套

**函数区域**

- Apply函数
- 当下拉框的选项改变时，触发事件（return）
- 导入音频的函数inputAudio_A
- 导入音频的函数inputAudio_B
- 判断是否导入音频A is_inputAudio_A
- 判断是否导入音频B is_inputAudio_B
- 获取输入框的值get_input_box
- 获取输入框的值get_value
- 打开文件夹open_folder
- 浮出警告窗口showFlyout(self,title,content)
- 浮出克制化窗口showFlyout_Custom(self,title,content)
- 浮出克制化窗口showFlyout_Custom2(self,infobaricon,title,content)
- 浮出带有图片和按钮的FlyoutA showComplexFlyout_A
- 浮出带有图片和按钮的FlyoutA showComplexFlyout_B



## Jupyter Notebook配置

1.LaTeX环境/MiKTeX

2.Pandoc(Github)

3.nbconvert库(pip install nbconvert)

4.Playwright(pip install Playwright)
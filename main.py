# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import os
import sys
import time
from random import randrange

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from qtpy import QtCore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from threading import BoundedSemaphore, Lock, Thread
from PyQt5 import QtWidgets
from view.MainWindow import Ui_MainWindow as mainForm

# 全局变量url
url = ""
flag = 0
flag2 = 0


def ManageImages(signal):
    global url
    global flag
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
    chrome_options.add_argument('--window-size=1920,1080')
    # 解决无界面加载问题
    # 创建chrome无界面对象
    driver = webdriver.Chrome(options=chrome_options)

    while (True):
        if flag == 0:
            break
        r = randrange(1, 380)  # 产生一个的随机数
        driver.get("https://interfacelift.com/wallpaper/downloads/downloads/any/index" + str(r) + ".html")

        sections = driver.find_elements(By.XPATH,
                                        '/html/body/div[1]/div[3]/div[2]/div[5]/div[*]/div/div[1]/div[2]/div/a')
        for s in sections:
            signal.acquire()
            url = s.get_property("href")
            print(url)
            signal.release()
            time.sleep(30)

    driver.quit()


def PlayImages(signal):
    global url
    global flag
    options = Options()
    options.page_load_strategy = 'none'
    options.add_argument("--kiosk")  # 加载启动项页面全屏效果，相当于F11。
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  # 禁止谷歌弹出正在被自动化软件控制
    driver2 = webdriver.Chrome(options=options)

    # 摸鱼
    # driver2.get('file:///' + os.path.abspath('updates-master/win10u/index.html'))

    while (True):
        if flag == 0:
            break
        if url != "":
            signal.acquire()
            driver2.get(url)
            url = ""
            signal.release()
        else:
            time.sleep(1)
    driver2.quit()


def PlayImages2():
    global url
    global flag2
    options = Options()
    options.page_load_strategy = 'none'
    options.add_argument("--kiosk")  # 加载启动项页面全屏效果，相当于F11。
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  # 禁止谷歌弹出正在被自动化软件控制
    driver2 = webdriver.Chrome(options=options)

    # 摸鱼
    # driver2.get('file:///' + os.path.abspath('updates-master/win10u/index.html'))
    url = 'file:///' + os.path.abspath('updates-master/win10u/index.html')

    while (True):
        if flag2 == 0:
            break
        if url != "":
            driver2.get(url)
            url = ""
        else:
            time.sleep(1)
    driver2.quit()


class MainWindow(QtWidgets.QMainWindow, mainForm):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._startPos = None
        self._endPos = None
        self._tracking = False

        # 窗体置顶(窗体置顶，仅仅为了方便测试)，去边框
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 窗体透明，控件不透明
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.pushButton.clicked.connect(self.NormalRun)
        self.pushButton_2.clicked.connect(self.FishRun)

    def NormalRun(self):
        global flag
        global flag2

        if flag == 1 and flag2 == 0:
            return

        flag = 1
        flag2 = 0
        self.pushButton.setStyleSheet("color:green;")
        self.pushButton_2.setStyleSheet("color:black;")
        signal = BoundedSemaphore(1)  # 信号量 值为1
        # 启动
        Thread(target=ManageImages, args=(signal,)).start()
        Thread(target=PlayImages, args=(signal,)).start()

    def FishRun(self):
        global flag
        global flag2

        if flag == 0 and flag2 == 1:
            return

        flag = 0
        flag2 = 1
        self.pushButton.setStyleSheet("color:black;")
        self.pushButton_2.setStyleSheet("color:green;")
        # 启动
        Thread(target=PlayImages2).start()

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setWindowOpacity(1)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setWindowOpacity(0.005)
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助

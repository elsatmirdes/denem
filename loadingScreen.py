from PyQt5 import QtWidgets, QtGui, QtCore
import time

class LoadingScreen(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(19, 0, 1450, 721)  # Yükleme ekranı boyutu ve konumu
        self.centerOnScreen()

        self.label = QtWidgets.QLabel('Loading...', self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(0, 0, 500, 500)  # Label boyutu ve konumu

        self.movie = QtGui.QMovie("System_Data/System_Data/ico/loading.gif")  # Animasyonlu bir yükleme gif'i
        self.movie.setScaledSize(QtCore.QSize(40, 40))  # Gif boyutu
        self.movie.frameChanged.connect(self.updateFrame)

        self.movie.start()

        self.label2 = QtWidgets.QLabel('Connecting', self)
        # self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setGeometry(275, 30, 100, 440)  # Label boyutu ve konumu
        self.dot_timer = QtCore.QTimer()

    def centerOnScreen(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def updateFrame(self, frame):
        pixmap = self.movie.currentPixmap()
        self.label.setPixmap(pixmap)
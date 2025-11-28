from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar
from PyQt5.QtGui import QIcon
from backend.MainModel import MainModel

def create_menu_bar(main: QMainWindow, menuBar: QMenuBar, model: MainModel):
    fileMenu = menuBar.addMenu('&File')
    
    exitAction = QAction(QIcon('exit.png'), '&Exit', main)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit application')
    exitAction.triggered.connect(main.close)

    fileMenu.addAction(exitAction)
# main.py
import sys
from PyQt5.QtWidgets import QApplication

print("Running main.py")

from backend.MainModel import MainModel
from frontend.MainWindow import *
from frontend.pages.DemoPage import DemoPage
from frontend.pages.BlankPage import BlankPage
from frontend.pages.ParamListExample import ParamListExample
from frontend.pages.PlotPage import PlotPage
from frontend.pages.Plot3DPage import Plot3DPage

import faulthandler

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('frontend/assets/icon.png'))

    # create a Data Model
    mainModel = MainModel()

    # create pages
    pages = [
        Plot3DPage(),
        DemoPage(),
        BlankPage(),
        ParamListExample(),
        PlotPage()
    ]

    print("Pages created, creating main window")

    ex = MainWindow(pages=pages, model=mainModel, title="App Title")

    faulthandler.enable()
    sys.exit(app.exec_())
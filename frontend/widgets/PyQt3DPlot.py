import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import typing as T

class PyQt3DPlot(QWidget):
    def __init__(self, parent=None):
        super(PyQt3DPlot, self).__init__(parent)

        # Create a GL View widget
        self.w = gl.GLViewWidget()
        self.w.setSizePolicy(pg.QtWidgets.QSizePolicy.Expanding, pg.QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.w.setWindowTitle('3D Plot')
        self.w.setCameraPosition(distance=200, azimuth=-90)

        self.permanent_items = []
        self.items = []

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.w)
        self.setLayout(self.layout)

    def clear(self):
        for item in self.items:
            if item in self.w.items:
                self.w.removeItem(item)
        self.items = []

    def add_grid(self, size=10):
        grid = gl.GLGridItem()
        grid.scale(size, size, 1)
        self.permanent_items.append(grid)

    def show(self):
        for item in self.items:
            self.w.addItem(item)
        for item in self.permanent_items:
            if item not in self.w.items:
                self.w.addItem(item)
        self.w.show()

    def plot_line(self, P0=np.identity(4), P1=np.identity(4), 
                  color=(1, 1, 1, 1), 
                  width=2, 
                  permanent=False,
                  mode: T.Literal['lines', 'line_strip'] = 'lines',
                  alpha=None):
        """
        Plot a line between two transformation matrices P0 and P1.
        """
        line = gl.GLLinePlotItem()
        color = (color[0], color[1], color[2], alpha if alpha is not None else color[3])
        line.setData(pos=np.array([[P0[0, 3], P0[1, 3], P0[2, 3]],
                                   [P1[0, 3], P1[1, 3], P1[2, 3]]]),
                     color=color, width=width, antialias=True, mode=mode)
        if permanent:
            self.permanent_items.append(line)
        else:
            self.items.append(line)


    def plot_axis(self, P0=np.identity(4), name="", length=10, permanent=True, fontsize=10):
        """
        Plot a coordinate system at the given transformation matrix P0 using lines.
        """
        xline = gl.GLLinePlotItem()
        xline.setData(pos=np.array([[0, 0, 0], [length, 0, 0]]), color=pg.glColor('r'), width=2, antialias=True)
        yline = gl.GLLinePlotItem()
        yline.setData(pos=np.array([[0, 0, 0], [0, length, 0]]), color=pg.glColor('g'), width=2, antialias=True)
        zline = gl.GLLinePlotItem()
        zline.setData(pos=np.array([[0, 0, 0], [0, 0, length]]), color=pg.glColor('b'), width=2, antialias=True)

        xlabel = gl.GLTextItem(pos=(length+1, 0, 0), text='X'+name, color=(255, 0, 0, 255), font=QtGui.QFont("Helvetica", fontsize))
        ylabel = gl.GLTextItem(pos=(0, length+1, 0), text='Y'+name, color=(0, 255, 0, 255), font=QtGui.QFont("Helvetica", fontsize))
        zlabel = gl.GLTextItem(pos=(0, 0, length+1), text='Z'+name, color=(0, 0, 255, 255), font=QtGui.QFont("Helvetica", fontsize))

        if not isinstance(P0, np.ndarray):
            P0 = np.identity(4)
        m = pg.Transform3D(P0)
        xline.setTransform(m)
        yline.setTransform(m)
        zline.setTransform(m)
        xlabel.setTransform(m)
        ylabel.setTransform(m)
        zlabel.setTransform(m)

        if permanent:
            self.permanent_items.extend([xline, yline, zline, xlabel, ylabel, zlabel])
        else:
            self.items.extend([xline, yline, zline, xlabel, ylabel, zlabel])
        
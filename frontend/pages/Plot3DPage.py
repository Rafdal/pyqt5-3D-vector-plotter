from frontend.pages.BaseClassPage import BaseClassPage
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QWidget

from frontend.widgets.PyQt3DPlot import PyQt3DPlot
from frontend.widgets.SympyLatexWidget import SympyLatexWidget
from frontend.widgets.BasicWidgets import Slider, Button
from frontend.widgets.DynamicSettingsWidget import DynamicSettingsWidget
from utils.ParamList import ParameterList, NumParam

from backend.math.MathCore import JointChain, DHParams, Line3D

import sympy as sp
import numpy as np

class Plot3DPage(BaseClassPage):
    title = "3D Plot"
    
    def initUI(self, layout):
        renderTexBtn = Button("Render Latex")
        renderTexBtn.clicked.connect(self.render_latex)

        self.paramList = ParameterList()
        self.joints = 0

        self.dynamicSettings = DynamicSettingsWidget(self.paramList, on_edit=self.render, 
                                                     submit_on_slider_move=True,
                                                     enable_scroll_area=False,
                                                     vertical=False)
        self.dynamicSettings.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


        self.latex_widget = SympyLatexWidget()
        self.latex_widget.show()

        self.plot3d_widget = PyQt3DPlot()
        self.plot3d_widget.add_grid(size=10)
        self.plot3d_widget.plot_axis(name="0", length=10, permanent=True)
        self.plot3d_widget.show()

        hlayout = QHBoxLayout()
        hvlayout = QVBoxLayout()
        
        hvlayout.addWidget(renderTexBtn)
        hvlayout.addWidget(self.dynamicSettings)
        hvlayout.addWidget(self.latex_widget)
        hlayout.addWidget(self.plot3d_widget)
        hlayout.addLayout(hvlayout)
        layout.addLayout(hlayout)

        self.add_joint()
        self.add_joint()
        self.dynamicSettings.updateUI(self.paramList)

    def add_joint(self):
        self.paramList.addParameters([
            NumParam(name=f"alfa{self.joints}", text=f"alfa {self.joints}", default=0, step=1, interval=(-180, 180)),
            NumParam(name=f"a{self.joints}", text=f"a {self.joints}", default=0, step=1, interval=(0, 100)),
            NumParam(name=f"tita{self.joints}", text=f"tita {self.joints+1}", default=0, step=1, interval=(-180, 180)),
            NumParam(name=f"d{self.joints}", text=f"d {self.joints+1}", default=0, step=1, interval=(0, 100)),
        ])
        self.joints += 1

    def compute(self):
        chain = JointChain()

        for i in range(self.joints):
            alfa = self.paramList[f"alfa{i}"]
            a = self.paramList[f"a{i}"]
            tita = self.paramList[f"tita{i}"]
            d = self.paramList[f"d{i}"]
            chain.append(DHParams(alfa, a, tita, d))
    
        chain.compute()

        for i, line in enumerate(chain.lines):
            P0 = np.array(line.P0).astype(np.float64)
            P1 = np.array(line.P1).astype(np.float64)
            P2 = np.array(line.P2).astype(np.float64)
            print(f"Line {i}: P0={P0}, P1={P1}, P2={P2}")
            self.plot3d_widget.plot_line(P0=P0, P1=P1, alpha=0.5)
            self.plot3d_widget.plot_line(P0=P1, P1=P2, alpha=0.5)

            self.plot3d_widget.plot_axis(P0=P2, name=f'{i+1}', length=5, permanent=False)

        self.expr = chain.end_effector

    def render_latex(self):
        self.compute()
        self.latex_widget.set_expression(self.expr)
        self.latex_widget.show()

    def render(self):
        self.plot3d_widget.clear()
        self.compute()
        # mat = self.expr.evalf()
        # self.plot3d_widget.plot_axis(P0=mat, name='1', length=10, permanent=False)
        self.plot3d_widget.show()

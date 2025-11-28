from frontend.pages.BaseClassPage import BaseClassPage

from frontend.widgets.MatplotWidget import MatplotWidget, MatplotWidgetSettings

import numpy as np

class PlotPage(BaseClassPage):
    title = "Plot Page"
    # ALWAYS define a title, a initUI method and inherit from BaseClassPage

    def initUI(self, layout):
        # layout is a QVBoxLayout
        self.plot_widget = MatplotWidget(settings=MatplotWidgetSettings())
        layout.addWidget(self.plot_widget)

        time = np.linspace(0, 10, 100)
        amplitude = np.sin(time)

        self.plot_widget.init_plot(time, [amplitude])

        # you can access to the model here and its methods/attributes with self.model
        pass

    def on_tab_focus(self):
        # define what happens when the tab is focused (optional)
        pass

    def on_tab_unfocus(self):
        # define what happens when the tab is unfocused (optional)
        pass
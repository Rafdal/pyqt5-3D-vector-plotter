from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib import rcParams
import numpy as np

from PyQt5.QtCore import Qt
import math

class MatplotWidgetSettings():
    def __init__(self,
                 draggable: bool = True,
                 scaleX: str = 'linear',
                 scaleY: str = 'linear',
                 xlabel: str = '',
                 plotLabels: list[str] = None,
                 yInitRange: float = 20.0,
                 postFix: str = None):
        self.draggable = draggable
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.xlabel = xlabel
        self.plotLabels = plotLabels if plotLabels is not None else []
        self.yInitRange = yInitRange
        self.postFix = postFix

class MatplotWidget(QWidget):
    def __init__(self, parent=None, settings: MatplotWidgetSettings = MatplotWidgetSettings()):
        super(MatplotWidget, self).__init__(parent)

        self.settings = settings

        self.x_max = 0
        self.x_min = 10.0

        self.layout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)
        self.figure.subplots_adjust(top=1.0, right=0.99, bottom=0.18)
        self.ax = self.figure.add_subplot(111)

        self.set_scaleX(self.settings.scaleX)

        self._dragging = False

        if self.settings.postFix != None:
            self.ax.yaxis.set_major_formatter(FuncFormatter(lambda y, t: f'{y:.2f}{self.settings.postFix}'))

        self.ax.grid(True, which='major', axis='both', linestyle='--', linewidth=0.5)

        self.ax.set_xlabel(self.settings.xlabel)

        # set background color DEBUG
        # rcParams['axes.facecolor'] = 'gray'
        # rcParams['figure.facecolor'] = 'gray'

        # Enable dragging and exploration of the plot if requested
        if self.settings.draggable:
            self.canvas.mpl_connect('button_press_event', self.on_press)
            self.canvas.mpl_connect('button_release_event', self.on_release)
            self.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    def set_scaleX(self, scale):
        self.scale = scale
        if scale == 'linear':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_linear))
        elif scale == 'log10':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_log10))
        elif scale == 'log2':
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_log2))
        else:
            raise ValueError(f'Invalid scale: {scale}')
        self.canvas.draw_idle()

    def format_linear(self, x, t):
        # Get the order of magnitude of the value
        if x == 0:
            return '0'
        order = int(np.floor(np.log10(abs(x))))
        # Calculate the number of significant digits to show
        digits = max(0, 2 - order)
        return f'{x:.{digits}f}'

    # Format x-axis tick labels in log scale
    def format_log10(self, exp, tick_number):
        coeff = (10**(exp - int(exp)))
        return f'${coeff:.1f} \\times 10^{{{int(exp)}}}$'
    
    def format_log2(self, exp, tick_number):
        coeff = (2**(exp - int(exp)))
        return f'${coeff:.1f} \\times 2^{{{int(exp)}}}$'

    def on_press(self, event):
        self._dragging = True
        self._x0 = event.xdata
        self._y0 = event.ydata

    def on_release(self, event):
        self._dragging = False

    def draw_x_ticks(self, x):
        x_min = self.x_min
        x_max = self.x_max
        x_range = x_max - x_min
        x_step = x_range / 10.0
        x_ticks = np.arange(x_min, x_max + 0.0001*x_range, x_step)
        self.ax.set_xticks(x_ticks)

        # set x tick labels using format_linear
        if self.scale == 'linear':
            self.ax.set_xticklabels([self.format_linear(x, None) for x in x_ticks])

        # set x limits
        self.ax.set_xlim(x_min - x_range*0.05, x_max + x_range*0.05)


    def init_plot(self, x, yList):
        for y in yList:
            self.plot = self.ax.plot(x, y)[0]

        if self.settings.plotLabels != []:
            self.ax.legend(self.settings.plotLabels, loc='upper right', fontsize=12)
        
        # check y limits range
        y_range = self.ax.get_ylim()[1] - self.ax.get_ylim()[0]
        if y_range < self.settings.yInitRange:
            # set y limits vertically centered to the plot with range of 20
            y_center = (self.ax.get_ylim()[0] + self.ax.get_ylim()[1]) / 2.0
            self.ax.set_ylim(y_center - self.settings.yInitRange/2.0, y_center + self.settings.yInitRange/2.0)

        # save initial limits
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

        self.x_min = self.initial_xlim[0]
        self.x_max = self.initial_xlim[1]

        self.ax.axhline(y=0, color='black', linewidth=1.0, alpha=0.5, zorder=2)

        # redraw plot
        self.canvas.draw_idle()

    def update_plot(self, x, yList):
        self.x_min = np.min(x)
        self.x_max = np.max(x)
        for i, y in enumerate(yList):
            if i < len(self.ax.lines):
                self.ax.lines[i].set_xdata(x)
                self.ax.lines[i].set_ydata(y)
            else:
                self.ax.plot(x, y)

        if self.settings.plotLabels != []:
            self.ax.legend(self.settings.plotLabels, loc='upper right', fontsize=12)

        self.canvas.draw_idle()

    def on_motion(self, event):
        if event is None:
            return
        if event.xdata is None or event.ydata is None:
            return
        if not self._dragging:
            return
    
        if event.button is MouseButton.RIGHT:
            dx = event.xdata - self._x0
            dy = event.ydata - self._y0

            self.ax.set_xlim(self.ax.get_xlim() - dx)
            self.ax.set_ylim(self.ax.get_ylim() - dy)
            self.canvas.draw_idle()
            return

        if event.button is MouseButton.LEFT:
            dx = event.xdata - self._x0
            dy = event.ydata - self._y0

            # Introduce a scaling sensitivity factor
            scaling_factor = 0.2

            # Calculate scaling based on mouse movement and sensitivity
            scale_x = 1 - scaling_factor * dx / (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
            scale_y = 1 - scaling_factor * dy / (self.ax.get_ylim()[1] - self.ax.get_ylim()[0])

            # Ensure scaling is proportional and centered around the mouse pointer
            self.ax.set_xlim(self._x0 - (self._x0 - self.ax.get_xlim()[0]) * scale_x,
                             self._x0 + (self.ax.get_xlim()[1] - self._x0) * scale_x)
            self.ax.set_ylim(self._y0 - (self._y0 - self.ax.get_ylim()[0]) * scale_y,
                             self._y0 + (self.ax.get_ylim()[1] - self._y0) * scale_y)
            self.canvas.draw_idle()

    def on_scroll(self, event):
        if event.button == 'up':
            # Zoom in
            scale_factor = 1 / 1.2

        elif event.button == 'down':
            # Zoom out
            scale_factor = 1.2
        else:
            # Ignore other buttons
            return

        x_range = self.ax.get_xlim()
        y_range = self.ax.get_ylim()

        x_center = (x_range[0] + x_range[1]) / 2
        y_center = (y_range[0] + y_range[1]) / 2

        x_new_range = (x_range[0] - x_center) * scale_factor + x_center, (x_range[1] - x_center) * scale_factor + x_center
        y_new_range = (y_range[0] - y_center) * scale_factor + y_center, (y_range[1] - y_center) * scale_factor + y_center

        self.ax.set_xlim(x_new_range[0], x_new_range[1])
        self.ax.set_ylim(y_new_range[0], y_new_range[1])
        self.canvas.draw_idle()

    def autoscale_x(self):
        # Get the x data from the plot
        x_range = self.x_max - self.x_min
        x_margin = x_range * 0.02
        self.ax.set_xlim(self.x_min - x_margin, self.x_max + x_margin)

        # Redraw the canvas
        self.canvas.draw_idle()

    def autoscale_y(self):
        # Get the y data from the plot
        y_data = []
        for line in self.ax.lines:
            y_data.extend(line.get_ydata())

        # Set the y axis limits based on the data range
        if y_data:
            # remove Inf or NaN
            y_data = [y for y in y_data if not math.isnan(y) and not math.isinf(y)]
            if(len(y_data) >= 5):
                y_min = min(y_data)
                y_max = max(y_data)
                y_range = y_max - y_min
                y_margin = y_range * 0.1
                self.ax.set_ylim(y_min - y_margin, y_max + y_margin)

        # Redraw the canvas
        self.canvas.draw_idle()
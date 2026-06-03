import numpy as np

from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.PyQt3DPlot import PyQt3DPlot
from frontend.widgets.DynamicSettingsWidget import DynamicSettingsWidget

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QWidget

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.ParamList import ParameterList, NumParam, BoolParam


class EMWavePage(BaseClassPage):
    title = "EM Waves"

    def initUI(self, layout):
        self.omega = 1.0  # Shared angular frequency for all waves.

        self.paramList = ParameterList()
        self.paramList.addParameters([
            NumParam(name="t", text="time", default=0, step=1, interval=(0, 360)),
            NumParam(name="z_max", text="z max", default=0.1, step=0.1, interval=(0.1, 80)),

            NumParam(name="alpha_1", text="Wave 1 alpha (deg)", default=0, step=15, interval=(0, 360)),

            NumParam(name="E0_2", text="Wave 2 E0", default=1.0, step=0.1, interval=(0, 10)),
            NumParam(name="beta_2", text="Wave 2 beta", default=1.0, step=0.1, interval=(0.1, 10.0)),
            NumParam(name="alpha_2", text="Wave 2 alpha (deg)", default=90, step=15, interval=(0, 360)),
            NumParam(name="phi_2", text="Wave 2 phase (deg)", default=0, step=15, interval=(0, 360)),

            BoolParam(name="show_w2", text="Show Wave 2", default=True),
            BoolParam(name="show_sum", text="Show Sum", default=True),
        ])

        self.dynamicSettings = DynamicSettingsWidget(
            self.paramList,
            on_edit=self.update_plot,
            submit_on_slider_move=True,
            enable_scroll_area=True,
            vertical=True,
        )
        self.dynamicSettings.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.plot3d_widget = PyQt3DPlot()
        self.plot3d_widget.add_grid(size=2)
        # self.plot3d_widget.plot_axis(name="", length=5, permanent=True)
        self.plot3d_widget.w.setCameraPosition(distance=55, azimuth=45, elevation=18)

        self.polarization_widget = QWidget()
        pol_layout = QVBoxLayout(self.polarization_widget)
        pol_layout.setContentsMargins(0, 0, 0, 0)
        pol_layout.setSpacing(0)
        self.pol_figure = Figure(figsize=(3.8, 3.0))
        self.pol_canvas = FigureCanvas(self.pol_figure)
        self.pol_ax = self.pol_figure.add_subplot(111)
        pol_layout.addWidget(self.pol_canvas)
        self.polarization_widget.setMinimumHeight(220)

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.dynamicSettings)
        right_panel.addWidget(self.polarization_widget)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.plot3d_widget)
        hlayout.addLayout(right_panel)
        layout.addLayout(hlayout)

        self.update_plot()

    def compute_wave(self, E0, beta, alpha_deg, phi_deg, t_deg, z_values):
        t_rad = np.deg2rad(t_deg)
        alpha_rad = np.deg2rad(alpha_deg)
        phi_rad = np.deg2rad(phi_deg)

        magnitude = E0 * np.cos(self.omega * t_rad - beta * z_values + phi_rad)
        ex = magnitude * np.cos(alpha_rad)
        ey = magnitude * np.sin(alpha_rad)
        return ex, ey

    def _build_vectors(self, ex, ey, z_values):
        starts = np.column_stack((np.zeros_like(z_values), np.zeros_like(z_values), z_values))
        ends = np.column_stack((ex, ey, z_values))
        return starts, ends

    def _build_curve(self, ex, ey, z_values):
        return np.column_stack((ex, ey, z_values))

    def _plot_signal(self, ex, ey, z_values, color, width_line=2, width_vector=3):
        curve = self._build_curve(ex, ey, z_values)
        self.plot3d_widget.plot_line_strip(curve, color=color, width=width_line)

        # Keep a single representative vector at z=0.
        starts, ends = self._build_vectors(ex[:1], ey[:1], z_values[:1])
        self.plot3d_widget.plot_vectors(starts, ends, color=color, width=width_vector)

    def _plot_polarization_xy(self, t_deg):
        t_values = np.linspace(0.0, 360.0, 240)
        z0 = np.zeros_like(t_values)

        ex1_curve, ey1_curve = self.compute_wave(
            E0=1.0,
            beta=1.0,
            alpha_deg=self.paramList["alpha_1"],
            phi_deg=0,
            t_deg=t_values,
            z_values=z0,
        )
        ex1_now, ey1_now = self.compute_wave(
            E0=1.0,
            beta=1.0,
            alpha_deg=self.paramList["alpha_1"],
            phi_deg=0,
            t_deg=t_deg,
            z_values=np.array([0.0]),
        )

        ex2_curve, ey2_curve = self.compute_wave(
            E0=self.paramList["E0_2"],
            beta=self.paramList["beta_2"],
            alpha_deg=self.paramList["alpha_2"],
            phi_deg=self.paramList["phi_2"],
            t_deg=t_values,
            z_values=z0,
        )
        ex2_now, ey2_now = self.compute_wave(
            E0=self.paramList["E0_2"],
            beta=self.paramList["beta_2"],
            alpha_deg=self.paramList["alpha_2"],
            phi_deg=self.paramList["phi_2"],
            t_deg=t_deg,
            z_values=np.array([0.0]),
        )

        ex_sum_curve = ex1_curve + ex2_curve
        ey_sum_curve = ey1_curve + ey2_curve
        ex_sum_now = ex1_now + ex2_now
        ey_sum_now = ey1_now + ey2_now

        self.pol_ax.clear()
        self.pol_ax.axhline(0, color='0.4', linewidth=0.8)
        self.pol_ax.axvline(0, color='0.4', linewidth=0.8)
        # self.pol_ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
        # Display convention: horizontal axis is Y (right), vertical axis is X (up).
        self.pol_ax.set_xlabel('Ey')
        self.pol_ax.set_ylabel('Ex')
        self.pol_ax.set_title('Polarization Plane (y right, x up, z in)')

        self.pol_ax.plot(ey1_curve, ex1_curve, color=(1.0, 0.0, 0.0), linewidth=1.6, linestyle='--', label='Wave 1')
        self.pol_ax.quiver(0, 0, ey1_now[0], ex1_now[0], angles='xy', scale_units='xy', scale=1,
                           color=(1.0, 0.0, 0.0), width=0.007)

        if self.paramList["show_w2"]:
            self.pol_ax.plot(ey2_curve, ex2_curve, color=(0, 1, 0), linewidth=1.6, linestyle='--', label='Wave 2')
            self.pol_ax.quiver(0, 0, ey2_now[0], ex2_now[0], angles='xy', scale_units='xy', scale=1,
                               color=(0.0, 1.0, 0.0), width=0.007)

        if self.paramList["show_sum"]:
            self.pol_ax.plot(ey_sum_curve, ex_sum_curve, color=(0.0, 0.0, 1.0), linewidth=2.0, label='Sum')
            self.pol_ax.quiver(0, 0, ey_sum_now[0], ex_sum_now[0], angles='xy', scale_units='xy', scale=1,
                               color=(0.0, 0.0, 1.0), width=0.009)

        max_abs = np.max(np.abs(np.concatenate([
            ex1_curve, ey1_curve,
            ex2_curve, ey2_curve,
            ex_sum_curve, ey_sum_curve
        ])))
        lim = max(1.5, float(max_abs) * 1.15)
        self.pol_ax.set_xlim(-lim, lim)
        self.pol_ax.set_ylim(-lim, lim)
        self.pol_ax.set_aspect('equal', adjustable='box')
        self.pol_ax.legend(loc='upper right', fontsize=8)
        self.pol_canvas.draw_idle()

    def update_plot(self):
        self.plot3d_widget.clear()

        t = self.paramList["t"]
        z_max = self.paramList["z_max"]
        n_pts = 300
        z_values = np.linspace(0.0, float(z_max), n_pts)

        ex1, ey1 = self.compute_wave(
            E0=1.0,
            beta=1.0,
            alpha_deg=self.paramList["alpha_1"],
            phi_deg=0,
            t_deg=t,
            z_values=z_values,
        )

        ex2, ey2 = self.compute_wave(
            E0=self.paramList["E0_2"],
            beta=self.paramList["beta_2"],
            alpha_deg=self.paramList["alpha_2"],
            phi_deg=self.paramList["phi_2"],
            t_deg=t,
            z_values=z_values,
        )

        self._plot_signal(ex1, ey1, z_values, color=(1.0, 0.0, 0.0, 1.0), width_line=2, width_vector=3)

        if self.paramList["show_w2"]:
            self._plot_signal(ex2, ey2, z_values, color=(0.0, 1.0, 0.0, 1.0), width_line=2, width_vector=3)

        if self.paramList["show_sum"]:
            ex_sum = ex1 + ex2
            ey_sum = ey1 + ey2
            self._plot_signal(ex_sum, ey_sum, z_values, color=(1.0, 1.0, 0.0, 1.0), width_line=3, width_vector=4)

        self.plot3d_widget.show()
        self._plot_polarization_xy(t)

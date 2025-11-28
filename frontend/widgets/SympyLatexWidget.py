from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer
import numpy as np
import sympy as sp

MATHJAX_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <script type="text/javascript" id="MathJax-script"
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
  </script>
  <style>
    body{{margin:0;padding:6px;background:#f7f7f7;display:flex;justify-content:center;}}
    #mathjax-container{{display:inline-block;}}
  </style>
</head>
<body><div id="mathjax-container">$$ {latex} $$</div></body>
</html>"""

class SympyLatexWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expr = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.web = QWebEngineView(self)
        self.web.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.web.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.web)
        self.setLayout(layout)

        self._probe_timer = QTimer(self)
        self._probe_timer.setInterval(40)
        self._probe_timer.timeout.connect(self._probe_mathjax_size)
        self._probe_attempts = 0

    def set_expression(self, expr: sp.Expr, symbol: sp.Symbol = None):
        self.expr = expr
        self._update_latex()

    def _probe_mathjax_size(self):
        js = """
        (function() {
            const node = document.getElementById('mathjax-container');
            if (!node) { return null; }
            const rect = node.getBoundingClientRect();
            if (!rect.width || !rect.height) { return null; }
            return {width: rect.width, height: rect.height};
        })();
        """
        self.web.page().runJavaScript(js, self._apply_size)

    def _apply_size(self, size):
        if not size:
            self._probe_attempts += 1
            if self._probe_attempts > 80:
                self._probe_timer.stop()
            return

        self._probe_timer.stop()
        padding = 12
        new_height = int(size["height"] + padding)
        new_width = int(size["width"] + padding)
        self.web.setMinimumHeight(new_height)
        self.web.setMaximumHeight(new_height)
        self.web.setMinimumWidth(min(new_width, 1200))
        self.updateGeometry()

    def _update_latex(self):
        latex_src = sp.latex(self.expr)
        self.web.setHtml(MATHJAX_HTML.format(latex=latex_src))
        self.web.show()
        self._probe_attempts = 0
        self._probe_timer.start()
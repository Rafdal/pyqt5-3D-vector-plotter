from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from frontend.pages.BaseClassPage import BaseClassPage
from frontend.widgets.BasicWidgets import Button

class DemoPage(BaseClassPage):
    title = "Demo Page"

    def initUI(self, layout):
        hlayout = QHBoxLayout()

        # Add a QPushButton
        button = QPushButton("Click me!")
        button.clicked.connect(self.on_button_click)

        # Add a custom (round) Button
        customButton = Button("Custom Button", on_click=lambda: print("Custom button clicked"))

        # Add a label
        self.label = QLabel("Count: 0")

        # Set layouts
        hlayout.addWidget(button)
        hlayout.addWidget(customButton)
        layout.addLayout(hlayout)
        layout.addWidget(self.label)

    def on_button_click(self):
        print("Button clicked")
        self.model.increment_count()
        self.label.setText(f"Count: {self.model.count}")
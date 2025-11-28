from frontend.pages.BaseClassPage import BaseClassPage

from PyQt5.QtWidgets import QLabel

from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam
from frontend.widgets.DynamicSettingsWidget import DynamicSettingsWidget

class ParamListExample(BaseClassPage):
    title = "ParamList Example"

    def initUI(self, layout):
        layout.addWidget(QLabel("ParameterList and DynamicSettingsWidget usage example"))
        layout.addSpacing(10)
        layout.addWidget(QLabel("These tools are useful for creating input UI directly from data structures containing parameters in various types like numbers, text, choices, etc."))
        layout.addWidget(QLabel("Don't worry about the UI, just define the data structures and let the tools handle the rest."))
        layout.addSpacing(20)

        # Normally, you should define a ParameterList object in your Model, not in the Page. 
        # But for this example, we will define it here
        self.paramList = ParameterList([
            NumParam("num1", interval=(-100, 100), step=1, value=0, text="Num parameter 1"),
            NumParam("num2", interval=(-100, 100), step=1, value=0, text="Num parameter 2"),
            ChoiceParam("operator", options=["Add", "Sub", "Mul", "Div"], value="Add", text="Choice parameter"),
            BoolParam("bool1", value=True, text="Bool parameter"),
            TextParam("text1", value="", text="Text parameter"),
            TextParam("text2", value="", text="Text parameter with regex", regex="^$|^[0-9]*$"),
            ConstParam("const1", value="constant value", text="Constant parameter")
        ])

        # Create a DynamicSettingsWidget with the ParameterList
        self.dynamicSettingsWidget = DynamicSettingsWidget(self.paramList, 
                                                           title="Math Operation Settings",
                                                           on_edit=self.on_param_edit,
                                                           submit_on_slider_move=True)

        # Show the result of the math operation in a QLabel
        self.resultLabel = QLabel("Result: 0")

        layout.addWidget(self.dynamicSettingsWidget)
        layout.addWidget(self.resultLabel)

    def on_param_edit(self):
        # This method is called when a parameter is changed
        # You can use the updated parameters from self.paramList
        num1 = self.paramList["num1"]
        num2 = self.paramList["num2"]
        operator = self.paramList["operator"]

        # This kind of scripts should be in the Model, not in the Page
        if self.paramList["bool1"]:
            match operator:
                case "Add":
                    result = num1 + num2
                case "Sub":
                    result = num1 - num2
                case "Mul":
                    result = num1 * num2
                case "Div":
                    result = num1 // num2 if num2 != 0 else "Division by zero"

            self.resultLabel.setText(f"Result: {result}")
        else:
            self.resultLabel.setText("Result: Math operation disabled")
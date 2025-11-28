from utils.ParamList import ParameterList, NumParam, BoolParam, TextParam, ChoiceParam, ConstParam

class MainModel:

    # Model attributes
    count = 0

    # Initialization of Model members
    def __init__(self) -> None:
        pass

    # Model methods
    def increment_count(self):
        self.count += 1
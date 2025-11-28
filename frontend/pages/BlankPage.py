from frontend.pages.BaseClassPage import BaseClassPage

class BlankPage(BaseClassPage):
    title = "Blank Page"
    # ALWAYS define a title, a initUI method and inherit from BaseClassPage

    def initUI(self, layout):
        # layout is a QVBoxLayout
        # you can access to the model here and its methods/attributes with self.model
        pass

    def on_tab_focus(self):
        # define what happens when the tab is focused (optional)
        pass

    def on_tab_unfocus(self):
        # define what happens when the tab is unfocused (optional)
        pass
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MainAppLayout(BoxLayout):
    pass


class TurnBasedCardGameApp(App):
    def build(self):
        return MainAppLayout()


if __name__ == "__main__":
    TurnBasedCardGameApp().run()

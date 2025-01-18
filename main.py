import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=20, padding=50)

        welcome_label = Label(text="Shadow Arena: Card Wars", font_size=32)
        play_button = Button(text="Play", font_size=24, size_hint=(0.5, 0.2))
        play_button.bind(on_press=self.start_game)

        layout.add_widget(welcome_label)
        layout.add_widget(play_button)
        self.add_widget(layout)

    def start_game(self, instance):
        """เปลี่ยนไปยังหน้าจอเกม"""
        self.manager.current = "game"


class TurnBasedCardGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = TurnBasedCardGame()
        self.add_widget(self.layout)


class TurnBasedCardGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # พลังชีวิตและสถานะ
        self.player_hp = 100
        self.enemy_hp = 100
        self.player_defense = 0
        self.enemy_attack_debuff = 0
        self.score = 0
        self.card_used = False

        # ส่วนแสดง HP ศัตรู
        self.add_widget(Label(text="ENEMY HP", font_size=20))
        self.enemy_hp_bar = ProgressBar(max=100, value=self.enemy_hp)
        self.add_widget(self.enemy_hp_bar)

        # ส่วนแสดง HP ผู้เล่น
        self.add_widget(Label(text="PLAYER HP", font_size=20))
        self.player_hp_bar = ProgressBar(max=100, value=self.player_hp)
        self.add_widget(self.player_hp_bar)

        # ส่วนแสดงคะแนน
        self.score_label = Label(text=f"Score: {self.score}", font_size=20)
        self.add_widget(self.score_label)

        # ส่วนแสดงการ์ดของผู้เล่น
        self.cards_area = BoxLayout(size_hint=(1, 0.6))
        self.add_widget(self.cards_area)

        # ปุ่มสำหรับจบเทิร์น
        self.end_turn_button = Button(
            text="END OF TURN", size_hint=(1, 0.2), font_size=18
        )
        self.end_turn_button.bind(on_press=self.end_turn)
        self.add_widget(self.end_turn_button)

        # สุ่มการ์ดเมื่อเริ่มเกม
        self.generate_cards()

    def generate_cards(self):
        """สุ่มการ์ดและแสดงในพื้นที่การ์ด"""
        self.card_used = False
        self.cards_area.clear_widgets()
        for _ in range(3):
            card_type = random.choice(["ATTACK", "HEAL", "DEFEND", "DEBUFF"])
            card_value = random.randint(5, 20)
            card_text = f"{card_type} {card_value} HP"

            card_button = Button(text=card_text)
            card_button.bind(
                on_press=lambda instance, ct=card_type, cv=card_value: self.use_card(
                    ct, cv
                )
            )
            self.cards_area.add_widget(card_button)

    def show_notification(self, message):
        """แสดงหน้าต่างแจ้งเตือน"""
        popup = Popup(
            title="Notification",
            content=Label(text=message, font_size=20),
            size_hint=(0.6, 0.4),
        )
        popup.open()

    def use_card(self, card_type, card_value):
        """การใช้การ์ด"""
        if self.card_used:
            self.show_notification("You have already used a card this turn!")
            return

        if card_type == "ATTACK":
            self.enemy_hp = max(0, self.enemy_hp - card_value)
            self.enemy_hp_bar.value = self.enemy_hp
            self.score += 10
        elif card_type == "HEAL":
            self.player_hp = min(100, self.player_hp + card_value)
            self.player_hp_bar.value = self.player_hp
            self.score += 5
        elif card_type == "DEFEND":
            self.player_defense = card_value
            self.score -= 2
        elif card_type == "DEBUFF":
            self.enemy_attack_debuff = card_value
            self.score -= 2

        self.update_score()
        self.card_used = True

        if self.player_hp <= 20:
            self.show_notification("Warning: Your HP is critically low!")

        self.check_game_over()

    def enemy_turn(self):
        """เทิร์นของศัตรู"""
        if self.enemy_hp > 0:
            card_type = random.choice(["ATTACK", "HEAL"])
            card_value = random.randint(5, 20)

            if card_type == "ATTACK":
                damage = max(
                    0, card_value - self.player_defense - self.enemy_attack_debuff
                )
                self.player_hp = max(0, self.player_hp - damage)
                self.player_hp_bar.value = self.player_hp
            elif card_type == "HEAL":
                self.enemy_hp = min(100, self.enemy_hp + card_value)
                self.enemy_hp_bar.value = self.enemy_hp

            self.player_defense = 0
            self.enemy_attack_debuff = 0

            self.update_score()
            self.check_game_over()

    def end_turn(self, instance):
        """ฟังก์ชันสำหรับสิ้นสุดเทิร์น"""
        if not self.card_used:
            self.show_notification("Please use a card before ending your turn.")
            return

        self.enemy_turn()
        self.generate_cards()

    def check_game_over(self):
        """ตรวจสอบเงื่อนไขจบเกม"""
        if self.player_hp == 0:
            self.show_game_over("LOSE!")
        elif self.enemy_hp == 0:
            self.show_game_over("WIN!")

    def update_score(self):
        """อัปเดตคะแนนใน UI"""
        self.score_label.text = f"Score: {self.score}"

    def show_game_over(self, result):
        """แสดงข้อความจบเกม"""
        popup = Popup(
            title="GAME OVER",
            content=Label(text=f"{result}\nFinal Score: {self.score}", font_size=24),
            size_hint=(0.6, 0.4),
        )
        popup.open()


class CardGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(TurnBasedCardGameScreen(name="game"))
        return sm


if __name__ == "__main__":
    CardGameApp().run()

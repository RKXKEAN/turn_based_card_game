import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup


class StartScreen(BoxLayout):
    def __init__(self, start_game_callback, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.spacing = 20
        self.padding = [50, 50, 50, 50]  # [left, top, right, bottom]

        # เพิ่ม BoxLayout กลางหน้าจอ
        center_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.5, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # ชื่อเกม
        title_label = Label(
            text="Battle Deck Chronicles",
            font_size=40,
            bold=True,
            color=[1, 1, 1, 1],
            size_hint=(1, 0.5),
        )
        center_layout.add_widget(title_label)

        # ปุ่ม Play
        play_button = Button(
            text="Play",
            size_hint=(1, 0.1),
            font_size=30,
            background_color=[0, 0.5, 1, 1],
            color=[1, 1, 1, 1],
        )
        play_button.bind(on_press=start_game_callback)
        center_layout.add_widget(play_button)

        self.add_widget(center_layout)


class TurnBasedCardGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.player_hp = 100
        self.enemy_hp = 100
        self.player_defense = 0
        self.enemy_attack_debuff = 0
        self.score = 0
        self.card_used = False
        self.special_used = False  # ใช้ Special Attack หรือยัง

        # Enemy HP
        self.add_widget(Label(text="ENEMY HP", font_size=20))
        self.enemy_hp_bar = ProgressBar(max=100, value=self.enemy_hp)
        self.add_widget(self.enemy_hp_bar)

        # Player HP
        self.add_widget(Label(text="PLAYER HP", font_size=20))
        self.player_hp_bar = ProgressBar(max=100, value=self.player_hp)
        self.add_widget(self.player_hp_bar)

        # Score
        self.score_label = Label(text=f"Score: {self.score}", font_size=20)
        self.add_widget(self.score_label)

        # Cards
        self.cards_area = BoxLayout(size_hint=(1, 0.6))
        self.add_widget(self.cards_area)

        # ปุ่ม Special Attack
        self.special_button = Button(
            text="Special Attack",
            size_hint=(1, 0.2),
            font_size=18,
            background_color=[1, 0, 0, 1],
        )
        self.special_button.bind(on_press=self.special_attack)
        self.add_widget(self.special_button)

        # End turn button
        self.end_turn_button = Button(
            text="END OF TURN", size_hint=(1, 0.2), font_size=18
        )
        self.end_turn_button.bind(on_press=self.end_turn)
        self.add_widget(self.end_turn_button)

        self.generate_cards()

    def generate_cards(self):
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
        popup = Popup(
            title="Notification",
            content=Label(text=message, font_size=20),
            size_hint=(0.6, 0.4),
        )
        popup.open()

    def use_card(self, card_type, card_value):
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
        self.check_game_over()

    def special_attack(self, instance):
        if self.special_used:
            self.show_notification("Special Attack already used!")
            return

        self.enemy_hp = max(0, self.enemy_hp - 50)  # ลด HP ศัตรู 50
        self.enemy_hp_bar.value = self.enemy_hp
        self.score += 20  # เพิ่มคะแนน
        self.special_used = True  # เปลี่ยนสถานะให้ใช้ไปแล้ว
        self.update_score()
        self.check_game_over()  # ตรวจสอบว่าชนะเกมหรือไม่

    def enemy_turn(self):
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
        if not self.card_used:
            self.show_notification("Please use a card before ending your turn.")
            return

        self.enemy_turn()
        self.generate_cards()

    def check_game_over(self):
        if self.player_hp == 0:
            self.show_game_over("LOSE!")
        elif self.enemy_hp == 0:
            self.show_game_over("WIN!")
            if self.special_used:
                self.show_notification("Victory with Special Attack!")

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"

    def show_game_over(self, result):
        popup = Popup(
            title="GAME OVER",
            content=Label(text=f"{result}\nFinal Score: {self.score}", font_size=24),
            size_hint=(0.6, 0.4),
        )
        popup.open()


class CardGameApp(App):
    def build(self):
        self.root_widget = BoxLayout()
        self.start_screen = StartScreen(self.start_game)
        self.root_widget.add_widget(self.start_screen)
        return self.root_widget

    def start_game(self, instance):
        self.root_widget.clear_widgets()
        self.root_widget.add_widget(TurnBasedCardGame())


if __name__ == "__main__":
    CardGameApp().run()

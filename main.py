from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.label import Label


class TurnBasedCardGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # แถบพลังชีวิต (HP Bars)
        self.player_hp = 100  # พลังชีวิตของผู้เล่น
        self.enemy_hp = 100  # พลังชีวิตของศัตรู

        # ส่วนแสดง HP ศัตรู
        self.add_widget(Label(text="ENEMY HP", font_size=20))
        self.enemy_hp_bar = ProgressBar(max=100, value=self.enemy_hp)
        self.add_widget(self.enemy_hp_bar)

        # ส่วนแสดง HP ผู้เล่น
        self.add_widget(Label(text="PLAYER HP", font_size=20))
        self.player_hp_bar = ProgressBar(max=100, value=self.player_hp)
        self.add_widget(self.player_hp_bar)

        # ส่วนแสดงการ์ดของผู้เล่น
        self.cards_area = BoxLayout(size_hint=(1, 0.6))
        self.add_widget(self.cards_area)

        # ปุ่มสำหรับจบเทิร์น
        self.end_turn_button = Button(
            text="END OF TURN", size_hint=(1, 0.2), font_size=18
        )
        self.end_turn_button.bind(on_press=self.end_turn)
        self.add_widget(self.end_turn_button)

        self.generate_cards()

    def generate_cards(self):
        """สุ่มการ์ดและแสดงในพื้นที่การ์ด"""
        self.cards_area.clear_widgets()
        for _ in range(3):  # แสดงการ์ด 3 ใบในแต่ละเทิร์น
            card_type = random.choice(["ATTACK", "HEAL"])
            card_value = random.randint(5, 20)
            card_text = f"{card_type} {card_value} HP"

            card_button = Button(text=card_text)
            card_button.bind(
                on_press=lambda instance, ct=card_type, cv=card_value: self.use_card(
                    ct, cv
                )
            )
            self.cards_area.add_widget(card_button)

    def use_card(self, card_type, card_value):
        """การใช้การ์ด"""
        if card_type == "ATTACK":
            # ลด HP ของศัตรู
            self.enemy_hp = max(0, self.enemy_hp - card_value)
            self.enemy_hp_bar.value = self.enemy_hp
            print(f"โจมตีศัตรู: {card_value} HP เหลือ {self.enemy_hp}")
        elif card_type == "HEAL":
            # เพิ่ม HP ของผู้เล่น
            self.player_hp = min(100, self.player_hp + card_value)
            self.player_hp_bar.value = self.player_hp
            print(f"HEAL PLAYER: {card_value} HP {self.player_hp}")

    def end_turn(self, instance):
        # ฟังก์ชันสำหรับสิ้นสุดเทิร์น
        print("END OF TURN! ENEMY ATTACKING...")

        # ตัวอย่างลด HP ของผู้เล่นเมื่อศัตรูโจมตี
        damage = 10
        self.player_hp = max(0, self.player_hp - damage)
        self.player_hp_bar.value = self.player_hp
        print(f"PLAYER TAKE DAMAGE: {damage} HP: {self.player_hp}")

        self.generate_cards()


class CardGameApp(App):
    def build(self):
        return TurnBasedCardGame()


if __name__ == "__main__":
    CardGameApp().run()

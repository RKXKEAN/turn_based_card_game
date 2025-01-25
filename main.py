import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class StartScreen(FloatLayout):  # เปลี่ยนจาก BoxLayout เป็น FloatLayout
    def __init__(self, start_game_callback, **kwargs):
        super().__init__(**kwargs)

        # พื้นหลัง
        background = Image(
            source="809633.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(background)

        # ส่วนกลาง
        center_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.5, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        space_label = Label(
            text="",
            font_size=40,
            bold=True,
            color=[1, 1, 1, 1],
            size_hint=(1, 10),
        )

        center_layout.add_widget(space_label)

        space2_label = Label(
            text="",
            font_size=40,
            bold=True,
            color=[1, 1, 1, 1],
            size_hint=(1, 10),
        )

        center_layout.add_widget(space2_label)
        title_label = Label(
            text="",
            font_size=100,
            bold=True,
            color=[1, 1, 1, 1],
            size_hint=(1, 10),
        )
        center_layout.add_widget(title_label)

        play_button = Button(
            text="[b][i]Play[/i][/b]",
            markup=True,
            size_hint=(1, 5),
            font_size=70,
            pos_hint={"center_x": 0.5, "center_y": -1},
            background_color=[0, 0, 0, 0],
            color=[1, 0.8, 0.3, 0.8],
        )
        play_button.bind(on_press=start_game_callback)
        center_layout.add_widget(play_button)

        self.add_widget(center_layout)


class TurnBasedCardGame(BoxLayout):
    def __init__(self, reset_game_callback, go_to_main_menu_callback, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.reset_game_callback = reset_game_callback
        self.go_to_main_menu_callback = go_to_main_menu_callback

        # Initialize attributes
        self.player_hp = 100
        self.enemy_hp = 100
        self.player_defense = 0
        self.enemy_defense = 0
        self.enemy_attack_debuff = 0
        self.player_attack_buff = 0
        self.enemy_attack_buff = 0
        self.score = 0
        self.card_used = False
        self.special_used = False
        self.reset_game_callback = reset_game_callback
        self.is_paused = False

        # Top-right layout for Pause and Reset buttons
        top_controls = BoxLayout(
            size_hint=(1, 0.4), padding=[10, 10, 10, 5], spacing=10
        )
        self.pause_button = Button(
            text="PAUSE GAME",
            font_size=24,
            background_color=[0.8, 0.8, 0, 1],
            size_hint=(0.2, 1),
        )
        self.pause_button.bind(on_press=self.toggle_pause)
        top_controls.add_widget(self.pause_button)

        self.reset_button = Button(
            text="RESET GAME",
            font_size=24,
            background_color=[0.5, 0.5, 0.5, 1],
            size_hint=(0.2, 1),
        )
        self.reset_button.bind(on_press=self.reset_game)
        top_controls.add_widget(self.reset_button)

        self.main_menu_button = Button(
            text="MAIN MENU",
            font_size=24,
            background_color=[0.2, 0.4, 1, 1],
            size_hint=(0.2, 1),
        )
        self.main_menu_button.bind(on_press=self.go_to_main_menu)
        top_controls.add_widget(self.main_menu_button)

        # Add top controls to the main layout
        self.add_widget(top_controls)

        # Enemy HP
        self.enemy_hp_bar = ProgressBar(
            max=100, value=self.enemy_hp, size_hint=(1, 0.1)
        )
        self.enemy_character = Image(
            source="kk.png",  # เปลี่ยนเป็นชื่อไฟล์ภาพตัวละคร
            size_hint=(None, None),
            size=(150, 150),  # ขนาดของตัวละคร
            pos_hint={"center_x": 0.2, "center_y": 0.5},  # ตำแหน่ง
        )
        self.add_widget(self.enemy_character)
        self.add_widget(self.enemy_hp_bar)

        self.enemy_hp_label = Label(
            text=f"{self.enemy_hp} HP", font_size=18, size_hint=(1, 0.1)
        )
        self.add_widget(self.enemy_hp_label)  # Add enemy HP number

        # Player HP
        self.player_hp_bar = ProgressBar(
            max=100, value=self.player_hp, size_hint=(1, 0.1)
        )

        self.player_hp_label = Label(
            text=f"{self.player_hp} HP", font_size=18, size_hint=(1, 0.1)
        )
        self.player_character = Image(
            source="ll.png",  # เปลี่ยนเป็นชื่อไฟล์ภาพตัวละคร
            size_hint=(None, None),
            size=(150, 150),  # ขนาดของตัวละคร
            pos_hint={"center_x": 0.8, "center_y": 0.5},  # ตำแหน่ง
        )
        self.add_widget(self.player_character)
        self.add_widget(self.player_hp_bar)
        self.add_widget(self.player_hp_label)  # Add player HP number

        # Score
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size=20,
            size_hint=(1, 0.1),
            padding=[10, 10, 10, 10],
        )
        self.add_widget(self.score_label)

        # Cards
        self.cards_area = BoxLayout(
            size_hint=(1, 2),
            padding=[10, 10, 10, 10],
            spacing=20,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.cards_area)

        # Layout for special attack and turn controls
        controls_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.4))

        # Special Attack Button
        self.special_button = Button(
            text="Special Attack",
            size_hint=(1, 2),
            padding=[0, 10, 0, 10],
            font_size=24,
            background_color=[1, 0, 0, 1],
        )
        self.special_button.bind(on_press=self.special_attack)
        controls_layout.add_widget(self.special_button)

        # Layout for Skip Turn and End Turn
        bottom_controls = BoxLayout(
            size_hint=(1, 2),
            spacing=20,
            padding=[10, 10, 10, -10],
        )
        self.skip_button = Button(
            text="SKIP TURN",
            font_size=20,
            background_color=[0.2, 0.6, 0.8, 1],
        )
        self.skip_button.bind(on_press=self.skip_turn)
        bottom_controls.add_widget(self.skip_button)

        self.end_turn_button = Button(
            text="END OF TURN",
            font_size=20,
            background_color=[0.1, 0.7, 0.3, 1],
        )
        self.end_turn_button.bind(on_press=self.end_turn)
        bottom_controls.add_widget(self.end_turn_button)

        controls_layout.add_widget(bottom_controls)
        self.add_widget(controls_layout)

        # Log Area
        self.log_area = ScrollView(
            size_hint=(1, 0.5),
        )
        self.log_label = Label(text="", font_size=18, size_hint_y=None, valign="top")
        self.log_label.bind(size=self.update_log_height)
        self.log_area.add_widget(self.log_label)
        self.add_widget(self.log_area)

        self.generate_cards()

    def update_log_height(self, *args):
        self.log_label.height = self.log_label.texture_size[1]
        self.log_label.text_size = (self.log_label.width, None)

    def log_action(self, message):
        self.log_label.text += message + "\n"
        self.log_area.scroll_y = 0  # Always show the latest log

    def toggle_pause(self, instance):
        self.is_paused = not self.is_paused
        status = "Game Paused" if self.is_paused else "Game Resumed"
        self.log_action(status)

    def generate_cards(self):
        if self.is_paused:
            return
        self.card_used = False
        self.cards_area.clear_widgets()
        for _ in range(5):
            card_type = random.choice(["ATTACK", "HEAL", "DEFEND", "DEBUFF", "BUFF"])
            card_value = random.randint(10, 20)
            card_text = f"{card_type} {card_value} "

            if card_type == "ATTACK":
                bg_color = "sword.png"
                text_color = [1, 0, 0, 1]
            elif card_type == "HEAL":
                bg_color = "heal.png"
                text_color = [0, 0, 0, 1]
            elif card_type == "DEFEND":
                bg_color = "sheird.png"
                text_color = [0, 0, 0, 1]
            elif card_type == "DEBUFF":
                bg_color = "debuff.png"
                text_color = [1, 1, 1, 1]
            elif card_type == "BUFF":
                bg_color = "buff.png"
                text_color = [0, 0, 0, 1]

            card_button = Button(
                text=card_text,
                font_size=25,
                background_normal=bg_color,
                background_down=bg_color,
                color=text_color,
                border=[0, 0, 0, 1],
                bold=True,
            )
            card_button.bind(
                on_press=lambda instance, ct=card_type, cv=card_value: self.use_card(
                    ct, cv
                )
            )
            self.cards_area.add_widget(card_button)

    def use_card(self, card_type, card_value):
        if self.card_used or self.is_paused:
            self.log_action("You cannot use a card right now!")
            return
        if self.card_used:
            return
        self.card_used = True

        def apply_effect(button):
            # เปลี่ยนสีพื้นหลังชั่วคราว
            button.background_color = [1, 0.5, 0.5, 1]  # สีชมพู
            anim = Animation(
                size=(button.size[0] + 20, button.size[1] + 20), duration=0.2
            ) + Animation(size=button.size, duration=0.2)
            anim.start(button)

            # กลับมาสู่สีเดิม
            Clock.schedule_once(
                lambda dt: setattr(button, "background_color", [1, 1, 1, 1]), 0.5
            )

        # เพิ่มเอฟเฟกต์ให้กับการ์ดที่กด
        for child in self.cards_area.children:
            if f"{card_type} {card_value} " in child.text:
                apply_effect(child)
        if card_type == "ATTACK":
            self.enemy_hp = max(
                0, self.enemy_hp - (card_value + self.player_attack_buff)
            )
            self.enemy_hp_bar.value = self.enemy_hp
            self.score += 10
            self.log_action(f"Player used ATTACK and dealt {card_value} damage!")
        elif card_type == "HEAL":
            self.player_hp = min(100, self.player_hp + card_value)
            self.player_hp_bar.value = self.player_hp
            self.score += 5
            self.log_action(f"Player used HEAL and recovered {card_value} HP!")
        elif card_type == "DEFEND":
            self.player_defense = card_value
            self.score -= 2
            self.log_action(f"Player used DEFEND to block {card_value} damage!")
        elif card_type == "DEBUFF":
            self.enemy_attack_debuff = card_value
            self.score -= 2
            self.log_action(
                f"Player used DEBUFF to reduce enemy attack by {card_value}!"
            )
        elif card_type == "BUFF":
            self.player_attack_buff = card_value
            self.score += 3
            self.log_action(f"Player used BUFF to increase attack by {card_value}!")

        self.update_score()
        self.card_used = True
        self.update_hp_labels()  # Update HP labels after using a card
        self.check_game_over()

    def special_attack(self, instance):
        if self.special_used:
            self.log_action("Special Attack already used!")
            return

        self.enemy_hp = max(0, self.enemy_hp - 40)
        self.enemy_hp_bar.value = self.enemy_hp
        self.score += 10
        self.special_used = True
        self.log_action("Player used SPECIAL ATTACK and dealt 40 damage!")
        self.update_score()
        self.update_hp_labels()  # Update HP labels after special attack
        self.check_game_over()

    def skip_turn(self, instance):
        if self.is_paused:
            return
        self.log_action("Player skipped their turn!")
        self.card_used = True
        self.end_turn(None)

    def enemy_turn(self):
        if self.enemy_hp > 0:
            card_type = random.choice(["ATTACK", "HEAL", "DEFEND", "DEBUFF", "BUFF"])
            card_value = random.randint(30, 40)

            if card_type == "ATTACK":
                damage = max(
                    0,
                    card_value
                    + self.enemy_attack_buff
                    - self.player_defense
                    - self.enemy_attack_debuff,
                )
                self.player_hp = max(0, self.player_hp - damage)
                self.player_hp_bar.value = self.player_hp
                self.log_action(f"Enemy used ATTACK and dealt {damage} damage!")
            elif card_type == "HEAL":
                self.enemy_hp = min(100, self.enemy_hp + card_value)
                self.enemy_hp_bar.value = self.enemy_hp
                self.log_action(f"Enemy used HEAL and recovered {card_value} HP!")
            elif card_type == "DEFEND":
                self.enemy_defense = card_value
                self.log_action(f"Enemy used DEFEND to block {card_value} damage!")
            elif card_type == "DEBUFF":
                self.player_attack_debuff = card_value
                self.log_action(
                    f"Enemy used DEBUFF to reduce player's attack by {card_value}!"
                )
            elif card_type == "BUFF":
                self.enemy_attack_buff = card_value
                self.log_action(f"Enemy used BUFF to increase attack by {card_value}!")

            # Reset player buffs and debuffs at the end of enemy turn
            self.player_defense = 0
            self.enemy_attack_debuff = 0

            self.update_score()
            self.update_hp_labels()  # Update HP labels after enemy's turn
            self.check_game_over()

    def end_turn(self, instance):
        if not self.card_used:
            self.log_action("Please use a card before ending your turn.")
            return

        self.log_action("Player ended their turn.")
        self.enemy_turn()
        self.generate_cards()

    def reset_game(self, instance):
        self.reset_game_callback()

    def go_to_main_menu(self, instance):
        self.go_to_main_menu_callback()

    def check_game_over(self):
        if self.player_hp == 0:
            self.show_popup("Game Over", "You Lose!")
        elif self.enemy_hp == 0:
            self.show_popup("Game Over", "You Win!")

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"

    def update_hp_labels(self):
        """Update HP numbers on the screen."""
        self.enemy_hp_label.text = f"{self.enemy_hp} HP"
        self.player_hp_label.text = f"{self.player_hp} HP"

    def show_popup(self, title, message):

        popup_content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        popup_content.add_widget(Label(text=message, font_size=24))

        close_button = Button(text="Close", size_hint=(1, 0.3), font_size=20)
        close_button.bind(on_press=lambda instance: self.reset_game_callback())
        popup_content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=popup_content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False,
        )

        close_button.bind(on_press=lambda instance: popup.dismiss())
        close_button.bind(on_press=lambda instance: self.reset_game(instance))

        popup.open()


class CardGameApp(App):
    def build(self):
        self.background_music = SoundLoader.load("viking.mp3")
        if self.background_music:
            self.background_music.loop = True  # ทำให้เล่นซ้ำอัตโนมัติ
            self.background_music.volume = 1  # ตั้งระดับเสียง (ค่าระหว่าง 0 ถึง 1)
            self.background_music.play()  # เริ่มเล่นเพลง
        self.root_widget = BoxLayout()
        self.start_screen = StartScreen(self.start_game)
        self.root_widget.add_widget(self.start_screen)
        return self.root_widget

    def start_game(self, instance=None):
        self.root_widget.clear_widgets()
        self.root_widget.add_widget(
            TurnBasedCardGame(self.reset_game, self.go_to_main_menu)
        )

    def go_to_main_menu(self):
        self.root_widget.clear_widgets()
        self.root_widget.add_widget(self.start_screen)

    def reset_game(self):
        self.start_game()

    def on_stop(self):
        # หยุดเพลงเมื่อแอปปิด
        if self.background_music:
            self.background_music.stop()


if __name__ == "__main__":
    CardGameApp().run()

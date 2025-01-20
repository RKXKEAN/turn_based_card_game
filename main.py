import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView


class StartScreen(BoxLayout):
    def __init__(self, start_game_callback, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.spacing = 20
        self.padding = [50, 50, 50, 50]  # [left, top, right, bottom]

        center_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.5, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        title_label = Label(
            text="Battle Deck Chronicles",
            font_size=40,
            bold=True,
            color=[1, 1, 1, 1],
            size_hint=(1, 0.5),
        )
        center_layout.add_widget(title_label)

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
    def __init__(self, reset_game_callback, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.player_hp = 100
        self.enemy_hp = 100
        self.player_defense = 0
        self.enemy_attack_debuff = 0
        self.player_attack_buff = 0
        self.enemy_attack_buff = 0
        self.score = 0
        self.card_used = False
        self.special_used = False
        self.reset_game_callback = reset_game_callback
        self.is_paused = False

        # Top-right layout for Pause and Reset buttons
        top_controls = BoxLayout(size_hint=(1, 0.15), padding=[0, 0, 10, 0], spacing=10)
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

        # Add top controls to the main layout
        self.add_widget(top_controls)

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

        # Layout for special attack and turn controls
        controls_layout = BoxLayout(orientation="vertical", size_hint=(1, 0.4))

        # Special Attack Button
        self.special_button = Button(
            text="Special Attack",
            size_hint=(1, 0.3),
            font_size=24,
            background_color=[1, 0, 0, 1],
        )
        self.special_button.bind(on_press=self.special_attack)
        controls_layout.add_widget(self.special_button)

        # Layout for Skip Turn and End Turn
        bottom_controls = BoxLayout(
            size_hint=(1, 0.3), spacing=20, padding=[10, 0, 10, 0]
        )
        self.skip_button = Button(
            text="SKIP TURN",
            font_size=24,
            background_color=[0.2, 0.6, 0.8, 1],
        )
        self.skip_button.bind(on_press=self.skip_turn)
        bottom_controls.add_widget(self.skip_button)

        self.end_turn_button = Button(
            text="END OF TURN",
            font_size=24,
            background_color=[0.1, 0.7, 0.3, 1],
        )
        self.end_turn_button.bind(on_press=self.end_turn)
        bottom_controls.add_widget(self.end_turn_button)

        controls_layout.add_widget(bottom_controls)
        self.add_widget(controls_layout)

        # Log Area
        self.log_area = ScrollView(size_hint=(1, 0.8))
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
        for _ in range(3):
            card_type = random.choice(["ATTACK", "HEAL", "DEFEND", "DEBUFF", "BUFF"])
            card_value = random.randint(5, 20)
            card_text = f"{card_type} {card_value} HP"

            card_button = Button(text=card_text, font_size=20)
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
        self.check_game_over()

    def special_attack(self, instance):
        if self.special_used:
            self.log_action("Special Attack already used!")
            return

        self.enemy_hp = max(0, self.enemy_hp - 50)
        self.enemy_hp_bar.value = self.enemy_hp
        self.score += 20
        self.special_used = True
        self.log_action("Player used SPECIAL ATTACK and dealt 50 damage!")
        self.update_score()
        self.check_game_over()

    def skip_turn(self, instance):
        if self.is_paused:
            return
        self.log_action("Player skipped their turn!")
        self.card_used = True
        self.end_turn(None)

    def enemy_turn(self):
        if self.enemy_hp > 0:
            card_type = random.choice(["ATTACK", "HEAL", "BUFF"])
            card_value = random.randint(5, 20)

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
            elif card_type == "BUFF":
                self.enemy_attack_buff = card_value
                self.log_action(f"Enemy used BUFF to increase attack by {card_value}!")

            self.player_defense = 0
            self.enemy_attack_debuff = 0

            self.update_score()
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

    def check_game_over(self):
        if self.player_hp == 0:
            self.log_action("Game Over: You Lose!")
        elif self.enemy_hp == 0:
            self.log_action("Game Over: You Win!")

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"


class CardGameApp(App):
    def build(self):
        self.root_widget = BoxLayout()
        self.start_screen = StartScreen(self.start_game)
        self.root_widget.add_widget(self.start_screen)
        return self.root_widget

    def start_game(self, instance=None):
        self.root_widget.clear_widgets()
        self.root_widget.add_widget(TurnBasedCardGame(self.reset_game))

    def reset_game(self):
        self.start_game()


if __name__ == "__main__":
    CardGameApp().run()

# Shadow of War Card Game - Turn-Based Battle

## Introduction
This is a turn-based card game where players battle against an AI-controlled enemy. The game features a variety of cards that allow players to attack, heal, defend, buff, and debuff. The goal is to defeat the enemy while managing your health and resources strategically.

## How to Play
- Start the Game: Click the "Play" button on the main menu to start the game.
- Use Cards: Each turn, you are given 5 random cards. Click on a card to use it.
    Attack: Deal damage to the enemy.
    Heal: Restore your health.
    Defend: Reduce damage taken from the enemy's next attack.
    Buff: Increase your attack power.
    Debuff: Reduce the enemy's attack power.
- Special Attack: Use the "Special Attack" button to deal massive damage to the enemy. This can only be used once per game.
- End Turn: After using a card, click "End Turn" to let the enemy take their turn
- Win/Lose: Defeat the enemy to win the game. If your health reaches 0, you lose.

## Game Features
- Randomized Levels: Each game starts with a randomly selected level, each with its own background and enemy.
- Dynamic Card System: Cards are randomly generated each turn, adding variety to gameplay.
- Enemy AI: The enemy uses random cards to attack, heal, defend, buff, or debuff.
- Score System: Earn points based on your actions during the game.
- Pause and Reset: Pause the game or reset it at any time.

## Function Descriptions
- StartScreen
    Purpose: The main menu screen where players can start the game or view help.
    
    Functions:

        show_help(): Displays a popup with instructions on how to play the game.

- TurnBasedCardGame
    Purpose: The main game screen where players battle the enemy.

    Functions:

        generate_cards(): Randomly generates 5 cards for the player to use.

        use_card(card_type, card_value): Applies the effect of the selected card.

        special_attack(): Deals massive damage to the enemy (can only be used once).

        skip_turn(): Skips the player's turn.

        end_turn(): Ends the player's turn and triggers the enemy's turn.

        enemy_turn(): Simulates the enemy's turn by randomly selecting and using a card.

        check_game_over(): Checks if the player or enemy has been defeated and displays a game over popup.

        reset_game(): Resets the game to its initial state.

        go_to_main_menu(): Returns to the main menu.

- CardGameApp
    Purpose: The main application class that manages the game's lifecycle.

    Functions:

        start_game(): Starts the game by switching to the TurnBasedCardGame screen.

        reset_game(): Resets the game.

        go_to_main_menu(): Returns to the main menu.

        on_stop(): Stops background music when the app is closed.

## Installation
- Install Python: Ensure you have Python 3.x installed on your system.
- Install Kivy: Install the Kivy framework using pip:
    pip install kivy

## Running the Game
- Navigate to the directory containing the game files.
- Run the game using Python:
    python main.py
- Use the mouse to interact with the game.

## Credits
- Developer: ROYKEAN
----------------------------------------------------------------------------------------------------------------------------------------
Enjoy the game! 🎮








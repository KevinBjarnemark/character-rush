"""Modules"""
# Built in libraries
import time
import random
import copy
# Quotes (Usign a third party library)
from assets.python.third_party_api import get_inspirational_quote
# Character groups
from assets.python.character_groups import CHARACTER_GROUPS
# Custom printing functions
from assets.python.printing import neutral_white
from assets.python.printing import random_green_nuance
from assets.python.printing import print_frame
from assets.python.printing import create_empty_lines
from assets.python.printing import sys_print
from assets.python.printing import count_down
# Helper functions
from assets.python.helpers import validated_input
# Static assets
from assets.python.static_assets import GAME_EXPLANATION


class CharacterRush:
    """A game used for memory training"""
    def __init__(self):
        # Default values (entries are named after the given variable)
        # Only add the ones that may need a reset at some point
        self.default_values = {
            "difficulty": {
                "level": 1,
                # CHARACTER_GROUPS entries
                # These will be included in the matrix rain
                "character_entries": [],
            },
            # NOTE this system doesn't support fewer characters
            # than the amount of rows
            "character_inc": 0,
            "frame_count": 0,
        }

        self.printed_frame = ["", "", "", "", ""]
        self.rows = len(self.printed_frame)
        self.columns = 22
        # Set default values
        self.default_values["character_inc"] = self.rows
        self.difficulty = copy.deepcopy(
            self.default_values["difficulty"]
        )
        self.character_inc = copy.deepcopy(
            self.default_values["character_inc"]
        )
        self.frame_count = copy.deepcopy(
            self.default_values["frame_count"]
        )
        self.settings = {
            "speed": "automatic"
        }
        self.speed = 0.7
        self.character_list = []  # List of dictionaries
        self.correct_answer = ""
        self.running = False
        self.first_render = True
        self.browser_terminal = False
        self.quotes = None

    def reset_variables(self):
        """Resets the dynamic variables to their default state"""

        self.difficulty = copy.deepcopy(
            self.default_values["difficulty"]
        )
        self.character_inc = copy.deepcopy(
            self.default_values["character_inc"]
        )
        self.frame_count = copy.deepcopy(
            self.default_values["frame_count"]
        )

    def inspirational_quote(self):
        """Asks the user if they want to include inspirational 
        quotes moving forward and sets the quotes variable 
        appropriately. 
        
        If the user wants to incorporate quotes, 
        it prints the quote with the sys_print function to the 
        terminal. 
        
        NOTE This is using the get_inspirational_quote which uses a 
        third-party library indirectly."""

        if self.quotes is None:
            # Set the quotes variable
            self.quotes = validated_input(
                "Would you like me to provide an inspirational quote\n" 
                "whenever facing adversity? (yes/no)\n",
                self.browser_terminal,
                None,
                True
            )
        if self.quotes is True:
            sys_print(
                get_inspirational_quote() + "\n",
                self.browser_terminal,
                True
            )

    def draw_initial_scene(self):
        """Clears the 'canvas' and 'draws' the initial scene
        without the matrix rain"""

        # Create empty lines
        self.printed_frame = [""] * self.rows

        # Draw the current frame
        self.printed_frame[0] = " " * self.columns
        self.printed_frame[1] = " " * self.columns
        self.printed_frame[2] = "    O                  "
        self.printed_frame[3] = "   /|\\                "
        self.printed_frame[4] = "___/_\\________________"

    def user_answer(self):
        """Ask the user to submit their answer and examine if the
        answer is accepted.

        Returns True if the answer is accepted"""

        neutral_white()
        # Ask the user to type in the correct characters
        user_input_data = {"type": "str", "min": 1}
        user_input = validated_input(
            "Type in all characters loosely eg. ABC123#@\n",
            self.browser_terminal,
            user_input_data)
        result = user_input == self.correct_answer
        # Summarize results
        if result:
            sys_print(
                "\nYou got it right!\n"
                f"Characters memorized: {len(user_input)}\n"
                "Press enter to start the next round", 
                self.browser_terminal,
                True
            )
            input("\n")
            count_down(3, True)
        else:
            sys_print(
                "Oh no, one or more characters were incorrect..\n\n"
                f"Your answer   : {user_input}\n"
                f"Correct answer: {self.correct_answer}\n\n",
                self.browser_terminal,
                True
            )
            # Help the user to maintain a positive mindset with
            # an inspirational quote
            self.inspirational_quote()

            sys_print("Press enter to start over.", self.browser_terminal, True)
            input("\n")
        return result

    def check_user_results(self):
        """Checks the user answer, resets edited variables and
        choses 'path' based on the user results"""

        if self.user_answer():
            self.character_inc += 1  # Introduce more characters
            self.frame_count = 0  # Reset frame_count
            self.build_matrix_rain()
            create_empty_lines(self.rows+1)
            self.running = True  # Run game
        else:
            self.reset_variables()
            create_empty_lines(self.rows+1)
            self.start_game()

    def build_frame(self):
        """Builds the current frame (matrix rain).
        1. Sets the color
        2. Clears the canvas
        3. Calculates where to insert characters
        4. Removes characters that are out of bounds
        5. Increments the frame count
        6. Executes the 'printing of the frame'
        7. Checks the user results when all characters are out of bounds"""

        # Green color effect, throttle when the speed is high
        if self.speed > 0.2:
            if self.frame_count % 5 == 0:
                random_green_nuance()
        else:
            random_green_nuance()

        # Prepare frame printing
        self.draw_initial_scene()

        character_amount = len(self.character_list)
        # Calculate loop length
        # Eg. if it's the 3:rd frame and there are
        # 5 rows, it will only loop 3 times
        loop_length = (
            self.frame_count
            if self.frame_count < self.rows
            else min(character_amount, self.rows)
        )
        # Matrix rain, insert characters at calculaed positions
        for i in range(0, loop_length):
            x = self.character_list[i]["x"]
            # README #2 Simulate 'rain effect' by calculating in reverse
            if self.frame_count < self.rows:
                y = self.frame_count - 1 - i
            else:
                y = self.rows - 1 - i
            # Insert character based on x and y
            sliced = (
                self.printed_frame[y][:x] +
                self.character_list[i]["character"] +
                self.printed_frame[y][x:]
            )
            self.printed_frame[y] = sliced

        # Remove the 'bottom-most' character
        if self.frame_count >= self.rows and character_amount > 0:
            self.character_list.pop(0)

        self.frame_count += 1
        print_frame(self.printed_frame)

        # If all characters are out of bounds
        if character_amount <= 0:
            self.check_user_results()
        else:
            time.sleep(self.speed)  # Limit the 'prinitng speed'

    def configure_settings(self):
        """Ask the user what to do and what settings to use"""

        # Set difficulty
        input_difficulty_data = {"type": "int", "min": 1, "max": 10}
        input_difficulty = validated_input(
            "Set difficulty (type in a number between 1-10)\n",
            self.browser_terminal,
            input_difficulty_data)
        self.difficulty["level"] = input_difficulty
        input_game_speed = validated_input(
            "Would you like to set the game speed automatically? (yes/no)\n",
            self.browser_terminal,
            None,
            True
        )
        # Set the speed variable.
        # Note that the validated_input() forces an approved
        # response, therefore 'elif' is not needed
        self.settings["speed"] = (
            "automatic" if input_game_speed else "manual"
        )
        if self.settings["speed"] == "manual":
            input_manual_speed_data = {"type": "int", "min": 1, "max": 10}
            input_manual_speed = validated_input(
                "Set the speed manually (type in a number between 1-10)\n",
                self.browser_terminal,
                input_manual_speed_data)
            self.speed = 1 / input_manual_speed
        else:
            self.speed = 1 / self.difficulty["level"]

        sys_print(
            "Great! Press enter whenever you're ready to play!",
            self.browser_terminal,
            True
        )
        input("\n")

    def set_browser_terminal_variable(self):
        """Asks the user if they're using the browser terminal
        with limited functionality"""

        setting_browser_terminal = validated_input(
            "Are you running this script in a browser? (yes/no)" +
            "\n(Your answer will optimize rendering)\n",
            False,
            None,
            True
        )
        if setting_browser_terminal:
            self.browser_terminal = False
        else:
            self.browser_terminal = True

    def game_setup(self):
        """Reset game settings and declare new settings"""

        # Show welcome screen
        if self.first_render:
            self.set_browser_terminal_variable()

            sys_print("\nWelcome! \n", self.browser_terminal, True)
            sys_print(
                "This game aims to improve your memorizing skills!\n",
                self.browser_terminal,
                True
            )
            # Ask if the user want to know how the game works
            explain_rules = validated_input(
                "Would you like to know how it works? (yes/no)\n",
                self.browser_terminal,
                None,
                True
            )
            if explain_rules:
                sys_print(GAME_EXPLANATION, self.browser_terminal, True)
                sys_print("Press enter to continue", self.browser_terminal, True)
                input("\n")

            sys_print(
                "Before we start, let's configure some settings.\n",
                self.browser_terminal,
                True
            )

        # Allow the user to configure their settings
        self.configure_settings()
        # Refactor settings
        level = self.difficulty["level"]
        entries = self.difficulty["character_entries"]
        # Add the entries to character groups based on difficulty level
        if level >= 1:
            entries.append("alphabet")
        if level >= 2:
            entries.append("numbers")
        if level >= 4:
            entries.append("symbols_easy")
        if level >= 6:
            entries.append("symbols_intermediate")
        if level >= 9:
            entries.append("symbols_advanced")
        if level >= 10:
            entries.append("symbols_expert")

    def get_group_depth(self, group_length):
        """Returns a reduced length of all character groups based
        on the difficulty[level] setting."""

        # Only allow 20 % of the group's characters to pass through
        if self.difficulty["level"] <= 1:
            return int(group_length*0.3)
        # Allow 50 % to pass through
        elif self.difficulty["level"] <= 3:
            return int(group_length*0.5)
        # Allow 80 % to pass through
        elif self.difficulty["level"] <= 6:
            return int(group_length*0.8)
        # Otherwise, allow all characters to pass through
        return group_length

    def build_matrix_rain(self):
        """Choose which characters that will be included in the matrix rain
        and append those to the character_list"""

        # Reset previously edited variables
        self.character_list = []
        self.correct_answer = ""
        # Get the entries based on the difficulty level
        entries = self.difficulty["character_entries"]
        # Choose random characters in random predetermined entries
        for _ in range(0, max(self.character_inc, self.rows)):
            # Choose a random predetermined entry
            random_entry = entries[random.randrange(len(entries))]
            character_groups_entry = CHARACTER_GROUPS[random_entry]
            # Choose a random character inside that entry
            group_length = self.get_group_depth(len(character_groups_entry))

            random_character = (
                character_groups_entry[random.randrange(group_length)]
            )
            # Mix lower and uppercase letters
            if self.difficulty["level"] > 8 and random_entry == "alphabet":
                if random.randrange(2) == 1:
                    random_character = random_character.upper()
            # Append character and set the x position randomly
            self.character_list.append(
                {
                    "character": random_character,
                    "x": 10 + random.randrange(10)
                }
            )
            self.correct_answer += random_character

    def start_game(self):
        """Starts the game. Here's what it does specifically.
        1. Runs the game_setup and lets the user configure settings.
        2. Builds the matrix rain
        3. Runs the build_frame to 'paint' the matrix rain effect"""

        neutral_white()
        self.game_setup()
        self.build_matrix_rain()
        count_down(3, True)
        create_empty_lines(self.rows+1)
        self.first_render = False
        # Run game
        self.running = True
        while self.running:
            self.build_frame()


game = CharacterRush()
game.start_game()

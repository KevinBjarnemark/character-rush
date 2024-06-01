"""Modules"""
import time
import sys
import random
import copy
from assets.python.character_groups import CHARACTER_GROUPS
from assets.python.printing import neutral_white, random_green_nuance, print_frame
from assets.python.helpers import count_down, validated_input

class CharacterRush:
    """A game used for memory training"""
    def __init__(self):
        # Default values (entries are named after the given variable)
        # Only add the ones that may need a reset at some point
        self.default_values = {
            "difficulty": {
                "level": 1,
                # CHARACTER_GROUPS entries, these will be included in the matrix rain
                "character_entries": [],
            },
            # NOTE this system doesn't support fewer characters than the amount of rows
            "character_inc": 0,
            "frame_count": 0,
        }

        self.printed_frame = ["", "", "", "", ""]
        self.rows = len(self.printed_frame)
        self.columns = 22
        # Set default value
        self.default_values["character_inc"] = self.rows

        self.difficulty = copy.deepcopy(self.default_values["difficulty"])
        self.character_inc = copy.deepcopy(self.default_values["character_inc"])
        self.frame_count = copy.deepcopy(self.default_values["frame_count"])
        self.settings = {
            "speed": "automatic"
        }
        self.speed = 0.7
        self.character_list = [] # List of dictionaries
        self.character_list_copy = [] # List of dictionaries
        self.running = False
        self.first_render = True

    def reset_variables(self):
        """Resets the dynamic variables to their default state"""

        self.difficulty = copy.deepcopy(self.default_values["difficulty"])
        self.character_inc = copy.deepcopy(self.default_values["character_inc"])
        self.frame_count = copy.deepcopy(self.default_values["frame_count"])

    def clear_canvas(self):
        """Clears the 'canvas' by drawing the initial scene"""

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

        neutral_white() # Set terminal color
        user_input_data = {"type": "str", "min": 1}
        user_input = validated_input(
            "Type in all characters loosely eg. ABC123#@\n", 
            user_input_data)
        result = True

        # Calculate result
        correct_answer = ""
        for answer, solution in zip(user_input, self.character_list_copy):
            correct_answer += solution["character"]
            if not answer == solution["character"]:
                result = False

        if result:
            print("\nYou got it right!")
            time.sleep(0.5)
            print(f"Characters memorized: {len(user_input)}\n")
            time.sleep(1)
            input("Press enter to start the next round\n")
            count_down(3, True)
        else:
            print("Oh no, one or more characters were incorrect..\n")
            time.sleep(1)
            print(f"Your answer   : {user_input}")
            print(f"Correct answer: {correct_answer}\n")
            time.sleep(1)
            input("Press enter to start over.\n")
        return result

    def check_user_results(self):
        """Checks the user answer, resets edited variables and 
        choses 'path' based on the user results"""
        if self.user_answer():
            self.character_inc += 1 # Introduce more characters
            self.frame_count = 0 # Reset frame_count
            self.build_matrix_rain()
            self.running = True # Run game
        else:
            self.reset_variables()
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

        # Green color effect
        if self.frame_count % 5 == 0:
            random_green_nuance()

        # Prepare frame printing
        self.clear_canvas()

        character_amount = len(self.character_list)
        # Calculate loop length
        # Eg. if it's the 3:rd frame and there are 5 rows, it will only loop 3 times
        loop_length = self.frame_count if self.frame_count < self.rows else min(character_amount, self.rows)
        # Matrix rain, insert characters at calculaed positions
        for i in range(0, loop_length):
            x = self.character_list[i]["x"]
            # README #1 Simulate 'rain effect' by calculating in reverse
            if self.frame_count < self.rows:
                y = self.frame_count-1 - i
            else:
                y = self.rows-1 - i

            # Insert character based on x and y
            sliced = self.printed_frame[y][:x] + self.character_list[i]["character"] + self.printed_frame[y][x:]
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
            time.sleep(self.speed) # Limit the 'prinitng speed'

    def user_input_welcome(self):
        """Ask the user what to do and what settings to use"""

        if self.first_render:
            print("Welcome!")
            time.sleep(1)
            print("This game aims to improve your memorizing skills!")
            time.sleep(2)
            print("Before we start, let's configure some settings.\n")
            time.sleep(2)

        # Set difficulty
        input_difficulty_data = {"type": "int", "min": 1, "max": 10}
        input_difficulty = validated_input(
            "Set difficulty (type in a number between 1-10)\n", 
            input_difficulty_data)
        self.difficulty["level"] = input_difficulty
        setting_game_speed = {"type": "str", "match_strings": ["yes", "Yes", "no", "No"]}
        input_game_speed = validated_input(
            "Would you like to set the game speed automatically? (yes/no)\n", 
            setting_game_speed)
        # Set the speed variable.
        # Note that the validated_input() forces an approved response, therefore
        # 'elif' is not needed"""
        self.settings["speed"] = "automatic" if input_game_speed == "yes" else "manual"
        if self.settings["speed"] == "manual":
            input_manual_speed_data = {"type": "int", "min": 1, "max": 10}
            input_manual_speed = validated_input(
                "Set the speed manually (type in a number between 1-10)\n", 
                input_manual_speed_data)
            self.speed = 1 / input_manual_speed
        else:
            self.speed = 1 / self.difficulty["level"]

        input("\nGreat! Press enter whenever you're ready to play!\n")

    def game_setup(self):
        """Reset game settings and declare new settings"""

        self.user_input_welcome()

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

    def build_matrix_rain(self):
        """Choose which characters that will be included in the matrix rain 
        and append those to the character_list"""

        # Reset previously edited variable
        self.character_list = []
        # Get the entries based on the difficulty level
        entries = self.difficulty["character_entries"]
        # Choose random characters in random predetermined entries
        for _ in range(0, max(self.character_inc, self.rows)):
            # Choose a random predetermined entry 
            random_entry = entries[random.randrange(len(entries))]
            character_groups_entry = CHARACTER_GROUPS[random_entry]
            # Choose a random character inside that entry
            random_character = character_groups_entry[random.randrange(len(character_groups_entry))]
            # Append character and set the x position randomly
            self.character_list.append({"character": random_character, "x": 10 + random.randrange(10)})
        # Since the character_list will be purged, we need a deep copy for testing the results
        self.character_list_copy = copy.deepcopy(self.character_list)

    def start_game(self):
        """Starts the game. Here's what it does specifically.
        1. Runs the game_setup and lets the user configure settings.
        2. Builds the matrix rain
        3. Runs the build_frame to 'paint' the matrix rain effect"""

        # Create empty lines to draw on
        # TODO Needs attention
        for _ in range(0, len(self.printed_frame)+1):
            sys.stdout.write("\n")

        self.game_setup()
        self.build_matrix_rain()
        count_down(3, True)
        self.first_render = False

        # Run game
        self.running = True
        while self.running:
            self.build_frame()

game = CharacterRush()
game.start_game()

"""Modules"""
import time
import sys
import random
import copy
from assets.python.character_groups import CHARACTER_GROUPS


def count_down(num, starting_in = False):
    """Counts down in seconds"""
    if starting_in:
        print("Starting in...")
    for i in range(0, num):
        print(num - i)
        time.sleep(1)

def neutral_white():
    """Change the terminal color to neutral white"""
    return sys.stdout.write(f"\x1B[38;2;{255};{255};{255}m")

def random_green_nuance():
    """Generates a random nuance of green"""
    r = random.randint(40, 140)
    g = random.randint(200, 250)
    b = random.randint(80, 180)
    return sys.stdout.write(f"\x1B[38;2;{r};{g};{b}m")

def validated_input(message, data=None):
    """
    Validates the user input based on the specified data.
    Note that the input is wrapped in a string to work as expected 
    in the deployed version.

    Parameters:
    message (str): The message to display to the user.
    data (dictionary): The specified rules that should be tested + info. Example below:

    {
        "type" (str): "int", "float", or "str"
        "min" (number): (optional) --> Limit the input 
            When type is str: The amount of characters submitted cannot be below than this number.
            When type is int or float: The submittend number cannot be below that what is specified.
        "max" (number): (optional) --> Limit the input 
            When type is str: The amount of characters submitted cannot be above than this number.
            When type is int or float: The submittend number cannot be above that what is specified.
        "match_strings" (list): (optional) --> Only allow strings that exists in this list
    }

    Returns:
    int, float, or str: The validated user input.
    """

    while True:
        user_input = str(input(message))
        error_message = ""

        try:
            error_message = "" # Reset
            optional_min = data.get("min")
            optional_max = data.get("max")
            is_number = data["type"] == "int" or data["type"] == "float"

            if is_number:
                if data["type"] == "int":
                    user_input = int(user_input)
                elif data["type"] == "float":
                    user_input = float(user_input)

                # Limit the number
                if optional_min is not None:
                    if user_input < optional_min:
                        error_message = f"Input must be at least {optional_min}"
                        raise ValueError()
                if optional_max is not None:
                    if user_input > optional_max:
                        error_message = f"Input must be at most {optional_max}"
                        raise ValueError()
            elif data["type"] == "str":
                optional_match_strings = data.get("match_strings")
                # Match any specified strings
                if optional_match_strings is not None and not user_input in optional_match_strings:
                    # Avoid embedding the alternatives here since they may be 'secret'
                    error_message ="Invalid input: Couln't recognize your input correctly"
                    raise ValueError()
                # Limit the amount of characters
                if optional_min is not None:
                    if len(user_input) < optional_min:
                        error_message = f"Input must be at least {optional_min} character(s)"
                        raise ValueError()
                if optional_max is not None:
                    if len(user_input) > optional_max:
                        error_message = f"Input must be at most {optional_max} character(s)"
                        raise ValueError()
            else:
                # Dev error
                error_message = "(Dev error) Only 'int', 'float' or 'str' are allowed."
                raise ValueError()

            return user_input
        # Avoid exposing the 'dev error' here to keep the UI user-friendly
        except ValueError:
            if len(error_message) > 0:
                print(f"\nInvalid input: {error_message}, please try again.")
            else:
                print("\nInvalid input: Please try again.")

def print_frame(frame_reference):
    """Executes the 'frame printing' after that frame has been built"""

    # Print the current frame
    sys.stdout.write(f"\033[{len(frame_reference)}A") # Move cursor to the top
    for i in range(0, len(frame_reference)):
        sys.stdout.write("\033[K")
        # Print and add a new line
        sys.stdout.write(frame_reference[i] + "\n")
        sys.stdout.flush() # Flush immediately to ensure DOM rendering

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
        self.COLUMNS = 22
        # Set default value
        self.default_values["character_inc"] = self.rows

        self.difficulty = self.default_values["difficulty"]
        self.character_inc = self.default_values["character_inc"]
        self.frame_count = self.default_values["frame_count"]
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

        self.difficulty = self.default_values["difficulty"]
        self.character_inc = self.default_values["character_inc"]
        self.frame_count = self.default_values["frame_count"]

    def clear_canvas(self):
        """Clears the 'canvas' by drawing the initial scene"""

        # Create empty lines
        self.printed_frame = [""] * self.rows

        # Draw the current frame
        self.printed_frame[0] = " " * self.COLUMNS
        self.printed_frame[1] = " " * self.COLUMNS
        self.printed_frame[2] = "    O                  "
        self.printed_frame[3] = "   /|\\                "
        self.printed_frame[4] = "___/_\\________________"

    def user_answer(self):
        """Ask the user to submit their answer and examine if the 
        answer is accepted"""

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
        loop_length = self.frame_count if self.frame_count < self.rows else min(character_amount, self.rows)

        # Matrix rain effect
        for i in range(0, loop_length):
            x = self.character_list[i]["x"]

            # Push characters down to fill empty space
            y = self.rows - i - 1 # Inverse
            if self.frame_count < self.rows and character_amount > 0:
                y = self.frame_count-1 - i

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
            random_entry = entries[random.randrange(len(entries))]
            character_groups_entry = CHARACTER_GROUPS[random_entry]
            random_character = character_groups_entry[random.randrange(len(character_groups_entry))]
            self.character_list.append({"character": random_character, "x": 10 + random.randrange(10)})

        self.character_list_copy = copy.deepcopy(self.character_list)

    def start_game(self):
        """Starts the game. Here's what it does specifically.
        1. Runs the game_setup and lets the user configure settings.
        2. Builds the matrix rain
        3. Runs the build_frame to 'paint' the matrix rain effect"""

        # Create empty lines to draw on
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

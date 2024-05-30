import time
import sys
import random
import copy
from assets.python.character_groups import CHARACTER_GROUPS

"""A dictionary of default values. 
Entries are named after the given variable.
Only add the ones that may need a reset at some point """
default_values = {
    "difficulty": {
        "level": 1,
        # CHARACTER_GROUPS entries, these will be included in the matrix rain
        "character_entries": [], 
    },
    # NOTE this system doesn't support fewer characters than the amount of rows
    "character_inc": 0, # Increased for each 'round'
    "frame_count": 0,
}

printed_frame = ["", "", "", "", ""]
rows = len(printed_frame)
COLUMNS = 22
# Set default value
default_values["character_inc"] = rows

difficulty = default_values["difficulty"]
character_inc = default_values["character_inc"]
frame_count = default_values["frame_count"]
settings = {
    "speed": "automatic"
}
speed = 0.7
character_list = [] # List of dictionaries
character_list_copy = [] # List of dictionaries
running = False
first_render = True

# Helpers
def count_down(num, starting_in = False):
    """Counts down in seconds"""
    if starting_in:
        print("Starting in...")
    for i in range(0, num):
        print(num - i)
        time.sleep(1)

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
        "min" (number): (optional) --> Only allow inputs above this number
        "max" (number): (optional) --> Only allow inputs below this number
        "match_strings" (list): (optional) --> Only allow strings that exists in this list
    }

    Returns:
    int, float, or str: The validated user input.
    """

    while True:
        user_input = str(input(message))

        try:
            is_number = data["type"] == "int" or data["type"] == "float"
            if is_number:
                if data["type"] == "int":
                    user_input = int(user_input)
                elif data["type"] == "float":
                    user_input = float(user_input)

                # Limit to min and max values when the input is a number
                if data["min"] is not None and user_input < data["min"]:
                    raise ValueError(f"Input must be at least {data["min"]}.")
                if data["max"] is not None and user_input > data["max"]:
                    raise ValueError(f"Input must be at most {data["max"]}.")
                
            elif data["type"] == "str":
                # If the input has to match any specified strings
                if data["match_strings"] is not None and user_input in data["match_strings"]:
                    pass
                else:
                    # Avoid embedding the alternatives here since they may be 'secret'
                    raise ValueError("Invalid input: Please try again.")
            else: 
                # Dev error
                raise ValueError("Invalid input type specified. Only 'int', 'float' or 'str' are allowed.")

            return user_input
        
        except ValueError: # Avoid adding 'as e' here to keep the interaction user friendly
            print(f"\nInvalid input: Please try again.")

def reset_variables():
    global default_values, difficulty, character_inc, frame_count

    difficulty = default_values["difficulty"]
    character_inc = default_values["character_inc"]
    frame_count = default_values["frame_count"]

def random_green_nuance():
    """Generates a random nuance of green"""
    r = random.randint(40, 140)
    g = random.randint(200, 250)
    b = random.randint(80, 180)
    return sys.stdout.write(f"\x1B[38;2;{r};{g};{b}m")

def neutral_white():
    """Change the terminal color to neutral white"""
    return sys.stdout.write(f"\x1B[38;2;{255};{255};{255}m")

# Clear the 'canvas'
def clear_canvas():
    """Clears the 'canvas' by drawing the initial scene"""
    global printed_frame
    # Clear the last frame
    printed_frame = [""] * rows
    # Draw the current frame 
    printed_frame[0] = " " * COLUMNS
    printed_frame[1] = " " * COLUMNS
    printed_frame[2] = "    O                  "
    printed_frame[3] = "   /|\\                "
    printed_frame[4] = "___/_\\________________"

def user_answer():
    """Ask the user to submit their answer and examine if the 
    answer is accepted"""
    global character_list_copy, settings
    
    neutral_white()
    user_input = input("Type in all characters loosely eg. ABC123#@\n")
    result = True
    
    # Calculate result
    correct_answer = ""
    for answer, solution in zip(user_input, character_list_copy):
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

def check_user_results():
    """Checks the user answer, resets edited variables and 
    choses 'path' based on the user results"""
    global character_inc, frame_count, running
    if user_answer():
        character_inc += 1 # Introduce more characters
        frame_count = 0 # Reset frame_count
        build_matrix_rain()
        running = True # Run game
    else:
        reset_variables()
        start_game()

def print_frame():
    """Executes the 'frame printing' after that frame has been built"""
    global printed_frame
    # Print the current frame 
    sys.stdout.write(f"\033[{len(printed_frame)}A") # Move cursor to the top
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\033[K")
        # Print and add a new line 
        sys.stdout.write(printed_frame[i] + "\n")
        sys.stdout.flush() # Flush immediately to ensure DOM rendering

def build_frame():
    """Builds the current frame (matrix rain).
    1. Sets the color
    2. Clears the canvas
    3. Calculates where to insert characters
    4. Removes characters that are out of bounds
    5. Increments the frame count 
    6. Executes the 'printing of the frame'
    7. Checks the user results when all characters are out of bounds"""
    global printed_frame, frame_count, character_list, rows, running, character_inc

    # Green color effect
    if frame_count % 5 == 0:
        random_green_nuance()

    # Prepare frame printing
    clear_canvas()
    character_amount = len(character_list)
    # Calculate loop length
    loop_length = frame_count if frame_count < rows else min(character_amount, rows)
    
    # Matrix rain effect
    for i in range(0, loop_length):
        x = character_list[i]["x"]

        # Push characters down to fill empty space
        y = rows - i - 1 # Inverse
        if frame_count < rows and character_amount > 0:
            y = frame_count-1 - i

        # Insert character based on x and y
        sliced = printed_frame[y][:x] + character_list[i]["character"] + printed_frame[y][x:]
        printed_frame[y] = sliced
        
    # Remove the 'bottom-most' character
    if frame_count >= rows and character_amount > 0:
        character_list.pop(0)

    frame_count += 1
    print_frame()

    # If all characters are out of bounds
    if character_amount <= 0:
        check_user_results()
    else:
        time.sleep(speed) # Limit the 'prinitng speed'
    
def user_input_welcome():
    """Ask the user what to do and what settings to use"""
    global difficulty, first_render, speed

    if first_render:
        print("Welcome!")
        time.sleep(1)
        print("This game aims to improve your memorizing skills!")
        time.sleep(2)
        print("Before we start, let's configure some settings.\n")
        time.sleep(2)

    # Set difficulty 
    input_difficulty_data = {"type": "int", "min": 1, "max": 10}
    input_difficulty = validated_input("Set difficulty (type in a number between 1-10)\n", input_difficulty_data)
    difficulty["level"] = input_difficulty
    setting_game_speed = {"type": "str", "match_strings": ["yes", "Yes", "no", "No"]}
    input_game_speed = validated_input("Would you like to set the game speed automatically? (yes/no)\n", setting_game_speed)
    """Set the speed variable.
    Note that the validated_input() forces an approved response, therefore 
    'elif' is not needed""" 
    settings["speed"] = "automatic" if input_game_speed == "yes" else "manual"
    if settings["speed"] == "manual":
        input_manual_speed_data = {"type": "int", "min": 1, "max": 10}
        input_manual_speed = validated_input("Set the speed manually (type in a number between 1-10)\n", input_manual_speed_data)
        speed = 1 / input_manual_speed 
    else:
        speed = 1 / difficulty["level"]  

    input("\nGreat! Press enter whenever you're ready to play!\n")

def game_setup():
    """Reset game settings and declare new settings"""
    global difficulty

    user_input_welcome()

    level = difficulty["level"]
    entries = difficulty["character_entries"]

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

def build_matrix_rain():
    """Choose which characters that will be included in the matrix rain 
    and append those to the character_list"""
    global rows, difficulty, character_list, character_list_copy, character_inc
    
    # Reset previously edited variable
    character_list = []
    # Get the entries based on the difficulty level
    entries = difficulty["character_entries"]
    # Choose random characters in random predetermined entries
    for i in range(0, max(character_inc, rows)): 
        random_entry = entries[random.randrange(len(entries))]
        character_groups_entry = CHARACTER_GROUPS[random_entry]
        random_character = character_groups_entry[random.randrange(len(character_groups_entry))]
        character_list.append({"character": random_character, "x": 10 + random.randrange(10)})
    
    character_list_copy = copy.deepcopy(character_list)

def start_game():
    global printed_frame, frame_count, running, first_render

    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)+1):
        sys.stdout.write("\n")

    game_setup()
    build_matrix_rain()
    count_down(3, True)
    first_render = False

    # Run game
    running = True
    while running:
        build_frame()

start_game()
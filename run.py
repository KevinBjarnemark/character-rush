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
    "character_inc": 0 # Increased for each 'round'
}

printed_frame = ["", "", "", "", ""]
rows = len(printed_frame)
COLUMNS = 22
# Set default value
default_values["character_inc"] = rows

difficulty = default_values["difficulty"]
character_inc = default_values["character_inc"]
settings = {
    "ordered": True # If true, all characters should be memorized in order
}
frame_count = 0
speed = 0.7
character_list = [] # List of dictionaries
character_list_copy = [] # List of dictionaries
running = False

# Helpers
def count_down(num, starting_in = False):
    """Counts down in seconds"""
    if starting_in:
        print("Starting in...")
    for i in range(0, num):
        print(num - i)
        time.sleep(1)

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
    user_answer = str(input("Type in all characters loosely eg. ABC123#@ \n"))
    result = True
    correct_answer = ""

    # Calculate result based on settings 
    if settings["ordered"]:
        for answer, solution in zip(user_answer, character_list_copy):
            correct_answer += solution["character"]
            if not answer == solution["character"]:
                result = False
    else:
        result = all(char["character"] in answer for char in character_list_copy)
    
    if result:
        print("Good work, you got it right! Starting next round...")
        time.sleep(3) # Give the user some time to read
        count_down(3)
    else:
        print("Oh no, one or more characters were incorrect..\n")
        time.sleep(1)
        print(f"Your answer   : {user_answer}")
        print(f"Correct answer: {correct_answer}\n")
        time.sleep(1)
        input("Press enter to start over.")
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
        # TODO Reset game
        print("TODO, reset game")

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
    global difficulty

    print("Welcome!")
    time.sleep(1)
    print("Your mission is to memorize the falling letters.\n")
    time.sleep(2)
    # Set difficulty 
    input_difficulty = int(input("How skilled are you at memorizing? \nType in a number between 1-10\n"))
    difficulty["level"] = input_difficulty
    setting_ordered = str(input("Would you like to momorize the characters in order? (yes/no)\n"))
    settings["ordered"] = True if setting_ordered == "yes" else False
    input("Great! Press enter whenever you're ready to play!")

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
    global printed_frame, frame_count, running

    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)+1):
        sys.stdout.write("\n")

    game_setup()
    build_matrix_rain()
    count_down(3, True)

    # Run game
    running = True
    while running:
        build_frame()

start_game()
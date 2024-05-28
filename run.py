import time
import sys
import random
import copy

# Character groups chosen based on the difficulty level
character_bank = {
    "alphabet": [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
        "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ],
    "numbers": [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ],
    "symbols_easy": [
        "!", "@", "#", "%", ",", ".", "?"
    ],
    "symbols_intermediate": [
        "$", "*", "(", ")", "_", "=", "+", "&", "/"
    ],
    "symbols_advanced": [
        "-", "[", "]", ":"
    ],
    "symbols_expert": [
        "^", "{", "}", ";", "'", "\"", "<", ">", "\\", "|", "~", "`"
    ],
}

difficulty = {
    "level": 1,
    "character_entries": [], # List of allowed entries in character_bank
}
speed = 0.7
character_list = [] # List of dictionaries
character_list_copy = [] # List of dictionaries
printed_frame = ["", "", "", "", ""]
frame_count = 0
rows = len(printed_frame)
COLUMNS = 22
running = False
# NOTE this system doesn't support fewer characters than the amount of rows
character_inc = rows-1 # Increased for each 'cycle'

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
    global character_list_copy
    answer = str(input("Type in all characters loosely eg. ABCD123#% \n"))
    result = all(char["character"] in answer for char in character_list_copy)

    if result:
        print("Good work, you got it right! Starting next round...")
        time.sleep(3) # Give the user some time to read
        count_down(3)
    else:
        print("Oh no, one or more characters were incorrect..")
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
        # TODO Reset game
        print("TODO, reset game")

# Print the current frame
def build_frame():
    """Builds the current frame (matrix rain).
    1. Sets the color
    2. Clears the canvas
    3. Calculates where to insert characters
    4. Removes characters that are out of bounds
    5. Increments the frame count 
    6. Checks the user results when all characters are out of bounds"""
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

    # If all characters are out of bounds
    if character_amount <= 0:
        check_user_results()
    else:
        time.sleep(speed) # Limit the 'prinitng speed'

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

def user_input_welcome():
    """Ask the user what to do and what settings to use"""
    global difficulty

    print("Welcome!") 
    # Choose what to do
    input_what_to_do = int(input("What do you want to do?\n 1. Play memorizing game\n"))
    print("Great!")
    # Choose difficulty 
    input_difficulty = int(input("How skilled are you at memorizing? \nType in a number between 1-10\n"))
    # Set difficulty
    difficulty["level"] = input_difficulty

def game_setup():
    """Reset game settings and declare new settings"""
    global difficulty

    user_input_welcome()

    # Reset edited variables
    difficulty["level"] = 1
    difficulty["character_entries"] = []
    
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
    global character_bank, rows, difficulty, character_list, character_list_copy, character_inc
    # Reset previously edited variable
    character_list = []
    # Get the entries based on the difficulty level
    entries = difficulty["character_entries"]
    # Choose random characters in random predetermined entries
    for i in range(0, max(character_inc, rows)): 
        random_entry = entries[random.randrange(len(entries))]
        character_bank_entry = character_bank[random_entry]
        random_character = character_bank_entry[random.randrange(len(character_bank_entry))]
        character_list.append({"character": random_character, "x": 10 + random.randrange(10)})
    
    character_list_copy = copy.deepcopy(character_list)

def start_game():
    global printed_frame, frame_count, running

    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    game_setup()
    build_matrix_rain()
    count_down(3, True)

    # Run game
    running = True
    while running:
        build_frame()
        print_frame()

start_game()

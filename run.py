import time
import sys
import random
import copy

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
    "level": 10, # Temporary
    "character_entries": [], # List of allowed entries in character_bank
}
character_list = [] # List of dictionaries
character_list_copy = [] # List of dictionaries
STEPS = 22
speed = 0.05
cycle = 0
printed_frame = ["", "", "", "", ""]
frame_count = 0
rows = len(printed_frame)
running = False

# Helpers
def count_down(num):
    for i in range(0, num):
        print(num - i)
        time.sleep(1)

def user_answer():
    global character_list_copy
    answer = str(input("Type in all characters loosely eg. ABCD123#% \n"))
    result = all(char["character"] in answer for char in character_list_copy)

    if result:
        print("Good work, you got it right! Starting next round...")
        time.sleep(3)
        count_down(3)
    else:
        print("Oh no, one or more characters were incorrect..")
        input("Press enter to start over.\n")
    return result

def print_frame():
    global printed_frame, frame_count, character_list, rows, running

    character_amount = len(character_list)

    # Clear the last frame
    printed_frame = [""] * rows
    # Draw the current frame 
    printed_frame[0] = " " * STEPS
    printed_frame[1] = " " * STEPS
    printed_frame[2] = "    O                  "
    printed_frame[3] = "   /|\\                "
    printed_frame[4] = "___/_\\________________"
    
    # Matrix rain
    # Calculate loop length
    loop_length = frame_count if frame_count < rows else min(character_amount, rows)
    for i in range(0, loop_length):
        y = i # Row position
        x = character_list[i]["x"]
        # Push 'left-over' characters down
        if frame_count > rows and character_amount > 0:
            y = rows - i - 1 # Inverse
        # Insert character in based on x and y
        sliced = printed_frame[y][:x] + character_list[i]["character"] + printed_frame[y][x:]
        printed_frame[y] = sliced
        
    # Remove the 'bottom-most' character
    if frame_count >= rows and character_amount > 0:
        character_list.pop(0)

    # Print the current frame 
    sys.stdout.write(f"\033[{len(printed_frame)}A") # Move cursor to the top
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\033[K")
        # Print and add a new line 
        sys.stdout.write(printed_frame[i] + "\n")
        sys.stdout.flush() # Flush immediately to ensure DOM rendering
    
    frame_count += 1
    if character_amount <= 0:
        running = False
        if user_answer():
            build_matrix_rain()
            running = True
        else:
            print("TODO, reset game")

def game_setup():
    global difficulty

    # User interaction
    print("Welcome!") 
    # Choose what to do
    input_what_to_do = int(input("What do you want to do?\n 1. Play memorizing game\n"))
    print("Great!")
    # Choose difficulty 
    input_difficulty = int(input("How skilled are you at memorizing? \nType in a number between 1-10\n"))
    
    # Set difficulty
    difficulty["level"] = input_difficulty

    level = difficulty["level"]
    entries = difficulty["character_entries"]
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
    global printed_frame, character_bank, rows, difficulty, character_list, character_list_copy
    entries = difficulty["character_entries"]

    character_list = [
        {"character": "A", "x": 12},
        {"character": "B", "x": 12},
        {"character": "C", "x": 12},
        {"character": "D", "x": 12},
    ]
    character_list_copy = copy.deepcopy(character_list)

    # Note, this system doesn't support fewer characters than the amount of rows
    """ for i in range(0, max(100, rows)): 
        random_entry = entries[random.randrange(len(entries))]
        character_bank_entry = character_bank[random_entry]
        random_character = character_bank_entry[random.randrange(len(character_bank_entry))]
        character_list.append({"character": random_character, "x": 10 + random.randrange(10)}) """

def start_game():
    global printed_frame, frame_count, running
    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    game_setup()
    build_matrix_rain()
    running = True

    # Game logic
    while running:
        if frame_count % 10 == 0:
            # Set color
            sys.stdout.write(f"\x1B[38;2;{random.randrange(40, 140)};{random.randrange(200, 250)};{random.randrange(80, 180)}m") # RGB color

        print_frame()
        time.sleep(speed)

start_game()
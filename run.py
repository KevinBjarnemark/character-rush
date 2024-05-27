import time
import sys
import random

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
STEPS = 22
speed = 0.05
cycle = 0
printed_frame = ["", "", "", "", ""]
frame_count = 0
rows = len(printed_frame)

def print_frame():
    global printed_frame, frame_count, character_list, rows

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

def game_setup():
    global difficulty

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
    global printed_frame, character_bank, rows, difficulty
    entries = difficulty["character_entries"]
    # Note, this system doesn't support fewer characters than the amount of rows
    for i in range(0, max(100, rows)): 
        random_entry = entries[random.randrange(len(entries))]
        character_bank_entry = character_bank[random_entry]
        random_character = character_bank_entry[random.randrange(len(character_bank_entry))]
        character_list.append({"character": random_character, "x": 10 + random.randrange(10)})

def start_game():
    global printed_frame, frame_count
    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    game_setup()
    build_matrix_rain()

    # Game logic
    while True:
        if frame_count % 10 == 0:
            # Set color
            sys.stdout.write(f"\x1B[38;2;{random.randrange(40, 140)};{random.randrange(200, 250)};{random.randrange(80, 180)}m") # RGB color

        print_frame()
        time.sleep(speed)

start_game()
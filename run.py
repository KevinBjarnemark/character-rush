import time
import random
import sys

CHARACTER_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
STEPS = 20
JUMPING_RANGE = [8, 9, 10]
speed = 0.3
character_index = 20
current_character = "A"
stickman_index = 7
cycle = 0
printed_frame = ["", "", "", "", ""]


def print_frame_old():
    global stickman_index, character_index, current_character

    # Draw the scene (except for bottom row)
    printed_frame = [
        "",
        "",
        "    O  ",
        "   /|\\ ",
        "",
    ]

    printed_frame[4] = ""
    # Draw the scene
    for i in range(0, STEPS):
        if i == 3:
            printed_frame[4] += "/" # Left leg 
        elif i == 5:
            printed_frame[4] += "\\" # Right leg 
        elif i == character_index:
            printed_frame[4] += current_character # Current character
        else:
            printed_frame[4] += "_" # Ground

    # Print the drawn scene (frame)
    for line in printed_frame:
        print(line)

def print_frame():
    global printed_frame, stickman_index, character_index, current_character

    # Draw the current frame 
    sys.stdout.write(f"\033[{5}A") # Move cursor up 5 lines
    for i in range(0, len(printed_frame)+1):
        if i == 0:
           sys.stdout.write("")
        elif i == 2:
            sys.stdout.write("")
        elif i == 3:
            sys.stdout.write("    O")
        elif i == 4:
            sys.stdout.write("   /|\\")
        elif i == 5:
            sys.stdout.write("___/_\\_____________")

        # New line
        sys.stdout.write("\n")

def choose_random_character():
    global current_character, character_index
    current_character = random.choice(CHARACTER_LIST)
    character_index = STEPS # Reset 

def start_game():
    global printed_frame, character_index
    # Set color
    print(f"\x1B[38;2;{100};{169};{231}m") # RGB color
    # Draw empty lines to draw on 
    for i in range(0, len(printed_frame)):
        print("\n")

    while True:
        # Choose a new character when it moves out of bounds 
        if character_index <= 0:
            choose_random_character()

        print_frame()

        time.sleep(speed)
        # Decrement the character_index
        character_index -= 1

start_game()

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



def choose_random_character():
    global current_character, character_index
    current_character = random.choice(CHARACTER_LIST)
    character_index = STEPS # Reset 

def start_game():
    # Set color
    print(f"\x1B[38;2;{100};{169};{231}m") # RGB color
    # Draw empty lines to draw on 
    for i in range(0, len(STEPS)):
        print("\n")



    while True:
        # Choose a new character when it moves out of bounds 
        if character_index <= 0:
            choose_random_character()

        # print_frame()

        sys.stdout.write(f"\033[{5}A") # Move cursor up 5 lines/rows
        sys.stdout.write("Row 1\n")
        sys.stdout.write("Row 2\n")
        sys.stdout.write("Row 3\n")
        sys.stdout.write("Row 4\n")
        sys.stdout.write("Row 5\n")

        time.sleep(speed)
        # Decrement the character_index
        character_index -= 1

start_game()
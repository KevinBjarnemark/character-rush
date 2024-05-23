import time
import random
import sys
import threading

CHARACTER_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
STEPS = 20
JUMPING_RANGE = [8, 9, 10]
speed = 0.1
character_index = 20
current_character = "A"
stickman_index = 7
cycle = 0
printed_frame = ["", "", "", "", ""]
jumping = False
frames_jumped = 0


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
    global printed_frame, stickman_index, character_index, current_character, jumping, frames_jumped

    printed_frame = [""] * len(printed_frame) # Clear the last frame

    # Draw the current frame 
    if jumping == False:
        printed_frame[0] = ""
        printed_frame[1] = ""
        printed_frame[2] = "    O  "
        printed_frame[3] = "   /|\\ "
        default_string =   "___/_\\_____________"
        # Add the moving character to the last line
        sliced_string = default_string[:character_index] + current_character + default_string[character_index:]
        printed_frame[4] = sliced_string
    else: 
        if frames_jumped < 5:
            frames_jumped += 1
        else:
            jumping = False
            frames_jumped = 0
        printed_frame[0] = ""
        printed_frame[1] = "    O  "
        printed_frame[2] = "   /|\\ "
        printed_frame[3] = "   / \\"
        default_string =   "____________________"
        # Add the moving character to the last line
        sliced_string = default_string[:character_index] + current_character + default_string[character_index:]
        printed_frame[4] = sliced_string
    
    # Print the current frame 
    sys.stdout.write(f"\033[{len(printed_frame)}A") # Move cursor to the top
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\033[K")
        # Print and add a new line 
        sys.stdout.write(printed_frame[i] + "\n")

def choose_random_character():
    global current_character, character_index
    current_character = random.choice(CHARACTER_LIST)
    character_index = STEPS # Reset 

def get_input():
    global jumping
    user_input = sys.stdin.read(1)
    if user_input == current_character:
        jumping = True

def start_game():
    global printed_frame, character_index
    # Set color
    print(f"\x1B[38;2;{100};{169};{231}m") # RGB color
    # Draw empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    while True:
        # Listen to the user input
        input_thread = threading.Thread(target=get_input)
        input_thread.daemon = True  # Allow the thread to exit when the main program exits
        input_thread.start()

        # Choose a new character when it moves out of bounds 
        if character_index <= 0:
            choose_random_character()

        print_frame()

        time.sleep(speed)
        # Decrement the character_index
        character_index -= 1

start_game()

import time
import random
import sys
import threading

character_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
STEPS = 20
JUMPING_RANGE = [8, 9, 10]
speed = 0.3
character_index = 20
current_character = "A"
stickman_index = 7
cycle = 0
printed_frame = ["", "", "", "", ""]
jumping = False
frames_jumped = 0
frame_count = 0

def print_frame():
    global printed_frame, frame_count, character_list

    rows = len(printed_frame)
    character_amount = len(character_list)

    # Clear the last frame
    printed_frame = [""] * rows
    # Draw the current frame 
    printed_frame[0] = " " * STEPS
    printed_frame[1] = " " * STEPS
    printed_frame[2] = "    O              "
    printed_frame[3] = "   /|\\             "
    printed_frame[4] = "___/_\\_____________"
    
    # Matrix rain
    for i in range(0, rows):
        sliced = printed_frame[i][:10] + character_list[i] + printed_frame[i][10:]
        printed_frame[i] = sliced

    # Print the current frame 
    sys.stdout.write(f"\033[{len(printed_frame)}A") # Move cursor to the top
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\033[K")
        # Print and add a new line 
        sys.stdout.write(printed_frame[i] + "\n")
        sys.stdout.flush() # Flush immediately to ensure DOM rendering
    
    frame_count =+ 1

def choose_random_character():
    global current_character, character_index
    current_character = random.choice(character_list)
    character_index = STEPS # Reset 

def get_input():
    global jumping
    while True:
        user_input = sys.stdin.read(1)
        if user_input == current_character:
            jumping = True

def start_game():
    global printed_frame, character_index, STEPS
    # Listen to the user input
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True  # Allow the thread to exit when the main program exits
    input_thread.start()
    # Set color
    print(f"\x1B[38;2;{100};{169};{231}m") # RGB color
    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    # Game logic
    while True:
        # Choose a new character when it moves out of bounds 
        if character_index <= 0:
            choose_random_character()

        print_frame()
        time.sleep(speed)
        # Decrement the character_index
        character_index -= 1

start_game()
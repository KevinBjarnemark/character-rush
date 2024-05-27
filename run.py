import time
import sys

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

character_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
STEPS = 20
speed = 0.1
cycle = 0
printed_frame = ["", "", "", "", ""]
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
    # Calculate loop length
    loop_length = frame_count if frame_count < rows else min(character_amount, rows)
    for i in range(0, loop_length):
        y = i # Row position
        # Push 'left-over' characters down
        if frame_count > rows and character_amount > 0:
            y = rows - i - 1 # Inverse
        
        sliced = printed_frame[y][:10] + character_list[i] + printed_frame[y][10:]
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

def build_matrix_rain():
    global printed_frame, character_bank


def start_game():
    global printed_frame
    # Set color
    print(f"\x1B[38;2;{100};{169};{231}m") # RGB color
    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    build_matrix_rain()

    # Game logic
    while True:
        print_frame()
        time.sleep(speed)

start_game()
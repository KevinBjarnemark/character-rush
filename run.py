import time
import sys

character_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
STEPS = 20
speed = 0.3
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
        sliced = printed_frame[y][:10] + character_list[y] + printed_frame[y][10:]
        printed_frame[y] = sliced

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

def start_game():
    global printed_frame
    # Set color
    print(f"\x1B[38;2;{100};{169};{231}m") # RGB color
    # Create empty lines to draw on 
    for i in range(0, len(printed_frame)):
        sys.stdout.write("\n")

    # Game logic
    while True:
        print_frame()
        time.sleep(speed)

start_game()

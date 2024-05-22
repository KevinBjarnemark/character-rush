import os
import time

CHARACTER_LIST = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
STEPS = 20
JUMPING_RANGE = [8, 9, 10]
speed = 1
character_index = 20
current_character = "A"
stickman_index = 7
cycle = 0

def print_frame():
    global stickman_index, character_index, current_character, jumped

    # Draw the scene (except for bottom row)
    printed_frame = [
        "",
        "",
        "    O  ",
        "   / \\ ",
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

while True:
    # Clear the console
    os.system('cls') 
    print_frame()
    time.sleep(speed)
    # Decrement the character_index
    character_index -= 1

"""Modules"""
import sys
import random

def neutral_white():
    """Change the terminal color to neutral white"""
    return sys.stdout.write(f"\x1B[38;2;{255};{255};{255}m")

def random_green_nuance():
    """Generates a random nuance of green"""
    r = random.randint(40, 140)
    g = random.randint(200, 250)
    b = random.randint(80, 180)
    return sys.stdout.write(f"\x1B[38;2;{r};{g};{b}m")

def print_frame(frame_reference):
    """Prints previously built 'frame' with sys"""

    # Print the current frame
    sys.stdout.write(f"\033[{len(frame_reference)}A") # Move cursor to the top
    for i in frame_reference:
        sys.stdout.write("\033[K")
        # Print and add a new line
        sys.stdout.write(i + "\n")
        sys.stdout.flush() # Flush immediately to ensure DOM rendering

"""Modules"""
import sys
import random
import time

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
    """Prints a previously built 'frame' with sys"""
    # README #1

    # Print the current frame
    sys.stdout.write(f"\033[{len(frame_reference)}A")  # Move cursor to the top
    for i in frame_reference:
        sys.stdout.write("\033[K")
        # Print and add a new line
        sys.stdout.write(i + "\n")
        sys.stdout.flush()  # Flush immediately to ensure DOM rendering


def create_empty_lines(amount):
    """Creates newlines in the terminal with sys"""
    for _ in range(0, amount):
        sys.stdout.write("\n")

def sys_print(text, simulate_writing=False):
    """A sys version of 'print', set the second 
    parameter to True if you want to simulate writing"""
    if simulate_writing:
        for char in text:
            sys.stdout.write(char)
            if random.randrange(10) > 8: # 10%
                time.sleep(random.randrange(10, 50)/100)
            else:
                time.sleep(random.randrange(1, 5)/100)
            sys.stdout.flush()
    else:
        sys.stdout.write(text)
        sys.stdout.flush()

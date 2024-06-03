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


def count_down(num, starting_in=False):
    """Counts down in seconds"""
    if starting_in:
        sys.stdout.write("Starting in...\n")
        sys.stdout.flush()
    for i in range(0, num):
        sys.stdout.write(f"{num - i}\n")
        sys.stdout.flush()
        time.sleep(1)


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


def sys_print(text, experimental, simulate_writing=False):
    """A sys version of 'print', set the second
    parameter to True if you want to simulate writing

    Parameters:
    text (str): The message to display in the terminal.
    experimental (bool): Since the browser DOM rendering
    relies on newlines, this will simulate writing by printing
    lines instead of the individual characters when True.
    """

    if simulate_writing:
        # Note that print(text, end="") would also work
        # but since flush is needed, I decided to use
        # sys.stdout here
        if experimental:
            for char in text:
                sys.stdout.write(char)
                sys.stdout.flush()
                # Delay
                if random.randrange(10) > 8:  # 20 %
                    time.sleep(random.randrange(10, 50)/100)
                else:
                    time.sleep(random.randrange(1, 5)/100)
        else:
            for index, line in enumerate(text.split("\n")):
                sys.stdout.write(line + "\n")
                sys.stdout.flush()
                if index > 0:
                    time.sleep(random.randrange(1, 2))
    else:
        sys.stdout.write(text)
        sys.stdout.flush()

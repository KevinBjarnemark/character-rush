"""A storage for different types of characters"""


# Character groups chosen based on the difficulty level
# NOTE Place the more difficult characters at the end. 
# The algorithm will dig deeper into each group the higher 
# the difficulty is. eg. l is very similar to 1

CHARACTER_GROUPS = {
    "alphabet": [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", 
        "n", "o", "p", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
        "q", "l",
    ],
    "numbers": [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ],
    "symbols_easy": [
        "?", ".", "!", "@", "#", "%", ","
    ],
    "symbols_intermediate": [
        "/", "=", "+", "_", "$", "*", "(", ")", "&"
    ],
    "symbols_advanced": [
        ":", "-", "[", "]"
    ],
    "symbols_expert": [
        "^", "{", "}", ";", "'", "\"", "<", ">", "\\", "|", "~", "`"
    ],
}

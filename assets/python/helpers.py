"""Modules"""
from assets.python.printing import sys_print


def validated_input(message, browser_terminal, data=None):
    """
    Validates the user input based on the specified data.
    Note that the input is wrapped in a string to work as expected
    in the deployed version.

    Parameters:
    message (str): The message to display to the user.
    data (dictionary): The specified rules that should be tested +
    info. Example below:

    {
        "type" (str): "int", "float", or "str"
        "min" (number): (optional) --> Limit the input
            When type is str: The amount of characters submitted
            cannot be below than this number.
            When type is int or float: The submittend number
            cannot be below that what is specified.
        "max" (number): (optional) --> Limit the input
            When type is str: The amount of characters submitted
            cannot be above than this number.
            When type is int or float: The submittend number
            cannot be above that what is specified.
        "match_strings" (list): (optional) --> Only allow strings
        that exists in this list
    }

    Returns:
    int, float, or str: The validated user input.
    """

    sys_print(message, browser_terminal, browser_terminal)
    while True:
        user_input = str(input("\n"))
        error_message = ""

        try:
            error_message = ""  # Reset
            optional_min = data.get("min")
            optional_max = data.get("max")
            is_number = data["type"] == "int" or data["type"] == "float"

            if is_number:
                if data["type"] == "int":
                    user_input = int(user_input)
                elif data["type"] == "float":
                    user_input = float(user_input)

                # Limit the number
                if optional_min is not None:
                    if user_input < optional_min:
                        error_message = (
                            f"Input must be at least {optional_min}"
                        )
                        raise ValueError()
                if optional_max is not None:
                    if user_input > optional_max:
                        error_message = f"Input must be at most {optional_max}"
                        raise ValueError()
            elif data["type"] == "str":
                optional_match_strings = data.get("match_strings")
                # Match any specified strings
                match_strings_exists = optional_match_strings is not None
                if match_strings_exists:
                    if user_input not in optional_match_strings:
                        # Avoid embedding the alternatives here
                        # since they may be 'secret'
                        error_message = (
                            "Invalid input: Couln't recognize " +
                            "your input correctly"
                        )
                        raise ValueError()
                # Limit the amount of characters
                if optional_min is not None:
                    if len(user_input) < optional_min:
                        error_message = (
                            "Input must be at least " +
                            f"{optional_min} character(s)"
                        )
                        raise ValueError()
                if optional_max is not None:
                    if len(user_input) > optional_max:
                        error_message = (
                            "Input must be at most " +
                            f"{optional_max} character(s)"
                        )
                        raise ValueError()
            else:
                # Dev error
                error_message = (
                    "(Dev error) Only 'int', 'float' or 'str' are allowed."
                )
                raise ValueError()

            return user_input
        # Avoid exposing the 'dev error' here to keep the UI user-friendly
        except ValueError:
            if len(error_message) > 0:
                sys_print(
                    f"\nInvalid input: {error_message}, please try again.",
                    browser_terminal,
                    True
                )
            else:
                sys_print(
                    "\nInvalid input: Please try again.",
                    browser_terminal,
                    True
                )

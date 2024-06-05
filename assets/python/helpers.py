"""Modules"""
from assets.python.printing import sys_print


def validated_input(message, browser_terminal, data=None, bool_question=False):
    """
    Validates the user input based on the specified data.
    Note that the input is wrapped in a string to work as expected
    in the deployed version. If an error occurs, the user will
    be 'stuck' inside this function.

    Parameters:
    message (str): The message to display to the user.
    browser_terminal (boolean): When True, the script is being run
    inside a browser terminal on the web.
    data (dictionary): The specified rules that should be tested +
    info. Example below:
    bool_question (boolena): Set this to True if it is a yes/no
    question. The data parameter should be set to None and if the
    user types 'yes' or 'Yes', this function return True.

    data parameter example:
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
    int, float, str, or boolean: If the bool_question parameter is
    True, it returns a booelan, otherwise the validated user input.
    """

    # Handle boolean questions
    if bool_question:
        data = {
            "type": "str",
            "match_strings": ["yes", "Yes", "no", "No"]
        }

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

            # Return a boolean if it is a yes/no question
            if bool_question:
                if user_input in ["Yes", "yes"]:
                    return True
                else:
                    return False
            else:
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

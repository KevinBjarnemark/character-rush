"""Modules"""
import random
# Third party library!
from inspirational_quotes import quote


def get_inspirational_quote():
    """Uses a third-party library to fetch quotes mixed with
    custom logic. It attempts to create a more realistic
    conversation by embedding the fetched quotes into the
    conversation. Here's a visualization of how the quotes
    are embedded:

    1 Leading in (A wise man named)

    2 Author (Albert Einstein)

    3 Inbetween (once said)

    4 Quote (Life is like riding a bicycle.......)

    5 Ending (I hope this will cheer you up!)
    """
    def get_error_message():
        """Returns a custom error message. This is a nested function
        to improve performance."""
        try:
            static_quotes = [
                "Angels fly because they take themselves lightly - Unknown",
                "If you do what you've always done you will get what you've "
                "always gotten - Anthony Roberts",
                "It's how you deal with everyday challenges that ultimately "
                "will determine your success - Liveral Johnsson",
            ]
            error_message = (
                "I encountered an error when trying to provide "
                "you a quote..."
            )
            stored_quote = (
                f"Here's a quote that I have stored in my system:"
                f"\n{random.choice(static_quotes)}\nYou might want to refresh "
                "the page."
            )
            return f"{error_message}\n{stored_quote}"
        except RuntimeError:
            return f"{error_message}\nYou might want to refresh the page."

    try:
        random_quote = quote()
        author = random_quote['author']
        fetched_quote = random_quote['quote']
    # Avoid exposing 'e' to the user and keep the app user friendly
    except RuntimeError:
        return get_error_message()

    leading_in = [
        "A wise person named",
        "If it cheers you up,",
        "Remember what",
        "As the great",
    ]
    inbetween = [
        "once said",
        "famously remarked",
        "reminded us of",
        "wisely pointed out",
        "beautifully stated",
    ]
    ending = [
        "I hope this will cheer you up!",
        "I hope you find this uplifting.",
    ]

    try:
        # Embedded quote
        q = {
            "leading_in": random.choice(leading_in),
            "inbetween": random.choice(inbetween),
            "ending": random.choice(ending),
        }

        out = (
            f"{q["leading_in"]} {author} {q["inbetween"]}, "
            f"'{fetched_quote}' {q["ending"]}"
        )
        accumulate = ""
        result = ""
        if len(out) >= 60:
            for index, word in enumerate(out.split()):
                accumulate += word + " "
                # Add a newline
                if len(accumulate) >= 60:
                    result += accumulate + "\n"
                    accumulate = ""
                # Last iteration
                if index == len(out.split())-1:
                    result += accumulate

        return result
    except RuntimeError:
        return get_error_message()

import typing as tp

# If you declare a variable with a direct instantiation of a class,
# any type checker will automatically infer the type of that variable.
# If the type has generic subtyping, then it _might_ be able to infer
# the subtypes as well.

# scalars (or 'simple' types) are pretty obvious

number = 1
string = "hey ai4dq!"
double = 3.14159265

# collection types

a = []  # it doesn't know what subtype this list might ever have
a += [2]  # assumes this list has only integers
a += ["hey"]  # assumes this list has only strings

a = [1, 2, 3, 4]
a = [1, 2, 3, 4, "five", "six", "seven"]
a = [1, 2.0, "three", complex(real=4, imag=0)]

# Now: what if I have a variable which could be different things? Can I
# rely on inference?
# If the assignments are disjoint and explicit, you usually can:

import random

should_split = random.choice((True, False))

if should_split:
    replacement = "this string"
else:
    replacement = ["this", "string"]

reveal_type(replacement)

# If you have a pre-defined type assignment, that can usually mess with it.
# Static type checkers are not great at keeping up with state changes.

my_list_of_numbers_and_strings = [1, 2, 3]  # inferred type is list[int]
my_list_of_numbers_and_strings += [
    "four",
    "five",
    "six",
]  # correctly infers that it now is list[int, str]
my_list_of_numbers_and_strings += [1.0, (1, 2, 3)]  # wrongly infers list[int, str]

reveal_type(my_list_of_numbers_and_strings)

# Type checkers' context length is usually pretty small, so if you know something can
# have many types beforehand, you should help it with a variable annotation:
new_list_of_numbers_and_strings: list[tp.Union[int, str]] = [1, "two"]

# Inference is great for short-lived variables, but not so much for long-lived ones.
# Because inference is not all that powerful, it will never complain about future
# operations for an unannotated variable. Because of this, if you know what types a
# variable may/should have in the future, it is worth it to annotate it:
foo: dict[str, float] = {"pi": 3.14}

# Now, whatever you do with an annotated variable, it's going to remember the annotation
# you gave it as an authoritative truth. Any operations not in accordance with it will
# raise type errors:
foo["greeting"] = "hey"


# EXTRA: variables can be typed without assignments too
a: list[tuple[int, str]]

# Remember: it's usually a good idea to annotate variables you'd like to restrict to
# particular types. This will allow your type checker (usually baked into IDEs) to let
# you know of possible mistakes much earlier.

# Imagine you have a function that may take either a str
# or a bytes object, and it spits out a DF of the same type.
# How do you annotate this function?

from typing import Union


def concat(s1: Union[str, bytes], s2: Union[str, bytes]) -> Union[str, bytes]:
    return s1 + s2


# Notice how the type checker already complains about the return
# expression. What about usage?

result = concat("Quantum", "Black")

# Why doesn't it know the result would be a `str`?

# Well, the right question is "why would it?". Think about
# it: type annotations are all independent from one another,
# so the type checker assumes nothing. What if `s1` is a `str`
# and `s2` is a `bytes`? That's where `TypeVar`s come in!

from typing import TypeVar

STR_OR_BYTES = TypeVar("STR_OR_BYTES", str, bytes)


def concat2(s1: STR_OR_BYTES, s2: STR_OR_BYTES) -> STR_OR_BYTES:
    return s1 + s2


_ = concat2("Quantum", "Black")
_ = concat2(b"McKinsey", b" & Company")

# Notice all the typing issues are gone! This is why it's called
# a Type Variable: in the moment you assign it in a context, it
# will be bound to all annotations with the same type variable for
# the whole scope it's been used in. This case of `str` and `bytes`
# is so common that `typing` already provides a type variable
# ready to use, called AnyStr.

from typing import AnyStr


def largest_palindromic_substring(string: AnyStr) -> AnyStr:
    def is_palindrome(string):
        if len(string) <= 1:
            return True
        return string[0] == string[-1] and is_palindrome(string[1:-1])

    # Notice that, even though the type checker does not know
    # what exact type `string` would be, either way it has a .lower()
    # method, so that's also known by the static checker.
    string = string.lower()

    if is_palindrome(string):
        return string

    left_cut_largest = largest_palindromic_substring(string[:-1])
    right_cut_largest = largest_palindromic_substring(string[1:])

    if len(left_cut_largest) > len(right_cut_largest):
        return left_cut_largest

    return right_cut_largest


_ = largest_palindromic_substring("abracadabra")
_ = largest_palindromic_substring(b"essex")

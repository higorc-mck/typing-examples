# Functions were the first addition to type annotations in
# Python 3.6. Variable annotation was actually added in 3.7 xD
def is_odd(x: int) -> bool:
    return x % 2


wrong_param = "three"
is_odd(wrong_param)

# annotations are always the authoritative SoT, so `is_it_odd` is
# assumed to be a `bool` even though the function body would
# return an integer
is_it_odd = is_odd(3)


# Items without type annotations goes completely unchecked
# by the type checker. This is because it can't know what you're
# going to pass in as parameters, so it's just assuming you know
# what you're doing (but... do you?)
def my_confusing_function(arg1, arg2, arg3=None):
    arg1 += "string"
    arg1 += 5
    return arg1 + arg2 == arg3


reveal_type(my_confusing_function(1, 2, 3))

# Note that functions that don't return anything actually return
# `None`. Annotating the return value is telling explicitly to
# the type checker that it does not return anything, whereas
# not annotating the return type leaves it up to inference.
# It _may_ be good, it _may_ also be horrible. Also, you don't
# get the benefits of type checking, because it can't tell you
# whether you're returning something that might not be the type
# you wanted to return.


def do_nothing() -> None:
    pass


# Other than this, all of the same other rules for variables hold.

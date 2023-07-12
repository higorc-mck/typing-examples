# There is one more very useful addition to typing. Sometimes
# you might have big dictionaries with some expected structure,
# but it might both be hard to remember and/or to discover this
# structure. Hence, PEP-589 added TypedDict to Python 3.8 to
# help with this.

# The way to do this is to subclass `typing.TypedDict` in almost
# the same way you would do with a NamedTuple.

from typing import TypedDict


class Person(TypedDict):
    name: str
    age: int
    height_cm: int
    works_at: str


# Now, whenever you type something as a Person, you'll get code
# hints to the structure of this dictionary as well as the types
# of its variables!

p: Person = {"name": "Higor", "age": 27, "height_cm": 185, "works_at": "McKinsey"}

# Notice that, while Person _looks_ like a normal class, it's just
# a fancy syntactic sugar for a regular dictionary.

# You can even use the class to instantiate it:

p = Person(name="Higor", age=27, height_cm=185, works_at="McKinsey")

# And, of course, you can create nested TypedDicts as well:


class Person(TypedDict):
    name: str
    age: int
    height_cm: int
    works_at: str
    parents: tuple["Person", "Person"]  # quoted because "Person" hasn't been
    # defined yet

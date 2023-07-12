# Dealing with user types is fairly straightforward.
# You can use class names as types anywhere you could annotate.

from dataclasses import dataclass


@dataclass
class Monke:
    name: str
    alive: bool


def rip(monke: Monke) -> None:
    if not monke.alive:
        print(f"May God rest {monke.name}'s soul")
    else:
        print(f"{monke.name}'s alive, dumbass")


harambe = Monke(name="Harambe", alive=False)
rip(harambe)

# Notice how the IDE can't know shit without the annotation:


def rip_unannotated(monke):
    if not monke.alive:
        print(f"May God rest {monke.name}'s soul")
    else:
        print(f"{monke.name}'s alive, dumbass")


rip_unannotated(harambe)
rip_unannotated(10)  # clearly a mistake, should shout an error!


# Now, type hinting methods will follow all the same rules as
# normal functions, with the exception of the first parameter
# to methods:


class OneMethod:
    def whos_self(self, name):
        reveal_type(self)
        reveal_type(name)
        pass


# Notice that, though I provided no type annotations, it knows
# that `self` (or whatever you name the first parameter) will
# always be an object of the corresponding class. This is a syntax
# quirk that allows you to skip an obvious type hint.

# ---------------------------------------------------------------

# Now for the weird part. Consider this example:


class GotAttributes:
    def __init__(self) -> None:
        self.number = 3
        self.float = 3.14
        self.cond = False

    def a_method(self) -> None:
        self.string = "o rly"
        if self.cond:
            self.animal = Monke("Higor", True)

    def _another_method(self):
        self.cond = not self.cond
        self.string = b"not a str anymore"


inst = GotAttributes()
# inst.a_method()
print(f"{inst.number = }")
print(f"{inst.float = }")
print(f"{inst.string = }")
print(f"{inst.animal = }")

# Notice it can't correctly infer the type for the attribute `animal`,
# because its definition happens inside a method that isn't __init__,
# i.e. a method that not necessarily will be ran upon instantiation.

# This happens because instance variables can be set at _any_ moment
# during its lifetime. So a parameter can come in and out of existence
# at any moment, and also change types just like that.

# For this, we can add variable-like annotation to instance variables:

from typing import Optional, Union


class GotTypedAttributes:
    """"""

    number: int = 5
    float: float
    string: Union[str, bytes]
    animal: Optional[Monke]

    ...


inst = GotTypedAttributes()

inst.number = 6
GotTypedAttributes.number

# In this case, a type checker will take the annotations as the
# authoritative source of type, as well as inform any code within the
# class about type mismatches in any of these variables. So, generally,
# typing attributes is better than not doing so, even when defined in
# __init__ (due to variable types). It also makes it easier to read, in
# one place, what are all of the attributes of a given instance of this
# class.

# Class Variables

# One more point is class variables, those which are part of the class
# itself and not the instances. `typing` provides one special class for
# this:

from typing import ClassVar


class Singleton:
    _instance_count: ClassVar[int] = 0

    @classmethod
    def my_func(cls, param):
        pass


Singleton.my_func(param=3)


# Notice what happens if I try to assign a value to an instance's
# attribute of the same name:

inst = Singleton()
inst._instance_count = (
    2  # cannot be assigned through a class instance because it is a ClassVar
)

inst.my_func(3)

Singleton._instance_count = 2

# This also helps prevent mistakes with state management :)

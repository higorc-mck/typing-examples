# A simple-looking feature that enables some rich stuff
# ouf of typing, Literal!

# Simple usage
from typing import Literal
from typing_extensions import TypeAlias

CONSTANT: Literal["HEY"] = "HEY"  # ... useless


companies = ["McK", "QB"]

my_type: TypeAlias = Literal["McK", "QB"]


# BUT
def my_func(company: my_type):
    ...


my_func(company="Bain")  # so much useful (unironically)

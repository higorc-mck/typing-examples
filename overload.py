# In almost all statically typed languages, the parameters of a
# function are as much part of its signature as the function name.
# That enables what's called Overloading, which is to define two
# functions/methods with the same name, but which accept different
# arguments and have different bodies. Python's approach to this
# (single argument dispatch) is not all that powerful (yet) but
# there's something close to that when it comes to `typing`.

# Say you have a function that can will do one "semantic" operation,
# but which could take in parameters in more than one specific way.
# Think of pandas.DataFrame.drop, for example:

import pandas as pd

my_df = pd.DataFrame(columns=list("abcd"))

# Drop a sequence of labels where you later specify the axis
my_df.drop(labels=["a", "b"], axis="columns")
# OR
# Drop a sequence of labels naming the axis directly.
my_df.drop(columns=["a", "b"])

# This function, for example, won't let you even try to use more than
# one of these call mechanisms at once. Either you use 'axis', or you
# name the axis directly as a keyword argument; anything else and you
# get an error. How did they do this?

# Well, turns out it's not complicated at all. The function body is
# as you would normally imagine in Python, normally handling all the
# parameter setttings according to the desired behavior. So, let's
# use a fake DataFrame as an example.


class DataFrame:
    index: list[int]
    columns: list[str]

    # You can imagine the implementation as you normally would within
    # this case:
    def drop(
        self,
        labels: list = None,
        axis: str = None,
        index: list[int] = None,
        columns: list[str] = None,
    ):
        if (labels or axis) and (index or columns):
            raise ValueError("Only one of them should be set at a time etc etc etc!")

        ...  # rest of function body

    # But how do you explicitly mean to the user that he should only
    # use one or another, almost as if the function had _different
    # signatures_? Here comes in typing.overload!


df = DataFrame()

df.drop(labels=[1, 2, 3], index=[1, 2, 3])


from typing import overload, Optional

# typing.overload will allow you to create fake function declarations
# with the same name as the one you'll create, but which specify
# discrete modes of usage. So our earlier example goes like this:


class DataFrame:
    index: list[int]
    columns: list[str]

    @overload
    def drop(self, *, labels: list, axis: str):
        ...

    @overload
    def drop(self, *, index: list[int]):
        ...

    @overload
    def drop(self, *, columns: list[str]):
        ...

    # You can imagine the implementation as you normally would within
    # this case:
    def drop(
        self,
        *,
        labels: Optional[list] = None,
        axis: Optional[str] = None,
        index: Optional[list[int]] = None,
        columns: Optional[list[str]] = None
    ):
        if (labels or axis) and (index or columns):
            raise ValueError("Only one of them should be set at a time etc etc etc!")

        ...  # rest of function body


my_df = DataFrame()

# Now, my type checker lets me know of wrong usage even if it's valid
# Python code, because I specified all the intended usages of this
# method!

my_df.drop(labels=[1, 2, 3])  # wrong, no axis
my_df.drop(labels=[1, 2, 3], axis="cols")
my_df.drop(
    columns=["a", "b", "c"], index=[1, 2, 3]
)  # wrong, can't use both cols and index
my_df.drop(columns=["a", "b", "c"])

# This is made way more useful by using typing.Literal. Ever had a
# function made to return different stuff based on the arguments?
# Consider this adapted excerpt from virgil:

from typing import Union
import pyspark.sql as ps


def load_data(as_spark: bool) -> Union[pd.DataFrame, ps.DataFrame]:  # type: ignore
    ...  # function body


from typing import Literal

# So, to overloading `load_data()`:


@overload
def load_data(as_spark: Literal[True]) -> ps.DataFrame:
    ...


@overload
def load_data(as_spark: Literal[False]) -> pd.DataFrame:
    ...


@overload
def load_data(as_spark: bool) -> Union[pd.DataFrame, ps.DataFrame]:
    ...


# Now:


my_df = load_data(as_spark=False)

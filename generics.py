# Now let's talk about Generics.

# Ever had a class that manages some other type of data? Many
# collection types are usually meant to hold many objects of
# one particular type, and hence many functions are bound to
# have parameter and return types based on this type.

# So, how do we type these? Here comes useful typing.Generic.
# Let's test it with a class:

from typing import AnyStr, Generic, Iterable, Union


class Queue(Generic[AnyStr]):
    values: list[AnyStr]

    def __init__(self, values: Iterable[AnyStr]) -> None:
        self.values = list(values)

    def pop(self) -> AnyStr:
        return self.values.pop(0)

    def insert(self, value: AnyStr) -> None:
        self.values.append(value)


str_queue = Queue(["hey", "everyone", "how", "you", "doing"])

val = str_queue.pop()
reveal_type(val)  # checker knows it's a `str`!

# Notice we had to use an extra class `Generic`. That's because,
# to hold the type variable information at a class-wide context,
# you can't just provide it at the level of functions - the class
# itself needs to hold that. That's what `Generic` is for :-)

# You can also subclass a typed-version of Queue, for example:


class StrQueue(Queue[str]):
    def as_bytes_queue(self, encoding: str) -> Queue[bytes]:
        return Queue(values=[val.encode(encoding) for val in self.values])


# Because we've subclassed `Queue[str]`, it assumes the `values`
# attributes is necessarily a `list[str]`, and hence the type checker
# does not bother about calling `.encode()` in a bytes object. xD

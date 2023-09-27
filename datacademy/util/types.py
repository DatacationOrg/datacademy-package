"""Module containing utilities related to types."""
from typing import TypeVar

T = TypeVar('T')


def check_isinstance(__obj: object, __cls: type[T]) -> T:
    """Check if an object is an instance of a class.

    Args:
        __obj (object): Object.
        __cls (type[T]): Class.

    Raises:
        TypeError: If this object is not an instance of the class.

    Returns:
        T: Object.
    """
    if isinstance(__obj, __cls):
        return __obj

    raise TypeError(f'Expected instance of {__cls.__name__}, but got {type(__obj)} for object {__obj!r}')

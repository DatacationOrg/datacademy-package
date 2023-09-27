"""Module containing class to send objects via requests."""

from datetime import datetime
from enum import Enum
from typing import Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel

from datacademy.util import check_isinstance

from .types import ANSWER_TYPES, OBJECT_TYPES

DF_ORIENT: Literal['tight'] = 'tight'
"""DataFrame orientation to use when converting from/to JSON."""


class ObjectType(str, Enum):
    """Enum to for the type of object that is being sent."""

    BOOL = 'bool'
    INT = 'int'
    FLOAT = 'float'
    STR = 'str'
    DATETIME = 'datetime'
    LIST = 'list'
    DICT = 'dict'
    CSV = 'csv'
    NP_ARRAY = 'numpy.ndarray'


class ObjectModel(BaseModel):
    """Pydantic model to resemble an object in a request."""
    obj_type: ObjectType
    obj: OBJECT_TYPES

    @staticmethod
    def create(obj: ANSWER_TYPES) -> 'ObjectModel':
        """Create a new request object.

        Args:
            obj (obj_types): Object to create this RequestObject for.

        Raises:
            NotImplementedError: If the type of the object is not supported.

        Returns:
            RequestObject: Created RequestObject.
        """
        if isinstance(obj, pd.DataFrame):
            return ObjectModel(
                obj_type=ObjectType.CSV,
                obj=obj.to_dict(orient=DF_ORIENT)
            )

        if isinstance(obj, np.ndarray):
            return ObjectModel(
                obj_type=ObjectType.NP_ARRAY,
                obj=obj.tolist()
            )

        if isinstance(obj, ANSWER_TYPES):
            return ObjectModel(obj=obj, obj_type=ObjectType(type(obj).__name__))  # type: ignore

        raise NotImplementedError(f'RequestObject is not implemented for {type(obj)}')

    def get(self) -> ANSWER_TYPES:
        """Get the object.

        Returns:
            Any: Object.
        """
        match self.obj_type:
            case ObjectType.CSV:
                return pd.DataFrame.from_dict(check_isinstance(self.obj, dict), orient=DF_ORIENT)
            case ObjectType.NP_ARRAY:
                return np.array(check_isinstance(self.obj, list))
            case ObjectType.DATETIME:
                check_isinstance(self.obj, datetime)
            case ObjectType.BOOL:
                check_isinstance(self.obj, bool)
            case ObjectType.INT:
                check_isinstance(self.obj, int)
            case ObjectType.FLOAT:
                check_isinstance(self.obj, float)
            case ObjectType.STR:
                check_isinstance(self.obj, str)
            case ObjectType.LIST:
                check_isinstance(self.obj, list)
            case ObjectType.DICT:
                check_isinstance(self.obj, dict)

        return self.obj

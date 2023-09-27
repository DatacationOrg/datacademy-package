"""Module containing type information."""

from datetime import datetime

import numpy as np
import pandas as pd
from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

OBJECT_TYPES = StrictBool | StrictInt | StrictFloat | datetime | StrictStr | list | dict
ANSWER_TYPES = bool | int | float | datetime | str | list | dict | pd.DataFrame | np.ndarray

""" Generic Production definition module"""

import dataclasses
from typing import Tuple, Union

from pyformlang import cfg


@dataclasses.dataclass
class Production:
    """ A data class representing an abstraction of a generic product """
    head: Tuple[Union[cfg.Variable, cfg.Terminal], ...]
    body: Tuple[Union[cfg.Variable, cfg.Terminal], ...]

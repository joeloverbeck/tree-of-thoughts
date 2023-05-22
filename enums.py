"""This module contains all the custom Enums used throughout the library
"""
from enum import Enum


class StateType(Enum):
    CONTEXT = 1
    PLANNING = 2
    IMPLEMENTATION = 3
    REFINEMENT = 4

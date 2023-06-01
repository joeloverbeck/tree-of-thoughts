"""This module contains all the custom Enums used throughout the library
"""
from enum import Enum


class StateType(Enum):
    """The type of a state (which are nodes in a tree of thoughts)

    Args:
        Enum (Enum): the base Enum class
    """

    CONTEXT = 1
    PLANNING = 2
    IMPLEMENTATION = 3
    REFINEMENT = 4
    BRAINSTORMING = 5
    RESEARCH = 6

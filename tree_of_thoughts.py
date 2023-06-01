"""This module contains the definition of a tree of thoughts, which handles the complex relationship
between a series of intermediate prompts to achieve a specific result with GPT-4.
"""
from collections import deque
from api_requests import request_response_from_ai_model
from defines import (
    MAX_NUMBER_OF_STEPS,
    MIN_NUMBER_OF_STEPS,
    get_directory_path_for_tree_of_thoughts,
)
from enums.state_type import StateType
from errors import (
    InvalidParameterError,
)
from file_utils import (
    create_directories,
    create_file_path_for_winner,
    write_response_to_file,
)
from responses.requesting import request_responses
from state import State
from tree import Tree
from voting import determine_winners


class TreeOfThoughts:
    """A class that handles the relationships to achieve complex prompt results with GPT-4 through intermediate steps."""

    def __init__(
        self,
        tree_of_thoughts_name,
        context_state,
        state_layers,
        number_of_steps,
        breadth,
    ):
        if not isinstance(context_state, State):
            raise InvalidParameterError(
                f"The TreeOfThoughts required a 'context_state' of type State, but it was: {context_state}"
            )

        if not context_state.get_state_type() == StateType.CONTEXT:
            raise InvalidParameterError(
                "Attempted to create a Tree of Thoughts with a state that wasn't of type CONTEXT."
            )

        if (
            number_of_steps < MIN_NUMBER_OF_STEPS
            or number_of_steps > MAX_NUMBER_OF_STEPS
        ):
            raise InvalidParameterError(
                f"The TreeOfThoughts requires a number of steps between {MIN_NUMBER_OF_STEPS} or {MAX_NUMBER_OF_STEPS}, but it was {number_of_steps}"
            )

        if breadth < MIN_NUMBER_OF_STEPS or breadth > MAX_NUMBER_OF_STEPS:
            raise InvalidParameterError(
                f"The TreeOfThoughts requires a breadth between {MIN_NUMBER_OF_STEPS} or {MAX_NUMBER_OF_STEPS}, but it was {breadth}"
            )

        if not isinstance(state_layers, list):
            raise InvalidParameterError(
                f"The TreeOfThoughts requires 'state_layers' to be a list, but it was: {state_layers}"
            )

        self._tree_of_thoughts_name = tree_of_thoughts_name

        self._tree = Tree(context_state)

        self._number_of_steps = number_of_steps
        self._breadth = breadth

        self._queue = deque(state_layers)

        self._request_response_from_ai_model_function = request_response_from_ai_model

        self._visual_output_active = False
        self._should_create_files = False

    def activate_visual_output(self):
        """Makes this class and other related functions output informative text to the console."""
        self._visual_output_active = True

    def activate_create_files(self):
        """Activates creating files to store responses to prompts, voting results, winners, etc."""
        self._should_create_files = True

    def set_request_response_from_ai_model_function(
        self, request_response_from_ai_model_function
    ):
        """Sets the function that will request responses from the AI model.
        Useful when you want to substitute it with a function that inputs to the user,
        or a fake one for test purposes.

        Args:
            request_response_from_ai_model_function (function): the function that will request a response from the AI model
        """
        self._request_response_from_ai_model_function = (
            request_response_from_ai_model_function
        )

    def _create_files_for_winners(self, winners):
        directory_path = get_directory_path_for_tree_of_thoughts(
            self._tree_of_thoughts_name
        )

        if self._should_create_files:
            create_directories(directory_path)

            for i, winner in enumerate(winners):
                file_path = create_file_path_for_winner(directory_path, winner, i)

                write_response_to_file(file_path, winner.name.get_response())

    def process_tree_of_thoughts(self):
        """Processes the whole tree of thoughts from start to finish. The options of the tree
        should have already been set properly.
        """
        state_type_of_last_winners = StateType.CONTEXT

        while self._queue:
            state_layer = self._queue.popleft()

            if not isinstance(state_layer, dict):
                error_message = f"The function '{self.process_tree_of_thoughts.__name__}' expected the popped value of the queue to be a dict, but it was: {state_layer}"
                raise ValueError(error_message)

            self._tree.add_state_type(
                state_layer["state_type"],
                state_type_of_last_winners,
                state_layer["state_type_text"],
                state_layer["include_ancestor_state_type_response"],
                self._number_of_steps,
                self._breadth,
            )

            request_responses(
                self._tree_of_thoughts_name,
                self._tree.get_leaf_nodes_without_responses(),
                self._visual_output_active,
                self._should_create_files,
                self._request_response_from_ai_model_function,
            )

            determine_winners(
                self._tree_of_thoughts_name,
                self._tree.get_unresolved_leaf_nodes_with_responses(),
                self._number_of_steps,
                self._should_create_files,
                self._request_response_from_ai_model_function,
            )

            self._create_files_for_winners(
                self._tree.get_winners_of_type(state_layer["state_type"], self._breadth)
            )

            # Set state type of these winners
            state_type_of_last_winners = state_layer["state_type"]

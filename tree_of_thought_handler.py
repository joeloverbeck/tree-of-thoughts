from collections import deque
from defines import get_directory_path_for_tree_of_thoughts
from enums import StateType
from file_utils import (
    create_directories,
    create_file_path_for_winner,
    write_response_to_file,
)
from state import State
from tree_of_thoughts import TreeOfThoughts


class TreeOfThoughtsHandler:
    def __init__(self, tree_of_thoughts_name, json_data):
        self._tree_of_thoughts_name = tree_of_thoughts_name

        self._tree_of_thoughts = TreeOfThoughts(
            tree_of_thoughts_name,
            State(json_data["context"], StateType.CONTEXT),
            json_data["number_of_steps"],
            json_data["breadth"],
        )

        self._queue = deque(json_data["state_layers"])

        self._should_create_files = False

    def activate_visual_output(self):
        self._tree_of_thoughts.activate_visual_output()

    def activate_create_files(self):
        self._should_create_files = True

        self._tree_of_thoughts.activate_create_files()

    def set_request_response_from_ai_model_function(
        self, request_response_from_ai_model_function
    ):
        self._tree_of_thoughts.set_request_response_from_ai_model_function(
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

    def handle_tree_of_thoughts(self):
        state_type_of_last_winners = StateType.CONTEXT

        while self._queue:
            current_state_type, text = self._queue.popleft()

            self._tree_of_thoughts.add_state_type(
                current_state_type, state_type_of_last_winners, text
            )

            self._tree_of_thoughts.request_responses()

            self._tree_of_thoughts.determine_winners()

            self._create_files_for_winners(
                self._tree_of_thoughts.get_winners_of_type(current_state_type)
            )

            # Set state type of these winners
            state_type_of_last_winners = current_state_type

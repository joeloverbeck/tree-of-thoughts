from anytree import Node
from colorama import Fore
from api_requests import request_response_from_ai_model
from defines import get_directory_path_for_tree_of_thoughts
from enums import StateType
from errors import (
    InvalidParameterError,
)
from file_utils import (
    create_directories,
    create_file_path_for_response,
)
from output import output_message
from responses import determine_response_for_node
from state import State
from voting import request_as_many_votes_as_steps


class TreeOfThoughts:
    def __init__(
        self, tree_of_thoughts_name, context_state, number_of_steps, breadth=1
    ):
        if not isinstance(context_state, State):
            raise InvalidParameterError(
                f"The TreeOfThoughts required a 'context_state' of type State, but it was: {context_state}"
            )

        if not context_state.get_state_type() == StateType.CONTEXT:
            raise InvalidParameterError(
                "Attempted to create a Tree of Thoughts with a state that wasn't of type CONTEXT."
            )

        self._tree_of_thoughts_name = tree_of_thoughts_name

        self._root_node = Node(context_state)
        self._number_of_steps = number_of_steps
        self._breadth = breadth

        self._request_response_from_ai_model_function = request_response_from_ai_model

        self._visual_output_active = False
        self._should_create_files = False

    def _add_new_state_to_leaf_node_according_to_steps(
        self, leaf_node, state_type, state_type_related_text
    ):
        for _ in range(self._number_of_steps):
            state = State(leaf_node.name.get_context(), state_type)
            state.set_state_type_related_text(state_type_related_text)

            Node(state, parent=leaf_node)

    def activate_visual_output(self):
        self._visual_output_active = True

    def activate_create_files(self):
        self._should_create_files = True

    def set_request_response_from_ai_model_function(
        self, request_response_from_ai_model_function
    ):
        self._request_response_from_ai_model_function = (
            request_response_from_ai_model_function
        )

    def add_state_type(
        self,
        state_type_of_new_state,
        state_type_of_last_winners,
        state_type_related_text,
    ):
        # Should only add state types to the winners (depending on breadth) of the leaf nodes
        resolved_leaf_nodes = [
            node
            for node in self._root_node.leaves
            if node.name.is_resolved()
            and node.name.get_state_type() == state_type_of_last_winners
        ]

        leaf_node_state_type = resolved_leaf_nodes[0].name.get_state_type()

        winners = self.get_winners_of_type(leaf_node_state_type)

        for winner in winners:
            self._add_new_state_to_leaf_node_according_to_steps(
                winner, state_type_of_new_state, state_type_related_text
            )

    def count_number_of_states_of_type(self, state_type):
        count = 0
        for node in self._root_node.descendants:
            if node.name.get_state_type() == state_type:
                count += 1
        return count

    def request_responses(self):
        # gets all unresolved nodes, then prompts the AI model for responses, that will be stored in the corresponding
        # state nodes.
        unresolved_leaf_nodes = [
            node for node in self._root_node.leaves if not node.name.has_response()
        ]

        # go through all these leaf nodes, requesting responses from the AI model
        for i, unresolved_leaf_node in enumerate(unresolved_leaf_nodes):
            output_message(
                Fore.LIGHTGREEN_EX,
                f"Requesting response from AI model for state '{unresolved_leaf_node.name.get_state_type().name.lower()}'...",
                self._visual_output_active,
            )

            # The response should either be requested from the AI model, or loaded from file if one is matching
            directory_path = get_directory_path_for_tree_of_thoughts(
                self._tree_of_thoughts_name
            )

            if self._should_create_files:
                create_directories(directory_path)

            unresolved_leaf_node.name.set_response(
                determine_response_for_node(
                    unresolved_leaf_node,
                    create_file_path_for_response(
                        directory_path, unresolved_leaf_node, i
                    ),
                    self._should_create_files,
                    self._request_response_from_ai_model_function,
                )
            )

            # sanity check
            if not unresolved_leaf_node.name.has_response():
                raise ValueError(
                    f"The function {self.request_responses.__name__} failed to set the response state of node {unresolved_leaf_node} properly."
                )

    def do_states_of_type_have_responses(self, state_type):
        nodes_of_type_with_responses = [
            node
            for node in self._root_node.leaves
            if node.name.has_response() and node.name.get_state_type() == state_type
        ]

        return len(nodes_of_type_with_responses) == self._number_of_steps

    def determine_winners(self):
        # Must collect all the responses of those leaf nodes with responses
        unresolved_leaf_nodes = [
            node
            for node in self._root_node.leaves
            if node.name.has_response() and not node.name.is_resolved()
        ]

        prompt = unresolved_leaf_nodes[0].name.get_context()

        prompt += f"\n\n{unresolved_leaf_nodes[0].name.get_state_type_related_text()}\n"

        for i, unresolved_leaf_node in enumerate(unresolved_leaf_nodes):
            prompt += f"\nAnswer {i + 1}: {unresolved_leaf_node.name.get_response()}"

        prompt += (
            "\n\nChoose the best answer. Use the format: 'The best answer is number X'."
        )

        request_as_many_votes_as_steps(
            self._tree_of_thoughts_name,
            self._number_of_steps,
            prompt,
            unresolved_leaf_nodes,
            self._should_create_files,
            self._request_response_from_ai_model_function,
        )

        for unresolved_leaf_node in unresolved_leaf_nodes:
            unresolved_leaf_node.name.consider_resolved()

    def get_winners_of_type(self, state_type):
        # Must collect all leaf nodes that are considered resolved and that are of the specified type
        resolved_leaf_nodes = [
            node
            for node in self._root_node.leaves
            if node.name.is_resolved() and node.name.get_state_type() == state_type
        ]

        # Sort the nodes in descending order of vote counts
        sorted_nodes = sorted(
            resolved_leaf_nodes, key=lambda node: node.name.get_votes(), reverse=True
        )

        # Return the first '_breadth' nodes
        return list(sorted_nodes[: self._breadth])

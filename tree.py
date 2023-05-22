"""This module contains the class Tree, that handles the nodes and links of a tree of thoughts.
"""
from anytree import Node
from enums import StateType
from errors import InvalidParameterError
from node_utils import create_child_state_node

from state import State


class Tree:
    """This class handles the nodes and their relationships involved in a tree of thoughts."""

    def __init__(self, context_state):
        if not isinstance(context_state, State):
            raise InvalidParameterError(
                f"During creation of a Tree, the 'context_state' passed wasn't a State: {context_state}"
            )

        self._root_node: Node = Node(context_state)

    def get_winners_of_type(self, state_type: StateType, breadth: int) -> list[Node]:
        """Returns the winning nodes of a specific state type

        Args:
            state_type (StateType): the state type that the winners will be returned from
            breadth (int): the amount of winners that will be chosen among those of a state type

        Returns:
            list[Node]: the winners of the specific state type
        """
        # Must collect all leaf nodes that are considered resolved and that are of the specified type
        resolved_leaf_nodes = [
            node
            for node in self._root_node.leaves
            if node.name.is_resolved() and node.name.get_state_type() == state_type
        ]

        if len(resolved_leaf_nodes) < breadth:
            error_message = f"The function {self.get_winners_of_type.__name__} found less resolved leaf nodes ({len(resolved_leaf_nodes)}) "
            error_message += f"than the specified breadth ({breadth})."
            raise ValueError(error_message)

        # Sort the nodes in descending order of vote counts
        sorted_nodes = sorted(
            resolved_leaf_nodes, key=lambda node: node.name.get_votes(), reverse=True
        )

        # Return the first '_breadth' nodes
        return list(sorted_nodes[:breadth])

    def add_state_type(
        self,
        state_type_of_new_state: StateType,
        state_type_of_last_winners: StateType,
        state_type_related_text: str,
        number_of_steps: int,
        breadth: int,
    ) -> None:
        """Adds a new state to the tree, of the determined state type

        Args:
            state_type_of_new_state (StateType): the state type that the new state will have
            state_type_of_last_winners (StateType): the state type of the last layer of winners
            state_type_related_text (str): the text associated with the new type of state
            number_of_steps (int): the number of steps that this layer of states will have
            breadth (int): now many winners will be picked among those voted the most
        """
        winners = self.get_winners_of_type(state_type_of_last_winners, breadth)

        for winner in winners:
            for _ in range(number_of_steps):
                create_child_state_node(
                    state_type_of_new_state, state_type_related_text, winner
                )

    def get_unresolved_leaf_nodes_with_responses(self) -> list[Node]:
        """Returns the leaf nodes of the tree that are unresolved and have responses stored in them

        Returns:
            list[Node]: the list of leaf nodes that are unresolved and have responses
        """
        return [
            node
            for node in self._root_node.leaves
            if node.name.has_response() and not node.name.is_resolved()
        ]

    def get_leaf_nodes_without_responses(self) -> list[Node]:
        """Returns the leaf nodes that don't have responses stored in them

        Returns:
            list[Node]: returns a list of leaf nodes that don't have responses stored in them
        """
        return [node for node in self._root_node.leaves if not node.name.has_response()]

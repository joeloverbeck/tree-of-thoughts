from anytree import Node
from enums.state_type import StateType
from state import State


def create_child_state_node(
    state_type: StateType,
    state_type_related_text: str,
    include_ancestor_state_type_response: StateType | None,
    leaf_node: Node,
):
    state = State(leaf_node.name.get_context(), state_type)
    state.set_state_type_related_text(state_type_related_text)
    state.set_include_ancestor_state_type_response(include_ancestor_state_type_response)

    Node(state, parent=leaf_node)

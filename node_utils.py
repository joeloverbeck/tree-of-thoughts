from anytree import Node
from state import State


def create_child_state_node(state_type, state_type_related_text, leaf_node):
    state = State(leaf_node.name.get_context(), state_type)
    state.set_state_type_related_text(state_type_related_text)

    Node(state, parent=leaf_node)

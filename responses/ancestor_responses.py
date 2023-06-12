from anytree import Node
from defines import DOUBLE_RETURNS
from errors import AncestorStateTypeNotFoundError


def determine_ancestor_with_required_state_type(
    unresolved_leaf_node: Node,
) -> Node | None:
    """Determines which is the ancestor with the required state type, according to
    the attribte 'include_ancestor_state_type_response' already set in the State.

    Args:
        unresolved_leaf_node (Node): a node that contains a state.

    Returns:
        Node | None: either the corresponding ancestor node or None
    """
    required_state_type = (
        unresolved_leaf_node.name.get_include_ancestor_state_type_response()
    )

    for ancestor in unresolved_leaf_node.ancestors:
        if ancestor.name.get_state_type() == required_state_type:
            return ancestor

    return None


def state_name_of_ancestor_state_type(ancestor_with_required_state_type):
    return f"{DOUBLE_RETURNS}{ancestor_with_required_state_type.name.get_state_type().name}:"


def state_response_of_ancestor(ancestor_with_required_state_type):
    return f"{DOUBLE_RETURNS}{ancestor_with_required_state_type.name.get_response()}"


def state_ancestor_of_expected_type_wasnt_found(
    unresolved_leaf_node, include_ancestor_state_type_response
):
    return f"Couldn't find an ancestor of type '{include_ancestor_state_type_response}' for node {unresolved_leaf_node}"


def determine_if_an_ancestor_response_should_be_included(
    unresolved_leaf_node: Node, prompt: str
) -> str:
    """Determines if an ancestor's response should be included in the prompt, and if so,
    includes it in the prompt

    Args:
        unresolved_leaf_node (Node): the unresolved leaf node.
        prompt (str): the prompt that will eventually be sent to an AI model for a response.

    Returns:
        str: the prompt, that might include the response from the specified ancestor.
    """
    if prompt is None:
        prompt = ""

    include_ancestor_state_type_response = (
        unresolved_leaf_node.name.get_include_ancestor_state_type_response()
    )

    if include_ancestor_state_type_response is not None:
        # We must find in the ancestors of 'unresolved_leaf_node.name' a node that contains a state with the type 'include_ancestor_state_type_response'
        ancestor_with_required_state_type = determine_ancestor_with_required_state_type(
            unresolved_leaf_node
        )

        if ancestor_with_required_state_type is None:
            raise AncestorStateTypeNotFoundError(
                state_ancestor_of_expected_type_wasnt_found(
                    unresolved_leaf_node, include_ancestor_state_type_response
                )
            )

        # if the ancestor has been found, add his response to the prompt.
        prompt += state_name_of_ancestor_state_type(ancestor_with_required_state_type)
        prompt += state_response_of_ancestor(ancestor_with_required_state_type)

        return prompt

    return prompt

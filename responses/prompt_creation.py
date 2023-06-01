from anytree import Node
from defines import DOUBLE_RETURNS
from enums.state_type import StateType
from errors import InvalidParameterError
from file_utils import create_file_path_for_response


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


def determine_if_an_ancestor_response_should_be_included(
    unresolved_leaf_node: Node, prompt: str
):
    """Determines if an ancestor's response should be included in the prompt, and if so,
    includes it in the prompt

    Args:
        unresolved_leaf_node (Node): the unresolved leaf node.
        prompt (str): the prompt that will eventually be sent to an AI model for a response.
    """
    include_ancestor_state_type_response = (
        unresolved_leaf_node.name.get_include_ancestor_state_type_response()
    )

    if include_ancestor_state_type_response is not None:
        # We must find in the ancestors of 'unresolved_leaf_node.name' a node that contains a state with the type 'include_ancestor_state_type_response'
        ancestor_with_required_state_type = determine_ancestor_with_required_state_type(
            unresolved_leaf_node
        )

        # if the ancestor has been found, add his response to the prompt.
        if ancestor_with_required_state_type is not None:
            prompt += f"{DOUBLE_RETURNS}{ancestor_with_required_state_type.name.get_state_type().name}:"
            prompt += f"{DOUBLE_RETURNS}{ancestor_with_required_state_type.name.get_response()}"


def create_prompt_for_response(unresolved_leaf_node: Node) -> str:
    """Creates a prompt to generate a response from the AI model.

    Args:
        unresolved_leaf_node (Node): an unresolved leaf node from the tree

    Returns:
        str: the prompt that will be sent to the AI model.

    Raises:
        InvalidParameterError: if 'unresolved_leaf_node' is not a node
    """
    if not isinstance(unresolved_leaf_node, Node):
        raise InvalidParameterError(
            f"The function {create_file_path_for_response.__name__} received an 'unresolved_leaf_node' that wasn't a Node: {unresolved_leaf_node}"
        )

    prompt = f"{unresolved_leaf_node.name.get_context()}"

    determine_if_an_ancestor_response_should_be_included(unresolved_leaf_node, prompt)

    # Must add to the prompt the response of this node's parent.
    if unresolved_leaf_node.parent.name.get_state_type() != StateType.CONTEXT:
        prompt += f"{DOUBLE_RETURNS}{unresolved_leaf_node.parent.name.get_response()}"

    if unresolved_leaf_node.name.get_state_type() != StateType.CONTEXT:
        prompt += (
            f"{DOUBLE_RETURNS}{unresolved_leaf_node.name.get_state_type_related_text()}"
        )

    return prompt

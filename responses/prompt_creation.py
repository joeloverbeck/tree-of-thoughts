from anytree import Node
from defines import DOUBLE_RETURNS
from enums.state_type import StateType
from errors import InvalidParameterError
from file_utils import create_file_path_for_response
from responses.ancestor_responses import (
    determine_if_an_ancestor_response_should_be_included,
)


def add_to_prompt_the_response_of_parent(
    unresolved_leaf_node: Node, prompt: str
) -> str:
    """Adds to the prompt the response of the unresolved leaf node's parent.

    Args:
        unresolved_leaf_node (Node): the unresolved leaf node.
        prompt (str): the prompt.

    Raises:
        ValueError: if the parent's response is None.

    Returns:
        str: the prompt, now including the parent's response.
    """
    if unresolved_leaf_node.parent.name.get_response() is None:
        error_message = "When attempting to add to a prompt the response from the current node's parent, "
        error_message += f"found that the parent didn't have a response associated. Parent: {unresolved_leaf_node.parent}"
        raise ValueError(error_message)

    prompt += f"{DOUBLE_RETURNS}{unresolved_leaf_node.parent.name.get_response()}"

    return prompt


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

    if unresolved_leaf_node.name.get_context() is None:
        error_message = "When attempting to create the prompt for a response, found that the unresolved leaf node doesn't have a context set: "
        error_message += f"{unresolved_leaf_node}"
        raise ValueError(error_message)

    prompt = determine_if_an_ancestor_response_should_be_included(
        unresolved_leaf_node, f"{unresolved_leaf_node.name.get_context()}"
    )

    if unresolved_leaf_node.parent.name.get_state_type() != StateType.CONTEXT:
        prompt = add_to_prompt_the_response_of_parent(unresolved_leaf_node, prompt)

    if unresolved_leaf_node.name.get_state_type() != StateType.CONTEXT:
        prompt += (
            f"{DOUBLE_RETURNS}{unresolved_leaf_node.name.get_state_type_related_text()}"
        )

    return prompt

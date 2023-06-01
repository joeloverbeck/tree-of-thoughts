"""This module contains functions associated with handling and producing responses from AI models.
"""
from typing import Callable
from anytree import Node
from errors import InvalidParameterError
from file_utils import (
    read_contents_of_file_if_it_exists,
    write_response_to_file,
)
from responses.prompt_creation import create_prompt_for_response


def determine_response_for_node(
    unresolved_leaf_node: Node,
    file_path: str,
    should_create_files: bool,
    request_response_from_ai_model_function: Callable[[str], str],
) -> str:
    """Determines a response for an unresolved leaf node, relying on the AI model.

    Args:
        unresolved_leaf_node (Node): the unresolved leaf node for which a response will be requested
        file_path (str): the file path where the response should be saved to file
        should_create_files (bool): whether or not a file should be created for this response
        request_response_from_ai_model_function (Callable[[str], str]): the function that will request a response from the AI model

    Returns:
        str: the response received from the AI model

    Raises:
        InvalidParameterError: if 'unresolved_leaf_node' is not a node
    """
    if not isinstance(unresolved_leaf_node, Node):
        raise InvalidParameterError(
            f"The function {determine_response_for_node.__name__} received an 'unresolved_leaf_node' that wasn't a Node: {unresolved_leaf_node}"
        )

    response = None

    if should_create_files:
        response = read_contents_of_file_if_it_exists(file_path)

    if response is None:
        response = request_response_from_ai_model_function(
            create_prompt_for_response(unresolved_leaf_node)
        )

        # Write the response to a file
        if should_create_files:
            write_response_to_file(file_path, response)

    return response

"""This module contains functions associated with handling and producing responses from AI models.
"""
from typing import Callable
from anytree import Node
from colorama import Fore
from defines import DOUBLE_RETURNS, get_directory_path_for_tree_of_thoughts
from enums import StateType
from errors import InvalidParameterError
from file_utils import (
    create_directories,
    create_file_path_for_response,
    read_contents_of_file_if_it_exists,
    write_response_to_file,
)
from output import output_message


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

    # Must add to the prompt the response of this node's parent.
    if unresolved_leaf_node.parent.name.get_state_type() != StateType.CONTEXT:
        prompt += f"{DOUBLE_RETURNS}{unresolved_leaf_node.parent.name.get_response()}"

    if unresolved_leaf_node.name.get_state_type() != StateType.CONTEXT:
        prompt += (
            f"{DOUBLE_RETURNS}{unresolved_leaf_node.name.get_state_type_related_text()}"
        )

    return prompt


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


def request_responses(
    tree_of_thoughts_name: str,
    leaf_nodes_without_responses: list[Node],
    visual_output_active: bool,
    should_create_files: bool,
    request_response_from_ai_model_function: Callable[[str], str],
) -> None:
    """Requests responses from the AI model for the leaf nodes without responses

    Args:
        tree_of_thoughts_name (str): the name of the associated tree of thoughts
        leaf_nodes_without_responses (list[Node]): the leaf nodes without responses
        visual_output_active (bool): whether or not the visual output should be active
        should_create_files (bool): whether or not files should be created for the responses
        request_response_from_ai_model_function (Callable[[str], str]): the function that will handle requesting responses from the AI model

    Raises:
        InvalidParameterError: if 'leaf_nodes_without_responses' is not a list
        ValueError: if any unresolved leaf node is left without a response by the end of the process
    """
    if not isinstance(leaf_nodes_without_responses, list):
        error_message = f"The function '{request_responses.__name__}' requires 'unresolved_leaf_nodes_without_responses' to be a list, "
        error_message += f"but it was: {leaf_nodes_without_responses}"
        raise InvalidParameterError(error_message)

    # go through all these leaf nodes, requesting responses from the AI model
    for i, unresolved_leaf_node in enumerate(leaf_nodes_without_responses):
        output_message(
            Fore.LIGHTGREEN_EX,
            f"Requesting response from AI model for state '{unresolved_leaf_node.name.get_state_type().name.lower()}'...",
            visual_output_active,
        )

        # The response should either be requested from the AI model, or loaded from file if one is matching
        directory_path = get_directory_path_for_tree_of_thoughts(tree_of_thoughts_name)

        if should_create_files:
            create_directories(directory_path)

        unresolved_leaf_node.name.set_response(
            determine_response_for_node(
                unresolved_leaf_node,
                create_file_path_for_response(directory_path, unresolved_leaf_node, i),
                should_create_files,
                request_response_from_ai_model_function,
            )
        )

        # sanity check
        if not unresolved_leaf_node.name.has_response():
            raise ValueError(
                f"The function {request_responses.__name__} failed to set the response state of node {unresolved_leaf_node} properly."
            )

from enums import StateType
from file_utils import read_contents_of_file_if_it_exists, write_response_to_file


def create_prompt_for_response(unresolved_leaf_node):
    prompt = f"{unresolved_leaf_node.name.get_context()}"

    # Must add to the prompt the response of this node's parent.
    if unresolved_leaf_node.parent.name.get_state_type() != StateType.CONTEXT:
        prompt += f"\n\n{unresolved_leaf_node.parent.name.get_response()}"

    if unresolved_leaf_node.name.get_state_type() != StateType.CONTEXT:
        prompt += f"\n\n{unresolved_leaf_node.name.get_state_type_related_text()}"

    return prompt


def determine_response_for_node(
    unresolved_leaf_node,
    file_path,
    should_create_files,
    request_response_from_ai_model_function,
):
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

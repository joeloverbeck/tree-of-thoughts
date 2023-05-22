from defines import (
    DOUBLE_RETURNS,
    VOTING_STRING_FOR_AI_MODEL,
    get_directory_path_for_tree_of_thoughts,
)
from errors import UnableToExtractVoteFromResponse
from file_utils import (
    create_directories,
    create_file_path_for_vote,
    read_contents_of_file_if_it_exists,
    write_response_to_file,
)
from regular_expressions import extract_vote


def determine_vote_for_step(
    prompt,
    directory_path,
    i,
    unresolved_leaf_nodes,
    should_create_files,
    request_response_from_ai_model_function,
):
    file_path = create_file_path_for_vote(
        directory_path, unresolved_leaf_nodes[i - 1], i
    )

    response = None

    if should_create_files:
        response = read_contents_of_file_if_it_exists(file_path)

    if response is None:
        response = request_response_from_ai_model_function(prompt)

    voted_answer = extract_vote(response.lower())

    if voted_answer is None:
        error_message = f"Was unable to determine the vote given the following response from the AI model: {response}\n"
        error_message += (
            "The response should contain the text 'best answer is number X'."
        )
        raise UnableToExtractVoteFromResponse(error_message)

    # Write the response to a file, now that we know that it contains a valid vote
    if should_create_files:
        write_response_to_file(file_path, response)

    unresolved_leaf_nodes[voted_answer - 1].name.add_vote()


def request_as_many_votes_as_steps(
    tree_of_thoughts_name,
    number_of_steps,
    prompt,
    unresolved_leaf_nodes,
    should_create_files,
    request_response_from_ai_model_function,
):
    directory_path = get_directory_path_for_tree_of_thoughts(tree_of_thoughts_name)

    if should_create_files:
        create_directories(directory_path)

    for i in range(number_of_steps):
        determine_vote_for_step(
            prompt,
            directory_path,
            i,
            unresolved_leaf_nodes,
            should_create_files,
            request_response_from_ai_model_function,
        )


def determine_winners(
    tree_of_thoughts_name,
    unresolved_leaf_nodes_with_responses,
    number_of_steps,
    should_create_files,
    request_response_from_ai_model_function,
):
    prompt = unresolved_leaf_nodes_with_responses[0].name.get_context()

    prompt += f"{DOUBLE_RETURNS}{unresolved_leaf_nodes_with_responses[0].name.get_state_type_related_text()}\n"

    for i, unresolved_leaf_node in enumerate(unresolved_leaf_nodes_with_responses):
        prompt += f"\nAnswer {i + 1}: {unresolved_leaf_node.name.get_response()}"

    prompt += f"{DOUBLE_RETURNS}Choose the best answer. Use the format: '{VOTING_STRING_FOR_AI_MODEL}'."

    request_as_many_votes_as_steps(
        tree_of_thoughts_name,
        number_of_steps,
        prompt,
        unresolved_leaf_nodes_with_responses,
        should_create_files,
        request_response_from_ai_model_function,
    )

    for unresolved_leaf_node in unresolved_leaf_nodes_with_responses:
        unresolved_leaf_node.name.consider_resolved()

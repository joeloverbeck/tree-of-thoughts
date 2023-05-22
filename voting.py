from defines import get_directory_path_for_tree_of_thoughts
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
        raise UnableToExtractVoteFromResponse(
            f"Was unable to determine the vote given the following response from the AI model: {response}\nThe response should contain the text 'best answer is number X'."
        )

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

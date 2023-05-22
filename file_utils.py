import os


def create_directories(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def create_file_path_for_response(directory_path, node, i):
    return f"{directory_path}/{node.name.get_state_type().name.lower()}_{i + 1}.txt"


def create_file_path_for_vote(directory_path, node, i):
    return (
        f"{directory_path}/{node.name.get_state_type().name.lower()}_vote_{i + 1}.txt"
    )


def create_file_path_for_winner(directory_path, node, i):
    return (
        f"{directory_path}/{node.name.get_state_type().name.lower()}_winner_{i + 1}.txt"
    )


def read_contents_of_file_if_it_exists(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf8") as file:
            return file.read().strip()

    return None


def write_response_to_file(file_path, response):
    with open(file_path, "w", encoding="utf8") as file:
        file.write(response)

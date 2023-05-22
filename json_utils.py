import os
import json

from defines import TREES_OF_THOUGHTS_DIRECTORY
from enums import StateType
from errors import MissingContextFileError
from file_utils import read_contents_of_file_if_it_exists


def load_tree_of_thoughts(tree_of_thoughts_name):
    with open(
        f"{TREES_OF_THOUGHTS_DIRECTORY}/{tree_of_thoughts_name.lower()}.json",
        encoding="utf8",
    ) as file:
        return json.load(file)


def convert_raw_json_data(tree_of_thoughts_name, raw_json_data):
    converted_json_data = raw_json_data

    # Note: we gotta load the file '{tree_of_thoughts_name}_context.txt' into 'converted_json_data["context"]'
    context_file_path = (
        f"{TREES_OF_THOUGHTS_DIRECTORY}/{tree_of_thoughts_name.lower()}_context.txt"
    )
    if not os.path.isfile(context_file_path):
        raise MissingContextFileError(
            f"The function {convert_raw_json_data.__name__} expected a context file to exist at {context_file_path}."
        )

    converted_json_data["context"] = read_contents_of_file_if_it_exists(
        context_file_path
    )

    converted_json_data["number_of_steps"] = int(converted_json_data["number_of_steps"])
    converted_json_data["breadth"] = int(converted_json_data["breadth"])

    for i, state_layer in enumerate(converted_json_data["state_layers"]):
        state_type_str, state_text = state_layer
        state_type_enum = StateType[state_type_str]

        converted_json_data["state_layers"][i] = (state_type_enum, state_text)

    return converted_json_data

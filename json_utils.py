import os
import json

from defines import TREES_OF_THOUGHTS_DIRECTORY
from enums import StateType
from errors import InvalidStateTypeError, MissingContextFileError
from file_utils import read_contents_of_file_if_it_exists


def load_tree_of_thoughts(tree_of_thoughts_name):
    with open(
        f"{TREES_OF_THOUGHTS_DIRECTORY}/{tree_of_thoughts_name.lower()}.json",
        encoding="utf8",
    ) as file:
        return json.load(file)


def convert_raw_json_data(tree_of_thoughts_name: str, raw_json_data: dict) -> dict:
    """Converts the raw json data loaded from the json file into a dict with the program structures.

    Args:
        tree_of_thoughts_name (str): the name of the tree of thoughts this json data corresponds to.
        raw_json_data (dict): the raw json data loaded from the json file

    Raises:
        MissingContextFileError: if the context file for the tree of thoughts doesn't exist
        InvalidStateTypeError: if any of the state types contained in the json file are invalid

    Returns:
        dict: _description_
    """
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
        try:
            state_type_enum = StateType[state_type_str]
        except KeyError as exception:
            error_message = f"Failed to convert the raw json data to the program structures because the state type '{state_type_str}' is unrecognized.\n"
            error_message += f"Fix the json file of your tree of thoughts named '{tree_of_thoughts_name}'."
            raise InvalidStateTypeError(error_message) from exception

        converted_json_data["state_layers"][i] = (state_type_enum, state_text)

    return converted_json_data

import argparse
from colorama import Fore
from enums import StateType
from errors import InvalidStateTypeError, RequestToAiModelFailedError

from json_utils import convert_raw_json_data, load_tree_of_thoughts
from output import output_message
from state import State
from tree_of_thoughts import TreeOfThoughts


def main():
    parser = argparse.ArgumentParser(
        description="Executes a tree of thoughts, but sending the prompts to the user"
    )
    parser.add_argument(
        "tree_of_thoughts_name",
        help="Name of the tree of thoughts (json name must match)",
    )

    args = parser.parse_args()

    if not args.tree_of_thoughts_name:
        print("Error: The name of the tree of thoughts cannot be empty")
        return None

    try:
        json_data = convert_raw_json_data(
            args.tree_of_thoughts_name,
            load_tree_of_thoughts(args.tree_of_thoughts_name),
        )
    except InvalidStateTypeError as exception:
        print(f"Error:\n{exception}")
        return

    tree_of_thoughts = TreeOfThoughts(
        args.tree_of_thoughts_name,
        State(json_data["context"], StateType.CONTEXT),
        json_data["state_layers"],
        json_data["number_of_steps"],
        json_data["breadth"],
    )

    tree_of_thoughts.activate_visual_output()
    tree_of_thoughts.activate_create_files()

    try:
        tree_of_thoughts.process_tree_of_thoughts()
    except RequestToAiModelFailedError as exception:
        output_message(
            Fore.LIGHTRED_EX,
            f"Execution of the tree of thoughts failed while requesting a response from the AI model: {exception}",
            True,
        )


if __name__ == "__main__":
    main()

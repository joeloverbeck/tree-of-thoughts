import argparse
from colorama import Fore
from errors import RequestToAiModelFailedError

from json_utils import convert_raw_json_data, load_tree_of_thoughts
from output import output_message
from tree_of_thought_handler import TreeOfThoughtsHandler


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

    json_data = convert_raw_json_data(
        args.tree_of_thoughts_name, load_tree_of_thoughts(args.tree_of_thoughts_name)
    )

    tree_of_thoughts_handler = TreeOfThoughtsHandler(
        args.tree_of_thoughts_name, json_data
    )

    tree_of_thoughts_handler.activate_visual_output()
    tree_of_thoughts_handler.activate_create_files()

    try:
        tree_of_thoughts_handler.handle_tree_of_thoughts()
    except RequestToAiModelFailedError as exception:
        output_message(
            Fore.LIGHTRED_EX,
            f"Execution of the tree of thoughts failed while requesting a response from the AI model: {exception}",
            True,
        )


if __name__ == "__main__":
    main()

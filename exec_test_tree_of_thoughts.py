import argparse
from defines import INSTRUCT_GPT_PROMPT_ANSWER_OPENING, INSTRUCT_GPT_PROMPT_HEADER
from enums.state_type import StateType
from errors import InvalidStateTypeError

from json_utils import convert_raw_json_data, load_tree_of_thoughts
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
    except UnicodeDecodeError as exception:
        print(f"There are invalid characters in the json file. Error: {exception}")
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

    def user_input_request_response_function(prompt):
        return input(
            f"\n{INSTRUCT_GPT_PROMPT_HEADER}{prompt}{INSTRUCT_GPT_PROMPT_ANSWER_OPENING}\n"
        )

    tree_of_thoughts.set_request_response_from_ai_model_function(
        user_input_request_response_function
    )

    tree_of_thoughts.process_tree_of_thoughts()


if __name__ == "__main__":
    main()

import argparse
from defines import INSTRUCT_GPT_PROMPT_ANSWER_OPENING, INSTRUCT_GPT_PROMPT_HEADER

from json_utils import convert_raw_json_data, load_tree_of_thoughts
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

    def user_input_request_response_function(prompt):
        return input(
            f"\n{INSTRUCT_GPT_PROMPT_HEADER}{prompt}{INSTRUCT_GPT_PROMPT_ANSWER_OPENING}\n"
        )

    tree_of_thoughts_handler.set_request_response_from_ai_model_function(
        user_input_request_response_function
    )

    tree_of_thoughts_handler.handle_tree_of_thoughts()


if __name__ == "__main__":
    main()

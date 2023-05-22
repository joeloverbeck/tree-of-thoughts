INSTRUCT_GPT_PROMPT_HEADER = "Question. "
INSTRUCT_GPT_PROMPT_ANSWER_OPENING = (
    " Answer: Let's try to work out the answer step by step: "
)

TREES_OF_THOUGHTS_DIRECTORY = "trees_of_thoughts"


def get_directory_path_for_tree_of_thoughts(tree_of_thoughts_name):
    return f"{TREES_OF_THOUGHTS_DIRECTORY}/{tree_of_thoughts_name.lower()}"
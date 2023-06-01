import unittest
from enums.state_type import StateType
from errors import InvalidParameterError

from state import State
from tree_of_thoughts import TreeOfThoughts


class TestTreeOfThoughts(unittest.TestCase):
    def test_can_create_tree_of_thoughts(self):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        context_state = State(prompt, StateType.CONTEXT)

        tree_of_thoughts = TreeOfThoughts(
            "test",
            context_state,
            [
                (StateType.PLANNING, "Planning context"),
                (StateType.IMPLEMENTATION, "Implementation context"),
            ],
            5,
            1,
        )

        self.assertTrue(isinstance(tree_of_thoughts, TreeOfThoughts))

    def test_if_attempting_to_create_tree_of_thoughts_with_state_other_than_of_type_context_it_will_crash(
        self,
    ):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        planning_state = State(prompt, StateType.PLANNING)

        with self.assertRaises(InvalidParameterError):
            TreeOfThoughts(
                "test",
                planning_state,
                [
                    (StateType.PLANNING, "Planning context"),
                    (StateType.IMPLEMENTATION, "Implementation context"),
                ],
                5,
                1,
            )


if __name__ == "__main__":
    unittest.main()

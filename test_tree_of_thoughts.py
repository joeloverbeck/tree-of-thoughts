import unittest
from enums import StateType
from errors import InvalidParameterError

from state import State
from tree_of_thoughts import TreeOfThoughts


class TestTreeOfThoughts(unittest.TestCase):
    def test_can_create_tree_of_thoughts(self):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        context_state = State(prompt, StateType.CONTEXT)

        tree_of_thoughts = TreeOfThoughts("test", context_state, 5)

        self.assertTrue(isinstance(tree_of_thoughts, TreeOfThoughts))

    def test_if_attempting_to_create_tree_of_thoughts_with_state_other_than_of_type_context_it_will_crash(
        self,
    ):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        planning_state = State(prompt, StateType.PLANNING)

        with self.assertRaises(InvalidParameterError):
            TreeOfThoughts("test", planning_state, 5)

    def test_can_add_state_type_to_tree_of_thoughts(self):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        context_state = State(prompt, StateType.CONTEXT)

        tree_of_thoughts = TreeOfThoughts("test", context_state, 5)

        tree_of_thoughts.add_state_type(
            StateType.PLANNING,
            StateType.CONTEXT,
            "Develop a plan for how to write the scene using the summary as well as the notes.",
        )

        self.assertEqual(
            tree_of_thoughts.count_number_of_states_of_type(StateType.PLANNING), 5
        )

    def test_can_request_responses(self):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        context_state = State(prompt, StateType.CONTEXT)

        tree_of_thoughts = TreeOfThoughts("test", context_state, 5)

        tree_of_thoughts.add_state_type(
            StateType.PLANNING,
            StateType.CONTEXT,
            "Develop a plan for how to write the scene using the summary as well as the notes.",
        )

        self.assertEqual(
            tree_of_thoughts.count_number_of_states_of_type(StateType.PLANNING), 5
        )

        def fake_request_response_function(_prompt):
            return "Response"

        tree_of_thoughts.set_request_response_from_ai_model_function(
            fake_request_response_function
        )

        tree_of_thoughts.request_responses()

        self.assertTrue(
            tree_of_thoughts.do_states_of_type_have_responses(StateType.PLANNING)
        )

    def test_can_determine_winner_among_unresolved_state_nodes(self):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        context_state = State(prompt, StateType.CONTEXT)

        tree_of_thoughts = TreeOfThoughts("test", context_state, 5)

        tree_of_thoughts.add_state_type(
            StateType.PLANNING,
            StateType.CONTEXT,
            "Develop a plan for how to write the scene using the summary as well as the notes.",
        )

        self.assertEqual(
            tree_of_thoughts.count_number_of_states_of_type(StateType.PLANNING), 5
        )

        def fake_request_response_function(_prompt):
            return "Response"

        tree_of_thoughts.set_request_response_from_ai_model_function(
            fake_request_response_function
        )

        tree_of_thoughts.request_responses()

        self.assertTrue(
            tree_of_thoughts.do_states_of_type_have_responses(StateType.PLANNING)
        )

        def fake_request_response_that_returns_vote_function(_prompt):
            return "The best answer is number 3"

        tree_of_thoughts.set_request_response_from_ai_model_function(
            fake_request_response_that_returns_vote_function
        )

        tree_of_thoughts.determine_winners()

        winners = tree_of_thoughts.get_winners_of_type(StateType.PLANNING)

        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].name.get_state_type(), StateType.PLANNING)

    def test_can_add_new_state_type_when_state_type_has_been_resolved(self):
        prompt = "Given the following summary of the recent events in the fictional narrative:\nStuff happened.\nGiven the following notes to develop the scene:\nNotes."

        context_state = State(prompt, StateType.CONTEXT)

        tree_of_thoughts = TreeOfThoughts("test", context_state, 5)

        tree_of_thoughts.add_state_type(
            StateType.PLANNING,
            StateType.CONTEXT,
            "Develop a plan for how to write the scene using the summary as well as the notes.",
        )

        def fake_request_response_function(_prompt):
            return "Response"

        tree_of_thoughts.set_request_response_from_ai_model_function(
            fake_request_response_function
        )

        tree_of_thoughts.request_responses()

        def fake_request_response_that_returns_vote_function(_prompt):
            return "The best answer is number 3"

        tree_of_thoughts.set_request_response_from_ai_model_function(
            fake_request_response_that_returns_vote_function
        )

        tree_of_thoughts.determine_winners()

        tree_of_thoughts.add_state_type(
            StateType.IMPLEMENTATION, StateType.PLANNING, "Implement the plan."
        )

        self.assertEqual(
            tree_of_thoughts.count_number_of_states_of_type(StateType.IMPLEMENTATION), 5
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from anytree import Node
from defines import DOUBLE_RETURNS
from enums import StateType

from responses import create_prompt_for_response
from state import State


class TestResponses(unittest.TestCase):
    def test_when_the_parent_of_a_leaf_node_has_a_response_it_appears_in_prompt_for_response(
        self,
    ):
        parent_node = Node(State("Parent node context.", StateType.PLANNING))

        parent_node.name.set_response("Parent node response.")

        unresolved_leaf_node = Node(
            State("Unresolved leaf node context.", StateType.IMPLEMENTATION),
            parent=parent_node,
        )

        unresolved_leaf_node.name.set_state_type_related_text("State related text.")

        prompt = create_prompt_for_response(unresolved_leaf_node)

        self.assertEqual(
            prompt,
            f"Unresolved leaf node context.{DOUBLE_RETURNS}Parent node response.{DOUBLE_RETURNS}State related text.",
        )


if __name__ == "__main__":
    unittest.main()

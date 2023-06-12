import unittest

from anytree import Node
from enums.state_type import StateType
from responses.ancestor_responses import (
    determine_if_an_ancestor_response_should_be_included,
)

from state import State


class TestAncestorResponses(unittest.TestCase):
    def test_when_ancestor_exists_it_should_add_to_prompt_the_expected_text(
        self,
    ):
        implementation_node = Node(State("context", StateType.IMPLEMENTATION))

        implementation_node.name.set_response("Implementation")

        research_node = Node(
            State("context", StateType.RESEARCH), parent=implementation_node
        )

        refinement_node = Node(
            State("context", StateType.REFINEMENT), parent=research_node
        )

        refinement_node.name.set_include_ancestor_state_type_response(
            StateType.IMPLEMENTATION
        )

        prompt = determine_if_an_ancestor_response_should_be_included(
            refinement_node, ""
        )

        self.assertEqual(prompt, "\n\nIMPLEMENTATION:\n\nImplementation")


if __name__ == "__main__":
    unittest.main()

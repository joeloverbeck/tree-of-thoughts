import unittest
from json_utils import convert_raw_json_data

from tree_of_thought_handler import TreeOfThoughtsHandler


class TestTreeOfThoughtsHandler(unittest.TestCase):
    def test_can_create_tree_of_thoughts_handler(self):
        json_data = {
            "number_of_steps": "5",
            "breadth": "1",
            "state_layers": [
                ("PLANNING", "Planning text"),
                ("IMPLEMENTATION", "Implementation text"),
            ],
        }

        tree_of_thoughts_handler = TreeOfThoughtsHandler(
            "test", convert_raw_json_data("test", json_data)
        )

        self.assertTrue(isinstance(tree_of_thoughts_handler, TreeOfThoughtsHandler))

    def test_can_handle_tree_of_thoughts(self):
        json_data = {
            "number_of_steps": "5",
            "breadth": "1",
            "state_layers": [
                ("PLANNING", "Planning text"),
                ("IMPLEMENTATION", "Implementation text"),
            ],
        }

        tree_of_thoughts_handler = TreeOfThoughtsHandler(
            "test", convert_raw_json_data("test", json_data)
        )

        self.assertTrue(isinstance(tree_of_thoughts_handler, TreeOfThoughtsHandler))

        def fake_request_response_function(_prompt):
            return "The best answer is number 3"

        tree_of_thoughts_handler.set_request_response_from_ai_model_function(
            fake_request_response_function
        )

        tree_of_thoughts_handler.handle_tree_of_thoughts()


if __name__ == "__main__":
    unittest.main()

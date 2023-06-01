import unittest
from enums.state_type import StateType
from json_utils import convert_raw_json_data


class TestJsonUtils(unittest.TestCase):
    def test_can_transform_json_raw_data_to_proper_structures(self):
        json_data = {
            "context_state": {"context": "Context text"},
            "number_of_steps": "5",
            "breadth": "1",
            "state_layers": [
                {
                    "state_type": "PLANNING",
                    "state_type_text": "Planning text",
                    "include_ancestor_state_type_response": None,
                },
                {
                    "state_type": "IMPLEMENTATION",
                    "state_type_text": "Implementation text",
                    "include_ancestor_state_type_response": None,
                },
            ],
        }

        json_data = convert_raw_json_data("test", json_data)

        self.assertEqual(json_data["number_of_steps"], 5)
        self.assertEqual(json_data["breadth"], 1)

        planning_layer = json_data["state_layers"][0]

        self.assertEqual(planning_layer["state_type"], StateType.PLANNING)
        self.assertEqual(planning_layer["state_type_text"], "Planning text")

        implementation_layer = json_data["state_layers"][1]

        self.assertEqual(implementation_layer["state_type"], StateType.IMPLEMENTATION)
        self.assertEqual(implementation_layer["state_type_text"], "Implementation text")


if __name__ == "__main__":
    unittest.main()

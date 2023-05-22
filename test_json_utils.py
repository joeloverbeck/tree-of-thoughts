import unittest
from enums import StateType
from json_utils import convert_raw_json_data


class TestJsonUtils(unittest.TestCase):
    def test_can_transform_json_raw_data_to_proper_structures(self):
        json_data = {
            "context_state": {"context": "Context text"},
            "number_of_steps": "5",
            "breadth": "1",
            "state_layers": [
                ("PLANNING", "Planning text"),
                ("IMPLEMENTATION", "Implementation text"),
            ],
        }

        json_data = convert_raw_json_data("test", json_data)

        self.assertEqual(json_data["number_of_steps"], 5)
        self.assertEqual(json_data["breadth"], 1)

        planning_layer = json_data["state_layers"][0]

        self.assertEqual(planning_layer[0], StateType.PLANNING)
        self.assertEqual(planning_layer[1], "Planning text")

        implementation_layer = json_data["state_layers"][1]

        self.assertEqual(implementation_layer[0], StateType.IMPLEMENTATION)
        self.assertEqual(implementation_layer[1], "Implementation text")


if __name__ == "__main__":
    unittest.main()

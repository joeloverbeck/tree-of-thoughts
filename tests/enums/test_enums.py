import unittest


from enums.state_type import StateType


class TestEnums(unittest.TestCase):
    def test_can_retrieve_name_of_state_type_as_expected(self):
        state_type = StateType.IMPLEMENTATION

        self.assertEqual(state_type.name, "IMPLEMENTATION")


if __name__ == "__main__":
    unittest.main()

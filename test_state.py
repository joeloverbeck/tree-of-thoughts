import unittest
from enums import StateType

from state import State


class TestState(unittest.TestCase):
    def test_can_create_a_state(self):
        prompt = ""
        state = State(prompt, StateType.CONTEXT)

        self.assertTrue(isinstance(state, State))


if __name__ == "__main__":
    unittest.main()

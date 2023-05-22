from enums import StateType


class State:
    def __init__(self, context, state_type):
        self._context = context
        self._state_type = state_type

        self._state_type_related_text = None

        self._response = None

        self._is_resolved = False

        # Mark as resolved if state_type is CONTEXT
        if self._state_type is StateType.CONTEXT:
            self._is_resolved = True

        self._votes = 0

    def set_state_type_related_text(self, state_type_related_text):
        self._state_type_related_text = state_type_related_text

    def get_context(self):
        return self._context

    def get_state_type(self):
        return self._state_type

    def get_state_type_related_text(self):
        return self._state_type_related_text

    def has_response(self):
        if self._response is None:
            return False

        return True

    def get_response(self):
        return self._response

    def set_response(self, response):
        self._response = response

    def is_resolved(self):
        return self._is_resolved

    def add_vote(self):
        self._votes += 1

    def get_votes(self):
        return self._votes

    def consider_resolved(self):
        self._is_resolved = True

    def __str__(self):
        return f"State: {self._state_type} | Is resolved: {self._is_resolved}"

    def __repr__(self) -> str:
        return self.__str__()

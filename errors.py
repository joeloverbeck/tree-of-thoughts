class MissingContextFileError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


class RequestToAiModelFailedError(Exception):
    pass


class UnableToExtractVoteFromResponse(Exception):
    pass


class InvalidStateTypeError(Exception):
    pass


class AncestorStateTypeNotFoundError(Exception):
    pass

class MissingStateRelatedTextError(Exception):
    pass


class MissingContextFileError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


class RequestToAiModelFailedError(Exception):
    pass


class UnableToExtractVoteFromResponse(Exception):
    pass

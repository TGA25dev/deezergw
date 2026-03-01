class ExpiredException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class NoRightOnMedia(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class UnknownException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

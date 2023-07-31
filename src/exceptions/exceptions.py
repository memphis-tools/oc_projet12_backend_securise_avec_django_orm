class ForeignKeyDependyException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsufficientPrivilegeException(Exception):
    pass


class SuppliedDataNotMatchModel(Exception):
    pass

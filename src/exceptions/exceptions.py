class ForeignKeyDependyException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsufficientPrivilegeException(Exception):
    pass


class MissingUpdateParamException(Exception):
    pass


class NewPasswordIsNotValidException(Exception):
    pass


class NewPasswordDoesRespectMinSpecialCharsException(Exception):
    pass


class NewPasswordDoesRespectForbiddenSpecialCharsException(Exception):
    pass


class OldPasswordNotValidException(Exception):
    pass


class SuppliedDataNotMatchModel(Exception):
    pass

class ApiQueryFailedException(Exception):
    pass


class ApplicationErrorException(Exception):
    pass


class AuthenticationCredentialsFailed(Exception):
    pass


class ForeignKeyDependyException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsufficientPrivilegeException(Exception):
    pass


class ContractAmountToPayException(Exception):
    pass


class CustomIdEmptyException(Exception):
    pass


class CustomIdMatchNothingException(Exception):
    pass


class LocationCustomIdAlReadyExists(Exception):
    pass


class MissingApiStaticFileException(Exception):
    pass


class MissingUpdateParamException(Exception):
    pass


class CollaboratorAlreadyExistException(Exception):
    pass


class CommercialCollaboratorIsNotAssignedToClient(Exception):
    pass


class CommercialCollaboratorIsNotAssignedToContract(Exception):
    pass


class ClientNotFoundWithClientId(Exception):
    pass


class ContractNotFoundWithContractId(Exception):
    pass


class SupportCollaboratorIsNotAssignedToEvent(Exception):
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

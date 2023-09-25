class ApiQueryFailedException(Exception):
    pass


class ApplicationErrorException(Exception):
    pass


class ApplicationCanNotBeInitializeFromOperatingSystemException(Exception):
    pass


class AuthenticationCredentialsFailed(Exception):
    pass


class ForeignKeyDependyException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InsufficientPrivilegeException(Exception):
    pass


class CommercialCanNotUpdateClientCommercialContactException(Exception):
    pass


class ContractAmountToPayException(Exception):
    pass


class ContractUnsignedException(Exception):
    pass


class ContractCanceledException(Exception):
    pass


class CustomIdEmptyException(Exception):
    pass


class RegistrationNumberEmptyException(Exception):
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


class RegistrationNumberAlreadyExistException(Exception):
    pass


class ContractAlreadyExistException(Exception):
    pass


class CompanyAlreadyExistException(Exception):
    pass


class RoleAlreadyExistException(Exception):
    pass


class DepartmentAlreadyExistException(Exception):
    pass


class EventAlreadyExistException(Exception):
    pass


class ClientAlreadyExistException(Exception):
    pass


class LocationAlreadyExistException(Exception):
    pass


class CommercialCollaboratorIsNotAssignedToClient(Exception):
    pass


class CommercialCollaboratorIsNotAssignedToContract(Exception):
    pass


class ClientNotFoundWithClientId(Exception):
    pass


class ContractNotFoundWithContractId(Exception):
    pass


class CompanyNotFoundWithCompanyId(Exception):
    pass


class EventNotFoundWithEventId(Exception):
    pass


class RoleNotFoundWithRoleId(Exception):
    pass


class DepartmentNotFoundWithDepartmentId(Exception):
    pass


class LocationNotFoundWithLocationId(Exception):
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


class OnlySuportMemberCanBeAssignedToEventSupportException(Exception):
    pass


class QueryFailureException(Exception):
    pass


class QueryStructureException(Exception):
    pass


class SuppliedDataNotMatchModel(Exception):
    pass


class EventAttachedContractStatusCanNotBeUpdateException(Exception):
    pass

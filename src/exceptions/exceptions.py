"""
Description:
Toutes les exceptions personnalisées.
"""


class ApiQueryFailedException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ApplicationErrorException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ApplicationCanNotBeInitializeFromOperatingSystemException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class AuthenticationCredentialsFailed(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ForeignKeyDependyException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """

    def __init__(self, message):
        super().__init__(message)


class InsufficientPrivilegeException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CommercialCanNotUpdateClientCommercialContactException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ContractAmountToPayException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ContractUnsignedException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ContractCanceledException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CustomIdEmptyException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class RegistrationNumberEmptyException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CustomIdMatchNothingException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class LocationCustomIdAlReadyExists(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class MissingApiStaticFileException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class MissingUpdateParamException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CollaboratorAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class RegistrationNumberAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ContractAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CompanyAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class RoleAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class DepartmentAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class EventAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ClientAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class LocationAlreadyExistException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CommercialCollaboratorIsNotAssignedToClient(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CommercialCollaboratorIsNotAssignedToContract(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ClientNotFoundWithClientId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class ContractNotFoundWithContractId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class CompanyNotFoundWithCompanyId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class EventNotFoundWithEventId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class RoleNotFoundWithRoleId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class DepartmentNotFoundWithDepartmentId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class LocationNotFoundWithLocationId(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class SupportCollaboratorIsNotAssignedToEvent(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class OnlySuportMemberCanBeAssignedToEventSupportException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class QueryFailureException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class QueryStructureException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class SuppliedDataNotMatchModel(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """


class EventAttachedContractStatusCanNotBeUpdateException(Exception):
    """
    Description: exception personnalisée pour gérer finement l'application.
    """

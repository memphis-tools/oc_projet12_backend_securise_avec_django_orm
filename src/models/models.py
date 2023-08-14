"""
Les modèles métier.

"""
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Date,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy_utils import ChoiceType
from datetime import date, datetime

try:
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from settings import settings
    from utils import utils


Base = declarative_base()
TRANSLATED_MONTHS = [
    ("janvier", "Jan"),
    ("février", "Feb"),
    ("mars", "Mar"),
    ("avril", "Apr"),
    ("mai", "May"),
    ("juin", "Jun"),
    ("juillet", "Jul"),
    ("aout", "Aug"),
    ("septembre", "Sep"),
    ("octobre", "Oct"),
    ("novembre", "Nov"),
    ("décembre", "Dec"),
]


def get_base():
    """
    Description: permet à AppViews:init_db d'atteindre la base de données.
    """
    return Base


def get_today_date():
    """
    Description: on permet le formatage type '18 avril 2021' du cahier des charges pour les Clients.
    """
    today = date.today()
    returned_date = f"{today.day}-{TRANSLATED_MONTHS[today.month-1][1]}-{today.year}"
    return returned_date


class ModelMixin:
    def get_id(self):
        return self.id


class Collaborator_Department(Base):
    """
    Description: table dédiée à référencer les départements des utilisateurs de l'application.
    Remarque:
    Nom de la classe doit correspondre au nom de __tablename__.
    Lien avec la requete SQL construite à partir des arguments (lors d'une vue filtrée).
    Voir filtered_db_model dans utils.rebuild_filter_query.
    """

    __tablename__ = "collaborator_department"
    id = Column(Integer, primary_key=True)
    department_id = Column(String(120), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )
    collaborator = relationship("Collaborator", back_populates="department")

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(department_id|{self.department_id})'
        descriptors += f',(name|{self.name})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        department_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "department_id": self.department_id,
            "name": self.name,
        }
        return department_dict

    @staticmethod
    def _get_keys():
        return [
            "name",
        ]


class Collaborator_Role(Base):
    """
    Description: table dédiée à référencer les rôles des utilisateurs /collaborateurs de l'application.
    """

    __tablename__ = "collaborator_role"
    id = Column(Integer, primary_key=True)
    role_id = Column(String(120), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )
    collaborator = relationship("Collaborator", back_populates="role")

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(role_id|{self.role_id})'
        descriptors += f',(name|{self.name})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        role_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "role_id": self.role_id,
            "name": self.name,
        }
        return role_dict

    @staticmethod
    def _get_keys():
        return [
            "name",
        ]


class Collaborator(Base):
    """
    Description: table dédiée à désigner /caractériser un utilisateur /collaborateur.
    """

    __tablename__ = "collaborator"
    id = Column(Integer, primary_key=True)
    registration_number = Column(String(12), nullable=False, unique=True)
    username = Column(String(65), nullable=False)
    department_id = Column(Integer, ForeignKey("collaborator_department.id"))
    role_id = Column(Integer, ForeignKey("collaborator_role.id"), default=2)
    department = relationship("Collaborator_Department", back_populates="collaborator")
    role = relationship("Collaborator_Role", back_populates="collaborator")
    client = relationship("Client", back_populates="collaborator")
    contract = relationship("Contract", back_populates="collaborator")
    event = relationship("Event", back_populates="collaborator")
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(user_id|{self.registration_number})'
        descriptors += f',(username|{self.username})'
        descriptors += f',(department_id|{self.department.department_id})'
        descriptors += f',(role|{self.role.role_id})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        collaborator_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "registration_number": self.registration_number,
            "username": self.username,
            "department_id": self.department_id,
            "role_id": self.role.role_id,
        }
        return collaborator_dict

    @staticmethod
    def _get_keys():
        return [
            "username",
            "department_id",
            "role_id",
        ]


class Company(Base):
    """
    Description: table dédiée à désigner /caractériser l'entreprise d'un client, obtenu par un commercial.
    """

    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    company_id = Column(String(120), nullable=False, unique=True)
    company_name = Column(String(130), nullable=False)
    company_registration_number = Column(String(100), nullable=False)
    company_subregistration_number = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey("location.id"))
    client = relationship("Client", back_populates="company")
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(company_id|{self.company_id})'
        descriptors += f',(company_name|{self.company_name})'
        descriptors += f',(company_registration_number|{self.company_registration_number})'
        descriptors += f',(company_subregistration_number|{self.company_subregistration_number})'
        descriptors += f',(location_id|{self.location_id})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        company_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "company_id": self.company_id,
            "company_name": self.company_name,
            "company_registration_number": self.company_registration_number,
            "company_subregistration_number": self.company_subregistration_number,
            "location_id": self.location_id,
        }
        return company_dict

    @staticmethod
    def _get_keys():
        return [
            "company_name",
            "company_registration_number",
            "company_subregistration_number",
            "location_id",
        ]


class Client(Base):
    """
    Description: table dédiée à désigner /caractériser un client, obtenu par un commercial.
    """

    __tablename__ = "client"
    CIVILITIES = [
        ("MR", "monsieur"),
        ("MME", "madame"),
        ("MLE", "mademoiselle"),
        ("AUTRE", "autre"),
    ]
    id = Column(Integer, primary_key=True)
    client_id = Column(String(120), nullable=False, unique=True)
    civility = Column(ChoiceType(CIVILITIES), nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(75), nullable=False)
    employee_role = Column(String(100), nullable=False)
    email = Column(String(130), nullable=False)
    telephone = Column(String(60), nullable=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    creation_date = Column(Date(), nullable=False, default=get_today_date())
    last_update_date = Column(Date(), nullable=False, default=get_today_date())
    commercial_contact = Column(Integer, ForeignKey("collaborator.id"))
    collaborator = relationship("Collaborator", back_populates="client")
    company = relationship("Company", back_populates="client")
    contract = relationship("Contract", back_populates="client")
    event = relationship("Event", back_populates="client")

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(client_id|{self.client_id})'
        descriptors += f',(civility|{self.civility})'
        descriptors += f',(first_name|{self.first_name})'
        descriptors += f',(last_name|{self.last_name})'
        descriptors += f',(email|{self.email})'
        descriptors += f',(telephone|{self.telephone})'
        descriptors += f',(company_id|{self.company.company_id})'
        descriptors += f',(commercial_contact|{self.commercial_contact})'
        descriptors += f',(collaborator|{self.collaborator.registration_number})'
        descriptors += f',(contract|{self.contract})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        client_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y"),
            "client_id": self.client_id,
            "civility": f"{self.civility}",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "employee_role": self.employee_role,
            "email": self.email,
            "telephone": self.telephone,
            "company_id": self.company_id,
            "last_update_date": self.last_update_date.strftime("%d-%m-%Y"),
            "commercial_contact": self.commercial_contact,
        }
        return client_dict

    @staticmethod
    def _get_keys():
        return [
            "civility",
            "first_name",
            "last_name",
            "employee_role",
            "email",
            "telephone",
            "company_id",
            "commercial_contact",
        ]


class Contract(Base):
    """
    Description:
    Table dédiée à désigner /caractériser un contrat, négocié par un commercial, entre un client et un évènement.
    """

    __tablename__ = "contract"
    STATUS = [("signed", "signed"), ("unsigned", "unsigned"), ("canceled", "canceled")]
    id = Column(Integer, primary_key=True)
    contract_id = Column(String(120), nullable=False, unique=True)
    full_amount_to_pay = Column(Float, nullable=False)
    remain_amount_to_pay = Column(Float, nullable=False, default=full_amount_to_pay)
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )
    status = Column(ChoiceType(STATUS), default="unsigned")
    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship("Client", back_populates="contract")
    collaborator_id = Column(Integer, ForeignKey("collaborator.id"))
    collaborator = relationship("Collaborator", back_populates="contract")
    event = relationship("Event", back_populates="contract")

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(contract_id|{self.contract_id})'
        descriptors += f',(client_id|{self.client.client_id})'
        descriptors += f',(collaborator_id|{self.collaborator.registration_number})'
        descriptors += f',(status|{self.status})'
        descriptors += f',(full_amount_to_pay|{self.full_amount_to_pay}{settings.DEFAULT_CURRENCY[1]})'
        descriptors += f',(remain_amount_to_pay|{self.remain_amount_to_pay}{settings.DEFAULT_CURRENCY[1]})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        contract_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "contract_id": self.contract_id,
            "full_amount_to_pay": self.full_amount_to_pay,
            "remain_amount_to_pay": self.remain_amount_to_pay,
            "creation_date": self.creation_date.strftime("%d-%m-%Y"),
            "status": f"{self.status}",
            "client_id": self.client_id,
            "collaborator_id": self.collaborator_id,
        }
        return contract_dict

    @staticmethod
    def _get_keys():
        return [
            "full_amount_to_pay",
            "remain_amount_to_pay",
            "creation_date",
            "status",
            "client_id",
            "telephone",
            "collaborator_id",
        ]


class Location(Base, ModelMixin):
    """
    Description: table dédiée à désigner /caractériser une localisation.
    """

    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    location_id = Column(String(120), nullable=False, unique=True)
    adresse = Column(String(150), nullable=True)
    complement_adresse = Column(String(75), nullable=True)
    code_postal = Column(Integer, nullable=False)
    ville = Column(String(100), nullable=False)
    pays = Column(String(100), nullable=True, default="France")
    event = relationship("Event", back_populates="location")
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(location_id|{self.location_id})'
        descriptors += f',(adresse|{self.adresse})'
        descriptors += f',(complement_adresse|{self.complement_adresse})'
        descriptors += f',(code_postal|{self.code_postal})'
        descriptors += f',(ville|{self.ville})'
        descriptors += f',(pays|{self.pays})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        location_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "location_id": self.location_id,
            "adresse": self.adresse,
            "complement_adresse": self.complement_adresse,
            "code_postal": self.code_postal,
            "ville": self.ville,
            "pays": self.pays,
        }
        return location_dict

    @staticmethod
    def _get_keys():
        return [
            "adresse",
            "complement_adresse",
            "code_postal",
            "ville",
            "pays",
        ]


class Event(Base):
    """
    Description: table dédiée à désigner /caractériser un évènement.
    """

    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    event_id = Column(String(120), nullable=False, unique=True)
    title = Column(String(125), nullable=False)
    contract_id = Column(Integer, ForeignKey("contract.id"))
    contract = relationship("Contract", back_populates="event")
    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship("Client", back_populates="event")
    collaborator_id = Column(Integer, ForeignKey("collaborator.id"))
    collaborator = relationship("Collaborator", back_populates="event")
    creation_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )
    event_start_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )
    event_end_date = Column(
        DateTime(timezone=False), default=datetime.now()
    )
    location_id = Column(Integer, ForeignKey("location.id"))
    location = relationship("Location", back_populates="event")
    attendees = Column(Integer, nullable=False)
    notes = Column(String(2500), nullable=True)

    def __str__(self):
        descriptors = "["
        descriptors += f'(creation_date|{self.creation_date.strftime("%d-%m-%Y")})'
        descriptors += f',(event_id|{self.event_id})'
        descriptors += f',(title|{self.title})'
        descriptors += f',(contract_id|{self.contract.contract_id})'
        descriptors += f',(client_id|{self.client.client_id})'
        descriptors += f',(collaborator_id|{self.collaborator.registration_number})'
        descriptors += f',(event_start_date|{self.event_start_date.strftime("%d-%m-%Y")})'
        descriptors += f',(event_end_date|{self.event_end_date.strftime("%d-%m-%Y")})'
        descriptors += f',(location_id|{self.location.location_id})'
        descriptors += f',(attendees|{self.attendees})'
        descriptors += f',(notes|{self.notes})'
        descriptors += "]"
        return descriptors

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        event_dict = {
            "id": self.id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y %H:%M"),
            "event_id": self.event_id,
            "title": self.title,
            "contract_id": self.contract_id,
            "client_id": self.client_id,
            "collaborator_id": self.collaborator_id,
            "event_start_date": self.event_start_date.strftime("%d-%m-%Y %H:%M"),
            "event_end_date": self.event_end_date.strftime("%d-%m-%Y %H:%M"),
            "location_id": self.location_id,
            "attendees": self.attendees,
            "notes": self.notes,
        }
        return event_dict

    @staticmethod
    def _get_keys():
        return [
            "title",
            "contract_id",
            "client_id",
            "collaborator_id",
            "event_start_date",
            "event_end_date",
            "location_id",
            "attendees",
            "notes",
        ]

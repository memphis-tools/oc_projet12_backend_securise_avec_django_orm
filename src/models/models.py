"""
Les modèles métier
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    String,
    Integer,
    Date,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy_utils import ChoiceType
from datetime import date, datetime


Base = declarative_base()
MONTHS = [
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
    returned_date = f"{today.day}-{MONTHS[today.month-1][1]}-{today.year}"
    return returned_date


class ModelMixin:
    def get_id(self):
        return self.id


class UserDepartment(Base):
    """
    Description: table dédiée à référencer les départements des utilisateurs de l'application.
    """

    __tablename__ = "collaborator_department"
    DEPARTEMENTS = [
        ("OC12_COMMERCIAL", "oc12_commercial"),
        ("OC12_GESTION", "oc12_gestion"),
        ("OC12_SUPPORT", "oc12_support"),
    ]
    id = Column(Integer, primary_key=True)
    department_id = Column(String(120), nullable=False, unique=True)
    name = Column(ChoiceType(DEPARTEMENTS), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        department_dict = {
            "id": self.id,
            "department_id": self.department_id,
            "name": self.name,
        }
        return department_dict


class UserRole(Base):
    """
    Description: table dédiée à référencer les rôles des utilisateurs /collaborateurs de l'application.
    """

    __tablename__ = "collaborator_role"
    ROLES = [
        ("MANAGER", "manager"),
        ("EMPLOYEE", "employee"),
    ]
    id = Column(Integer, primary_key=True)
    role_id = Column(String(120), nullable=False, unique=True)
    name = Column(ChoiceType(ROLES), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        role_dict = {
            "id": self.id,
            "role_id": self.role_id,
            "name": self.name,
        }
        return role_dict


class User(Base):
    """
    Description: table dédiée à désigner /caractériser un utilisateur /collaborateur.
    """

    __tablename__ = "collaborator"
    id = Column(Integer, primary_key=True)
    registration_number = Column(String(12), nullable=False)
    username = Column(String(65), nullable=False)
    department = Column(Integer, ForeignKey("collaborator_department.id"))
    role = Column(Integer, ForeignKey("collaborator_role.id"), default=2)
    client = relationship("Client", back_populates="collaborator")
    contract = relationship("Contract", back_populates="collaborator")

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        collaborator_dict = {
            "id": self.id,
            "registration_number": self.registration_number,
            "username": self.username,
            "department": self.department,
            "role": self.role,
        }
        return collaborator_dict


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

    def __str__(self):
        return f"{self.company_id}: {self.company_name}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        company_dict = {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company_name,
            "company_registration_number": self.company_registration_number,
            "company_subregistration_number": self.company_subregistration_number,
            "location_id": self.location_id,
        }
        return company_dict


class Client(Base):
    """
    Description: table dédiée à désigner /caractériser un client, obtenu par un commercial.
    """

    __tablename__ = "client"
    CIVILITIES = [
        ("MR", "monsieur"),
        ("MRS", "madame"),
        ("MISS", "madamoiselle"),
        ("OTHER", "autre"),
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
    collaborator = relationship("User", back_populates="client")
    company = relationship("Company", back_populates="client")
    contract = relationship("Contract", back_populates="client")
    event = relationship("Event", back_populates="client")

    def __str__(self):
        return f"{self.company_id} {self.civility} {self.first_name} {self.last_name}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        client_dict = {
            "id": self.id,
            "client_id": self.client_id,
            "civility": f"{self.civility}",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "employee_role": self.employee_role,
            "email": self.email,
            "telephone": self.telephone,
            "company_id": self.company_id,
            "creation_date": self.creation_date.strftime("%d-%m-%Y"),
            "last_update_date": self.last_update_date.strftime("%d-%m-%Y"),
            "commercial_contact": self.commercial_contact,
        }
        return client_dict


class Contract(Base):
    """
    Description:
    Table dédiée à désigner /caractériser un contrat, négocié par un commercial, entre un client et un évènement.
    """

    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    contract_id = Column(String(120), nullable=False, unique=True)
    full_amount_to_pay = Column(Float, nullable=False)
    remain_amount_to_pay = Column(Float, nullable=False, default=full_amount_to_pay)
    creation_date = Column(
        DateTime(timezone=False), nullable=False, default=datetime.now()
    )
    # statut pour signifier si contrat signé ou non
    status = Column(Boolean, default=False)
    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship("Client", back_populates="contract")
    collaborator_id = Column(Integer, ForeignKey("collaborator.id"))
    collaborator = relationship("User", back_populates="contract")
    event = relationship("Event", back_populates="contract")

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        contract_dict = {
            "id": self.id,
            "contract_id": self.contract_id,
            "full_amount_to_pay": self.full_amount_to_pay,
            "remain_amount_to_pay": self.remain_amount_to_pay,
            "creation_date": self.creation_date.strftime("%d-%m-%Y"),
            "status": self.status,
            "client_id": self.client_id,
            "collaborator_id": self.collaborator_id,
        }
        return contract_dict


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

    def __str__(self):
        return f"{self.id}-{self.location_id}: {self.ville} {self.pays}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        location_dict = {
            "id": self.id,
            "location_id": self.location_id,
            "adresse": self.adresse,
            "complement_adresse": self.complement_adresse,
            "code_postal": self.code_postal,
            "ville": self.ville,
            "pays": self.pays,
        }
        return location_dict


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
    event_start_date = Column(
        DateTime(timezone=False), nullable=False, default=datetime.now()
    )
    event_end_date = Column(
        DateTime(timezone=False), nullable=False, default=datetime.now()
    )
    location_id = Column(Integer, ForeignKey("location.id"))
    attendees = Column(Integer, nullable=False)
    notes = Column(String(2500), nullable=True)

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return self.__str__()

    def get_dict(self):
        event_dict = {
            "id": self.id,
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

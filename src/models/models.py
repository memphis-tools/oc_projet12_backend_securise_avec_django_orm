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


class UserDepartment(Base):
    """
    Description: table dédiée à référencer les départements des utilisateurs de l'application.
    """

    __tablename__ = "collaborator_department"
    DEPARTEMENTS = [
        ("COMMERCIAL", "commercial"),
        ("GESTION", "gestion"),
        ("SUPPORT", "support"),
    ]
    id = Column(Integer, primary_key=True)
    name = Column(ChoiceType(DEPARTEMENTS), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()


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
    name = Column(ChoiceType(ROLES), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()


class User(Base):
    """
    Description: table dédiée à désigner /caractériser un utilisateur /collaborateur.
    """

    __tablename__ = "collaborator"
    id = Column(Integer, primary_key=True)
    registration_number = Column(String(12), nullable=False)
    password = Column(String(200), nullable=False)
    username = Column(String(65), nullable=False)
    departement = Column(Integer, ForeignKey("collaborator_department.id"))
    role = Column(Integer, ForeignKey("collaborator_role.id"), default=2)
    client = relationship("Client", back_populates="collaborator")
    contract = relationship("Contract", back_populates="collaborator")

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return self.__str__()


class Client(Base):
    """
    Description: table dédiée à désigner /caractériser un client, obtenu par un commercial.
    """

    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    information = Column(String(2500), nullable=True)
    fullname = Column(String(130), nullable=False)
    email = Column(String(130), nullable=False)
    telephone = Column(String(60), nullable=True)
    company_name = Column(String(130), nullable=False)
    creation_date = Column(Date(), nullable=False, default=get_today_date())
    last_update_date = Column(Date(), nullable=False, default=get_today_date())
    commercial_contact = Column(Integer, ForeignKey("collaborator.id"))
    collaborator = relationship("User", back_populates="client")
    contract = relationship("Contract", back_populates="client")
    event = relationship("Event", back_populates="client")

    def __str__(self):
        return f"{self.fullname}"

    def __repr__(self):
        return self.__str__()


class Contract(Base):
    """
    Description:
    Table dédiée à désigner /caractériser un contrat, négocié par un commercial, entre un client et un évènement.
    """

    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    information = Column(String(2500), nullable=True)
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


class Location(Base):
    """
    Description: table dédiée à désigner /caractériser une localisation.
    """

    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    adresse = Column(String(150), nullable=True)
    complement_adresse = Column(String(75), nullable=True)
    code_postal = Column(Integer, nullable=False)
    ville = Column(String(100), nullable=False)
    pays = Column(String(100), nullable=True, default="France")

    def __str__(self):
        return f"{self.adresse}-{self.complement_adresse}-{self.code_postal}-{self.ville} {self.pays}"

    def __repr__(self):
        return self.__str__()


class Event(Base):
    """
    Description: table dédiée à désigner /caractériser un évènement.
    """

    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
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

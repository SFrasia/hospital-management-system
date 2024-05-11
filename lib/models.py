from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, MetaData, Table, Date
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

custom_metadata = MetaData()

Base = declarative_base(metadata=custom_metadata)

if __name__ == '__main__':
    engine = create_engine('sqlite:///hospital.db', echo=True)
    Session = sessionmaker(bind = engine)
    session = Session()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)

    def __repr__ (self):
        return f"<Patient {self.id}: {self.name}, {self.age}, {self.gender}, {self.mobile_number}"
    
    def __init__(self, name, age, gender, mobile_number):
        self.name = name
        self.age = age
        self.gender = gender
        self.mobile_number = mobile_number
        self.appointments = []

class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    def __repr__(self):
        return f"Name: {self.name}, Specialization: {self.specialization}"
    
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.appointments = []
        
class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(Date, nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)

    def __repr__(self):
        return f"Appointment ID: {self.id}\n\tDate of Appointment: {self.appointment_date}"
    
    def __init__(self, doctor, patient, appointment_date):
        self.doctor = doctor  
        self.patient = patient  
        self.appointment_date = appointment_date 

    def __repr__(self):
        return f"Appointment ID: {self.id}\n\tDate of Appointment: {self.appointment_date}"
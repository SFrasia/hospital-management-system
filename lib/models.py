from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

if __name__ == '__main__':
    engine = create_engine('sqlite:///hospital.db')
    Session = sessionmaker(bind = engine)
    session = Session()

#Patient table
# class Patient(Base):
#     __tablename__ = 'patients'

    
# #     id = Column(Integer, primary_key=True, autoincrement=True)
# #     name = Column(String, nullable=False)
# #     age = Column(Date, nullable=False)
# #     gender = Column(String, nullable=False)
# #     mobile_number = Column(String, nullable=False)

# #     def __repr__ (self):
# #         return f"<Patient {self.id}: {self.name}, {self.age}, {self.gender}, {self.mobile_number}"
    
# class Patient:
#     def __init__(self, name, age, gender, mobile_number):
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.mobile_number = mobile_number
#         self.appointments = [] 

# # Appointment table
# class Appointment(Base):
#     __tablename__ = 'appointments'



# # Doctor table

# class Doctors(Base):
#     __tablename__ = 'doctor'



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
        self.doctor = doctor  # Doctor object
        self.patient = patient  # Patient object
        self.appointment_date = appointment_date 

    def __repr__(self):
        return f"Appointment ID: {self.id}\n\tDate of Appointment: {self.appointment_date}"
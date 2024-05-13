from models.doctor import Doctor
from models.patient import Patient

def exit_program():
    print("Goodbye!")
    exit()

#Doctor
def list_doctor():
    doctors = Doctor.get_all()
    for doctor in doctors:
        print(doctor)

def find_doctor_by_name():
    name = input("Enter the doctor's name: ")
    doctor = Doctor.find_by_name(name)
    print(doctor) if doctor else print(
        f'Doctor {name} not found')
    
def find_department_by_id():
    id_ = input("Enter the doctor's id: ")
    doctor = Doctor.find_by_id(id_)
    print(doctor) if doctor else print(f'Doctor {id_} not found')

def create_doctor():
    name = input("Enter the doctor's name: ")
    specialization = input("Enter the doctor's specialization: ")
    try:
        doctor = Doctor.create(name, specialization)
        print(f'Success: {doctor}')
    except Exception as exc:
        print("Error creating doctor: ", exc)

def update_doctor():
    id_ = input("Enter the doctor's id: ")
    if doctor := Doctor.find_by_id(id_):
        try:
            name = input("Enter the doctor's new name: ")
            doctor.name = name
            specialization = input("Enter the doctor's new specialization: ")
            doctor.specialization = specialization

            doctor.update()
            print(f'Success: {doctor}')
        except Exception as exc:
            print("Error updating doctor: ", exc)
    else:
        print(f'Doctor {id_} not found')

def delete_doctor():
    id_ = input("Enter the doctor's id: ")
    if doctor := Doctor.find_by_id(id_):
        doctor.delete()
        print(f'Doctor {id_} deleted')
    else:
        print(f'Doctor {id_} not found')

#Patient
def list_patient():
    patients = Patient.get_all()
    for patient in patients:
        print(patient)

def find_patient_by_name():
    name = input("Enter the patient's name: ")
    patient = Patient.find_by_name(name)
    print(patient) if patient else print(
        f'Patient {name} not found')
    
def find_patient_by_id():
    id_ = input("Enter the patient's id: ")
    patient = Patient.find_by_id(id_)
    print(patient) if patient else print(f'Patient {id_} not found')

def create_patient(self):
        name = input("Enter patient name: ")
        age = int(input("Enter patient age: "))
        gender = input("Enter patient gender: ")
        try:
            patient = Patient.create(name=name, age=age, gender=gender)
            print(f'Success: {patient}')
        except Exception as exc:
         print("Error creating patient: ", exc)


def update_patient():
    id_ = input("Enter the patient's id: ")
    if patient := Patient.find_by_id(id_):
        try:
            name = input("Enter the patient's new name: ")
            patient.name = name
            age = int(input("Enter the patient's new age: "))
            patient.age = age
            gender = input("Enter the patient's gender: ")
            patient.gender = gender

            patient.update()
            print(f'Success: {patient}')
        except Exception as exc:
            print("Error updating patient: ", exc)
    else:
        print(f'Patient {id_} not found')

def delete_patient():
    id_ = input("Enter the patient's id: ")
    if patient:= Patient.find_by_id(id_):
        patient.delete()
        print(f'Patient {id_} deleted')
    else:
        print(f'Patient {id_} not found')
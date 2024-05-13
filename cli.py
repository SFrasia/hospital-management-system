from lib.patient import *  # Import SQLAlchemy models
from datetime import datetime
from seed import session

class HospitalCLI:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []

        # Populate lists from the database
        self.populate_lists()

    def populate_lists(self):
        # Fetch patients from the database and add them to the patients list
        self.patients = session.query(Patient).all()

        # Fetch doctors from the database and add them to the doctors list
        self.doctors = session.query(Doctor).all()

        # Fetch appointments from the database and add them to the appointments list
        self.appointments = session.query(Appointment).all()

    def display_menu(self):
        print("\nHospital Management System")
        print("1. Patients")
        print("2. Doctors")
        print("3. Appointments")
        print("4. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                self.manage_patients()
            elif choice == "2":
                self.manage_doctors()
            elif choice == "3":
                self.manage_appointments()
            elif choice == "4":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    # Patients
    def manage_patients(self):
        while True:
            print("\nPatients Management")
            print("1. Create a patient")
            print("2. Delete a patient")
            print("3. Display all patients")
            print("4. View patient appointments")
            print("5. Find a patient by id")
            print("6. Back to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_patient()
            elif choice == "2":
                self.delete_patient()
            elif choice == "3":
                self.display_all_patients()
            elif choice == "4":
                self.view_patient_appointments()
            elif choice == "5":
                self.find_patient_by_id()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_patient(self):
        name = input("Enter patient name: ")
        age = input("Enter patient age: ")
        gender = input("Enter patient gender: ")
        mobile_number = input("Enter patient mobile number: ")
        patient = Patient(name=name, age=age, gender=gender, mobile_number=mobile_number)
#       self.patients.append(patient)  
        session.add(patient)
        session.commit()
        print("Patient created successfully.")

    def delete_patient(self):
        patient_name = input("Enter the name of the patient to delete: ")
        for patient in self.patients:
            if patient.name == patient_name:
                self.patients.remove(patient)
                session.delete(patient)
                session.commit()
                print("Patient deleted successfully.")
                return
        print("Patient not found.")

    def display_all_patients(self):
        print("\nAll Patients:")
        for patient in self.patients:
            print(patient.name)

    def view_patient_appointments(self):
        patient_name = input("Enter the name of the patient: ")
        for patient in self.patients:
            if patient.name == patient_name:
                appointments = patient.get_all_appointments()
                print(f"\nAppointments for {patient_name}:")
                for appointment in appointments:
                    print(f"- Doctor: {appointment.doctor.name}, Date: {appointment.date_time}")
                return
        print("Patient not found.")

    def find_patient_by_id(self):
        patient_id = input("Enter the patient's id: ")
        for patient in self.patients:
            if patient.id == patient_id:
                print(f"Patient found: {patient.name}, Age: {patient.age}, Gender: {patient.gender}")
                return
        print("Patient not found.")

    # Doctors
    def manage_doctors(self):
        while True:
            print("\nDoctors Management")
            print("1. Create a doctor")
            print("2. Delete a doctor")
            print("3. Display all doctors")
            print("4. Find a doctor by id")
            print("5. Back to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_doctor()
            elif choice == "2":
                self.delete_doctor()
            elif choice == "3":
                self.display_all_doctors()
            elif choice == "4":
                self.find_doctor_by_id()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_doctor(self):
        name = input("Enter doctor name: ")
        specialization = input("Enter doctor specialization: ")
        # Create and add the doctor to the session
        doctor = Doctor(name=name, specialization=specialization)
#       self.doctors.append(doctor)
        session.add(doctor)
        session.commit()
        print("Doctor created successfully.")

    def delete_doctor(self):
        doctor_name = input("Enter the name of the doctor to delete: ")
        for doctor in self.doctors:
            if doctor.name == doctor_name:
                self.doctors.remove(doctor)
                session.delete(doctor)
                session.commit()
                print("Doctor deleted successfully.")
                return
        print("Doctor not found.")

    def display_all_doctors(self):
        print("\nAll Doctors:")
        for doctor in self.doctors:
            print(doctor.name)

    def find_doctor_by_id(self):
        doctor_id = input("Enter the doctor's id: ")
        for doctor in self.doctors:
            if doctor.id == doctor_id:
                print(f"Doctor found: {doctor.name}, Specialization: {doctor.specialization}")
                return
        print("Doctor not found.")

    # Appointments
    def manage_appointments(self):
        while True:
            print("\nAppointment Management")
            print("1. Schedule appointment")
            print("2. Delete an appointment")
            print("3. Display all appointments")
            print("4. Find an appointment by id")
            print("5. Back to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.schedule_appointment()
            elif choice == "2":
                self.delete_appointment()
            elif choice == "3":
                self.display_all_appointments()
            elif choice == "4":
                self.find_appointment_by_id()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def schedule_appointment(self):
        appointment_date = input("Enter the appointment date (YYYY-MM-DD): ")
        try:
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Get patient and doctor IDs from the user
        patient_id = int(input("Enter the patient ID: "))
        doctor_id = int(input("Enter the doctor ID: "))

        # Fetch patient and doctor objects from the database
        patient = session.query(Patient).get(patient_id)
        doctor = session.query(Doctor).get(doctor_id)

        if not patient:
            print("Patient not found.")
            return
        if not doctor:
            print("Doctor not found.")
            return

        # Create the appointment and assign patient and doctor using relationships
        appointment = Appointment(appointment_date=appointment_date)
        appointment.patient = patient
        appointment.doctor = doctor

        session.add(appointment)
        session.commit()
        print("Appointment scheduled successfully.")

    def delete_appointment(self):
        appointment_id = int(input("Enter the appointment ID to delete: "))
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                self.appointments.remove(appointment)
                # Delete the appointment from the database
                session.delete(appointment)
                session.commit()
                print("Appointment deleted successfully.")
                return
        print("Appointment not found.")

    def display_all_appointments(self):
        print("\nAll Appointments:")
        for appointment in self.appointments:
            print(f"Date: {appointment.appointment_date}, Patient ID: {appointment.patient_id}, Doctor ID: {appointment.doctor_id}")

    def find_appointment_by_id(self):
        appointment_id = int(input("Enter the appointment ID: "))
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                print(f"Appointment found: Date: {appointment.appointment_date}, Patient ID: {appointment.patient_id}, Doctor ID: {appointment.doctor_id}")
                return
        print("Appointment not found.")

# Example:
if __name__ == "__main__":
    cli = HospitalCLI()
    cli.run()
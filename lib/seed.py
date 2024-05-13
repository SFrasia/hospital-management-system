from lib.models.__init__ import CONN, CURSOR
from lib.models.doctor import Doctor
from lib.models.patient import Patient

def seed_database():
    try:
        # Drop existing tables
        Patient.drop_table()
        Doctor.drop_table()
        
        # Create new tables
        Doctor.create_table()
        Patient.create_table()

        # Create seed data
        doctor1 = Doctor.create("Dr. Linda", "Gynaecologist")
        doctor2 = Doctor.create("Dr. Mark", "Physician")

        Patient.create("Jane Doe", 53, "Female", doctor1.id)
        Patient.create("John Doe", 35, "Male", doctor1.id)
        Patient.create("Mark", 12, "Male", doctor2.id)
        Patient.create("Hannah", 34, "Female", doctor2.id)

        print("Database seeded successfully.")

    except Exception as e:
        print("Error seeding database:", e)

seed_database()

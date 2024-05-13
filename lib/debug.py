#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.doctor import Doctor
from models.patient import Patient
import ipdb


def reset_database():
    # Drop existing tables and recreate them
    Patient.drop_table()
    Doctor.drop_table()
    Doctor.create_table()
    Patient.create_table()

    # Create seed data
    doctor1 = Doctor.create("Dr. Linda", "Gynaecologist")
    doctor2 = Doctor.create("Dr. Mark", "Physician")

    # Create patients with associated doctors
    Patient.create("Jane Doe", 53, "Female", doctor1.id)
    Patient.create("John Doe", 35, "Male", doctor1.id)
    Patient.create("Mark", 12, "Male", doctor1.id)
    Patient.create("Hannah", 34, "Female", doctor2.id)


reset_database()
ipdb.set_trace()

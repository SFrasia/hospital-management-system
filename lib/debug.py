#!/usr/bin/env python3
#lib/testing/debug.py

from __init__ import CONN, CURSOR
from lib.models.patient import Patient

import ipdb

Patient.drop_table()
Patient.create_table()

patient1 = Patient.create("Mary", 23, "Female")
print(patient1) 

patient1.save() 
print(patient1)

patient1.name = "Mary"
patient1.age = 23
patient1.gender = "Female"

print("Delete patient1")
patient1.delete()
print(patient1)


reset_database()
ipdb.set_trace()
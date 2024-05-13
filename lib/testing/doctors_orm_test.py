from models.__init__ import CONN, CURSOR
from models.doctor import Doctor
import pytest


class TestDoctor:
    '''Class Doctor in doctor.py'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''drop tables prior to each test.'''

        CURSOR.execute("DROP TABLE IF EXISTS patients")
        CURSOR.execute("DROP TABLE IF EXISTS doctors")
        Doctor.all = {}

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "departments" if it does not exist.'''

        Doctor.create_table()
        assert (CURSOR.execute("SELECT * FROM departments"))

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "departments" if it exists.'''

        sql = """
            CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT,
            specialization TEXT,
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

        Doctor.drop_table()

        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='doctor'
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result is None)

    def test_saves_department(self):
        '''contains method "save()" that saves a Department instance to the db and assigns the instance an id.'''

        Doctor.create_table()
        doctor = Doctor("Dr. Mark", "Physician")
        doctor.save()

        sql = """
            SELECT * FROM doctors
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (doctor.id, doctor.name, doctor.specialization) ==
                (row[0], "Dr. Mark", "Physician"))

    def test_creates_department(self):
        '''contains method "create()" that creates a new row in the db using parameter data and returns a Doctor instance.'''

        Doctor.create_table()
        doctor = Doctor.create("Dr. Mark", "Physician")

        sql = """
            SELECT * FROM doctors
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (doctor.id, doctor.name, doctor.location) ==
                (row[0], "Dr. Mark", "Physician"))

    def test_updates_row(self):
        '''contains a method "update()" that updates an instance's corresponding db row to match its new attribute values.'''
        Doctor.create_table()

        doctor1 = Doctor.create(
            "Dr. Linda", "Gynaecologist")
        id1 = doctor1.id
        doctor2 = Doctor.create("Dr. Linda", "Gynaecologist")
        id2 = doctor2.id

        # Assign new values for name and specialization
        doctor2.name = "Dr. Humphrey"
        doctor2.specialization = "General"

        # Persist the updated name and specialization values
        doctor2.update()

        # assert doctor1 row was not updated, doctor1 object state not updated
        # assert row not updated
        doctor = Doctor.find_by_id(id1)
        assert ((doctor.id, doctor.name, doctor.specialization)
                == (id1, "Dr. Mark", "Physician")
                == (doctor1.id, doctor1.name, doctor1.specialization))

        # assert doctor2 row was updated, doctor2 object state is correct
        doctor = Doctor.find_by_id(id2)
        assert ((doctor.id, doctor.name, doctor.specialization)
                == (id2, "Dr. Linda", "Gynaecologist")
                == (doctor2.id, doctor2.name, doctor2.specialization))

    def test_deletes_row(self):
        '''contains a method "delete()" that deletes the instance's corresponding db row'''
        Doctor.create_table()

        doctor1 = Doctor.create(
            "Dr. Mark", "Physician")
        id1 = doctor1.id
        doctor2 = Doctor.create(
            "Dr. Linda", "Gynaecologist")
        id2 = doctor2.id

        doctor2.delete()

        # assert doctor1 row was not deleted, doctor1 object state is correct
        doctor = Doctor.find_by_id(id1)
        assert ((doctor.id, doctor.name, doctor.location)
                == (id1, "Dr. Mark", "Physician")
                == (doctor1.id, doctor1.name, doctor1.location))

        # assert doctor2 row is deleted
        assert (Doctor.find_by_id(id2) is None)
        # assert doctor2 object state is correct, id should be None
        assert ((None, "Dr. Linda", "Gynaecologist")
                == (doctor2.id, doctor2.name, doctor2.location))
        # assert dictionary entry was deleted
        assert(Doctor.all.get(id2) is None)

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Doctor instances for every row in the db.'''

        Doctor.create_table()

        doctor1 = Doctor.create(
            "Dr. Mark", "Physician")
        doctor2 = Doctor.create("Dr. Linda", "Gynaecologist")

        doctor = Doctor.get_all()

        assert (len(doctor) == 2)
        assert (
            (doctor[0].id, doctor[0].name, doctor[0].specialization) ==
            (doctor1.id, "Dr. Mark", "Physician"))
        assert ((doctor[1].id, doctor[1].name, doctor[1].specialization) ==
                (doctor2.id, "Dr. Linda", "Gynaecologist")
                )

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Department instance corresponding to the db row retrieved by id.'''

        Doctor.create_table()
        doctor1 = Doctor.create(
            "Dr. Mark", "Physician")
        doctor2 = Doctor.create("Dr. Linda", "Gynaecologist")

        doctor = Doctor.find_by_id(doctor1.id)
        assert (
            (doctor.id, doctor.name, doctor.specialization) ==
            (doctor1.id, "Dr. Mark", "Physician")
        )
        doctor = Doctor.find_by_id(doctor2.id)
        assert (
            (doctor.id, doctor.name, doctor.specialization) ==
            (doctor2.id, "Dr. Linda", "Gynaecologist")
        )
        doctor = Doctor.find_by_id(0)
        assert (doctor is None)

    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns a Doctor instance corresponding to the db row retrieved by name.'''

        Doctor.create_table()
        doctor1 = Doctor.create(
            "Dr. Mark", "Physician")
        doctor2 = Doctor.create("Dr. Linda", "Gynaecologist")

        doctor = Doctor.find_by_name("Dr. Mark")
        assert (
            (doctor.id, doctor.name, doctor.specialization) ==
            (doctor1.id, "Dr. Mark", "Physician")
        )

        doctor = Doctor.find_by_name("Dr. Linda")
        assert (
            (doctor.id, doctor.name, doctor.specialization) ==
            (doctor2.id, "Dr. Linda", "Gynaecologist")
        )
        doctor = Doctor.find_by_name("Unknown")
        assert (doctor is None)

    def test_get_patients(self):
        '''contain a method "patients" that gets the patients for the current Doctor instance '''

        from models.patient import Patient
        Patient.all = {}

        Doctor.create_table()
        doctor1 = Doctor.create("Dr. Linda", "Gynaecologist")
        doctor2 = Doctor.create(
            "Dr. Mark", "Physician")

        Patient.create_table()
        patient1 = Patient.create("Jane Doe", 53, "Female", doctor1.id)
        patient2 = Patient.create(
            "John Doe", 35, "Male", doctor1.id)
        patient3 = Patient.create("Mark", 12, "Male", doctor2.id)
        patient4 = Patient.create("Hannah", 34, "Female", doctor2.id)

        patients = doctor1.patients()
        assert (len(patients) == 2)
        assert ((patients[0].id, patients[0].name, patients[0].age, patients[0].gender, patients[0].doctor_id) ==
                (patient1.id, patient1.name, patient1.age, patient1.gender, patient1.doctor_id))
        assert ((patients[1].id, patients[1].name, patients[1].age, patients[1].gender, patients[1].doctor_id) ==
                (patient2.id, patient2.name, patient2.age, patient1.gender, patient2.doctor_id))

# lib/patient.py
from __init__ import CONN, CURSOR
from doctor import Doctor

class Patient:

    all = {}

    def __init__(self, name, age, gender, doctor_id, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.doctor_id = doctor_id
        self.appointments = []

    def __repr__(self):
        return (
            f"<Patient {self.id}: {self.name}, {self.age}, {self.gender}" +
            f"Doctor's ID: {self.doctor_id}>"
        )
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )
        
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if isinstance(age, int):
            self._age = age
        else:
            raise ValueError(
                "age must be an integer"
            )
        
    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if isinstance(gender, str) and len(gender):
            self._gender = gender
        else:
            raise ValueError(
                "gender must be a non-empty string"
            )

    @property
    def doctor_id(self):
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, doctor_id):
        if type(doctor_id) is int and Doctor.find_by_id(doctor_id):
            self._doctor_id = doctor_id
        else:
            raise ValueError(
                "doctor_id must reference a doctor in the database")
        
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Patients instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            appointments TEXT,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Patients instances """
        sql = """
            DROP TABLE IF EXISTS patients;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, age, gender, appointment values of the current Patient instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO patients (name, age, gender, appointments, doctor_id)
            VALUES (?, ?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.age, self.gender, str(self.appointments), self.doctor_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, age, gender, appointments, doctor_id):
        """ Initialize a new Patient instance and save the object to the database """
        patient = cls(name, age, gender, doctor_id)
        patient.appointments = appointments
        patient.save()
        return patient

    def update(self):
        """Update the table row corresponding to the current Patient instance."""
        sql = """
            UPDATE patients
            SET name = ?, age = ?, gender = ?, appointments = ? doctor_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.age, self.gender, str(self.appointments), self.doctor_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Patient instance"""
        sql = """
            DELETE FROM patients
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing a Patients object per row in the table"""
        sql = """
            SELECT *
            FROM patients
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls(*row) for row in rows]

    @classmethod
    def find_by_id_min(cls, id):
        """Return a Patient object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM patients
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(*row) if row else None

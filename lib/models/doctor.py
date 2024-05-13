# lib/doctor.py
from models.__init__ import CURSOR, CONN

class Doctor:

    all = {}

    def __init__ (self, name, specialization, id=None):
        self.id = id
        self.name = name
        self.specialization = specialization

    def __repr__(self):
        return "<Doctor {}: {}, {}>".format(self.id, self.name, self.specialization)
    
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
    def specialization(self):
        return self._specialization

    @specialization.setter
    def specialization(self, specialization):
        if isinstance(specialization, str) and len(specialization):
            self._specialization = specialization
        else:
            raise ValueError(
                "specialization must be a non-empty string"
            )
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Doctor instances """
        sql = """
            CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT,
            specialization TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Doctor instances """
        sql = """
            DROP TABLE IF EXISTS doctors;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, specialization values of the current Doctor instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO doctors (name, specialization)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.specialization))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, specialization):
        """ Initialize a new Doctor instance and save the object to the database """
        doctor = cls(name, specialization)
        doctor.save()
        return doctor

    def update(self):
        """Update the table row corresponding to the current Doctor instance."""
        sql = """
            UPDATE doctors
            SET name = ?, specialization = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.specialization, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Doctor instance"""
        sql = """
            DELETE FROM doctors
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing a Doctor object per row in the table"""
        sql = """
            SELECT *
            FROM doctors
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls(*row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a Doctor object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM doctors
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(*row) if row else None
    
    def patients(self):
        """Return list of patients associated with current doctor"""
        from lib.models.patient import Patient
        sql = """
            SELECT * FROM patients
            WHERE doctor_id = ?
        """
        CURSOR.execute(sql, (self.id,))

        rows = CURSOR.fetchall()
        return [
        Patient(*row) for row in rows
        ]
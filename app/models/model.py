from app.models.database import Database

class Model:
    table = ""
    fields = []
    pk = "id"
    db = Database()

    def __init__(self, **kwargs):
        for field in self.fields:
            setattr(self, field, kwargs.get(field))

    # ----------------- metodos instanciados -----------------
    def save(self):
        values = [getattr(self, f) for f in self.fields if f != self.pk]

        if getattr(self, self.pk, None):
            sets = ",".join(f"{f}=?" for f in self.fields if f != self.pk)
            params = values + [getattr(self, self.pk)]
            query = f"UPDATE {self.table} SET {sets} WHERE {self.pk}=?"
            self.db.execute(query, params)
        else:
            cols = ",".join(f for f in self.fields if f != self.pk)
            placeholders = ",".join("?" for _ in values)
            query = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
            con = self.db.connect()
            cur = con.cursor()
            cur.execute(query, values)
            con.commit()
            self.id = cur.lastrowid
            con.close()


    def delete(self):
        pk_value = getattr(self, self.pk, None)
        if pk_value:
            query = f"DELETE FROM {self.table} WHERE {self.pk}=?"
            self.db.execute(query, (pk_value,))
            setattr(self, self.pk, None)

    def to_dict(self):
        return {f: getattr(self, f) for f in self.fields}

    # ----------------- metodos de classe -----------------
    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        obj = cls()
        if isinstance(row, tuple):
            for i, value in enumerate(row):
                if i < len(cls.fields):
                    setattr(obj, cls.fields[i], value)
            return obj
        elif isinstance(row, dict):
            for key, value in row.items():
                if key in cls.fields:
                    setattr(obj, key, value)
            return obj
        return None


    @classmethod
    def get(cls, pk_value):
        query = f"SELECT * FROM {cls.table} WHERE {cls.pk} = ?"
        row = cls.db.fetch_one(query, (pk_value,))
        return cls.from_row(row)

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.table}"
        rows = cls.db.fetch_all(query)
        return [cls.from_row(r) for r in rows]

    @classmethod
    def update(cls, pk_value, **kwargs):
        sets = ",".join(f"{k}=?" for k in kwargs.keys())
        params = list(kwargs.values()) + [pk_value]
        query = f"UPDATE {cls.table} SET {sets} WHERE {cls.pk}=?"
        cls.db.execute(query, params)

    @classmethod
    def delete_by_pk(cls, pk_value):
        query = f"DELETE FROM {cls.table} WHERE {cls.pk}=?"
        cls.db.execute(query, (pk_value,))

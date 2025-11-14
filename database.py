import sqlite3
from pathlib import Path
from klasseopgave import dnd_class

BASE_DIR = Path(__file__).resolve().parent
DB_DND = str((BASE_DIR / "dndclass.db").resolve())


class Database:
    def __init__(self, DB_DND: str = DB_DND):
        self.DB_DND = DB_DND

    def _connect(self):
        conn = sqlite3.connect(self.DB_DND)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute(self, query, params=()):
        conn = self._connect()
        try:
            conn.execute(query, params)
            conn.commit()
        finally:
            conn.close()

    def _run_query(self, query, params=()):
        conn = self._connect()
        try:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
        finally:
            conn.close()

        return {"rows": [dict(r) for r in rows]}

    def search(self, term: str):
        """Returnerer liste af dnd_class objekter."""
        query = """
            SELECT * FROM dnd5_classes
            WHERE class_name LIKE ? OR class_ability LIKE ?
        """
        params = (f"%{term}%", f"%{term}%")

        d = self._run_query(query, params)
        result = []

        for row in d["rows"]:
            obj = dnd_class(
                class_id=row.get("class_id"),
                class_name=row.get("class_name"),
                class_ability=row.get("class_ability"),
                class_description=row.get("class_description")
            )
            result.append(obj)

        return result

    def load(self, class_id: int):
        query = "SELECT * FROM dnd5_classes WHERE class_id = ?"
        d = self._run_query(query, (class_id,))

        if not d["rows"]:
            return None

        row = d["rows"][0]

        return dnd_class(
            class_id=row.get("class_id"),
            class_name=row.get("class_name"),
            class_ability=row.get("class_ability"),
            class_description=row.get("class_description")
        )


    def load_all(self):
        query = "SELECT * FROM dnd5_classes"
        d = self._run_query(query)

        result = []
        for row in d["rows"]:
            obj = dnd_class(
                class_id=row.get("class_id"),
                class_name=row.get("class_name"),
                class_ability=row.get("class_ability"),
                class_description=row.get("class_description")
            )
            result.append(obj)

        return result


    def insert(self, class_name, class_ability, class_description):
        query = """
            INSERT INTO dnd5_classes (class_name, class_ability, class_description)
            VALUES (?, ?, ?)
        """
        self._execute(query, (class_name, class_ability, class_description))

    # ----------------------------------------------------
    # UPDATE
    # ----------------------------------------------------
    def update(self, class_id: int, updated: dnd_class):
        query = """
            UPDATE dnd5_classes
            SET class_name = ?, class_ability = ?, class_description = ?
            WHERE class_id = ?
        """
        params = (
            updated.class_name,
            updated.class_ability,
            updated.class_description,
            class_id
        )
        self._execute(query, params)

    def delete(self, class_id: int):
        query = "DELETE FROM dnd5_classes WHERE class_id = ?"
        self._execute(query, (class_id,))

if __name__ == "__main__":
    # Lokal import så filen kan køres selvstændigt
    from klasseopgave import dnd_class

    db = Database()

    # Opret eksempelobjekt ud fra din allerede lavede klasse
    sample = dnd_class(None, "barbarian", "strength", "se database bro")

    name = getattr(sample, "class_name", None) or getattr(sample, "name", None)
    ability = getattr(sample, "class_ability", None) or getattr(sample, "abilityscore", None)
    desc = getattr(sample, "class_description", None) or getattr(sample, "desc", None)

    if name:
        db.insert(name, ability, desc)

    # Vis hvad der ligger i databasen nu
    print("All classes:")
    for row in db.load_all():
        # _run_query kan returnere dict eller modelobjekt afhængigt af implementering
        if isinstance(row, dict):
            print(row.get("class_name") or row.get("name"))
        else:
            print(getattr(row, "class_name", None) or getattr(row, "name", None) or str(row))

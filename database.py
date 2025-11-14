import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_DND= str((BASE_DIR / "dndclass.db").resolve())#class-databasen(fordi den anden er lidt for kompliceret)


class Database:
    def __init__(self, DB_DND: str = DB_DND):
        self.DB_DND = DB_DND

    #database class
    def _connect(self):
        #Opret og returner en databaseforbindelse
        conn = sqlite3.connect(self.DB_DND)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute(self, query, params=()):
        #lav en INSERT, UPDATE eller DELETE
        conn = self._connect()
        try:
            conn.execute(query, params)
            conn.commit()
        finally:
            conn.close()

    def _run_query(self, query, params=()):
        #Kører SELECT
        conn = self._connect()
        try:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
        finally:
            conn.close()
        return [dict(row) for row in rows]


    def search(self, term):
        #Søger efter DND Classes ud fra navn eller ability
        query = """
            SELECT * FROM dnd5_classes
            WHERE class_name LIKE ? OR class_ability LIKE ?
        """
        params = (f"%{term}%", f"%{term}%")
        return self._run_query(query, params)

    def load(self, class_id):
        #Hent en klasse ud fra id
        query = "SELECT * FROM dnd5_classes WHERE class_id = ?"
        rows = self._run_query(query, (class_id,))
        return rows[0] if rows else None
    
    def __str__(self):
        # Returnerer kun klassens navn ved print
        return self.__class__.__name__

    def load_all(self):
        #Hent alle klasser
        query = "SELECT * FROM dnd5_classes"
        return self._run_query(query)

    def insert(self, class_name, class_ability, class_description):
        #Tilføj en ny class
        query = """
            INSERT INTO dnd5_classes (class_name, class_ability, class_description)
            VALUES (?, ?, ?)
        """
        self._execute(query, (class_name, class_ability, class_description))
        
    def update(self, class_id, class_name=None, class_ability=None, class_description=None):
        # Opdater en klasse kun de felter der ikke er None bliver ændret
        updates = []
        params = []
        if class_name is not None:
            updates.append("class_name = ?")
            params.append(class_name)
        if class_ability is not None:
            updates.append("class_ability = ?")
            params.append(class_ability)
        if class_description is not None:
            updates.append("class_description = ?")
            params.append(class_description)
        if not updates:
            # Intet at opdatere
            return
        params.append(class_id)
        query = f"UPDATE dnd5_classes SET {', '.join(updates)} WHERE class_id = ?"
        self._execute(query, tuple(params))
        
    def delete(self, class_id):
        # Slet en klasse ud fra id
        query = "DELETE FROM dnd5_classes WHERE class_id = ?"
        self._execute(query, (class_id,))


if __name__ == "__main__":
    # Lokal import så filen kan køres selvstændigt
    from klasseopgave import dnd_class

    db = Database()

    # Opret eksempelobjekt ud fra din allerede lavede klasse
    sample = dnd_class("commoner", "nothing", "weak ahh mofo")

    # Indsæt i databasen ved at bruge modelens felter
    # understøtter både gamle feltnavne (name, abilityscore, desc)
    # og de nye (class_name, class_ability, class_description)
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
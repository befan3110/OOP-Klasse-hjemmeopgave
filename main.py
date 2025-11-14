from database import Database
from klasseopgave import dnd_class

db = Database()

# Insert eksempel
# db.insert("Bloodhunter", "Strength", "Uses cursed blood magic")

# Search
print("Search result for 'Strength':")
for c in db.search("Strength"):
    print(c)
    print("------")

# Load specifik
print("Load class with ID 1:")
print(db.load(1))

# Load all
print("\nAll classes:")
for c in db.load_all():
    print(c)
    print("------")

# Update example
updated_class = dnd_class(None, "Wizard", "Intelligence", "Smart magic boi")
db.update(1, updated_class)

# Delete example
db.delete(14)

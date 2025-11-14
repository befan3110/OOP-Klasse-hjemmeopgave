from database import Database
from klasseopgave import dnd_class

db = Database()

def print_menu():
    print("\n------------------------------")
    print(" D&D Class Database Menu")
    print("------------------------------")
    print("1. Add new class")
    print("2. Search classes")
    print("3. Load class by ID")
    print("4. Show all classes")
    print("5. Update class")
    print("6. Delete class")
    print("0. Exit")
    print("------------------------------")

def add_class():
    print("\n--- Add New Class ---")
    name = input("Class name: ")
    ability = input("Main ability: ")
    desc = input("Description: ")

    db.insert(name, ability, desc)
    print("Class added!")

def search_classes():
    term = input("\nSearch term: ")
    results = db.search(term)

    if not results:
        print("No classes found.")
        return

    print("\n--- Search Results ---")
    for c in results:
        print(c)
        print("----------------------")

def load_class():
    try:
        class_id = int(input("\nClass ID to load: "))
    except ValueError:
        print("Invalid ID.")
        return

    c = db.load(class_id)
    if c:
        print("\n--- Class Loaded ---")
        print(c)
    else:
        print("Class not found.")

def show_all():
    print("\n--- All Classes ---")
    classes = db.load_all()

    if not classes:
        print("No classes in database.")
        return

    for c in classes:
        print(c)
        print("----------------------")

def update_class():
    try:
        class_id = int(input("\nID of class to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    existing = db.load(class_id)
    if not existing:
        print("Class not found.")
        return

    print("\nLeave fields empty to keep old values.")
    new_name = input(f"New name ({existing.class_name}): ") or existing.class_name
    new_ability = input(f"New ability ({existing.class_ability}): ") or existing.class_ability
    new_desc = input(f"New description ({existing.class_description}): ") or existing.class_description

    updated = dnd_class(
        class_id=class_id,
        class_name=new_name,
        class_ability=new_ability,
        class_description=new_desc
    )

    db.update(class_id, updated)
    print("Class updated!")

def delete_class():
    try:
        class_id = int(input("\nID of class to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    confirm = input("Are you sure? (y/n): ").lower()
    if confirm != "y":
        print("Cancelled.")
        return

    db.delete(class_id)
    print("Class deleted!")


while True:
    print_menu()
    choice = input("Choose option: ").strip()

    if choice == "1":
        add_class()
    elif choice == "2":
        search_classes()
    elif choice == "3":
        load_class()
    elif choice == "4":
        show_all()
    elif choice == "5":
        update_class()
    elif choice == "6":
        delete_class()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")

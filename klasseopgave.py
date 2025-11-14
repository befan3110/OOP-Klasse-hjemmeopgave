class dnd_class:
    def __init__(self, class_id=None, class_name=None, class_ability=None, class_description=None):
        self.class_id = class_id
        self.class_name = class_name
        self.class_ability = class_ability
        self.class_description = class_description

    def __str__(self):
        return (
            f"[{self.class_id}] {self.class_name}\n"
            f"Ability: {self.class_ability}\n"
            f"Description: {self.class_description}"
        )

"""
class spells:
    def __init__(self, name, level, casttime, range, components, dura, desc, higher_levels):

        self.name = name
        self.level = level
        self.casttime = casttime
        self.range = range
        self.components = components
        self.dura = dura
        self.desc = desc
        self.higher_levels = higher_levels

    def showspell(self):
        print(f"{self.name}, level: {self.level}, casting time: {self.casttime}, components: {self.components}, duration: {self.dura}, described by: {self.desc}, higher levels: {self.higher_levels}")

Fireball = spells("Fireball", "3rd", "action", "60 feet", "gunpowder idk", "instant", "BOOM!", "BIGGER BOOM!")

Fireball.showspell()
"""
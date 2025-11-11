class dnd_class:
    def __init__(self, name, abilityscore, desc):
        self.name = name
        self.abilityscore = abilityscore
        self.desc = desc
    def showclass(self):
        print(f"your searched class is {self.name}, it uses {self.abilityscore} and is described by {self.desc}")


Class1 = dnd_class("barbarian", "strength", "se database bro")

Class1.showclass()

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
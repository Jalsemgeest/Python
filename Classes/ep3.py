class EvolvableMonster():

    def __init__(self, name):
        self.name = name

    def evolve(self):
        if self.name == "Bulbasaur":
            return "Ivysaur,Grass,70,70"
        # ...
        return None

class Pokemon(EvolvableMonster):
    
    super_effective_mod = 1.5
    num_of_pokemon = 0

    def __init__(self, name, type, hp, attack):
        super().__init__(name)
        self.type = type
        self.hp = hp
        self.attack = attack
        Pokemon.num_of_pokemon += 1

    def attackLog(self):
        return "{} of type {}".format(self.attack, self.type)
    
    def defense(self, attack_type, amount):
        if (Pokemon.is_super_effective(self.type, attack_type)):
            return self.super_effective(amount)
        return amount

    def super_effective(self, amount):
        return amount * Pokemon.super_effective_mod

    @staticmethod
    def what():
        return "A pokemon is a monster that has attributes and a species that may be able to evolve. Also they fight - but it's totally fine and not frowned upon :)"
    
    @staticmethod
    def is_super_effective(poke_type, attack_type):
        if poke_type == "Grass" and attack_type == "Fire":
            return True
        return False

    def evolve(self):
        result = super().evolve()
        if result == None:
            return self
        return Pokemon.pokemon_from_string(result)

    @classmethod
    def pokemon_from_string(cls, string):
        name, type, hp, attack = string.split(',')
        return cls(name, type, hp, attack)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Pokemon("{}", "{}", {}, {})'.format(self.name, self.type, self.hp, self.attack)

    def __add__(self, other):
        if other.name == self.name:
            return Pokemon.evolve(self)
        return 
    
    def __eq__(self, other):
        return other.name == self.name
    
    '''
    ne - not equal (!=)
    lt - checks if something is less than (<)
    gt - checks if something is greater than (>)
    le - (<=)
    ge - (>=)
    '''

bulb = Pokemon("Bulbasaur", "Grass", 45, 49)
charm = Pokemon("Charmander", "Fire", 45, 49)

# bulb - uses __repr__ for programmers
# print(bulb) - uses __str__ for users

# print(bulb == Pokemon("Bulbasaur", "Grass", 45, 49))

print(bulb.evolve())

from enum import Enum
import json
import random
import termimon.termimon_generator as termimon_generator


class Move:
    def __init__(self, Movename, Description, Damage, Type, Statuseffect, Chance, Cooldown):
        self.Movename = Movename
        self.Description = Description
        self.Damage = Damage
        self.Type = Type
        self.Statuseffect = Statuseffect
        self.Chance = Chance
        self.Cooldown = Cooldown


class Dimensions:
    def __init__(self, Length, Width, Height):
        self.Length = Length
        self.Width = Width
        self.Height = Height


class Stats:
    def __init__(self, damage, magic, health, defense, magicdefense, speed):
        self.damage = damage
        self.magic = magic
        self.health = health
        self.defense = defense
        self.magicdefense = magicdefense
        self.speed = speed


class TermimonInformation:
    def __init__(self, Name, Types, Moves, Icon, Weight, Dimensions, Stats, description=None, parents=None):
        self.Name = Name
        self.Types = Types if Types is not None else []
        self.Moves = Moves  # List of Move objects
        self.Icon = Icon
        self.Weight = Weight
        self.Dimensions = Dimensions
        self.Stats = Stats
        self.description = description
        self.parents = parents if parents is not None else []  # List of TermimonInformation

    def display(self):
        print(f"Species: {self.Name}")


# --- Utilities: Conversion ---


def dict_to_termimoninformation(data):
    moves = [Move(
        m['Movename'],
        m['Description'],
        m['Damage'],
        m['Type'],
        m['Statuseffect'],
        m['Chance'],
        m['Cooldown']
    ) for m in data['Moves']]
    dimensions = Dimensions(
        data['Dimensions']['Length'],
        data['Dimensions']['Width'],
        data['Dimensions']['Height'],
    )
    stats = Stats(
        data['Stats']['damage'],
        data['Stats']['magic'],
        data['Stats']['health'],
        data['Stats']['defense'],
        data['Stats']['magicdefense'],
        data['Stats']['speed'],
    )
    parents = []
    if 'parents' in data and data['parents']:
        for p in data['parents']:
            parents.append(dict_to_termimoninformation(p))
    return TermimonInformation(
        Name=data.get('Name', None),
        Types=data.get('Types', []),
        Moves=moves,
        Icon=data.get('Icon', None),
        Weight=data['Weight'],
        Dimensions=dimensions,
        Stats=stats,
        description=data.get('description', None),
        parents=parents,
    )


def termimon_to_dict(ti):
    return {
        "Name": ti.Name,
        "Types": ti.Types,
        "Moves": [{
            "Movename": m.Movename,
            "Description": m.Description,
            "Damage": m.Damage,
            "Type": m.Type,
            "Statuseffect": m.Statuseffect,
            "Chance": m.Chance,
            "Cooldown": m.Cooldown,
        } for m in ti.Moves],
        "Icon": ti.Icon,
        "Weight": ti.Weight,
        "Dimensions": {
            "Length": ti.Dimensions.Length,
            "Width": ti.Dimensions.Width,
            "Height": ti.Dimensions.Height,
        },
        "Stats": {
            "damage": ti.Stats.damage,
            "magic": ti.Stats.magic,
            "health": ti.Stats.health,
            "defense": ti.Stats.defense,
            "magicdefense": ti.Stats.magicdefense,
            "speed": ti.Stats.speed,
        },
        "description": ti.description,
        "parents": [termimon_to_dict(p) for p in ti.parents] if hasattr(ti, "parents") else [],
    }

# --- Data Classes ---


class Move:
    def __init__(self, Movename, Description, Damage, Type, Statuseffect, Chance, Cooldown):
        self.Movename = Movename
        self.Description = Description
        self.Damage = Damage
        self.Type = Type
        self.Statuseffect = Statuseffect
        self.Chance = Chance
        self.Cooldown = Cooldown


class Dimensions:
    def __init__(self, Length, Width, Height):
        self.Length = Length
        self.Width = Width
        self.Height = Height


class Stats:
    def __init__(self, damage, magic, health, defense, magicdefense, speed):
        self.damage = damage
        self.magic = magic
        self.health = health
        self.defense = defense
        self.magicdefense = magicdefense
        self.speed = speed


class TermimonInformation:
    def __init__(self, Name, Types, Moves, Icon, Weight, Dimensions, Stats, description=None, parents=None):
        self.Name = Name
        self.Types = Types if Types is not None else []
        self.Moves = Moves  # List of Move objects
        self.Icon = Icon
        self.Weight = Weight
        self.Dimensions = Dimensions
        self.Stats = Stats
        self.description = description
        self.parents = parents if parents is not None else []

    def display(self):
        print(f"Species: {self.Name}")
        print(f"Types: {', '.join(self.Types)}")
        print(f"Description: {self.description}")
        print("Parents:", ', '.join(
            [parent.Name for parent in self.parents]) if self.parents else "Unknown")
        print(f"Weight: {self.Weight}kg, Size: {self.Dimensions.Length}x{
              self.Dimensions.Width}x{self.Dimensions.Height}m")
        print("Moves:")
        for m in self.Moves:
            print(f" - {m.Movename}: {m.Description} (Type: {m.Type}, Dmg: {
                  m.Damage}, Effect: {m.Statuseffect} {m.Chance}%)")


class LifeStage(Enum):
    BABY = "Baby"
    TEEN = "Teen"
    ADULT = "Adult"
    OLDIE = "Oldie"
    DEAD = "Dead"


class TermimonEntity:
    def __init__(self, info, environment, nickname=None):
        self.info = info
        self.environment = environment  # Reference to TermiVironment
        self.nickname = nickname or info.Name
        self.current_health = info.Stats.health
        self.age = 0  # Time units (100 units = 1 day)
        self.lifestage = LifeStage.BABY
        self.cooldowns = {move.Movename: 0 for move in info.Moves}
        self.status_effects = []

    def progress_age(self, time_units=1):
        self.age += time_units
        previous_stage = self.lifestage
        if self.age < 1000:
            self.lifestage = LifeStage.BABY
        elif self.age < 3000:
            self.lifestage = LifeStage.TEEN
        elif self.age < 7000:
            self.lifestage = LifeStage.ADULT
        elif self.age < 10000:
            self.lifestage = LifeStage.OLDIE
        else:
            self.lifestage = LifeStage.DEAD
        if self.lifestage != previous_stage:
            print(f"{self.nickname} evolved to {self.lifestage.value} stage!")

    @property
    def is_breedable(self):
        return self.lifestage == LifeStage.ADULT

    def breed(self, partner):
        if not self.is_breedable or not partner.is_breedable:
            print(f"{self.nickname} or {
                  partner.nickname} are not both adults!")
            return None
        return self.environment.breed_entities(self, partner)

    def decrement_cooldowns(self):
        for k in self.cooldowns:
            if self.cooldowns[k] > 0:
                self.cooldowns[k] -= 1

    def attack(self, target, move_name):
        move = None
        for m in self.info.Moves:
            if m.Movename == move_name:
                move = m
                break
        if not move:
            print(f"{self.nickname} doesn't know {move_name}!")
            return
        if self.cooldowns[move_name] > 0:
            print(f"{self.nickname}'s {move_name} is on cooldown for {
                  self.cooldowns[move_name]} more turns!")
            return
        base_damage = move.Damage + self.info.Stats.damage
        reduced_damage = max(1, base_damage - target.info.Stats.defense)
        target.current_health = max(0, target.current_health - reduced_damage)
        effect_applied = False
        if move.Statuseffect != "None" and random.randint(1, 100) <= move.Chance:
            target.status_effects.append(move.Statuseffect)
            effect_applied = True
        self.cooldowns[move_name] = move.Cooldown
        self.decrement_cooldowns()
        target.decrement_cooldowns()
        print(f"{self.nickname} used {move.Movename} on {target.nickname}! {
              target.nickname} took {reduced_damage} damage.")
        if effect_applied:
            print(f"{target.nickname} is now affected by {move.Statuseffect}!")

    def display(self):
        print(f"{self.nickname} ({self.lifestage.value}, Age: {
              self.age} units) | Species: {self.info.Name}")
        print(f"HP: {self.current_health}/{self.info.Stats.health}")
        print(f"Status Effects: {', '.join(
            self.status_effects) if self.status_effects else 'None'}")

# --- TermiDex ---


class TermiDex:
    def __init__(self, filename='termidex.json'):
        self.filename = filename
        self.termimons = []
        self.load()

    def add(self, termimoninfo):
        if any(ti.Name == termimoninfo.Name for ti in self.termimons):
            return
        self.termimons.append(termimoninfo)
        self.save()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump([termimon_to_dict(ti)
                      for ti in self.termimons], f, indent=2)

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            self.termimons = [dict_to_termimoninformation(d) for d in data]
        except Exception:
            self.termimons = []

    def get(self, name):
        for ti in self.termimons:
            if ti.Name == name:
                return ti
        return None

    def display(self):
        print(f"TermiDex: {len(self.termimons)} entries")
        for t in self.termimons:
            print(f"- {t.Name} ({', '.join(t.Types)})")


class TermiVironment:
    def __init__(self, termidex=None, party=None, storage=None):
        self.termidex = termidex or TermiDex()
        self.entities = []  # All living entities (for world simulation)
        # List of TermimonEntity (active, max 6)
        self.current_party = party or []
        # List of TermimonEntity (PC storage)
        self.storage = storage or []
        self.time = 0  # time units (100 = 1 day)

    def add_entity(self, entity, to_party=False):
        # Adds to environment and (optionally) to party if space, otherwise to storage
        self.entities.append(entity)
        if to_party and len(self.current_party) < 6:
            self.current_party.append(entity)
        else:
            self.storage.append(entity)

    def move_to_party(self, entity):
        if entity in self.current_party:
            print(f"{entity.nickname} is already in the party!")
            return
        if len(self.current_party) >= 6:
            print("Party is full! Remove someone first.")
            return
        if entity in self.storage:
            self.storage.remove(entity)
        self.current_party.append(entity)
        print(f"Moved {entity.nickname} to the party.")

    def move_to_storage(self, entity):
        if entity in self.current_party:
            self.current_party.remove(entity)
            self.storage.append(entity)
            print(f"Moved {entity.nickname} to storage.")
        else:
            print(f"{entity.nickname} is not in the party.")

    def remove_entity(self, entity):
        # Remove everywhere
        if entity in self.current_party:
            self.current_party.remove(entity)
        if entity in self.storage:
            self.storage.remove(entity)
        if entity in self.entities:
            self.entities.remove(entity)

    def passtime(self, time_units=1):
        self.time += time_units
        for ent in self.entities:
            ent.progress_age(time_units)
            if ent.lifestage == LifeStage.DEAD:
                print(f"{ent.nickname} has died.")
        self.entities = [
            e for e in self.entities if e.lifestage != LifeStage.DEAD]
        # Clean up party/storage for dead Termimons too
        self.current_party = [
            e for e in self.current_party if e.lifestage != LifeStage.DEAD]
        self.storage = [
            e for e in self.storage if e.lifestage != LifeStage.DEAD]

    def breed_entities(self, parent1, parent2):
        d1 = termimon_to_dict(parent1.info)
        d2 = termimon_to_dict(parent2.info)
        result = termimon_generator.breed(d1, d2)
        if isinstance(result, str):
            result = json.loads(result)
        info = dict_to_termimoninformation(result)
        self.termidex.add(info)
        child = TermimonEntity(info, self)
        self.add_entity(child)
        print(f"{parent1.nickname} and {
              parent2.nickname} bred! Offspring: {child.nickname}")
        return child

    def generate_starter(self, starter_type, to_party=True):
        result = termimon_generator.startermon(starter_type)
        if isinstance(result, str):
            result = json.loads(result)
        info = dict_to_termimoninformation(result)
        self.termidex.add(info)
        entity = TermimonEntity(info, self)
        self.add_entity(entity, to_party=to_party)
        print(f"Generated new starter: {entity.nickname}")
        return entity

    def display(self):
        print(f"\nTermiVironment | Time: {self.time} units | {
              len(self.entities)} living Termimons")
        print(f"Current Party ({len(self.current_party)}/6):")
        for ent in self.current_party:
            ent.display()
        print(f"Storage ({len(self.storage)}):")
        for ent in self.storage:
            ent.display()
        self.termidex.display()

    # ---- Saving and Loading ----
    def save_to_file(self, filename="termivironment.json"):
        data = {
            "time": self.time,
            "termidex": [termimon_to_dict(ti) for ti in self.termidex.termimons],
            "entities": [self._entity_to_dict(e) for e in self.entities],
            "current_party": [self.entities.index(e) for e in self.current_party],
            "storage": [self.entities.index(e) for e in self.storage]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Environment saved to {filename}.")

    @classmethod
    def load_from_file(cls, filename="termivironment.json"):
        with open(filename, "r") as f:
            data = json.load(f)
        termidex = TermiDex()
        termidex.termimons = [dict_to_termimoninformation(
            d) for d in data["termidex"]]
        env = cls(termidex=termidex)
        # First, create all entities without links
        env.entities = [cls._entity_from_dict(
            ed, env) for ed in data["entities"]]
        # Set up party and storage lists using indices
        env.current_party = [env.entities[i]
                             for i in data.get("current_party", [])]
        env.storage = [env.entities[i] for i in data.get("storage", [])]
        env.time = data.get("time", 0)
        print(f"Environment loaded from {filename}.")
        return env

    @staticmethod
    def _entity_to_dict(entity):
        return {
            "info": termimon_to_dict(entity.info),
            "nickname": entity.nickname,
            "current_health": entity.current_health,
            "age": entity.age,
            "lifestage": entity.lifestage.value,
            "cooldowns": entity.cooldowns,
            "status_effects": entity.status_effects,
        }

    @staticmethod
    def _entity_from_dict(data, environment):
        info = dict_to_termimoninformation(data["info"])
        ent = TermimonEntity(info, environment, nickname=data.get("nickname"))
        ent.current_health = data.get("current_health", info.Stats.health)
        ent.age = data.get("age", 0)
        ent.lifestage = LifeStage(data.get("lifestage", "Baby"))
        ent.cooldowns = data.get(
            "cooldowns", {move.Movename: 0 for move in info.Moves})
        ent.status_effects = data.get("status_effects", [])
        return ent

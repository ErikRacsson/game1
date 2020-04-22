# lib_fa_game 
import random
import types

# Return codes for bad things.  TODO: Replace this construct with exception raising
SUCCESS = 0
ERR_NAME_EXISTS = 1
ERR_NOT_THERE = 2

class characters:
    names = {}
    
    def __init__(self, name, location, race="human"):
        self.name = name
        self.race = race
        self.attributes = {}
        self.__init_attributes()
        characters.names[name] = self
        self.location = "new"
        location.enter(self)
        self.inventory = []
    
    def __init_attributes(self):
        self.attributes["strength"] = random.randint(1,10)
        self.attributes["intelligence"] = random.randint(1,10)
        self.attributes["dexterity"] = random.randint(1,10)
    
    def describe(self):
        print("{} is a {}.".format(self.name, self.race))
        for attribute in self.attributes:
            print(f"\t{attribute} is {self.attributes[attribute]}")
    
    def createchar(name, location):
        ''' attempt to create a new character with given name and place in the
            specified location
            name - string representing the desired name for the character
            location - location object where character should be placed
            
            returns character object reference or ERR_NAME_EXISTS if
            character name already exists.
        '''
        if name in characters.names:
            return(ERR_NAME_EXISTS)
        else:
            return(characters(name, location))
    
    def move(self, port):
        ''' move a character to a new location by way of a specified port
            (door) name
        
            port = string that is the name of the port in the location
                   of the character
        '''
        valid_ports = self.location.ports
        return_list = []
        if port in valid_ports:
            return_list.extend(valid_ports[port].use(self))
        else:
            return_list.append(f'There is no way you can reach ' 
                               f'the {port} here.')
        return(return_list)
        
    def look_around(self):
        ''' return a string list describing the character's environment '''
        return_list = []
        return_list.append(f'{self.name} is in the {self.location.name}')
        return_list.extend(self.location.look())
        return(return_list)
    
    def take(self, thing_to_take):
        #Look to see if item is in room.
        items_in_room = self.location.list_entities()
        if thing_to_take in items_in_room:
            self.inventory.append(self.location.take_entity(thing_to_take))
            return(SUCCESS)
        return(ERR_NOT_THERE)
        #If in room, character take item into inventory (removed from room's
        #inventory)
        #If not in room, fail to take item
    
    def view_inventory(self):
        return_list = []
        for item in self.inventory:
            return_list.append(item.name)
        return(return_list)

    def count():
        return(len(characters.names))
        
    def describechar(name):
        if name in characters.names:
            characters.names[name].describe()
        else:
            print("Sorry, can't find anyone named {}.".format(name))
            
    def list():
        for character in characters.names :
            print(f'{character} is in '
                  f'{characters.names[character].location.name}')


class location:
    names = dict()
    
    def __init__(self, name):
        self.name = name
        location.names[name] = self
        self.description = "This is a generic location.  Everything is normal"
        self.short_description = "Generic Location"
        self.characters = dict()
        self.ports = {}
        self.entities = {}
        
    def look(self):
        return_list = []
        return_list.append(self.name)
        return_list.append(self.description)
        return_list.append(f"There are {len(self.characters)} characters here:")
        for name in self.characters:
            return_list.append(f'\t{name}')
        return_list.append(f"There are {len(self.entities)} items here:")
        for name in self.entities:
            return_list.append(f'\t{name}')
        return_list.append(f'There are {len(self.ports)} '
                           f'ways in and out of here:')
        for port_name in self.ports:
            return_list.append(f'\t{port_name}')
        return(return_list)
        
        
    def enter(self, character):
        return_list = []
        if character.location != "new":
            return_list.extend(character.location.exit(character))
        return_list.append(f'{character.name} has entered the {self.name}')
        return_list.append(f'{self.short_description}')
        self.characters[character.name] = character
        character.location = self
        return(return_list)
    
    def exit(self, character):
        return_list = []
        del self.characters[character.name]
        return_list.append(f'{character.name} has exited the {self.name}')
        return(return_list)
        
    def look_chars(self):
        for character in self.characters:
            print(f'{character} is here')
            
    def describe_chars(self):
        for character in self.characters:
            character.describe()

    def put_entity(self, item):
        self.entities[item.name] = item
        
    def list_entities(self):
        return_list = []
        for entity in self.entities:
            return_list.append(entity)
        return(return_list)
    
    def take_entity(self, item):
        if item in self.entities:
            return(self.entities.pop(item))

    def list_verbose():
        return_list = []
        for loc in location.names :
            return_list.append(f'{loc}')
            for character in location.names[loc].characters:
                return_list.append(f'\tA funloving character named {character}')
        return(return_list)        
        
    def list():
        return_list = []
        for loc in location.names:
            return_list.append(loc)
        return(return_list)

class ports:
    __all = {}
    def __init__(self, name):
        self.name = name
        self.description = "This is a generic port.  Everything is normal"
        self.short_description = "Generic Port"
        self.side_a = "empty"
        self.side_b = "empty"
        self.travel = False
        ports.__all[name] = self
        
    def connect(self, side_a, side_b):
        self.travel = True
        self.side_a = side_a
        self.side_b = side_b
        side_a.ports[side_b.name+self.name] = self
        side_b.ports[side_a.name+self.name] = self
        
    def use(self, character):
        return_list = []
        characters_location = character.location
        if self.travel:
            if characters_location == self.side_a:
                return_list.extend(self.side_b.enter(character))
            else:
                return_list.extend(self.side_a.enter(character))
        else:
            return_list.append("The way is blocked!")
        return(return_list)
    
    def list():
        for port in ports.__all:
            print(f'{port} is connecting {ports.__all[port].side_a.name} '
                  f'to {ports.__all[port].side_b.name}')

class entity:
    def __init__(self, name):
        self.name = name
        self.description = "Long description of an entity"
        self.short_description = "Short description of an entity"
     

def format(list):
    for line in list:
        print(line)

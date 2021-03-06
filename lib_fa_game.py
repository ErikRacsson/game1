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
        self.__init_inventory()
    
    def __init_attributes(self):
        self.attributes["strength"] = random.randint(1, 10)
        self.attributes["intelligence"] = random.randint(1, 10)
        self.attributes["dexterity"] = random.randint(1, 10)

    def __init_inventory(self):
       lint = entity("A tuft of lint")
       ring = entity("gold ring")
       mousecatool = entity("mousecatool")
       mousecatool.description = "A secret mousecatool that will help us later!"
       self.inventory.append(lint)
       self.inventory.append(ring)
       self.inventory.append(mousecatool)

    def drop(self, thing_to_drop):
        return_list = []
        if thing_to_drop.isdigit():
            self.location.put_entity(self.inventory[((int(thing_to_drop)-1))])
            return_list.append(f'\n{self.inventory[(int(thing_to_drop)-1)].name} dropped!\n')
            self.inventory.pop(int(thing_to_drop)-1)
        else:
            for item in self.inventory:
                if item.name == thing_to_drop:
                    self.location.put_entity(item)
                    self.inventory.remove(item)
                    return_list.append(f'\n {thing_to_drop} dropped!\n')
                    break
        return(return_list)

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
        return_list = []
        #Look to see if item is in room.
        items_in_room = self.location.list_entities()
        if thing_to_take in items_in_room:
            self.inventory.append(self.location.take_entity(thing_to_take))
            return_list.append(f" You've taken {thing_to_take} ")
        return(return_list)
        #If in room, character take item into inventory (removed from room's
        #inventory)
        #If not in room, fail to take item
    
    def view_inventory(self):
        return_list = []
        i = 0
        for item in self.inventory:
            i += 1
            return_list.append(f' {i} {item.name}')
        return (return_list)

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
        self.items = {}

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
        

class envelope(entity):
    def __init__(self, name, width=4.25, height=9.5, window=False):
          entity.__init__(self, name)
          self.description = "describe"
          self.width = width
          self.height = height
          self.window = window
          self.flap_state = "Closed"
          self.contents = []
                   
    def size(self):
          return("{}inches by {} inches".format(self.width, self.height))
                
    def describe(self):
        return_list = []
        return_list.append("f'The size of the envelope is: {self.size}.")
        return_list.append("f'The flap state is {self.flap_state}.")
        if self.window:
            return_list.append("this has a window")
        else:
            return_list.append("this doesn't have a window")
        return(return_list)
                       
    def open(self):
        self.flap_state = "Open"
        
    def insert(self, ThingtoInsert):
        return_list = []
        self.contents.append(ThingtoInsert)
        return_list.append(f"You've inserted the {ThingtoInsert.name}!")
        return(return_list)

    def remove(self, ThingtoRemove):
        return_list = []
        self.contents.remove(ThingtoRemove)
        return_list.append(f"You've removed the {ThingtoRemove.name}!")
        return(return_list)
    
    def look_inside(self):
        return_list = []
        for entity in self.contents:
            return_list.append(f'There is a {entity.name} in here!')
        return(return_list)
    
    def take_envelope_contents(self, thing_to_take):
         contents_in_envelope = self.envelope.list_entities()
         if thing_to_take in contents_in_envelope:
            self.inventory.append(self.envelope.take_entity(thing_to_take))
            return_list.append(f" You've taken {thing_to_take} ")
         return(return_list)
        

class big_envelope(envelope):
    def __init__(self, name):
        envelope.__init__(self, name, 100, 200)
        
        
class CD_envelope(envelope):
    def __init__(self, name):
        envelope.__init__(self, name, 5, 5, True)
        self.description = \
        '''This envelope is rather small, only 5" by 5". A round window on the
           front indicates that this particular envelope is used to hold disks.
           The white color is rather boring, but I suppose it IS just an
           envelope. It doesn't have to look interesting.'''
        self.short_description = \
        '''This small envelope is used to hold disks.'''
        
 

class CD(entity):
    def __init__(self, name, artist="", album_name="" ):
        entity.__init__(self, name)
        self.artist = artist
        self.album_name = album_name
        self.short_description = f'{album_name} CD'
        self.description = f'A CD with the album {album_name} by {artist}'


def format(list):
    for line in list:
        print(line)

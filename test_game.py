import lib_fa_game as game

print("-- Creating map of locations with links")        
mailbox = game.location("Mailbox")
mailbox.short_description = "This is the inside of a mailbox"
mailbox.description = ''' It is very dark and cramped.  Frankly it is leaving you wondering how you even got here.
Very odd.  Anyway, looking around you can see what looks like steps leading to a patio...'''

shrub = game.location("Shrubbery")
shrub.short_description = "This is the shrubbery"
shrub.description = " It is a very nice shrubbery, neatly trimmed.  Or, rather it would be very nice if you could see \n \
it.  As it is, you find yourself crouched down among the branches trying to avoid getting yourself too \n \
dirty.  Looking around you notice that there does seem to be a way out..." 

patio = game.location("Patio")
patio.short_description = "Lovely patio in front of house"
patio.description = " The patio is made of tile and very well kept, although a bit barren.  I suppose having no \n \
furniture (or anything else for that matter) does make it easier to clean up.  There is an ornate door \n \
to the house here.  You can just make out the foyer through it."

foyer = game.location("Foyer")
foyer.short_description = "Formal entrance room of the house"
foyer.description = " This is a formal foyer.  There is a tapestry hanging on one wall that rather reminds you \n \
of a palace, which this house certainly is not.  The ceiling is a bit low for the size of that wall hanging \n \
and it makes it appear out of place.  The umbrella stand is empty, as is the coat rack.  There are doors \n \
leading out of this room."

kitchen = game.location("Kitchen")
kitchen.short_description = "House kitchen"
kitchen.description = ''' This is the kitchen.  It is somewhat messy, but you may be able
to make a sandwich if you were to push the dirty dishes off the counter'''

kitchen_door = game.ports("Door")
kitchen_door.connect(kitchen,foyer)

# Create door between patio and foyer
patio_foyer_door=game.ports("door")
patio_foyer_door.connect(patio, foyer)
# Create steps leading between mailbox and patio
path = game.ports("Steps")
path.connect(mailbox, patio)
# Create path between mailbox and shrub
path = game.ports("Pathway")
path.connect(mailbox, shrub)

print("-- Creating test characters and dropping them into locations")

sue = game.characters.createchar("Sue",shrub)
joe = game.characters.createchar("Joe",mailbox)

player_name = input("What is your name? ")
player_char = game.characters.createchar(player_name,mailbox)
while player_char == game.ERR_NAME_EXISTS:
    player_name = input(f"I'm sorry, {player_name} but someone with your name is already here.\nPlease choose another name")
    player_char = game.characters.createchar(player_name,mailbox)

commands_list = {'Look' : 'Look around', 'Go' : 'as in "go PatioSteps"', 'Exit' : 'as in exit the game', 'Commands' : 'as in give this list'}

def commands():
    print(f'You can choose from one of the following commands:\n')
    for command in commands_list:
        print(f'{command}:  {commands_list[command]}')
    

print(f"\n\n\nWelcome to the game {player_name}!")
game.format(player_char.look_around())
print(f'\nWhat would you like to do now, {player_name}? ')
command = input(f'Type "commands" for options \n')
print('\n\n\n')
while command != "exit":
    command_list = command.split(' ')
    action = command_list[0].upper()
    if len(command_list) > 1:
        object = command_list[1]
    if action == "GO":
        game.format(player_char.move(object))
    elif action == "LOOK":
        game.format(player_char.look_around())
    elif action == "COMMANDS":
        commands()
    command = input(f'\nWhat would you like to do now, {player_name}? ')
    print('\n\n')
    
print(f'Goodbye {player_name}, I do hope you had fun')
    



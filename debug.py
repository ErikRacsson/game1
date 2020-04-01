#  File to use for just testing and debugging new features etc...
import lib_fa_game as game

room = game.location("room")

character = game.characters.createchar("Dayle", room)

toy = game.entity("toy")

room.put_entity(toy)

game.format(room.look())

print("------ROOM inventory BEFORE take")
game.format(room.list_entities())

print("-----character inventory after take")
game.format(character.view_inventory())

print("-----taking toy")
character.take("toy")

print("-----character inventory after take")
game.format(character.view_inventory())

print("-----ROOM inventory after take")
game.format(room.list_entities())
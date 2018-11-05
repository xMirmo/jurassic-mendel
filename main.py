import libtcodpy as libtcod
from objects.objects import Player
from objects.map import Map

def handle_keys(currentMap, player):
 
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game

    save_x = player.x
    save_y = player.y

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP) or chr(key.c) == "k":
        player.move_object(0, -1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or chr(key.c) == "j":
        player.move_object(0, 1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or chr(key.c) == "h":
        player.move_object(-1, 0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or chr(key.c) == "l":
        player.move_object(1, 0)
    elif chr(key.c) == "y":
    	player.move_object(-1, -1)
    elif chr(key.c) == "u":
    	player.move_object(1, -1)
    elif chr(key.c) == "b":
    	player.move_object(-1, 1)
    elif chr(key.c) == "n":
    	player.move_object(1, 1)

    if currentMap.getTile(player.x, player.y).block:
        player.x = save_x
        player.y = save_y


SCREEN_WIDTH = 40
SCREEN_HEIGHT = 40

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'jurassic-mendel', False)

player = Player('@', 0, 0)

currentMap = Map(40, 40)

currentMap.getTile(10,10).block = True
currentMap.getTile(10,11).block = True

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    currentMap.draw()
    player.draw()
    libtcod.console_flush()

    player.clear()
    exit = handle_keys(currentMap, player)
    if exit:
        break
import libtcodpy as libtcod
from collections import deque
from objects.objects import Player

from objects.map import *
from states.states import *

class Game():
    def __init__(self):
        # FIXME this first part should be read from a config file
        SCREEN_WIDTH = 40
        SCREEN_HEIGHT = 40

        libtcod.console_set_custom_font('resources/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'jurassic-mendel', False)
        libtcod.console_set_default_foreground(0, libtcod.white)

        self.event_queue = deque()

        # FIXME we start with the room, but it could be anything else

        # self.player = Player('@', 5, 5)

        self.current_map = MapBuilder(1).make_map(SCREEN_WIDTH, SCREEN_HEIGHT)

        starting_position = self.current_map.get_free_space()
        self.player = Player('@', starting_position[0], starting_position[1])
        self.current_map.entity_list.append(self.player)

        self.currentDrawMap = DrawableMap(self.current_map, self.player)

        self.game_states_map = {
            "Active": ActiveState(),
            "Pause": PauseState(),
        }

        self.game_state = self.game_states_map.get("Active")



    def enqueue_event(self, eventName, eventData):
        self.event_queue.append((eventName, eventData))
    
    def dequeue_event(self):
        return self.event_queue.pop()
    
    def change_game_state(self, newState):
        self.game_state = newState
    
    def run_game(self):
        while not libtcod.console_is_window_closed():
            libtcod.console_clear(0)
            self.game_state.handle_video(self)
            libtcod.console_flush()

            self.game_state.handle_world(self)
            # handling events
            while self.event_queue:
                (eventName, eventData) = self.dequeue_event()
                # FIXME maybe a dictonary of functions ?
                if(eventName == "exit_game"):
                    sys.exit()
                elif(eventName == "player_movement"):
                    player_new_position = (self.player.x + eventData[0][0], self.player.y + eventData[0][1])
                    enemy = self.current_map.is_anyone_at(player_new_position[0], player_new_position[1])
                    if enemy:
                        print(enemy.get_infos())
                    elif self.current_map.is_blocked_at(player_new_position[0], player_new_position[1]):
                        self.player.move_object(eventData[0])
                elif(eventName == "monster_movement"):
                    vector = eventData[0]
                    enemy = eventData[1]
                    enemy_new_position = (enemy.x + vector[0], enemy.y + vector[1])
                    if self.current_map.is_anyone_at(enemy_new_position[0], enemy_new_position[1]):
                        pass
                    elif self.current_map.is_blocked_at(enemy_new_position[0], enemy_new_position[1]):
                        enemy.move_object(vector)
                elif(eventName == "monster_action"):
                    if(eventData[0] == "pip"):
                        print(str(eventData[1]) + " says: Pip!")
                #FIXME these should be a static factories        
                elif(eventName == "go_pause"):
                    self.game_state = self.game_states_map.get("Pause")
                elif(eventName == "go_active"):
                    self.game_state = self.game_states_map.get("Active")

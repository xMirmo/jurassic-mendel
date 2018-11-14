import libtcodpy as libtcod
import sys


class GameState():
    def __init__(self, nameState):
        self.nameState = nameState
    
    def handle_video(self, game):
        pass
    
    def handle_world(self, game):
        pass


class ActiveState(GameState):
    def __init__(self):
        GameState.__init__(self, "Active")
    
    def handle_video(self, game):
        game.currentDrawMap.draw()
        game.player.draw()
        for enemy in game.current_map.entity_list:
            if game.currentDrawMap.is_in_fov(enemy.x, enemy.y):
                enemy.draw()

    def handle_world(self, game):
        for enemy in game.current_map.entity_list:
            action = enemy.act(game)
            #FIXME Maybe a tuple with 3 elements instead?
            game.enqueue_event(action[0], (action[1], enemy))


class PauseState(GameState):
    def __init__(self):
        GameState.__init__(self, "Pause")
    
    def handle_video(self, game):
        libtcod.console_print_ex(0, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "Pause")

    def handle_world(self, game):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            game.enqueue_event("exit_game", None)
        if key.vk == libtcod.KEY_ENTER:
            game.enqueue_event("go_active", None)


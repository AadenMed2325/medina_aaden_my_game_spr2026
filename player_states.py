from state_machine import *
from settings import *

# first class for when the Player is stationary
class PlayerIdleState(State):
    def __init__(self, player):
        self.player = player
        self.name = "idle"
    
    # runs the get_state_name method from state_machine
    def get_state_name(self):
        return "idle"

    def enter(self):
        # cancels out previous animation
        self.player.image.fill(WHITE)
        print('enter player idle state')
        keys = pg.key.get_pressed()
        # if player hits k, attack will happen
        if keys[pg.K_k]:
            print('transition to the attack state')
            self.player.state_machine.transition("attack")

# is State class imported to instantiate it here?
class PlayerMoveState(State):
    def __init__(self, player):
        self.player = player
        self.name = 'move'
    
    def get_state_name(self):
        return 'move'
    
    def enter(self):
        self.player.image.fill(RED)
        print('enter player move state')
    
    def exit(self):
        print('exit player move state')
    
    def update(self):
        self.player.image.fill(BLUE)
        keys = pg.key.get_pressed()
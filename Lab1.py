import vacuumworld
from vacuumworld.vwc import action, direction


class MyMind:

    def __init__(self):
        self.grid_size = - 1

    def decide(self):
        print(self.grid_size)
        if not self.observation.forward and (not self.observation.left or not self.observation.right):
            if (self.observation.center.coordinate.x == 0) and (self.observation.center.coordinate.y == 0):
                return action.turn(direction.right)
            elif self.observation.center.coordinate.x > self.observation.center.coordinate.y:
                self.grid_size = self.observation.center.coordinate.x + 1
            else:
                self.grid_size = self.observation.center.coordinate.y + 1
        elif not self.observation.forward:
            return action.turn(direction.right)
        elif self.observation.forward:
            return action.move()
        else:
            return action.idle()

    def revise(self, observation, messages):
        self.observation = observation
        print(self.observation)


vacuumworld.run(MyMind())

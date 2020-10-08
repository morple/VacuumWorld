# Lab 2 -
#   Create two agents of different colours e.g. a green agent and an orange
#   agent, and program them to find out about each other. For this simple
#   task, finding out about each other means knowing the unique id of the other
#   agent. Ensure your solution is valid for any possible initial positions of the
#   agents, which may include situations where the two agents do not see each
#   other. Hint: Consider the broadcasting communicative action.

import random
import vacuumworld
from vacuumworld import vwc
from vacuumworld.vwc import action, direction


class MyMind:

    def __init__(self):
        self.grid_size = 5
        self.should_say_hello = False
        self.should_send_location = False
        self.should_move = False
        self.should_turn = False
        self.should_go_to_location = False
        self.relative_direction = []
        self.location_to_go_to = [0, 0]
        self.should_reorientate = False
        self.should_avoid = False
        self.times_said_hello = 0

    def decide(self):
        print("1. Should move :", self.should_move)
        print("1. Should turn :", self.should_turn)
        if self.should_reorientate:
            print("Should be reorientating")
            return action.turn(direction.right)
       # elif self.should_go_to_location and not self.observation.forward:
         #   print("Should be avoiding wall")
        #    return action.turn(direction.right)
        elif self.should_avoid:
            self.should_avoid = False
            return action.move()
        elif self.should_go_to_location and self.observation.forward and self.observation.forward.agent:
            print("Should be avoiding agent")
            self.should_avoid = True
            return vwc.random([action.turn(direction.left), action.turn(direction.right)])
        elif self.should_move:
            print("Should be moving")
            return action.move()
        elif self.should_turn:
            print("Should be turning")
            return action.turn(direction.right)
        elif self.should_say_hello:
            return vwc.random([action.speak("Hello"), action.idle()])
        elif self.should_send_location:
            if not self.messages:
                return action.idle()
            else:
                x = random.randint(1, self.grid_size - 1)
                y = random.randint(1, self.grid_size - 1)
                location = [x, y]
                self.location_to_go_to[0], self.location_to_go_to[1] = location[0] - 1, location[1]
                if self.location_to_go_to[0] < 0:
                    self.location_to_go_to[0] += 2
                self.should_go_to_location = True
                self.relative_direction = self.get_relative_direction(self.location_to_go_to)
                return action.speak(location, self.messages[0].sender)
        else:
            return action.idle()

    def get_relative_direction(self,coords):
        self.location_to_go_to = coords
        relative_direction = ['', '']
        direction = [self.observation.center.coordinate.x - coords[0], self.observation.center.coordinate.y -
                     coords[1]]
        if direction[0] < 0:
            relative_direction[0] = self.observation.center.agent.orientation.east
        else:
            relative_direction[0] = self.observation.center.agent.orientation.west
        if direction[1] < 0:
            relative_direction[1] = self.observation.center.agent.orientation.south
        else:
            relative_direction[1] = self.observation.center.agent.orientation.north

        return relative_direction

    def revise(self, observation, messages):
        self.observation = observation
        self.messages = messages

        # checks if agent has no messages and is Agent A-1
        if not self.messages and (not self.should_go_to_location or not self.should_reorientate):
            if random.randint(1, 100) < 10:
                self.should_say_hello = True
        # Checks messages to see if another agent said hello or has sent a location to travel to
        else:
            for message in messages:
                print('Message Content:', message.content)
                if message.content == 'Hello':
                    self.times_said_hello += 1
                    if self.times_said_hello > 2:
                        self.times_said_hello = 0
                        self.should_say_hello = False
                        self.should_send_location = False
                    self.should_send_location = True
                    self.should_say_hello = False
                else:
                    self.should_say_hello = False
                    self.relative_direction = self.get_relative_direction([message.content[0], message.content[1]])
                    self.should_go_to_location = True

        if self.should_go_to_location:
            self.should_send_location = False
            if self.observation.center.coordinate.x != self.location_to_go_to[0]:
                if self.observation.center.agent.orientation != self.relative_direction[0]:
                    self.should_move = False
                    self.should_turn = True
                else:
                    self.should_turn = False
                    self.should_move = True
            elif self.observation.center.coordinate.y != self.location_to_go_to[1]:
                if self.observation.center.agent.orientation != self.relative_direction[1]:
                    self.should_move = False
                    self.should_turn = True
                else:
                    self.should_turn = False
                    self.should_move = True
            else:
                self.should_go_to_location = False
                self.should_turn = False
                self.should_move = False
                self.should_reorientate = True

            print("Should move :", self.should_move)
            print("Should turn :", self.should_turn)

        if self.should_reorientate:
            if not self.observation.forward:
                pass
            elif self.observation.forward.agent:
                self.should_reorientate = False



vacuumworld.run(MyMind())

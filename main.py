''''''
from random import randint
from math import log2

def send_none(f):
    def wrapper(*args, **kwargs):
        v = f(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class LifeSimulation:
    ''''''
    def __init__(self) -> None:
        self.hunger = 100
        self.sleep = 100
        self.tiredness = 0

        self.start = self._create_start()
        self.sleep = self._sleep()
        self.eat = self._eat()
        self.study = self._study()

        self.current_state = self.start
        self.stopped = False

    def send(self, hour):
        try:
            self.current_state.send(hour)
        except StopIteration:
            self.stopped = True

    @send_none
    def _create_start(self):
        while True:
            hour = yield
            if hour == 0:
                self.current_state = self.sleep

    @send_none
    def _sleep(self):
        while True:
            hour = yield
            if 0 <= hour < 7:
                self.current_state = self.sleep
            elif hour == 7:
                self.current_state = self.eat

    @send_none
    def _eat(self):
        while True:
            hour = yield
            self.hunger = min(self.hunger+randint(20,40), 100)
            if hour in (8,15):
                self.current_state = self.study
            if hour == 21:
                self.current_state = self.sleep

    @send_none
    def _study(self):
        while True:
            hour = yield
            self.tiredness += randint(log2(self.tiredness), 2*log2(self.tiredness))
            self.hunger -= randint(log2(self.hunger/2), 2*log2(self.hunger/2))
            if hour in (13,20):
                self.current_state = self.eat
            if hour == 23:
                self.current_state = self.sleep

def simulate_life(days: int):
    simulator = LifeSimulation()
    for day in range(days):
        print(f'DAY {day}: ')
        for hour in range(24):
            simulator.send(hour)
            print(f'HOUR: {hour}, {simulator.current_state}')

simulate_life(5)

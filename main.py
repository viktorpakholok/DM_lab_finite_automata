''''''

def send_none(f):
    def wrapper(*args, **kwargs):
        v = f(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class LifeSimulation:
    ''''''
    def __init__(self) -> None:
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
            if hour in (8,15):
                self.current_state = self.study
            if hour == 21:
                self.current_state = self.sleep

    @send_none
    def _study(self):
        while True:
            hour = yield
            if hour == 13:
                self.current_state = self.eat
            if hour == 23:
                self.current_state = self.sleep

def simulate_life(days: int):
    simulator = LifeSimulation()
    for day in range(days):
        for hour in range(24):
            simulator.send(hour)
            print(f'HOUR: {hour}, {simulator.current_state}')
        print(f'DAY {day}: ')

# simulate_life(5)

''''''
import random
from math import log2
import matplotlib.pyplot as plt

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
        self.tiredness = 0
        self.mental_health = 100
        self.success = 0
        self.states = {'sleep': 0, 'eat': 0, 'study': 0, 'exercise': 0, 'super_study': 0}

        self.start = self._create_start()
        self.sleep = self._sleep()
        self.eat = self._eat()
        self.study = self._study()
        self.exercise = self._exercise()
        self.super_study = self._super_study()

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
            self.states['sleep'] += 1
            self.tiredness = max(self.tiredness-random.randint(15, 20), 0)
            self.mental_health = min(100, self.mental_health + random.randint(10,15))
            if hour == 7:
                self.current_state = self.eat
            elif random.random() >= self.tiredness/100 + 0.7:
                self.current_state = self.study

    @send_none
    def _eat(self):
        while True:
            hour = yield
            self.states['eat'] += 1
            self.hunger = min(self.hunger+random.randint(40,50), 100)
            self.mental_health = min(100, self.mental_health + random.randint(20,30))
            self.tiredness = max(0, self.tiredness - random.randint(5,10))
            rand = random.random()
            if hour >= 23 and rand >= 0.2:
                self.current_state = self.sleep
            elif rand >= 0.8*(self.hunger+20)/80:
                self.current_state = self.eat
            elif rand >= 0.5:
                self.current_state = self.exercise
            elif hour == 22:
                self.current_state = self.sleep
                self.success = 0
            else:
                self.current_state = self.study
    @send_none
    def _study(self):
        while True:
            hour = yield
            self.states['study'] += 1
            self.tiredness = min(self.tiredness+random.randint(10, 15), 100)
            self.mental_health = max(0, self.mental_health - random.randint(10,15))
            self.success += random.randint(int(10-self.tiredness/10+self.mental_health/10), int(20-self.tiredness/10+self.mental_health/10))
            # print(f'random: {int((self.hunger/2)**(1/1.5)), int(self.hunger**(1/1.5))}')
            self.hunger = max(0, self.hunger-random.randint(7,15))
            if hour in (7,13,20):
                self.current_state = self.eat
            elif hour == 23:
                self.current_state = self.sleep
                self.success = 0

    @send_none
    def _exercise(self):
        while True:
            hour = yield
            self.states['exercise'] += 1
            self.tiredness = min(100, self.tiredness+random.randint(5,10))
            self.hunger = max(0, self.hunger-random.randint(7,12))
            self.mental_health = min(100, self.mental_health+random.randint(20,30))
            if 8 <= hour <= 20 and random.random() >= 0.8:
                self.current_state = self.super_study
            elif 8 <= hour <= 22:
                self.current_state = self.study
            elif hour >= 23:
                self.current_state = self.sleep
                self.success = 0

    @send_none
    def _super_study(self):
        while True:
            hour = yield
            self.states['super_study'] += 1
            self.tiredness = min(100, self.tiredness+random.randint(20,30))
            self.hunger = max(0, self.hunger-random.randint(15,20))
            self.mental_health = max(0, self.mental_health-random.randint(15,20))
            if hour >= 23 or hour <= 6:
                self.current_state = self.sleep
                self.success = 0
            elif random.random() <= self.tiredness/80:
                self.current_state = self.study

    @property
    def overall(self):
        return (self.hunger - self.tiredness + self.mental_health + self.success)/4

def simulate_life(days: int):
    hours, hunger_levels, tiredness_levels, mental_levels, success_levels, overall_levels = [], [], [], [], [], []
    simulator = LifeSimulation()

    for day in range(days):
        print(f'DAY {day}: ')
        for hour in range(24):
            hours.append(hour + day * 24)
            hunger_levels.append(simulator.hunger)
            tiredness_levels.append(simulator.tiredness)
            mental_levels.append(simulator.mental_health)
            success_levels.append(simulator.success)
            overall_levels.append(simulator.overall)
            simulator.send(hour)
            print(f'HOUR: {hour}, {simulator.current_state}')

        # hours.append(day)
        # hunger_levels.append(simulator.hunger)
        # tiredness_levels.append(simulator.tiredness)
        # sleep_levels.append(simulator.sleep_l)
        # mental_levels.append(simulator.mental_health)
        # success_levels.append(simulator.success)

    return hours, hunger_levels, tiredness_levels, mental_levels, success_levels, overall_levels, {key: val/days for key, val in simulator.states.items()}

# simulate_life(5)

def plot_simulation(days: int):
    res = simulate_life(days)
    # print(res)

    fig, axs = plt.subplots(3, 2, figsize=(20, 12))

    # print(axs)

    axs[0][0].plot(res[0], res[1], label='Hunger', color = 'red')
    axs[0][0].set_xlabel('Hour')
    axs[0][0].set_ylabel('Hunger Level')
    axs[0][0].set_title('Hunger Level Over Time')
    axs[0][0].legend()
    axs[0][0].grid(True)

    axs[0][1].plot(res[0], res[2], label='Tiredness', color = 'blue')
    axs[0][1].set_xlabel('Hour')
    axs[0][1].set_ylabel('Tiredness Level')
    axs[0][1].set_title('Tiredness Level Over Time')
    axs[0][1].legend()
    axs[0][1].grid(True)

    axs[1][0].plot(res[0], res[3], label='Mental health', color = 'indigo')
    axs[1][0].set_xlabel('Hour')
    axs[1][0].set_ylabel('Mental health Level')
    axs[1][0].set_title('Mental health Level Over Time')
    axs[1][0].legend()
    axs[1][0].grid(True)

    axs[1][1].plot(res[0], res[4], label='Success', color = 'green')
    axs[1][1].set_xlabel('Hour')
    axs[1][1].set_ylabel('Success Level')
    axs[1][1].set_title('Success Level Over Time')
    axs[1][1].legend()
    axs[1][1].grid(True)

    axs[2][0].plot(res[0], res[5], label='Overall', color = 'olive')
    axs[2][0].set_xlabel('Hour')
    axs[2][0].set_ylabel('Overall Level')
    axs[2][0].set_title('Overall Level Over Time')
    axs[2][0].legend()
    axs[2][0].grid(True)

    axs[2][1].bar(res[6].keys(), res[6].values(), label='States', color = ['tab:red', 'tab:orange', 'tab:cyan', 'lime', 'blueviolet'])
    axs[2][1].set_xlabel('State')
    axs[2][1].set_ylabel('States Level')
    axs[2][1].set_title('States Level Over Time')
    # axs[2][1].legend()
    # axs[2][1].grid(True)

    plt.tight_layout()
    plt.show()

plot_simulation(10)

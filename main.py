'''The fourth laboratory on discrete mathematics about finite automata'''

import random
import matplotlib.pyplot as plt

def send_none(func):
    '''A decorator function that sends a None value to a coroutine's first yield point'''
    def wrapper(*args, **kwargs):
        var = func(*args, **kwargs)
        var.send(None)
        return var
    return wrapper

class LifeSimulation:
    '''
    A class representing a life simulation with hunger, tiredness, mental health, and success levels
    '''
    def __init__(self) -> None:
        self.hunger = 100
        self.tiredness = 100
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
        '''Sends the hour to the current state coroutine'''
        try:
            self.current_state.send(hour)
        except StopIteration:
            self.stopped = True

    @send_none
    def _create_start(self):
        """Coroutine representing the starting state of the simulation"""
        while True:
            hour = yield
            if hour == 0:
                self.current_state = self.sleep

    @send_none
    def _sleep(self):
        """Coroutine representing the sleep state of the simulation"""
        while True:
            hour = yield
            self.states['sleep'] += 1
            self.tiredness = max(self.tiredness-random.randint(15, 20), 0)
            self.mental_health = min(100, self.mental_health + random.randint(10,15))
            if hour == 1:
                self.success = 0
            if hour == 7 and random.random() >= 0.4:
                self.current_state = self.eat
            elif random.random() >= self.tiredness/100 + 0.7:
                print("I don't have time to eat, I have to study")
                self.current_state = self.study

    @send_none
    def _eat(self):
        """Coroutine representing the eat state of the simulation"""
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
                print("It's never a bad idea to eat one more time")
                self.current_state = self.eat
            elif rand >= 0.5:
                print('What a nice weather to move a little bit')
                self.current_state = self.exercise
            else:
                self.current_state = self.study
    @send_none
    def _study(self):
        """Coroutine representing the study state of the simulation"""
        while True:
            hour = yield
            self.states['study'] += 1
            self.tiredness = min(self.tiredness+random.randint(10, 15), 100)
            self.mental_health = max(0, self.mental_health - random.randint(10,15))
            self.success += random.randint(int(10-self.tiredness/10+self.mental_health/10), \
int(20-self.tiredness/10+self.mental_health/10))
            self.hunger = max(0, self.hunger-random.randint(7,15))
            if hour in (7,13,20):
                self.current_state = self.eat
            elif hour == 23:
                self.current_state = self.sleep

    @send_none
    def _exercise(self):
        """Coroutine representing the exercise state of the simulation"""
        while True:
            hour = yield
            self.states['exercise'] += 1
            self.tiredness = min(100, self.tiredness+random.randint(5,10))
            self.hunger = max(0, self.hunger-random.randint(7,12))
            self.mental_health = min(100, self.mental_health+random.randint(20,30))
            if 8 <= hour <= 20 and random.random() >= 0.8:
                print('I feel my powers')
                self.current_state = self.super_study
            elif 8 <= hour <= 22:
                self.current_state = self.study
            elif hour >= 23:
                self.current_state = self.sleep

    @send_none
    def _super_study(self):
        """Coroutine representing the super_study state of the simulation"""
        while True:
            hour = yield
            self.states['super_study'] += 1
            self.tiredness = min(100, self.tiredness+random.randint(20,30))
            self.hunger = max(0, self.hunger-random.randint(15,20))
            self.mental_health = max(0, self.mental_health-random.randint(15,20))
            if hour >= 23 or hour <= 6:
                self.current_state = self.sleep
            elif random.random() <= self.tiredness/80:
                print("I am to tired to continue to study like that")
                self.current_state = self.study

    @property
    def overall(self):
        """
        Calculates the overall well-being based on hunger, tiredness, mental health, and success 
        levels
        """
        return (self.hunger - self.tiredness + self.mental_health + self.success)/4

def simulate_life(days: int):
    """Simulates life for the specified number of days"""
    levels = ([], [], [], [], [], [])
    simulator = LifeSimulation()

    for day in range(days):
        print(f'DAY {day}: ')
        temp = ([], [], [], [], [], [])
        for hour in range(24):
            temp[0].append(hour + day * 24)
            temp[1].append(simulator.hunger)
            temp[2].append(simulator.tiredness)
            temp[3].append(simulator.mental_health)
            temp[4].append(simulator.success)
            temp[5].append(simulator.overall)
            simulator.send(hour)
            print(f'HOUR: {hour}, CUR_STATE: \
{str(simulator.current_state).split('._')[1].split(' ', maxsplit=1)[0]}')

        if days <= 25:
            for ind, tem in enumerate(temp):
                levels[ind].extend(tem)
        else:
            for ind, tem in enumerate(temp):
                if ind == 0:
                    levels[0].append(day)
                else:
                    levels[ind].append(sum(tem)/len(tem))

    return levels, {key: val/days for key, val in simulator.states.items()}

def plot_simulation(days: int):
    """Plots the simulation results for the specified number of days"""
    res = simulate_life(days)

    axs = plt.subplots(3, 2, figsize=(20, 12))[1]

    axs[0][0].plot(res[0][0], res[0][1], label='Hunger', color = 'red')
    axs[0][0].set_xlabel('Hour' if days <= 25 else 'Day')
    axs[0][0].set_ylabel('Hunger Level')
    axs[0][0].set_title('Hunger Level Over Time')
    axs[0][0].legend()
    axs[0][0].grid(True)

    axs[0][1].plot(res[0][0], res[0][2], label='Tiredness', color = 'blue')
    axs[0][1].set_xlabel('Hour' if days <= 25 else 'Day')
    axs[0][1].set_ylabel('Tiredness Level')
    axs[0][1].set_title('Tiredness Level Over Time')
    axs[0][1].legend()
    axs[0][1].grid(True)

    axs[1][0].plot(res[0][0], res[0][3], label='Mental health', color = 'indigo')
    axs[1][0].set_xlabel('Hour' if days <= 25 else 'Day')
    axs[1][0].set_ylabel('Mental health Level')
    axs[1][0].set_title('Mental health Level Over Time')
    axs[1][0].legend()
    axs[1][0].grid(True)

    axs[1][1].plot(res[0][0], res[0][4], label='Success', color = 'green')
    axs[1][1].set_xlabel('Hour' if days <= 25 else 'Day')
    axs[1][1].set_ylabel('Success Level')
    axs[1][1].set_title('Success Level Over Time')
    axs[1][1].legend()
    axs[1][1].grid(True)

    axs[2][0].plot(res[0][0], res[0][5], label='Overall', color = 'olive')
    axs[2][0].set_xlabel('Hour' if days <= 25 else 'Day')
    axs[2][0].set_ylabel('Overall Level')
    axs[2][0].set_title('Overall Level Over Time')
    axs[2][0].legend()
    axs[2][0].grid(True)

    axs[2][1].bar(res[1].keys(), res[1].values(), label='States', color = \
['tab:red', 'tab:orange', 'tab:cyan', 'lime', 'blueviolet'])
    axs[2][1].set_xlabel('State')
    axs[2][1].set_ylabel('States Level')
    axs[2][1].set_title('States Level Over Time')
    # axs[2][1].legend()
    # axs[2][1].grid(True)

    plt.tight_layout()
    plt.show()

plot_simulation(10)#Change amount of days here

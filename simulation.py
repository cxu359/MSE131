import random
import math

SIMULATION_LENGTH = 365
BURGER = 1
BURGER_AND_ICE_CREAM = 2
BURGER_PRICE = 10
BURGER_COST = 2
ICE_CREAM_PRICE = 2
ICE_CREAM_COST = 0.10
MACHINE_BROKEN_CHANCE = 0.1
DAY = 900
EMPLOYEE_WAGE = 17.60



# burger shop

'''
Assumptions

Burger: price $10, cost $2, profit $8
Ice cream: price $2, cost $0.10, profit $1.90
50/50 chance of customer ordering burger or burger and ice cream, nobody orders only ice cream
10% of days the ice cream machine is broken and everybody orders only burgers
Day goes from 7:00 - 22:00, rush hours 7:00 - 10:00, 12:00 - 14:00, 18:00 - 20:00, double customer rate

Baseline values:
3 minute average burger service
1 minute average ice cream service
0.5 minutes average cashier
3 cashiers, 5 kitchen staff, each staff can take/prepare 1 order at a time
2 customers/minute usually, 4 customers/minute rush hours
M/M/1 model

'''

'''
1.  customer -> line -> cashier -> table
    food -> kitchen staff -> table

    measure average wait time and profit per day

2.  burger / ice cream
    rush hours between 7:00 - 10:00, 12:00 - 14:00, 18:00 - 20:00
    ice cream machine broken 10% of the times
    worker lunch breaks
    seating

3.  single vs separate lines
    different worker distribution
    different number of workers

    arrival rates
    service times
    
'''

class Customer:
    def __init__(self, service_time, cashier_time, start_time):
        self.time_in_system = 0
        self.service_time = service_time
        self.cashier_time = cashier_time
        self.start_time = start_time

    def add_time_in_system(self, time):
        self.time_in_system += time
    
    def subtract_cashier_time(self, time):
        self.cashier_time -= time

def did_machine_break():
    num = random.random()
    if num < MACHINE_BROKEN_CHANCE:
        return True
    return False

def get_customer_order(is_machine_broken):
    if is_machine_broken:
        return BURGER
    return random.choice([BURGER, BURGER_AND_ICE_CREAM])

def get_arrival_time(lam):
    return random.expovariate(lam)

def get_service_time(lam):
    return random.expovariate(lam)

def is_rush_hour(time):
    rush_hours1 = (0, 180)
    rush_hours2 = (300, 420)
    rush_hours3 = (660, 780)

    if rush_hours1[0] <= time <= rush_hours1[1]:
        return True
    if rush_hours2[0] <= time <= rush_hours2[1]:
        return True
    if rush_hours3[0] <= time <= rush_hours3[1]:
        return True
    return False

def build_queue(arrival_lam, service_lam, cashier_lam):
    queue = []
    time = 0
    while time < DAY:
        rush_hour = is_rush_hour(time)
        if rush_hour:
            time += get_arrival_time(2 * arrival_lam)
        else:
            time += get_arrival_time(arrival_lam)

        queue.append(Customer(get_service_time(service_lam), get_service_time(cashier_lam), time))
    
    return queue

def one_day_simulation(arrival_lam, service_lam, cashier_lam, num_cashiers):
    order_queue = build_queue(arrival_lam, service_lam, cashier_lam)
    service_queue = []
    cashiers = [None for i in range(num_cashiers)] 
    time = 0

    while len(order_queue) > 0 or cashiers != [None] * len(cashiers):
        for i in range(len(cashiers)):
            if len(order_queue) > 0:
                if cashiers[i] == None and time >= order_queue[0].start_time:
                    cashiers[i] = order_queue.pop(0)
        
        if cashiers == [None] * len(cashiers):
            time += order_queue[0].start_time - time

        cashier_times = []
        for i in range(len(cashiers)):
            if cashiers[i]:
                cashier_times.append(cashiers[i].cashier_time)
        time += min(cashier_times, default=0)
        
        for i in range(len(cashiers)):
            if cashiers[i]:
                cashiers[i].subtract_cashier_time(min(cashier_times))

        for i in range(len(cashiers)):
            if cashiers[i]:
                if math.isclose(cashiers[i].cashier_time, 0, abs_tol=1e-9):
                    cashiers[i].time_in_system = time - cashiers[i].start_time
                    service_queue.append(cashiers[i])
                    cashiers[i] = None

    return service_queue

def main():
    queue = one_day_simulation(2, 3, 2, 3)
    avg = 0
    for i in range(len(queue)):
        print(f"Customer {i}: {queue[i].service_time} {queue[i].cashier_time} {queue[i].start_time}")
        avg += queue[i].time_in_system
    avg = avg/len(queue)
    print(avg)

if __name__ == "__main__":
    main()
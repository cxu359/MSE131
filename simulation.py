import random

SIMULATION_LENGTH = 365
BURGER = 1
BURGER_AND_ICE_CREAM = 2
BURGER_PRICE = 10
BURGER_COST = 2
ICE_CREAM_PRICE = 2
ICE_CREAM_COST = 0.10
MACHINE_BROKEN_CHANCE = 0.10



# burger shop

'''
Assumptions

Burger: price $10, cost $2, profit $8
Ice cream: price $2, cost $0.10, profit $1.90
50/50 chance of customer ordering burger or burger and ice cream, nobody orders only ice cream
10% of days the ice cream machine is broken and everybody orders only burgers
Day goes from 7:00 - 22:00, rush hours 7:00 - 10:00, 12:00 - 14:00, 18:00 - 20:00

Baseline values:
3 minute average burger service
1 minute average ice cream service
0.5 minutes average cashier
3 cashiers, 5 kitchen staff, each staff can take/prepare 1 order at a time
2 customers/minute usually, 5 customers/minute
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
    def __init__(self):
        self.time = 0

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

def main():
    pass

if __name__ == "__main__":
    main()
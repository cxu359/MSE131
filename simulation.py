import random

SIMULATION_LENGTH = 365
BURGER = 0
BURGER_AND_ICE_CREAM = 1
BURGER_PRICE = 10
BURGER_COST = 2
ICE_CREAM_PRICE = 2
ICE_CREAM_COST = 0.10
MACHINE_BROKEN_CHANCE = 0.1
DAY = 900
EMPLOYEE_WAGE = 17.60
WINTER_DEMAND = 1
SPRING_DEMAND = 1.1
FALL_DEMAND = 1.2
SUMMER_DEMAND = 1.3
SPRING_START = 79
SUMMER_START = 171
FALL_START = 265
WINTER_START = 355
MINIMUM_WAGE = 17.60

# class to store variables related to each customer
class Customer:
    def __init__(self, cashier_time, start_time, order, cook_time):
        self.time_in_system = 0
        self.cashier_time = cashier_time
        self.start_time = start_time
        self.order = order
        self.food_start_time = 0
        self.cook_time = cook_time

    def add_time_in_system(self, time):
        self.time_in_system += time
    
    def subtract_cashier_time(self, time):
        self.cashier_time -= time

    def subtract_cook_time(self, time):
        self.cook_time -= time

# generates number between 0 and 1, if its less than 0.1 then the machine is broken for the day
def did_machine_break():
    num = random.random()
    if num < MACHINE_BROKEN_CHANCE:
        return True
    return False

# 50/50 order burger or burger and ice cream
def get_customer_order(is_machine_broken):
    if is_machine_broken:
        return BURGER
    return random.choice([BURGER, BURGER_AND_ICE_CREAM])

# exponential distribution for arrival time
def get_arrival_time(lam):
    return random.expovariate(lam)

# exponential distribution for cashier service time
def get_service_time(lam):
    return random.expovariate(lam)

# exponential distribution for total service time
def get_order_time(burger_lam, ice_cream_lam, order):
    return random.expovariate(burger_lam) + order * random.expovariate(ice_cream_lam)

# checks if the current time is during rush hours
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

# makes M/M/s queue for a day
def build_mms_queue(arrival_lam, cashier_lam, burger_lam, ice_cream_lam, is_machine_broken):
    queue = []
    time = 0

    while time < DAY:
        rush_hour = is_rush_hour(time)
        if rush_hour:
            time += get_arrival_time(2 * arrival_lam)
        else:
            time += get_arrival_time(arrival_lam)

        order = get_customer_order(is_machine_broken)
        queue.append(Customer(get_service_time(cashier_lam), time, order, get_order_time(burger_lam, ice_cream_lam, order)))
    
    return queue

# simulates one day for M/M/s
def mms_one_day_simulation(arrival_lam, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken):
    order_queue = build_mms_queue(arrival_lam, cashier_lam, burger_lam, ice_cream_lam, is_machine_broken)
    food_queue = []
    cashiers = [None for i in range(num_cashiers)] 
    cooks = [None for i in range(num_cooks)]
    output = []
    time = 0

    while len(order_queue) > 0 or cashiers != [None] * len(cashiers):
        # if there is a customer in line and an available cashier then the customer goes to the cashier
        for i in range(len(cashiers)):
            if len(order_queue) > 0:
                if cashiers[i] == None and time >= order_queue[0].start_time:
                    cashiers[i] = order_queue.pop(0)
        
        # advance time if there's no cashiers busy to avoid infinite loops
        if cashiers == [None] * len(cashiers):
            time += order_queue[0].start_time - time

        # advance time to make the next cashier available
        cashier_times = []
        for i in range(len(cashiers)):
            if cashiers[i]:
                cashier_times.append(cashiers[i].cashier_time)
        time += min(cashier_times, default=0)
        
        for i in range(len(cashiers)):
            if cashiers[i]:
                cashiers[i].subtract_cashier_time(min(cashier_times))

        # if a customer is done with the cashier they get moved to food queue and cashier becomes available
        for i in range(len(cashiers)):
            if cashiers[i]:
                if cashiers[i].cashier_time < 1e-9:
                    cashiers[i].food_start_time = time
                    cashiers[i].time_in_system = time - cashiers[i].start_time
                    food_queue.append(cashiers[i])
                    cashiers[i] = None

    time = 0
    while len(food_queue) > 0 or cooks != [None] * len(cooks):
        # if there is an order present and a cook available then they make the order
        for i in range(len(cooks)):
            if len(food_queue) > 0:
                if cooks[i] == None and time >= food_queue[0].food_start_time:
                    cooks[i] = food_queue.pop(0)

        # advance time if there's no cook busy to avoid infinite loops
        if cooks == [None] * len(cooks):
            time += food_queue[0].food_start_time - time

        # advance time to make the next cook available
        cook_times = []
        for i in range(len(cooks)):
            if cooks[i]:
                cook_times.append(cooks[i].cook_time)
        time += min(cook_times, default=0)

        for i in range(len(cooks)):
            if cooks[i]:
                cooks[i].subtract_cook_time(min(cook_times))

        # if a cook is done making an order they get moved to output queue so customer information can be accessed
        # and cook becomes available
        for i in range(len(cooks)):
            if cooks[i]:
                if cooks[i].cook_time < 1e-9:
                    cooks[i].time_in_system += time - cooks[i].food_start_time
                    output.append(cooks[i])
                    cooks[i] = None

    return output

# creates s M/M/1 queue for a day
def build_mm1_queue(arrival_lam, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, is_machine_broken):
    queues = [[] for i in range(num_cashiers)]
    time = 0

    while time < DAY:
        rush_hour = is_rush_hour(time)
        if rush_hour:
            time += get_arrival_time(2 * arrival_lam)
        else:
            time += get_arrival_time(arrival_lam)

        order = get_customer_order(is_machine_broken)
        queues[random.randint(0, num_cashiers - 1)].append(Customer(get_service_time(cashier_lam), time, order, get_order_time(burger_lam, ice_cream_lam, order)))

    return queues

# simulates s M/M/1 queus for a day
def s_mm1_one_day_simulation(arrival_lam, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken):
    order_queues = build_mm1_queue(arrival_lam, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, is_machine_broken)
    food_queue = []
    cashier = None
    cooks = [None for i in range(num_cooks)]
    output = []

    for queue in order_queues:
        time = 0
        while len(queue) > 0:
            # take next customer order if there is one
            if time >= queue[0].start_time:
                cashier = queue.pop(0)

                time += cashier.cashier_time

                cashier.time_in_system = time - cashier.start_time
                cashier.food_start_time = time
                food_queue.append(cashier)
                cashier = None
            
            # advance time if nobody is in line
            else:
                time = queue[0].start_time

    # sort food queue by times they join the queue
    food_queue = sorted(food_queue, key=lambda c: c.food_start_time)

    time = 0
    while len(food_queue) > 0 or cooks != [None] * len(cooks):
        # if there is an order present and a cook available then they make the order
        for i in range(len(cooks)):
            if len(food_queue) > 0:
                if cooks[i] == None and time >= food_queue[0].food_start_time:
                    cooks[i] = food_queue.pop(0)

        # advance time if there's no cook busy to avoid infinite loops
        if cooks == [None] * len(cooks):
            time += food_queue[0].food_start_time - time

        # advance time to make the next cook available
        cook_times = []
        for i in range(len(cooks)):
            if cooks[i]:
                cook_times.append(cooks[i].cook_time)
        time += min(cook_times, default=0)

        for i in range(len(cooks)):
            if cooks[i]:
                cooks[i].subtract_cook_time(min(cook_times))

        # if a cook is done making an order they get moved to output queue so customer information can be accessed and cook becomes available
        for i in range(len(cooks)):
            if cooks[i]:
                if cooks[i].cook_time < 1e-9:
                    cooks[i].time_in_system += time - cooks[i].food_start_time
                    output.append(cooks[i])
                    cooks[i] = None

    return output

# gets average time in system (used for a day)
def compute_average_time(queue):
    total = 0
    for i in range(len(queue)):
        total += queue[i].time_in_system
    avg = total/len(queue)
    return avg

# gets profit (used for a day)
def compute_profit(queue, num_employees):
    profit = 0
    for i in range(len(queue)):
        if queue[i].order == BURGER:
            profit += (BURGER_PRICE - BURGER_COST)
        else:
            profit += (BURGER_PRICE - BURGER_COST) + (ICE_CREAM_PRICE - ICE_CREAM_COST)

    profit -= num_employees * DAY/60 * MINIMUM_WAGE

    return profit

# gets average of the average time(used for a year)
def compute_average_of_averages(averages):
    total = 0
    for i in range(len(averages)):
        total += averages[i]
    avg = total/len(averages)
    return avg

def main():
    mm1 = int(input("Press 0 for M/M/s. Press 1 for s M/M/1.\n"))

    arrival_lam = float(input("Enter the average arrival rate in customers/minute.\n"))
    cashier_time = float(input("Enter the average time a customer interacts with the cashier in minutes.\n"))
    cashier_lam = 1/cashier_time
    burger_time = float(input("Enter the average time a burger takes to make.\n"))
    burger_lam = 1/burger_time
    ice_cream_time = float(input("Enter the average time ice cream takes to make.\n"))
    ice_cream_lam = 1/ice_cream_time
    num_cashiers = int(input("Enter the number of cashiers.\n"))
    num_cooks = int(input("Enter the number of kitchen staff.\n"))

    if mm1:
        queues = []
        for i in range(365):
            if SPRING_START <= i < SUMMER_START:
                queues.append(s_mm1_one_day_simulation(arrival_lam*SPRING_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))
        
            elif SUMMER_START <= i < FALL_START:
                queues.append(s_mm1_one_day_simulation(arrival_lam*SUMMER_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))

            elif FALL_START <= i < WINTER_START:
                queues.append(s_mm1_one_day_simulation(arrival_lam*FALL_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))

            else:
                queues.append(s_mm1_one_day_simulation(arrival_lam*WINTER_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))

        queues_time = compute_average_of_averages([compute_average_time(queues[i]) for i in range(365)])
        queues_profit = sum([compute_profit(queues[i], 20) for i in range(365)])

        print(f"Average time customer spends in system: {queues_time} minutes, profit over year: ${queues_profit}")
        print()

    else:
        queues = []
        for i in range(365):
            if SPRING_START <= i < SUMMER_START:
                queues.append(mms_one_day_simulation(arrival_lam*SPRING_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))
        
            elif SUMMER_START <= i < FALL_START:
                queues.append(mms_one_day_simulation(arrival_lam*SUMMER_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))

            elif FALL_START <= i < WINTER_START:
                queues.append(mms_one_day_simulation(arrival_lam*FALL_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))

            else:
                queues.append(mms_one_day_simulation(arrival_lam*WINTER_DEMAND, cashier_lam, burger_lam, ice_cream_lam, num_cashiers, num_cooks, is_machine_broken=did_machine_break()))

        queues_time = compute_average_of_averages([compute_average_time(queues[i]) for i in range(365)])
        queues_profit = sum([compute_profit(queues[i], 20) for i in range(365)])

        print(f"Average time customer spends in system: {queues_time} minutes, profit over year: ${queues_profit}")
        print()

if __name__ == "__main__":
    main()
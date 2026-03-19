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
def main():
    pass

if __name__ == "__main__":
    main()
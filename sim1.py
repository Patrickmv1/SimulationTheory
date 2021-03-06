"""
Checkout Simulation

"""
import sys
import Simulation

"""
seed
duration
lanes
customer arrival time
customer service rate

ex. sim1 789 1000 5 4 3
"""


def main():
    read_args()
    sim = Simulation.Simulation()
    sim.start()


def read_args():
    if len(sys.argv) != 6:
        print("Usage: sim1.py [seed] [duration] [lanes] [customer arrival time] [customer service rate]\n"
              "Ex. sim1 789 1000 5 4 3")
        sys.exit(-1)


if __name__ == '__main__':
    main()

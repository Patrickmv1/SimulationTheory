"""
Simulation.py
"""
import sys
import random
import CheckoutLane
import Customer
import SimEvent
import Statistics
import numpy as np


class Simulation:

    def __init__(self):
        self.logfile = open('logfile.txt', 'a+')
        self.stats = Statistics.Statistics()
        self.rand_seed = sys.argv[1]
        self.sim_duration_minutes = sys.argv[2]
        self.num_checkout_lanes = sys.argv[3]
        self.customer_arrival_rate = sys.argv[4]
        self.customer_service_rate = sys.argv[5]
        self.checkout_lanes = list()
        # self.current_customer = Customer.Customer()
        # self.current_lane = CheckoutLane.CheckoutLane()

    def start(self):
        """
        begin the simulation
        :return: none
        """
        # TODO SETUP
        # Time used for checking when customers are added to system and when they need to be removed
        stop = self.sim_duration_minutes
        sim_time = 0.0
        self.create_lanes(self)
        seed = str(self.rand_seed)
        customer_number = 1
        # Length of seed for random number generation
        N = len(seed)
        # Random number used for uniform transformation
        R = self.generateR(N)
        # Service time of customer
        time_service = self.uniTransform(R, self.customer_service_rate, N)
        # Current customer to add to queue
        current_customer = Customer.Customer(0.0, time_service, customer_number)
        # Current lane for adding customers to
        current_lane_nr = self.checkout_lanes[0]
        # Add initial customer to Queue at time 0.0
        SimEvent.SimEvent(0, current_lane_nr, current_customer)
        Customer.Customer.log_in(self)
        # Run simulation for specified duration
        while self.sim_duration_minutes != 0:
            if sim_time >= stop:
                break
            # Add customers to lane in one-time step per the customer arrival rate
            # Create a customer and add them to a lane
            customer_number += 1
            R = self.generateR(N)
            # Perform uniform transformation for customer and add it to current sim_time to accurately detail when
            # it's added to the system
            sim_time += self.uniTransform(R, self.customer_arrival_rate, N)
            R = self.generateR(N)
            time_service = self.uniTransform(R, self.customer_service_rate, N)
            current_customer = Customer.Customer(sim_time, time_service, customer_number)
            current_lane_nr = Customer.Customer.set_lane_nr()
            SimEvent.SimEvent(0, self.checkout_lanes[current_lane_nr], current_customer)
            Customer.Customer.log_in(self)
            # Check if a customer is ready to be checked out
            for i in range(self.checkout_lanes):
                if self.checkout_lanes[i].checkout_lanes[0].time_ <= sim_time:
                    SimEvent.SimEvent(1, current_lane_nr, current_customer)
                    Customer.Customer.log_out(self, sim_time)
            self.sim_duration_minutes -= 1
        pass

    # Creates lanes based off of the amount of lanes given on the command line
    def create_lanes(self):
        for i in range(self.num_checkout_lanes):
            list.append(CheckoutLane.CheckoutLane(i))

    # Uniform transformation function for interarrival times
    def uniTransform(R, lam, N):
        customerDist = round((-np.log(1 - R) * lam), N)
        # customerDist = round((-(1/lam)* np.log(1-R)), N)
        return customerDist

    # Random number generator
    def generateR(N):
        R = round(random.uniform(0, 1), N)
        return R

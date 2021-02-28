#!/usr/bin/python
# -*- coding: latin-1 -*-

from heapq import *
import time

#STATE
class State:
    def __init__(self):
        self.green = False
        self.yellow = False
        self.cars = 0

    def g_green(self):

        return self.green

    def y_yellow(self):

        return self.yellow
    def cars_wait(self):
        #Car Waiting
        self.cars = 0

    def adding_car(self):
        #Adding the car in the queue
        self.cars = self.cars + 1

    def waiting_cars(self):
        return self.cars

    def turn_green_on(self):
        self.green = True

    def turn_yellow_on(self):
        self.green = False
        self.yellow = True

    def turn_red_on(self):
        self.yellow = False
        self.green = False

    def __str__(self):
    #This displays the crossroads status
        return "Green light =" + str(self.green) + ", cars=" + str(self.cars)

#EVENTS

timeG = 180
timeY = 5
timeR = 55

endTime = 1000


class Event:
    def time(self):
        #This function will the time event will be processed

        return self.t

    def __str__(self):
        #This function Displays Event

        return self.name + "(" + str(self.t) + ")"

    def __lt__(self, other):
        #Comparing the event with another sorted by processing order priority

        return self.t < other.t


class CAR(Event):
    def __init__(self, time):
        self.t = time
        self.name = "CAR"

    def action(self, queue, state):
        if (state.waiting_cars() == 0):
            if(state.g_green() == True):

                queue.clear(state)
                queue.insert(G2Y(self.t))

        state.adding_car()

class G2Y(Event):
    def __init__(self, time):
        self.t = time
        self.name = "G2Y"

    def action(self, queue, state):
        #queue.clear(state)
        state.turn_yellow_on()
        queue.insert(Y2R(self.t + timeY))

class Y2R(Event):
    def __init__(self, time):
        self.t = time
        self.name = "Y2R"

    def action(self, queue, state):
        state.turn_red_on()
        state.cars_wait()
        queue.insert(R2G(self.t + timeR))

class R2G(Event):
    def __init__(self, time):
        self.t = time
        self.name = "R2G"

    def action(self, queue, state):
        state.turn_green_on()
        queue.insert(G2Y(self.t + timeG))

#QUEUE EVENT

class EventQueue:
    def __init__(self):
        self.q = []
        self.q_temp = []

    def notEmpty(self):
        return len(self.q) > 0

    def remaining(self):
        return len(self.q)

    def insert(self, event):
        heappush(self.q, event)

    def next(self):
        #removes from the queue to process next event

        return heappop(self.q)

    def clear(self, state):
        while(len(self.q) > 0):
            e = heappop(self.q)
            if e.name == "CAR":
                heappush(self.q_temp,e)
                e_time = e.t
                #if state.g_green == True:
                heappush(self.q_temp,G2Y(e_time))
        self.q = self.q_temp

#MAIN

Q = EventQueue()

Q.insert(R2G(0))
Q.insert(CAR(30))
Q.insert(CAR(60))
Q.insert(CAR(90))


S = State()

#Processing events till the queue Q is empty
while Q.notEmpty():
    e = Q.next()
    print("The Current event that occurs is: " + e.name + " at time: " + str(e.t))
    e.action(Q, S)
    if S.g_green():
        print("Main light State is Green")
    if not S.g_green():
        if S.y_yellow():
            print("Main light State is Yellow")
        else:
            print("Main light State is Red")
    print("............................................")
    time.sleep(.2)

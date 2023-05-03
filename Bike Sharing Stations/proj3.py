import numpy as np
import pandas as pd
import scipy.stats as st

#This is a bike station. It keeps track of the number of bikes there and the rider queue.
class BikeStation:
    def __init__(self):
        self.bikeCount = 10
        self.riderQueue = 0

    #Returns a bike to a station once its ride is finished.
    def returnBike(self):
        self.bikeCount = self.bikeCount + 1
    
    #A biker joins the queue (default bc next step will be use bike and decrease queue)
    def riderJoins(self):
        self.riderQueue = self.riderQueue + 1

    #A biker uses a bike if one is available. The bike gets a destination and time to destination.
    def useBike(self, stationIndex, bikesInTransit, currTime):
        if (self.bikeCount > 0 and self.riderQueue > 0):
            self.bikeCount = self.bikeCount - 1
            self.riderQueue = self.riderQueue - 1
            bikesInTransit.append(BikeRide(chooseDestination(destProb[stationIndex]), currTime))

#This is a bike ride of a certain time length and a destination.
class BikeRide:
    def __init__(self, destIndex, currTime):
        self.returnTime = currTime + round(np.random.lognormal(mean=2.78, sigma=0.619), 2)
        self.destIndex = destIndex

############################################################################################

#This method chooses the starting station for a rider.
#probs should be the array of probs that relate to initial choosing
def chooseStation(probs):
   index = np.random.choice([i for i in range(81)], p=probs)
   return index

#This method chooses the destination station for a rider.
#probs should be the array COLUMN of the 2D array that relates to choosing destination from a respective start position
#probs are divided by sum bc the probs are actually counts not probabiities
def chooseDestination(probs):
    index = np.random.choice([i for i in range(133)], p=probs/np.sum(probs))
    return index


#This method checks all bikes that have a ride for their arrival time. If it is currently arrival time, the destinaton gets the bike.
def checkMovingBikes(bikeStations, bikesInTransit, currTime):
    for bike in bikesInTransit:
        if (bike.returnTime >= currTime):
            bikeStations[bike.destIndex].returnBike()
            bikesInTransit.remove(bike)

#returns all bikes
def returnAll(bikeStations, bikesInTransit):
    for bike in bikesInTransit:
        bikeStations[bike.destIndex].returnBike()
        bikesInTransit.remove(bike)

#This method checks all queues in the stations to see if they can be moved.
def moveQueues(bikeStations, bikesInTransit, currTime):
    for station in bikeStations:
        station.useBike(bikeStations.index(station), bikesInTransit, currTime)

############################################################################################

#This method runs the simulation
def simulation(startProb):
    totalTime = 60 * 24
    currentTime = 0.0
    newRiders = 0
    bikeStations = [BikeStation() for i in range(133)]
    bikesInTransit = []
    totalRiders = 0

    while (currentTime < totalTime and newRiders < 3500): #while current sim time is less than 24h (divided by min)
        if (currentTime.is_integer()):
            newRiders = newRiders + np.random.exponential(scale=2.38) #every min new riders arrive
        for i in range(int(newRiders)): #every time the new riders is a whole number
            stationIndex = chooseStation(startProb) #rider chooses station
            bikeStations[stationIndex].riderJoins() #joins it
            newRiders = newRiders - 1 #the total new riders arrived decreases by one
            totalRiders = totalRiders + 1
        moveQueues(bikeStations, bikesInTransit, currentTime) #all queues are moved (every .01 min) (which means if a bike is available the person uses it)
        checkMovingBikes(bikeStations, bikesInTransit, currentTime) #all moving bikes are checked (every .01 min) if they have reached their arrival time and need to be added back to a station
        currentTime = round(currentTime + 0.01, 2) #increments current time (rounded do .01s)
    returnAll(bikeStations, bikesInTransit) #returns all bikes at the end of the 24 hour period (just to evaluate return counts)

    stillInQueue = 0 #calculates how many are still in the queue at the end of the day
    for i in range(len(bikeStations)):
        stillInQueue = stillInQueue + bikeStations[i].riderQueue

    print('Total: ', totalRiders) #prints total that entered system
    print('Successful: ', totalRiders - stillInQueue) #prints riders that successfully rode a bike
    print('Successful Rental Prob: ', (totalRiders - stillInQueue)/ totalRiders) #prints success probability
    print('Average Wait Time for Successful: ', currentTime/ (totalRiders - stillInQueue)) #prints average wait time per success
    print()

    return (totalRiders - stillInQueue)/ totalRiders, currentTime/ (totalRiders - stillInQueue) #returns prob and wait time

############################################################################################

startProb = np.zeros((81, 1)) #starting probability array
destProb = np.zeros((133, 133)) #destintion probability array

startProbFile = pd.read_csv("data/start_station_probs.csv", sep=",") #reads starting probs
startProbFile = startProbFile.loc[:, ["station", "station_prob"]] #edited titles inside csv for what it was to station, station_prob
startProbFile = startProbFile.sort_values("station", ignore_index=True) #reorders based on station name to match starts in 2nd data file (destination probs)
startProb = startProbFile["station_prob"]

destProbFile = pd.read_csv("data/trip_stats.csv", sep=",") #reads destination probs
destProbFile = destProbFile.loc[:, ["start", "end", "count"]] #takes the 3 needed columns
destProbFile = destProbFile.sort_values(["start", "end"], ignore_index=True) #sorts by start column then end column
colsToClean = ["start", "end"]

#assign integer numbers to each unique string in each text column (basically creates indexes into destProb arary)
for i in range(len(colsToClean)):
    thisCol = colsToClean[i]
    uniqueValues = destProbFile[thisCol].unique()
    for j in range(len(uniqueValues)):
        destProbFile[thisCol] = destProbFile[thisCol].replace(uniqueValues[j], j)

#maps start to end probabilities into 2d array
for index, row in destProbFile.iterrows():
    destProb[row['start']][row['end']] = row['count']

############################################################################################

#allows multiple simulations to be run and computes confidence intervals for the runs
def multipleSimulations(startProb, simCount):
    probSuccess = []
    successWaitTime = []
    for i in range(simCount):
        aSuccessProb, aWaitTime = simulation(startProb) #runs sim
        probSuccess.append(aSuccessProb) #adds prob to list
        successWaitTime.append(aWaitTime) #adds wait time to list

    probInt = st.t.interval(confidence=0.90, df=len(probSuccess)-1,
              loc=np.mean(probSuccess),
              scale=st.sem(probSuccess)) 
    print('Success Probability Confidence Interval (90%): ', probInt) #prints confidence interval for probabilities

    waitInt = st.t.interval(confidence=0.90, df=len(successWaitTime)-1,
              loc=np.mean(successWaitTime),
              scale=st.sem(successWaitTime))
    print('Wait Time Confidence Interval (90%): ', waitInt) #prints condifence interval for wait times

multipleSimulations(startProb, 10)
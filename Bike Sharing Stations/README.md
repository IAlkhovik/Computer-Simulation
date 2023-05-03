# Team MP3 18

Members: Ivan Alkhovik

## PDF

The PDF can be found at Alkhovik Mini-Project 3 Report.pdf.

## Code Organization

Code is written in Python, divided into methods, and each method is explained through comments. The code uses numpy, pandas, and scipy.stats.

The code contains a few custom objects: BikeStation and BikeRide. A BikeStation has a riderQueue counter and a bikeCount counter. It has 3 methods: returnBike(), riderJoins(), and useBike(). A BikeRide simply stores the return time for a bike and its return destination.

After the two objects are defined, a number of methods are defined. These are chooseStation() which chooses the initial station, chooseDestination(), checkMovingBikes() which checks all the bikes if the simulation has caught up to their return times, returnAll() which is used at the end of the simulation time, and moveQueues() which tries to use a bike in every BikeStation.

After these methods, there is the simulation() method which runs the simulation, a section of code which reads the given probability csv files, and then a multipleSimulations() method which runs multiple simulations and calculates the confidence intervals.

The custom objects, methods, simulation, reading csv files, and multiple simulation sections are divided by a line of #'s.

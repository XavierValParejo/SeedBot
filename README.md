# SeedBot

![Seedbot1](https://github.com/XavierValParejo/SeedBot/blob/master/readMe%20images/0.png) ![Seedbot1](https://github.com/XavierValParejo/SeedBot/blob/master/readMe%20images/1.png)
![Seedbot1](https://github.com/XavierValParejo/SeedBot/blob/master/readMe%20images/2.png)


An eco-friendly robot

## Table of contents
* [Introduction](#introduction)
* [Requirements](#requirements)
* [Usage](#usage)
* [Mapping](#mapping)
* [Path planning](#path-planning)
* [Contributing](#contributing)
* [Special thanks](#special-thanks)
* [Authors](#authors)
* [License](#license)



## Introduction
Welcome to the SeedBot github, this has been an exciting project where we've learned a lot of robotics for the RLP 
subject in the CS degree from the UAB, we hope you can see we tried our best and you're welcome in helping to improve the Seedbot.
What are you going to find in the code?
A 2D simulation in pygame featuring A star and PPT path plannig in an occupancy grid map that has gotten its data from a ultrasonic sensor.

## Requirements
- Pygame
- Numpy
- Matplotlib

## Usage
To launch the 2D Seedbot simulation you just need to get all the files and launch the game.py 

What if I want to make another map?
You need a txt like 'mesures.txt' with a full circle of data.

Interested in changing the starting and finish points? 
For the starting point go to game.py and change lines 32 and 33 although we reccomend to keep it like this.
For the final point change lines 34 and 35.

## Mapping
Our idea for the physical robot was to get our data stored in a txt where we should find (distance, alfa) and we'd have every possible entry to make a full circle.
We had some issues with our mapping as the ultrasonic sensor can be a bit tricky, thats why we used [this](https://github.com/AtsushiSakai/PythonRobotics/blob/master/Mapping/lidar_to_grid_map/lidar_to_grid_map.py) as a template.
Then we used a script to get an OGM (occupancy grid map) in order to be able to make movements inside the map.

## Path planning
From the beginning we knew that A star was one of the main algorithms we wanted to try as it was the one we are most familiar with. While looking at [[1]](https://github.com/AtsushiSakai/PythonRobotics/tree/master/PathPlanning) we loved the idea behind the Probabilistic Road Map and wanted to get it in our project. Sadly we only got it to work as a plot in console.

## Contributing
You are free to make any change in this code as it can be improved a lot.

## Special Thanks
Many thanks to the authors of the diferent scripts we've tried to use for our project.
- Atsushi Sakai and all the ones behind [Python Robotics](https://github.com/AtsushiSakai/PythonRobotics)
- Richardos [github](https://github.com/richardos/occupancy-grid-a-star)
- To our RLP teachers 
- To you, the one who got this far!

## Authors
This part of the project was made by Nischey Verma Kumar and Xavier Val Parejo. </br>
We had a more ambitious approach to this project but unfortunately couldn't reach those heights as many things happened during this project.

## License
[MIT](https://choosealicense.com/licenses/mit/)


#!/usr/bin/env python

# SAFMC_course_navigator.py


##################################################################################################################################

# Script to complete the 2022 SAFMC CAT E competition course. Program basis is loading the trajectory coordinates and
# current formation from a .csv file, then writing the coordinates to the swarm. Coordinates saved in the .csv are
# given as the forward-most drone in the swarm, e.g. the top of the circle formation or the head of the conga-line
# formation.

# Program flow:
# 1. Load the .csv file and parse into a workable dictionary
# 2. Initialise the crazyswarm, takeoff and adjust the CFs into proper formation
# 3. Iterate through the co-ordinate dictionary moving the swarm as follows:
#   3A. If the next dictionary value is in a different formation, first perform the formation change and THEN execute
#       either 3B or 3C.
#   3B. If the drones are in the circle formation, perform a swarm relative move equal to the current global coord minus
#       the previous global coord (in the circle state the drones can always move together). For the first move, "rebuild"
#       the formation at the first global coord.
#   3C. If the drones are in the line formation, create a fresh coord array with length equal to num CFs to store their
#       positions. Initial values here should be the current values in the circle formation (absolute position), with
#       coords[0] = new position and coords[n] removed. Iterate over this array, performing global moves on a drone by
#       drone basis. For the following moves add the next coord from the trajectory dictionary to the top of the array,
#       remove the final value from the array, and write the values to the drones in order. The initial moves will cause
#       the circle formation to "unwrap" into the line formation.
# 4. When the end of the dictionary is reached, the drones should be in the circle formation above the landing zone. Perform
#    a final swarm adjustment to ensure a clean circle, then call the swarm to land.
# 5. Win and lift the trophy reminding your rivals it was EZPZ.

##################################################################################################################################


# Python
import numpy as np
import rospkg
import csv

# Crazyswarm
from pycrazyswarm import *

# ROS
import rospy
import rospkg
from std_msgs.msg import *
from geometry_msgs.msg import *
# from crazyswarm_lnkd.srv import *

# Crazyswarm
# from crazyswarm.msg import GenericLogData


# GLOBAL CONSTANTS
FORMATION_RADIUS = 1.25  # m
TAKEOFF_HEIGHT = 1.0    # m


def initSwarm():
    # Load the crazyflies from file and build the swarm object
    print("CF swarm starting...")
    rospack = rospkg.RosPack()
    launchPath = rospack.get_path(
        'crazyswarm_lnkd')+"/launch/allCrazyflies.yaml"
    # launchPath = "../launch/allCrazyflies.yaml"
    swarm = Crazyswarm(crazyflies_yaml=launchPath)
    timeHelper = swarm.timeHelper
    timeHelper.sleep(3)

    # Reset the estimator to reduce RVIZ jank
    resetEstimator(swarm, timeHelper)

    return swarm, timeHelper


def stableTakeoff(swarm: Crazyswarm, timeHelper):
    # Performs a more stable takeoff facilitated by estimator reset
    resetEstimator(swarm, timeHelper)

    swarm.allcfs.takeoff(targetHeight=TAKEOFF_HEIGHT, duration=4)
    timeHelper.sleep(4.0)


def circleLand(swarm: Crazyswarm, timeHelper, landCoord, reverse=False):
    circleArrangement(swarm, timeHelper, landCoord, avoidance=False, reverse=reverse)
    swarm.allcfs.land(0.04, 2.0)
    timeHelper.sleep(2.0)


def resetEstimator(swarm: Crazyswarm, timeHelper):
    swarm.allcfs.setParam("kalman/resetEstimation", 1)
    timeHelper.sleep(0.1)
    swarm.allcfs.setParam("kalman/resetEstimation", 0)
    timeHelper.sleep(1.0)


def circleArrangement(swarm: Crazyswarm, timeHelper, frontCoord, avoidance=True, reverse=False):
    # Takes front co-ordinates and arranges drones into circle formation
    # Assumes initial positions consider (0,0) to be front drone

    formationPoses = getCircleCoords(swarm, frontCoord, reverse=reverse)
    # if reverse:
    #     formationPos = np.add(np.flip(cf.initialPosition), np.array(frontCoord))
    # else:
    #     formationPos = np.add(cf.initialPosition, np.array(frontCoord))

    if avoidance:
        # 1. Split drones into 5 different movement planes
        for num, cf in enumerate(swarm.allcfs.crazyflies):
            height = calcFlightLevelValue(num, 5)
            cf.goTo([0, 0, height], 0, 2.5, relative=True)
        timeHelper.sleep(2.5)

        # 2. Create drone co-ord from its formation position and the formation's front and move
        for num, cf in enumerate(swarm.allcfs.crazyflies):
            height = calcFlightLevelValue(num, 5)
            formationPos = formationPoses[num]
            formationPos[2] += height
            cf.goTo(formationPos, 0, 2.5, relative=False)
        timeHelper.sleep(2.5)

        # 3. Return to normal height
        for num, cf in enumerate(swarm.allcfs.crazyflies):
            height = calcFlightLevelValue(num, 5)
            cf.goTo([0, 0, -height], 0, 2.5, relative=True)
        timeHelper.sleep(2.5)

    else:
        for num, cf in enumerate(swarm.allcfs.crazyflies):
            formationPos = formationPoses[num]
            cf.goTo(formationPos, 0, 2.5, relative=False)
        timeHelper.sleep(2.5)


def calcFlightLevelValue(droneNum, numLevels):
    # Returns absolute height for drone flight level
    # This might break for number of flight levels different from 5 idfk
    height = (0.25*(droneNum % numLevels)) - 0.5
    return height


def getCircleCoords(swarm: Crazyswarm, circlePosition, reverse=False):
    lineCoords = [[0, 0, 0]]*len(swarm.allcfs.crazyflies)

    for num, cf in enumerate(swarm.allcfs.crazyflies):
        lineCoords[num] = np.add(cf.initialPosition, np.array(circlePosition))

    if reverse:
        lineCoords.reverse()

    return lineCoords


if __name__ == "__main__":
    # Setup swarm object
    swarm, timeHelper = initSwarm()

    # Multi-ranger code has been removed for now, potential to re-add in future
    # MR_checker = rospy.ServiceProxy("MR_checker", MRProximityAlert, persistent=True)

    previousCoord = [0, 0, TAKEOFF_HEIGHT]   # For circle moves
    currentFormation = 0        # 0 = circle, 1 = line
    lineCoords = [[0, 0, 0]]*len(swarm.allcfs.crazyflies)
    reversed = False    # Indicate if the swarm has wrap & unwrapped, lining in reverse order

    # Main program loop
    with open('testCSV.csv', newline='') as csvfile:
    # with open('waypoints.csv', newline='') as csvfile:
        # Load CSV coordinates into iterable object
        # csv_Reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        csv_Reader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')

        # Takeoff
        stableTakeoff(swarm, timeHelper)
        # timeHelper.sleep(4)    UNCOMMENT IF NEEDED FOR STABILITY

        # 3. Iterate over coordate array and move the swarm
        for row in csv_Reader:
            currentCoord = np.array(
                [row['x'], row['y'], row['z']]).astype(np.float32)
            formation = int(row['Formation'])

            # 3A - Circle (FUNCTIONALLY COMPLETE)
            if formation == 0:
                if formation != currentFormation:
                    # Handle formation update from 1 to 0
                    # Hard coded to wrap in the same pattern as starting pattern
                    # this assumes the fleet is returning in opposite direction
                    print("1 to 0")
                    # circleArrangement(swarm, timeHelper, currentCoord)
                    circleCoords = getCircleCoords(swarm, currentCoord, reversed)
                    for coord in circleCoords:
                        lineCoords.pop(len(lineCoords)-1)  # Remove final element
                        lineCoords.insert(0, coord)  # Add new coord to front
                        for num, cf in enumerate(swarm.allcfs.crazyflies):
                            cf.goTo(lineCoords[num].tolist(), 0, 2.5, relative=False)
                        timeHelper.sleep(2.5)
                    reversed = not reversed

                elif int(row['ID']) != 1:
                    relativeMove = np.subtract(
                        currentCoord, previousCoord).tolist()
                    # swarm.allcfs.goTo(relativeMove, 0, 2.5, relative=True)
                    swarm.allcfs.goTo(relativeMove, 0, 2.5)
                    timeHelper.sleep(2.5)
                else:
                    circleArrangement(swarm, timeHelper, currentCoord, False, reverse=reversed)

            # 3B - Line
            else:
                if formation != currentFormation:
                    # Handle formation update from 0 to 1
                    lineCoords = getCircleCoords(swarm, previousCoord, reversed)
                # print("3B")
                lineCoords.pop(len(lineCoords)-1)  # Remove final element
                lineCoords.insert(0, currentCoord)  # Add new coord to front
                # print(lineCoords)
                # Write to drones
                for num, cf in enumerate(swarm.allcfs.crazyflies):
                    cf.goTo(lineCoords[num].tolist(), 0, 2.5, relative=False)
                timeHelper.sleep(2.5)

            # Store the previous coord as DictReader object can't be indexed
            previousCoord = currentCoord
            currentFormation = formation

    # Land
    circleLand(swarm, timeHelper, previousCoord, reverse=reversed)

    # GG

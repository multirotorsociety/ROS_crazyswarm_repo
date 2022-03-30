# ROS_crazyswarm_repo
 Contains all packages/projects linked with Crazyswarm. Crazyswarm_lnkd is a ros package designed to be linked with the main crazyswarm file, using instructions from here: https://crazyswarm.readthedocs.io/en/latest/howto/howto.html (See Option 2: Custom ROS Package)

## Instruction
1. Clone this repo into `crazyswarm/ros_ws/src/`
2. Source ROS and `crazyswarm/ros_ws/devel/setup.bash`
3. In the terminal, run: 
    ```
    export PYTHONPATH=$PYTHONPATH:/path/to/crazyswarm/ros_ws/src/crazyswarm/scripts
    ```
4. Before running 
    ```
    python3 SAFMC_course_navigator.py --sim
    ```
    check the crazyflies initial configuration yaml file and the waypoint csv file that the script is reading, make the essential amendment and run the script with `--sim` first to see if it is working as expected in simulation
5. Run the script without `--sim` on the actual drones, and pray to the UWB/crazyflie/downward ranger deity.
# Crazyflie Diagnosing

Do ensure that the Console Tab is enabled in the CF Client in order to access these options. There are a bunch of other tabs that can graph or help diagnose issues. Do play around with it as it is your only clue about what is going on.

## Hardware Tests

*These tests should be conducted after crashes to determine if the drone is still flight ready. Ideally brand new crazyflies should pass all of this checks and they may be skipped. Especially important when diagnosing a multi-deck setup with UWB*

**Console Logs(CF Client):** Check the Console Tab in cf client. The logs should reveal that the number of decks detected is same as the number of decks listed. Ie Deck 0 and deck 1(if there are two decks))

**Propeller Test (CF Client Console Tab)**, fails if there is too much vibration on a motor

**Battery Test (CF Client Console Tab)**, dispose of high voltage sag batteries

Position Test(No decks, IMU Only), should have no drift

OF Test(With surface)

Position test (With UWB, Without OF) - Ensure x-axis is aligned, should not drift too badly

Position test (With OF and UWB)

Hover/Waypoint Script

# Preflight Checks

**Crazyflie Drones**
1. Battery is not obstructing the UWB deck 
    - Flush the battery back
    - There is a forbidden area underneath the UWB deck that the batter should not enter(marked on pcb)
2. Battery wire is not obstructing the rear propellers
    - Slightly bend the battery wire downwards 
3. The propellers type are matched correctly
    - 2 types of propellers: Type A and Type B
    - Each type should be on opposite ends 
4. Drones and decks are facing +x direction (to the front)
    - Align with the Crazyflie coordinate system
5. Drones are at/near the correct initial position
6. Switch on the drones with it flat on the ground
    - Allows z-ranger to configure properly
7. No self-test fail (5 continuous red blinks)
    - Else, reconnect decks like UWB and reboot
8. No low battery sign (continuous red light)

**UWB Beacons**
1. All beacons are switched on (look for colourful LED)
2. All beacons are raised to the right height
    - Lower beacon: odd number, 0.40m
    - Upper beacon: even number, 2.75m
3. Beacon arms should not droop down too much
4. Perimeter beacons should face inwards
5. Beacons should be far away from metal surfaces 
    - Place mid-point between the stand's metal legs


**Preparation Before Starting 20min Setup Period**
1. Mount UWBs, holders and power banks on the poles
2. Raise UWB poles to 2.75m(or as high as possible) and 0.4m
3. Ensure the UWB Center Points are over the marked position(not the stand center)
4. Power on all the beacons
5. Load poles from the same row onto a trolley
6. Check if there is enough space around 20x40m area to put down poles, else the LPS area has to be shrunk



#### Acknowledgements
Thx JiaHwee & @yufanana
# UWB(DWM1000)/ Crazyflie Loco Positioning notes

## Setup
 Follow: https://www.bitcraze.io/documentation/repository/lps-node-firmware/master/user-guides/anchor-setup/
 
##### Terminology
Anchor - UWB mounted at stationary predetermined points
Node - UWB mounted on CF(Crazyflie)
 
### Inital Setup
In addition to the [LPS Configuration tool](https://www.bitcraze.io/documentation/repository/lps-node-firmware/master/user-guides/tools/), the firmware has to be [downloaded or compiled from the cf github.](https://www.bitcraze.io/documentation/repository/lps-node-firmware/master/building/build_flash/)

Ensure that the stands are distanced away from any other objects( ie walls or any other surfaces) as it might result in [multipathing](https://youtu.be/TcIcC1tqbmk).

There seems to be a significant decrease in accuracy when a UWB beacon is close to a UWB Anchor, this might be a result of Dilution of Precision(Not confirmed).
 
 Ensure the UWB Anchors are mounted with the DWM1000 pointed horizontally for the most even coverage, [see pg15 of the DW1000 datasheet for more details](https://www.decawave.com/sites/default/files/resources/DWM1000-Datasheet-V1.6.pdf).
 
 Here are the distances that Bitcraze managed to achieve with the [various power settings and orientations.](https://wiki.bitcraze.io/misc:investigations:lps-max-range)

Use TDOA3 for larger setups requiring many beacons.

```python3 -m lpstools```
 
 ## Configuring positions
 Enable the Loco Positioning Tab in the CF Client and connect a CF with a loco positioning deck on board to flash it. The anchor id must be added manually for all new anchors in the CF Client configuration. Take note that the CF only flashes parameters to those UWB Anchors in range. 
 
## Biggest Gotcha
The CF must be orientated in the direction of the X-AXIS as defined in the Loco Positioning System or else it will behave erratically and flip out.
 
## Configuring Power
By default, the UWB anchors use SmartPower which works well in most scenarios by increasing power if there is more drones in its radius. However, multi-pathing might occur and the varying power might result in inconsistencies. Hence, it might be more desirable to set the power manually increased for the appropriate range and to reduce interference. Do manually verify if the loco positioing system is giving accurate readings in the cfclient before proceeding to test scripts. For reference, a power of 23.5dB was used in a 5mx5m smaller indoor setup and 24dB in a 10mx10m larger indoor setup. This is particularly important for high anchor setups as...

For TDOA3, a maximum of only [15-20 anchors](https://www.bitcraze.io/documentation/repository/lps-node-firmware/master/functional-areas/tdoa3_implementation/) should be visible to each device(including anchors and tags) at once. Do ensure the power is tuned properly for that to occur.

### Via USB(Slower)
```picocom /dev/ttyACM0```
Type H for help
https://www.bitcraze.io/documentation/repository/lps-node-firmware/master/development/anchor-low-level-config/

### Wirelessly(Recommended due to more power levels and speed)
Edit and run the [set_tx_power.py](https://github.com/bitcraze/lps-node-firmware/blob/master/tools/lpp/set_tx_power.py) script in the lps-node-firmware folder, requires a CF with UWB Deck connected over CF Radio and only updates the anchors in range.

## Debugging TDOA3
This script may be used after an anchor is flashed to SNIFFER mode via PICOCOM(or LPS Configuration Tool). It helps to verify if the anchors are able to see and talk to each other. The script below should help to verify the distances between the anchors.
```python3 tools/sniffer/sniffer_binary.py /dev/ttyACM0 yaml | python3 tools/sniffer/tdoa3_decoder.py | python3 tools/sniffer/tdoa3_tof.py m```
[source](https://www.bitcraze.io/documentation/repository/lps-node-firmware/master/user-guides/tdoa3_setup/)
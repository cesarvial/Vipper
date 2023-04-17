# Introduction

All the code for the `Desktop App` should be in this folder.

The app will be implemented in `Python`, and will have the following features:
 - It will receive all information from the `Sensor Board` and show it to the user in real time;
    - The `mapping` is an exception, it will need more processing to graphically show the path of the robot.
 - It will be connected to the `webcam`, transmiting the images and sounds in real time;
 - It will be connected to the `Control Board`, sending the commands to roll/unroll the body;

Every item is a different implementation, and should be tested independently.

Everything related to the communication must follow the protocol documented.

# Mapping

The algorithm used, needs that the acceleration values are in `g` (the MPU6050 reads in `m/s2`, so it needs to changed for the algorithm to work), and the gyroscope readings are in `deg/s` (the MPU6050 reads in `rad/s`, so it needs to changed for the algorithm to work).

The data must be passed to a `csv` file, in the following format, for each line of readings:
`Packet_Number,Gyro_x,Gyro_y,Gyro_z,Acc_x,Acc_y,Acc_z`.

The data collected is not enough for the algorithm, it also needs a `starting time (s)`, a `ending time (s)`, and a `period between readings (s)`. These values must also be given by the `ESP32` to send, by measuring the time between the first measurement and the last, then with the number of measures we can get the period.

It only reads data from files that end with `_CallInertialAndMag.csv`. This could be easily changed, **but, for some godforsaken reason**, it only accepts the original files from the project (`spiralStairs, stairsAndCorridor, straightLine`). For example, it won't find the data in the `squares` file. So, the file i used to test was the `spiralStairs` file, where i simply pasted all the info there.
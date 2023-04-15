All the code for the `Desktop App` should be in this folder.

The app will be implemented in `Python`, and will have the following features:
 - It will receive all information from the `Sensor Board` and show it to the user in real time;
    - The `mapping` is an exception, it will need more processing to graphically show the path of the robot.
 - It will be connected to the `webcam`, transmiting the images and sounds in real time;
 - It will be connected to the `Control Board`, sending the commands to roll/unroll the body;

Every item is a different implementation, and should be tested independently.

Everything related to the communication must follow the protocol documented.
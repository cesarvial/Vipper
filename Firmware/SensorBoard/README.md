All the code for the firmware in the `ESP32` in the `Sensor Board` should be here.

The firmware will have the following functionalites:
 - It will read all the `sensors` and send all the information to the `Desktop App`.

# Accelerometer/Gyroscope
For the accelerometer and gyroscope, the following data must be sent, for each measure:
 - the id (number) of the measure;
 - the gyroscope value in the x, y, and z axis;
 - the acceleration value in the x, y, and z axis;
 - the time between the current measure and the first.

The protocol to send this information is in the `CommunicationProtocol.md` file.

# Temperature
For the temperature sensor, the only thing needed is the temperature value.

The protocol to send this information is in the `CommunicationProtocol.md` file.

# Gas
For the gas sensor, the only thing needed is the flag indicating the presence of harmfull gas.

The protocol to send this information is in the `CommunicationProtocol.md` file.

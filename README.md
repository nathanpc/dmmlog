# dmmlog

A simple logging manager for your digital multimeter. With this simple script you can send commands to your DMM, perform data logging, and dump the logs stored in the device's memory.

In the current version it only supports Agilent's U1200 line of multimeters, since the only logging multimeter I own at the time is a U1242B, but I plan on implementing others. **If you want your multimeter included in the program please open a Issue** and if possible provide some resources about the protocol it uses.

## Requirements

To run this application you'll need:

  - Python
  - [pySerial](http://pyserial.sourceforge.net/)


## Special Thanks

I would like to thank Daniel Nyberg for reverse engineering Agilent's protocol and publishing this [awesome reference](http://ufpr.dl.sourceforge.net/project/dmmutils/Protocol%20reference).

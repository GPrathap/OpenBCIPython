OpenBCI_Python
==============

The Python software library designed to work with OpenBCI hardware.

Please direct any questions, suggestions and bug reports to the github repo at: https://github.com/OpenBCI/OpenBCI_Python

## Dependancies:

* Python 2.7 or later (https://www.python.org/download/releases/2.7/)
* Numpy 1.7 or later (http://www.numpy.org/)
* Yapsy -- if using pluging (http://yapsy.sourceforge.net/)
* librosa -- (https://librosa.github.io/librosa/)
* matplotlib -- (https://matplotlib.org/)

OpenBCI 8 and 32 bit board with 8 or 16 channels.

This library includes the main open_bci_v3 class definition that instantiates an OpenBCI Board object. This object will initialize communication with the board and get the environment ready for data streaming. This library is designed to work with iOS and Linux distributions. To use a Windows OS, change the __init__ function in open_bci_v3.py to establish a serial connection in Windows.

For additional details on connecting your board visit: http://docs.openbci.com/tutorials/01-GettingStarted

### Ganglion Board

The Ganglion board relies on Bluetooth Low Energy connectivity (BLE). You should also retrieve the bluepy submodule for a more up-to-date version than the version `1.0.5` available at that time through `pip`. To do so, clone this repo with the `--recursive` flag then type `make` inside `bluepy/bluepy`. Note that you may need to run the script with root privileges to for some functionality, e.g. auto-detect MAC address.

You may also need to alter the settings of your bluetooth adapter in order to reduce latency and avoid packet drops -- e.g. if the terminal spams "Warning: Dropped 1 packets" several times a seconds, DO THAT.

On linux, assuming `hci0` is the name of your bluetooth adapter:

`sudo echo 9 > /sys/kernel/debug/bluetooth/hci0/conn_min_interval`

`sudo echo 10 > /sys/kernel/debug/bluetooth/hci0/conn_max_interval`

# Audience:

you can visit http://openbci.com/downloads and browse other OpenBCI software that will fit your needs.

## Functionality

### Basic usage

The startStreaming function of the Board object takes a callback function and begins streaming data from the board. Each packet it receives is then parsed as an OpenBCISample which is passed to the callback function as an argument. 

OpenBCISample members:
-id:
	int from 0-255. Used to tell if packets were skipped.

-channel_data:
	8 int array with current voltage value of each channel (1-8)

-aux_data:
	3 int array with current auxiliary data. (0s by default)

### csv_collect_and_publish.py


[This](https://github.com/GPrathap/OpenBCI_Python/blob/master/plugins/csv_collect_and_publish.py) is the newly created plgin which does a few things in row: collect data from openbci board and save it to csv, collect data from Kinect device over UDP and marge with openbci unprocessed data and create a streasm that will be published to processing unit.


Then simply run the code given as an argument the port your board is connected to:
Ex Linux:
> $python csv_collect_and_publish.py -p /dev/ttyUSB0 

The program should establish a serial connection and reset the board to default settings. When a '-->' appears, you can type a character (character map http://docs.openbci.com/software/01-OpenBCI_SDK)  that will be sent to the board using ser.write. This allows you to change the settings on the board. 

### Proposed Moving Dynamic Time Warping (MDTW) Technique

## Desired Pattern Identification

## Apply Moving Dynamic Time Warping (MDTW) on Kinect Angle (elbow)

## Detecting Local Minima of Distance Vector

## Extracting Labeled Samples







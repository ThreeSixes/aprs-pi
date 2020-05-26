# aprs-pi
## Background
This project is set up to provide network server and message bus access to APRS messages 
originating from a or destined to a KISS TNC. This project also allows client applications such as APRSDroid to connect to the KISS raw port over the network. It's designed to share the radio with any client application that supports KISS over TCP.

## Prerequisites
- An Internet connection (required only for the installation process)
- Appropriate radio license (Ham radio Technician or better in the US)
- VHF radio with (must be able to use it as a KISS TNC)
  - Tested with: Kenwood TM-D710, Kenwood TM-V71, Yaesu FT-991A using the 6-pin data port
- KISS TNC if your radio doesn't already include one (connected via USB serial, Bluetooth, RS-232)
  - Tested with: Kantronics KPC 3+ USB
  - Note: To use a Bluetooth TNC you'll have to figure out how to establish a connection to the BT device using SPP or something similar.
- Functional Raspberry Pi 3+ or newer
  - Tested with a Raspberry Pi 3+ model B
- Installed operating system
  - Tested with Raspbian Buster deployed via NOOBS
- Docker [installed on the Rasbperry Pi](https://docs.docker.com/engine/install/debian/)
- Docker Compose [installed on the Raspberry Pi](https://docs.docker.com/engine/install/debian/)
- MQTT server
  - Tested using Mosquitto

### Theory of operation
This project relies on a KISS TNC to mediate communication between the VHF radio and Raspberry Pi. We leverage Chris Snell's `tnc-server` to share connections to the KISS TNC between muliple applications and software processes. We expose the `tnc-server` port as TCP 6700 on the Raspberry Pi to allow additional applications to leverage the radio. This in effect turns the Raspberry Pi into a KISS TCP server. This project also runs a Docker container that parses and forwards incoming APRS packets into JSON blobs on a message bus so other applications which don't know how to parse APRS frames can still leverage incoming information easily. A base-64 copy of every incoming raw frame is also included in each message bus message. Plans are in the works to create transmit capabilities from the message bus as well.

## Installation
- Ensure all prerequisites are already met.
- Log into the Raspberry Pi via SSH or via graphical console.
  - If you're using the graphical console you'll need to open up a terminal.
- Execute the installation script provided below in the terminal. These can be run as the `pi` user in Rasbpian.
```
sudo apt-get install git -y
git clone git@github.com:ThreeSixes/aprs-pi.git
cd aprs-pi
docker-compose up -d --build
```
- Wait for this script to finish. Building takes a while.
- Run `docker container ls`. You should see `` and `` running.
- You're done installing. These containers will automatically restart on boot.

## Configuration

## Running the project

## Known issues
* Transmit functionality from the message bus is still under development.
* We use a pre-compiled `tnc-server` binary because compiling the Go application fails in Alpine due to build chain issues.

## Acknowledgements
* Bob Bruninga, WB4APR for creating the [APRS protocol](http://www.aprs.org)
* Chris Snell for his [tnc-server](https://github.com/chrissnell/tnc-server) project
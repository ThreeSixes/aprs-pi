# aprs-pi
## Background
This project is set up to provide network server and message bus access to APRS messages 
originating from a or destined to a KISS TNC. This project also allows client applications such as APRSDroid to connect to the KISS raw port over the network. It's designed to share the radio with any client application that supports KISS over TCP, and to allow applications that can leverage MQTT to send and recieve APRS messages.

## Prerequisites
- An Internet connection
  * Notes: An Internet connection is only required for installation and updates. Thi should function without an Internet connection once installed.
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
```
- Configure the .env file as specified in the configuration section.
- Build and start the containers:
```
docker-compose up -d --build
```
- Wait for this script to finish. Building takes a while.
- Run `docker container ls`. You should see two containers named `aprs-pi_aprs-bot_1` and `aprs-pi_tnc-server_1` running.
- You're done installing. These containers will automatically start on boot assuming you've configured Docker to start on boot.

## Configuration
The primary source of configuration values for the application is the `.env` file wich passes environment variables to `docker-compose` that define the applications' behavior.

### Configuration process
- If you haven't already copy the `dotenv.dist` file in the repository to `.env`. These environment variables serve to configure the containers.
  * Edit the `.env` file to suit your needs. The parameter you'll most likely want to change is `MQTT_SERVER`. This should be the address of your MQTT server. You might also need to change `TNC_BAUD` and `TNC_SERIAL` to match your KISS TNC's configuration.
- In the event you're just re-configuring the containers run `docker-compose down -d` and the n `docker-compose up -d` up to apply your new configuration.

## Updating aprs-pi
In order to update the version of this software running on your Raspberry Pi run the following commands inside the `aprs-pi` repo.
```
git pull
docker-compose down
docker-compose up -d --build
```

## Known issues
* Transmit functionality from the message bus is still under development.
* We use a pre-compiled `tnc-server` binary because compiling the Go application fails in Alpine due to build chain issues. I will attempt to get building from source working again.

## Application notes
* The KISS TNC server port will be exposed on your Raspberry Pi as `6700` by default, or whatever you set `TNC_LISTEN_PORT` to in the `.env` file. The containers inside the Docker network still use the default TCP `6700`.
* The default MQTT topic APRS messages are recieved on is `aprs/rx`. Messages will be transmitted from `aprs/tx`. If you adjust the `MQTT_TOPIC_PREFIX` in the `.env` just replace `aprs` with whatever you topic prefix you set. The `rx` and `tx` endpoints will be unchanged.
* An MQTT server such as Mosquitto can be run on the Raspberry Pi along with this application. I didn't include an MQTT server in the `docker-compose.yml` because I already have one running on my network. I did include an alternative docker-compose and dotenv dist file named `docker-compose-mosquitto.yml` and `dotenv-mosquitto.dist` which will also fire up a MQTT server on the Raspberry Pi. The `dotenv-mosquitto.dist` file should be copied to `.env` and customized as-needed. To use the Docker Compose file that provides the Mosquitto MQTT server just add `-f docker-compose-mosquitto.yml` to the `docker-compose up` command you're using to start the stack. When enabled Mosquitto exposes the `MQTT_SERVER_PORT` as defined in the `.env` file on the Raspberry Pi for MQTT clients to use.

## Acknowledgements
* Bob Bruninga, WB4APR for creating the [APRS protocol](http://www.aprs.org)
* Chris Snell for his [tnc-server](https://github.com/chrissnell/tnc-server) project
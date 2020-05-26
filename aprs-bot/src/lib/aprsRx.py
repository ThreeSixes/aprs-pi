import base64
import hexdump
import json
import struct
import time
import traceback

import aprs
import aprslib
import kiss
import paho.mqtt.client as mqtt


class aprsRx:
    def __init__(self,
        connection_spec,
        mqtt_base_topic,
        mqtt_host="127.0.0.1",
        mqtt_port=1883,
        debug=False):

        self.__config = {}
        self.__debug = debug
        self.__mqtt_host = mqtt_host
        self.__mqtt_port = mqtt_port
        self.__mqtt_base_topic = mqtt_base_topic
        self.__mqtt_rx_topic = mqtt_base_topic + "/rx"
        self.__mqtt_tx_topic = mqtt_base_topic + "/tx"
        self.__connection_spec = connection_spec

        self.__k = None
        self.__m = None


    def __mqtt_connect(self):
        """
        Connect to our MQTT server.
        """

        self.__m.connect(self.__mqtt_host, self.__mqtt_port)


    @staticmethod
    def hexdump(frame):
        """
        Hex dump a given frame
        """

        hexdump.hexdump(frame)


    def process_frame(self, frame):
        """
        Process an incoming frame according to configured options.
        """
        
        frame_dict = {}

        # If we're in debug mode...
        if self.__debug:
            print("Incoming frame:")
            self.hexdump(frame)
            print("")

        frame_base64 = "%s" %base64.standard_b64encode(frame).decode()
        frame_dict.update({'frame_base64': frame_base64})

        try:
            aprs_parsed = "%s" %aprs.parse_frame(frame)
            frame_dict.update(aprslib.parse(aprs_parsed))
        
        
        except ValueError:
            frame_dict.update({'parse_error_message': "ValueError"})

        except aprslib.exceptions.ParseError:
            frame_dict.update({'parse_error_message': "ParseError"})

        except aprslib.exceptions.UnknownFormat:
            frame_dict.update({'parse_error_message': "UnknownFormat"})

        # Ugly AF, we really don't want to be doing this.
        try:
            self.__m.publish(self.__mqtt_rx_topic, json.dumps(frame_dict))

        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            print(traceback.format_exc())
            self.__mqtt_connect()


    def start(self):
        """
        Start.
        """
        print("aprs-bot RX starting...")

        # Do the MQTT things.
        self.__m = mqtt.Client()

        # Ugly AF. Do this better.
        try:
            self.__mqtt_connect()

        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            print(traceback.format_exc())
            time.sleep(1)
            self.__mqtt_connect()

        # Determine what sort of connection method to use.
        if self.__connection_spec['type'] == "tcp":
            self.__k = kiss.TCPKISS(
                self.__connection_spec['host'],
                self.__connection_spec['port'])

        elif self.__connection_spec['type'] == "serial":
            self.__k = kiss.SerialKISS(
                self.__connection_spec['serial_port'],
                self.__connection_spec['baud'])

        # Connect up.
        self.__k.start()
        self.__k.read(callback=self.process_frame)
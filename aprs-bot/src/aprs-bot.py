import os
import socket
import time
from pprint import pprint

from aprsRx import aprsRx


# APRS Bot Entrypoint
if __name__ == "__main__":
    try:
        print("aprs-bot starting...")

        # Are we enabled?
        aprs_bot_enabled = os.getenv("APRS_BOT_ENABLED", "true")

        # Go into a holding pattern.
        if aprs_bot_enabled.lower() == "false":
            print("aprs-bot disabled. Sleeping.")
            while True:
                time.sleep(600)

        # Create configuration objects.
        kiss_connction_spec = {
            "baud":        int(os.getenv("KISS_BAUD", 1200)),
            "type":        os.getenv("KISS_CONN_TYPE", "tcp"),
            "host":        socket.gethostbyname(os.getenv("KISS_HOST", "127.0.0.1")),
            "port":        int(os.getenv("KISS_PORT", 6700)),
            "serial_port": os.getenv("KISS_SERIAL_PORT", "/dev/ttyUSB0")
        }

        debug_mode   = os.getenv("DEBUG", "false")
        topic_prefix = os.getenv("MQTT_TOPIC_PREFIX", "aprs")
        mqtt_port    = int(os.getenv("MQTT_PORT", 1883))
        mqtt_server  = socket.gethostbyname(os.getenv("MQTT_SERVER", "127.0.0.1"))

        # Make sure our debug flag is set correctly.
        if debug_mode.lower() == "true":
            debug_mode = True
        elif debug_mode.lower() == "false":
            debug_mode = False

        pprint(kiss_connction_spec)

        aprsRx = aprsRx(
            kiss_connction_spec,
            topic_prefix,
            mqtt_server,
            mqtt_port=mqtt_port,
            debug=debug_mode)

        aprsRx.start()

    except (KeyboardInterrupt, SystemExit):
        print("Caught exit signal.")
        exit(0)
    
    finally:
        print("aprs-bot exiting...")
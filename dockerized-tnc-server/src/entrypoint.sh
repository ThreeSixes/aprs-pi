#!/bin/sh

echo "Starting TNC server..."
/app/tnc-server -port=$SERIAL_PORT -baud=$BAUDRATE -listen=$LISTEN_SPEC
export KISS_CONN_TYPE="tcp"
export KISS_HOST="uhfvhf.robots"
export MQTT_TOPIC_PREFIX="homeautomation/aprs"
export MQTT_SERVER="house.robots"
export DEBUG=true

python src/aprs-bot.py

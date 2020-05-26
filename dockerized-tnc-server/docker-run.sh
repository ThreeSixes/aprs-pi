docker run \
    -d \
    -p "6700:6700" \
    --device "/dev/ttyUSB0:/dev/ttyTNC0" \
    --restart unless-stopped \
    --name tnc-server \
    tnc-server:latest
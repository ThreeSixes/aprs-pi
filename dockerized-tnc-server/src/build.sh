#!/bin/sh

cd /tmp 
wget http://island.nu/tnc-server/tnc-server-linux-arm6.tar.gz 
tar x -f tnc-server-linux-arm6.tar.gz 
mv tnc-server/tnc-server /app/ 
chown root:root /app/tnc-server
chmod +x /app/tnc-server
rm -rf /tmp/*
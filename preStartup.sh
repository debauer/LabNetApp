#!/bin/bash
PI_IP=192.168.1.11

PS= ps -e -o pid,unit | grep labnetapp | awk '{print $1}'
echo $PS > out
echo "PID is $PS"

echo "stop can2socket service"
ssh pi@$PI_IP "sudo systemctl stop can2socket"
echo "wait 1sec"
sleep 1
echo "set can1 link down"
ssh pi@$PI_IP "sudo ip link set can1 down"
echo "set can1 link up with 125kbit"
ssh pi@$PI_IP "sudo ip link set can1 up type can bitrate 125000"
echo "start can2socket service"
ssh pi@$PI_IP "sudo systemctl start can2socket"
sleep 5

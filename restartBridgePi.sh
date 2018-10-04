PI_IP=192.168.1.11

echo "stop can2socket service"
ssh root@$PI_IP "systemctl stop can2socket"
echo "wait 1sec"
sleep 1
echo "set can1 link down"
ssh root@$PI_IP "ip link set can1 down"
echo "set can1 link up with 125kbit"
ssh root@$PI_IP "ip link set can1 up type can bitrate 125000"
echo "start can2socket service"
ssh root@$PI_IP "systemctl start can2socket"


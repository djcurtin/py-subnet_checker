# py-subnet_checker
Python script which takes an IP and subnet in CIDR notation, calculates subnet values and validates supplied IP.

Usage: ```subnet.py [cidr]```

Where cidr consists of an IPv4 IP address (x.x.x.x) a slash (/) and a number between 1 and 31*

examples: 
```
    subnet.py 172.16.160.0/19
    subnet.py 192.168.1.21/24
```

**Note**:
Although /32 is a valid CIDR, this script does not accept it as input because there's no calculation to be done.

x.x.x.x/32 just means the IP address x.x.x.x itself
The subnet mask is 255.255.255.255

## Sample Output
```
$ python subnet.py 172.16.160.0/19

Host IP:	172.16.160.0
Subnet Mask:	255.255.224.0
Upstream:	172.16.0.0
Hosts:		32
Subnets:	8

Network IDs of each subnet:
0)	172.16.0.0
1)	172.16.32.0
2)	172.16.64.0
3)	172.16.96.0
4)	172.16.128.0
5)	172.16.160.0
6)	172.16.192.0
7)	172.16.224.0

Broadcast IDs of each subnet:
0)	172.16.31.255
1)	172.16.63.255
2)	172.16.95.255
3)	172.16.127.255
4)	172.16.159.255
5)	172.16.191.255
6)	172.16.223.255
7)	172.16.255.255

IP Address 172.16.160.0 is an INVALID address on subnet 172.16.160.0.
REASON: IP Address is Network ID.
```

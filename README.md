# py-subnet_checker
Python script which takes an IP and subnet in CIDR notation, calculates subnet values and validates supplied IP.

Usage: ```subnet.py [cidr]```

Where cidr consists of an IPv4 IP address (x.x.x.x) a slash (/) and a number between 1 and 32*

examples: 
```
    subnet.py 172.16.160.0/19
    subnet.py 192.168.1.21/24
```

x.x.x.x/32 just means the IP address x.x.x.x itself

## Sample Output
```
$ python subnet.py 172.16.160.0/19


Calculating subnet values for:

IP Address:	172.16.160.0
Subnet Mask:	255.255.224.0
Host Octet:	3
Upstream ID:	172.16.0.0

IP in binary:	10101100.00010000.10100000.00000000
Subnet binary:	11111111.11111111.11100000.00000000

Total IPs:	65536
Total Subnets:	8
IPs Per Subnet:	8192

The following are the network IDs and broadcast IDs for each subnet:
172.16.0.0	172.16.31.255
172.16.32.0	172.16.63.255
172.16.64.0	172.16.95.255
172.16.96.0	172.16.127.255
172.16.128.0	172.16.159.255
172.16.160.0	172.16.191.255
172.16.192.0	172.16.223.255
172.16.224.0	172.16.255.255


IP Address 172.16.160.0/19 is an INVALID IP on subnet id 172.16.160.0.
REASON: IP Address is the network ID for the associated subnet.

```

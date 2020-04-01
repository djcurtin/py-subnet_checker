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

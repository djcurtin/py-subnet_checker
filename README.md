# py-subnet_checker
Python script which takes an IP and subnet in CIDR notation, calculates subnet values and validates supplied IP.

Usage: subnet.py [ip/cidr] where ip is in ipv4 x.x.x.x format and cidr is between 1 and 31
    
The slash (/) must immediately follow the ip. NO SPACES IN THE NOTATION.
IP must have four octets separated by periods (x.x.x.x)

example: 
```
    subnet.py 172.16.160.0/19
    subnet.py 192.168.1.21/24
```

**Note**:
Although /32 is a valid CIDR, this script does not accept it as input because there's no calculation to be done.

x.x.x.x/32 just means the IP address x.x.x.x itself
The subnet mask is 255.255.255.255

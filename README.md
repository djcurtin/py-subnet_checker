# py-subnet_checker
Python script which takes an IP and subnet in CIDR notation, calculates subnet values and validates supplied IP.

Usage: subnet.py [ip/cidr] where ip is in ipv4 x.x.x.x format and cidr is between 1 and 31
    
The slash (/) must immediately follow the ip. NO SPACES IN THE NOTATION.
IP must have four octets separated by periods (x.x.x.x)

example: subnet.py 172.16.160.0/19
         subnet.py 192.168.1.21/24

*Note*: This script is used for subnetting purposes where /32 is not seen because there is not enough room for a network id, broadcast ip and host ips. In ACLs or areas where a single IP is to be specified with x.x.x.x/32, this is outside the scope of the script.

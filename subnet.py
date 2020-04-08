"""
Script to determine characteristics of subnet and IP based on supplied CIDR notation.

Takes input in x.x.x.x/y format where x.x.x.x is valid IP and y is 1-32 CIDR notation.
From this input, script determines the following:
    - Upstream Network ID: Network ID of network being subnetted.
      - e.g., 1.2.3.4/24 = 1.2.3.0; 1.2.3.4/19 = 1.2.0.0
    - Subnet mask in x.x.x.x format
    - Total number of subnets created, and total number of available ip addresses
    - All valid subnet network IDs and broadcast IDs created by supplied CIDR
    - Subnet network ID and broadcast ID for supplied IP
    - Whether supplied IP is valid IP for calculated subnet
"""
import sys

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Error handling functions
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def show_help():
    print("""
    Script is designed to take a properly formatted CIDR notation and calculate subnet information.
    After displaying subnet information, script will determine whether IP is valid host IP for the subnet.

    Usage: subnet.py [ip/cidr] where ip is in ipv4 x.x.x.x format and cidr is between 1 and 32
    Note:  the slash (/) must immediately follow the ip. NO SPACES IN THE NOTATION.

    example: subnet.py 172.16.160.0/19
             subnet.py 192.168.1.21/24
    """)

def ip_octet_error():
    print("""\nIP Error: Check IP address entered.

    1) Each IP address octet must be between 0 and 255, and
    2) IPs must have 4 octets
    """)

def cidr_error():
    print("\nError: CIDR notation must be between 1 and 31\n")

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Command line checking code.
#:
#: I know using exit() is not "proper" program flow, but this ain't software
#: engineering :)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Make sure one and only one ip/cidr input
#:
if len(sys.argv) != 2:
    show_help()
    exit()

#: Cannot have ip without dots, and cannot have cidr without slash
#:
if ("." not in sys.argv[1]) or ("/" not in sys.argv[1]):
    show_help()
    exit()

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Main code
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Parse the arguments
#:
ip, cidr = sys.argv[ 1 ].split( "/" )
ip       = [ int(i) for i in ip.split(".") ]
cidr     = int( cidr )

#: Check for proper ip octets and cidr values
#:
for octet in ip:
    if octet < 0 or octet > 255:
        ip_octet_error()
        exit()

if len(ip) != 4:
    ip_octet_error()
    exit()

if cidr < 1 or cidr > 32:
    cidr_error()
    exit()

#: CIDR of /32 means the IP address itself. Nothing more to be done
if cidr == 32:
    ip = '.'.join([ str(s) for s in ip ])
    print(f"\n{sys.argv[1]} means IP address {ip}.\n")
    exit()

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::: And Now The Main Event ::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: First figure out what I call the first host octet of the IP address.
#:
##: This is what I call the first octet of the IP address where the
##: corresponding subnet mask octet is not 255. This is easy to figure out. The
##: formula is ( CIDR // 8 ) + 1. This will be used later.
##:
##: x // y is equivalent to rounding down a division to zero decimal places. We
##: then add 1 to the answer. So (7 // 8) + 1 = 1, which means the first subnet
##: mask octet is not 255, which is true. (9 // 8) + 1 = 2, which means the
##: subnet mask is 255.x.0.0
##:
host_octet = (cidr // 8) + 1

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Calculating subnet mask
#:
##: Subnet mask is simple: a string of 32 ones or zeros, which begins with 
##: CIDR consecutive ones. So /1 means 10000..., /8 111111110000...
##: We break this into an array of 4 octets so it's easier to work with.
##:
##: e.g.: /19 subnet mask is 255.255.224.0, which this will store as 
##:       [255, 255, 224, 0]
##:
subnet_bits = ("1" * cidr) + ("0" * (32 - cidr))
subnet_mask = [ int(subnet_bits[i : i+8], 2) for i in range(0, 32, 8) ]

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Calculate number of subnets created
#:
##: This is simple when you understand what CIDR and subnet mask are. For every
##: bit in an octet, you double the amount of subnets created, which is to say
##: 2 ^ (bits), where bits is going to be equal to CIDR % 8.
##:
##: x % y returns the remainder of x/y. So 1 % 8 = 1, 9 % 8 = 1, 8 % 8 = 0, etc
##:
##: examples:
##:   /1 makes the subnet mask of octet 1 "10000000". This creates 2 subnets
##:   /2 is "11000000" which creates 4 subnets [00, 01, 10 and 11]
##:   /3 is "11100000" which creates 8, and so on
##:   /9 does what /1 does, but for octet 2, /10 same as /2 and so on.
##:
##: So number of subnets is 2 ^ CIDR for CIDR between 1 and 7, but after 7,
##: it loops back around to 1 because /8, /16 and /24 creates one subnet. Thus,
##: we use mod (%) operator. Number of subnets, thus, is as follows:
##:
subnets = 2 ** (cidr % 8)

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Calculate number of ip per subnet
#:
##: Quickest way to do this is to take total number of IP addresses available
##: in IPv4 (2 ^ 32) and divide is by 2 ^ CIDR. Easiest way to do this is to
##: subtract the powers, which gives us 2 ^ (32 - CIDR).
##:
##: Note: This is total IP addresses, not total host addresses per subnet.
##:       Because each subnet needs one network id and one broadcast id, the
##:       number of host IPs per subnet is total IPs minus 2.
##:
ip_per_subnet = 2 ** (32 - cidr)
total_ip_addresses = ip_per_subnet * subnets

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Get upstream network ID
#:
##: This is the network ID of the network being subnetted. In other words, it
##: is every octet in the IP address which corresponds to a 255 octet subnet
##: mask, and zeros for the rest. Here we just take the first host_octet octets
##: and do not add zeros to make it easier to work with below. We add the zeros
##: when outputting it.
##:
upstream_id = ip[0 : host_octet-1]

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Calculate all valid subnet network IDs and broadcast IDs
#:
##: Each subnet will make up n ip addresses. So calculating all the subnet
##: network IDs is easily done by starting with upstream_id and increasing the
##: host octet by (hosts_per_subnet), starting at zero. Thus, on a /27, which
##: creates subnets with 32 ip addresses each, we should see the following
##: values: 0, 32, 64, 96, 128, 160, 192, 224. And, indeed, these will be our
##: network IDs.
##:
##: The broadcast ID, since it is the all-ones version, will be the highest
##: possible value, so using the same /27 with the network values above, our
##: broadcast values will be the highest end, which is as follows:
##: [31, 63, 95, 127, 159, 191, 223, 255]
##:
id_per_subnet = 2 ** (8 - (cidr % 8))

subnet_ids = []
broadcasts = []
subnet_index = -1
step = 0
for i in range(0, 256, id_per_subnet):
    network_id = i
    broadcast  = network_id + id_per_subnet - 1

    #: Subnet network id is first address in subnet. All zeros after subnet mask
    tmp_subnet = upstream_id + [network_id] + ([0] * (4 - host_octet))
    subnet_ids.append( '.'.join([ str(s) for s in tmp_subnet ]) )

    #: Broadcast is all ones so highest host value and all ones afterward
    tmp_broadcast = upstream_id + [broadcast] + ([255] * (4 - host_octet))
    broadcasts.append( '.'.join([ str(b) for b in tmp_broadcast ]) )

    #: If supplied IP falls into this subnet, keep note of the index for later 
    #: and validate IP by making sure it is not the network id or broadcast id
    if (ip[host_octet-1] >= network_id) and (ip[host_octet-1] <= broadcast):
        subnet_index = step

    step = step + 1

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Output time.
#:
#: First we format our data. Convert all ip lists into string dot format.
ip_bits = '.'.join([ format(s, "08b") for s in ip ]) 

ip_address  = '.'.join([ str(s) for s in ip ])
subnet_mask = '.'.join([ str(s) for s in subnet_mask ])
upstream_id = '.'.join([ str(s) for s in upstream_id + ([0] * (5 - host_octet)) ])
ip_per_sub  = int( total_ip_addresses / subnets )

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Is IP Address a valid one for this subnet?
#:
#: Not if it matches either the network ID or broadcast ID. Yes otherwise
#:
if ip_address == subnet_ids[ subnet_index ]:
    is_valid = f"\nIP Address {ip_address}/{cidr} is an INVALID IP on subnet id {subnet_ids[ subnet_index]}.\nREASON: IP Address is the network ID for the associated subnet.\n"
elif ip_address == broadcasts[ subnet_index ]:
    is_valid = f"\nIP Address {ip_address}/{cidr} is an INVALID IP on subnet id {subnet_ids[ subnet_index]}.\nREASON: IP Address is the broadcast ID for the associated subnet.\n"
else:
    is_valid = f"IP Address {ip_address}/{cidr} is a VALID IP on subnet id {subnet_ids[ subnet_index]}.\n"

subnet_info = '\n'.join([ subnet_ids[i] + "\t" + broadcasts[i] for i in range(0, subnets) ])
subnet_bits = '.'.join([ subnet_bits[i : i+8] for i in [0, 8, 16, 24] ])

output = f"""
Calculating subnet values for:

IP Address:\t{ip_address}
Subnet Mask:\t{subnet_mask}
Host Octet:\t{host_octet}
Upstream ID:\t{upstream_id}

IP in binary:\t{ip_bits}
Subnet binary:\t{subnet_bits}

Total IPs:\t{total_ip_addresses}
Total Subnets:\t{subnets}
IPs Per Subnet:\t{ip_per_sub}

The following are the network IDs and broadcast IDs for each subnet:
{subnet_info}

{is_valid}"""

print(output)

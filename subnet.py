import sys
import math

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Error handling functions
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def show_help():
    print("""
    Script is designed to take a properly formatted CIDR notation and calculate subnet information.
    After displaying subnet information, script will determine whether IP is valid host IP for the subnet.

    Usage: subnet.py [ip/cidr] where ip is in ipv4 x.x.x.x format and cidr is between 1 and 31
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

if cidr < 1 or cidr > 31:
    cidr_error()
    exit()

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::: And Now The Main Event ::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#: Use CIDR to determine host ID octet.
#:
##: Host ID octet is what I call the first octet of the subnet mask, which is 
##: not 255. 
##:
##: /1 - /7 starts in octet 1
##: /8 - /15 is 2, etc
##:
##: Easily done by rounding up cidr / 8, and adding 1 if it lands on 8, 16, or 24
##:
host_octet = math.ceil( cidr / 8 )
host_octet = host_octet if cidr % 8 != 0 else host_octet + 1

#: Build subnet mask using binary
#:
##: CIDR is the number of 1s in the subnet mask, which will always be filled from
##: left-to-right. So /1 is "1000000...", /2 is "1100000...." and so on.
##:
##: This makes use of pythons string multiple functionality to make the binary
##: subnet mask, which is then turned into an array of decimal values.
##:
subnet_mask = ( "1" * cidr ) + ( "0" * (32 - cidr) )
subnet_mask = [ int(subnet_mask[i:i+8], 2) for i in [0, 8, 16, 24] ]

#: Find upstream Network ID. This is the network ID being subnetted
#:
##: Upstream id for a 172.16.160.x/24 CIDR will be 172.16.160.0.
##: For 172.16.160.x/19, however, host id begins in octet 3 so upstream is 172.16.0.0.
##:
##: The code below takes the first x octets of the submitted ip, where x is the number of
##: octets of the subnet mask equaliing 255. It then adds zeroes to the end.
##:
##: upstream_id will be an array of decimal values, to make it easier to work with
##:
upstream_id = ip[0:host_octet-1] + [ 0 ] * ( 5 - host_octet )

# Calculate number of networks and hosts created by subnet mask
#:
##: Number of subnets will be equal to 2^(cidr % 8). e.g., 2^(1 % 8) = 2, 2^(19 % 8) = 8
##: Maximum hosts per octet is 256. So to get host count, divide 256 by # of subnets
##:
subnets = 2 ** ( cidr % 8 )
hosts   = int( 256 / subnets )

#: Now calculate the network IDs, and broadcast IDs for all subnets under upstream_id/CIDR
#:
##: First, we store the non-host values in the upstream_id list
##:
network_octets = upstream_id[0:host_octet-1]

#: This calculates the first and last values in each subnet's range for the first non-network octet
#: which will be used to calculate the subnet network IDs and broadcast IPs
#:
##: The number of hosts per subnet dictates the ranges here. So on a /25, for instance,
##: there are 128 host addresses (0 to 127 and 128 to 255). And on a /26 there are 64,
##: (0 to 63, 64 to 127, 128 to 191, 192 to 255). Each time you add a bit to the CIDR,
##: you double the number of subnets, and halve the number of hosts per subnet.
##:
##: e.g., for 192.168.1.0/17, the first non-network octet is where the 1 is located. But
##: the lowest value here is 0 so the subnets are:
##: 192.168.0 to 192.168.127, and
##: 192.168.128 to 192.168.255
##:
##: for 192.168.1.0/24 the first non-network octet is the last one. But the host octet does not
##: contain subnet bits, so the range is 192.168.1.0 to 192.168.1.255
##:
##: for 192.168.1.0/25, the first is also the last octet, but now there is one subnet bit.
##: Thus, the subnets here are:
##: 192.168.1.0 to 192.168.1.127, and
##: 192.168.1.128 to 192.168.1.255
##:
subnet_data = [ (hosts * i, hosts * (i + 1) - 1) for i in range( subnets ) ]

#: Make a list of all subnet network IDs.
#: 
##: This is done by combining the network_octets with the low end of each of the
##: subnet_data entries calculated above, and filling remaining octets with zeros.
##:
subnet_list = [ network_octets + [s[0]] + ((4 - host_octet) * [0]) for s in subnet_data ]

#: Determine broadcast IDs for each subnet.
#:
##: Broadcast IDs are like network IDs computed above, but using the high end of
##: subnet_data entries, and filling remaining octets with 255
##:
broadcast_list = [ network_octets + [s[1]] + ((4 - host_octet) * [255]) for s in subnet_data ]

#: Find subnet ID on which IP given at command line is located.
#:
##: Just search the subnet_data array until one where the host_octet is between
##: the low end and the high end is found
##: 
i = 0
subnet_id = -1
host_id   = ip[ host_octet - 1]

while (subnet_id == -1) and (i < subnets):
    sub_low = subnet_data[i][0]
    sub_hi  = subnet_data[i][1]

    if (host_id >= sub_low) and (host_id <= sub_hi):
        subnet_id = i

    i = i + 1

#: Validate IP supplied at command line
#:
##: The network ID and broadcast IP of a subnet are reserved, so these are not
##: valid IP addresses on a subnet. So to validate the supplied IP, we simply
##: make sure it is greater than the network ID and less than broadcast IP.
##:
##: Both subnet id and broadcast ip are created the same way:
##: - Start with upstream network id (network_octets calculated above)
##: - Add low end value of host id for subnet id and high end for broadcast ip
##: - Fill any remaining octets with 0 for subnet id and 255 for broadcast ip
##:
##: e.g., for 172.16.160.0/19:
##: - The upstream network is 172.16.0.0 so the network octets are 172.16
##: - The subnet is between 160 and 191 so 160 for subnet, 191 for broadcast
##:   - 172.16.160 [low end] to 172.16.191 [high end]
##: - Add zeros to ensure four octets to get subnet id, and 255 for broadcast
##:   - subnet id: 172.16.160.0
##:   - broadcast: 172.16.191.255
##:
ip_subnet = network_octets + [sub_low] + ((4 - host_octet) * [0])
ip_broadc = network_octets + [sub_hi] + ((4 - host_octet) * [255])

#: Simplest way to validate IPs
#:
##: Loop through each octet and compare supplied IP with subnet id and broadcast
##: IP. If it matches one of them exactly, IP is invalid on that subnet.
##:
is_netid = True
is_bcid  = True

for i in range(0, 4):
    is_netid = is_netid and (ip_subnet[i] == ip[i])
    is_bcid = is_bcid and (ip_broadc[i] == ip[i])

#: Format our validity reporting string for output later
#:
if is_netid:
    is_valid = "IP Address {} is an INVALID address on subnet {}.\nREASON: IP Address is Network ID."
elif is_bcid:
    is_valid = "IP Address {} is an INVALID address on subnet {}.\nREASON: IP Address is Broadcast Address."
else:
    is_valid = "IP Address {} is a VALID address on subnet {}."

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: Output our results
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#: To make the output pretty, each IP array is:
#: 1) Converted from decimal values to strings
#: 2) Combined into a single string, separated by periods (.)
#:
ip  = '.'.join([ str(i) for i in ip ])
snm = '.'.join([ str(i) for i in subnet_mask ])
ups = '.'.join([ str(i) for i in upstream_id ])

#: Create the arrays which will store every subnet ID, and every broadcast
#: IP possible for the given IP and CIDR.
#:
sns = []
bcs = []

#: Run through the list of subnet ids and broadcast ips calculated above,
#: convert them to strings and combine them into period separated strings
#: like we did with ip, subnet mask and upstream network id above
#:
for s in range(subnets):
    sns.append( '.'.join( [str(i) for i in subnet_list[s]] ) )
    bcs.append( '.'.join( [str(i) for i in broadcast_list[s]] ) )

#: Also convert subnet ID for subnet to which supplied IP belongs
#:
ip_subnet = '.'.join([ str(i) for i in ip_subnet ])

#: Sloppy way of making the output string, but it gets the job done, and made it
##: easy to build the output as I went along. Just plug in the values calculated,
##: and enjoy the results.
##:
output = """
Host IP:\t{ip}
Subnet Mask:\t{snm}
Upstream:\t{ups}
Hosts:\t\t{h}
Subnets:\t{s}

Network IDs of each subnet:
{sns}

Broadcast IDs of each subnet:
{bcs}

{iv}
""".format(
        ip  = ip,
        snm = snm,
        ups = ups,
        h   = hosts,
        s   = subnets,
        sns = "\n".join(sns),
        bcs = "\n".join(bcs),
        iv  = is_valid.format(ip, ip_subnet)
)

print(output)

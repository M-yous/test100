import pexpect
from pprint import pprint
import re

# Define constants
ROUTER_IP = '192.168.56.130'
USERNAME = 'prne'
PASSWORD = 'cisco123!'

# Create regular expressions
# (Your existing regex patterns here)

# Connect to device and run 'show ip route' command
print('--- Connecting to router at', ROUTER_IP)

session = pexpect.spawn(f'telnet {ROUTER_IP}', encoding='utf-8', timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

# Check for failure
if result != 0:
    print('Timeout or unexpected reply from device')
    exit()

# Enter username
session.sendline(USERNAME)
result = session.expect('Password:')

# Enter password
session.sendline(PASSWORD)
result = session.expect('>')

# Set terminal length to zero for long replies, no pauses
print('--- Setting terminal length to 0')
session.sendline('terminal length 0')
result = session.expect('>')

# Run the 'show ip route' command on device
print('--- Successfully logged into device, running show ip route command')
session.sendline('show ip route')

# Wait for the command to complete and prompt to be ready
result = session.expect([pexpect.TIMEOUT, '>'])

if result == 0:
    print('Timeout while waiting for command to complete')
    exit()

# Display the output of the command, for comparison
print('--- Show ip route output:')
show_ip_route_output = session.before
print(show_ip_route_output)

# Rest of your code (processing routes, etc.)
# Create dictionary to hold information about the default gateway
default_gateway = {}

# Go through the list of routes to get routes per interface
for route in routes_list:
    OSPF_match = OSPF_pattern.search(route)
    
    if OSPF_match:
        # Check if it's the default gateway route
        if '0.0.0.0/0' in route:
            # Extract the default gateway information
            gateway_match = route_pattern.search(route)
            default_gateway['next-hop'] = gateway_match.group(1)
        else:
            # Match for GigabitEthernet interfaces
            intf_match = intf_pattern.search(route)

            # Check to see if we matched the GigabitEthernet interfaces string
            if intf_match:
                # Get the interfaces from the match
                intf = intf_match.group(2)

                # If route list not yet created, do so now
                if intf not in intf_routes:
                    intf_routes[intf] = []

                # Extract the prefix (destination IP address/subnet)
                prefix_match = prefix_pattern.search(route)
                prefix = prefix_match.group(1)

                # Extract the route
                route_match = route_pattern.search(route)
                next_hop = route_match.group(1)

                # Create dictionary for this this route,
                # and add it to the list
                route = {'prefix': prefix, 'next-hop': next_hop}
                intf_routes[intf].append(route)

# Display default gateway information
print('--- Default Gateway:')
pprint(default_gateway)
# Close the session
session.close()


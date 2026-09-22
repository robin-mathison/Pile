#!/usr/bin/env python3

# Echo server program
import socket

def get_ip_address():
    """
    Returns the local IP address of the machine. Works on Linux (unlike some stackoverflow answers...)
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) # ping google
    return s.getsockname()[0] # find IP address used to ping google

ip_addr = get_ip_address()
host_addr = (ip_addr, 50007) # host on an unused port

# hold a map from a short, easy to remember key to a list of actual keys
auth_keys = {'test_key1': ['spotify1', 'discord1', 'google1'], 'test_key2': ['spotify2', 'google2'], 'test_key3': ['google3']}

def parse_packet(data: str) -> str:
    data_split = data.split()

    if len(data_split) < 2 or len(data_split) > 3:
        return None # wrong number of strings in command

    cmd = data_split[0].decode('utf8') # convert bytes back to a string
    arg = data_split[1].decode('utf8')

    arg2 = None
    if len(data_split) == 3:
        arg2 = data_split[2].decode('utf8')

    print(f'got {cmd} and {arg}')

    if cmd == 'get_key':
        print(f'looking up key {arg}...')
        print(auth_keys)
        if arg in auth_keys.keys():
            print(f'key exists, returning auth keys')
            return auth_keys[arg]
        else:
            print(f'no key exists')
            return None
    elif cmd == 'set_key':
        print(f'setting value {arg2} for key {arg}')
        if arg in auth_keys:
            # append key to existing list
            auth_keys[arg].append(arg2)
        else:
            # new list of keys
            auth_keys[arg] = [arg2]
        return None
    else:
        print(f'unknown command!')
        return None

print(f'key server IP address: {ip_addr}')

while True:
    with socket.create_server(host_addr) as s: # create a TCP server bound to host_addr
        s.listen() # enable listening for the server
        conn, addr = s.accept()
        with conn:
            print(f'connected to client {addr}')
            while True:
                data = conn.recv(1024) # recieve 1kb of data (more than enough for us!)
                if not data:
                    break

                resp = parse_packet(data)
                conn.sendall(str(resp).encode())


#!/usr/bin/env python3

# Echo client program
import socket
import sys

def get_ip_address():
    """
    Returns the local IP address of the machine. Works on Linux (unlike some stackoverflow answers...)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) # ping google
    return s.getsockname()[0] # find IP address used to ping google

HOST = get_ip_address() # assuming that the server and the client are running on the same machine - replace with host IP address if not
PORT = 50007
s = None

# connect to the host
for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM):
    # res contains the information we need to set up a socket to talk to the host
    af, socktype, proto, canonname, sa = res

    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        print('could not open socket?')
        sys.exit(1)

    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        print('could not connect to host?')
        sys.exit(2)

with s:
    s.sendall(b'askldfkl;sdf')
    data = s.recv(1024)
    print('bad cmd response:', repr(data))

    s.sendall(b'get_key test_key1')
    data = s.recv(1024)
    print('existing key response:', repr(data))

    s.sendall(b'get_key bad_key')
    data = s.recv(1024)
    print('invalid key response:', repr(data))

    s.sendall(b'set_key new_key spotify45')
    data = s.recv(1024) # need to call recv() after sendall to actually send the request (even if we don't use the return value)
    s.sendall(b'set_key new_key other123')
    data = s.recv(1024)
    s.sendall(b'get_key new_key')
    data = s.recv(1024)
    print('new key response:', repr(data))


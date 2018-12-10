#!/usr/bin/env python

import socket

#-- Create Socket
# address family (AF) can be socket.AF_INET/AF_UNIX
# type can be socket.SOCK_STREAM/SOCK_DGRAM
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket !')
    sys.exit()

print('Socket created!')

#-- Get Host IP
host = 'www.google.com'
port = 80

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print('Hostname, ', host, ', can\'t be resolved, exiting')
    sys.exit()

#print('Get IP: ', remote_ip, ' for Host ,', host)

#-- Connect Host
try:
    print('Connecting host,', host, ' at ', remote_ip, ' port: ', port)
    s.connect((remote_ip, port))
except:
    print('Failed to connect host, ', host, ', exiting.')
    sys.exit()

#-- To get data from server
message = bytes("GET / HTTP/1.1\r\n\r\n".encode(encoding='ascii'))
print(message)
try:
    s.sendall(message)
except socket.error:
    print('Failed to send request to server.')
    sys.exit()

print('Message was sent successfully.')

#-- Receive data and print out
try:
    reply = s.recv(4096)
except:
    print('Failed to receive data from server.')
    s.close()

print(reply.decode(encoding='ascii'))
s.close()




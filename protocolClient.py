#Dylan Dockery
#Client to generate message and send it using a custom protocol. 
#libraries needed : socket, argparse, random
#instructions: 
#Start via commandline. Commandline parameters are as follows:
#-p --- Port used for server. Required 
#-m --- Message to be send via UDP with custom protocol

from socket import *
import argparse
import random
from header import *

    
#corrupts random byte of packet bar the first idnetifier byte
def corrurpPacket(packet):
    packet[random.randrange(1, 18, 1)]=random.randrange(0, 255, 1)
    return packet

#command line argmuent declaration
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('-i', type=str, default='127.0.0.1',help='IP address for server Default is 127.0.0.1')
parser.add_argument('-p', type=int, help='Port used for server. Required', required=True)
parser.add_argument('-m', type=str,help='Message to be sent to server', required=True)
args = parser.parse_args()
message = args.m
ip_addr = args.i
port = args.p

#protocol variables
SND=0
ACK=1
NACK=2
#initial sequence number
seq=1

#partition message longer than 8 characters into payloads of sixe 8 or less
payloads = [message[start:start+8] for start in range(0,len(message),8)]
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)
#send each payload across UDP connection
for p in payloads:
    packet = encode(port,p,SND,seq)
    while True: 
        try:
            #1 in 10 chance to corrupt packet
            corrupt_flag=random.randrange(0, 10, 1)
            if corrupt_flag == 1:
                packet=corrurpPacket(packet)
            clientSocket.sendto(packet,(ip_addr,port))
            response, serverAddress=clientSocket.recvfrom(2048)
            #resend packet until ACK
            while(response[6]==NACK):
                packet = encode(port,p,SND,seq)
                clientSocket.sendto(packet,(ip_addr,port))
                response, serverAddress=clientSocket.recvfrom(2048)
            #flip sequence numebr 
            seq=response[7]^1
            break

        #if timeout occurs resend packet
        except timeout:
            print("TO")
            pass
        




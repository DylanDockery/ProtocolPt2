#Dylan Dockery
#Server to process custom protocol and print out payload as buffer. Checks for data integrity and rerequests packet if corrupt
#libraries needed : socket, argparse, random, sys
#instructions: 
#Start via commandline. Commandline parameters are as follows:
#-p --- Port used for server. Required 

from socket import *
import argparse
import random
from sys import stdout
from header import *

#protocol numbers
ACK=1
NACK=2
#header indices
protocol_IND=0
seq_IND=7



#checks the integretiy of the pack by recalculating checksum and comparing
def integrityCheck(message):
    #partition packet into header and message snas check sum and message
    headerLength=8
    checkByte1=8
    checkByte2=9
    messageIndex=10
    packet_header=message[0:headerLength]
    packet_message=message[messageIndex:]

    check_sum1 = 0
    check_sum2 = 0

    for i in range(0,len(packet_header),2):
        check_sum1=check_sum1^packet_header[i]
        check_sum2=check_sum2^packet_header[i+1]

    for j in range(0,len(packet_message),2):
        check_sum1=check_sum1^packet_message[j]
        check_sum2=check_sum2^packet_message[j+1]

    if check_sum1 != message[checkByte1] or check_sum2 != message[checkByte2]:
        return True
    else:
        return False

#decodes message from received packet   
def decode(message):
    return message[10:message[1]].decode('utf-8')

#processes message to check for integrity and respond accordingly
def process(message):
    if integrityCheck(message):
        flag=NACK
    else:
        flag=ACK
        data=decode(message)
        print(data, end="")
        stdout.flush()
    #emulate s lost NACK and ACK packets
    drop_flag=random.randrange(0, 10, 1)
    if drop_flag != 1:
        response = encode(clientAddress[1],'', flag,message[seq_IND])
        serverSocket.sendto(response,clientAddress)
    return flag


#command line argmuent declaration
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('-p', type=int, default=8000,help='Port used for server. Required', required=True)
args = parser.parse_args()
port = args.p




serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',port))
print("The server is ready to receive")

#data store
client_port="-1"
prev_seq=0
prev_flag=NACK

while True:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)
        #reinitializes seq number on a new connection
        if clientAddress[1]!=client_port:
            client_port=clientAddress[1]
            prev_seq=0
        #emulates lost packets with SND flag from client to server
        drop_flag=random.randrange(0, 10, 1)
        if message[protocol_IND]==0 and drop_flag!=1:
            data=decode(message)
            #check for duplicate messages and processing
            duplicate= (prev_seq==message[seq_IND])
            if duplicate and prev_flag == ACK:
                response = encode(clientAddress[1],'', ACK ,message[seq_IND])
                serverSocket.sendto(response,clientAddress)
            else:
                prev_flag = process(message)
            
            prev_seq=message[seq_IND]

    except KeyboardInterrupt:
        break

print("Server offline")
        
        


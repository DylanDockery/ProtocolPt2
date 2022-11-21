# Protocol Assignment Part 2

Description:
This project is a server and client program that send a message over UDP with a custom protocol.
Protocol:
Identifier is the first bit with a 0
Flag options are SND, ACK, and NACK
Sequnce number alternates from 1 to 0 begining at 1
Check sum is calculated using a XOR on buytes 2 at a time
Also includes code to emulate packet loss on both sides of trnasit and packet corruptionj

Client arguements:
-i <IP> (address of the server) (optional) (default: 127.0.0.1)
-p <Port> (port of the UDP listener on the server) (required)
-m <message> (message to be sent to the server) (required)
-h (help message)
 
Server Arguements:
-p <Port> (port of the UDP listener on the server)(required)
-h (help message)

Instuctions:
 The server must be started before the client and the port must be set. Once server is started the client can be started and the port and message must be set. The IP address is optional but will default to 127.0.0.1 if none is given. 
  Not that if the message contains any spaces the whole message msut be enclosed in double quotation marks ""
  Client gives no out put but the server prints data as it is received. 
  To be launched from the command line using python3 command in Linuix or py in Windows.

 Areas of improvement:
 The processsing of the check sum may be able to be combined into a single loop than two consecutive.
 May be possible to do this in a manner where bytearrays are not used.

 

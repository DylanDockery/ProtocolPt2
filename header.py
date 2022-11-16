import random
#formats the packet in bytes Arguments: destination port, packet payload, protocol flag, sequence number
def encode(port, message,flag,seq):
    #packet
    protocol_header=bytearray()
    #protocol identifier
    protocol_header.append(0)
    #length of packet
    protocol_header.append((len(message)+10))
    #port and 2 bytes ro store it 
    port_bytes=port.to_bytes(2,'big')
    protocol_header.append(port_bytes[0])
    protocol_header.append(port_bytes[1])
    #random integer and 2 bytes to store it
    random_int=random.randrange(0, 65535, 1).to_bytes(2,'big')
    protocol_header.append(random_int[0])
    protocol_header.append(random_int[1])
    #protocol flag
    protocol_header.append(flag)
    #sequnece number
    protocol_header.append(seq)
    
    #if packet payload is less then 8 characters pad with 0s then encode as bytes
    if len(message)%8 != 0:
        message = message + '0' * (8-len(message)%8)
    protocol_message=message.encode('utf-8')

    #check sum calculation then stored as 2 bytes at end of header 
    check_sum1 = 0
    check_sum2 = 0
    
    for i in range(0,len(protocol_header),2):
        check_sum1=check_sum1^protocol_header[i]
        check_sum2=check_sum2^protocol_header[i+1]

    for j in range(0,len(protocol_message),2):
        check_sum1=check_sum1^protocol_message[j]
        check_sum2=check_sum2^protocol_message[j+1]
    protocol_header.append(check_sum1)
    protocol_header.append(check_sum2)

    #merge header and payload and return as packet
    packet=protocol_header+protocol_message
    return packet
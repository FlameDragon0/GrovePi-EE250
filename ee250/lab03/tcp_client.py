"""
Server IP is 52.88.20.156, ports are 5000-5008, socket is UNIX TCP 
Server receiver buffer is char[256]
If correct, the server will send a message back to you saying "I got your message"
Write your socket client code here in python
Establish a socket connection -> send a short message -> get a message back -> ternimate
"""
import socket

def main():
    
    # TODO: Create a socket and connect it to the server at the designated IP and port
    HOST = "34.209.114.30"
    #HOST = "52.88.20.156"
    PORT = 5008
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # AF_INET tells the program that it will use IPv4, and SOCK_STREAM says that the connection will use TCP protocol
        s.connect((HOST, PORT)) # Connects to the server through IPv4, which requires a 2-tuple (IP address and Port)
    
    # TODO: Get user input and send it to the server using your TCP socket
        info = input("Enter message you want to send: ")
        s.sendall(str.encode(info)) #str.encode() converts the input message into bytes of data with utf-8 encoding by default
    
    # TODO: Receive a response from the server and close the TCP connection
        data = s.recv(1024) # This allows the client to read up to 1024 bytes of data
        print("Received: " , repr(data)) 
        s.close() # Closes the connection with the server

if __name__ == '__main__':
    main()

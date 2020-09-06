/* A simple server in the internet domain using TCP
 * Answer the questions below in your writeup
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    /* 1. What is argc and *argv[]?
     *      argc tells the program the number of arguments that will be passed into the main function, and *argv[] is the array that contains these arguments. These arguments
            are passed to the program through the command line.
     */
    int sockfd, newsockfd, portno;
    /* 2. What is a UNIX file descriptor and file descriptor table?
     *      A UNIX file descriptor is an abstract indicator used to access a file or any sort of input/output resource. The first three file descritors on a standard UNIX OS are
            STDIN, STDOUT and STDERR. A file descriptor table records the mode in which a file has been opened (such as for reading or writing) and indexes into a third inode
            table which describes the files.
     */
    socklen_t clilen;

    struct sockaddr_in serv_addr, cli_addr;
    /* 3. What is a struct? What's the structure of sockaddr_in?
     *      A struct is a collection of variables under a single name. The struct sockaddr_in is a struct that stores an address family (such as AF_INET for IPv4) in sa_family, 
            a 16-bit port number to store the port value in sin_port, and a 32-bit number that stores the IP address in sin_addr. It also has another variable called sin_zero,
            however its value is normally NULL as it is not used.
     */
    
    int n;
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    /* 4. What are the input parameters and return value of socket()
     *      socket() has 3 input parameters: domain, type and protocl. Domain is an integer that determins the communication domain, such as AF_INET for IPv4 or AF_INET6 for IPv6.
            Type stores the communication type, such as SOCK_STREAM for TCP or SOCK_DGRAM for UDP. Protocol stores the internet protocol, which is 0.
     */
    
    if (sockfd < 0) 
       error("ERROR opening socket");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
             sizeof(serv_addr)) < 0) 
             error("ERROR on binding");
    /* 5. What are the input parameters of bind() and listen()?
     *      For bind, the first input parameter is sockfd which is a socket descriptor integer, the second is a custom struct that contains the socket address and port, and the third
            parameter is integer of the length of the second parameter. In listen, the first parameter is the same as that of bind, and the second parameter is an int called backlog
            which defines the maximum time length to which the queue for sockfd may grow.
     */
    
    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    
    while(1) {
        /* 6.  Why use while(1)? Based on the code below, what problems might occur if there are multiple simultaneous connections to handle?
        *       This infinte loop is used to keep on receiving requests from clients and attend to them. If there are multiple simultaneous connections, however, the program
                will only read the first information received by the client and move on to the next client without checking if the latter one had sent more information.
        */
        
	char buffer[256];
        newsockfd = accept(sockfd, 
                    (struct sockaddr *) &cli_addr, 
                    &clilen);
	/* 7. Research how the command fork() works. How can it be applied here to better handle multiple connections?
         *      fork() is a command that creates a "child process" which runs in parallel with the "parent process" (or main program). Whatever is called below fork is equally done
                by the child process, therefore if there were multiple requests from different clients, fork could be called based on the number of requests and attend to all of them.
         */
        
	if (newsockfd < 0) 
             error("ERROR on accept");
	bzero(buffer,256);
        
	n = read(newsockfd,buffer,255);
        if (n < 0) 
            error("ERROR reading from socket");
        //printf("Here is the message: %s\n",buffer);
        n = write(newsockfd,"I got your message",18);
        if (n < 0) 
            error("ERROR writing to socket");
        close(newsockfd);
    }
    close(sockfd);
    return 0; 
}
  
/* This program makes several system calls such as 'bind', and 'listen.' What exactly is a system call?
 *      A system call is a service request made by the program to the kernel. This kind of service is special as only the kernel can do it.
 */

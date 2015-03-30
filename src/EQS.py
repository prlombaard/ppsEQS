'''
@Author = Rudolph Lombaard
@Original URL = from Python docs / example

#Created Date = 29 March 2015
'''

# state of the EQS
# 0 -> Startup server and wait for incomming connection
# 0 -> 1 : Valid binding to HOST / PORT, incoming TCP connection on host / port
# 1 -> Waiting for valid logon
# 1 >- 2 : Valid logon received
# 2 -> Awaiting commands
# 2 -> 3: txmode

global state_EQS
global status_BITE

import SocketServer
import time

__EQS__VERSION__ = '1.00T01'

class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    supported_commands = ["<help>Returns a list of supported commands",
                          "<version>Returns version number of EQS", 
                          "<upper>returns the received string to the\
                          requestor with all characters in upper case", 
                          "<lower>returns the received string to the \
                          requestor with all characters in lower case",
                          "<set><txmode>Set the transmitter in a mode",
                          "<get><txmode>Returns the transmitter mode]"]

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        # TODO:make received data all lower case before testing
        if ("<upper>" in self.data):
            self.wfile.write(self.data.upper()[7:])
        if ("<lower>" in self.data):
            self.wfile.write(self.data.lower()[7:])
        if ("<version>" in self.data):
            self.wfile.write("[version][%s]\ndjambo" % __EQS__VERSION__)
        if ("<help>" in self.data):
            output = ""

            output += ("[help]%s\n" % "list of supported commands")
            
            for cmmnd in self.supported_commands:
                output += ("%s\n" % cmmnd)
            
            self.wfile.write(output)

# hostname to where server must bind listening socket. 127.0.0.1 or localhost
HOST_NAME = 'localhost'
# Port number to bind listening server socket to
PORT_NUMBER = 9995

if __name__ == "__main__":
    # TODO: Insert commandline parser, example input args EQS.py -host localhost -port 9999 -EQSuptime 30
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST_NAME, PORT_NUMBER), MyTCPHandler)

    # set Server timeout to 10seconds, ignored by server.server_forever()
    server.timeout = 10

    starttime = time.time()

    EQS_timeout = 0.5 * 60

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        # server TCP requests handled for x minutes then closes server, 
        # or when keyboard interrupt is received
        while time.time() - starttime < (0.5*60):
            # waits for one request to come in. handles ONLY one request
            server.handle_request()
        print "Server timed out after %d seconds" % (EQS_timeout)
    except KeyboardInterrupt:
        print "Server received KeyboardInterrupt."
        pass
    server.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)        
    
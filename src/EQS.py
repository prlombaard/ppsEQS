'''
@Author = Rudolph Lombaard
@Original URL = from Python docs / example

#Created Date = 29 March 2015
'''

# module imports
import SocketServer
import time
import string
from random import randint

def logout():
    global state_EQS

    print "state_EQS = [%d]" % state_EQS
    print "logging out"
    # Change state to 1, awaiting login request
    state_EQS = 1
    print "state_EQS = [%d]" % state_EQS    

class MyTCPHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    magic_number = 1234

    sessioncnt = 0

    # Dictionary that holds all valid commands for the EQS
    # TODO: Reasearch better method of making the commands
    #       getters and setters much more dynamic
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
        # Likewise, self.wfile is a file-like object used to write back to the client
        # TODO:make received data all lower case before testing
        global state_EQS

        print "state_EQS = [%d]" % state_EQS

        print "Magic Number[%d]" % magic_number

        # test what state EQS is in
        # test if EQS is in waiting valid loging request state
        if (state_EQS == 1):
            # awaiting login request in the form <username>admin<password>password
            # test if username and password is in received string
            if ("<username>" in self.data) and ("<password>" in self.data):
                # username and password tags received

                # Extract username from received string
                usr = self.data[string.find(self.data, ">") + 1:string.rfind(self.data,"<")]

                # Extract password from received string
                passwd = self.data[string.rfind(self.data, ">") + 1:]

                # TODO: Add debug info
                print ("Username: [%s]" % usr)
                print ("Password: [%s]" % passwd)

                # TODO: Update method for retrieving credentials safely, NOT using text openly
                # Test if username and password maches
                if (usr == username) and (passwd == password):
                    # Change state to 2, username and password matches, i.e. valid loging request received
                    state_EQS = 2

                    print "state_EQS = [%d]" % state_EQS

                    self.sessioncnt += 1

                    print "Session Count = [%d]" % self.sessioncnt

                    # TODO: choose better way of creating a magic number
                    self.magic_number = randint(0, 9999)

                    print "Magic Number = [%d]" % self.magic_number

                    # TODO: update the reponse messages to be read from conf, instead of hardcoded
                    # Send success response back to requestor
                    self.wfile.write("[login][successfull]\n")
                else:
                    # TODO: update the reponse messages to be read from conf, instead of hardcoded
                    # Send failed response back to requestor
                    self.wfile.write("[login][failed]\n")
        # test if EQS is waiting for commands state
        elif (state_EQS == 2):
            # awaiting commands from requestors
            if ("<upper>" in self.data):
                self.wfile.write(self.data.upper()[7:])
            if ("<lower>" in self.data):
                self.wfile.write(self.data.lower()[7:])
            if ("<version>" in self.data):
                self.wfile.write("[version][%s]" % __EQS__VERSION__)
            if ("<help>" in self.data):
                output = ""

                output += ("[help]%s\n" % "list of supported commands")
                for cmmnd in self.supported_commands:
                    output += ("%s\n" % cmmnd)
                self.wfile.write(output)
            if ("logout" in self.data):
                # Logout the current session
                logout()
                self.wfile.write("[logout][%s]\n" % "successfull")

if __name__ == "__main__":
    # TODO: Insert commandline parser, example input args EQS.py -host localhost -port 9999 -EQSuptime 30

    # EQS module variables
    # Version of this EQS
    __EQS__VERSION__ = '1.00T01'

    # hostname to where server must bind listening socket. 127.0.0.1 or localhost
    HOST_NAME = 'localhost'
    # Port number to bind listening server socket to
    PORT_NUMBER = 9995


    # state of the EQS
    # -1 -> Pre-Startup
    # -1 -> 0 : Sucesfull init of the module
    # 0 -> Startup server and wait for incomming connection
    # 0 -> 1 : Valid binding to HOST / PORT, incoming TCP connection on host / port
    # 1 -> Awaiting valid logon request <username>username<password>password
    # 1 >- 2 : Valid logon received
    # 2 -> Awaiting commands
    # 2 -> 3: txmode
    state_EQS = -1

    # status BITE for the EQS
    status_BITE = 0

    # Process variable to hold created pifm process
    fm_process = None

    # user details
    # TODO: save the credentials using hash algorithms, NOT as clear test
    username = "root"
    password = "password"

    # change state to 0, sucessfull module init
    state_EQS = 0

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST_NAME, PORT_NUMBER), MyTCPHandler)

    #change state to 1, successfull binding of listening server socket
    state_EQS = 1

    # set Server timeout to 10seconds, ignored by server.server_forever()
    server.timeout = 10

    # get current system time
    starttime = time.time()

    EQS_timeout = 0.5 * 60

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        # server TCP requests handled for x minutes then closes server
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

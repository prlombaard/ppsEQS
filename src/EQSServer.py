"""
@Author = Rudolph Lombaard
@Original URL = from Python docs / example

#Created Date = 30 March 2015
"""

# module imports
import SocketServer
import time
import logging

class EQSServer(object):
    """
    An EQS Server class that creates the correct StreamRequestHandler to handle TCP requests.
    The class also implements a statemachine to keep track of where the sessions' state is

    """
    # Version of this EQS Server class
    version = '1.00T01'


    def __init__(self, arghostname='localhost', argportnumber=9995, argtimeout=(0.5*60)):
        """
        EQSServer constructor method gets called when class is instantiated
        """
        logging.info("ENTER:EQSServer:__init__")

        logging.info("Calling super:EQSServer:__init__")

        super(EQSServer, self).__init__()

        logging.info("Setting default instance variable:EQSServer:__init__")

        self.set_watchdog_timeout(argtimeout)

        # hostname to where server must bind listening socket. 127.0.0.1 or localhost
        self.host_name = arghostname
        # Port number to bind listening server socket to
        self.port_number = argportnumber

        # state of the EQS Server
        # -1 -> Pre-Startup
        # -1 -> 0 : Sucesfull init of the module
        # 0 -> Startup server and wait for incomming connection
        # 0 -> 1 : Valid binding to HOST / PORT, incoming TCP connection on host / port
        # 1 -> Awaiting valid logon request <username>username<password>password
        # 1 >- 2 : Valid logon received
        # 2 -> Awaiting commands
        # 2 -> 3: txmode
        self.set_state(-1)

        # status BITE for the EQS
        self.status_BITE = 0

        # Process variable to hold created pifm process
        self.fm_process = None

        # user details
        # TODO: save the credentials using hash algorithms, NOT as clear test
        self.username = "root"
        self.password = "password"

        logging.info("Setting host name   = [%s]:EQSServer:__init__" % self.host_name)
        logging.info("Setting port number = [%d]:EQSServer:__init__" % self.port_number)
        logging.info("Setting server time out = [%d]:EQSServer:__init__" % self.get_watchdog_timeout())        

        # change state to 0, sucessfull module init
        self.set_state(0)

    def get_watchdog_timeout(self):
        """
        returns watchdog timeout variable
        """
        return self.watchdog_timeout

    def set_watchdog_timeout(self, newtimeout):
        """
        sets watchdog timeout variable
        """
        self.watchdog_timeout = newtimeout

    def get_state(self):
        """
        returns state variable
        """
        return self.state

    def set_state(self, newstate):
        """
        sets state variable
        """
        self.state = newstate
        logging.info("Changing state to[%d]:EQSServer:set_state" % (newstate))

    def run(self):
        """
        main entry point that enables the EQS server to run and start accepting connection and handle requests
        """
        logging.info("ENTER:EQSServer:run")

        logging.info("Creating Server Socket to bind at hostname=[%s] port number=[%d]:EQSServer:run" % (self.host_name, self.port_number))

        # Create the server, binding to localhost on port 9999
        self.socketserver = SocketServer.TCPServer((self.host_name, self.port_number), MyTCPHandler)

        # set Server timeout to newtimeout seconds, ignored by server.server_forever()
        self.socketserver.timeout = self.get_watchdog_timeout()

        #change state to 1, successfull binding of listening server socket
        self.set_state(1)

        # get current system time
        self.eqs_starttime = time.time()

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        logging.info("%s Server Starts - %s:%s" % (time.asctime(), self.host_name, self.port_number))

        try:
            # server TCP requests handled for x minutes then closes server
            # or when keyboard interrupt is received
            while time.time() - starttime < (self.get_watchdog_timeout()):
                # waits for one request to come in. handles ONLY one request
                self.socketserver.handle_request()
            print "Server timed out after %d seconds" % (self.get_watchdog_timeout())
        except KeyboardInterrupt:
            print "Server received KeyboardInterrupt."
            pass
        logging.info("Closing Server Socket:EQSServer:run")
        self.socketserver.server_close()
        logging.info("%s Server Stop - %s:%s" % (time.asctime(), self.host_name, self.port_number))

        logging.info("EXIT:EQSServer:run")

def logout():
    global state_EQS

    print "state_EQS = [%d]" % state_EQS
    print "logging out"
    # Change state to 1, awaiting login request
    state_EQS = 1
    print "state_EQS = [%d]" % state_EQS    

if __name__ == "__main__":
    logging.info("Running EQSServer.py as script")
    print("Running EQSServer.py as script")
    pass
    # TODO: Insert commandline parser, example input args EQS.py -host localhost -port 9999 -EQSuptime 30

    #TODO: Insert test code here when module is called by itself.

    # Create EQSServer instance
    #server = EQSServer()
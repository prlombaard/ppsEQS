'''
@Author = Rudolph Lombaard

#Created Date = 30 March 2015
'''
import logging
import time


class EQSApp(object):
    """
    An EQS Application class that creates the correct server to handle TCP requests.
    """

    def __init__(self, argtimeout=(0.25 * 60)):
        logging.info("ENTER:EQSApp:__init__")

        logging.info("Calling super:EQSApp:__init__")

        super(EQSApp, self).__init__()

        logging.info("Setting variables to default values:EQSApp:__init__")

        # Set internal variables to known default states
        self.set_watchdog_timeout(argtimeout)

        logging.info("ENTER:EQSApp:__init__")

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

    def main(self):
        """
        #besides __init__ this method is the main entry point for this instance
        """
        logging.info("ENTER:EQSAppClass")

        logging.info("Application starts - %s" % time.asctime())

        # get current system time
        starttime = time.time()

        try:
            while (time.time() - starttime) < (self.get_watchdog_timeout()):
                pass
        except KeyboardInterrupt:
            print "Application received KeyboardInterrupt."

        logging.info("Application stops - %s" % time.asctime())

        logging.info("EXIT:EQSAppClass")

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    logging.info("ENTER:EQSapp.py")

    logging.info("Creating Application Object")

    app = EQSApp()

    logging.info("Calling EQSapp.main()")

    app.main()

logging.info("EXIT:EQSapp.py")

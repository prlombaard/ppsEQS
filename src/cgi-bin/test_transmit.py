#!/usr/bin/env python

import cgitb
import cgi
import logging
from string import Template

#create logging and set output to to CONSOLE
#logger = logging.getLogger('test_transmit.py')
#logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)

# create formatter
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
#ch.setFormatter(formatter)

# add ch to logger
#logger.addHandler(ch)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logging.info("CGIScript test_transmit.py")
logging.info("Enabling cgitb")
cgitb.enable()


#output header
logging.info("printing header")
print "Content-type: text/html"
print

#must include a blank line aka print statement to end the header


#output start of HTML code
#output Title of the HTML page
logging.info("printing TITLE")
print "<TITLE>CGI script output</TITLE>"

#get form values from the filled in HTML page
logging.info("Reading values from cgi.FieldStorage()")
form = cgi.FieldStorage()

#print BODY
logging.info("printing body")
print "<html><body>"
print "<h1>Logging Mode:</h1>"

#template = Template("<html><body><h1>Logging Mode = ${logging_mode}</h1></body></html>")
#print template.substitute(dict(logging_mode=form["logging_mode"].value))

logging.info("Determining what logging should be set to")

#TODO:push a arg from the webpage request to control logging of cgi script
if (form["logging_mode"].value == 'logging append'):
    logfile = "cgiscript.log"
    logging.info("Logging set to append to log file [%s]" % logfile)
    logging.info("Logging messages will be output to log file ONLY, after this refer to log file")
    #create logging and set output to append to filename
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename = logfile, level=logging.DEBUG)
    #logging.debug('This message should go to the log file')
    logging.info('Start of Logging in test_transmit.py')
    
    print "<h2>%s</h2>" % "Logging on, Appending to file"
    
if (form["logging_mode"].value == 'logging rewrite'):
    logfile = "cgiscript.log"
    logging.info("Logging set to rewrite to log file [%s]" % logfile)
    logging.info("Logging messages will be output to log file ONLY, after this refer to log file")
    #create blank log file
    #f = open("example.log", mode = 'w')
    #f.close()

    #create logging and set output to to filename
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode = 'w', filename = logfile, level=logging.DEBUG)

    #logging.debug('This message should go to the log file')
    logging.info('Start of Logging in test_transmit.py')
    
    print "<h2>%s</h2>" % "Logging on, Starting new log file"    


if (form["logging_mode"].value == 'logging off'):
    logging.info("Logging set to output to console only not a file")
    logging.info("Logging messages will be output to CONSOLE ONLY")

    #logging is turned off. So logging will only output to console

    #create logging and set output to to CONSOLE
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    
    logging.info("Logging set to output to console only")

    #logging.debug('This message should go to the log file')
    logging.info('Start of Logging in test_transmit.py: CONSOLE ONLY')
    
    print "<h2>%s</h2>" % "Logging off, output of CGI scripts routes to CONSOLE only"
    print "<h3>%s</h3>" % "CONSOLE = Terminal where the CGIServer python script is running"

#if "custname" not in form or "custtel" not in form:
#if "custname" not in form:
#    print "<H1>Error</H1>"
#    print "Please fill in the name and addr fields."
#    #return
    
#print "<p>name:", form["custname"].value
#print "<p>custtel:", form["custtel"].value

#TODO:test mode values if not correct log a warning
logging.debug('Values from form')
logging.debug('Transmitter Mode      : %s', form["mode"].value)
logging.debug('Logging Mode          : %s', form["logging_mode"].value)
logging.debug('Fixed Frequency Start : %s', form["fixedstart"].value)
logging.debug('Fixed Frequency Stop  : %s', form["fixedstop"].value)
logging.debug('Hopper delay          : %s', form["hopdelay"].value)
logging.debug('Sweep Frequency Start : %s', form["sweepstart"].value)
logging.debug('Sweep Frequency Start : %s', form["sweepstop"].value)

print "<h1>Transmitter Mode:</h1>"
#test mode
if (form["mode"].value == 'fixed freq'):
    
    logging.debug('requested mode = fixed frequency')
    logging.debug('call test transmit app with fixed frequency args')
    #TODO:test fixed frequency values if not correct log a warning
    fstart = form["fixedstart"].value
    logging.debug('Fixed Frequency = %d [Hz]', int(fstart))
    logging.debug('Fixed Frequency = %0.2f [kHz]', int(fstart)/1000)
    logging.debug('Fixed Frequency = %0.2f [MHz]', int(fstart)/1000.0/1000.0)
    
    print "<h2>%s</h2>" % "Fixed frequency"

    
if (form["mode"].value == 'sweep freq'):
    logging.debug('requested mode = frequency sweep')
    logging.debug('call test transmit app repeatedly and sweep through frequencies')
    #TODO:test sweep frequency values if not correct log a warning
    fstart = form["sweepstart"].value
    fstop  = form["sweepstop"].value
    logging.debug('Sweep Frequency Start= %d [Hz]', int(fstart))
    logging.debug('Sweep Frequency Stop = %d [Hz]', int(fstop))
    
    print "<h2>%s</h2>" % "Frequency Sweep"

if (form["mode"].value == 'freq hop'):
    logging.debug('requested mode = frequency hop')
    logging.debug('call test transmit app and randomly hop in frequencies')
    #TODO:test hopper frequency values if not correct log a warning
    fstart = form["fixedstart"].value
    fstop  = form["fixedstop"].value
    fdelay  = form["hopdelay"].value
    logging.debug('Hopper Frequency Start= %d [Hz]', int(fstart))
    logging.debug('Hopper Frequency Stop = %d [Hz]', int(fstop))
    logging.debug('Hopper Delay          = %d [ms]', int(fdelay))
    
    print "<h2>%s</h2>" % "Frequency Hopper"
    
#print end of BODY and en of HTML
print "</html></body>"
    
logging.info('End of Logging in test_transmit.py')

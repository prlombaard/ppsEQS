# ppsEQS

# README #

This Python script pings an IP address continously. After a predetermined time the ping process stops. The data from the ping responses is collected and graphed.

Before the script finishes with execution it writes the contents of the graph to a PNG file as well as CSV containing the ping responses.

### What is this repository for? ###

* Quick summary
	* Ping script that nicely graphs the response times.
	* Example. Usage: python ping -ip www.google.com -time 10
	* Help Example  : python ping --help
* Version
	* Beta 1.0

### How do I get set up? ###

* Summary of set up
	* Clone the repository to your local drive.
* Configuration
* Dependencies
	* OS - Windows.
	* Needs a stable internet connection.
  	* Python Libraries
  		* Matplotlib (installed via Python(x,y))
* Database configuration
	* No database configurtion required
* How to run tests
	* Use the --test argument when calling the script from commandline.
	* Help Example  : python ping --test
* Deployment instructions


### Contribution guidelines ###

* Writing tests
	* Script was only tested in Window and as such the stability on another platform cannot be confirmed.
* Code review
	* The code is written in a style that tries to conform to the PEPXYZ standard. pylint or similar should be used to check the codes' formatting.
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
	* Owner of this repo is Rudolph Lombaard aka Rakker (prlombaard@gmail.com)
* Other community or team contact

import subprocess

# this function will return a list of lists describing the list of devices in the network
# format: [IP, MAC, NAME/MANUFACTURER]
# find out interface by running ifconfig and determining which interface is being used, like eth0 or wlp3s0
def scanner(INTERFACE):
	# use subprocess.run to run the command 
	cliOutput = subprocess.run(['arp-scan', '--interface=%s' %INTERFACE, '--localnet'], stdout=subprocess.PIPE)
	# extract the output from the subprocess
	strOutput = cliOutput.stdout.decode()
	# generate a list of lists in the specified format and return it
	return [i.split('\t') for i in strOutput('\n')][2:-4]

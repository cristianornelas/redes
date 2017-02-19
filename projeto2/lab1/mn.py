import time
from time import sleep, time
import termcolor as T
import os
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, info, setLogLevel
from mininet.util import dumpNodeConnections, quietRun, moveIntf
from mininet.node import Switch, OVSKernelSwitch, Node
 
def main():
	os.system("mn -c >/dev/null 2>&1")
	os.system("killall -9 zebra bgpd > /dev/null 2>&1")


	net = Mininet()
	c0 = net.addController()
	s1 = net.addSwitch("s1")
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")
	net.addLink(h1, s1)
	net.addLink(h2, s1)

        s1.cmd("sysctl -w net.ipv4.ip_forward=1")
	print "Wait 3 seconds"
	sleep(3)
        print "Configuring router"
	s1.cmd("/usr/lib/quagga/zebra -f conf/s1.conf -d -i /tmp/zebraS1.pid > S1-zebra-stdout 2>&1")

	net.start()

	h1.cmd("ifconfig h1-eth0 10.0.1.2/24")
	h1.waitOutput()
	h1.cmd("route add default gw 10.0.1.1")
	h1.waitOutput()

	h2.cmd("ifconfig h2-eth0 10.0.3.2/24")
	h2.waitOutput()
	h2.cmd("route add default gw 10.0.3.1")
	h2.waitOutput()

	#net.start()
	CLI(net)
	net.stop()
	os.system("killall -9 zebra bgpd")

if __name__ == "__main__":
	main()

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
	
	r1 = net.addSwitch("r1")
	s1 = net.addSwitch("s1")
	s2 = net.addSwitch("s2")
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")
	h3 = net.addHost("h3")
	h4 = net.addHost("h4")

	net.addLink(r1, s1)
	net.addLink(r1, s2)
	
	net.addLink(s1, h1)
	net.addLink(s1, h2)
	net.addLink(s2, h3)
	net.addLink(s2, h4)

	r2 = net.addSwitch("r2")
	s3 = net.addSwitch("s3")
	s4 = net.addSwitch("s4")
	h5 = net.addHost("h5")
	h6 = net.addHost("h6")
	h7 = net.addHost("h7")
	h8 = net.addHost("h8")

	net.addLink(r2, s3)
	net.addLink(r2, s4)
	
	net.addLink(s3, h5)
	net.addLink(s3, h6)
	net.addLink(s4, h7)
	net.addLink(s4, h8) 
	
	r3 = net.addSwitch("r3")
	s5 = net.addSwitch("s5")
	s6 = net.addSwitch("s6")
	h9 = net.addHost("h9")
	h10 = net.addHost("h10")
	h11 = net.addHost("h11")
	h12 = net.addHost("h12")

	net.addLink(r3, s5)
	net.addLink(r3, s6)
	
	net.addLink(s5, h9)
	net.addLink(s5, h10)
	net.addLink(s6, h11)
	net.addLink(s6, h12) 

	r1.cmd("sysctl -w net.ipv4.ip_forward=1")
        r2.cmd("sysctl -w net.ipv4.ip_forward=1")
	r3.cmd("sysctl -w net.ipv4.ip_forward=1")
	print "Wait 3 seconds"
	sleep(3)

	net.start()

	#net.start()
	CLI(net)
	net.stop()
	os.system("killall -9 zebra bgpd")

if __name__ == "__main__":
	main()

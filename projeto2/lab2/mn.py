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

	net = Mininet()
	c0 = net.addController()
	s1 = net.addSwitch("s1")
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")
	net.addLink(h1, s1)
	net.addLink(h2, s1)

	s2 = net.addSwitch("s2")
	h3 = net.addHost("h3")
	h4 = net.addHost("h4")
	net.addLink(h3, s2)
	net.addLink(h4, s2)

	net.addLink(s1, s2)

        s1.cmd("sysctl -w net.ipv4.ip_forward=1")
	s2.cmd("sysctl -w net.ipv4.ip_forward=1")
	print "Wait 3 seconds"
	sleep(3)

	net.start()

	CLI(net)
	net.stop()

if __name__ == "__main__":
	main()

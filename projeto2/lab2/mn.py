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

	h1.cmd("ifconfig h1-eth0 10.0.0.1/24")
	h1.waitOutput()
	h2.cmd("ifconfig h2-eth0 10.0.0.2/24")
	h2.waitOutput()

	h1.cmd("route add default gw 10.0.0.254 h1-eth0")
	h1.waitOutput()
	h2.cmd("route add default gw 10.0.0.254 h2-eth0")
	h2.waitOutput()

	h3.cmd("ifconfig h3-eth0 20.0.0.1/24")
	h3.waitOutput()
	h4.cmd("ifconfig h4-eth0 20.0.0.2/24")
	h4.waitOutput()

	h3.cmd("route add default gw 20.0.0.254 h3-eth0")
	h3.waitOutput()
	h4.cmd("route add default gw 20.0.0.254 h4-eth0")
	h4.waitOutput()

	s1.cmd("ifconfig s1:0 10.0.0.254")
	s2.cmd("ifconfig s2:0 20.0.0.254")	

	CLI(net)
	net.stop()

if __name__ == "__main__":
	main()

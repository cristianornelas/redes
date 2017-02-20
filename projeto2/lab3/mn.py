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


	#Inicia o objeto mininet
	net = Mininet()

	#Cria o controlador
	c0 = net.addController()
	
	#Cria o roteador da primeira subrede
	r1 = net.addSwitch("r1")

	#Cria os switches da primeira subrede
	s1 = net.addSwitch("s1")
	s2 = net.addSwitch("s2")

	#Cria os hosts da primeira subrede
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")
	h3 = net.addHost("h3")
	h4 = net.addHost("h4")

	#Cria os links entre os switches e o roteador da primeira subrede
	net.addLink(r1, s1)
	net.addLink(r1, s2)
	
	#Cria os links entre os switches e os hosts da primeira subrede
	net.addLink(s1, h1)
	net.addLink(s1, h2)
	net.addLink(s2, h3)
	net.addLink(s2, h4)

	#Cria o roteador da segunda subrede
	r2 = net.addSwitch("r2")

	#Cria os switches da segunda subrede
	s3 = net.addSwitch("s3")
	s4 = net.addSwitch("s4")

	#Cria os hosts da segunda subrede
	h5 = net.addHost("h5")
	h6 = net.addHost("h6")
	h7 = net.addHost("h7")
	h8 = net.addHost("h8")

	#Cria os links entre os switches e o roteador da segunda subrede
	net.addLink(r2, s3)
	net.addLink(r2, s4)
	
	#Cria os links entre os switches e os hosts da segunda subrede
	net.addLink(s3, h5)
	net.addLink(s3, h6)
	net.addLink(s4, h7)
	net.addLink(s4, h8) 

	#Cria o roteador da terceira subrede
	r3 = net.addSwitch("r3")

	#Cria os switches da terceira subrede
	s5 = net.addSwitch("s5")
	s6 = net.addSwitch("s6")

	#Cria os hosts da terceira subrede
	h9 = net.addHost("h9")
	h10 = net.addHost("h10")
	h11 = net.addHost("h11")
	h12 = net.addHost("h12")

	#Cria os links entre os switches e o roteador da terceira subrede
	net.addLink(r3, s5)
	net.addLink(r3, s6)
	
	#Cria os links entre os switches e os hosts da terceira subrede
	net.addLink(s5, h9)
	net.addLink(s5, h10)
	net.addLink(s6, h11)
	net.addLink(s6, h12) 

	#Ativa o ip_forward entre os dois switches das duas subredes e espera as mudancas terem efeito
	r1.cmd("sysctl -w net.ipv4.ip_forward=1")
    r2.cmd("sysctl -w net.ipv4.ip_forward=1")
	r3.cmd("sysctl -w net.ipv4.ip_forward=1")
	print "Wait 3 seconds"
	sleep(3)

	#Inicia a rede
	net.start()

	#Inicia o CLI
	CLI(net)

	#Para a rede
	net.stop()
	os.system("killall -9 zebra bgpd")

if __name__ == "__main__":
	main()

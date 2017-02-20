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

	#Inicia o objeto mininet
	net = Mininet()

	#Cria o controlador
	c0 = net.addController()

	#Cria o roteador da primeira subrede
	s1 = net.addSwitch("s1")

	#Cria os dois hosts da primeira subrede
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")

	#Cria os links entre os hosts e o switch da primeira subrede
	net.addLink(h1, s1)
	net.addLink(h2, s1)

	#Cria o roteador da segunda subrede
	s2 = net.addSwitch("s2")
	
	#Cria os dois hosts da segunda subrede
	h3 = net.addHost("h3")
	h4 = net.addHost("h4")

	#Cria os links entre os hosts e o switch da segunda subrede
	net.addLink(h3, s2)
	net.addLink(h4, s2)

	#Cria o link entre os dois switches das duas subredes
	net.addLink(s1, s2)

	#Ativa o ip_forward nos switches e espera 3 segundos para que as mudancas tenham efeito
	s1.cmd("sysctl -w net.ipv4.ip_forward=1")
	s2.cmd("sysctl -w net.ipv4.ip_forward=1")
	print "Wait 3 seconds"
	sleep(3)

	#Inicia a rede
	net.start()

	#Configura o endereco ip dos hosts da primeira subrede
	h1.cmd("ifconfig h1-eth0 10.0.0.1/24")
	h1.waitOutput()
	h2.cmd("ifconfig h2-eth0 10.0.0.2/24")
	h2.waitOutput()

	#Configura o gateway padrao dos hosts da primeira subrede
	h1.cmd("route add default gw 10.0.0.254 h1-eth0")
	h1.waitOutput()
	h2.cmd("route add default gw 10.0.0.254 h2-eth0")
	h2.waitOutput()

	#Configura o endereco ip dos hosts da segunda subrede
	h3.cmd("ifconfig h3-eth0 20.0.0.1/24")
	h3.waitOutput()
	h4.cmd("ifconfig h4-eth0 20.0.0.2/24")
	h4.waitOutput()

	#Configura o gateway padrao dos hosts da primeira subrede
	h3.cmd("route add default gw 20.0.0.254 h3-eth0")
	h3.waitOutput()
	h4.cmd("route add default gw 20.0.0.254 h4-eth0")
	h4.waitOutput()

	#Cria as interfaces para as subredes em seus respectivos switches
	s1.cmd("ifconfig s1:0 10.0.0.254")
	s2.cmd("ifconfig s2:0 20.0.0.254")	

	#Abre o CLI
	CLI(net)

	#Para a rede
	net.stop()

if __name__ == "__main__":
	main()

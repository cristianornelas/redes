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

	#inicia o objeto mininet
	net = Mininet()

	#Cria o controlador
	c0 = net.addController()

	#Cria o roteador
	s1 = net.addSwitch("s1")

	#Cria os dois hosts
	h1 = net.addHost("h1")
	h2 = net.addHost("h2")

	#Cria os links entre os hosts e os switches
	net.addLink(h1, s1)
	net.addLink(h2, s1)

	#Ativa o ip_forward no switch e espera 3 segundos para que as mudancas tenham efeito
    s1.cmd("sysctl -w net.ipv4.ip_forward=1")
	print "Wait 3 seconds"
	sleep(3)

	#Inicia a rede e abre o CLI
	net.start()
	CLI(net)

	#Para a rede
	net.stop()

if __name__ == "__main__":
	main()

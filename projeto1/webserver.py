#!/usr/bin/python

import cgi, cgitb, ipaddress, binascii, time
from bitstring import BitArray
from socket import *
cgitb.enable()

#Autor: Cristiano Ornelas 
#Bibliografia: http://www.feng.pucrs.br/~stemmer/processadores2/trab2-2012-2/crc.html (Acesso em 5 dez-2016)

def crc16(data):

        crcpolInv = BitArray(bin='10100000000000011')
        crc = BitArray(bin='00000000000000000')

        #print 'CRC anterior(inicial):                  {0}'.format(niceBin(crc))

        #print niceBin(data)

        while len(data) > 0:
                #1. PEGAR UM BYTE DA MENSAGEM
                byte = BitArray(bin='000000000')
                byte.append(data[:8])
                del data[:8]
                #print niceBin(byte)
                #print niceBin(data)

                #print 'Byte da mensagem:                       {0}'.format(niceBin(byte))

                #2. FAZER UM XOR DESTE BYTE VALOR CORRENTE DO CRC
                for i in reversed(range(17)):
                        crc[i] = byte[i] ^ crc[i]

                #print 'Xor com o CRC anterior:                 {0}'.format(niceBin(crc))

                #3. REPETIR 8 vezes
                for i in range(8):
                        #print '---------------------------------------------------------------'
                        #3.1. SE O BIT MAIS DA DIREITA DO CRC ATUAL FOR 1
                        if crc[16] == 1:
                                #print 'Bit da direita eh 1:'
                                #print 'Pegar CRCPOL refletido:                 {0}'.format(niceBin(crcpolInv))
                                #3.1. FAZER XOR COM POLINOMIO DE CRC REFLETIDO
                                for j in reversed(range(17)):
                                        crc[j] = crcpolInv[j] ^ crc[j]

                                #print 'Fazer xor:                              {0}'.format(niceBin(crc))
                        #else:
                                #print 'Bit da direita eh 0:'
                        #3.2. DESLOCAR O VALOR CORRENTE CRC 1 BIT PRA DIREITA
                        crc = crc >> 1
                        #print 'Deslocar para a direita:                {0}'.format(niceBin(crc))
                        #print '---------------------------------------------------------------'


        del crc[0]
        return crc


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head><title> My first CGI Program</title></head>"
print "<body>"

form = cgi.FieldStorage()

cmd1 = {}
cmd2 = {}
cmd3 = {}

counter1 = 0
counter2 = 0
counter3 = 0

output1 = 'Maquina 1<br><br>'
output2 = 'Maquina 2<br><br>'
output3 = 'Maquina 3<br><br>'


#Definicao dos valores fixos do cabecalho
VERSION = BitArray(int=2, length=4)
IHL = BitArray(int=5, length=4)
TYPEOFSERVICE = BitArray(int=0, length=8)
FLAGS = BitArray(int=0, length=3)
OFFSET = BitArray(int=0, length=13)
TIMETOLIVE = BitArray(int=127, length=8)
SOURCE = BitArray(bin(int(ipaddress.IPv4Address(u'192.168.56.101'))))
DESTINATION = BitArray(int=int(ipaddress.IPv4Address(u'127.0.0.1')), length=32)

#Maquina 1
if form.getvalue('maq1_ps'):
	cmd1[1] = form.getvalue('maq1-ps')
if form.getvalue('maq1_df'):
	cmd1[2] = form.getvalue('maq1-df')
if form.getvalue('maq1_finger'):
	cmd1[3] = form.getvalue('maq1-finger')
if form.getvalue('maq1_uptime'):
	cmd1[4] = form.getvalue('maq1-uptime')
#Maquina 2
if form.getvalue('maq2_ps'):
        cmd2[1] = form.getvalue('maq2-ps')
if form.getvalue('maq2_df'):
        cmd2[2] = form.getvalue('maq2-df')
if form.getvalue('maq2_finger'):
        cmd2[3] = form.getvalue('maq2-finger')
if form.getvalue('maq2_uptime'):
        cmd2[4] = form.getvalue('maq2-uptime')
#Maquina 3
if form.getvalue('maq3_ps'):
        cmd3[1] = form.getvalue('maq3-ps')
if form.getvalue('maq3_df'):
        cmd3[2] = form.getvalue('maq3-df')
if form.getvalue('maq3_finger'):
        cmd3[3] = form.getvalue('maq3-finger')
if form.getvalue('maq3_uptime'):
        cmd3[4] = form.getvalue('maq3-uptime')

for x in cmd1:
	msg = BitArray()
        IDENTIFICATION = BitArray(int=counter1, length=16)
        PROTOCOL = BitArray(int=int(x), length=8)
        if cmd1[x] != None:
		hexa = binascii.hexlify(cmd1[x])
		OPTIONS = BitArray(hex=hexa)
	else:
		OPTIONS = BitArray()
        CHECKSUM = BitArray(int=0, length=16)
        counter1 += 1
	
	serverName = '127.0.0.1'
	serverPort = 3001
	
	#Calcula qnts bits serao necessarios para que OPTIONS
	#tenha um tamanho multiplo de 32
	if len(OPTIONS) != 0:
		resto = len(OPTIONS) % 32
		complete = 32 - resto
		#Completa OPTIONS com o 0s de forma que este seja multiplo
		#de 32 bits
		for i in range(0, complete):
			OPTIONS.prepend('0b0')
	
		TOTALLENGTH = BitArray(int=5 * 32 + len(OPTIONS), length=16)
	else:
		TOTALLENGTH = BitArray(int = 5 * 32, length=16)	


	#Concatena todos os valores para calcular o CRC16
	#Ate aqui checksum eh 0, seguindo wikipedia
        msg.append(VERSION)
        msg.append(IHL)
        msg.append(TYPEOFSERVICE)
        msg.append(TOTALLENGTH)
        msg.append(IDENTIFICATION)
        msg.append(FLAGS)
        msg.append(OFFSET)
        msg.append(TIMETOLIVE)
        msg.append(PROTOCOL)
        msg.append(CHECKSUM)
        msg.append(SOURCE)
        msg.append(DESTINATION)

	#Caucula e atualiza o checksum
	CHECKSUM = crc16(msg)

	#Cria e concatena todos os valores do header incluindo OPTIONS
	#para enviar o socket
	msg = BitArray()
        msg.append(VERSION)
        msg.append(IHL)
        msg.append(TYPEOFSERVICE)
        msg.append(TOTALLENGTH)
        msg.append(IDENTIFICATION)
        msg.append(FLAGS)
        msg.append(OFFSET)
        msg.append(TIMETOLIVE)
        msg.append(PROTOCOL)
        msg.append(CHECKSUM)
        msg.append(SOURCE)
        msg.append(DESTINATION)
	if len(OPTIONS) != 0:
		msg.append(OPTIONS)
	
	#Cria um socket tcp para serverName e serverPort
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	
	try:
		#Envia a msg
		clientSocket.sendall(msg.bin.encode())
	
		#Concatena os bits da resposta em uma string
		string = ''
		parte = clientSocket.recv(32).decode()
		string += parte

		TOTALLENGTH = BitArray(bin=string[16:32])
		totalRcved = len(string)
		while totalRcved < TOTALLENGTH.uint:
			parte = clientSocket.recv(32).decode()
			string += parte
			totalRcved = len(string)
	
		#Cria um bitarray da resposta
		msg = BitArray(bin=string)
		
		CHECKSUM = BitArray(bin=msg.bin[80:96])
		TIMETOLIVE = BitArray(bin=msg.bin[64:72])
		PROTOCOL = BitArray(bin=msg.bin[72:80])
		
		#Seta o campo de checksum pra 0 para calcular o crc novamente
		msg[80:96] = [0] * (96-80)

		#Faz uma copia da msg pois crc16 destroi o parametro
		auxMsg = BitArray(bin=msg.bin)

		#Calcula o crc da msg
		crc = crc16(auxMsg[:160])

		#Verifica se o crc calculado eh igual ao que veio no header
		if crc.bin != CHECKSUM.bin:
			print 'Checksum diferente'
			print '</body>'
			print '</html>'
			exit()

		#Decrementa o TTL
		ttl = TIMETOLIVE.uint
		ttl -= 1
		TIMETOLIVE = BitArray(int=ttl, length=8)
		
		#Verifica qual comando foi executado
		cmd = PROTOCOL.uint

		#Adiciona o comando a string de saida
		if cmd == 1:
			output1 += 'ps<br>'
		elif cmd == 2:
			output1 += 'df<br>'
		elif cmd == 3:
			output1 += 'finger<br>'
		elif cmd == 4:
			output1 += 'uptime<br>'

		#Converte OPTIONS para ascii e adiciona a string de saida
		OPTIONS = BitArray(bin=msg.bin[160:])
		output1 += '<br>' + binascii.unhexlify(OPTIONS.hex).replace('\x00', '').replace('\n', '<br>') + '<br>'

	finally:
		clientSocket.close()

#Imprime os resultados de todos os comandos no html
print output1 + '<br><br>'

for x in cmd2:
        msg = BitArray()
        IDENTIFICATION = BitArray(int=counter2, length=16)
        PROTOCOL = BitArray(int=int(x), length=8)
        if cmd2[x] != None:
                hexa = binascii.hexlify(cmd2[x])
                OPTIONS = BitArray(hex=hexa)
        else:
                OPTIONS = BitArray()
        CHECKSUM = BitArray(int=0, length=16)
        counter2 += 1

        serverName = '127.0.0.1'
        serverPort = 3002

        #Calcula qnts bits serao necessarios para que OPTIONS
        #tenha um tamanho multiplo de 32
        if len(OPTIONS) != 0:
                resto = len(OPTIONS) % 32
                complete = 32 - resto
                #Completa OPTIONS com o 0s de forma que este seja multiplo
                #de 32 bits
                for i in range(0, complete):
                        OPTIONS.prepend('0b0')

                TOTALLENGTH = BitArray(int=5 * 32 + len(OPTIONS), length=16)
        else:
                TOTALLENGTH = BitArray(int = 5 * 32, length=16)


        #Concatena todos os valores para calcular o CRC16
        #Ate aqui checksum eh 0, seguindo wikipedia
        msg.append(VERSION)
        msg.append(IHL)
        msg.append(TYPEOFSERVICE)
        msg.append(TOTALLENGTH)
        msg.append(IDENTIFICATION)
        msg.append(FLAGS)
        msg.append(OFFSET)
        msg.append(TIMETOLIVE)
        msg.append(PROTOCOL)
        msg.append(CHECKSUM)
        msg.append(SOURCE)
        msg.append(DESTINATION)

        #Caucula e atualiza o checksum
        CHECKSUM = crc16(msg)

        #Cria e concatena todos os valores do header incluindo OPTIONS
        #para enviar o socket
        msg = BitArray()
        msg.append(VERSION)
        msg.append(IHL)
        msg.append(TYPEOFSERVICE)
        msg.append(TOTALLENGTH)
        msg.append(IDENTIFICATION)
        msg.append(FLAGS)
        msg.append(OFFSET)
        msg.append(TIMETOLIVE)
        msg.append(PROTOCOL)
        msg.append(CHECKSUM)
        msg.append(SOURCE)
        msg.append(DESTINATION)
        if len(OPTIONS) != 0:
                msg.append(OPTIONS)

        #Cria um socket tcp para serverName e serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        try:
                #Envia a msg
                clientSocket.sendall(msg.bin.encode())

                #Concatena os bits da resposta em uma string
                string = ''
                parte = clientSocket.recv(32).decode()
                string += parte

                TOTALLENGTH = BitArray(bin=string[16:32])
                totalRcved = len(string)
                while totalRcved < TOTALLENGTH.uint:
                        parte = clientSocket.recv(32).decode()
                        string += parte
                        totalRcved = len(string)

                #Cria um bitarray da resposta
                msg = BitArray(bin=string)

                CHECKSUM = BitArray(bin=msg.bin[80:96])
                TIMETOLIVE = BitArray(bin=msg.bin[64:72])
                PROTOCOL = BitArray(bin=msg.bin[72:80])

                #Seta o campo de checksum pra 0 para calcular o crc novamente
                msg[80:96] = [0] * (96-80)

                #Faz uma copia da msg pois crc16 destroi o parametro
                auxMsg = BitArray(bin=msg.bin)

                #Calcula o crc da msg
                crc = crc16(auxMsg[:160])

                #Verifica se o crc calculado eh igual ao que veio no header
                if crc.bin != CHECKSUM.bin:
                        print 'Checksum diferente'
                        print '</body>'
                        print '</html>'
                        exit()

                #Decrementa o TTL
                ttl = TIMETOLIVE.uint
                ttl -= 1
                TIMETOLIVE = BitArray(int=ttl, length=8)

                #Verifica qual comando foi executado
                cmd = PROTOCOL.uint

                #Adiciona o comando a string de saida
                if cmd == 1:
                        output1 += 'ps<br>'
                elif cmd == 2:
                        output1 += 'df<br>'
                elif cmd == 3:
                        output1 += 'finger<br>'
                elif cmd == 4:
                        output1 += 'uptime<br>'

                #Converte OPTIONS para ascii e adiciona a string de saida
                OPTIONS = BitArray(bin=msg.bin[160:])
                output2 += '<br>' + binascii.unhexlify(OPTIONS.hex).replace('\x00', '').replace('\n', '<br>') + '<br>'
                
        finally:
                clientSocket.close()

#Imprime os resultados de todos os comandos no html
print output2 + '<br><br>'
	
for x in cmd3:
        msg = BitArray()
        IDENTIFICATION = BitArray(int=counter3, length=16)
        PROTOCOL = BitArray(int=int(x), length=8)
        if cmd3[x] != None:
                hexa = binascii.hexlify(cmd3[x])
                OPTIONS = BitArray(hex=hexa)
        else:
                OPTIONS = BitArray()
        CHECKSUM = BitArray(int=0, length=16)
        counter3 += 1

        serverName = '127.0.0.1'
        serverPort = 3003

        #Calcula qnts bits serao necessarios para que OPTIONS
        #tenha um tamanho multiplo de 32
        if len(OPTIONS) != 0:
                resto = len(OPTIONS) % 32
                complete = 32 - resto
                #Completa OPTIONS com o 0s de forma que este seja multiplo
                #de 32 bits
                for i in range(0, complete):
                        OPTIONS.prepend('0b0')

                TOTALLENGTH = BitArray(int=5 * 32 + len(OPTIONS), length=16)
        else:
                TOTALLENGTH = BitArray(int = 5 * 32, length=16)


        #Concatena todos os valores para calcular o CRC16
        #Ate aqui checksum eh 0, seguindo wikipedia
        msg.append(VERSION)
        msg.append(IHL)
        msg.append(TYPEOFSERVICE)
        msg.append(TOTALLENGTH)
        msg.append(IDENTIFICATION)
        msg.append(FLAGS)
        msg.append(OFFSET)
        msg.append(TIMETOLIVE)
        msg.append(PROTOCOL)
        msg.append(CHECKSUM)
        msg.append(SOURCE)
        msg.append(DESTINATION)

        #Caucula e atualiza o checksum
        CHECKSUM = crc16(msg)

        #Cria e concatena todos os valores do header incluindo OPTIONS
        #para enviar o socket
        msg = BitArray()
        msg.append(VERSION)
        msg.append(IHL)
        msg.append(TYPEOFSERVICE)
        msg.append(TOTALLENGTH)
        msg.append(IDENTIFICATION)
        msg.append(FLAGS)
        msg.append(OFFSET)
        msg.append(TIMETOLIVE)
        msg.append(PROTOCOL)
        msg.append(CHECKSUM)
        msg.append(SOURCE)
        msg.append(DESTINATION)
        if len(OPTIONS) != 0:
                msg.append(OPTIONS)

        #Cria um socket tcp para serverName e serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        try:
                #Envia a msg
                clientSocket.sendall(msg.bin.encode())

                #Concatena os bits da resposta em uma string
                string = ''
                parte = clientSocket.recv(32).decode()
                string += parte

                TOTALLENGTH = BitArray(bin=string[16:32])
                totalRcved = len(string)
                while totalRcved < TOTALLENGTH.uint:
                        parte = clientSocket.recv(32).decode()
                        string += parte
                        totalRcved = len(string)

                #Cria um bitarray da resposta
                msg = BitArray(bin=string)

                CHECKSUM = BitArray(bin=msg.bin[80:96])
                TIMETOLIVE = BitArray(bin=msg.bin[64:72])
                PROTOCOL = BitArray(bin=msg.bin[72:80])

                #Seta o campo de checksum pra 0 para calcular o crc novamente
                msg[80:96] = [0] * (96-80)

                #Faz uma copia da msg pois crc16 destroi o parametro
                auxMsg = BitArray(bin=msg.bin)

                #Calcula o crc da msg
                crc = crc16(auxMsg[:160])

                #Verifica se o crc calculado eh igual ao que veio no header
                if crc.bin != CHECKSUM.bin:
                        print 'Checksum diferente'
                        print '</body>'
                        print '</html>'
                        exit()

                #Decrementa o TTL
                ttl = TIMETOLIVE.uint
                ttl -= 1
                TIMETOLIVE = BitArray(int=ttl, length=8)

                #Verifica qual comando foi executado
                cmd = PROTOCOL.uint

                #Adiciona o comando a string de saida
                if cmd == 1:
                        output1 += 'ps<br>'
                elif cmd == 2:
                        output1 += 'df<br>'
                elif cmd == 3:
                        output1 += 'finger<br>'
                elif cmd == 4:
                        output1 += 'uptime<br>'

                #Converte OPTIONS para ascii e adiciona a string de saida
                OPTIONS = BitArray(bin=msg.bin[160:])
                output3 += '<br>' + binascii.unhexlify(OPTIONS.hex).replace('\x00', '').replace('\n', '<br>') + '<br>'
                
        finally:
                clientSocket.close()

#Imprime os resultados de todos os comandos no html
print output3 + '<br><br>'

		
print "</body>"
print "</html>"


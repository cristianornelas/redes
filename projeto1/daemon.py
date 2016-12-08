#!/usr/bin/python

from bitstring import BitArray
from socket import *
import sys, threading, binascii, subprocess

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

def handleConnection(connectionSocket, address):
	try:
		#Concatena os bits da msg em uma string
        	string = ''
		parte = connectionSocket.recv(32).decode()
		string += parte
		
		TOTALLENGTH = BitArray(bin=string[16:32])
		totalRcved = len(string)
	       	while totalRcved < TOTALLENGTH.uint:
			parte = connectionSocket.recv(32).decode()
			string += parte
			totalRcved = len(string)
		
	        #Cria um bitarray da msg
	        msg = BitArray(bin=string)

		#Pega o valores que vieram no header
		IDENTIFICATION = BitArray(bin=msg.bin[32:48])
		TIMETOLIVE = BitArray(bin=msg.bin[64:72])
		PROTOCOL = BitArray(bin=msg.bin[72:80])
		CHECKSUM = BitArray(bin=msg.bin[80:96])
		print 0	
		OPTIONS = BitArray(bin=msg.bin[160:])
		print 1
		print OPTIONS
		print 2	
		#Seta o campo de checksum pra 0 para calcular o crc novamente
		msg[80:96] = [0] * (96 - 80)
	
		#Faz uma copia da msg pois crc16 destroi o parametro
		auxMsg = BitArray(bin=msg.bin)
	
		#Calcula o crc da msg
		crc = crc16(auxMsg[:160])

		#Verifica se o crc calculado eh igual ao que veio no header
		if crc.bin != CHECKSUM.bin:
			return 'Checksum diferente'
	
		#Decrementa o TTL
		ttl = TIMETOLIVE.uint
		ttl -= 1
		TIMETOLIVE = BitArray(int=ttl, length=8)

		#Verifica qual o comando a ser executado
		cmd = PROTOCOL.uint
	
		#Converte os argumentos para string, remove null characters
		argms = binascii.unhexlify(OPTIONS.hex).replace('\x00', '').split()
	
		#Executa o comando e armazena a saida em output
		if cmd == 1:
			argms = ['ps']  + argms
			p = subprocess.Popen(argms, stdout=subprocess.PIPE)
			output, err = p.communicate() 
		elif cmd == 2:
			argms = ['df']  + argms
        	        p = subprocess.Popen(argms, stdout=subprocess.PIPE)
	                output, err = p.communicate() 
		elif cmd == 3:
			argms = ['finger']  + argms
        	        p = subprocess.Popen(argms, stdout=subprocess.PIPE)
	                output, err = p.communicate() 
		elif cmd == 4:
			argms = ['uptime']  + argms
	                p = subprocess.Popen(argms, stdout=subprocess.PIPE)
        	        output, err = p.communicate() 
	
		#Recria cabecalho	
		VERSION = BitArray(int=2, length=4)
		IHL = BitArray(int=5, length=4)
		TYPEOFSERVICE = BitArray(int=0, length=8)
		FLAGS = BitArray(bin='111')
		OFFSET = BitArray(int=0, length=13)
		SOURCE = BitArray(bin=msg.bin[128:160])
		DESTINATION = BitArray(bin=msg.bin[96:128])
		hexa = binascii.hexlify(output)
		OPTIONS = BitArray(hex=hexa)

		#Calcula qnts bits serao necessarios para que OPTIONS
        	#tenha um tamanho multiplo de 32
	        resto = len(OPTIONS) % 32
        	complete = 32 - resto
	        #Completa OPTIONS com o 0s de forma que este seja multiplo
        	#de 32 bits
	        for i in range(0, complete):
	                OPTIONS.prepend('0b0')

		TOTALLENGTH = BitArray(int= 5 * 32 + len(OPTIONS), length=16)
		CHECKSUM = BitArray(int=0, length=16)
	
		#Cria o header para o calculo do checksum
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
	        msg.append(OPTIONS)
		
		print binascii.unhexlify(OPTIONS.hex).replace('\x00', '')
	
		#Envia a resposta
		if connectionSocket.sendall(msg.bin.encode()) != None:
			return 'Erro ao enviar resposta'
	finally:
		connectionSocket.close()
		print 'Conexao encerrada'


if __name__ == '__main__':

	#Cria o server socket
	serverSocket = socket(AF_INET, SOCK_STREAM)

	#Liga o socket a porta passada por parametro e escuta a ate 5 conexoes
	serverSocket.bind(('', int(sys.argv[1])))
	serverSocket.listen(5)

	threads = []

	while True:
		#Aceita conexao do cliente
		connectionSocket, addr = serverSocket.accept()	
		
		#Inicia uma thread para processar a msg
		t = threading.Thread(target=handleConnection, args=(connectionSocket, addr))
		threads.append(t)
		t.start()
		print 'Thread: {0}'.format(t)

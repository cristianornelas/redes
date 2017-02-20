====== **Terceiro Laboratório** =======

Desenhamos a seguinte topologia :
![Topologia 3] (images/1.png)

O Objetivo principal desse lab era integrar o Quagga com o mininet. Precisamos do Quagga para gerenciar o protoloco que iriamos utilizar para esse lab de ip dinâmico.

Infelizmente não conseguimos fazer a integração com o mininet e acertar as configurações necessárias. Mesmo trocando informações com os colegas via facebook e utilizando laboratório de bgp attack como base, não conseguimos chegar a uma solução.

Nas diversas tentativas tivemos problemas em:

-Fazer a integração das interfaces configuradas nos arquivos de conf do zebra. Mesmo que os hosts, por exemplo, aderiam os ips não conseguimos pingar nem os neighbors definidos.

-Tentamos iniciar uma topologia minimalista para realizar a o funcionamento do Quagga, porém sem sucesso nas configurações.

-A troca de informação entre roteadores para as tabelas, mesmo debugando o lab do bgp não conseguimos implementar no nosso lab. Mesmo se tentassemos mexer no código do próprio lab, já não rodava mais.

-Tentamos implementar com o protocolo BGP ( por ser o mesmo do lab exemplo) para depois passar para o protocolo ospf e não deu certo também.


-> Decidimos fazer somente a topologia em mininet pois ficamos atados com o Quagga.

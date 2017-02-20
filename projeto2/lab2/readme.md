=======** Segundo Laboratório ** =======

Implementamos a seguinte topologia: 
- 2 Hosts em uma subrede (10.0.0.1)
- 2 Hosts em outra subrede (20.0.0.1)
- 2 roteadores (Utilizamos 1 Switch com ipforward como aconselhado na última aula)
- 1 controlador

O objetivo principal era estabelecer a conexão entre os hosts das diferentes subredes. Para isso configuramos os IPs e default gateways dos hosts de modo a representar as duas subredes citadas e configuramos as interfaces de cada subrede em cada roteador.

Resultados : 

Conseguimos realizar o ping entre os hosts de diferentes subredes, mas apenas se utilizassemos primeiro o comando ping host a host. Sem esse passo, o comando pingall era incapaz de verificar a conexão entre todos os hosts.

Subrede 1

![Subrede 1] (images/1.png)

Subrede 2

![Subrede 2] (images/2.png)

Nodes, subredes e pingall

![nodes subredes pingall ] (images/3.png)
=

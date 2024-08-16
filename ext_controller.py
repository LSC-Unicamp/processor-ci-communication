'''
Analisar dados para validação de processadores em FPGAs se torna uma tarefa díficil
no quesito da analise de sinais internos e externos do processador. Para isso, é
necessário a utilização de um controlador para a captura de sinais e envio de dados
para o processador. Contudo precisamos enviar as informações a serem enviadas pelo 
controlador e recebermos resultados do processador que serão enviados ao controlador 
para a análise dos dados e realização de testes.

Este módulo tem como objetivo realizar a comunicação entre a maquina host e o controlador
enviados comandos e recebendo respostas para a checagem enventual no jenkins.


Comandos:

Descrição                                       | Opcode    | ASCII opcode | Imediato | Segundo pacote
------------------------------------------------|-----------|--------------|----------|---------------
Enviar N pulsos de CLK                          | 01000011  | C            |          |
Parar o CLK do Core                             | 01010011  | S            |          |
Retomar o CLK do Core                           | 01110010  | r            |          |
Resetar o Core                                  | 01010010  | R            |          |
Escrever na posição N de memória                | 01010111  | W            |          | Y
Ler a posição N de memória                      | 01001100  | L            |          |
Carregar bits mais significativos no Acumulador | 01010101  | U            |          |
Carregar bits menos significativos no acumulador| 01101100  | l            |          |
Somar N ao acumulador                           | 01000001  | A            |          |
Escrever Acumulador na posição N                | 01110111  | w            |          |
Escrever N na posição do acumulador             | 01110011  | s            |          |
Ler a posição do acumulador                     | 01110010  | r            |          |
Setar timeout                                   | 01010100  | T            |          |
Setar tamanho da página de memória              | 01010000  | P            |          |
Executar testes em memória                      | 01000101  | E            |          |
Obter o ID e verificar funcionamento do módulo  | 01110000  | p            |          |
Definir endereço N de término de execução       | 01000100  | D            |          |
Definir o valor do Acumulador como              | 01100100  | d            |          |
endereço de término                             |           |              |          |
'''
import serial

class ExtController:
    def __init__(self, PortDescriptor, baudrate = 115200, timeout = 1):
        self.ser = serial.Serial(PortDescriptor, baudrate)
        self.ser.timeout = timeout

    def send_data(self, data):
        self.ser.write(data)
        return self.ser.read(1)
    
    def close(self):
        self.ser.close()

    def run(self, data):
        while True:
            option = input('Digite o comando: ')
            if option == 'C': # Enviar N pulsos de CLK
                opcode = 0b01000011
                N = int(input('Digite o número de pulsos de CLK: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')  # Converte para 4 bytes (32 bits)
                self.send_data(mensagem_bytes)
            elif option == 'S': # Parar o CLK do Core
                opcode = 0b01010011
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'r': # Retomar o CLK do Core
                opcode = 0b01110010
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'R': # Resetar o Core
                opcode = 0b01010010
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'W': # Escrever na posição N de memória
                opcode = 0b01010111
                N = int(input('Digite o endereço de memória: '))
                Y = int(input('Digite o valor a ser escrito: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
                Y_bytes = Y.to_bytes(4, 'big')
                self.send_data(Y_bytes)
            elif option == 'L': # Ler a posição N de memória
                opcode = 0b01001100
                N = int(input('Digite o endereço de memória: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'U': # Carregar bits mais significativos no Acumulador
                opcode = 0b01010101
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'l': # Carregar bits menos significativos no acumulador
                opcode = 0b01101100
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'A': # Somar N ao acumulador
                opcode = 0b01000001
                N = int(input('Digite o valor a ser somado: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'w': # Escrever Acumulador na posição N
                opcode = 0b01110111
                N = int(input('Digite o endereço de memória: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 's': # Escrever N na posição do acumulador
                opcode = 0b01110011
                N = int(input('Digite o valor a ser escrito: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'r': # Ler a posição do acumulador
                opcode = 0b01110010
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'T': # Setar timeout
                self.send_data([0b01010100])
            elif option == 'P': # Setar tamanho da página de memória
                self.send_data([0b01010000])
            elif option == 'E': # Executar testes em memória
                self.send_data([0b01000101])
            elif option == 'p': # Obter o ID e verificar funcionamento do módulo
                self.send_data([0b01110000])
            elif option == 'D': # Definir endereço N de término de execução
                self.send_data([0b01000100])
            elif option == 'd': # Definir o valor do Acumulador como endereço de término
                opcode = 0b01100100
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'help':
                help()
            elif option == 'exit':
                break
        self.close()

def help():
    help_text = open('help.txt', 'r')
    print(help_text.read())
    help_text.close()

def main():
    help()
    #controller = ExtController()
    return 0

main()
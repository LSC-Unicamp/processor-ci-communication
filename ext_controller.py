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
Escrever N posições a partir do acumulador      | 01100101  | e            |          |
Ler N posições a partir do acumulador           | 01100010  | b            |          |
Obter o valor do Acumulador                     | 01100001  | a            |          |
Alterar prioridade de acesso a memória para o   | 01001111  | O            |          |
core                                            |           |              |          |
Executar até o ponto de parada                  | 01110101  | u            |          |
'''
import serial

class ExtController:
    def __init__(self, PortDescriptor, baudrate = 115200, timeout = 1):
        self.ser = serial.Serial(PortDescriptor, baudrate)
        self.ser.timeout = timeout

    def send_data(self, data):
        self.ser.write(data)

    def read_data(self):
        x = self.ser.read(4)
        print("Bytes de x:")
        for byte in x:
            print(f"{byte:02x}", end='')
        print()
    
    def close(self):
        self.ser.close()

    def run(self):
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
                print(mensagem_bytes)
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
                opcode = 0b01010100
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'P': # Setar tamanho da página de memória
                opcode = 0b01010000
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'E': # Executar testes em memória
                opcode = 0b01000101
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
                self.read_data() # Confirmar se os testes foram realizados
            elif option == 'p': # Obter o ID e verificar funcionamento do módulo
                opcode = 0b01110000
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'D': # Definir endereço N de término de execução
                opcode = 0b01000100
                N = int(input('Digite o endereço de término: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'd': # Definir o valor do Acumulador como endereço de término
                opcode = 0b01100100
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'e': # Escrever N posições a partir do acumulador
                opcode = 0b01100101
                N = n = int(input('Digite o número de posições a serem escritas: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
                for i in range(n):
                    Y = int(input(f'Digite o valor da posição {i}: '))
                    Y_bytes = Y.to_bytes(4, 'big')
                    self.send_data(Y_bytes)
            elif option == 'b': # Ler N posições a partir do acumulador
                opcode = 0b01100010
                N = n = int(input('Digite o número de posições a serem lidas: '))
                N = N << 8
                mensagem = opcode | N
                mensagem_bytes = mensagem.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
                for i in range(n):
                    self.read_data()
            elif option == 'a': # Obter o valor do Acumulador
                opcode = 0b01100001
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
                self.read_data()
            elif option == 'O': # Alterar prioridade de acesso a memória para o core
                opcode = 0b01001111
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
            elif option == 'u': # Executar até o ponto de parada
                opcode = 0b01110101
                mensagem_bytes = opcode.to_bytes(4, 'big')
                self.send_data(mensagem_bytes)
                self.read_data() # Confirmar se a execução foi até o ponto de parada
            elif option == 'exit':
                break
            self.read_data()
            self.read_data()
        self.close()

def main():
    controller = ExtController("/dev/ttyUSB1", 115200, 1)
    controller.run()
    return 0

if __name__ == "__main__":
    main()
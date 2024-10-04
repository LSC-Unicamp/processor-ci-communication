import serial
import argparse
import os
import glob


class ExtController:
    def __init__(self, PortDescriptor, baudrate=115200, timeout=1):
        self.ser = serial.Serial(PortDescriptor, baudrate)
        self.ser.timeout = timeout

    def send_data(self, data):
        self.ser.write(data)

    def read_data(self):
        x = self.ser.read(4)
        print("Bytes de x:")
        for byte in x:
            print(f"{byte:02x}", end="")
        print()
        return x

    def close(self):
        self.ser.close()

    def load_program(self, program: str, start_acm_address: int = 0, breakpoint: int = 60):
        self.set_execution_end_address(breakpoint)
        acm_address = self.read_accumulator(self)
        if start_acm_address != acm_address:
            self.load_lsb_accumulator(start_acm_address & 0x0000FFFF)
            self.load_msb_accumulator((start_acm_address & 0xFFFF0000) >> 16)
        file = open(program, "r")
        num_lines = sum(1 for _ in file)
        file.seek(0)
        opcode = 0x65
        opcode_bytes = (opcode | num_lines).to_bytes(4, "big")
        self.send_data(opcode_bytes)
        for line in file.readlines():
            command = int(line, 16)
            command_bytes = command.to_bytes(4, "big")
            self.send_data(command_bytes)

    def run_directory_tests(self, directory: str):
        files = glob.glob(os.path.join(directory, "*"))
        result_file = open(str + "_" + "result.txt", "w")
        for file_path in files:
            self.load_program(file_path, 0)
            result = self.read_data()
            result_file.write(f"{file_path}: {result}\n")

    def send_command(self, opcode, immidiate):
        pass

    def send_clk_pulses(self):
        opcode = 0b01000011
        N = int(input("Digite o número de pulsos de CLK: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def stop_clk(self):
        opcode = 0b01010011
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def resume_clk(self):
        opcode = 0b01110010
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def reset_core(self):
        opcode = 0b01010010
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def write_memory(self):
        opcode = 0b01010111
        N = int(input("Digite o endereço de memória: "))
        Y = int(input("Digite o valor a ser escrito: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        Y_bytes = Y.to_bytes(4, "big")
        self.send_data(Y_bytes)

    def read_memory(self):
        opcode = 0b01001100
        N = int(input("Digite o endereço de memória: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        self.read_data()

    def load_msb_accumulator(self):
        opcode = 0b01010101
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def load_lsb_accumulator(self):
        opcode = 0b01101100
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def add_to_accumulator(self):
        opcode = 0b01000001
        N = int(input("Digite o valor a ser somado: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def write_accumulator_to_memory(self):
        opcode = 0b01110111
        N = int(input("Digite o endereço de memória: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def write_to_accumulator(self):
        opcode = 0b01110011
        N = int(input("Digite o valor a ser escrito: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def read_accumulator(self):
        opcode = 0b01110010
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        return self.read_data()  # Return in hex

    def set_timeout(self):
        opcode = 0b01010100
        N = int(input("Digite o valor do timeout em ciclos de CLK: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def set_memory_page_size(self):
        opcode = 0b01010000
        N = int(input("Digite o tamanho da página de memória: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def run_memory_tests(self):
        opcode = 0b01000101
        N = int(input("Digite o número de paginas a serem utilizadas: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        result = self.read_data()
        if result == 0x676F6F64:
            print("Testes realizados com sucesso")
        else:
            print("Erro ao realizar testes")

    def get_module_id(self):
        opcode = 0b01110000
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        result = self.read_data()

    def set_execution_end_address(self):
        opcode = 0b01000100
        N = int(input("Digite o endereço de término: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def set_accumulator_as_end_address(self):
        opcode = 0b01100100
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def write_from_accumulator(self):
        opcode = 0b01100101
        N = n = int(input("Digite o número de posições a serem escritas: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        for i in range(n):
            Y = int(input(f"Digite o informação para posição {i}: "))
            Y_bytes = Y.to_bytes(4, "big")
            self.send_data(Y_bytes)

    def read_from_accumulator(self):
        opcode = 0b01100010
        N = n = int(input("Digite o número de posições a serem lidas: "))
        N = N << 8
        mensagem = opcode | N
        mensagem_bytes = mensagem.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        data = []
        for i in range(n):
            data_line = self.read_data()
            data.append(data_line)

    def get_accumulator_value(self):
        opcode = 0b01100001
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        acumulador = self.read_data()

    def change_memory_access_priority(self):
        opcode = 0b01001111
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)

    def execute_until_stop(self):
        opcode = 0b01110101
        mensagem_bytes = opcode.to_bytes(4, "big")
        self.send_data(mensagem_bytes)
        result = self.read_data()
        if result == 0x6C75636B:
            print("Execução até o ponto de parada")
        else:
            print("Erro ao executar até o ponto de parada")
        informacao = self.read_data()

    def run(self):
        while True:
            option = input("Digite o comando: ")
            if option == "C":
                self.send_clk_pulses()
            elif option == "S":
                self.stop_clk()
            elif option == "r":
                self.resume_clk()
            elif option == "R":
                self.reset_core()
            elif option == "W":
                self.write_memory()
            elif option == "L":
                self.read_memory()
            elif option == "U":
                self.load_msb_accumulator()
            elif option == "l":
                self.load_lsb_accumulator()
            elif option == "A":
                self.add_to_accumulator()
            elif option == "w":
                self.write_accumulator_to_memory()
            elif option == "s":
                self.write_to_accumulator()
            elif option == "r":
                self.read_accumulator()
            elif option == "T":
                self.set_timeout()
            elif option == "P":
                self.set_memory_page_size()
            elif option == "E":
                self.run_memory_tests()
            elif option == "p":
                self.get_module_id()
            elif option == "D":
                self.set_execution_end_address()
            elif option == "d":
                self.set_accumulator_as_end_address()
            elif option == "e":
                self.write_from_accumulator()
            elif option == "b":
                self.read_from_accumulator()
            elif option == "a":
                self.get_accumulator_value()
            elif option == "O":
                self.change_memory_access_priority()
            elif option == "u":
                self.execute_until_stop()
            elif option == "exit":
                break
        self.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port", help="Porta de comunicação com o controlador", required=True
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        help="Velocidade de comunicação com o controlador",
        default=115200,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help="Tempo de espera para a comunicação com o controlador",
        default=1,
    )
    parser.add_argument(
        "-tp", "--test_program", help="Programa de teste a ser carregado no controlador"
    )
    parser.add_argument(
        "-td",
        "--test_directory",
        help="Diretório com os programas de teste a serem carregados no controlador",
    )
    args = parser.parse_args()

    controller = ExtController(args.port, args.baudrate, args.timeout)
    if args.test_program:
        controller.load_program(args.test_program)
    elif args.test_directory:
        pass
    else:
        controller.run()
    return 0


if __name__ == "__main__":
    main()

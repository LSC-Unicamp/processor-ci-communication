import cmd
from core.serial import ProcessorCIInterface
from core.file import read_file


class ProcessorCIInterfaceShell(cmd.Cmd, ProcessorCIInterface):
    prompt = "ProcessorCIInterface> "

    def __init__(self, port: str, baudrate: int, timeout: int = 1) -> None:
        ProcessorCIInterface.__init__(self, port, baudrate, timeout)
        cmd.Cmd.__init__(self)

    def do_exit(self, arg):
        return True

    def do_write_clk(self, arg):
        self.send_clk_pulses(int(arg))

    def do_stop_clk(self, _):
        self.stop_clk()

    def do_resume_clk(self, _):
        self.resume_clk()

    def do_reset_core(self, _):
        self.reset_core()

    def do_write_memory(self, arg):
        arg = arg.split()
        address, value = arg[0], arg[1]
        second_memory = False
        if len(arg) > 2:
            second_memory = bool(int(arg[1]))

        self.write_memory(int(address, 16), int(value, 16), second_memory)

    def do_read_memory(self, arg):
        arg = arg.split()
        second_memory = False
        address = int(arg[0], 16)
        if len(arg) > 1:
            second_memory = bool(int(arg[1]))

        self.print_data(self.read_memory(address, second_memory))

    def do_load_msb_accumulator(self, arg):
        self.load_msb_accumulator(int(arg, 16))

    def do_load_lsb_accumulator(self, arg):
        self.load_lsb_accumulator(int(arg, 16))

    def do_add_to_accumulator(self, arg):
        self.add_to_accumulator(int(arg, 16))

    def do_write_accumulator_to_memory(self, arg):
        self.write_accumulator_to_memory(int(arg, 16))

    def do_write_to_accumulator(self, arg):
        self.write_to_accumulator(int(arg, 16))

    def do_read_accumulator(self, _):
        self.print_data(self.read_accumulator())

    def do_set_timeout(self, arg):
        self.set_timeout(int(arg))

    def do_set_memory_page_size(self, arg):
        self.set_memory_page_size(int(arg))

    def do_run_memory_tests(self, _):
        self.run_memory_tests()

    def do_get_module_id(self, _):
        self.print_data(self.get_module_id())

    def do_set_breakpoint(self, arg):
        self.set_execution_end_address(int(arg, 16))

    def do_set_accumulator_as_breakpoint(self, arg):
        self.set_accumulator_as_end_address()

    def do_write_from_accumulator(self, arg):
        data = []

        for _ in range(int(arg)):
            data.append(int(input(), 16))

        self.write_from_accumulator(int(arg), data)

    def do_read_to_accumulator(self, arg):
        data = self.read_to_accumulator(int(arg))

        for byte in data:
            self.print_data(byte)

    def do_read_accumulator(self):
        self.print_data(self.get_accumulator_value())

    def do_swap_memory_to_core(self):
        self.change_memory_access_priority()

    def do_until(self, _):
        self.execute_until_stop()

    def do_sync(self, _):
        self.print_data(self.sync())

    def do_write_file_in_memory(self, arg):
        arg = arg.split()

        if len(arg) > 1:
            self.add_to_accumulator(int(arg[1], 16))

        data, size = read_file(arg[0])

        self.write_from_accumulator(size, data)

    def do_help(self, arg):
        if arg:
            try:
                func = getattr(self, "do_" + arg)
                print(
                    func.__doc__ if func.__doc__ else f"Sem ajuda disponível para {arg}"
                )
            except AttributeError:
                print(f"Comando {arg} não encontrado.")
        else:
            print("Comandos disponíveis:")
            print("exit - Sai do shell.")
            print("write_clk <n> - Envia n pulsos de clock.")
            print("stop_clk - Para o clock.")
            print("resume_clk - Retoma o clock.")
            print("reset_core - Reseta o núcleo.")
            print(
                "write_memory <endereço> <valor> - Escreve na memória no endereço fornecido."
            )
            print("read_memory <endereço> - Lê a memória no endereço fornecido.")
            print("load_msb_accumulator <valor> - Carrega o MSB no acumulador.")
            print("load_lsb_accumulator <valor> - Carrega o LSB no acumulador.")
            print("add_to_accumulator <valor> - Adiciona um valor ao acumulador.")
            print(
                "write_accumulator_to_memory <endereço> - Escreve o acumulador na memória."
            )
            print("write_to_accumulator <valor> - Escreve diretamente no acumulador.")
            print("read_accumulator - Lê o valor do acumulador.")
            print("set_timeout <tempo> - Define o tempo limite.")
            print(
                "set_memory_page_size <tamanho> - Define o tamanho da página de memória."
            )
            print("run_memory_tests - Executa testes de memória.")
            print("get_module_id - Obtém o ID do módulo.")
            print("set_breakpoint <endereço> - Define um breakpoint no endereço.")
            print(
                "set_accumulator_as_breakpoint - Define o acumulador como breakpoint."
            )
            print(
                "write_from_accumulator <n> - Escreve n bytes a partir do acumulador."
            )
            print("read_to_accumulator <n> - Lê n bytes no acumulador.")
            print("swap_memory_to_core - Troca a prioridade de acesso à memória.")
            print("until - Executa até a condição de parada.")

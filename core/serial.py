import os
import time
import serial


class ProcessorCIInterface:
    def __init__(self, port: str, baudrate: int, timeout: int = 1) -> None:
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port, baudrate)
        self.serial.flushInput()
        self.serial.flushOutput()

    def send_data(self, data: bytes) -> None:
        self.serial.write(data)

    def read_data(self, size: int = 4) -> bytes:
        return self.serial.read(size)

    def print_data(self, data: bytes) -> None:
        print("Bytes de x:")
        for byte in data:
            print(f"{byte:02x}", end="")
        print()

    def data_available(self) -> bool:
        return self.serial.in_waiting > 0

    def close(self) -> None:
        self.serial.close()

    def send_command(self, opcode: int, immediate: int) -> None:
        opcode = opcode & 0xFF
        immediate = immediate << 8

        data = opcode | immediate
        data = data.to_bytes(4, "big")
        self.send_data(data)

    def send_rawdata(self, data: int) -> None:
        data = data.to_bytes(4, "big")
        self.send_data(data)

    def send_clk_pulses(self, n: int) -> None:
        self.send_command(0x43, n)

    def stop_clk(self) -> None:
        self.send_command(0x53, 0)

    def resume_clk(self) -> None:
        self.send_command(0x72, 0)

    def reset_core(self) -> None:
        self.send_command(0x52, 0)

    def write_memory(self, address: int, value: int) -> None:
        self.send_command(0x57, address >> 2)
        self.send_rawdata(value)

    def read_memory(self, address: int) -> int:
        self.send_command(0x4C, address >> 2)
        return self.read_data()

    def load_msb_accumulator(self, value: int) -> None:
        self.send_command(0x55, value)

    def load_lsb_accumulator(self, value: int) -> None:
        self.send_command(0x6C, value & 0xFF)

    def add_to_accumulator(self, value: int) -> None:
        self.send_command(0x41, value)

    def write_accumulator_to_memory(self, address: int) -> None:
        self.send_command(0x77, address)

    def write_to_accumulator(self, value: int) -> None:
        self.send_command(0x73, value)

    def read_accumulator(self) -> int:
        self.send_command(0x72, 0)
        return self.read_data()

    def set_timeout(self, timeout: int) -> None:
        self.send_command(0x54, timeout)

    def set_memory_page_size(self, size: int) -> None:
        self.send_command(0x50, size)

    def run_memory_tests(
        self, number_of_pages: int, breakpoint: int = -1, timeout: int = -1
    ) -> bytes:
        if breakpoint != -1:
            self.set_execution_end_address(breakpoint)
        if timeout != -1:
            self.set_timeout(timeout)

        self.send_command(0x45, number_of_pages)

        while not self.data_available():
            time.sleep(0.1)

        return self.read_data()

    def get_module_id(self) -> int:
        self.send_command(0x70, 0)
        return self.read_data()

    def set_execution_end_address(self, address: int) -> None:
        self.send_command(0x44, address)

    def set_accumulator_as_end_address(self):
        self.send_command(0x64, 0)

    def write_from_accumulator(self, n: int, data: list[int]) -> None:
        self.send_command(0x65, n)
        for i in range(n):
            self.send_rawdata(data[i])

    def read_from_accumulator(self, n: int) -> list[int]:
        self.send_command(0x62, n)
        data = []
        for _ in range(n):
            data_line = self.read_data()
            data.append(data_line)

        return data

    def get_accumulator_value(self) -> int:
        self.send_command(0x61, 0)
        return self.read_data()

    def change_memory_access_priority(self) -> None:
        self.send_command(0x4F, 0)

    def execute_until_stop(self, breakpoint: int = -1, timeout: int = -1) -> bytes:
        if breakpoint != -1:
            self.set_execution_end_address(breakpoint)
        if timeout != -1:
            self.set_timeout(timeout)

        self.send_command(0x75, 0)

        while not self.data_available():
            time.sleep(0.1)

        return self.read_data(8)

    def sync(self) -> bytes:
        self.send_data(0x70)

        if not self.data_available():
            self.send_data(0x70)

        return self.read_data(4)

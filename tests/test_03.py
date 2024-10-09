import os
import unittest
import xmlrunner
from core.serial import ProcessorCIInterface
from core.file import read_file, list_files_in_dir, open_files_in_dir


class TestTypeRBasic(unittest.TestCase):
    def setUp(self):
        self.port = os.getenv("PORT", "/dev/ttyACM0")
        self.controller = ProcessorCIInterface(self.port, 115200, 1)
        id = self.controller.get_module_id()
        self.controller.set_timeout(200)
        self.controller.set_execution_end_address(60)

    def test_beq(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/028-beq.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x11)

    def test_beq_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/029-beq.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)

    def test_bne(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/038-bne.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x11)

    def test_bne_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/039-bne.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)

    def test_blt(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/034-blt.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x11)

    def test_blt_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/035-blt.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)

    def test_bge(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/030-bge.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x11)

    def test_bge_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/031-bge.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)

    def test_bltu(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/036-bltu.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x11)

    def test_bltu_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/037-bltu.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)

    def test_bgeu(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/032-bgeu.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x11)

    def test_bgeu_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/033-bgeu.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)


if __name__ == "__main__":
    with open("test-reports/results_type_b_basic.xml", "w") as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))

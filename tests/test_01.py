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

    def test_add(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/001-add.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 10)

    def test_sub(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/002-sub.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 10)

    def test_and(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/003-and.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 1)

    def test_or(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/004-or.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 7)

    def test_xor(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/005-xor.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 6)

    def test_slt(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/007-slt.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0)

    def test_sltu(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/008-sltu.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0)

    def test_sll(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/006-sll.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 8)

    def test_srl(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/009-srl.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 2)

    def test_sra(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/010-sra.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 2)


if __name__ == "__main__":
    with open("test-reports/results_type_r_basic.xml", "w") as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))

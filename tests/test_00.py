import os
import unittest
import xmlrunner
from core.serial import ProcessorCIInterface
from core.file import read_file, list_files_in_dir, open_files_in_dir


class TestTypeIBasic(unittest.TestCase):
    def setUp(self):
        self.port = os.getenv("PORT", "/dev/ttyACM0")
        self.controller = ProcessorCIInterface(self.port, 115200, 1)
        id = self.controller.get_module_id()
        self.controller.set_timeout(200)
        self.controller.set_execution_end_address(60)

    def test_addi(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/000-addi.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 5)

    def test_andi(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/014-andi.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 1)

    def test_ori(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/015-ori.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 7)

    def test_xori(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/016-xori.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 6)

    def test_slti(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/012-slti.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0)

    def test_slti_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/018-slti.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 1)

    def test_sltiu(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/019-sltiu.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 1)

    def test_slli(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/011-slli.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 8)

    def test_slli_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/017-slli.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0x10)

    def test_srli(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/013-srli.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 2)

    def test_lw(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/022-lw.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0x809)

    def test_lh(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/023-lh.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0xFFC0)

    def test_lb(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/024-lb.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 0xFF)

    def test_jalr(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/042-jalr.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 7)

    def test_jalr_2(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/043-jalr.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, "big"), 7)


if __name__ == "__main__":
    with open("test-reports/results_type_i_basic.xml", "w") as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))

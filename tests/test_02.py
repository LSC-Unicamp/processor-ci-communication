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

    def test_sw(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/025-sw.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0x1E)

    def test_sh(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/026-sh.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0xFFC0)

    def test_sb(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/027-sb.hex")
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 0xFE)


if __name__ == "__main__":
    with open("test-reports/results_type_s_basic.xml", "wb") as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))

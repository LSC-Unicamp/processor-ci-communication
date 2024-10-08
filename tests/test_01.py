import os
import unittest
import xmlrunner
from core.serial import ProcessorCIInterface
from core.file import read_file, list_files_in_dir, open_files_in_dir


class TestBasicAdd(unittest.TestCase):
    def setUp(self):
        self.port = os.getenv("PORT", "/dev/ttyACM0")
        self.controller = ProcessorCIInterface(self.port, 115200, 1)

    def test_add(self):
        dados, size = read_file("/eda/processor-ci-tests/tests/memory/001-add.hex")
        id = self.controller.get_module_id()
        self.controller.set_timeout(200)
        self.controller.set_execution_end_address(60)
        self.controller.write_from_accumulator(size, dados)
        self.controller.execute_until_stop()
        retorno = self.controller.read_memory(60)
        self.assertEqual(int.from_bytes(retorno, 'big'), 10)


if __name__ == "__main__":
    with open("test-reports/results_basicadd.xml", "wb") as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))

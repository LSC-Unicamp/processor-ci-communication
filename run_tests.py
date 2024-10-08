import os
import time
import unittest
import xmlrunner


if __name__ == '__main__':
    # Diretório onde os testes estão localizados
    test_dir = '/eda/processor-ci-communication/tests'

    # Descobrir todos os testes dentro do diretório
    suite = unittest.defaultTestLoader.discover(test_dir, pattern="*.py")

    # Criar a pasta para os relatórios XML, se não existir
    os.makedirs('test-reports', exist_ok=True)

    # Executar os testes e salvar os resultados em formato XML
    with open(f'test-reports/results_{time.time()}.xml', 'w') as output:
        xmlrunner.XMLTestRunner(output=output).run(suite)
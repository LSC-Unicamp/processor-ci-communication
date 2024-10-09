import os
import time
import unittest
import xmlrunner

if __name__ == '__main__':
    # Diretório onde os testes estão localizados
    test_dir = '/eda/processor-ci-communication/tests'

    # Descobrir todos os testes dentro do diretório
    test_suites = unittest.defaultTestLoader.discover(test_dir, pattern="*.py")

    # Criar a pasta para os relatórios XML, se não existir
    os.makedirs('test-reports', exist_ok=True)

    # Iterar sobre cada arquivo de teste
    for test_suite in test_suites:
        # Para cada suite de teste, percorra os casos de teste
        for test_case in test_suite:
            # Gera um nome de arquivo único com base no nome da suite e no timestamp
            test_case_name = test_case.__class__.__name__
            timestamp = str(int(time.time()))
            report_file = f'test-reports/results_{test_case_name}_{timestamp}.xml'

            # Executar os testes e salvar os resultados em arquivos separados
            with open(report_file, 'wb') as output:
                xmlrunner.XMLTestRunner(output=output).run(test_case)

import os
import argparse
from core.shell import ProcessorCIInterfaceShell
from core.serial import ProcessorCIInterface


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
        "-T", "--test_program", help="Programa de teste a ser carregado no controlador"
    )
    parser.add_argument(
        "-d",
        "--test_directory",
        help="Diretório com os programas de teste a serem carregados no controlador",
    )
    parser.add_argument(
        "-s",
        "--shell",
        help="Inicia um shell de comunicação com o controlador",
        action="store_true",
    )
    args = parser.parse_args()

    if args.shell:
        shell = ProcessorCIInterfaceShell(args.port, args.baudrate, args.timeout)
        shell.cmdloop()


if __name__ == "__main__":
    main()

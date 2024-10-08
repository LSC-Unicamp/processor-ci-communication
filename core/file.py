import os
import glob


def read_file(path: str) -> tuple[list[str], int]:
    if not os.path.isfile(path):
        FileNotFoundError(f"Erro: O arquivo '{path}' não foi encontrado.")

    file = open(file)
    data = []

    for line in file.readlines():
        data.append(line)

    return data, len(data)


def list_files_in_dir(path: str) -> list[str]:
    try:
        return [
            file
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file))
        ]
    except FileNotFoundError:
        print(f"Erro: O diretório '{path}' não foi encontrado.")
        return []
    except Exception as e:
        print(f"Erro: {e}")
        return []


def open_files_in_dir(path: str) -> list[dict[str, list[str]]]:
    files_content = []
    try:
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data = f.readlines()
                files_content.append({file_name: [line.strip() for line in file_data]})
    except FileNotFoundError:
        print(f"Erro: O diretório '{path}' não foi encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

    return files_content

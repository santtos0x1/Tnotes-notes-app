def load_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            return text
    except Exception as e:
        raise Exception(f"Erro ao abrir o arquivo: {e}")
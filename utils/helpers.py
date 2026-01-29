# Вспомогательные функции

import os
import yaml
from datetime import datetime

def ensure_directory(path: str):
    # Создаем каталог, если он не существует
    os.makedirs(path, exist_ok=True)

def load_yaml_file(file_path: str):
    # Загружает файл YAML
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"File upload error {file_path}: {e}")
        return None

def get_timestamp():
    # Возвращаем текущую временную метку
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_separator(title: str = ""):
    # Печатает разделитель c заголовком
    if title:
        print(f"\n{'='*50}")
        print(f" {title}")
        print(f"{'='*50}")
    else:
        print(f"\n{'='*50}")
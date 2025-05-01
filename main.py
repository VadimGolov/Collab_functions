import subprocess
import sys
import os
from pathlib import Path
from urllib.parse import quote_plus
from loguru import logger

# ==== КОНФИГУРАЦИЯ ====
GITHUB_USERNAME = 'VadimGolov'  # ← Замени на свой GitHub логин
GITHUB_REPO = 'https://github.com/VadimGolov/Collab_functions.git'  # ← Замени на имя репозитория
GITHUB_BRANCH = 'heicwebp_to_png'  # ← Или другую ветку, если нужно
# =======================


def run_command(command, cwd=None):
    """
    Запускает команду и возвращает вывод, либо логирует ошибку.
    """
    logger.debug(f'Выполняется команда: {command}')
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        logger.error(f'Ошибка при выполнении команды: {command}')
        logger.error(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()


def convert_py_to_ipynb(py_path: Path):
    """
    Конвертирует .py в .ipynb
    """
    ipynb_path = py_path.with_suffix('.ipynb')
    logger.info(f'Конвертация: {py_path.name} → {ipynb_path.name}')
    run_command(f'ipynb-py-convert {py_path} {ipynb_path}')
    return ipynb_path


def git_commit_and_push(file_path: Path):
    """
    Добавляет, коммитит и пушит .ipynb в Git
    """
    logger.info('Добавление файла в git...')
    run_command(f'git add {file_path}')

    logger.info('Создание коммита...')
    run_command(f'git commit -m "Auto update {file_path.name}"')

    logger.info('Отправка в репозиторий...')
    run_command('git push')


def generate_colab_link(file_path: Path):
    """
    Создает ссылку на открытие файла в Google Colab
    """
    rel_path = file_path.relative_to(Path.cwd()).as_posix()
    url = f'https://colab.research.google.com/github/{GITHUB_USERNAME}/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{quote_plus(rel_path)}'
    logger.success(f'Colab URL: {url}')
    return url


def main():
    if len(sys.argv) != 2:
        logger.error('Укажите путь к .py файлу: python sync_to_colab.py my_script.py')
        sys.exit(1)

    py_file = Path(sys.argv[1])
    if not py_file.exists() or py_file.suffix != '.py':
        logger.error('Файл не найден или не является .py')
        sys.exit(1)

    ipynb_file = convert_py_to_ipynb(py_file)
    git_commit_and_push(ipynb_file)
    generate_colab_link(ipynb_file)


if __name__ == '__main__':
    main()
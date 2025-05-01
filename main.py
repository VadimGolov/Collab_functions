import subprocess
import sys
# import pyperclip
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus
from loguru import logger

from bracher import select_branch

# ==== КОНФИГУРАЦИЯ ====
GITHUB_USERNAME = 'VadimGolov'  # ← Замени на свой GitHub логин
GITHUB_REPO = 'https://github.com/VadimGolov/Collab_functions.git'  # ← Замени на имя репозитория
GITHUB_BRANCH = select_branch()  # ← Или другую ветку, если нужно
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


def convert_py_to_ipynb(py_path: Path, cwd: Path):
    """
    Конвертирует .py в .ipynb
    """
    ipynb_path = py_path.with_suffix('.ipynb')
    logger.info(f'Конвертация: {py_path.name} → {ipynb_path.name}')
    run_command(f'ipynb-py-convert {py_path} {ipynb_path}', cwd=cwd)
    return ipynb_path


def git_commit_and_push(file_path: Path, cwd: Path):
    """
    Добавляет, коммитит и пушит .ipynb в Git
    """
    logger.info('Добавление файла в git...')
    run_command(f'git add {file_path}', cwd=cwd)

    logger.info('Создание коммита...')
    run_command(f'git commit -m "Auto update {file_path.name}"', cwd=cwd)

    logger.info('Отправка в репозиторий...')
    run_command('git push', cwd=cwd)


def generate_colab_link(file_path: Path, cwd: Path):
    """
    Создает ссылку на открытие файла в Google Colab
    """
    rel_path = file_path.relative_to(cwd).as_posix()
    url = f'https://colab.research.google.com/github/{GITHUB_USERNAME}/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{quote_plus(rel_path)}'
    logger.success(f'Colab URL: {url}')
    # try:
    #     pyperclip.copy(url)
    #     logger.info('Ссылка скопирована в буфер обмена.')
    # except pyperclip.PyperclipException:
    #     logger.warning('Не удалось скопировать в буфер обмена. Для Linux установи xclip или pbcopy для Mac.')
    try:
        webbrowser.open_new_tab(url)
        logger.info('Ссылка открыта в браузере.')
    except Exception as e:
        logger.warning(f'Не удалось открыть браузер: {e}')

    return url


def main():
    # Определяем текущую рабочую директорию проекта
    project_root = Path('D:\Storage\Zerocoder\Showcase\Collab_functions')

    # Находим все .py-файлы, кроме main.py
    py_files = list(project_root.glob('*.py'))

    if len(py_files) == 0:
        logger.error('В этом проекте нет .py-файлов')
        sys.exit(1)
    elif len(py_files) > 1:
        logger.error('В этом проекте найдено несколько .py-файлов. Необходим только один.')
        for f in py_files:
            logger.error(f' - {f.name}')
        sys.exit(1)

    py_file = py_files[0].resolve()
    logger.info(f'Найден файл: {py_file.name}')

    ipynb_file = convert_py_to_ipynb(py_file, cwd=project_root)
    git_commit_and_push(ipynb_file, cwd=project_root)
    generate_colab_link(ipynb_file, cwd=project_root)


if __name__ == '__main__':
    main()
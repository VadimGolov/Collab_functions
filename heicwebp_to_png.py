from pathlib import Path


def heicwebp_to_png(arguments: dict[str, str | list | bool]):
    from pathlib import Path
    from PIL import Image, UnidentifiedImageError
    from pillow_heif import register_heif_opener

    """
     Конвертирует файлы *.heic и *.webp в формат png.

    Для выполнения конвертации функция использует библиотеку pillow_heif (register_heif_opener)
    Для работы с файловой системой используется библиотека pathlib:
    Валидация путей, создание необходимых папок, управление перезаписью файлов.

    Для описания аргументов предполагается что я передаю несколько файлов для конвертации.
    Но функция будет работать и с одним файлом.

    Args:
        arguments (dict): Словарь с параметрами функции:
            - input_path (str): Список из полных путей к исходным файлам (с указанием имен файлов). Обязательный.
            - output_path (str, optional): По умолчанию папка с исходными файлами. Полный путь папке для сохранения PNG-файлов. Не обязательный.
            - overwrite (bool, optional): По умолчанию True. Перезаписать выходные файлы, если файлы с такими именами существуют. Не обязательный.

    Returns:
        dict: Результат выполнения операции status : ('success' или 'error'),
        message : ('сообщение об ошибке'). При успехе, возвращает полный путь к созданным файлам (без указания их имен) (output_path).

    """
    # Проверяем, что arguments — это словарь
    if not isinstance(arguments, dict):
        message: str = 'Аргументы должны быть переданы в виде словаря'
        return {'status': 'error', 'message': message}

    # Проверка input_path
    input_path = arguments.get('input_path', None)

    if input_path is None:
        err_code = 0
    elif not isinstance(input_path, str):
        err_code = 1
    elif not Path(input_path).is_file():
        err_code = 2
    elif not Path(input_path).suffix in ('.heic', '.webp'):
        err_code = 3
    else:
        err_code = -1

    input_error = ['Обязательный параметр input_path отсутствует',
                   'Параметр input_path должен быть должен быть строкой',
                   f'Файл: {input_path} не найден',
                   f'Файл {input_path} должен иметь тип .heic или .webp']

    if err_code != -1:
        return {'status': 'error', 'message': input_error}

    # Проверка output_path
    output_path = arguments.get('output_path', None)

    if output_path is None:
        output_path = Path(input_path).parent
    elif not isinstance(output_path, str):
        err_code = 0
    elif not Path(output_path).is_dir():
        err_code = 1
    else:
        err_code = -1

    output_error = ['Параметр output_path должен быть строкой',
                    f'Папка: {output_path} не найдена или не является папкой']

    if err_code != -1:
        return {'status': 'error', 'message': output_error}

    # Проверка overwrite
    overwrite = arguments.get('overwrite', True)
    if not isinstance(overwrite, bool):
        return {'status': 'error', 'message': '"overwrite" должен быть типа bool'}

    # Проверка show_progress
    # show_progress = arguments.get('show_progress', True)
    # if not isinstance(show_progress, bool):
    #     return {'status': 'error', 'message': '"show_progress" должен быть типа bool'}

    # Конвертация фото

    register_heif_opener()

    try:
        src_image: Image = Image.open(input_path)

    except UnidentifiedImageError:
        return {'status': 'error', 'message': f'Не удалось открыть файл {input_path}'}

    output_name = Path(input_path).stem + '.png'
    output_image = Path(output_path, output_name)

    if overwrite:
        src_image.save(output_image)
    else:
        number = 1
        while output_image.exists():
            output_name = Path(input_path).stem + f'[{number}].png'
            output_image = Path(output_path, output_name)
            number += 1

        src_image.save(output_image)

    src_image.close()

    return {'status': 'success', 'message': f'{output_image}'}
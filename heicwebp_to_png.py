def heicwebp_to_png(arguments: dict[str, str | bool]) -> dict[str, str]:

    from pathlib import Path
    from PIL import Image, UnidentifiedImageError
    from pillow_heif import register_heif_opener

    """
     Конвертирует файл *.heic и *.webp в формат png.

    Для выполнения конвертации функция использует библиотеку pillow_heif (register_heif_opener)
    Для работы с файловой системой используется библиотека pathlib:
    Валидация путей, создание необходимых папок, управление перезаписью файлов.

    На данный момент функция может работать только с одним файлом.

    Args:
        arguments (dict): Словарь с параметрами функции:
            - input_path (str): Полный путь к исходному файлу (с указанием имени файла). Обязательный.
            - output_path (str, optional): По умолчанию папка с исходным файлом. Полный путь папке для сохранения PNG-файла. Не обязательный.
            - overwrite (bool, optional): По умолчанию True. Перезаписать выходной файл, если файл с такими именем существует. Не обязательный.

    Returns:
        dict: Результат выполнения операции status : ('success' или 'error'),
        message : ('сообщение об ошибке'). При успехе, возвращает полный путь к созданному файлу (с указанием имени файла) (output_path).

    """
    # Проверяем, что arguments — это словарь
    print(f'arguments {arguments}')
    if not isinstance(arguments, dict):
        message: str = 'Аргументы должны быть переданы в виде словаря'
        print({'status': 'error', 'message': message})
        return {'status': 'error', 'message': message}

    # Проверка input_path
    input_path: str | None = arguments.get('input_path', None)

    if input_path is None:
        err_code: int = 0
    elif not isinstance(input_path, str):
        err_code: int = 1
    elif not Path(input_path).is_file():
        err_code: int = 2
    elif not Path(input_path).suffix in ('.heic', '.webp', '.HEIC', '.WEBP'):
        err_code: int = 3
    else:
        err_code: int = -1

    input_error: list[str] = ['Обязательный параметр input_path отсутствует',
                              'Параметр input_path должен быть должен быть строкой',
                              f'Файл: {input_path} не найден',
                              f'Файл {input_path} должен иметь тип .heic или .webp']

    if err_code != -1:
        print({'status': 'error', 'message': input_error[err_code]})
        return {'status': 'error', 'message': input_error[err_code]}

    # Проверка output_path
    output_path: str | None = arguments.get('output_path', None)

    if output_path == '' or output_path is None:
        output_path: Path = Path(input_path).parent
    elif not isinstance(output_path, str):
        err_code: int = 0
    elif not Path(output_path).is_dir():
        err_code: int = 1
    else:
        err_code: int = -1

    output_error: list[str] = ['Параметр output_path должен быть строкой',
                               f'Папка: {output_path} не найдена или не является папкой']

    if err_code != -1:
        print({'status': 'error', 'message': output_error[err_code]})
        return {'status': 'error', 'message': output_error[err_code]}

    # Проверка overwrite
    overwrite: bool = arguments.get('overwrite', True)
    if not isinstance(overwrite, bool):
        print({'status': 'error', 'message': '"overwrite" должен быть типа bool'})
        return {'status': 'error', 'message': '"overwrite" должен быть типа bool'}

    # Конвертация фото

    register_heif_opener()

    try:
        src_image: Image = Image.open(input_path)

    except UnidentifiedImageError:
        print({'status': 'error', 'message': f'Не удалось открыть файл {input_path}'})
        return {'status': 'error', 'message': f'Не удалось открыть файл {input_path}'}

    if overwrite:
        output_name: str = Path(input_path).stem + '.png'
        output_image: Path = Path(output_path, output_name)

    else:
        number: int = 1
        output_name: str = Path(input_path).stem + f'[{number}].png'
        output_image: Path = Path(output_path, output_name)

        while output_image.exists():
            number += 1
            output_name: str = Path(input_path).stem + f'[{number}].png'
            output_image: Path = Path(output_path, output_name)

    try:
        src_image.save(output_image)
    finally:
        src_image.close()
        print({'status': 'success', 'message': f'{output_image}'})
        return {'status': 'success', 'message': f'{output_image}'}

if __name__ == '__main__':

    heicwebp_to_png(arguments={'input_path': 'D:\Storage\Zerocoder\heic\IMG_4442.HEIC', 'output_path': 'D:\Storage\Zerocoder\heic\png', 'overwrite': True})
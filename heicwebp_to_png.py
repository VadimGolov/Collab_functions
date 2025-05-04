def heicwebp_to_png(arguments: dict[str, str | bool]) -> dict[str, str]:

    import requests
    from io import BytesIO
    from pathlib import Path
    from PIL import Image, UnidentifiedImageError
    from pillow_heif import register_heif_opener
    from urllib.parse import urlparse

    """
    Конвертирует изображение в формате .heic или .webp в формат .png.  
    Поддерживает как локальные пути к файлам, так и URL-ссылки на изображения.

    Функция предназначена для использования в автоматизированных пайплайнах обработки изображений
    и применима в задачах, где требуется конвертация HEIC/WebP-файлов в PNG без использования стороннего ПО.

    Используемые библиотеки:
        - `pathlib` — для валидации и управления путями к файлам и директориям.
        - `pillow_heif` — для поддержки формата HEIC (регистрирует обработчик формата для Pillow).
        - `PIL` (Pillow) — основная библиотека для работы с изображениями.
        - `requests` — для загрузки изображений по URL.
        - `io.BytesIO` — для открытия изображения из байтового потока.
        - `urllib.parse` — для разбора URL-ссылок и получения имени файла.

    Аргументы:
        arguments (dict):
            - input_path (str): Обязательный. Путь к изображению.  
              Может быть как локальным:
                  Windows:  'D:\\Pictures\\my_image.heic' или r'D:\Pictures\my_image.heic' (сырая строка)
                  POSIX:    '/home/user/images/my_image.webp'
              Так и URL-ссылкой:
                  'https://example.com/images/sample.webp'
            - output_path (str, optional): Путь к директории, в которую будет сохранён PNG-файл.  
              Если не указан, используется директория, где находится входной файл (или временная директория при URL).
            - overwrite (bool, optional): По умолчанию True.  
              Если False и файл уже существует, к имени будет добавлен индекс в квадратных скобках (например: `my_image[1].png`).

    Возвращает:
        dict:
            - status (str): `'success'` при успешной конвертации, `'error'` при возникновении ошибки.
            - message (str): При успехе — полный путь к сохранённому файлу PNG.  
                             При ошибке — человекочитаемое описание проблемы.

    Примеры вызова:
        >>> heicwebp_to_png({
                'input_path': 'D:/Pictures/photo.HEIC',
                'output_path': 'D:/Pictures/converted',
                'overwrite': False
            })

        >>> heicwebp_to_png({
                'input_path': 'https://www.gstatic.com/webp/gallery/1.webp'
            })
    """

    # Проверяем, что arguments — это словарь
    if not isinstance(arguments, dict):
        message: str = 'Аргументы должны быть переданы в виде словаря'
        print({'status': 'error', 'message': message})
        return {'status': 'error', 'message': message}

    # Проверка input_path
    input_path: str | None = arguments.get('input_path', None)
    url_link: bool = False

    if input_path is None:
        err_code: int = 0
    elif not isinstance(input_path, str):
        err_code: int = 1
    else:
        parsed = urlparse(input_path)
        url_link = parsed.scheme in ('http', 'https') and parsed.netloc != ''
        if not url_link and not Path(input_path).is_file():
            err_code: int = 2
        elif not Path(input_path).suffix.lower() in ('.heic', '.webp'):
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
        print({'status': 'error', 'message': 'Параметр output_path должен быть строкой'})
        return {'status': 'error', 'message': 'Параметр output_path должен быть строкой'}
    elif not Path(output_path).is_dir():
        new_path = Path(output_path)
        new_path.mkdir(parents=True, exist_ok=True)

    # Проверка overwrite
    overwrite: bool = arguments.get('overwrite', True)
    if not isinstance(overwrite, bool):
        print({'status': 'error', 'message': '"overwrite" должен быть типа bool'})
        return {'status': 'error', 'message': '"overwrite" должен быть типа bool'}

    # Конвертация фото

    register_heif_opener()

    if url_link:

        try:
            response = requests.get(input_path)
        except requests.RequestException:
            return {'status': 'error', 'message': f'Ошибка при загрузке изображения'}

        src_image: Image = Image.open(BytesIO(response.content))
        image_stem = Path(urlparse(input_path).path).stem
    else:

        try:
            src_image: Image = Image.open(input_path)
        except UnidentifiedImageError:
            print({'status': 'error', 'message': f'Не удалось открыть файл {input_path}'})
            return {'status': 'error', 'message': f'Не удалось открыть файл {input_path}'}

        image_stem = Path(input_path).stem

    if overwrite or not Path(output_path, image_stem + '.png').exists():
        output_image: Path = Path(output_path, image_stem + '.png')

    else:
        number: int = 1
        output_image: Path = Path(output_path, image_stem + f'[{number}].png')
        while output_image.exists():
            number += 1
            output_image: Path = Path(output_path, image_stem + f'[{number}].png')

    try:
        src_image.save(output_image)
    finally:
        src_image.close()
        print({'status': 'success', 'message': f'{output_image}'})
        return {'status': 'success', 'message': f'{output_image}'}


if __name__ == '__main__':
    # options = {'input_path': 'https://www.gstatic.com/webp/gallery/1.webp', 'output_path': r'D:\Storage\Zerocoder\heic', 'overwrite': False}
    options = {'input_path': r'D:\Storage\Zerocoder\heic\IMG_4443.HEIC', 'output_path': r'D:\Storage\Zerocoder\heic'}
    heicwebp_to_png(options)
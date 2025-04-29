# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
# ---

# %%
def heicwebp_to_png(arguments: dict[str, str | list]) -> dict[str, str]:
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
            - show_progress (bool, optional): По умолчанию True. Отображать прогресс-бар конвертации. Не обязательный.

    Returns:
        dict: Результат выполнения операции со статусом ('success' или 'error'),
        сообщением (str). При успехе, полным путем к созданным файлам (без указания их имен) (output_path).

    """
    print(arguments)
    return arguments

# %% [markdown]
# def validate_arguments(arguments: dict) -> dict:
#     # Проверяем, что arguments — это словарь
#     if not isinstance(arguments, dict):
#         return {"status": "error", "message": "Аргументы должны быть переданы в виде словаря."}
#
#     # Проверка input_path
#     input_path = arguments.get('input_path')
#     if input_path is None:
#         return {"status": "error", "message": "Обязательный параметр 'input_path' отсутствует."}
#     elif not isinstance(input_path, list):
#         return {"status": "error", "message": "Параметр 'input_path' должен быть списком."}
#
#     if isinstance(input_path, str):
#         input_path = [input_path]  # Преобразуем один путь в список
#     elif not isinstance(input_path, list):
#         return {"status": "error", "message": "Параметр 'input_path' должен быть строкой или списком строк."}
#
#     # Проверяем каждый путь в input_path
#     validated_input_paths = []
#     for path_str in input_path:
#         path = Path(path_str)
#         if not path.is_file():
#             return {"status": "error", "message": f"Файл не найден: {path}"}
#         validated_input_paths.append(path)
#
#     # Проверка output_path
#     output_path = arguments.get('output_path')
#     if output_path is not None:
#         output_dir = Path(output_path)
#         if output_dir.exists() and not output_dir.is_dir():
#             return {"status": "error", "message": f"Указанный 'output_path' не является папкой: {output_path}"}
#         # Создаём папку, если её нет
#         output_dir.mkdir(parents=True, exist_ok=True)
#     else:
#         # Если output_path не указан, берем папку первого файла
#         output_dir = validated_input_paths[0].parent
#
#     # Проверка overwrite
#     overwrite = arguments.get('overwrite', True)
#     if not isinstance(overwrite, bool):
#         return {"status": "error", "message": "'overwrite' должен быть типа bool."}
#
#     # Проверка show_progress
#     show_progress = arguments.get('show_progress', True)
#     if not isinstance(show_progress, bool):
#         return {"status": "error", "message": "'show_progress' должен быть типа bool."}
#
#     # Все аргументы валидны, возвращаем их в нужной форме
#     return {
#         "status": "success",
#         "input_paths": validated_input_paths,
#         "output_path": output_dir,
#         "overwrite": overwrite,
#         "show_progress": show_progress
#     }
#
# from typing import Iterator
# from pathlib import Path
# from PIL import Image, UnidentifiedImageError
# from pillow_heif import register_heif_opener
#
# # Проверка типа входного словаря аргументов - первый и критически важный шаг.
# if not isinstance(arguments, dict):
#     message = "Аргументы должны быть словарем (dict)."
#     return {"status": "error", "message": message}
#
# # Извлечение обязательных строковых аргументов
# input_img_path = arguments.get('input_path')
# if not isinstance(input_img_path, list):
#   message = "Файлы для конвертации должны быть переданны в виде списка."
#   return {"status": "error", "message": message}
#
# output_img_path = arguments.get('output_path')
# if not output_img_path:
#     output_img_path = Path(output_img_path[0]).parent
#
# # Проверка наличия и типа обязательных строковых аргументов.
# # Возврат ошибки, если они отсутствуют или имеют некорректный тип/значение.
# if not isinstance(input_video_path, str) or not input_video_path:
#     message = "Отсутствует или имеет некорректный тип обязательный параметр 'input_path' (ожидается непустая строка)."
#     # Логгер функции еще может быть не полностью настроен, используем базовый логгер.
#     logger = logging.getLogger(__name__)
#     logger.error(message)
#     return {"status": "error", "message": message}
# if not isinstance(output_audio_path, str) or not output_audio_path:
#     message = "Отсутствует или имеет некорректный тип обязательный параметр 'output_path' (ожидается непустая строка)."
#     # Используем базовый логгер.
#     logger = logging.getLogger(__name__)
#     logger.error(message)
#     return {"status": "error", "message": message}
#
# # Извлечение необязательных аргументов с значениями по умолчанию.
# overwrite_existing = arguments.get('overwrite', False)
# safe_base_directory = arguments.get('safe_base_directory', '/content/')
# log_level_str = arguments.get('log_level', 'INFO')
# show_progress_bar = arguments.get('show_progress', True)
#
# # Проверка типа 'safe_base_directory' (должна быть непустой строкой).
# if not isinstance(safe_base_directory, str) or not safe_base_directory:
#      message = "Отсутствует или имеет некорректный тип необязательный параметр 'safe_base_directory' (ожидается непустая строка)."
#      # Используем базовый логгер.
#      logger = logging.getLogger(__name__)
#      logger.error(message)
#      return {"status": "error", "message": message}
#
#
# def get_path(initdir: Path) -> Path:
#     path: str = ask_path(title='HEIC Convereter - Выберите папку', initialdir=initdir, mustexist=True)
#
#     if not path:
#         print('В меню выбора папки была нажата кнопка "Отмена"')
#         input('\nДля завершения программы нажмите Enter')
#         sys.exit(1)
#
#     return Path(path)
#
#
# def create_photo(img_path: Path) -> None | list[str]:
#
#     bad_images: list[str] = []
#
#     heic_images: list[Path] = list(img_path.glob('*.heic'))
#     webp_images: list[Path] = list(img_path.glob('*.webp'))
#
#     if heic_images and webp_images:
#         new_images: list[Path] = heic_images + webp_images
#     elif heic_images:
#         new_images: list[Path] = heic_images
#     elif webp_images:
#         new_images: list[Path] = webp_images
#     else:
#         print('В папке не найдено ни одного изображения heic или webp')
#         input('\nДля завершения программы нажмите Enter')
#         sys.exit(1)
#
#     progress_bar: Iterator = screen_decor.process_bar(title='Обработано файлов: ', max_value=len(new_images))
#
#     for num_image, one_image in enumerate(new_images, start=1):
#
#         next(progress_bar)
#         photo_out: Path = Path(img_path, one_image.stem + '.png')
#
#         image_error: str = save_image(one_image, photo_out)
#
#         if image_error:
#             bad_images.append(image_error)
#
#     if bad_images:
#         return bad_images
#     else:
#         return None
#
#
# def save_image(input_file: Path, output_file: Path, ) -> None | str:
#
#     register_heif_opener()
#
#     try:
#         src_image: Image = Image.open(input_file)
#
#     except UnidentifiedImageError:
#         return f'{input_file.name} - не удалось открыть файл'
#
#     if not src_image:
#         return None
#
#     output_image: Image = src_image
#
#     output_image.save(output_file)
#     output_image.close()
#
#     src_image.close()
#
#
#
# if __name__ == '__main__':
#
#     # Рабочая папка
#     work_folder: Path = Path.cwd()
#
#     # Папка с картинками
#     main_folder: Path = get_path(initdir=work_folder)
#     info: list[str] = create_photo(main_folder)
#
#     if info:
#         print(info)

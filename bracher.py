import tkinter as tk
from tkinter import ttk
import subprocess


def get_branches():
    """
    Получить список всех веток репозитория
    """
    all_branches = subprocess.check_output(['git', 'branch', '--list']).strip().decode('utf-8').split('\n')
    return [one_branch.strip('* ').strip() for one_branch in all_branches]


def select_branch():
    """
    Создает окно для выбора ветки из списка branches и возвращает выбранную ветку
    """
    # Создание окна Tkinter
    root = tk.Tk()
    root.title('Выбор ветки')
    root.configure(bg='#2E2E2E')  # Темная тема
    root.geometry('380x140')
    root.resizable(False, False)

    # Лейбл
    label = tk.Label(root, text='Выберите ветку  репозитория Collab_functions', font=('Arial', 12), fg='white', bg='#2E2E2E')
    label.pack(pady=5)

    # Получение списка веток
    branch_heap = get_branches()

    # Список выбора веток
    branch_var = tk.StringVar()
    branch_var.set(branch_heap[0])  # Установим первую ветку по умолчанию
    branch_menu = ttk.Combobox(root, textvariable=branch_var, values=branch_heap, font=('Arial', 11), state='readonly', width=30)
    branch_menu.pack(pady=10)

    # Кнопка для подтверждения выбора
    def on_select():
        selected_branch = branch_var.get()
        root.quit()  # Закрыть окно после выбора
        root.destroy()
        return selected_branch

    button = tk.Button(root, text='Выбрать', command=on_select, font=('Arial', 11), bg='#505050', fg='white')
    button.pack(pady=10)

    # Запуск окна
    root.mainloop()

    return branch_var.get()
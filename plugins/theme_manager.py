# theme_manager.py
import flet as ft
import json
import os

# Путь к папке serverShiDari
SERVER_DIR = r"C:\serverShiDari"
os.makedirs(SERVER_DIR, exist_ok=True)  # Создаем папку, если её нет

# Путь к файлу настроек
SETTINGS_FILE = os.path.join(SERVER_DIR, "theme_settings.json")

# Функция загрузки темы
def load_theme():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            data = json.load(file)
            return data.get("theme", "light")
    return "light"

# Функция сохранения темы
def save_theme(theme):
    with open(SETTINGS_FILE, "w") as file:
        json.dump({"theme": theme}, file)

# Функция создания кнопки для переключения темы
def create_theme_button(page: ft.Page):
    page.theme_mode = load_theme()

    def toggle_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        save_theme(page.theme_mode)
        icon_button.icon = (
            ft.icons.WB_SUNNY if page.theme_mode == "dark" else ft.icons.NIGHTS_STAY
        )
        icon_button.update()
        page.update()

    icon_button = ft.IconButton(
        icon=ft.Icons.WB_SUNNY if page.theme_mode == "dark" else ft.Icons.NIGHTS_STAY,
        on_click=toggle_theme,
    )
    return icon_button
import flet as ft
import aiohttp
import sqlite3
import bcrypt
import time
from pages.home import home_page
from pathlib import Path

# Конфигурация сервера
SERVER_IP = "192.168.1.103"
SERVER_PORT = 8000
SCAN_INTERVAL = 600

# Пути для файлов
BASE_DIR = Path(__file__).parent.resolve()
SAVE_DIR = BASE_DIR / "backend"
SAVE_DIR.mkdir(exist_ok=True)
DEFAULT_DB_PATH = SAVE_DIR / "back.db"
IMGS_DIR = SAVE_DIR / "Imgs"
IMGS_DIR.mkdir(exist_ok=True)
LAST_SYNC_PATH = SAVE_DIR / "last_sync.txt"

async def get_server_db_hash():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{SERVER_IP}:{SERVER_PORT}/db_hash") as response:
                return await response.text()
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def get_local_db_hash():
    return open(LAST_SYNC_PATH, "r").read() if LAST_SYNC_PATH.exists() else ""

async def download_db():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{SERVER_IP}:{SERVER_PORT}/download_db") as response:
                with open(DEFAULT_DB_PATH, "wb") as f:
                    f.write(await response.read())
                print("DB downloaded successfully")
    except Exception as e:
        print(f"DB download failed: {e}")

async def download_imgs():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{SERVER_IP}:{SERVER_PORT}/list_imgs") as response:
                if response.ok:
                    files = (await response.json()).get("files", [])
                    print(f"Files to download: {files}")

                    for file in files:
                        start_time = time.time()
                        img_url = f"http://{SERVER_IP}:{SERVER_PORT}/download_img/{file}"
                        async with session.get(img_url) as img_response:
                            if img_response.status == 200:
                                img_data = await img_response.read()
                                (IMGS_DIR / file).write_bytes(img_data)
                                end_time = time.time()
                                file_size = len(img_data) / 1024
                                print(
                                    f"Изображение {file} скачано за {end_time - start_time:.2f} секунд. Размер: {file_size:.2f} КБ"
                                )
                            else:
                                print(f"Ошибка при скачивании {file}. Статус: {img_response.status}")
                else:
                    print(f"Ошибка при получении списка файлов. Статус: {response.status}")
    except Exception as e:
        print(f"Ошибка при скачивании изображений: {e}")

async def check_server():
    try:
        server_hash = await get_server_db_hash()
        local_hash = get_local_db_hash()

        if server_hash and server_hash != local_hash:
            await download_db()
            await download_imgs()
            with open(LAST_SYNC_PATH, "w") as f:
                f.write(server_hash)
    except Exception as e:
        print(f"Ошибка: {e}")
        raise  # Пробрасываем исключение дальше

async def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    await loading(page)
    home_page(page)

async def loading(page):
    # Создаем ProgressRing
    progress_ring = ft.ProgressRing(visible=True)
    # Создаем контейнер для ProgressRing с полупрозрачным фоном
    loading_container = ft.Container(
        content=progress_ring,
        alignment=ft.alignment.center,
        expand=True,
    )

    # Добавляем контейнер с ProgressRing на страницу
    page.add(loading_container)
    page.update()

    try:
        # Запускаем проверку сервера
        await check_server()
    except Exception as e:
        print(f"Ошибка при проверке сервера: {e}")
        # Показываем сообщение об ошибке
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка подключения: {e}"))
        page.snack_bar.open = True
    finally:
        # Скрываем ProgressRing после завершения загрузки или ошибки
        loading_container.visible = False
        page.update()

def login_page(page: ft.Page):
    def check_login(username, password):
        conn = sqlite3.connect(DEFAULT_DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return False

        stored_hash = result[0].encode('utf-8')

        try:
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except:
            return False

    def on_login_click(e):
        username = user_login.current.value
        password = user_pass.current.value

        if check_login(username, password):
            page.clean()
            home_page(page)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Неверный логин или пароль"))
            page.snack_bar.open = True
            page.update()

    user_login = ft.Ref[ft.TextField]()
    user_pass = ft.Ref[ft.TextField]()

    login_form = ft.Container(
        content=ft.Column(
            [
                ft.Text("Авторизация", size=24),
                ft.TextField(label="Логин", width=250, ref=user_login),
                ft.TextField(label="Пароль", width=250, password=True, ref=user_pass),
                ft.ElevatedButton(text="Войти", on_click=on_login_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )

    # Добавляем форму входа на страницу
    page.add(login_form)

if __name__ == "__main__":
    ft.app(target=main)
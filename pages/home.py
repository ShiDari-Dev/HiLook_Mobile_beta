import flet as ft
from pages.catalogue import categories_page
from pages.tovari import items_page  # Импортируем items_page
from plugins.theme_manager import create_theme_button

def home_page(page: ft.Page):
    # Контейнер для динамического содержимого
    content_container = ft.Container(expand=True)

    def show_categories():
        # Показываем список категорий
        content_container.content = categories_page(page, on_category_click)
        page.update()  # Обновляем страницу

    def show_items(category_id):
        # Показываем список товаров выбранной категории
        content_container.content = items_page(page, category_id, on_back_click)
        page.update()  # Обновляем страницу

    def on_category_click(category_id):
        # Обработка клика по категории
        show_items(category_id)

    def on_back_click(e):
        # Обработка клика по кнопке "Назад"
        show_categories()

    # Инициализация содержимого первой вкладки
    show_categories()

    tab = ft.Tabs(
        selected_index=0,
        animation_duration=200,
        tabs=[
            ft.Tab(
                text="Товары и услуги",
                content=ft.Column([content_container], expand=True),
            ),
            ft.Tab(
                text="Посчитать",
                content=ft.Text("ЛОХ")  # Пример другого содержимого
            )
        ],
        expand=True,
    )

    appbar = ft.AppBar(
        title=ft.Row(
            controls=[ft.Text("ShiDari Informator")],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        ),
        actions=[
            ft.IconButton(ft.Icons.HOME, on_click=lambda e: home(page)),
            create_theme_button(page)
        ],
        bgcolor=ft.Colors.BLUE_500,
        toolbar_height=80
    )
    page.appbar = appbar

    # Добавляем вкладку на страницу
    page.add(tab)

def home(page):
    # Очищаем страницу и перезагружаем домашнюю страницу
    page.clean()
    home_page(page)
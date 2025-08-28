import flet as ft
from plugins.card_styles import create_card
from bdinit import get_categories
from pages.tovari import items_page

def create_category_card(category, on_click_handler):
    return ft.Container(
        content=create_card(
            title=category['name'],
            subtitle=f"Параметр: {category['parameter'] or 'Не указан'}",
            description=f"Ед. измерения: {category['unit']}",
            on_click_handler=lambda e: on_click_handler(category['id']),  # Передаем ID категории
            description_color=ft.Colors.BLUE_800,
        ),
        margin=ft.margin.all(1),  # Добавляем отступы вокруг карточки
        width=float("inf"),  # Растягиваем карточку на всю доступную ширину
        expand=True,  # Разрешаем растягивание
    )

def categories_page(page: ft.Page, on_category_click):
    categories = get_categories()
    if not categories:
        return ft.Text("Нет доступных категорий.")  # Возвращаем виджет с сообщением

    category_cards = ft.Column(
        [create_category_card(category, on_category_click) for category in categories],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.Container(content=category_cards, expand=True, padding=10)  # Возвращаем виджет
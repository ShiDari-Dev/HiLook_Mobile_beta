import flet as ft
from bdinit import get_items, get_categories
from pathlib import Path

# Пути к изображениям (должны быть импортированы из main.py)
IMGS_DIR = Path("backend/Imgs")  # Путь к папке с изображениями
DEFAULT_IMAGE_PATH = Path("default.jpg")  # Путь к изображению по умолчанию

def create_item_card(item, categories):
    image_id = item.get('image_id')
    if image_id:
        image_path = IMGS_DIR / f"{image_id}.jpg"  # Добавляем .jpg на клиенте
        if not image_path.exists():
            image_path = DEFAULT_IMAGE_PATH
    else:
        image_path = DEFAULT_IMAGE_PATH

    parameter_text = ""
    if item.get('parameter_value'):
        category = next((cat for cat in categories if cat['id'] == item['category_id']), None)
        if category and category.get('parameter'):
            parameter_text = f"{category['parameter']}: {item['parameter_value']}"
        else:
            parameter_text = f"Параметр: {item['parameter_value']}"

    card = ft.Card(
        content=ft.Column(
            controls=[
                ft.Image(
                    src=str(image_path),  # Используем локальный путь к изображению
                    width=100,
                    height=100,
                    fit=ft.ImageFit.COVER,
                    border_radius=ft.border_radius.all(10)),
                ft.Text(value=item['name'], weight=ft.FontWeight.BOLD, size=16),
                ft.Text(value=f"Ед. измерения: {item['unit']}", size=14),
                ft.Text(value=parameter_text, size=14) if parameter_text else None,
                ft.Divider(height=1, color=ft.colors.GREY_300),
                ft.Column(
                    controls=[
                        ft.Text(value=f"Цена : {item['selling_price']} UZS", color=ft.colors.ORANGE,
                                weight=ft.FontWeight.BOLD, size=16),
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        elevation=2,
        expand=False
    )
    return card


def items_page(page: ft.Page, category_id: int, on_back_click):
    # Получаем товары и категории
    items = get_items(category_id)
    categories = get_categories()

    # Создаем GridView для карточек товаров
    item_grid = ft.GridView(
        controls=[create_item_card(item, categories) for item in items],
        max_extent=250,  # Максимальная ширина карточки
        child_aspect_ratio=0.75,  # Соотношение сторон карточки (ширина / высота)
        spacing=10,  # Расстояние между элементами по горизонтали
        run_spacing=10,  # Расстояние между элементами по вертикали
        expand=True,  # Растягиваем на всю доступную ширину
    )

    # Создаем контейнер с GridView и кнопкой "Назад"
    content = ft.Column(
        controls=[
            item_grid,
            ft.ElevatedButton("Назад", on_click=on_back_click),
        ],
        expand=True,
    )

    return ft.Container(content=content, expand=True, padding=10)  # Возвращаем виджет
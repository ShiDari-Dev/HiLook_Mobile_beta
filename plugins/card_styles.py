import flet as ft

def create_card(
    *,
    title: str,
    subtitle: str = None,
    description: str = None,
    icon: str = None,
    image: str = None,
    on_click_handler=None,
    elevation: float = 2,
    margin: ft.margin = ft.margin.symmetric(vertical=5),
    padding: ft.padding = ft.padding.symmetric(vertical=15, horizontal=20),
    title_size: int = 16,
    subtitle_size: int = 14,
    description_size: int = 12,
    title_color: str = None,
    subtitle_color: str = None,
    description_color: str = None,
    image_width: int = 100,
    image_height: int = 100,
    base_image_url: str = "http://localhost:8000/imgs/"
) -> ft.Card:
    """
    Универсальная карточка с гибкой настройкой.
    
    :param title: Основной заголовок (обязательный)
    :param subtitle: Подзаголовок (опционально)
    :param description: Описание (опционально)
    :param icon: Иконка (опционально)
    :param image: URL или путь к изображению (опционально)
    :param on_click_handler: Обработчик клика
    :param elevation: Тень карточки
    :param margin: Отступы вокруг карточки
    :param padding: Внутренние отступы
    :param title_size: Размер шрифта заголовка
    :param subtitle_size: Размер шрифта подзаголовка
    :param description_size: Размер шрифта описания
    :param title_color: Цвет заголовка
    :param subtitle_color: Цвет подзаголовка
    :param description_color: Цвет описания
    :param image_width: Ширина изображения
    :param image_height: Высота изображения
    :param base_image_url: Базовый URL для изображений
    :return: Объект ft.Card
    """
    # Обработка изображения
    image_control = None
    if image:
        full_image_src = f"{base_image_url}{image}" if not image.startswith(("http://", "https://")) else image
        image_control = ft.Image(
            src=full_image_src,
            width=image_width,
            height=image_height,
            fit=ft.ImageFit.COVER
        )

    # Создание контента
    content_controls = []
    
    if icon:
        content_controls.append(ft.Icon(name=icon, size=title_size))
    
    content_controls.append(
        ft.Text(
            title,
            weight=ft.FontWeight.BOLD,
            size=title_size,
            color=title_color
        )
    )
    
    if subtitle:
        content_controls.append(
            ft.Text(
                subtitle,
                size=subtitle_size,
                color=subtitle_color
            )
        )
    
    if description:
        content_controls.append(
            ft.Text(
                description,
                size=description_size,
                color=description_color
            )
        )

    # Основной контейнер
    main_content = ft.Column(
        controls=content_controls,
        spacing=5,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    # Если есть изображение, добавляем его в Row
    if image_control:
        main_content = ft.Row(
            controls=[image_control, main_content],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    return ft.Card(
        content=ft.Container(
            content=main_content,
            padding=padding,
            on_click=on_click_handler
        ),
        elevation=elevation,
        margin=margin
    )
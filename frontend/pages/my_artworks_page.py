import flet as ft


class MyArtworksPage(ft.Container):
    def __init__(self, page: ft.Page, api, go_to_home_func):
        super().__init__()
        self._page = page
        self.api = api
        self.go_to_home = go_to_home_func

        self.expand = True
        self.alignment = ft.Alignment(0, 0)
        self.bgcolor = ft.Colors.BLACK

        title = ft.Text(
            "МОЁ ТВОРЧЕСТВО", size=36, color=ft.Colors.BLUE_300, weight="bold"
        )

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            tooltip="Назад в профиль",
            on_click=lambda _: self.go_to_home(),
        )

        self.status_text = ft.Text("", color=ft.Colors.GREEN_400, size=14)

        self.artworks_grid = ft.GridView(
            runs_count=3,
            max_extent=320,
            spacing=25,
            run_spacing=25,
            padding=ft.padding.only(top=80, left=20, right=20),
            expand=True,
        )

        top_bar = ft.Row(
            [
                back_button,
                ft.Container(expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        main_content = ft.Container(
            content=ft.Column(
                [
                    top_bar,
                    ft.Container(height=10),
                    title,
                    ft.Container(height=15),
                    self.status_text,
                    self.artworks_grid,
                ],
                spacing=0,
            ),
            alignment=ft.Alignment(0, 0),
            bgcolor=ft.Colors.BLACK_45,
            expand=True,
            padding=20,
        )

        self.content = main_content

        self._page.run_task(self.load_artworks)

    async def load_artworks(self):
        try:
            artworks = await self.api.get_my_artworks()

            if not artworks:
                empty_message = ft.Container(
                    content=ft.Text(
                        "У вас пока нет работ",
                        size=24,
                        color=ft.Colors.WHITE_70,
                        weight="bold",
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                )
                self.artworks_grid.controls = [empty_message]
                self._page.update()
                return

            cards = []
            for art in artworks:
                card = self.create_artwork_card(art)
                cards.append(card)

            self.artworks_grid.controls = cards
            self._page.update()

        except Exception as e:
            self.status_text.value = f"Ошибка загрузки: {str(e)}"
            self.status_text.color = ft.Colors.RED_400
            self._page.update()

    def create_artwork_card(self, artwork):
        artwork_id = artwork.get("id", 0)
        title = artwork.get("title", "Без названия")
        image_url = artwork.get("image_url", "")

        full_image_url = (
            f"http://localhost:8000{image_url}"
            if image_url and image_url.startswith("/")
            else None
        )

        # Картинка арта
        if full_image_url:
            art_image = ft.Image(
                src=full_image_url, width=200, height=150, fit="cover", border_radius=8
            )
        else:
            art_image = ft.Container(
                content=ft.Icon(ft.Icons.IMAGE, size=40, color=ft.Colors.GREY_500),
                width=200,
                height=150,
                bgcolor=ft.Colors.BLACK_45,
                border_radius=8,
                alignment=ft.Alignment(0, 0),
            )

        sell_button = ft.ElevatedButton(
            "sell",
            on_click=lambda e: self.sell_artwork_click(artwork_id),
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            width=100,
            height=35,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                shadow_color=ft.Colors.GREEN_300,
                elevation=2,
            ),
        )

        card_content = ft.Column(
            [
                art_image,
                ft.Container(height=10),
                ft.Text(
                    title,
                    color=ft.Colors.WHITE,
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                sell_button,
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=card_content,
            padding=10,
            bgcolor=ft.Colors.BLACK_45,
            border_radius=8,
        )

    def sell_artwork_click(self, artwork_id):
        def on_price_submit(e):
            try:
                price = float(price_field.value)
                if price <= 0:
                    raise ValueError("Цена должна быть положительной")

                dialog.open = False
                self._page.update()

                async def create_listing_task():
                    try:
                        await self.api.create_listing(artwork_id, price)
                        self.status_text.value = (
                            f"Работа выставлена на продажу за {price} ₽"
                        )
                        self.status_text.color = ft.Colors.GREEN_400

                        await self.load_artworks()

                    except Exception as ex:
                        self.status_text.value = f"Ошибка: {str(ex)}"
                        self.status_text.color = ft.Colors.RED_400
                        self._page.update()

                self._page.run_task(create_listing_task)

            except ValueError as ve:
                error_text.value = str(ve)
                error_text.visible = True
                self._page.update()

        def close_dialog():
            dialog.open = False
            self._page.update()

        price_field = ft.TextField(
            label="Цена (₽)", keyboard_type=ft.KeyboardType.NUMBER, width=200
        )

        error_text = ft.Text("", color=ft.Colors.RED_400, visible=False)

        close_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.WHITE,
            tooltip="Закрыть",
            on_click=lambda e: close_dialog(),
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [ft.Text("Установить цену"), ft.Container(expand=True), close_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Column([price_field, error_text], tight=True),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: close_dialog()),
                ft.TextButton("Выставить", on_click=on_price_submit),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        dialog.open = True

        self._page.overlay.append(dialog)
        self._page.update()

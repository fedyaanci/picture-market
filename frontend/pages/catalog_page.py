import flet as ft


class CatalogPage(ft.Container):
    def __init__(self, page: ft.Page, api, go_to_login_func, go_to_home_func):
        try:
            super().__init__()
            self._page = page
            self.api = api
            self.go_to_login = go_to_login_func
            self.go_to_home = go_to_home_func

            self.expand = True
            self.alignment = ft.Alignment(0, 0)
            self.bgcolor = ft.Colors.BLACK

            refresh_button = ft.IconButton(
                icon=ft.Icons.REFRESH,
                icon_color=ft.Colors.WHITE,
                tooltip="Обновить каталог",
                on_click=lambda _: self.refresh_catalog(),
            )

            profile_button = ft.IconButton(
                icon=ft.Icons.ACCOUNT_CIRCLE,
                icon_color=ft.Colors.WHITE,
                tooltip="Мой профиль",
                on_click=lambda _: self.go_to_home(),
            )

            title = ft.Text(
                "PICTUREMARKET", size=40, color=ft.Colors.WHITE, weight="bold"
            )

            self.status_text = ft.Text("", color=ft.Colors.GREEN_400, size=14)

            self.artworks_grid = ft.GridView(
                runs_count=3,
                max_extent=350,
                spacing=25,
                run_spacing=25,
                padding=ft.padding.only(top=80, left=20, right=20),
                expand=True,
            )

            top_bar = ft.Row(
                [refresh_button, ft.Container(expand=True), profile_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

            filter_buttons = ft.Row(
                [
                    ft.ElevatedButton(
                        "Все",
                        on_click=self.filter_all,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "В продаже",
                        on_click=self.filter_available,
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Продано",
                        on_click=self.filter_sold,
                        bgcolor=ft.Colors.RED_600,
                        color=ft.Colors.WHITE,
                    ),
                ],
                spacing=10,
            )

            main_content = ft.Column(
                [
                    top_bar,
                    ft.Container(height=10),
                    ft.Container(content=title, alignment=ft.Alignment(0, 0)),
                    ft.Container(height=15),
                    filter_buttons,
                    ft.Container(height=15),
                    self.status_text,
                    self.artworks_grid,
                    ft.Container(height=50),
                ],
                expand=True,
                spacing=0,
            )
            self.content = main_content

            async def load_initial():
                await self.load_listings(None)

            self._page.run_task(load_initial)

        except Exception as e:
            print(f"ошибка в CatalogPage: {e}")
            self.content = ft.Text(f"Ошибка: {e}", color=ft.Colors.RED_400)

    def refresh_catalog(self):
        async def load():
            await self.load_listings()

        self._page.run_task(load)

    async def load_listings(self, is_sold_filter=None):
        try:
            if is_sold_filter is None:
                url = "/listing/"
            elif is_sold_filter is True:
                url = "/listing/?is_sold=true"
            else:
                url = "/listing/?is_sold=false"

            listings = await self.api.get(url)

            if not listings:
                empty_message = ft.Container(
                    content=ft.Text(
                        "Каталог пуст", size=24, color=ft.Colors.WHITE_70, weight="bold"
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                )
                self.artworks_grid.controls = [empty_message]
                self._page.update()
                return

            cards = []
            for listing in listings:
                try:
                    artwork = await self.api.get_artwork(listing["artwork_id"])
                    seller = await self.api.get_user(listing["seller_id"])
                except Exception as e:
                    print(f"Ошибка загрузки данных: {e}")
                    artwork = {"title": "Ошибка загрузки", "image_url": ""}
                    seller = {"username": "Неизвестный", "avatar_url": None}

                card = self.create_listing_card(listing, artwork, seller)
                cards.append(card)

            self.artworks_grid.controls = cards
            self._page.update()

        except Exception as e:
            self.status_text.value = f"Ошибка загрузки: {str(e)}"
            self.status_text.color = ft.Colors.RED_400
            self._page.update()

    def create_listing_card(self, listing, artwork, seller):
        listing_id = listing.get("id", 0)
        price = listing.get("price", 0)
        is_sold = listing.get("is_sold", False)

        title = artwork.get("title", "Без названия")
        image_url = artwork.get("image_url", "")
        artist_name = seller.get("username", "Неизвестный")

        full_image_url = (
            f"http://localhost:8000{image_url}"
            if image_url and image_url.startswith("/")
            else None
        )

        if full_image_url:
            art_image = ft.Image(
                src=full_image_url, width=140, height=140, fit="cover", border_radius=12
            )
        else:
            art_image = ft.Container(
                content=ft.Icon(ft.Icons.IMAGE, size=40, color=ft.Colors.GREY_500),
                width=140,
                height=140,
                bgcolor=ft.Colors.BLACK_45,
                border_radius=12,
                alignment=ft.Alignment(0, 0),
            )

        info_below_image = ft.Column(
            [
                ft.Text(title, size=18, color=ft.Colors.WHITE, weight="bold"),
                ft.Text(f"Автор: {artist_name}", size=14, color=ft.Colors.WHITE_70),
                ft.Text(
                    f"{price} ₽", size=18, color=ft.Colors.GREEN_400, weight="bold"
                ),
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        if not is_sold:
            buy_button = ft.ElevatedButton(
                "Купить",
                on_click=lambda _: self.buy_artwork_click(listing_id),
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                width=120,
                height=35,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    shadow_color=ft.Colors.GREEN_300,
                    elevation=2,
                ),
            )
        else:
            buy_button = ft.Text(
                "Продано", color=ft.Colors.RED_400, size=16, weight="bold"
            )

        card_content = ft.Column(
            [
                art_image,
                ft.Container(height=10),
                info_below_image,
                ft.Container(height=10),
                buy_button,
                ft.Text("         ", size=18, color=ft.Colors.WHITE, weight="bold"),
                ft.Text("         ", size=18, color=ft.Colors.WHITE, weight="bold"),
                ft.Text("         ", size=18, color=ft.Colors.WHITE, weight="bold"),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=card_content,
            width=620,
            height=420,
            padding=5,
            border_radius=15,
            bgcolor=ft.Colors.BLACK_45,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.Colors.BLUE_900,
                offset=ft.Offset(0, 5),
            ),
        )

    def buy_artwork_click(self, listing_id):
        async def buy_task():
            try:
                result = await self.api.buy_artwork(listing_id)
                self.status_text.value = f"{result['message']}"
                self.status_text.color = ft.Colors.GREEN_400
                await self.load_listings()
            except Exception as ex:
                self.status_text.value = f"Ошибка: {str(ex)}"
                self.status_text.color = ft.Colors.RED_400
                self._page.update()

        self._page.run_task(buy_task)

    def filter_all(self, e):
        async def load():
            await self.load_listings(None)

        self._page.run_task(load)

    def filter_available(self, e):
        async def load():
            await self.load_listings(False)

        self._page.run_task(load)

    def filter_sold(self, e):
        async def load():
            await self.load_listings(True)

        self._page.run_task(load)

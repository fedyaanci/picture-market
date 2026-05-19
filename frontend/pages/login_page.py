import flet as ft


class LoginPage(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        api,
        go_to_register_func,
        go_to_catalog_func,
        error_msg=None,
    ):
        super().__init__()
        self._page = page
        self.api = api
        self.go_to_register = go_to_register_func
        self.go_to_catalog = go_to_catalog_func

        self.background_image = ft.Image(
            src="http://localhost:8000/uploads/system/background.jpg",
            width=page.width,
            height=page.height,
            fit="cover",
            opacity=0.3,
        )

        welcome_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=50),
                    ft.Text("WELCOME", size=48, color=ft.Colors.WHITE, weight="bold"),
                    ft.Text(
                        "Добро пожаловать в мир творчества",
                        size=20,
                        color=ft.Colors.WHITE_70,
                    ),
                    ft.Container(height=30),
                    ft.Divider(color=ft.Colors.WHITE_30, height=2),
                    ft.Container(height=30),
                    ft.Column(
                        [
                            ft.Text(
                                "• Создавайте уникальные работы",
                                size=16,
                                color=ft.Colors.WHITE_70,
                            ),
                            ft.Text(
                                "• Продавайте своё творчество",
                                size=16,
                                color=ft.Colors.WHITE_70,
                            ),
                            ft.Text(
                                "• Покупайте искусство других",
                                size=16,
                                color=ft.Colors.WHITE_70,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.STAR, size=80, color=ft.Colors.BLUE_100),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=500,
            padding=50,
            bgcolor=ft.Colors.BLACK,
            expand=True,
        )

        self.username_field = ft.TextField(
            label="Имя пользователя",
            width=300,
            border_color=ft.Colors.WHITE_30,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.TRANSPARENT,
            prefix_icon=ft.Icons.PERSON,
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
        )

        self.password_field = ft.TextField(
            label="Пароль",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.WHITE_30,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.TRANSPARENT,
            prefix_icon=ft.Icons.LOCK,
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
        )

        self.error_text = ft.Text("Ошибичка выходит", color=ft.Colors.RED_400, size=14)
        self.error_text.visible = bool(error_msg)
        if error_msg:
            self.error_text.value = error_msg

        self.login_button = ft.ElevatedButton(
            content=ft.Text("Войти", color=ft.Colors.WHITE, weight="bold"),
            width=250,
            height=50,
            bgcolor=ft.Colors.BLUE_600,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                shadow_color=ft.Colors.BLUE_300,
                elevation=5,
            ),
            on_click=self.on_login_click,
        )

        register_button = ft.TextButton(
            "Нет аккаунта? Зарегистрируйтесь",
            on_click=lambda _: self.go_to_register(),
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
        )

        login_form = ft.Container(
            content=ft.Column(
                [
                    ft.Text("ВХОД", size=32, color=ft.Colors.WHITE, weight="bold"),
                    ft.Container(height=30),
                    self.username_field,
                    self.password_field,
                    self.error_text,
                    ft.Container(height=20),
                    self.login_button,
                    ft.Container(height=15),
                    register_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=400,
            padding=40,
            bgcolor=ft.Colors.BLACK_45,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=15,
                color=ft.Colors.BLUE_900,
                offset=ft.Offset(0, 5),
            ),
        )

        right_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(expand=True),
                    ft.Container(content=login_form, alignment=ft.Alignment(0, 0)),
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=50,
        )

        main_content = ft.Row([welcome_panel, right_panel], expand=True)

        self.content = ft.Stack([self.background_image, main_content])
        self.expand = True

        page.on_resize = self.on_page_resize

    def on_page_resize(self, e):
        self.background_image.width = self._page.width
        self.background_image.height = self._page.height
        self._page.update()

    def on_login_click(self, e):
        if not self.username_field.value:
            self.show_error("Введите имя пользователя")
            return
        if not self.password_field.value:
            self.show_error("Введите пароль")
            return

        self.login_button.content = ft.ProgressRing(
            width=20, height=20, color=ft.Colors.WHITE
        )
        self.login_button.disabled = True
        self.error_text.visible = False
        self._page.update()

        self._page.run_task(self.do_login)

    async def load_purchased_artworks(self):
        try:
            orders = await self.api.get("/orders/")

            purchased_artworks = []
            for order in orders:
                listing = await self.api.get(f"/listing/{order['listing_id']}")
                artwork = await self.api.get_artwork(listing["artwork_id"])
                seller = await self.api.get_user(listing["seller_id"])

                purchased_artworks.append(
                    {
                        "artwork": artwork,
                        "seller": seller,
                        "price": listing["price"],
                        "purchase_date": order["purchased_at"],
                    }
                )

            return purchased_artworks

        except Exception as e:
            print(f"Ошибка загрузки купленных работ: {e}")
            return []

    async def do_login(self):
        try:
            response = await self.api.login(
                self.username_field.value, self.password_field.value
            )
            self.api.set_token(response["access_token"])
            self.go_to_catalog()

        except Exception as e:
            self.error_text.value = str(e)
            self.error_text.visible = True
            self.login_button.content = ft.Text(
                "Войти", color=ft.Colors.WHITE, weight="bold"
            )
            self.login_button.disabled = False
            self._page.update()

    def show_error(self, message):
        self.error_text.value = message
        self.error_text.visible = True
        self._page.update()

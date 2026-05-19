import flet as ft


class RegisterPage(ft.Container):
    def __init__(self, page: ft.Page, api, go_to_login_func, go_to_catalog_func):
        super().__init__()
        self._page = page
        self.api = api
        self.go_to_login = go_to_login_func
        self.go_to_catalog = go_to_catalog_func

        background_image = ft.Image(
            src="http://localhost:8000/uploads/system/background.jpg",
            width=page.width,
            height=page.height,
            fit="cover",
            opacity=0.3,
        )

        welcome_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=100),
                    ft.Text("JOIN US", size=48, color=ft.Colors.WHITE, weight="bold"),
                    ft.Text(
                        "Станьте частью нашего сообщества",
                        size=20,
                        color=ft.Colors.WHITE_70,
                    ),
                    ft.Container(height=50),
                    ft.Divider(color=ft.Colors.WHITE_30, height=2),
                    ft.Container(height=30),
                    ft.Text(
                        "• Создавайте и продавайте", size=16, color=ft.Colors.WHITE_70
                    ),
                    ft.Text(
                        "• Открывайте новые таланты", size=16, color=ft.Colors.WHITE_70
                    ),
                    ft.Text(
                        "• Вдохновляйтесь каждый день",
                        size=16,
                        color=ft.Colors.WHITE_70,
                    ),
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.STAR, size=80, color=ft.Colors.GREEN_300),
                ],
                alignment=ft.MainAxisAlignment.START,
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

        self.confirm_password_field = ft.TextField(
            label="Подтвердите пароль",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.WHITE_30,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.TRANSPARENT,
            prefix_icon=ft.Icons.LOCK_CLOCK,
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
        )

        self.is_artist_check = ft.Checkbox(
            label="Я художник",
            value=False,
            check_color=ft.Colors.BLACK_26,
            fill_color=ft.Colors.BLUE_400,
        )

        self.error_text = ft.Text("", color=ft.Colors.RED_400, size=14)
        self.error_text.visible = False

        self.register_button = ft.ElevatedButton(
            content=ft.Text("Зарегистрироваться", color=ft.Colors.WHITE, weight="bold"),
            width=280,
            height=50,
            bgcolor=ft.Colors.GREEN_600,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                shadow_color=ft.Colors.GREEN_300,
                elevation=5,
            ),
            on_click=self.on_register_click,
        )

        back_button = ft.TextButton(
            "Уже есть аккаунт? Войти",
            on_click=lambda _: self.go_to_login(),
            style=ft.ButtonStyle(color=ft.Colors.WHITE),
        )

        register_form = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "РЕГИСТРАЦИЯ", size=32, color=ft.Colors.WHITE, weight="bold"
                    ),
                    ft.Container(height=30),
                    self.username_field,
                    self.password_field,
                    self.confirm_password_field,
                    ft.Container(height=10),
                    ft.Container(
                        content=self.is_artist_check,
                        alignment=ft.Alignment(0, 0),
                        width=300,
                    ),
                    self.error_text,
                    ft.Container(height=20),
                    self.register_button,
                    ft.Container(height=15),
                    back_button,
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
                color=ft.Colors.GREEN_900,
                offset=ft.Offset(0, 5),
            ),
        )

        right_panel = ft.Container(
            content=ft.Column(
                [ft.Container(height=100), register_form, ft.Container(height=100)],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=50,
        )

        main_content = ft.Row([welcome_panel, right_panel], expand=True)

        self.content = ft.Stack([background_image, main_content])
        self.expand = True

    def on_register_click(self, e):
        if not self.username_field.value:
            self.show_error("Введите имя пользователя")
            return
        if not self.password_field.value:
            self.show_error("Введите пароль")
            return
        if not self.confirm_password_field.value:
            self.show_error("Подтвердите пароль")
            return
        if self.password_field.value != self.confirm_password_field.value:
            self.show_error("Пароли не совпадают")
            return
        if len(self.password_field.value) < 6:
            self.show_error("Пароль должен быть не менее 6 символов")
            return

        self.register_button.content = ft.ProgressRing(
            width=20, height=20, color=ft.Colors.WHITE
        )
        self.register_button.disabled = True
        self.error_text.visible = False
        self._page.update()

        self._page.run_task(self.do_register)

    async def do_register(self):
        try:
            await self.api.register(
                self.username_field.value,
                self.password_field.value,
                self.is_artist_check.value,
            )

            response = await self.api.login(
                self.username_field.value, self.password_field.value
            )
            self.api.set_token(response["access_token"])
            self.go_to_catalog()

        except Exception as e:
            self.error_text.value = str(e)
            self.error_text.visible = True
            self.register_button.content = ft.Text(
                "Зарегистрироваться", color=ft.Colors.WHITE, weight="bold"
            )
            self.register_button.disabled = False
            self._page.update()

    def show_error(self, message):
        self.error_text.value = message
        self.error_text.visible = True
        self._page.update()

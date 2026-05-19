import flet as ft
import tkinter as tk
from tkinter import filedialog


class HomePage(ft.Container):
    def __init__(self, page: ft.Page, api, go_to_login_func, go_to_catalog_func):
        super().__init__()
        self._page = page
        self.api = api
        self.go_to_login = go_to_login_func
        self.go_to_catalog = go_to_catalog_func

        self.expand = True
        self.alignment = ft.Alignment(0, 0)
        self.bgcolor = ft.Colors.BLACK

        home_button = ft.IconButton(
            icon=ft.Icons.HOME,
            icon_color=ft.Colors.WHITE,
            tooltip="В каталог",
            on_click=lambda _: self.go_to_catalog(),
        )

        self.avatar_container = ft.Container(
            content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color=ft.Colors.WHITE_70),
            alignment=ft.Alignment(0, 0),
        )

        self.user_info = ft.Column(
            [
                self.avatar_container,
                ft.Text("Загрузка...", size=20, color=ft.Colors.WHITE),
                ft.Text("", color=ft.Colors.WHITE_70),
                ft.Text("", color=ft.Colors.WHITE_70),
                ft.Text("", color=ft.Colors.GREEN_400),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        self.action_buttons = ft.Column(spacing=15)

        logout_button = ft.ElevatedButton(
            "Выйти из аккаунта",
            width=250,
            height=50,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                shadow_color=ft.Colors.RED_300,
                elevation=5,
            ),
            on_click=self.on_logout_click,
        )

        content = ft.Column(
            [
                ft.Container(height=30),
                self.user_info,
                ft.Container(height=20),
                self.action_buttons,
                ft.Container(height=20),
                logout_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        main_content = ft.Container(
            content=content,
            width=400,
            padding=30,
            bgcolor=ft.Colors.BLACK_45,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.Colors.BLUE_900,
                offset=ft.Offset(0, 5),
            ),
        )

        top_bar = ft.Row(
            [
                home_button,
                ft.Container(expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        centered_content = ft.Container(
            content=main_content, alignment=ft.Alignment(0, 0), expand=True
        )

        full_content = ft.Column([top_bar, centered_content], expand=True, spacing=0)

        self.content = full_content

        self._page.run_task(self.load_user_info)

    def on_logout_click(self, e):
        self.api.clear_token()
        self.go_to_login()

    async def load_user_info(self):
        try:
            user_data = await self.api.get_current_user()

            username = user_data.get("username", "Пользователь")
            user_id = user_data.get("id", "Неизвестно")
            is_artist = user_data.get("is_artist", False)
            balance = user_data.get("balance", 0.0)
            avatar_url = user_data.get("avatar_url", "")

            if avatar_url:
                import time

                timestamp = int(time.time())
                full_avatar_url = f"http://localhost:8000{avatar_url}?t={timestamp}"
                avatar_content = ft.Image(
                    src=full_avatar_url,
                    width=80,
                    height=80,
                    border_radius=40,
                    fit="cover",
                )
            else:
                avatar_content = ft.Icon(
                    ft.Icons.ACCOUNT_CIRCLE, size=80, color=ft.Colors.WHITE_70
                )

            self.avatar_container.content = avatar_content
            self.user_info.controls[1].value = f"Привет, {username}!"
            self.user_info.controls[1].color = ft.Colors.WHITE
            self.user_info.controls[2].value = f"ID: {user_id}"
            self.user_info.controls[
                3
            ].value = f"Художник: {'Да' if is_artist else 'Нет'}"
            self.user_info.controls[4].value = f"Баланс: {balance:.2f} ₽"

            self.action_buttons.controls.clear()

            upload_avatar_button = ft.ElevatedButton(
                "Загрузить аватар",
                width=250,
                height=50,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=15),
                    shadow_color=ft.Colors.BLUE_300,
                    elevation=5,
                ),
                on_click=self.upload_avatar_click,
            )
            self.action_buttons.controls.append(upload_avatar_button)

            topup_button = ft.ElevatedButton(
                "Пополнить баланс",
                width=250,
                height=50,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=15),
                    shadow_color=ft.Colors.GREEN_300,
                    elevation=5,
                ),
                on_click=self.topup_balance_click,
            )
            self.action_buttons.controls.append(topup_button)

            if is_artist:
                my_art_button = ft.ElevatedButton(
                    "Моё творчество",
                    width=250,
                    height=50,
                    bgcolor=ft.Colors.PURPLE_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        shadow_color=ft.Colors.PURPLE_300,
                        elevation=5,
                    ),
                    on_click=self.show_my_artworks,
                )
                self.action_buttons.controls.append(my_art_button)

            self._page.update()

        except Exception as e:
            self.avatar_container.content = ft.Icon(
                ft.Icons.ERROR, size=80, color=ft.Colors.RED_400
            )
            self.user_info.controls[1].value = f"Ошибка: {str(e)}"
            self.user_info.controls[1].color = ft.Colors.RED_400
            self._page.update()

    def upload_avatar_click(self, e):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Выберите аватар",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("All files", "*.*"),
            ],
        )

        root.destroy()

        if file_path:

            async def upload_task():
                await self.upload_avatar_task(file_path)

            self._page.run_task(upload_task)

    async def upload_avatar_task(self, file_path):
        try:
            self.avatar_container.content = ft.ProgressRing(
                width=80, height=80, color=ft.Colors.BLUE_400
            )
            self._page.update()

            await self.api.upload_avatar(file_path)
            await self.load_user_info()

        except Exception as ex:
            self.avatar_container.content = ft.Icon(
                ft.Icons.ERROR, size=80, color=ft.Colors.RED_400
            )
            self.user_info.controls[1].value = f"Ошибка: {str(ex)}"
            self.user_info.controls[1].color = ft.Colors.RED_400
            self._page.update()

    def topup_balance_click(self, e):
        def on_amount_submit(e):
            try:
                amount = float(amount_field.value)
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")

                self._page.run_task(lambda: self.topup_balance_task(amount))
                dialog.open = False
                self._page.update()

            except ValueError as ve:
                error_text.value = str(ve)
                error_text.visible = True
                self._page.update()

        amount_field = ft.TextField(
            label="Сумма пополнения", keyboard_type=ft.KeyboardType.NUMBER, width=200
        )

        error_text = ft.Text("", color=ft.Colors.RED_400, visible=False)

        dialog = ft.AlertDialog(
            title=ft.Text("Пополнение баланса"),
            content=ft.Column([amount_field, error_text]),
            actions=[
                ft.TextButton("Отмена", on_click=lambda _: self.close_dialog(dialog)),
                ft.TextButton("Пополнить", on_click=on_amount_submit),
            ],
        )

        self._page.dialog = dialog
        dialog.open = True
        self._page.update()

    def close_dialog(self, dialog):
        dialog.open = False
        self._page.update()

    async def topup_balance_task(self, amount):
        try:
            await self.api.topup_balance(amount)
            await self.load_user_info()
        except Exception as ex:
            self.user_info.controls[1].value = f"Ошибка: {str(ex)}"
            self.user_info.controls[1].color = ft.Colors.RED_400
            self._page.update()

    def show_my_artworks(self, e):
        from pages.my_artworks_page import MyArtworksPage

        my_artworks_page = MyArtworksPage(self._page, self.api, self.go_to_home)

        self._page.controls.clear()
        self._page.add(my_artworks_page)
        self._page.update()

    def go_to_home(self):
        from pages.home_page import HomePage

        home_page = HomePage(self._page, self.api, self.go_to_login, self.go_to_catalog)

        self._page.controls.clear()
        self._page.add(home_page)
        self._page.update()

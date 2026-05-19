import flet as ft

from api_client import APIClient
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.home_page import HomePage
from pages.catalog_page import CatalogPage


async def main(page: ft.Page):
    page.title = "Art Platform"
    page.window.width = 1000
    page.window.height = 800
    page.window.min_width = 1000
    page.window.min_height = 800
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0

    api = APIClient()

    def go_to_login(error_msg=None):
        page.controls.clear()
        login_page = LoginPage(page, api, go_to_register, go_to_catalog, error_msg)
        page.add(login_page)
        page.update()

    def go_to_register():
        page.controls.clear()
        register_page = RegisterPage(page, api, go_to_login, go_to_catalog)
        page.add(register_page)
        page.update()

    def go_to_home():
        page.controls.clear()
        home_page = HomePage(page, api, go_to_login, go_to_catalog)
        page.add(home_page)
        page.update()

    def go_to_catalog():
        page.controls.clear()
        catalog_page = CatalogPage(page, api, go_to_login, go_to_home)
        page.add(catalog_page)
        page.update()

    go_to_login()


if __name__ == "__main__":
    ft.run(main)

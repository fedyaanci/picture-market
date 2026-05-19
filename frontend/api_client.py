import aiohttp


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self._session = None
        self.token = None

    async def get_session(self):  # открывает tcp соединение
        if self._session is None:
            self._session = aiohttp.ClientSession()  # создает сессию для HTTP-запросов
        return self._session

    async def close(self):
        if self._session:
            await self._session.close()
            self._session = None

    def set_token(self, token: str):
        self.token = token

    def clear_token(self):
        self.token = None

    async def _make_request(self, method: str, endpoint: str, **kwargs):
        session = await self.get_session()
        url = f"{self.base_url}{endpoint}"

        #         kwargs = {
        #           "headers": {"Content-Type": "application/json"},
        #           "json": {...}
        #         }

        headers = kwargs.get("headers", {})
        if self.token:  # все защищенные запросы автом-ски пол-т заголовок авторизации
            headers["Authorization"] = f"Bearer {self.token}"
        kwargs["headers"] = headers

        async with session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"HTTP {response.status}: {error_text}")
            return await response.json()

    async def get(self, endpoint: str):
        return await self._make_request("GET", endpoint)

    async def post(self, endpoint: str, json_data=None):
        return await self._make_request("POST", endpoint, json=json_data)

    async def login(self, username: str, password: str):
        return await self.post(
            "/users/login", {"username": username, "password": password}
        )

    async def register(
        self,
        username: str,
        password: str,
        is_artist: bool = False,
        avatar_url: str = None,
    ):
        return await self.post(
            "/users/register",
            {
                "username": username,
                "password": password,
                "is_artist": is_artist,
                "avatar_url": avatar_url,
            },
        )

    async def get_current_user(self):
        return await self.get("/users/me")

    async def get_listings(self):
        return await self.get("/listing/")

    async def get_artwork(self, artwork_id: int):
        return await self.get(f"/artworks/{artwork_id}")

    async def get_user(self, user_id: int):
        return await self.get(f"/users/{user_id}")

    async def buy_artwork(self, listing_id: int):
        return await self.post(f"/purchase/buy/{listing_id}")

    async def upload_avatar(self, file_path: str):
        url = f"{self.base_url}/avatar/upload"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                form = aiohttp.FormData()
                form.add_field("file", f, filename=file_path.split("/")[-1])
                async with session.post(url, data=form, headers=headers) as resp:
                    if resp.status >= 400:
                        error_text = await resp.text()
                        raise Exception(f"HTTP {resp.status}: {error_text}")
                    return await resp.json()

    async def get_my_artworks(self):
        return await self.get("/artworks/my")

    async def get_categories(self):
        return await self.get("/categories/")

    async def create_listing(self, artwork_id: int, price: float):
        return await self.post("/listing/", {"artwork_id": artwork_id, "price": price})

    async def get_available_listings(self):
        return await self.get("/listing/?is_sold=false")

    async def get_sold_listings(self):
        return await self.get("/listing/?is_sold=true")

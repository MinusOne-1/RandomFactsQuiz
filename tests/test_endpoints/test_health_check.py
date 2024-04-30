from starlette import status


class TestHealthCheckHandler:
    @staticmethod
    def get_ping_app_url() -> str:
        return "/api/v1/health_check/ping_application"

    @staticmethod
    def get_ping_db_url() -> str:
        return "/api/v1/health_check/ping_database"

    async def test_ping_app(self, client):
        response = await client.get(url=self.get_ping_app_url())
        assert response.status_code == status.HTTP_200_OK

    async def test_ping_db(self, client):
        response = await client.get(url=self.get_ping_db_url())
        assert response.status_code == status.HTTP_200_OK

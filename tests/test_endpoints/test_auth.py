from starlette import status

from utils.get_url_service import GetUrl


class TestAuthenticationAndRegistration:

    async def test_registration_base_success(self, client):
        data = {
            "username": "basecase",
            "password": "psw",
            "email": "basecase@example.com"
        }
        reg_response = await client.post(
            url=GetUrl.get_registration_url(),
            json=data)
        assert reg_response.status_code == status.HTTP_201_CREATED

    async def test_registration_user_already_exist(self, client):
        data = {
            "username": "basecase",
            "password": "psw",
            "email": "basecase@example.com"
        }
        await client.post(url=GetUrl.get_registration_url(), json=data)
        reg_response_again = await client.post(
            url=GetUrl.get_registration_url(),
            json=data)
        assert reg_response_again.status_code == status.HTTP_400_BAD_REQUEST

    async def test_authentication_after_registration_success(self, client):
        data = {
            "username": "basecase",
            "password": "psw",
            "email": "basecase@example.com"
        }
        await client.post(url=GetUrl.get_registration_url(), json=data)

        auth_data = {"username": data["username"],
                     "password": data["password"],
                     "grant_type": ""}
        auth_response = await client.post(
            url=GetUrl.get_authentication_url(),
            data=auth_data,
            headers={"content-type": "application/x-www-form-urlencoded"})
        assert auth_response.status_code == status.HTTP_200_OK

    async def test_authentication_without_registration_fail(self, client):
        auth_data = {"username": "basecase",
                     "password": "psw",
                     "grant_type": ""}
        auth_response = await client.post(
            url=GetUrl.get_authentication_url(),
            data=auth_data,
            headers={"content-type": "application/x-www-form-urlencoded"})
        assert auth_response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_authentication_wrong_password_fail(self, client):
        data = {
            "username": "basecase",
            "password": "psw",
            "email": "basecase@example.com"
        }
        await client.post(url=GetUrl.get_registration_url(), json=data)
        auth_data = {"username": data["username"],
                     "password": "wreongpsw",
                     "grant_type": ""}
        auth_response = await client.post(
            url=GetUrl.get_authentication_url(),
            data=auth_data,
            headers={"content-type": "appli"
                                     + "cation/x-www-form-urlencoded"})
        assert auth_response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_me_fail_unauthorized(self, client):
        me_response = await client.get(url=GetUrl.get_me_url())
        assert me_response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_me_success(self, client, authorize):
        me_response = await client.get(url=GetUrl.get_me_url(),
                                       headers={
                                           "Authorization":
                                               f"Bearer {authorize}"})
        assert me_response.status_code == status.HTTP_200_OK

    async def test_takeout_fail_unauthorized(self, client):
        takeout_response = await client.delete(url=GetUrl.get_takeout_url())
        assert takeout_response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_takeout_success(self, client, authorize):
        takeout_response = await client.delete(url=GetUrl.get_takeout_url(),
                                               headers={
                                                   "Authorization":
                                                       f"Bearer {authorize}",
                                                   "content-"
                                                   + "type": "application/"
                                                             + "x-www-form"
                                                             + "-urlencoded"})
        assert takeout_response.status_code == status.HTTP_204_NO_CONTENT

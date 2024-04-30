class GetUrl:
    @staticmethod
    def get_authentication_url() -> str:
        return "/api/v1/user/authentication"

    @staticmethod
    def get_registration_url() -> str:
        return "/api/v1/user/registration"

    @staticmethod
    def get_me_url() -> str:
        return "/api/v1/user/me"

    @staticmethod
    def get_takeout_url() -> str:
        return "/api/v1/user/takeout"

import requests
from etudatasphere.exceptions import BadStatusCode
import json


class RequestController:
    def __init__(self, oauth_token: str = None) -> None:
        self.__BASE_HEADERS = {
            "Authorization": "Bearer {}".format(
                self.__request_iam_token(oauth_token=oauth_token)
            )
        }
        self.__is_valid()

    def make_get_request(self, url, params=None):
        res = requests.get(url, headers=self.__BASE_HEADERS, params=params)
        if res.status_code != 200:
            raise BadStatusCode(res.status_code, res.text)
        else:
            return res

    def make_post_request(self, url, data):
        res = requests.post(url, headers=self.__BASE_HEADERS, data=json.dumps(data))
        if res.status_code != 200:
            raise BadStatusCode(res.status_code, res.text)
        else:
            return res

    def make_patch_request(self, url, data):
        res = requests.patch(url, headers=self.HEADERS, data=json.dumps(data))
        if res.status_code != 200:
            raise BadStatusCode(res.status_code, res.text)
        else:
            return res

    def __request_iam_token(self, oauth_token):
        """
        Requests an IAM token from Yandex Cloud IAM API using the provided OAuth token.
        """

        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        headers = {"Authorization": f"OAuth {oauth_token}"}
        payload = {"yandexPassportOauthToken": oauth_token}

        res = requests.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            raise BadStatusCode(res.status_code, res.text)
        else:
            response_json = res.json()
            return response_json.get("iamToken")

    def __is_valid(self):
        url = "https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations"
        try:
            res = self.make_get_request(url)
            if res.ok:
                print("Oauth is valid.")
        except:
            raise BadStatusCode(res.status_code)

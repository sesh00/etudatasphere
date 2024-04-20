from etudatasphere.requests import RequestController


class OperationManager:
    __BASE_OPERATION_URL = "https://operation.api.cloud.yandex.net/operations/"

    def __init__(self, oauth_token: str) -> None:
        self.rc = RequestController(oauth_token=oauth_token)

    def is_completed(self, operation_id: str):
        res = self.check_operation_status(operation_id)
        if res["done"]:
            return True
        else:
            return False

    def check_operation_status(self, operation_id: str):
        """
        Checks the status of the specified operation.
        """
        url = self.__BASE_OPERATION_URL + operation_id
        res = self.rc.make_get_request(url)
        return res.json()

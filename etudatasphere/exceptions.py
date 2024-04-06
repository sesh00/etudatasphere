import traceback


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception occurred: {e}")
            print(f"Exception {traceback.format_exc()}")

    return wrapper


class BadStatusCode(Exception):
    def __init__(self, status_code, text='Error', message="Bad request"):
        self.status_code = status_code
        if status_code == 401:
            self.message = f"Check or update your IAM Token. Status code = {status_code}"
        if status_code == 404:
            self.message = f"{message}. Not found. Status code = {status_code}"
        else:
            self.message = f"{message}. Status code = {status_code}. Error message {text}"
        super().__init__(self.message)


class BadProjectRequest(Exception):
    def __init__(self, project_id, community_id):
        self.project_id = project_id
        self.community_id = community_id
        if self.project_id and self.community_id:
            self.message = 'Use only one of the available options'
        if (not self.project_id) and (not self.community_id):
            self.message = 'One of the parameters must be present'
        super().__init__(self.message)

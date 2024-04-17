import traceback


class BadStatusCode(Exception):
    def __init__(self, status_code, text="Error", message="Bad request"):
        self.status_code = status_code

        error_messages = {
            401: f"Check or update your IAM Token. Status code = {status_code}",
            404: f"{message}. Not found. Status code = {status_code}",
            400: f"{message}. Bad request. Status code = {status_code}",
            403: f"{message}. Forbidden. Status code = {status_code}",
            405: f"{message}. Method Not Allowed. Status code = {status_code}",
            409: f"{message}. Conflict. Status code = {status_code}",
            429: f"{message}. Too Many Requests. Status code = {status_code}",
            500: f"{message}. Internal Server Error. Status code = {status_code}",
            503: f"{message}. Service Unavailable. Status code = {status_code}",
        }

        self.message = error_messages.get(
            status_code, f"{message}. Status code = {status_code}. Error message {text}"
        )
        super().__init__(self.message)


class BadProjectRequest(Exception):
    def __init__(self, project_id, community_id):
        self.project_id = project_id
        self.community_id = community_id
        if self.project_id and self.community_id:
            self.message = "Use only one of the available options"
        if (not self.project_id) and (not self.community_id):
            self.message = "One of the parameters must be present"
        super().__init__(self.message)


class BadUpdateAllProjects(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BadAddContributors(Exception):
    def __init__(self):
        self.message = "No participants selected"
        super().__init__(self.message)

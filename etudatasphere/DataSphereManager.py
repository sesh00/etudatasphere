import requests
import traceback
import json


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Exception occurred: {e}")
            print(f"Exception {traceback.format_exc()}")

    return wrapper


class BadStatusCode(Exception):
    def __init__(self, status_code, message="Bad request"):
        self.status_code = status_code
        if status_code == 401:
            self.message = f"Check or update your IAM Token. Status code = {status_code}"
        if status_code == 404:
            self.message = f"{message}. Status code = {status_code}"
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


class ProjectSettings():
    settings = ('vmInactivityTimeout')
    limits = ('maxUnitsPerHour', 'maxUnitsPerExecution')

    def __init__(self, community_id: str,
                 name: str,
                 maxUnitsPerHour: int = None,
                 maxUnitsPerExecution: int = None,
                 description: str = None,
                 vmInactivityTimeout: str = "300s") -> dict:
        self.community_id = community_id
        self.name = name
        if description:
            self.description = description
        if maxUnitsPerHour:
            self.maxUnitsPerHour = maxUnitsPerHour
        if maxUnitsPerExecution:
            self.maxUnitsPerExecution = maxUnitsPerExecution
        if vmInactivityTimeout:
            self.vmInactivityTimeout = vmInactivityTimeout

    def to_dict(self):
        base_dict = {}
        settings_dict = {}
        limits_dict = {}
        for key, value in self.__dict__.items():
            if not (key.startswith('_') or key.endswith('__') or callable(
                    key)):
                if key in self.settings:
                    settings_dict[key] = value
                elif key in self.limits:
                    limits_dict[key] = value
                else:
                    base_dict[key] = value
        if settings_dict:
            base_dict['settings'] = settings_dict
        if limits_dict:
            base_dict['limits'] = limits_dict
        return base_dict


class DataSphereManager():

    def __init__(self, iam_token: str) -> None:
        self.HEADERS = {"Authorization": "Bearer {}".format(iam_token)}

    @handle_exceptions
    def __make_get_request(self, url, params=None):
        res = requests.get(url, headers=self.HEADERS, params=params)
        if res.status_code != 200:
            raise BadStatusCode(res.status_code)
        else:
            return res

    @handle_exceptions
    def __make_post_request(self, url, data):
        res = requests.post(url, headers=self.HEADERS, data=json.dumps(data))
        if res.status_code != 200:
            raise BadStatusCode(res.status_code)
        else:
            return res

    @handle_exceptions
    def get_organizations(self):

        url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds"
        res = self.__make_get_request(url)
        orgs = res.json()['clouds']

        for org in orgs:
            print('NAME', org['name'])
            print('ID', org['organizationId'])
            print('*' * 25)

    @handle_exceptions
    def get_billing_accounts(self):
        url = "https://billing.api.cloud.yandex.net/billing/v1/billingAccounts"
        res = self.__make_get_request(url)
        return res.json()

    @handle_exceptions
    def get_possible_ds_roles(self):
        url = "https://iam.api.cloud.yandex.net/iam/v1/roles"
        res = self.__make_get_request(url)
        roles = res.json()['roles']
        return [role for role in roles if 'datasphere' in role['id']]

    @handle_exceptions
    def get_organization_members(self, org_id: str):

        url = "https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations/{}/users".format(
            org_id)
        res = self.__make_get_request(url)
        users = res.json()['users']
        for user in users:
            print('NAME', user['subjectClaims']['name'])
            print('ID', user['subjectClaims']['sub'])
            print('*' * 25)

    @handle_exceptions
    def get_organization_communities(self, organization_id: str):
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/communities"
        params = {
            "organizationId": organization_id
        }
        res = self.__make_get_request(url, params)
        return res.json()

    @handle_exceptions
    def create_project(self,
                       community_id: str,
                       name: str,
                       description: str = None,
                       maxUnitsPerHour: int = None,
                       maxUnitsPerExecution: int = None,
                       vmInactivityTimeout: str = "300s"):
        data = ProjectSettings(
            community_id=community_id,
            name=name,
            description=description,
            maxUnitsPerHour=maxUnitsPerHour,
            maxUnitsPerExecution=maxUnitsPerExecution,
            vmInactivityTimeout=vmInactivityTimeout
        ).to_dict()
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects"
        res = self.__make_post_request(url, data)
        return res.json()

    @handle_exceptions
    def check_operation_status(self, id_operation: str):
        url = "https://operation.api.cloud.yandex.net/operations/{}".format(id_operation)
        res = self.__make_get_request(url)
        return res.json()

    @handle_exceptions
    def get_projects(self, project_id: str = None, community_id: str = None):
        if (community_id and project_id) or (
                (not project_id) and (not community_id)
        ):
            raise BadProjectRequest(community_id, project_id)

        if community_id:
            params = {
                "communityId": community_id
            }
        else:
            params = None
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}".format(
            project_id if project_id else "")
        res = self.__make_get_request(url, params)
        return res.json()

    @handle_exceptions
    def add_contributors(self, project_id, contributors: list[dict]):
        """
        project_id: str - ID of project
        contributors: list[dict] - The list of contributors to add
            format:
                [
                    {
                    "id": "aje3e6pnq1io5fe801d3",
                    "role":"datasphere.communities.admin"
                    },
                    {
                    "id": "ajebni1dr6lgce3jkl3d",
                    "role": "datasphere.communities.admin"
                    }
                ]
        """

        if not contributors:
            return 'No participants selected'
        else:
            data = {}
            data['accessBindings'] = []

            for user in contributors:
                data['accessBindings'].append({
                    "roleId": user['role'],
                    "subject": {
                        "id": user['id'],
                        "type": "userAccount"
                    }
                })
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}:setAccessBindings". \
            format(project_id)

        res = self.__make_post_request(url, data)
        return res.json()

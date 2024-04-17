import json
import requests
from etudatasphere.exceptions import (
    BadProjectRequest,
    BadStatusCode,
    BadUpdateAllProjects,
    BadAddContributors,
)
from etudatasphere.utils import (
    parse_projects,
    ProjectSettings,
    CommunitySettings,
    parse_communities,
)
from etudatasphere.requests import RequestController
from etudatasphere.OperationManager import OperationManager


class DataSphereManager:
    """
    Class for managing interactions with Yandex DataSphere API.
    """

    def __init__(self, oauth_token: str) -> None:
        """
        Initializes DataSphereManager object with the provided OAuth token.
        """
        self.rc = RequestController(oauth_token=oauth_token)

    def get_organizations(self):
        """
        Retrieves a list of organizations available for the account and prints their titles and IDs.
        """

        url = "https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations"
        res = self.rc.make_get_request(url)
        orgs = res.json()["organizations"]

        for org in orgs:
            print("TITLE", org["title"])
            print("ID", org["id"])
            print("*" * 25)

    def get_clouds(self, organization_id: str = ""):
        """
        Prints a list of clouds in organization, if organization_id is
        not provided prints a list of all clouds in all organizations available for the account
        organization_id: str - ID of organization
        """

        if organization_id:
            params = {"organizationId": organization_id}
        else:
            params = None

        url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds"
        res = self.rc.make_get_request(url, params)
        clouds = res.json()["clouds"]

        for cloud in clouds:
            print("NAME", cloud["name"])
            print("CLOUD_ID", cloud["id"])
            print("ORGANIZATION_ID", cloud["organizationId"])
            print("*" * 25)

    def get_unit_balance(self, project_id):
        """
        Retrieves the unit balance for the specified project.
        """
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}:unitBalance".format(
            project_id
        )
        res = self.rc.make_get_request(url)
        return res.json()

    def get_billing_accounts(self):
        """
        Retrieves a list of billing accounts.
        """
        url = "https://billing.api.cloud.yandex.net/billing/v1/billingAccounts"
        res = self.rc.make_get_request(url)
        return res.json()

    def get_possible_ds_roles(self):
        """
        Retrieves a list of possible roles in DataSphere.
        """
        url = "https://iam.api.cloud.yandex.net/iam/v1/roles"
        res = self.rc.make_get_request(url)
        roles = res.json()["roles"]
        return [role for role in roles if "datasphere" in role["id"]]

    def get_organization_members(self, org_id: str):
        """
        Retrieves members of the specified organization and prints their names and IDs.
        """
        url = "https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations/{}/users".format(
            org_id
        )
        res = self.rc.make_get_request(url)
        users = res.json()["users"]
        for user in users:
            print("NAME", user["subjectClaims"]["name"])
            print("ID", user["subjectClaims"]["sub"])
            print("*" * 25)

    def get_organization_communities(
        self, organization_id: str, parse_communities_flag=False
    ):
        """
        Retrieves communities of the specified organization.
        """
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/communities"
        params = {"organizationId": organization_id}
        res = self.rc.make_get_request(url, params)

        if parse_communities_flag:
            return parse_communities(res.json())
        else:
            return res.json()

    def create_project(
        self,
        community_id: str,
        name: str,
        description: str = None,
        vmInactivityTimeout: str = "1800s",
    ):
        """
        Creates a project with the specified parameters.
        """
        data = ProjectSettings(
            community_id=community_id,
            name=name,
            description=description,
            vmInactivityTimeout=vmInactivityTimeout,
        ).to_dict()
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects"
        res = self.rc.make_post_request(url, data)
        return res.json()

    def get_community(self, community_id: str = None):
        if community_id:
            url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/communities/{}".format(
                community_id
            )
            res = self.rc.make_get_request(url)
            return res.json()

    def get_projects(
        self,
        project_id: str = None,
        community_id: str = None,
        parse_projects_flag=False,
    ):
        """
        Retrieves information about projects based on project_id or community_id.
        """
        if (community_id and project_id) or ((not project_id) and (not community_id)):
            raise BadProjectRequest(community_id, project_id)

        if community_id:
            params = {"communityId": community_id}
        else:
            params = None

        url = (
            "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}".format(
                project_id if project_id else ""
            )
        )
        res = self.rc.make_get_request(url, params=params)

        if parse_projects_flag:
            res_json = res.json()
            unit_balances = {}

            if res_json.get("projects"):
                for project in res_json.get("projects"):
                    project_id = project.get("id")
                    unit_balance_res = self.get_unit_balance(project_id)
                    unit_balance = unit_balance_res.get("unitBalance")
                    unit_balances[project_id] = unit_balance
            else:
                project_id = res_json.get("id")
                unit_balance_res = self.get_unit_balance(project_id)
                unit_balance = unit_balance_res.get("unitBalance")
                unit_balances[project_id] = unit_balance

            return parse_projects(res_json, unit_balances)

        else:
            return res.json()

    def add_contributors(self, project_id, contributors: list[dict]):
        """
        Adds contributors to the specified project.

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
            raise BadAddContributors()
        else:
            data = {"accessBindings": []}

            for user in contributors:
                data["accessBindings"].append(
                    {
                        "roleId": user["role"],
                        "subject": {"id": user["id"], "type": "userAccount"},
                    }
                )
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}:setAccessBindings".format(
            project_id
        )

        res = self.rc.make_post_request(url, data)
        return res.json()

    def update_unit_balance(self, project_id, new_unit_balance):
        """
        Updates the unit balance for the specified project.
        """
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}:unitBalance".format(
            project_id
        )
        data = {"unitBalance": new_unit_balance}
        res = self.rc.make_post_request(url, data)
        return res.json()

    def update_all_community_projects(
        self,
        community_id: str,
        vmInactivityTimeout: str = "1000s",
        unit_balance: int = None,
    ):
        """
        Updates settings for all projects in the specified community.
        """
        data = ProjectSettings(vmInactivityTimeout=vmInactivityTimeout).to_dict()

        projects = self.get_projects(community_id=community_id)

        updateMask_list = []
        for k, v in data.items():
            for n in v.keys():
                updateMask_list.append(f"{k}.{n}")
        data["updateMask"] = ", ".join(updateMask_list)

        try:
            for idx, project in enumerate(projects["projects"]):
                print(f"{idx + 1}/{len(projects['projects'])}")
                url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}".format(
                    project.get("id")
                )
                res = self.rc.make_patch_request(url, data)
                print("Operation id:", res.json()["id"])

                if unit_balance is not None:
                    self.update_unit_balance(project.get("id"), unit_balance)

            return "ok"
        except Exception as e:
            raise BadUpdateAllProjects(str(e))

    def create_community(
        self,
        name: str,
        description: str,
        organizationId: str,
        billingAccountId: str = None,
    ):
        url = "https://datasphere.api.cloud.yandex.net/datasphere/v2/communities"
        data = CommunitySettings(
            organizationId=organizationId,
            name=name,
            description=description,
            billingAccountId=billingAccountId,
        ).to_dict()
        res = self.rc.make_post_request(url, data)
        return res.json()

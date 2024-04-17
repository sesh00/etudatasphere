def parse_projects(res: dict, unit_balances: dict):

    if res.get("projects"):
        parse_str = """"""
        for project in res.get("projects"):
            parse_str = (
                parse_str
                + f"""
Project name: {project.get('name')}\n
Project ID: {project.get('id')}\n
Project settings:\n
{parse_settings(project.get('settings'))}\n
Project unit balance: {unit_balances.get(project.get('id'), 'undefined')}\n
***********************************************
        """
            )
        return parse_str
    else:
        return f"""
Project name: {res.get('name')}\n
Project ID: {res.get('id')}\n
Project settings:\n
{parse_settings(res.get('settings'))}\n
Project unit balance: {unit_balances.get(res.get('id'), 'undefined')}\n
***********************************************
        """


def parse_communities(res: dict):
    parse_str = """"""

    for community in res.get("communities"):
        parse_str = (
            parse_str
            + f"""
Community Id: {community.get('id')}\n
Community Name: {community.get('name')}\n
Community CreatedById: {community.get('createdById')}\n
Community OrganizationId: {community.get('organizationId')}\n
***********************************************
        """
        )
    return parse_str


def parse_settings(project_settings: dict):
    settings_str = ""
    for el in project_settings:
        settings_str += f"\t{el}:{project_settings[el]}\n"
    return settings_str


class BaseSettings:
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    def to_dict(self):
        base_dict = {}
        for key, value in self.__dict__.items():
            if not (key.startswith("_") or key.endswith("__") or callable(key)):
                base_dict[key] = value
        return base_dict


class ProjectSettings(BaseSettings):
    settings = "vmInactivityTimeout"
    limits = ("maxUnitsPerHour", "maxUnitsPerExecution")

    def __init__(
        self,
        community_id: str = None,
        name: str = None,
        description: str = None,
        vmInactivityTimeout: str = "300s",
    ):
        if community_id:
            self.community_id = community_id
        if name:
            self.name = name
        if description:
            self.description = description
        if vmInactivityTimeout:
            self.vmInactivityTimeout = vmInactivityTimeout

    def to_dict(self):
        base_dict = {}
        settings_dict = {}
        limits_dict = {}
        for key, value in self.__dict__.items():
            if not (key.startswith("_") or key.endswith("__") or callable(key)):
                if key in self.settings:
                    settings_dict[key] = value
                elif key in self.limits:
                    limits_dict[key] = value
                else:
                    base_dict[key] = value
        if settings_dict:
            base_dict["settings"] = settings_dict
        if limits_dict:
            base_dict["limits"] = limits_dict
        return base_dict


class CommunitySettings(BaseSettings):
    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

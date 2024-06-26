# EtuDataSphere 

![PyPI](https://img.shields.io/pypi/v/etudatasphere?color=orange) ![Python 3.6, 3.7, 3.8](https://img.shields.io/pypi/pyversions/etudatasphere?color=blueviolet) ![GitHub Pull Requests](https://img.shields.io/github/issues-pr/sesh00/etudatasphere?color=blueviolet) ![License](https://img.shields.io/pypi/l/d?color=blueviolet) 

This is a Python library for interacting with Yandex DataSphere API. It provides functions to perform various operations such as getting organizations, billing accounts, projects, managing organization members, creating projects, checking operation status, and adding contributors to projects.

## Installation

Install the current version with [PyPI](https://pypi.org/project/etudatasphere):

```bash
pip install etudatasphere
```

Or from GitHub:
```bash
pip install https://github.com/sesh00/etudatasphere/archive/main.zip
```
## Usage
### Importing the DataSphereManager
```python
from etudatasphere import DataSphereManager
```
### Initializing DataSphereManager
[oauth token](https://yandex.cloud/ru/docs/iam/concepts/authorization/oauth-token)
```python
oauth_token = ""
dataSphereManager = DataSphereManager(oauth_token)
```
### Request for Organizations and Their Identifiers
Retrieves a list of organizations and their identifiers.
```python
dataSphereManager.get_organizations()
```
### Request for Role Identifiers in DataSphere
Retrieves a list of possible roles in DataSphere.
```python
dataSphereManager.get_possible_ds_roles()
```
### Request for Payment Accounts
Retrieves a list of billing accounts.
```python
dataSphereManager.get_billing_accounts()
```
### Request for Members of a Specific Organization
Retrieves members of a specific organization
```python
org_id = "" # From the section with the request for organizations
dataSphereManager.get_organization_members(org_id)
```
### Request for the List of Organization Communities
Retrieves communities of a specific organization.
```python
org_id = "" # From the section with the request for organizations
dataSphereManager.get_organization_communities(org_id)
```
### Project Creation, Participant Addition, Settings
Creates a project, adds contributors, and configures settings.
```python

community_id = "" # From the section with the request for communities
name = "" # Project name
description = "" # Project description
vmInactivityTimeout = "100s" # Release resources in the specified format, where 300 is the number of seconds of inactivity

dataSphereManager.create_project(
                        community_id = community_id,
                        name = name,
                        description = description,
                        vmInactivityTimeout = vmInactivityTimeout)
```
### Operation Status Check
Checks the status of a specific operation.
```python
id_operation = "" # Operation identifier from the section with project creation
dataSphereManager.check_operation_status(id_operation)

community_id = "" # From the section with project creation
dataSphereManager.get_projects(community_id=community_id)
```
### Project Request
Retrieves information about projects.
```python
project_id = "" # Identifier of the created project from the section with checking operation status
dataSphereManager.get_projects(project_id=project_id)

```
### Adding Participants to a Project
Adds contributors to a project.
```python
project_id = "" # Identifier of an existing project
contributors = [
        {
        "id": "", # Identifier of an organization member from the section with requesting members of a specific organization
        "role":"datasphere.communities.admin" # Possible role of a member from the section with requesting role identifiers
        },
        {
        "id": "",
        "role": "datasphere.communities.admin"
        }
    ]

dataSphereManager.add_contributors(project_id=project_id, contributors=contributors)

```

### Update all community projects
```python
community_id = ""
vm_inactivity_timeout = "100s"
unit_balance = 100
dataSphereManager.update_all_community_projects(community_id, vm_inactivity_timeout, unit_balance)
```

### Get & Update unit balance
```python
project_id = ""
unit_balance = 100
print(dataSphereManager.get_unit_balance(project_id))
dataSphereManager.update_unit_balance(project_id, unit_balance)
```

## Contributing

Contributions to EtuDataSphere are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository


## License

The module is available as open source under the terms of the [MIT License](https://opensource.org/licenses/mit)


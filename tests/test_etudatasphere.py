import pytest
from etudatasphere import DataSphereManager


@pytest.fixture(scope="module")
def data_sphere_manager():
    data_sphere_manager = DataSphereManager(oauth_token="")
    return data_sphere_manager


def test_get_organizations(data_sphere_manager):
    organizations = data_sphere_manager.get_organizations()


def test_get_communities(data_sphere_manager):
    organization_id = "bpfa94oocmi345p7tpv7"
    communities = data_sphere_manager.get_organization_communities(organization_id)
    print(communities)


def test_get_projects(data_sphere_manager):
    community_id = "bt1u8sr3l01444sc22gm"
    projects = data_sphere_manager.get_projects(community_id=community_id)
    print(projects)


def test_get_unit_balance(data_sphere_manager):
    project_id = "bt15an734pcprskkvjkt"
    print(data_sphere_manager.get_unit_balance(project_id))


def test_update_unit_balance(data_sphere_manager):
    project_id = "bt15an734pcprskkvjkt"
    data_sphere_manager.update_unit_balance(project_id, 100)


def test_create_project(data_sphere_manager):
    community_id = "bt1u8sr3l01444sc22gm"
    name = "Test Project"
    description = "This is a test project"
    vm_inactivity_timeout = "1800s"
    data_sphere_manager.create_project(community_id, name, description, vm_inactivity_timeout)


def test_update_all_community_projects(data_sphere_manager):
    community_id = "bt1u8sr3l01444sc22gm"
    vm_inactivity_timeout = "666s"
    unit_balance = 150
    data_sphere_manager.update_all_community_projects(community_id, vm_inactivity_timeout, unit_balance)

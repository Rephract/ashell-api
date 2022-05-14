from enum import Enum

USER_TYPE_CHOICES = [
    ('admin', 'Admin'),
    ('scenario_creator', 'Scenario Creator'),
    ('content_creator', 'Content Creator'),
]


class UserRoles(str, Enum):
    ADMIN = "admin"
    SCENARIO_CREATOR = "scenario_creator"
    CONTENT_CREATOR = "content_creator"

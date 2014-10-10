from unittest import TestCase
from youtracker.entities import Project

__author__ = 'Matthew'


class TestProject(TestCase):

    def setUp(self):
        connection = {}
        data = {
            "id": "TP",
            "name": "Test Project",
            "startingNumber": 1,
            "lead": "admin"
        }
        self.project = Project(connection)

    def test_update(self):
        self.fail()
from unittest import mock
from unittest import TestCase
from youtracker.entities import Project
from youtrack.connection import Connection
import requests


class TestProject(TestCase):

    def setUp(self):
        data = {
            "id": "TP",
            "name": "Test Project",
            "startingNumber": 1,
            "lead": "admin"
        }
        self.project = Project(Connection(), data)

    def test_update(self):
        self.assertTrue(self.project.update())
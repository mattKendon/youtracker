__author__ = 'Matthew'

import abc
import requests


class Abstract(metaclass=abc.ABCMeta):
    """The base class of all Youtrack classes in this package"""

    def __init__(self, connection):
        self.connection = connection

    @abc.abstractmethod
    def update(self):
        """Method to update (put) the current object back into Youtrack

        Returns:
            requests response obejct with code=200 if successful
        """

    @abc.abstractmethod
    def delete(self):
        """Method to delete (delete) the current object back into Youtrack

        Returns:
            requests response object with code=200 if successful
        """


class Project(Abstract):
    """The class that represents all Projects in Youtrack"""

    def __init__(self, connection, data):
        super().__init__(connection)
        self.name = data.get('name')
        self.id = data.get('id')
        self.lead = data.get('lead')
        self.starting_number = data.get('startingNumber')
        self.description = ""
        self.url = "/rest/admin/project/{id}".format(id=self.id)
        self._assignees = []
        self._assignee_groups = []
        self.issues = {}

    def update(self):
        params = {
            "projectName": self.name,
            "startingNumber": self.starting_number,
            "projectLeadLogin": self.lead,
            "description": self.description
        }
        return self.connection.put(self.url, params=params)

    def delete(self):
        return self.connection.delete(self.url)

    @property
    def assignees(self):
        """Method to get assignees for this project"""

        if len(self._assignees) < 1:
            url = "{base}/assignee/individual".format(base=self.url)
            try:
                results = self.connection.get(url)
            except requests.ConnectionError as e:
                results = None
            # todo: create Users from results
            self._assignees = []
        return self._assignees

    @property
    def assignee_groups(self):
        """Method to get assignee groups for this project"""

        if len(self._assignee_groups) < 1:
            url = "{base}/assignee/group".format(base=self.url)
            try:
                results = self.connection.get(url)
            except requests.Connection as e:
                results = None
            # todo: create Groups from results
            self._assignee_groups = []
        return self._assignee_groups

    def get_issue(self, issue_id):
        """Method for getting a specific issue for this project

        Tries to get the issue from the cache on this object, but
        otherwise will get the issue from the Youtrack server and add
        it to the cache.

        Returns:
            An Issue object or None
        """

        if issue_id not in self.issues:
            issue = self.connection.get_issue(issue_id)
            if not issue:
                return None
            self.issues[issue_id] = issue
        return self.issues[issue_id]


class Issue(Abstract):
    """The class that represents all Issues in Youtrack"""

    def __init__(self, connection, data, project):
        super().__init__(connection)
        self.project = project
        self.id = data['id']

    def update(self):
        pass

    def delete(self):
        url = "/issue/{id}".format(id=self.id)
        self.connection.delete(url)


class WorkItem(Abstract):
    """The class that represents all WorkItems in Youtrack"""

    def __init__(self, connection, data, issue):
        super().__init__(connection)
        self.issue = issue


class User(Abstract):
    """The class that represents all Users in Youtrack"""

    def __init__(self, connection, data):
        super().__init__(connection)


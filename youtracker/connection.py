__author__ = 'Matthew'

from youtracker.entities import Project
from youtracker.entities import Issue
import requests


class Connection(object):
    """Connection class to send requests to Youtrack server"""

    def __init__(self, url, login, password, proxy_info=None):
        self.url = url
        self.base_url = url + "/rest"
        self.login = login
        self.password = password
        self.proxy_info = proxy_info
        self.headers = {}
        self._cache = {}

        self._login(login, password)

    def _login(self, login, password):
        url = self.base_url + "/user/login?login=" + login + "&password=" + password
        response = requests.post(url, headers={'Content-Length': '0'}, proxies=self.proxy_info)
        if response.status_code != 200:
            raise Exception('/user/login', response)
        self.headers = {'Cookie': response.headers['set-cookie'],
                        'Cache-Control': 'no-cache',
                        'Accept': 'application/json'}

    def get(self, url, **kwargs):
        return requests.get(self.base_url + url, headers=self.headers, **kwargs)

    def post(self, url, **kwargs):
        return requests.post(self.base_url + url, headers=self.headers, **kwargs)

    def put(self, url, **kwargs):
        return requests.put(self.base_url + url, headers=self.headers, **kwargs)

    def delete(self, url, **kwargs):
        return requests.delete(self.base_url + url, headers=self.headers, **kwargs)

    def get_projects(self, **kwargs):
        projects = self._cache.get('projects', {})
        if not len(projects) or 'force' in kwargs:
            url = "/admin/project"
            response = self.get(url)
            data = response.json()
            for project_data in data:
                projects[project_data['id']] = project_data
            self._cache['projects'] = projects
        return self._cache.get('projects')

    def get_project(self, project_id):
        project_data = self.get_projects().get(project_id, None)
        if not project_data:
            return None
        if "entity" not in project_data:
            url = "/admin/project/{id}".format(id=project_id)
            response = self.get(url)
            if response.status_code != 200:
                # if we don't get a 200 code, lets find out why
                raise YoutrackException(response.status_code)
            project_data["entity"] = Project(self, response.json())
        return project_data["entity"]

    def get_issue(self, issue_id):
        project = self.get_project(issue_id.split("-")[0])
        if not project:
            return None
        issue = project.issues.get(issue_id, None)
        if not issue:
            url = "/issue/{id}".format(id=issue_id)
            response = self.get(url)
            if response.status_code != 200:
                # if we don't get a 200 code, lets find out why
                raise YoutrackException(response.status_code)
            project.issues[issue_id] = Issue(self, response.json(), project)
        return project.issues[issue_id]


class YoutrackException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code


if __name__ == '__main__':
    connection = Connection("http://tracker.outlandishideas.co.uk", "matt", "strangeCharm")
    print(connection.get_projects())
    project = connection.get_project("AOO")
    print(project)
    issue = project.get_issue("AOO-1")
    print(issue)


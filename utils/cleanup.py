"""
(c) Copyright Jalasoft. 2023

projects.py
    configuration of logger file
"""
import logging
import requests
from api.todo_base import TodoBase

from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class CleanUp:
    @classmethod
    def projects(cls):
        url_base_projects = "https://api.todoist.com/rest/v2/projects"
        session = requests.Session()
        projects_json = TodoBase().get_all_projects()["body"]
        for project in projects_json:
            project_id = project["id"]
            url_project_delete = f"{url_base_projects}/{project_id}"
            response = RestClient().send_request("delete", session=session, headers=HEADERS,
                                                 url=url_project_delete, data=None)
            # ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
            #                                      feature="projects")

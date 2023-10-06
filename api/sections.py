import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.cleanup import CleanUp
from utils.logger import get_logger
from utils.rest_client import RestClient
from api.validate_response import ValidateResponse

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.url_project = "https://api.todoist.com/rest/v2/projects"
        cls.session = requests.Session()
        # cls.project_id = TodoBase().get_all_projects()["body"][1]["id"]

    @classmethod
    def tearDownClass(cls):
        """
        Tear down of sections
        Delete all projects, and in the process it deletes all the sections
        :return:
        """
        CleanUp.projects()

    def createSection(self, name_section, name_project):
        """
        Creates a Project that will contain a Section
        Creates a Section inside the previously created Project
        this is used to set up the SUT with a project and a section
        :return:
        section_response: Dictionary that contains [body, headers, status]
        """
        body_project = {
            "name": name_project
        }
        body_section = {
            "name": name_section,
            "project_id": RestClient().send_request("post", session=self.session,
                                                    url=self.url_project, headers=HEADERS,
                                                    data=body_project)["body"]["id"]
        }
        section_response = RestClient().send_request("post", session=self.session,
                                                     url=self.url_section, headers=HEADERS,
                                                     data=body_section)
        return section_response

    def test_create_section(self):
        """
        Test to create section
        :return:
        """
        response = self.createSection(name_section="SECTION TEST", name_project="PROJECT TEST SECTION")
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="sections")

    def test_get_all_sections(self):
        """
        Test to get all sections from 2 different projects
        :return:
        """
        # Create project 1 and 2 sections inside
        self.createSection(name_section="SECTION 1: TEST GET ALL SECTIONS",
                           name_project="PROJECT 1: TEST GET ALL SECTIONS")
        self.createSection(name_section="SECTION 2: TEST GET ALL SECTIONS",
                           name_project="PROJECT 2: TEST GET ALL SECTIONS")
        response = TodoBase().get_all_sections()
        print("ALL SECTIONS:", response)
        # LOGGER.info("Number of sections returned: %s", len(response["body"]))
        # ValidateResponse().validate_response()

    def test_get_all_sections_by_project(self):
        if self.project_id:
            url_section = f"{self.url_section}?project_id={self.project_id}"

        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        LOGGER.info("Number of sections returned: %s", len(response["body"]))
        assert response["status"] == 200

    def test_get_section(self):
        response = TodoBase().get_all_sections()
        section_id = response["body"][0]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        assert response["status"] == 200

    def test_update_section(self):
        # Create a section
        self.test_create_section()
        response_sections = TodoBase().get_all_sections()
        section_id = response_sections["body"][0]["id"]
        LOGGER.info("Section to be updated: %s", section_id)
        url_section_update = f"{self.url_section}/{section_id}"
        data = {
            "name": "UPDATED SECTION"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_section_update, data=data)
        assert response["status"] == 200

    def test_delete_section(self):
        self.test_create_section()
        response_sections = TodoBase().get_all_sections()
        section_id = response_sections["body"][1]["id"]
        LOGGER.info("Section to be deleted: %s", section_id)
        url_section_delete = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_section_delete, data=None)
        assert response["status"] == 204

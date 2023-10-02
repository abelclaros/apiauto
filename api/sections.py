import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects()["body"][1]["id"]

    def test_create_session(self):
        """
        Test to create session
        :return:
        """
        data = {
            "project_id": self.project_id,
            "name": "Section 2"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        assert response["status"] == 200

    def test_get_all_sections(self):
        response = TodoBase().get_all_sections()
        LOGGER.info("Number of sections returned: %s", len(response["body"]))
        assert response["status"] == 200

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
        # data = {
        #     "project_id": self.project_id,
        #     "name": "Section 2"
        # }
        # response = RestClient().send_request("post", session=self.session, headers=HEADERS,
        #                                      url=self.url_section, data=data)
        # assert response["status"] == 200

        response_sections = TodoBase().get_all_sections()
        section_id = response_sections["body"][0]["id"]
        # LOGGER.info("Section to be updated:", section_id)
        url_section_update = f"{self.url_section}/{section_id}"
        data = {
            "name": "UPDATED SECTION"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_section_update, data=data)
        assert response["status"] == 200

    def test_delete_section(self):
        response_sections = TodoBase().get_all_sections()
        section_id = response_sections["body"][1]["id"]
        # LOGGER.info("Section to be deleted:", section_id)
        url_section_delete = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_section_delete, data=None)
        assert response["status"] == 204

import logging
import unittest

import requests

# from api.projects import Projects
from api.todo_base import TodoBase
from config.config import HEADERS
from utils.cleanup import CleanUp
from utils.logger import get_logger
from utils.rest_client import RestClient
from api.validate_response import ValidateResponse

# LOGGER = get_logger(__name__, logging.DEBUG)
#
#
# class Sections(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         cls.url_section = "https://api.todoist.com/rest/v2/sections"
#         cls.url_project = "https://api.todoist.com/rest/v2/projects"
#         cls.session = requests.Session()
#         # cls.project_id = TodoBase().get_all_projects()["body"][1]["id"]
#
#     @classmethod
#     def tearDownClass(cls):
#         """
#         Tear down of sections
#         Delete all projects, and in the process it deletes all the sections
#         :return:
#         """
"""Base Functional Test Class for superlists project"""
import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):

  @classmethod
  def setUpClass(cls):
    """Hack for overriding server URL to use a staging server

    Use self.server_url instead of self.live_server_url
    """
    for arg in sys.argv:
      if 'liveserver' in arg:
        cls.server_url = 'http://' + arg.split('=')[1]
        return
    super().setUpClass()
    cls.server_url = cls.live_server_url

  @classmethod
  def tearDownClass(cls):
    if cls.server_url == cls.live_server_url:
      super().tearDownClass()

  def setUp(self):
    self.setUpBrowser()

  def tearDown(self):
    self.tearDownBrowser()

  def setUpBrowser(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDownBrowser(self):
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  def get_item_input_box(self):
    return self.browser.find_element_by_id('id_text')

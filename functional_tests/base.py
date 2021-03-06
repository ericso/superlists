"""Base Functional Test Class for superlists project"""
import sys
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .server_tools import reset_database


class FunctionalTest(StaticLiveServerTestCase):

  @classmethod
  def setUpClass(cls):
    """Hack for overriding server URL to use a staging server

    Use self.server_url instead of self.live_server_url
    """
    for arg in sys.argv:
      if 'liveserver' in arg:
        cls.server_host = arg.split('=')[1]
        cls.server_url = 'http://' + cls.server_host
        cls.against_staging = True
        return
    super().setUpClass()
    cls.against_staging = False
    cls.server_url = cls.live_server_url

  @classmethod
  def tearDownClass(cls):
    if not cls.against_staging:
      super().tearDownClass()


  def setUp(self):
    if self.against_staging:
      reset_database(self.server_host)
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()


  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  def get_item_input_box(self):
    return self.browser.find_element_by_id('id_text')

  def switch_to_new_window(self, text_in_title):
    retries = 60
    while retries > 0:
      for handle in self.browser.window_handles:
        self.browser.switch_to_window(handle)
        if text_in_title in self.browser.title:
          return
      retries -= 1
      time.sleep(0.5)
    self.fail('could not find window')

  def wait_for_element_with_id(self, element_id):
    WebDriverWait(self.browser, timeout=30).until(
      lambda b: b.find_element_by_id(element_id),
      'Could not find element with id {}. Page text was {}'.format(
        element_id, self.browser.find_element_by_tag_name('body').text
      )
    )

  def wait_to_be_logged_in(self, email):
    self.wait_for_element_with_id('id_logout')
    navbar = self.browser.find_element_by_css_selector('.navbar')
    self.assertIn(email, navbar.text)

  def wait_to_be_logged_out(self, email):
    self.wait_for_element_with_id('id_login')
    navbar = self.browser.find_element_by_css_selector('.navbar')
    self.assertNotIn(email, navbar.text)


  def get_new_persona_test_user(self):
    resp = requests.get('http://personatestuser.org/email')
    data = resp.json()
    return (data['email'], data['pass'])

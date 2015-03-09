import time

from selenium.webdriver.support.ui import WebDriverWait

from .base import FunctionalTest


TEST_EMAIL = 'edith@mockmyid.com'


class LoginTest(FunctionalTest):

  def test_login_with_persona(self):
    # Edith goes to the awesome superlists site and notices a "Sign in" link
    #  for the first time
    self.browser.get(self.server_url)
    self.browser.find_element_by_id('id_login').click()

    # A Persona login box appears
    self.switch_to_new_window('Mozilla Persona')

    # Edith logs in with her email address
    ## Use mockmyid.com for test email
    ## Use http://personatestuser.org/ for test email
    test_email, test_password = self.get_new_persona_test_user()
    self.browser.find_element_by_id(
      'authentication_email'
    ).send_keys(test_email)
    self.browser.find_element_by_tag_name('button').click()

    self.browser.find_element_by_id(
      'authentication_password'
    ).send_keys(test_password)

    buttons = self.browser.find_elements_by_tag_name('button')
    for el in buttons:
      if 'sign in' in el.text:
        el.click()

    # The Persona window closes
    self.switch_to_new_window('To-Do')

    # She can see that she is logged in
    self.wait_to_be_logged_in(email=test_email)

    # Refreshing the page, she sees it's a real session login, not just a
    #  one-off for that page
    self.browser.refresh()
    self.wait_to_be_logged_in(email=test_email)

    # Terrified of this new feature, she reflexively clicks "logout"
    self.browser.find_element_by_id('id_logout').click()
    self.wait_to_be_logged_out(email=test_email)

    # The "logged out" status also persists after a refresh
    self.browser.refresh()
    self.wait_to_be_logged_out(email=test_email)

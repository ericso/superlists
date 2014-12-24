from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):

  def test_root_url_resolves_to_home_page_view(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  def test_home_page_returns_correct_html(self):
    request = HttpRequest()
    response = home_page(request)

    # content from the response is in raw bytes
    # we have to compare them with the b'' syntax
    self.assertTrue(response.content.startswith(b'<html>'))
    self.assertIn(b'<title>To-Do lists</title>', response.content)
    self.assertTrue(response.content.endswith(b'</html>'))

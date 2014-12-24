"""Unit tests for lists app in superlists project"""
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):

  def test_root_url_resolves_to_home_page_view(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  # def test_home_page_returns_correct_html(self):
  #   request = HttpRequest()
  #   response = home_page(request)

  #   print(repr(response.content))

  #   # content from the response is in raw bytes
  #   # we have to compare them with the b'' syntax
  #   self.assertTrue(response.content.startswith(b'<html>'))
  #   self.assertIn(b'<title>To-Do lists</title>', response.content)
  #   self.assertTrue(response.content.strip().endswith(b'</html>'))

  def test_home_page_returns_correct_html(self):
    request = HttpRequest()
    response = home_page(request)
    expected_html = render_to_string('home.html')

    # .decode() converts the response.content bytes to a
    #  Python Unicode string
    self.assertEqual(response.content.decode(), expected_html)

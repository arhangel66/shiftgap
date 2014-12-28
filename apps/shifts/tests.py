from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from .views import ShiftListing


class ShiftsTest(TestCase):

    def test_returns_correct_html(self):
        request_factory = RequestFactory()
        request = request_factory.get('/shifts')
        view = ShiftListing.as_view()
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shifts/shift_list.html')
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertTrue(response.content.endswith(b'</html>'))
from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from .views import ShiftListing


class ShiftsTest(TestCase):
    base_url = '/'

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

    # You can't unit test middleware with request factory hrmmmm...
    # def test_timezone_change_is_reflected(self):
    #     request_factory = RequestFactory()
    #     request = request_factory.post('/shifts/set-timezone', data={'timezone': 'Canada/Mountain'})
    #     from .views import set_timezone
    #     response = set_timezone(request)
    #     response.render()
    #     request = request_factory.get('/shifts')
    #     self.assertEqual(request.session['django_timezone'] == 'Canada/Mountain')
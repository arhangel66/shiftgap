from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string
from .views import ShiftListing
from .models import Shift


class ShiftsTest(TestCase):
    base_url = '/'

    def test_returns_correct_html(self):
        request_factory = RequestFactory()
        request = request_factory.get('/shifts')
        view = ShiftListing.as_view()
        response = view(request)
        response.render()
        expected_html = render_to_string('shifts/shift_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shifts/shift_list.html')
        self.assertTrue(response.content.startswith(b'<!DOCTYPE html>'))
        self.assertTrue(response.content.strip().endswith(b'</html>'))
        self.assertEqual(response.content.decode(), expected_html)

    # You can't unit test middleware with request factory hrmmmm...
    # def test_timezone_change_is_reflected(self):
    #     request_factory = RequestFactory()
    #     request = request_factory.post('/shifts/set-timezone', data={'timezone': 'Canada/Mountain'})
    #     from .views import set_timezone
    #     response = set_timezone(request)
    #     response.render()
    #     request = request_factory.get('/shifts')
    #     self.assertEqual(request.session['django_timezone'] == 'Canada/Mountain')

    # since we can't test the middleware might as well test the view
    def test_set_timezone_returns_correct_html(self):
        from .views import set_timezone
        found = resolve(reverse('shifts:set_timezone'))
        self.assertEqual(found.func, set_timezone)

    def test_can_save_shift(self):
        from django.utils import timezone
        shift = Shift.objects.create(
            start_time=timezone.now(),
            end_time=timezone.now(),
            employee='Blah'
        )
        self.assertIsInstance(shift, Shift)
        self.assertEqual(shift.employee, 'Blah')
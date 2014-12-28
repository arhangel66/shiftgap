from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import ShiftListing


class SmokeTest(TestCase):

    def test_url_resolves_to_shift_listing(self):
        found = resolve('/shifts')
        self.assertEqual(found.func, ShiftListing.as_view())
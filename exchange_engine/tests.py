from django.test import TestCase, Client


class IndexPageTestCase(TestCase):
    def test_index_response(self):
        c=Client()
        response=c.get(reversed('profile_editing'))
        self.assertEqual(response.status_code,200)

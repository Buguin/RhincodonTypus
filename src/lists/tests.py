from django.test import TestCase
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
        # self.assertEqual(response.content.decode(), expected_html)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())


class ItemModleTest(TestCase):
    def test_saving_and_retrieving_items(self):
        fist_item = Item()
        fist_item.text = 'The first (ever) list item'
        fist_item.save()

        second_item = Item()
        second_item.text = 'The second (ever) list item'
        second_item.save()

        save_items = Item.objects.all()
        self.assertEqual(save_items.count(), 2)

        fist_saved_item = save_items[0]
        second_saved_item = save_items[1]
        self.assertEqual(fist_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second (ever) list item')

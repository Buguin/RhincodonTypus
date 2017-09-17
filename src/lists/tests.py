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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

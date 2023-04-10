import unittest
from django.conf import settings
from django.test import TestCase, Client
from products.models import Product
from django.urls import reverse
from django.shortcuts import get_object_or_404


class AddToBag_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            price=10.99,
            image='test-image.jpg',
            category='test'
        )
        self.url = reverse('add_to_bag', args=[self.product.id])
        self.redirect_url = '/products/'

    def add_to_bag(self):
        response = self.client.post(self.url, {'quantity': 2, 'redirect_url': self.redirect_url})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        bag = self.client.session.get('bag')
        self.assertIsNotNone(bag)
        self.assertIn(str(self.product.id), bag)
        self.assertEqual(bag[str(self.product.id)], 2)


class AdjustBag_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_id = 'test_item'
        self.bag = {self.item_id: 2}
        self.url = reverse('adjust_bag', args=[self.item_id])

    def adjust_quantity(self):
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url, {'quantity': 4})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(session['bag'][self.item_id], 4)


class RemoveFromBag_test(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_id = 'test_item'
        self.bag = {self.item_id: 2}
        self.url = reverse('remove_from_bag', args=[self.item_id])

    def remove_item(self):
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.item_id, session['bag'])


if __name__ == '__main__':
    unittest.main()



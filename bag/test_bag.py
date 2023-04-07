import unittest
from django.conf import settings
from django.test import TestCase, Client
from products.models import Product
from django.urls import reverse
from django.shortcuts import get_object_or_404


class TestAddToBagView(TestCase):
    def setUp(self):
        settings.configure()
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

    def test_add_to_bag(self):
        response = self.client.post(self.url, {'quantity': 2, 'redirect_url': self.redirect_url})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        bag = self.client.session.get('bag')
        self.assertIsNotNone(bag)
        self.assertIn(str(self.product.id), bag)
        self.assertEqual(bag[str(self.product.id)], 2)

    def test_add_to_existing_item_in_bag(self):
        initial_quantity = 3
        self.client.session['bag'] = {str(self.product.id): initial_quantity}
        response = self.client.post(self.url, {'quantity': 2, 'redirect_url': self.redirect_url})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        bag = self.client.session.get('bag')
        self.assertIsNotNone(bag)
        self.assertIn(str(self.product.id), bag)
        self.assertEqual(bag[str(self.product.id)], initial_quantity + 2)


class AdjustBagViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_id = 'test_item'
        self.bag = {self.item_id: 2}
        self.url = reverse('adjust_bag', args=[self.item_id])

    def test_adjust_quantity(self):
        """Test that adjusting the quantity of an item in the bag works"""
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url, {'quantity': 4})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(session['bag'][self.item_id], 4)

    def test_remove_item(self):
        """Test that removing an item from the bag works"""
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url, {'quantity': 0})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.item_id, session['bag'])


class RemoveFromBagViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_id = 'test_item'
        self.bag = {self.item_id: 2}
        self.url = reverse('remove_from_bag', args=[self.item_id])

    def test_remove_item(self):
        """Test that removing an item from the bag works"""
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.item_id, session['bag'])

    def test_error_handling(self):
        """Test that error handling works"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 500)
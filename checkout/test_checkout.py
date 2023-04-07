from django.test import TestCase
from django.urls import reverse
from products.models import Product
from checkout.forms import OrderForm
from .models import Order, OrderLineItem
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from django.contrib.auth.models import User
from unittest.mock import patch
from decimal import Decimal
import stripe


class TestCacheCheckoutDataView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.session = self.client.session
        self.session['bag'] = {'1': 1}
        self.session.save()
        self.stripe_secret_key = 'test_secret_key'
        self.stripe_pid = 'test_pid'
        stripe.api_key = self.stripe_secret_key

    def test_cache_checkout_data_view_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': f'{self.stripe_pid}_secret',
            'save_info': True,
        })
        self.assertEqual(response.status_code, 200)
        payment_intent = stripe.PaymentIntent.retrieve(self.stripe_pid)
        self.assertEqual(payment_intent.metadata.get('bag'), '{"1": 1}')
        self.assertEqual(payment_intent.metadata.get('save_info'), 'true')
        self.assertEqual(payment_intent.metadata.get('username'), 'testuser')

    def test_cache_checkout_data_view_error(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': f'{self.stripe_pid}_secret',
            'save_info': True,
        })
        stripe.api_key = 'invalid_key'
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': f'{self.stripe_pid}_secret',
            'save_info': True,
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.content.decode())


class TestCheckoutView(TestCase):

    def setUp(self):
        self.url = reverse('checkout')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
        )

    def test_checkout_view_with_empty_bag(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('products'))
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "There's nothing in your bag at the moment")

    def test_checkout_view_with_bag(self):
        self.client.post(reverse('bag_add'), {'product_id': self.product.id, 'quantity': 1})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIsInstance(response.context.get('order_form'), OrderForm)
        self.assertEqual(response.context.get('stripe_public_key'), settings.STRIPE_PUBLIC_KEY)

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view_with_valid_form(self, mock_create_intent):
        mock_create_intent.return_value.client_secret = 'test_secret'
        bag = {str(self.product.id): 1}
        response = self.client.post(self.url, {'full_name': 'Test User',
                                                'email': 'test@test.com',
                                                'phone_number': '123456789',
                                                'country': 'US',
                                                'postcode': '12345',
                                                'town_or_city': 'Test City',
                                                'street_address1': 'Test Street 1',
                                                'street_address2': '',
                                                'county': '',
                                                'client_secret': 'test_secret',
                                                'save_info': 'on'}, {'bag': bag})
        self.assertRedirects(response, reverse('checkout_success', args=['test']))
        self.assertEqual(mock_create_intent.call_count, 1)
        self.assertEqual(response.context.get('client_secret'), 'test_secret')

    def test_checkout_view_with_invalid_form(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIsInstance(response.context.get('order_form'), OrderForm)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'There was an error with your form. Please double check your information.')


class TestCheckoutSuccessView(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.order = Order.objects.create(
            full_name='Test User',
            email='testuser@example.com',
            phone_number='123456789',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='Test Street 1',
            street_address2='Test Street 2',
            county='Test County',
            order_total=Decimal('10.00'),
            stripe_pid='test_pid',
            order_number='test123'
        )
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            lineitem_total=Decimal('10.00')
        )

    def test_checkout_success_view_with_order(self):
        self.client.force_login(self.user)
        url = reverse('checkout_success', args=[self.order.order_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, self.order.full_name)
        self.assertContains(response, self.order.email)
        self.assertContains(response, self.order.phone_number)
        self.assertContains(response, self.order.country)
        self.assertContains(response, self.order.postcode)
        self.assertContains(response, self.order.town_or_city)
        self.assertContains(response, self.order.street_address1)
        self.assertContains(response, self.order.street_address2)
        self.assertContains(response, self.order.county)
        self.assertContains(response, self.order.order_total)
        self.assertContains(response, self.order.order_number)
        self.assertContains(response, self.order_line_item.product.name)
        self.assertContains(response, self.order_line_item.quantity)
        self.assertContains(response, self.order_line_item.lineitem_total)

    def test_checkout_success_view_with_no_order(self):
        url = reverse('checkout_success', args=['test456'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

from django.test import TestCase
from django.urls import reverse
from products.models import Product
from checkout.forms import OrderForm
from .models import Order, OrderLineItem
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
import stripe


class Checkout_test(TestCase):
    def setUp(self):
        self.url = reverse('checkout')
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
        )

    def checkout_view_with_bag(self):
        self.client.post(reverse('bag_add'), {'product_id': self.product.id, 'quantity': 1})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIsInstance(response.context.get('order_form'), OrderForm)
        self.assertEqual(response.context.get('stripe_public_key'), settings.STRIPE_PUBLIC_KEY)


class CheckoutSuccess_test(TestCase):
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

    def checkout_success_with_order(self):
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


if __name__ == '__main__':
    unittest.main()




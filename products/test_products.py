from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Category


class TestAllProductsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.products_url = reverse('products')
        self.category_1 = Category.objects.create(name='Category 1')
        self.category_2 = Category.objects.create(name='Category 2')
        self.product_1 = Product.objects.create(
            name='Product 1',
            price=10,
            description='Description for product 1',
            category=self.category_1
        )
        self.product_2 = Product.objects.create(
            name='Product 2',
            price=20,
            description='Description for product 2',
            category=self.category_2
        )

    def test_all_products_view_with_no_query_params(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_2.name)
        self.assertContains(response, self.category_1.name)
        self.assertContains(response, self.category_2.name)

    def test_all_products_view_with_sort_query_param(self):
        response = self.client.get(self.products_url, {'sort': 'price'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_2.name)
        self.assertContains(response, self.category_1.name)
        self.assertContains(response, self.category_2.name)
        products_in_context = response.context['products']
        self.assertQuerysetEqual(
            products_in_context,
            [self.product_1.id, self.product_2.id],
            transform=lambda x: x.id
        )

    def test_all_products_view_with_category_query_param(self):
        response = self.client.get(self.products_url, {'category': f'{self.category_1.id}'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product_1.name)
        self.assertNotContains(response, self.product_2.name)
        self.assertContains(response, self.category_1.name)
        self.assertNotContains(response, self.category_2.name)
        products_in_context = response.context['products']
        self.assertQuerysetEqual(
            products_in_context,
            [self.product_1.id],
            transform=lambda x: x.id
        )

    def test_all_products_view_with_search_query_param(self):
        response = self.client.get(self.products_url, {'q': 'product 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product_1.name)
        self.assertNotContains(response, self.product_2.name)
        self.assertContains(response, self.category_1.name)
        self.assertNotContains(response, self.category_2.name)
        products_in_context = response.context['products']
        self.assertQuerysetEqual(
            products_in_context,
            [self.product_1.id],
            transform=lambda x: x.id
        )

class AdjustBagViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.item_id = 'test_item'
        self.quantity = 2
        self.bag = {self.item_id: self.quantity}
        self.url = reverse('adjust_bag', args=[self.item_id])

    def test_increase_quantity(self):
        """Test that increasing the quantity of an item in the bag works"""
        data = {'quantity': 3}
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('show_bag'))
        self.assertEqual(session['bag'][self.item_id], 3)

    def test_decrease_quantity(self):
        """Test that decreasing the quantity of an item in the bag works"""
        data = {'quantity': 1}
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('show_bag'))
        self.assertEqual(session['bag'][self.item_id], 1)

    def test_remove_item(self):
        """Test that removing an item from the bag works"""
        data = {'quantity': 0}
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('show_bag'))
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

    def test_remove_item_error(self):
        """Test that an error is returned if the item cannot be removed"""
        # remove the item from the bag before sending the request
        session = self.client.session
        session['bag'] = self.bag
        session.save()
        session['bag'].pop(self.item_id)
        session.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 500)



if __name__ == '__main__':
    unittest.main()



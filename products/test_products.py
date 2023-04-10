from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Category


class AllProducts_test(TestCase):
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

    def all_products(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_2.name)
        self.assertContains(response, self.category_1.name)
        self.assertContains(response, self.category_2.name)


if __name__ == '__main__':
    unittest.main()



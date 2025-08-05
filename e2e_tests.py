from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Order, Wishlist
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

class E2ECommerceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.product1 = Product.objects.create(
            name='Classic White Shirt',
            price=Decimal('29.99'),
            description='Premium cotton white shirt, perfect for formal and casual occasions.'
        )
        self.product2 = Product.objects.create(
            name='Running Sneakers',
            price=Decimal('79.99'),
            description='Lightweight running sneakers with breathable mesh and cushioned sole.'
        )

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(str(self.product1), 'Classic White Shirt')

    def test_user_signup_and_login(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        login = self.client.login(username='newuser', password='testpass123')
        self.assertTrue(login)

    def test_add_to_cart_and_checkout(self):
        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        session['cart'] = {str(self.product1.id): 2}
        session.save()
        response = self.client.get(reverse('cart_view'))
        self.assertContains(response, 'Classic White Shirt')
        # Simulate checkout
        response = self.client.post(reverse('checkout'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'address': '123 Test Street',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    def test_wishlist(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_to_wishlist', args=[self.product2.id]))
        self.assertEqual(response.status_code, 302)
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertIn(self.product2, wishlist.products.all())

    def test_order_history(self):
        self.client.login(username='testuser', password='testpass123')
        Order.objects.create(user=self.user, name='John Doe', email='john@example.com', address='123 Test Street', cart_data={str(self.product1.id): 1}, total_price=Decimal('29.99'))
        response = self.client.get(reverse('order_history'))
        self.assertContains(response, 'John Doe')

    def tearDown(self):
        # Django test runner will delete the test database automatically
        pass

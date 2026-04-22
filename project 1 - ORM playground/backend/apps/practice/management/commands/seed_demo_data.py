from django.core.management.base import BaseCommand

from apps.practice.models import Category, Customer, Order, Product


class Command(BaseCommand):
    help = "Seed initial demo data for ORM practice."

    def handle(self, *args, **options):
        if Customer.objects.exists():
            self.stdout.write(self.style.WARNING("Seed skipped: data already exists."))
            return

        electronics = Category.objects.create(name="Electronics")
        books = Category.objects.create(name="Books")
        grocery = Category.objects.create(name="Grocery")

        laptop = Product.objects.create(name="Laptop", category=electronics, price=1200.00, stock=25)
        phone = Product.objects.create(name="Phone", category=electronics, price=800.00, stock=50)
        novel = Product.objects.create(name="Novel", category=books, price=20.00, stock=200)
        rice = Product.objects.create(name="Rice Bag", category=grocery, price=35.00, stock=120)

        alice = Customer.objects.create(name="Alice", email="alice@example.com", city="Bangalore")
        bob = Customer.objects.create(name="Bob", email="bob@example.com", city="Mysore")
        carol = Customer.objects.create(name="Carol", email="carol@example.com", city="Mumbai")

        Order.objects.create(customer=alice, product=laptop, quantity=1)
        Order.objects.create(customer=alice, product=novel, quantity=3)
        Order.objects.create(customer=bob, product=phone, quantity=1)
        Order.objects.create(customer=carol, product=rice, quantity=4)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

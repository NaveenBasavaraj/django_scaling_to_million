from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category, Customer, Order, Product
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    OrderSerializer,
    ProductSerializer,
)


class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CustomerViewSet(ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [ReadOnlyPermission]


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyPermission]


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [ReadOnlyPermission]


class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.select_related("customer", "product").all()
    serializer_class = OrderSerializer
    permission_classes = [ReadOnlyPermission]


router = DefaultRouter()
router.register("customers", CustomerViewSet, basename="customers")
router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("orders", OrderViewSet, basename="orders")

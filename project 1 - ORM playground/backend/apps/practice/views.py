import ast

from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
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


class ORMQueryView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    allowed_models = {
        "Customer": Customer,
        "Category": Category,
        "Product": Product,
        "Order": Order,
    }

    serializers = {
        Customer: CustomerSerializer,
        Category: CategorySerializer,
        Product: ProductSerializer,
        Order: OrderSerializer,
    }

    queryset_methods = {"all", "filter", "exclude", "order_by", "values", "values_list"}
    terminal_methods = {"count", "exists", "first", "last"}

    def post(self, request):
        expression = (request.data.get("expression") or "").strip()
        if not expression:
            return Response({"detail": "Provide an ORM expression."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result, output_mode = self._execute_expression(expression)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "expression": expression,
            "result": self._serialize_result(result, output_mode),
        }
        return Response(payload)

    def _execute_expression(self, expression):
        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Invalid syntax: {exc.msg}") from exc

        chain, model_name = self._extract_chain(parsed.body)
        model = self.allowed_models.get(model_name)
        if model is None:
            raise ValueError(f"Model '{model_name}' is not allowed.")

        current = model.objects
        output_mode = "serializer"

        for index, (method_name, args, kwargs) in enumerate(chain):
            is_last_call = index == len(chain) - 1

            if method_name in self.queryset_methods:
                current = self._run_queryset_method(current, method_name, args, kwargs)
                if method_name in {"values", "values_list"}:
                    output_mode = "raw"
                continue

            if method_name in self.terminal_methods:
                if not is_last_call:
                    raise ValueError(f"Method '{method_name}' must be the last call in the chain.")
                return self._run_terminal_method(current, method_name, args, kwargs), output_mode

            raise ValueError(f"Method '{method_name}' is not allowed.")

        return current, output_mode

    def _extract_chain(self, node):
        calls = []
        current = node

        while isinstance(current, ast.Call):
            if not isinstance(current.func, ast.Attribute):
                raise ValueError("Only method-call expressions are allowed.")

            method_name = current.func.attr
            args = [self._literal_value(arg) for arg in current.args]
            kwargs = {}
            for kw in current.keywords:
                if kw.arg is None:
                    raise ValueError("Starred kwargs are not allowed.")
                kwargs[kw.arg] = self._literal_value(kw.value)

            calls.insert(0, (method_name, args, kwargs))
            current = current.func.value

        if not isinstance(current, ast.Attribute) or current.attr != "objects":
            raise ValueError("Expression must start with Model.objects")
        if not isinstance(current.value, ast.Name):
            raise ValueError("Invalid model reference.")

        return calls, current.value.id

    def _literal_value(self, node):
        try:
            return ast.literal_eval(node)
        except (ValueError, SyntaxError) as exc:
            raise ValueError("Only literal arguments are allowed.") from exc

    def _run_queryset_method(self, queryset, method_name, args, kwargs):
        if method_name == "all":
            if args or kwargs:
                raise ValueError("all() does not accept arguments.")
            return queryset.all()

        if method_name in {"filter", "exclude"}:
            if args:
                raise ValueError(f"{method_name}() positional args are not allowed.")
            return getattr(queryset, method_name)(**kwargs)

        if method_name == "order_by":
            return queryset.order_by(*args)

        if method_name == "values":
            return queryset.values(*args)

        if method_name == "values_list":
            allowed_kwargs = {"flat", "named"}
            invalid = set(kwargs.keys()) - allowed_kwargs
            if invalid:
                raise ValueError("values_list() supports only flat/named kwargs.")
            return queryset.values_list(*args, **kwargs)

        raise ValueError(f"Method '{method_name}' is not allowed.")

    def _run_terminal_method(self, queryset, method_name, args, kwargs):
        if args or kwargs:
            raise ValueError(f"{method_name}() does not accept arguments.")
        return getattr(queryset, method_name)()

    def _serialize_result(self, result, output_mode):
        if isinstance(result, (int, bool)):
            return result

        if result is None:
            return None

        if output_mode == "raw":
            return list(result[:100])

        if hasattr(result, "model"):
            serializer_class = self.serializers.get(result.model)
            if serializer_class is None:
                raise ValueError("Serializer not configured for this model.")
            queryset = result[:100]
            return serializer_class(queryset, many=True).data

        model_class = result.__class__
        serializer_class = self.serializers.get(model_class)
        if serializer_class:
            return serializer_class(result).data

        raise ValueError("Unsupported result type.")


router = DefaultRouter()
router.register("customers", CustomerViewSet, basename="customers")
router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("orders", OrderViewSet, basename="orders")

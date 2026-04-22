from django.http import JsonResponse
from django.urls import include, path

from .views import router


def api_home(_request):
    return JsonResponse(
        {
            "message": "ORM Playground API",
            "resources": ["customers", "categories", "products", "orders"],
            "note": "Read-only endpoints. Only GET methods are allowed.",
        }
    )


urlpatterns = [
    path("", api_home, name="api-home"),
    path("", include(router.urls)),
]

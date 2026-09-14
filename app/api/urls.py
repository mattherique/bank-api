from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from app.api.views import BalanceView, EventView, ResetView

urlpatterns = [
    path("reset", ResetView.as_view(), name="reset"),
    path("balance", BalanceView.as_view(), name="balance"),
    path("event", EventView.as_view(), name="event"),
    re_path(r"^schema/?$", SpectacularAPIView.as_view(), name="schema"),
    re_path(
        r"^docs/?$",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

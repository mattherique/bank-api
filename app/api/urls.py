from django.urls import path

from app.api.views import BalanceView, EventView, ResetView

urlpatterns = [
    path("reset", ResetView.as_view(), name="reset"),
    path("balance", BalanceView.as_view(), name="balance"),
    path("event", EventView.as_view(), name="event"),
]

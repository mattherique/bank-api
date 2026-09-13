from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from app.domain.exceptions import AccountNotFound, InsufficientFunds


def domain_exception_handler(exc, context):
    if isinstance(exc, AccountNotFound):
        return Response(0, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, InsufficientFunds):
        return Response(
            {"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return drf_exception_handler(exc, context)

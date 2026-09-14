from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.schema import (
    ACCOUNT_ID_PARAMETER,
    ACCOUNT_NOT_FOUND,
    BALANCE_RESPONSE,
    EVENT_REQUEST_EXAMPLES,
    EVENT_RESPONSE,
    EVENT_RESPONSE_EXAMPLES,
    RESET_RESPONSE,
)
from app.api.serializers import EventSerializer
from app.application.dtos import DepositDTO, TransferDTO, WithdrawDTO
from app.domain.entities.account import Account
from app.wiring import get_balance_service, get_reset_service, get_transaction_service


def _account_payload(account: Account) -> dict:
    return {"id": account.id, "balance": account.balance}


class EventView(APIView):
    @extend_schema(
        summary="Process a banking event (deposit, withdraw, transfer)",
        description=(
            "deposit creates the destination account if it doesn't exist. withdraw and "
            "transfer require the origin account to exist, otherwise they respond with 404 and "
            "body 0. The response format follows the event type."
        ),
        request=EventSerializer,
        responses={201: EVENT_RESPONSE, 404: ACCOUNT_NOT_FOUND},
        examples=EVENT_REQUEST_EXAMPLES + EVENT_RESPONSE_EXAMPLES,
    )
    def post(self, request: Request) -> Response:
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = serializer.to_dto()
        service = get_transaction_service()

        match dto:
            case DepositDTO():
                account = service.deposit(dto)
                body = {"destination": _account_payload(account)}
            case WithdrawDTO():
                account = service.withdraw(dto)
                body = {"origin": _account_payload(account)}
            case TransferDTO():
                origin, destination = service.transfer(dto)
                body = {
                    "origin": _account_payload(origin),
                    "destination": _account_payload(destination),
                }

        return Response(body, status=status.HTTP_201_CREATED)


class BalanceView(APIView):
    @extend_schema(
        summary="Check the balance of an account",
        parameters=[ACCOUNT_ID_PARAMETER],
        responses={200: BALANCE_RESPONSE, 404: ACCOUNT_NOT_FOUND},
    )
    def get(self, request: Request) -> Response:
        account_id = request.query_params.get("account_id")
        if not account_id:
            return Response(
                {"account_id": "required"}, status=status.HTTP_400_BAD_REQUEST
            )

        balance = get_balance_service().get_balance(account_id)
        return Response(balance, status=status.HTTP_200_OK)


class ResetView(APIView):
    @extend_schema(
        summary="Reset the application state",
        request=None,
        responses={200: RESET_RESPONSE},
    )
    def post(self, request: Request) -> HttpResponse:
        get_reset_service().reset()
        return HttpResponse("OK", content_type="text/plain")

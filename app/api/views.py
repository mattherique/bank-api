from django.db import transaction
from django.http import HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import EventSerializer
from app.application.dtos import DepositDTO, TransferDTO, WithdrawDTO
from app.application.services import TransactionService
from app.domain.entities.account import Account
from app.wiring import get_balance_service, get_reset_service, get_transaction_service


def _account_payload(account: Account) -> dict[str, object]:
    return {"id": account.id, "balance": account.balance}


class EventView(APIView):
    def _deposit(self, service: TransactionService, dto: DepositDTO) -> dict[str, object]:
        account = service.deposit(dto)
        return {"destination": _account_payload(account)}

    def _withdraw(self, service: TransactionService, dto: WithdrawDTO) -> dict[str, object]:
        account = service.withdraw(dto)
        return {"origin": _account_payload(account)}

    def _transfer(self, service: TransactionService, dto: TransferDTO) -> dict[str, object]:
        origin, destination = service.transfer(dto)
        return {
            "origin": _account_payload(origin),
            "destination": _account_payload(destination),
        }
    
    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = serializer.to_dto()
        service = get_transaction_service()

        dto_task = {
            DepositDTO: self._deposit,
            WithdrawDTO: self._withdraw,
            TransferDTO: self._transfer,
        }

        body = dto_task[type(dto)](service, dto)

        return Response(body, status=status.HTTP_201_CREATED)


class BalanceView(APIView):
    def get(self, request: Request) -> Response:
        account_id = request.query_params.get("account_id")
        if not account_id:
            return Response(
                {"account_id": "required"}, status=status.HTTP_400_BAD_REQUEST
            )

        balance = get_balance_service().get_balance(account_id)
        return Response(balance, status=status.HTTP_200_OK)


class ResetView(APIView):
    @transaction.atomic
    def post(self, request: Request) -> HttpResponse:
        get_reset_service().reset()
        return HttpResponse("OK", content_type="text/plain")

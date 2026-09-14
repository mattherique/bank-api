from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer,
)
from rest_framework import serializers


class AccountPayloadSerializer(serializers.Serializer):
    id = serializers.CharField()
    balance = serializers.IntegerField()


class DepositResponseSerializer(serializers.Serializer):
    destination = AccountPayloadSerializer()


class WithdrawResponseSerializer(serializers.Serializer):
    origin = AccountPayloadSerializer()


class TransferResponseSerializer(serializers.Serializer):
    origin = AccountPayloadSerializer()
    destination = AccountPayloadSerializer()


EVENT_RESPONSE = PolymorphicProxySerializer(
    component_name="EventResponse",
    serializers=[
        DepositResponseSerializer,
        WithdrawResponseSerializer,
        TransferResponseSerializer,
    ],
    resource_type_field_name=None,
)

ACCOUNT_NOT_FOUND = OpenApiResponse(
    response=OpenApiTypes.INT,
    description="Account not found.",
    examples=[OpenApiExample("Not found", value=0)],
)

EVENT_REQUEST_EXAMPLES = [
    OpenApiExample(
        "Deposit",
        value={"type": "deposit", "destination": "100", "amount": 10},
        request_only=True,
    ),
    OpenApiExample(
        "Withdraw",
        value={"type": "withdraw", "origin": "100", "amount": 5},
        request_only=True,
    ),
    OpenApiExample(
        "Transfer",
        value={"type": "transfer", "origin": "100", "destination": "300", "amount": 15},
        request_only=True,
    ),
]

EVENT_RESPONSE_EXAMPLES = [
    OpenApiExample(
        "Deposit",
        value={"destination": {"id": "100", "balance": 10}},
        response_only=True,
        status_codes=["201"],
    ),
    OpenApiExample(
        "Withdraw",
        value={"origin": {"id": "100", "balance": 15}},
        response_only=True,
        status_codes=["201"],
    ),
    OpenApiExample(
        "Transfer",
        value={
            "origin": {"id": "100", "balance": 0},
            "destination": {"id": "300", "balance": 15},
        },
        response_only=True,
        status_codes=["201"],
    ),
]

ACCOUNT_ID_PARAMETER = OpenApiParameter(
    name="account_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Account identifier",
    examples=[OpenApiExample("Account 100", value="100")],
)

BALANCE_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.INT,
    description="Current Balance.",
    examples=[OpenApiExample("Balance", value=20, response_only=True)],
)

RESET_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.STR,
    description="Reset successful.",
)

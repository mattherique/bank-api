from rest_framework import serializers

from app.application.dtos import DepositDTO, TransferDTO, WithdrawDTO
from app.domain.entities.enums import TransactionType


class EventSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[t.value for t in TransactionType])
    amount = serializers.IntegerField(min_value=1)
    origin = serializers.CharField(required=False, max_length=255)
    destination = serializers.CharField(required=False, max_length=255)

    _REQUIRED_FIELDS = {
        TransactionType.DEPOSIT: ("destination",),
        TransactionType.WITHDRAW: ("origin",),
        TransactionType.TRANSFER: ("origin", "destination"),
    }

    def validate(self, attrs: dict) -> dict:
        event_type = TransactionType(attrs["type"])
        required = self._REQUIRED_FIELDS[event_type]

        errors = {
            field: f"required for {event_type.value}"
            for field in required
            if not attrs.get(field)
        }
        errors.update({
            field: f"not allowed for {event_type.value}"
            for field in ("origin", "destination")
            if field not in required and attrs.get(field)
        })
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def to_dto(self) -> DepositDTO | WithdrawDTO | TransferDTO:
        data = self.validated_data
        event_type = TransactionType(data["type"])

        if event_type is TransactionType.DEPOSIT:
            return DepositDTO(destination=data["destination"], amount=data["amount"])
        if event_type is TransactionType.WITHDRAW:
            return WithdrawDTO(origin=data["origin"], amount=data["amount"])
        return TransferDTO(
            origin=data["origin"],
            destination=data["destination"],
            amount=data["amount"],
        )

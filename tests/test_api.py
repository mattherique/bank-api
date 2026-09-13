import json

from django.test import TestCase


class ChallengeSpecTest(TestCase):
    def post_event(self, payload):
        return self.client.post(
            "/event", data=json.dumps(payload), content_type="application/json"
        )

    def assert_response(self, response, status, body):
        self.assertEqual(response.status_code, status)
        raw = response.content.decode()
        if isinstance(body, (dict, list)):
            self.assertEqual(json.loads(raw), body)
        else:
            self.assertEqual(raw, body)

    def test_challenge_sequence(self):
        self.assert_response(self.client.post("/reset"), 200, "OK")

        self.assert_response(
            self.client.get("/balance?account_id=1234"), 404, "0"
        )

        self.assert_response(
            self.post_event({"type": "deposit", "destination": "100", "amount": 10}),
            201,
            {"destination": {"id": "100", "balance": 10}},
        )
        self.assert_response(
            self.post_event({"type": "deposit", "destination": "100", "amount": 10}),
            201,
            {"destination": {"id": "100", "balance": 20}},
        )

        self.assert_response(self.client.get("/balance?account_id=100"), 200, "20")

        self.assert_response(
            self.post_event({"type": "withdraw", "origin": "200", "amount": 10}),
            404,
            "0",
        )
        self.assert_response(
            self.post_event({"type": "withdraw", "origin": "100", "amount": 5}),
            201,
            {"origin": {"id": "100", "balance": 15}},
        )

        self.assert_response(
            self.post_event(
                {
                    "type": "transfer",
                    "origin": "100",
                    "amount": 15,
                    "destination": "300",
                }
            ),
            201,
            {
                "origin": {"id": "100", "balance": 0},
                "destination": {"id": "300", "balance": 15},
            },
        )
        self.assert_response(
            self.post_event(
                {
                    "type": "transfer",
                    "origin": "200",
                    "amount": 15,
                    "destination": "300",
                }
            ),
            404,
            "0",
        )

        self.assert_response(self.client.get("/balance?account_id=100"), 200, "0")
        self.assert_response(self.client.get("/balance?account_id=300"), 200, "15")


class PayloadValidationTest(TestCase):
    def post_event(self, payload):
        return self.client.post(
            "/event", data=json.dumps(payload), content_type="application/json"
        )

    def test_malformed_payloads_are_rejected_with_400(self):
        cases = [
            {"type": "explode", "destination": "100", "amount": 10},
            {"type": "deposit", "destination": "100", "amount": 0},
            {"type": "deposit", "destination": "100", "amount": -5},
            {"type": "deposit", "amount": 10},
            {"type": "withdraw", "amount": 10},
            {"type": "transfer", "origin": "100", "amount": 10},
            {"type": "deposit", "destination": "100", "origin": "200", "amount": 10},
            {"type": "withdraw", "origin": "100", "destination": "300", "amount": 10},
        ]
        for payload in cases:
            with self.subTest(payload=payload):
                self.assertEqual(self.post_event(payload).status_code, 400)

    def test_balance_requires_the_account_id(self):
        self.assertEqual(self.client.get("/balance").status_code, 400)

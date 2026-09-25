import unittest
from fastapi.testclient import TestClient
from backend.api import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.claim = dict(claim_id="CLM001", patient_id="P1001", payer="Example Health Insurance", procedure_code="99213", diagnosis_code="J06.9", claim_amount=250, denial_code="CO-16")

    def test_codes_and_assessments(self):
        codes = self.client.get("/api/denial-codes").json()
        self.assertEqual(len(codes), 7)
        for code in codes:
            self.claim["denial_code"] = code["denial_code"]
            response = self.client.post("/api/assess", json=self.claim)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["denial_info"]["denial_code"], code["denial_code"])
            self.assertEqual(response.json()["recommendation"], code["recommended_action"])

    def test_rejects_invalid_claims(self):
        for changes in ({"claim_id":" "}, {"claim_amount":-1}, {"denial_code":"UNKNOWN"}, {"payer":"x"*121}, {"extra":"unexpected"}):
            with self.subTest(changes=changes):
                self.assertEqual(self.client.post("/api/assess", json={**self.claim, **changes}).status_code, 422)

    def test_health(self):
        self.assertEqual(self.client.get("/api/health").json()["status"], "ok")

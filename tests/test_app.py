import contextlib
import importlib
import io
import json
from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest
from agents.workflow import claim_workflow
from tools.policy_tool import lookup_denial_code

ROOT = Path(__file__).resolve().parents[1]


class ClaimTests(unittest.TestCase):
    def test_reference_codes(self):
        entries = json.loads((ROOT / "data/denial_codes.json").read_text())
        for code, entry in entries.items():
            with self.subTest(code=code):
                result = claim_workflow.invoke({
                    "denial_code": "  " + code.lower() + "  ",
                    "procedure_code": "99213", "diagnosis_code": "J06.9",
                })
                self.assertTrue(result["denial_info"]["found"])
                self.assertEqual(result["denial_info"]["denial_code"], code)
                self.assertEqual(result["recommendation"], entry["recommended_action"])
                self.assertTrue(result["analysis"])

    def test_unknown_and_blank_codes(self):
        for code in ("UNKNOWN", "  "):
            self.assertFalse(lookup_denial_code(code)["found"])

    def test_main_import_has_no_execution(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            importlib.import_module("main")
        self.assertEqual(output.getvalue(), "")

    def test_ui_escapes_claim_input_and_selects_sample(self):
        at = AppTest.from_file(str(ROOT / "app.py")).run(timeout=20)
        self.assertFalse(at.exception)
        at.text_input[3].set_value("<b>INJECTED</b>")
        at.button[0].click().run(timeout=20)
        self.assertFalse(at.exception)
        html = "\n".join(m.proto.body for m in at.get("html"))
        self.assertNotIn("<b>INJECTED</b>", html)
        self.assertIn("&lt;b&gt;INJECTED&lt;/b&gt;", html)
        self.assertEqual(len(at.selectbox[0].options), 7)
        self.assertIn("CO-18 \u2014 Duplicate Claim", at.selectbox[0].options)
        at.selectbox[0].select("CO-18")
        at.button[0].click().run(timeout=20)
        self.assertFalse(at.exception)
        html = "\n".join(m.proto.body for m in at.get("html"))
        self.assertIn('class="code-badge">CO-18', html)
        self.assertIn("Check the claim history", html)


if __name__ == "__main__":
    unittest.main()

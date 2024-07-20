import unittest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)

class TestValidateObject(unittest.TestCase):
    def test_validate_object(self):
        test_cases = [
            # True cases
            ({"object": {}, "max_depth": 1}, True),
            ({"object": {"a1": "b1"}, "max_depth": 1}, True),
            ({"object": {"a1": "b1"}, "max_depth": 2}, True),
            ({"object": {"a1": {}}, "max_depth": 1}, True),
            ({"object": {"a1": {}}, "max_depth": 2}, True),
            ({"object": {"a1": {}, "a2": "b1", "a3": [1, 2, 3]}, "max_depth": 1}, True),
            # False cases
            ({"object": {"a1": {"b1": "c1"}}, "max_depth": 1}, False),
            ({"object": {"a1": {"b1": {}}}, "max_depth": 1}, False),
            ({"object": {"a1": {}, "a2": "b1", "a3": [1, 2, 3], "a4": {"b4": "c4"}}, "max_depth": 1}, False),
        ]
        for payload, expected in test_cases:
            with self.subTest(payload=payload, expected=expected):
                response = client.post("/validate/", json=payload)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), expected)

if __name__ == "__main__":
    unittest.main()

import unittest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)

class TestTruncateObject(unittest.TestCase):
    def test_truncate_object(self):
        test_cases = [
            # no changes cases
            ({"object": {}, "max_depth": 1}, {}),
            ({"object": {"a1": "b1"}, "max_depth": 1}, {"a1": "b1"}),
            ({"object": {"a1": "b1"}, "max_depth": 2}, {"a1": "b1"}),
            ({"object": {"a1": {}}, "max_depth": 1}, {"a1": {}}),
            ({"object": {"a1": {}}, "max_depth": 2}, {"a1": {}}),
            ({"object": {"a1": {}, "a2": "b1", "a3": [1, 2, 3]}, "max_depth": 1}, {"a1": {}, "a2": "b1", "a3": [1, 2, 3]}),
            # truncate cases
            ({"object": {"a1": {"b1": "c1"}}, "max_depth": 1}, {"a1": {}}),
            ({"object": {"a1": {"b1": {}}}, "max_depth": 1}, {"a1": {}}),
            ({"object": {"a1": {}, "a2": "b1", "a3": [1, 2, 3], "a4": {"b4": "c4"}}, "max_depth": 1}, {"a1": {}, "a2": "b1", "a3": [1, 2, 3], "a4": {}}),
        ]
        for payload, expected in test_cases:
            with self.subTest(payload=payload, expected=expected):
                response = client.post("/truncate/", json=payload)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), expected)

if __name__ == "__main__":
    unittest.main()

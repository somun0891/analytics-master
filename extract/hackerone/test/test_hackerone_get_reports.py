"""
Tests for hackerone_get_reports.py
"""

import os
import unittest
from unittest.mock import MagicMock, patch

os.environ["is_full_refresh"] = "false"

# Import the functions to test
from hackerone_get_reports import (
    get_reports,
    get_start_and_end_date,
    nullify_vulnerability_information,
)


class TestHackerOneGetReports(unittest.TestCase):
    """
    Test class for hackerone_get_reports.py
    """

    def setUp(self):
        "Set up environment variables for testing"
        os.environ["data_interval_start"] = "2024-09-02T00:00:00+00:00"
        os.environ["data_interval_end"] = "2024-09-03T00:00:00+00:00"

    def test_get_start_and_end_date(self):
        "Test get_start_and_end_date"
        start_date, end_date = get_start_and_end_date()
        self.assertEqual(start_date, "2024-09-02T00:00:00Z")
        self.assertEqual(end_date, "2024-09-03T00:00:00Z")

    def test_get_start_and_end_date_full_refresh(self):
        "Test get_start_and_end_date with is_full_refresh"
        os.environ["is_full_refresh"] = "true"
        start_date, end_date = get_start_and_end_date()
        self.assertEqual(start_date, "2020-01-01T00:00:00Z")
        self.assertEqual(end_date, "2024-09-03T00:00:00Z")

    @patch("hackerone_get_reports.requests.get")
    def test_get_reports(self, mock_get):
        "Test get_reports"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "123",
                    "attributes": {
                        "state": "triaged",
                        "created_at": "2024-09-02T12:00:00Z",
                    },
                    "relationships": {
                        "bounties": {"data": [{"attributes": {"amount": "500"}}]}
                    },
                }
            ],
            "links": {},
        }
        mock_get.return_value = mock_response

        reports = get_reports("2024-09-02T00:00:00Z", "2024-09-03T00:00:00Z")

        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["id"], "123")
        self.assertEqual(reports[0]["state"], "triaged")
        self.assertEqual(reports[0]["created_at"], "2024-09-02T12:00:00Z")
        self.assertIn("bounties", reports[0])

    def test_nullify_vulnerability_information(self):
        "Test nullify_vulnerability_information"
        report_data = {
            "bounties": [
                {
                    "relationships": {
                        "report": {
                            "data": {
                                "attributes": {
                                    "vulnerability_information": "sensitive info"
                                }
                            }
                        }
                    }
                }
            ]
        }

        nullified_data = nullify_vulnerability_information(report_data)

        self.assertEqual(
            nullified_data["bounties"][0]["relationships"]["report"]["data"][
                "attributes"
            ]["vulnerability_information"],
            "None",
        )


if __name__ == "__main__":
    unittest.main()

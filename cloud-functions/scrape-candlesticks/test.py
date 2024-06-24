import unittest
from unittest.mock import MagicMock, patch

from flask import Request
from main import main


class TestCloudFunction(unittest.TestCase):

    @patch("main.requests.post")
    @patch("main.requests.get")
    @patch("main.log")
    def test_main(self, mock_log, mock_get, mock_post):
        def mock_get_side_effect(url, params=None):
            if "tickers" in url:
                return MagicMock(
                    status_code=200,
                    json=lambda: {
                        "exchange_token": "100",
                        "upstox_instrument_key": "NSE_EQ|INE885A01032",
                    },
                )
            elif "historical-candle" in url:
                return MagicMock(
                    status_code=200,
                    json=lambda: {
                        "data": {
                            "candles": [
                                [
                                    "2023-10-01T00:00:00+05:30",
                                    100,
                                    200,
                                    50,
                                    150,
                                    1000,
                                    500,
                                ]
                            ]
                        }
                    },
                )

        mock_get.side_effect = mock_get_side_effect
        mock_post.return_value.status_code = 200

        # Given
        request_payload = {
            "date": "2020-01-01",
            "smallcase_name": "Amara Raja Energy & Mobility Ltd",
        }
        request = MagicMock(Request)
        request.get_json.return_value = request_payload

        # When
        response = main(request)

        # Then
        self.assertEqual(response[1], 200)
        mock_get.assert_called()
        mock_post.assert_called()


if __name__ == "__main__":
    unittest.main()

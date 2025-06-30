import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd
from inverse_volatility import get_volatility_and_performance

class TestInverseVolatility(unittest.TestCase):
    def setUp(self):
        # Mock data for UPRO around 2020-02-15
        self.mock_prices = [
            103.5,   # 2020-01-26 (oldest)
            103.2,  # 2020-01-27
            102.8,  # 2020-01-28
            103.0,  # 2020-01-29
            102.5,  # 2020-01-30
            101.9,  # 2020-01-31
            102.2,  # 2020-02-01
            101.8,  # 2020-02-02
            102.0,  # 2020-02-03
            101.5,  # 2020-02-04
            100.8,  # 2020-02-05
            101.2,  # 2020-02-06
            100.5,  # 2020-02-07
            99.8,   # 2020-02-08
            100.2,  # 2020-02-09
            99.5,   # 2020-02-10
            98.1,   # 2020-02-11
            97.8,   # 2020-02-12
            99.2,   # 2020-02-13
            98.5,   # 2020-02-14
            100.0   # 2020-02-15 (most recent)
        ]
        # The most recent date is 2020-02-15, matching the reference date
        self.mock_dates = [datetime(2020, 1, 26) + timedelta(days=i) for i in range(21)]
        self.mock_df = pd.DataFrame({
            'Close': self.mock_prices
        }, index=self.mock_dates)

    @patch('yfinance.Ticker')
    def test_get_volatility_and_performance(self, mock_ticker):
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.history.return_value = self.mock_df
        mock_ticker.return_value = mock_instance

        # Test with UPRO
        volatility, performance = get_volatility_and_performance('UPRO')

        # Expected values (calculated from mock data)
        expected_volatility = 0.114866  # Calculated volatility
        expected_performance = -0.033816  # Calculated performance

        # Assert with some tolerance for floating point calculations
        self.assertAlmostEqual(volatility, expected_volatility, places=6)
        self.assertAlmostEqual(performance, expected_performance, places=6)

    @patch('yfinance.Ticker')
    def test_insufficient_data(self, mock_ticker):
        # Create mock history with insufficient data
        insufficient_df = self.mock_df.iloc[:10]  # Only 10 days of data
        mock_instance = MagicMock()
        mock_instance.history.return_value = insufficient_df
        mock_ticker.return_value = mock_instance

        # Test that it raises an exception for insufficient data
        with self.assertRaises(Exception) as context:
            get_volatility_and_performance('UPRO')
        
        self.assertTrue('Not enough data points' in str(context.exception))

if __name__ == '__main__':
    unittest.main() 
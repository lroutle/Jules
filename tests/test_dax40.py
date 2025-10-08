import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from dax40 import compute_performance, get_dax40_data

class TestDax40(unittest.TestCase):
    @patch('yfinance.Ticker')
    def test_classification_strong_sell(self, mock_ticker):
        # Mocking the yfinance Ticker object
        mock_instance = mock_ticker.return_value
        mock_instance.history.return_value = pd.DataFrame({'Close': [100]})
        mock_instance.recommendations_summary = pd.DataFrame({
            'strongBuy': [0],
            'buy': [0],
            'hold': [2],
            'sell': [8],
            'strongSell': [10]
        }, index=[0])

        # Define a single ticker for the test
        mock_tickers = [("MOCK.DE", "Mock Company")]

        # Running the function
        df = get_dax40_data(mock_tickers)

        # Assertion
        self.assertEqual(df.loc[df['Ticker'] == 'MOCK.DE', 'Classification'].iloc[0], 'Strong Sell')

if __name__ == '__main__':
    unittest.main()
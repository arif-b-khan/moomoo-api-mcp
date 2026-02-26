"""Unit tests for option-related MarketDataService methods."""

import pytest
from unittest.mock import MagicMock
import pandas as pd

from moomoo_mcp.services.market_data_service import MarketDataService


@pytest.fixture
def mock_quote_ctx():
    return MagicMock()


@pytest.fixture
def market_data_service(mock_quote_ctx):
    return MarketDataService(quote_ctx=mock_quote_ctx)


def test_get_option_expiration_date_success(market_data_service, mock_quote_ctx):
    df = pd.DataFrame([
        {"strike_time": "2026-03-19", "option_expiry_date_distance": 10, "expiration_cycle": "WEEK"}
    ])
    mock_quote_ctx.get_option_expiration_date.return_value = (0, df)

    result = market_data_service.get_option_expiration_date(code="HK.00700")

    assert len(result) == 1
    assert result[0]["strike_time"] == "2026-03-19"
    mock_quote_ctx.get_option_expiration_date.assert_called_once()


def test_get_option_expiration_date_error(market_data_service, mock_quote_ctx):
    mock_quote_ctx.get_option_expiration_date.return_value = (-1, "error")

    with pytest.raises(RuntimeError, match="get_option_expiration_date failed"):
        market_data_service.get_option_expiration_date(code="HK.00700")


def test_get_option_chain_success(market_data_service, mock_quote_ctx):
    df = pd.DataFrame([
        {"code": "HK.TCH220330C490000", "strike_time": "2026-03-30", "strike_price": 490.0}
    ])
    mock_quote_ctx.get_option_chain.return_value = (0, df)

    result = market_data_service.get_option_chain(code="HK.00700", start="2026-03-30", end="2026-03-30")

    assert len(result) == 1
    assert result[0]["code"] == "HK.TCH220330C490000"
    mock_quote_ctx.get_option_chain.assert_called_once()


def test_get_option_chain_date_span_error(market_data_service, mock_quote_ctx):
    # Span > 30 days should raise
    with pytest.raises(RuntimeError, match="date span exceeds 30 days"):
        market_data_service.get_option_chain(code="HK.00700", start="2026-01-01", end="2026-03-31")


def test_get_option_chain_error(market_data_service, mock_quote_ctx):
    mock_quote_ctx.get_option_chain.return_value = (-1, "api error")

    with pytest.raises(RuntimeError, match="get_option_chain failed"):
        market_data_service.get_option_chain(code="HK.00700", start="2026-03-30", end="2026-03-30")

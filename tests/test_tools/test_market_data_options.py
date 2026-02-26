"""Unit tests for option-related market data tools."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from mcp.shared.context import RequestContext
from mcp.server.fastmcp import Context
from moomoo_mcp.server import AppContext
from moomoo_mcp.services.market_data_service import MarketDataService
from moomoo_mcp.tools.market_data import get_option_chain, get_option_expiration_date


@pytest.fixture
def mock_market_data_service():
    return MagicMock(spec=MarketDataService)


@pytest.fixture
def app_context(mock_market_data_service):
    return AppContext(
        moomoo_service=None,
        trade_service=None,
        market_data_service=mock_market_data_service,
    )


@pytest.fixture
def mcp_context(app_context):
    mock_session = MagicMock()
    mock_session.send_log_message = AsyncMock()

    request_context = RequestContext(
        request_id="test-req",
        meta=None,
        session=mock_session,
        lifespan_context=app_context,
    )

    mock_fastmcp = MagicMock()
    return Context(request_context=request_context, fastmcp=mock_fastmcp)


@pytest.mark.asyncio
async def test_get_option_expiration_date_tool(mcp_context, mock_market_data_service):
    mock_market_data_service.get_option_expiration_date.return_value = [
        {"strike_time": "2026-03-19"}
    ]

    result = await get_option_expiration_date(mcp_context, code="HK.00700")

    assert len(result) == 1
    assert result[0]["strike_time"] == "2026-03-19"
    mock_market_data_service.get_option_expiration_date.assert_called_once_with(code="HK.00700", index_option_type=None)


@pytest.mark.asyncio
async def test_get_option_chain_tool(mcp_context, mock_market_data_service):
    mock_market_data_service.get_option_chain.return_value = [
        {"code": "HK.TCH220330C490000", "strike_time": "2026-03-30"}
    ]

    result = await get_option_chain(mcp_context, code="HK.00700", start="2026-03-30", end="2026-03-30")

    assert len(result) == 1
    assert result[0]["code"] == "HK.TCH220330C490000"
    mock_market_data_service.get_option_chain.assert_called_once()

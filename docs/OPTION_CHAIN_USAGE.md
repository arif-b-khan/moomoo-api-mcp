Option Chain & Expiration — Usage Guide
======================================

Overview
--------
This document explains how to use the new MCP tools `get_option_expiration_date` and `get_option_chain` added in the `feature/add-option-chain-tool` branch.

MCP tool names
- `get_option_expiration_date(code: str, index_option_type: str | None = None) -> list[dict]`
- `get_option_chain(code: str, index_option_type: str | None = None, start: str | None = None, end: str | None = None, option_type: str | None = None, option_cond_type: str | None = None, data_filter: dict | None = None, max_count: int | None = None) -> list[dict]`

Parameters explanation
- `code`: underlying stock code (e.g., `HK.00700`, `US.AAPL`).
- `index_option_type`: optional enum name or value (map to SDK `IndexOptionType`).
- `start` / `end`: YYYY-MM-DD date range for expiration filter (max 30-day span). End must be today or a future date.
- `option_type`: `CALL`, `PUT`, or None for both.
- `option_cond_type`: in/out-of-the-money filter (map to SDK `OptionCondType`).
- `data_filter`: dict of numeric filters (implied_volatility_min/max, delta_min/max, gamma_min/max, vega_min/max, theta_min/max, rho_min/max, net_open_interest_min/max, open_interest_min/max, vol_min/max).

Return format
- Both tools return `list[dict]` when successful. Each dict comes from the SDK DataFrame converted via `to_dict('records')`.
- Example fields for `get_option_chain` records: `code`, `name`, `lot_size`, `stock_type`, `option_type`, `stock_owner`, `strike_time`, `strike_price`, `suspension`, `stock_id`, `index_option_type`, `expiration_cycle`, `option_standard_type`, `option_settlement_mode`, etc.

Examples
--------
1) Get expirations and then an option chain for a selected expiration date:

From an MCP client (RPC call named `get_option_expiration_date`):

  - Call `get_option_expiration_date(code='HK.00700')` -> returns list of expiry rows with `strike_time`.
  - Choose a date `d = '2026-03-30'` and call:
    `get_option_chain(code='HK.00700', start=d, end=d, data_filter={'delta_min':0,'delta_max':0.1})`

2) Example `mcp` Python client call (pseudo):

  result = mcp_client.call('get_option_chain', code='HK.00700', start='2026-03-30', end='2026-03-30')

Notes & limits
--------------
- `get_option_chain`: max 10 requests per 30 seconds. Do not query expired option chains; pick today or future dates for `end`.
- `get_option_expiration_date`: max 60 requests per 30 seconds.
- The service raises `RuntimeError` on SDK errors; MCP tools propagate those exceptions back to callers.

Testing
-------
- Unit tests are included in `tests/test_services/test_market_data_service_options.py` and `tests/test_tools/test_market_data_options.py`. These use mocked `quote_ctx` and `mcp.Context` fixtures.
- For integration testing, run the MCP server and use a real `OpenQuoteContext` or the moomoo emulator.

Troubleshooting
---------------
- If you get SDK errors, inspect the `data` returned when `ret != RET_OK` for human-readable messages.
- If tests fail due to missing packages (`moomoo`, `mcp`), ensure test environment has those packages or run tests that mock them only.

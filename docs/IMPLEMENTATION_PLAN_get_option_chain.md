Implementation Plan: Get Option Chain & Expiration (feature/add-option-chain-tool)

Overview
--------
Add moomoo option-chain and option-expiration retrieval to the MCP server. Place SDK logic in MarketDataService and expose thin MCP tools in tools/market_data.py named get_option_chain and get_option_expiration_date.

Files added / changed
- Modified: src/moomoo_mcp/services/market_data_service.py
  - Added get_option_expiration_date(...) and get_option_chain(...)
- Modified: src/moomoo_mcp/tools/market_data.py
  - Added MCP tools get_option_expiration_date and get_option_chain
- Added tests:
  - tests/test_services/test_market_data_service_options.py
  - tests/test_tools/test_market_data_options.py

Design decisions
----------------
- Service-first: SDK interaction implemented in MarketDataService to reuse shared quote_ctx.
- Tools stay in tools/market_data.py to avoid touching server imports; consider tools/options.py later.
- Filters: tool accepts data_filter as dict; service converts to OptionDataFilter.

Validation & limits
-------------------
- Date window: get_option_chain enforces max 30-day span and raises RuntimeError on invalid span.
- Rate limits: document and recommend caller throttling (see moomoo API limits).

Testing
-------
- Unit tests mock quote_ctx responses (pandas DataFrame-like) and assert behavior.
- Integration: start MCP server and call tools with a real OpenQuoteContext to validate response shape.

Blockers / confirmations
-----------------------
- Confirm SDK class/enum names: OptionDataFilter, IndexOptionType, OptionType, OptionCondType.
- Decide whether to implement retry/backoff for transient errors (429).

Next steps
----------
1. Review and merge PR for feature/add-option-chain-tool.
2. Add integration tests or examples using emulator/real quote_ctx.
3. Optionally extract option tools into tools/options.py as feature set grows.

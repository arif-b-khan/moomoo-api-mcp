"""Market data service for accessing quote data via Moomoo API."""

from moomoo import (
    OpenQuoteContext,
    RET_OK,
    SubType,
    KLType,
    AuType,
    OptionDataFilter,
    IndexOptionType,
    OptionType,
    OptionCondType,
)
from datetime import datetime


class MarketDataService:
    """Service to access market data via OpenQuoteContext.

    This service provides methods to retrieve market quotes, historical K-line data,
    snapshots, and order book data. It uses the shared OpenQuoteContext from MoomooService.
    """

    def __init__(self, quote_ctx: OpenQuoteContext):
        """Initialize MarketDataService with an existing quote context.

        Args:
            quote_ctx: An already-connected OpenQuoteContext instance.
        """
        self.quote_ctx = quote_ctx

    def subscribe(self, codes: list[str], sub_types: list[SubType]) -> None:
        """Subscribe to real-time data for specified stocks and data types.

        Args:
            codes: List of stock codes (e.g., ['US.AAPL', 'HK.00700']).
            sub_types: List of subscription types (e.g., [SubType.QUOTE, SubType.ORDER_BOOK]).

        Raises:
            RuntimeError: If subscription fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        ret, err = self.quote_ctx.subscribe(codes, sub_types, subscribe_push=False)
        if ret != RET_OK:
            raise RuntimeError(f"subscribe failed: {err}")

    def get_stock_quote(self, codes: list[str]) -> list[dict]:
        """Get real-time quotes for stocks.

        This method automatically subscribes to the stocks before fetching quotes.
        Returns current price, open, high, low, close, volume and other quote data.

        Args:
            codes: List of stock codes (e.g., ['US.AAPL']).

        Returns:
            List of quote dictionaries with price, volume, and other quote fields.

        Raises:
            RuntimeError: If quote retrieval fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        # Auto-subscribe before getting quotes
        self.subscribe(codes, [SubType.QUOTE])

        ret, data = self.quote_ctx.get_stock_quote(codes)
        if ret != RET_OK:
            raise RuntimeError(f"get_stock_quote failed: {data}")

        return data.to_dict("records")

    def get_historical_klines(
        self,
        code: str,
        ktype: str = "K_DAY",
        start: str | None = None,
        end: str | None = None,
        max_count: int = 100,
        autype: str = "QFQ",
    ) -> list[dict]:
        """Get historical candlestick (K-line) data.

        Args:
            code: Stock code (e.g., 'US.AAPL').
            ktype: K-line type. Options: K_1M, K_3M, K_5M, K_15M, K_30M, K_60M,
                   K_DAY, K_WEEK, K_MON, K_QUARTER, K_YEAR.
            start: Start date (YYYY-MM-DD format). Defaults to 365 days before end.
            end: End date (YYYY-MM-DD format). Defaults to today.
            max_count: Maximum number of candles to return (default 100).
            autype: Adjustment type. Options: QFQ (forward), HFQ (backward), NONE.

        Returns:
            List of K-line dictionaries with time_key, open, high, low, close, volume.

        Raises:
            RuntimeError: If K-line retrieval fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        # Convert string ktype to enum
        ktype_enum = getattr(KLType, ktype, KLType.K_DAY)
        autype_enum = getattr(AuType, autype, AuType.QFQ)

        ret, data, _ = self.quote_ctx.request_history_kline(
            code=code,
            start=start,
            end=end,
            ktype=ktype_enum,
            autype=autype_enum,
            max_count=max_count,
        )
        if ret != RET_OK:
            raise RuntimeError(f"request_history_kline failed: {data}")

        return data.to_dict("records")

    def get_market_snapshot(self, codes: list[str]) -> list[dict]:
        """Get market snapshot for multiple stocks.

        This is efficient for batch queries and does not require subscription.
        Returns current price, change, volume, and comprehensive market data.

        Args:
            codes: List of stock codes (up to 400). E.g., ['US.AAPL', 'US.TSLA'].

        Returns:
            List of snapshot dictionaries with last_price, open_price, high_price,
            low_price, prev_close_price, volume, turnover, and more.

        Raises:
            RuntimeError: If snapshot retrieval fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        if not codes:
            return []

        ret, data = self.quote_ctx.get_market_snapshot(codes)
        if ret != RET_OK:
            raise RuntimeError(f"get_market_snapshot failed: {data}")

        return data.to_dict("records")

    def get_order_book(self, code: str, num: int = 10) -> dict:
        """Get order book (market depth) for a stock.

        This method automatically subscribes to the stock before fetching the order book.
        Returns bid and ask price levels with volumes.

        Args:
            code: Stock code (e.g., 'HK.00700').
            num: Number of price levels to return (default 10).

        Returns:
            Dictionary with 'code', 'Bid' (list of tuples), and 'Ask' (list of tuples).
            Each tuple contains (price, volume, order_count, order_details).

        Raises:
            RuntimeError: If order book retrieval fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        # Auto-subscribe before getting order book
        self.subscribe([code], [SubType.ORDER_BOOK])

        ret, data = self.quote_ctx.get_order_book(code, num=num)
        if ret != RET_OK:
            raise RuntimeError(f"get_order_book failed: {data}")

        return data

    def get_user_security_group(self, group_type: int = 0) -> list[dict]:
        """Get list of user-defined security groups (watchlists).

        Args:
            group_type: Type of groups to return. Options:
                - 0: All groups (default)
                - 1: Custom groups only
                - 2: System groups only

        Returns:
            List of group dictionaries with group_name, group_id, etc.

        Raises:
            RuntimeError: If retrieval fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        from moomoo import UserSecurityGroupType

        group_type_enum = UserSecurityGroupType.ALL
        if group_type == 1:
            group_type_enum = UserSecurityGroupType.CUSTOM
        elif group_type == 2:
            group_type_enum = UserSecurityGroupType.SYSTEM

        ret, data = self.quote_ctx.get_user_security_group(group_type=group_type_enum)
        if ret != RET_OK:
            raise RuntimeError(f"get_user_security_group failed: {data}")

        return data.to_dict("records")

    def get_user_security(self, group_name: str) -> list[dict]:
        """Get list of securities in a specific user-defined group (watchlist).

        Args:
            group_name: Name of the security group (e.g., 'Favorites').

        Returns:
            List of security dictionaries with code, name, lot_size, etc.

        Raises:
            RuntimeError: If retrieval fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        ret, data = self.quote_ctx.get_user_security(group_name)
        if ret != RET_OK:
            raise RuntimeError(f"get_user_security failed: {data}")

        return data.to_dict("records")

    def get_option_expiration_date(self, code: str, index_option_type: str | None = None) -> list[dict]:
        """Get option expiration dates for an underlying stock.

        Args:
            code: Stock code (e.g., 'HK.00700').
            index_option_type: Optional index option type enum name or value.

        Returns:
            List of dicts with fields like `strike_time`, `option_expiry_date_distance`, `expiration_cycle`.

        Raises:
            RuntimeError: If the quote context is not connected or SDK call fails.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        index_enum = None
        if index_option_type is not None:
            index_enum = getattr(IndexOptionType, index_option_type, index_option_type)

        ret, data = self.quote_ctx.get_option_expiration_date(code=code, index_option_type=index_enum)
        if ret != RET_OK:
            raise RuntimeError(f"get_option_expiration_date failed: {data}")

        return data.to_dict("records")

    def get_option_chain(
        self,
        code: str,
        index_option_type: str | None = None,
        start: str | None = None,
        end: str | None = None,
        option_type: str | None = None,
        option_cond_type: str | None = None,
        data_filter: dict | None = None,
        max_count: int | None = None,
    ) -> list[dict]:
        """Retrieve option chain data for an underlying security.

        Args:
            code: Underlying code (e.g., 'HK.00700').
            index_option_type: Optional index option type enum name or value.
            start: Start date (YYYY-MM-DD) for expiration filter.
            end: End date (YYYY-MM-DD) for expiration filter (inclusive).
            option_type: 'CALL', 'PUT', or None for both.
            option_cond_type: In/Out of the money filter enum name or value.
            data_filter: Dict of numeric filters matching OptionDataFilter fields.
            max_count: Optional maximum number of rows to return (SDK may limit results).

        Returns:
            List[dict] of option records.

        Raises:
            RuntimeError: If quote context not connected or SDK returns error.
        """
        if not self.quote_ctx:
            raise RuntimeError("Quote context not connected")

        # Validate date window (API limits to 30 days span)
        if start is not None or end is not None:
            # normalize to datetime.date
            fmt = "%Y-%m-%d"
            if start is None:
                # if only end provided, start = end - 30 days
                end_date = datetime.strptime(end, fmt).date()
                start_date = end_date
            elif end is None:
                start_date = datetime.strptime(start, fmt).date()
                end_date = start_date
            else:
                start_date = datetime.strptime(start, fmt).date()
                end_date = datetime.strptime(end, fmt).date()
            # compute span
            delta = (end_date - start_date).days
            if delta < 0:
                raise RuntimeError("get_option_chain failed: end date is before start date")
            if delta > 30:
                raise RuntimeError("get_option_chain failed: date span exceeds 30 days")

        index_enum = None
        if index_option_type is not None:
            index_enum = getattr(IndexOptionType, index_option_type, index_option_type)

        option_type_enum = None
        if option_type is not None:
            option_type_enum = getattr(OptionType, option_type, option_type)

        option_cond_enum = None
        if option_cond_type is not None:
            option_cond_enum = getattr(OptionCondType, option_cond_type, option_cond_type)

        filter_obj = None
        if data_filter:
            filter_obj = OptionDataFilter()
            for k, v in data_filter.items():
                if hasattr(filter_obj, k):
                    setattr(filter_obj, k, v)

        # Call SDK
        kwargs = {
            "code": code,
            "index_option_type": index_enum,
            "start": start,
            "end": end,
            "option_type": option_type_enum,
            "option_cond_type": option_cond_enum,
            "data_filter": filter_obj,
        }
        if max_count is not None:
            kwargs["max_count"] = max_count

        # Remove None values to pass only provided args
        call_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        ret, data = self.quote_ctx.get_option_chain(**call_kwargs)
        if ret != RET_OK:
            raise RuntimeError(f"get_option_chain failed: {data}")

        return data.to_dict("records")

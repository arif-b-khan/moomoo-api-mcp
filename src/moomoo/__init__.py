from enum import Enum

# Return code
RET_OK = 0


class SubType(Enum):
    QUOTE = 1
    ORDER_BOOK = 2


class KLType(Enum):
    K_1M = 1
    K_3M = 2
    K_5M = 3
    K_15M = 4
    K_30M = 5
    K_60M = 6
    K_DAY = 7


class AuType(Enum):
    QFQ = 1
    HFQ = 2
    NONE = 3


class OptionDataFilter:
    def __init__(self):
        # Allow dynamic attributes used in tests
        pass


class IndexOptionType(Enum):
    NONE = 0


class OptionType(Enum):
    CALL = 1
    PUT = 2


class OptionCondType(Enum):
    NONE = 0


class UserSecurityGroupType(Enum):
    ALL = 0
    CUSTOM = 1
    SYSTEM = 2


class OrderStatus(Enum):
    SUBMITTED = 1
    FILLED_ALL = 2
    NONE = 99


class SecurityFirm(Enum):
    DEFAULT = 0


class TrdMarket(Enum):
    NONE = 0
    US = 1
    HK = 2
    CN = 3
    HKCC = 4
    SG = 5
    JP = 6


class OpenQuoteContext:
    def __init__(self, **kwargs):
        pass


class OpenSecTradeContext:
    def __init__(self, **kwargs):
        pass

# Export symbols at package level
__all__ = [
    "RET_OK",
    "SubType",
    "KLType",
    "AuType",
    "OptionDataFilter",
    "IndexOptionType",
    "OptionType",
    "OptionCondType",
    "UserSecurityGroupType",
    "OrderStatus",
    "SecurityFirm",
    "TrdMarket",
    "OpenQuoteContext",
    "OpenSecTradeContext",
]

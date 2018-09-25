from enum import Enum
from enum import auto


class Currency(Enum):
    USD = auto()
    CAD = auto()


class ListingExchange(Enum):
    TSX = auto()
    TSXV = auto()
    CNSX = auto()
    MX = auto()
    NASDAQ = auto()
    NYSE = auto()
    NYSEAM = auto()
    ARCA = auto()
    OPRA = auto()
    PinkSheets = auto()
    OTCBB = auto()


class AccountType(Enum):
    Cash = auto()
    Margin = auto()
    TFSA = auto()
    RRSP = auto()
    SRRSP = auto()
    LRRSP = auto()
    LIRA = auto()
    LIF = auto()
    RIF = auto()
    SRIF = auto()
    LRIF = auto()
    RRIF = auto()
    PRIF = auto()
    RESP = auto()
    FRESP = auto()


class ClientAccountType(Enum):
    Individual = auto()
    Joint = auto()
    #Informal Trust = auto()
    Corporation = auto()
    #Investment Club = auto()
    #Formal Trust = auto()
    Partnership = auto()
    #Sole Proprietorship = auto()
    Family = auto()
    #Joint and Informal Trust = auto()
    Institution = auto()


class AccountStatus(Enum):
    Active = auto()
    #Suspended (Closed) = auto()
    #Suspended (View Only) = auto()
    #Liquidate Only = auto()
    Closed = auto()


class TickType(Enum):
    Up = auto()
    Down = auto()
    Equal = auto()


class OptionType(Enum):
    Call = auto()
    Put = auto()


class OptionDurationType(Enum):
    Weekly = auto()
    Monthly = auto()
    Quarterly = auto()
    LEAP = auto()


class OptionExerciseType(Enum):
    American = auto()
    European = auto()


class SecurityType(Enum):
    Stock = auto()
    Option = auto()
    Bond = auto()
    Right = auto()
    Gold = auto()
    MutualFund = auto()
    Index = auto()


class OrderStateFilterType(Enum):
    All = auto()
    Open = auto()
    Closed = auto()


class OrderAction(Enum):
    Buy = auto()
    Sell = auto()


class OrderSide(Enum):
    Buy = auto()
    Sell = auto()
    Short = auto()
    Cov = auto()
    BTO = auto()
    STC = auto()
    STO = auto()
    BTC = auto()


class OrderType(Enum):
    Market = auto()
    Limit = auto()
    Stop = auto()
    StopLimit = auto()
    TrailStopInPercentage = auto()
    TrailStopInDollar = auto()
    TrailStopLimitInPercentage = auto()
    TrailStopLimitInDollar = auto()
    LimitOnOpen = auto()
    LimitOnClose = auto()


class OrderTimeInForce(Enum):
    Day = auto()
    GoodTillCanceled = auto()
    GoodTillExtendedDay = auto()
    GoodTillDate = auto()
    ImmediateOrCancel = auto()
    FillOrKill = auto()


class OrderState(Enum):
    Failed = auto()
    Pending = auto()
    Accepted = auto()
    Rejected = auto()
    CancelPending = auto()
    Canceled = auto()
    PartialCanceled = auto()
    Partial = auto()
    Executed = auto()
    ReplacePending = auto()
    Replaced = auto()
    Stopped = auto()
    Suspended = auto()
    Expired = auto()
    Queued = auto()
    Triggered = auto()
    Activated = auto()
    PendingRiskReview = auto()
    ContingentOrder = auto()


class HistoricalDataGranularity(Enum):
    OneMinute = auto()
    TwoMinutes = auto()
    ThreeMinutes = auto()
    FourMinutes = auto()
    FiveMinutes = auto()
    TenMinutes = auto()
    FifteenMinutes = auto()
    TwentyMinutes = auto()
    HalfHour = auto()
    OneHour = auto()
    TwoHours = auto()
    FourHours = auto()
    OneDay = auto()
    OneWeek = auto()
    OneMonth = auto()
    OneYear = auto()


class OrderClass(Enum):
    Primary = auto()
    Limit = auto()
    StopLoss = auto()


class StrategyTypes(Enum):
    CoveredCall = auto()
    MarriedPuts = auto()
    VerticalCallSpread = auto()
    VerticalPutSpread = auto()
    CalendarCallSpread = auto()
    CalendarPutSpread = auto()
    DiagonalCallSpread = auto()
    DiagonalPutSpread = auto()
    Collar = auto()
    Straddle = auto()
    Strangle = auto()
    ButterflyCall = auto()
    ButterflyPut = auto()
    IronButterfly = auto()
    CondorCall = auto()
    Custom = auto()

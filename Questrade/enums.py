from enum import Enum


class Currency(Enum):
    USD = 0
    CAD = 1


class ListingExchange(Enum):
    TSX = 0
    TSXV = 1
    CNSX = 2
    MX = 3
    NASDAQ = 4
    NYSE = 5
    NYSEAM = 6
    ARCA = 7
    OPRA = 8
    PinkSheets = 9
    OTCBB = 10


class AccountType(Enum):
    Cash = 0
    Margin = 1
    TFSA = 2
    RRSP = 3
    SRRSP = 4
    LRRSP = 5
    LIRA = 6
    LIF = 7
    RIF = 8
    SRIF = 9
    LRIF = 10
    RRIF = 11
    PRIF = 12
    RESP = 13
    FRESP = 14


class ClientAccountType(Enum):
    Individual = 0
    Joint = 1
    #Informal Trust = 2
    Corporation = 3
    #Investment Club = 4
    #Formal Trust = 5
    Partnership = 6
    #Sole Proprietorship = 7
    Family = 8
    #Joint and Informal Trust = 9
    Institution = 10


class AccountStatus(Enum):
    Active = 0
    #Suspended (Closed) = 1
    #Suspended (View Only) = 2
    #Liquidate Only = 3
    Closed = 4


class TickType(Enum):
    Up = 0
    Down = 1
    Equal = 2


class OptionType(Enum):
    Call = 0
    Put = 1


class OptionDurationType(Enum):
    Weekly = 0
    Monthly = 1
    Quarterly = 2
    LEAP = 3


class OptionExerciseType(Enum):
    American = 0
    European = 1


class SecurityType(Enum):
    Stock = 0
    Option = 1
    Bond = 2
    Right = 3
    Gold = 4
    MutualFund = 5
    Index = 6


class OrderStateFilterType(Enum):
    All = 0
    Open = 1
    Closed = 2


class OrderAction(Enum):
    Buy = 0
    Sell = 1


class OrderSide(Enum):
    Buy = 0
    Sell = 1
    Short = 2
    Cov = 3
    BTO = 4
    STC = 5
    STO = 6
    BTC = 7


class OrderType(Enum):
    Market = 0
    Limit = 1
    Stop = 2
    StopLimit = 3
    TrailStopInPercentage = 4
    TrailStopInDollar = 5
    TrailStopLimitInPercentage = 6
    TrailStopLimitInDollar = 7
    LimitOnOpen = 8
    LimitOnClose = 9


class OrderTimeInForce(Enum):
    Day = 0
    GoodTillCanceled = 1
    GoodTillExtendedDay = 2
    GoodTillDate = 3
    ImmediateOrCancel = 4
    FillOrKill = 5


class OrderState(Enum):
    Failed = 0
    Pending = 1
    Accepted = 2
    Rejected = 3
    CancelPending = 4
    Canceled = 5
    PartialCanceled = 6
    Partial = 7
    Executed = 8
    ReplacePending = 9
    Replaced = 10
    Stopped = 11
    Suspended = 12
    Expired = 13
    Queued = 14
    Triggered = 15
    Activated = 16
    PendingRiskReview = 17
    ContingentOrder = 18


class HistoricalDataGranularity(Enum):
    OneMinute = 0
    TwoMinutes = 1
    ThreeMinutes = 2
    FourMinutes = 3
    FiveMinutes = 4
    TenMinutes = 5
    FifteenMinutes = 6
    TwentyMinutes = 7
    HalfHour = 8
    OneHour = 9
    TwoHours = 10
    FourHours = 11
    OneDay = 12
    OneWeek = 13
    OneMonth = 14
    OneYear = 15


class OrderClass(Enum):
    Primary = 0
    Limit = 1
    StopLoss = 2


class StrategyTypes(Enum):
    CoveredCall = 0
    MarriedPuts = 1
    VerticalCallSpread = 2
    VerticalPutSpread = 3
    CalendarCallSpread = 4
    CalendarPutSpread = 5
    DiagonalCallSpread = 6
    DiagonalPutSpread = 7
    Collar = 8
    Straddle = 9
    Strangle = 10
    ButterflyCall = 11
    ButterflyPut = 12
    IronButterfly = 13
    CondorCall = 14
    Custom = 15

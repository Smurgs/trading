from datetime import datetime


class OptionDataFrame(object):
    def __init__(self, bid_price, bid_size, ask_price, ask_size, volume, volatility, delta, gamma, theta, vega, rho, open_interest, time):
        """Builds OptionDataFrame object that represents an option price for an interval of time (5 min)

            Args:
                bid_price (float): bid price
                bid_size (int): bid size
                ask_price (float): ask price
                ask_size (int): ask size
                volume (int): volume of contract traded today
                volatility (float): implied volatility of the contract
                delta (float): delta
                gamma (float): gamma
                theta (float): theta
                vega (float): vega
                rho (float): rho
                open_interest (int): number of contracts open
                time (datetime): time quote was taken
        """
        self.bid_price = bid_price
        self.bid_size = bid_size
        self.ask_price = ask_price
        self.ask_size = ask_size
        self.volume = volume
        self.volatility = volatility
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.rho = rho
        self.open_interest = open_interest
        self.time = time

    @staticmethod
    def to_dict(df):
        if type(df) is not OptionDataFrame:
            raise ValueError('Function only accepts OptionDataFrame objects')

        ret = {
            'bp': df.bid_price,
            'bs': df.bid_size,
            'ap': df.ask_price,
            'as': df.ask_size,
            'v': df.volume,
            'vola': df.volatility,
            'd': df.delta,
            'g': df.gamma,
            't': df.theta,
            've': df.vega,
            'r': df.rho,
            'o': df.open_interest,
            'ti': df.time.strftime("%Y-%m-%d %H:%M"),
        }
        return ret

    @staticmethod
    def from_dict(json):
        bid_price = float(json['bp']) if json['bp'] is not None else None
        bid_size = int(json['bs'])
        ask_price = float(json['ap']) if json['ap'] is not None else None
        ask_size = int(json['as'])
        volume = int(json['v'])
        volatility = float(json['vola'])
        delta = float(json['d'])
        gamma = float(json['g'])
        theta = float(json['t'])
        vega = float(json['ve'])
        rho = float(json['r'])
        open_interest = int(json['o'])
        time = datetime.strptime(json['ti'], '%Y-%m-%d %H:%M')
        return OptionDataFrame(bid_price, bid_size, ask_price, ask_size, volume, volatility, delta, gamma, theta, vega, rho, open_interest, time)

    @staticmethod
    def from_option_quote(option_quote, time):
        """Convert Questrade OptionQuote to OptionDataFrame
        Args:
            option_quote (OptionQuote): Questrade OptionQuote object
            time (datetime): Time quote was sampled
        Returns:
            OptionDataFrame
        """
        return OptionDataFrame(option_quote.bidPrice,
                               option_quote.bidSize,
                               option_quote.askPrice,
                               option_quote.askSize,
                               option_quote.volume,
                               option_quote.volatility,
                               option_quote.delta,
                               option_quote.gamma,
                               option_quote.theta,
                               option_quote.vega,
                               option_quote.rho,
                               option_quote.openInterest,
                               time)

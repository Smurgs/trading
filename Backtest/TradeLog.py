from Backtest.Action import Action

import matplotlib.pyplot as plt


class TradeLog(object):

    def __init__(self, data):
        self.data = data
        self.commission = 0
        self.equity = 1000
        self.completed_trades = []
        self.current_trade = None
        self.stats = {}

    def get_net_profit(self):
        return self.stats['all']['net_profit']

    def close_position(self, clk, data_frame):
        if self.current_trade is not None:
            self.current_trade.exit_clk = clk
            self.current_trade.exit_price = data_frame.close
            self.completed_trades.append(self.current_trade)
        self.current_trade = None

    def execute_action(self, clk, data_frame, action):
        self.current_trade = CompletedTrade()
        self.current_trade.enter_clk = clk
        self.current_trade.enter_price = data_frame.close
        self.current_trade.position = 1 if action.op == Action.Operation.BUY else -1

    def simulation_complete(self):
        # Calculate per trade values
        for trade in self.completed_trades:
            trade.trade_return = trade.position * ((trade.exit_price - trade.enter_price) / trade.enter_price)
            trade.trade_profit = (self.equity * trade.trade_return) - self.commission
            trade.trade_time = trade.exit_clk - trade.enter_clk
            if trade.position > 0:
                trade_low = min([x.close for x in self.data.data_frames[trade.enter_clk:trade.exit_clk+1]])
            else:
                trade_low = max([x.close for x in self.data.data_frames[trade.enter_clk:trade.exit_clk+1]])
            trade.trade_draw_down = trade.position * (trade_low - trade.enter_price) / trade.enter_price

        # Calculate overall statistics
        long_trades = [x for x in self.completed_trades if x.position > 0]
        short_trades = [x for x in self.completed_trades if x.position < 0]
        for key, trades in [('all', self.completed_trades), ('long', long_trades), ('short', short_trades)]:

            trade_profits = [x.trade_profit for x in trades]
            winners = [x for x in trade_profits if x > 0]
            losers = [x for x in trade_profits if x < 0]
            self.stats[key] = {
                'net_profit': sum(trade_profits),
                'gross_profit': sum(winners),
                'gross_loss': sum(losers),
                'profit_factor': 0 if sum(losers) == 0 else -1 * sum(winners) / sum(losers),
                'num_trades': len(trades),
                'num_winners': len(winners),
                'num_losers': len(losers),
                'win_percent': 0 if len(trades) == 0 else len(winners) / len(trades),
                'avg_net': 0 if len(trades) == 0 else sum(trade_profits) / len(trades),
                'avg_win': 0 if len(winners) == 0 else sum(winners) / len(winners),
                'avg_loss': 0 if len(losers) == 0 else sum(losers) / len(losers),
                'max_win': 0 if len(trade_profits) == 0 else max(trade_profits),
                'max_loss': 0 if len(trade_profits) == 0 else min(trade_profits),
                'avg_trade_time': 0 if len(trades) == 0 else sum([x.exit_clk - x.enter_clk for x in trades]) / len(
                    trades),
                'avg_win_time': 0 if len(winners) == 0 else sum(
                    [x.exit_clk - x.enter_clk for x in trades if x.trade_return > 0]) / len(winners),
                'avg_loss_time': 0 if len(losers) == 0 else sum(
                    [x.exit_clk - x.enter_clk for x in trades if x.trade_return < 0]) / len(losers)
            }

    def plot_graphs(self):
        # Equity graph
        equity = [self.equity]  # TODO: some fucked shit is going on with self.equity
        for trade in self.completed_trades:
            equity.append(equity[-1] + trade.trade_profit)
        plt.plot(equity)
        plt.title('Equity Curve')
        plt.show()

        # MAE graph
        win_draw_down = [100 * abs(x.trade_draw_down) for x in self.completed_trades if x.trade_return > 0]
        win_profit = [abs(x.trade_return) for x in self.completed_trades if x.trade_return > 0]
        lose_draw_down = [100 * abs(x.trade_draw_down) for x in self.completed_trades if x.trade_return < 0]
        lose_profit = [abs(x.trade_return) for x in self.completed_trades if x.trade_return < 0]
        plt.plot(win_draw_down, win_profit, marker='^', linestyle='None', color='green', markersize=2)
        plt.plot(lose_draw_down, lose_profit, marker='v', linestyle='None', color='red', markersize=2)
        plt.show()

    def _calculate_stats(self):
        long_trades = [x for x in self.completed_trades if x.position > 0]
        short_trades = [x for x in self.completed_trades if x.position < 0]

        for key, trades in [('all', self.completed_trades), ('long', long_trades), ('short', short_trades)]:
            trade_profits = [x.trade_profit for x in trades]
            winners = [x for x in trade_profits if x > 0]
            losers = [x for x in trade_profits if x < 0]

            self.stats[key] = {
                'net_profit': sum(trade_profits),
                'gross_profit': sum(winners),
                'gross_loss': sum(losers),
                'profit_factor': 0 if sum(losers) == 0 else -1 * sum(winners) / sum(losers),
                'num_trades': len(trades),
                'num_winners': len(winners),
                'num_losers': len(losers),
                'win_percent': 0 if len(trades) == 0 else len(winners) / len(trades),
                'avg_net': 0 if len(trades) == 0 else sum(trade_profits) / len(trades),
                'avg_win': 0 if len(winners) == 0 else sum(winners) / len(winners),
                'avg_loss': 0 if len(losers) == 0 else sum(losers) / len(losers),
                'max_win': 0 if len(trade_profits) == 0 else max(trade_profits),
                'max_loss': 0 if len(trade_profits) == 0 else min(trade_profits),
                'avg_trade_time': 0 if len(trades) == 0 else sum([x.exit_clk-x.enter_clk for x in trades]) / len(trades),
                'avg_win_time': 0 if len(winners) == 0 else sum([x.exit_clk - x.enter_clk for x in trades if x.trade_return > 0]) / len(winners),
                'avg_loss_time': 0 if len(losers) == 0 else sum([x.exit_clk - x.enter_clk for x in trades if x.trade_return < 0]) / len(losers)
            }

    def print_stats(self):
        all = self.stats['all']
        long = self.stats['long']
        short = self.stats['short']

        fmt_flt = '%-18s |%12.4f |%12.4f |%12.4f'
        fmt_int = '%-18s |%12d |%12d |%12d'
        print('------------------- Report -------------------')
        print('%-18s |%12s |%12s |%12s' % ('', 'All Trades', 'Long Trades', 'Short Trades'))
        print(fmt_flt % ('Total Net Profit', all['net_profit'], long['net_profit'], short['net_profit']))
        print(fmt_flt % ('Gross Profit', all['gross_profit'], long['gross_profit'], short['gross_profit']))
        print(fmt_flt % ('Gross Loss', all['gross_loss'], long['gross_loss'], short['gross_loss']))
        print(fmt_flt % ('Profit Factor', all['profit_factor'], long['profit_factor'], short['profit_factor']))
        print(fmt_int % ('Number of Trades', all['num_trades'], long['num_trades'], short['num_trades']))
        print(fmt_int % ('Winning Trades', all['num_winners'], long['num_winners'], short['num_winners']))
        print(fmt_int % ('Losing Trades', all['num_losers'], long['num_losers'], short['num_losers']))
        print(fmt_flt % ('Percent Profitable', all['win_percent'], long['win_percent'], short['win_percent']))
        print(fmt_flt % ('Avg Net Trade', all['avg_net'], long['avg_net'], short['avg_net']))
        print(fmt_flt % ('Avg Win Trade', all['avg_win'], long['avg_win'], short['avg_win']))
        print(fmt_flt % ('Avg Lose Trade', all['avg_loss'], long['avg_loss'], short['avg_loss']))
        print(fmt_flt % ('Largest Win', all['max_win'], long['max_win'], short['max_win']))
        print(fmt_flt % ('Largest Loss', all['max_loss'], long['max_loss'], short['max_loss']))
        print(fmt_flt % ('Avg Trade Time', all['avg_trade_time'], long['avg_trade_time'], short['avg_trade_time']))
        print(fmt_flt % ('Avg Win Time', all['avg_win_time'], long['avg_win_time'], short['avg_win_time']))
        print(fmt_flt % ('Avg Loss Time', all['avg_loss_time'], long['avg_loss_time'], short['avg_loss_time']))

    def _per_trade_metrics(self, trades, data):
        for trade in trades:
            trade.trade_return = trade.position * ((trade.exit_price - trade.enter_price) / trade.enter_price)
            trade.trade_profit = (self.equity * trade.trade_return) - self.commission
            trade.trade_time = trade.exit_clk - trade.enter_clk
            if trade.position > 0:
                trade_low = min([x.close for x in data.data_frames[trade.enter_clk:trade.exit_clk+1]])
            else:
                trade_low = max([x.close for x in data.data_frames[trade.enter_clk:trade.exit_clk+1]])
            trade.trade_draw_down = trade.position * (trade_low - trade.enter_price) / trade.enter_price

            self.equity += trade.trade_profit


class CompletedTrade(object):
    def __init__(self):
        self.enter_price = None
        self.enter_clk = None
        self.exit_price = None
        self.exit_clk = None
        self.position = None
        self.trade_draw_down = None
        self.trade_return = None
        self.trade_profit = None
        self.trade_time = None

from Backtest.Strategies.FollowMovingAverageSlope import FollowMovingAverageSlope
from Backtest.Simulator import Simulator


def main():
    simulator = Simulator(FollowMovingAverageSlope())
    simulator.run()


if __name__ == '__main__':
    main()

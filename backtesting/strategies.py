from abc import ABC, abstractmethod

from pyalgotrade import strategy
from pyalgotrade.technical import ma

from utils import safe_round


class BaseStrategy(strategy.BacktestingStrategy):
  def __init__(self, feed, instrument, startingBalance):
    super(BaseStrategy, self).__init__(feed, startingBalance)
    self.position = None
    self.instrument = instrument
    self.setUseAdjustedValues(True)

  def onEnterOk(self, position):
    execInfo = position.getEntryOrder().getExecutionInfo()
    self.info("BUY at $%.2f" % (execInfo.getPrice()))

  def onEnterCanceled(self, position):
    self.position = None

  def onExitOk(self, position):
    execInfo = position.getExitOrder().getExecutionInfo()
    self.info("SELL at $%.2f" % (execInfo.getPrice()))
    self.position = None

  def onExitCanceled(self, position):
    # If the exit was canceled, re-submit it.
    self.position.exitMarket()

  def onBars(self, bars):
    pass


class VWMAStrategy(BaseStrategy):
  def __init__(self, feed, instrument, startingBalance, smaPeriod, vwmaPeriod):
    print(feed[instrument], dir(feed[instrument]))
    self.sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)
    # VWMA: (sum(volume * close, vwmaPeriod) / sum(volume, vwmaPeriod))
    # self.vwma = ma.SMA()
    super(VWMAStrategy, self).__init__(feed, instrument, startingBalance)

  def onBars(self, bars):
    bar = bars[self.instrument]
    self.info("%s %s" % (bar.getClose(), safe_round(self.sma[-1], 2)))

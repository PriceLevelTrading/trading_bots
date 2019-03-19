import logging
import datetime as dt


class Backtester:
  def __init__(self):
    self._logger = logging.getLogger(__name__)
    self._settings = {}
    self._default_settings = {
      'Porfolio': Portfolio(),
      'Algorithm': Algorithm(),
      'Source': '',
      'Start_Day': dt.datetime(2019, 1, 1),
      'End_Day': dt.datetime.today(),
      'Ticker': '/NQ'
    }

  def set_portfolio(self, portfolio):
    self._settings['Portfolio'] = portfolio

  def set_algorithm(self, algorithm):
    self._settings['Algorithm'] = algorithm

  def set_source(self, source):
      self._settings['Source'] = source

  def set_start_date(self, date):
    self._settings['Start_Day'] = date

  def set_end_date(self, date):
    self._settings['End_Day'] = date

  def set_stock_universe(self, stock):
    self._settings['Ticker'] = stock

  def backtest():
    pass
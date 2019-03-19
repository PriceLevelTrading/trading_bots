from pyalgotrade.barfeed import quandlfeed

from strategies import VWMAStrategy


def main():
  # Load the bar feed from the CSV file
  feed = quandlfeed.Feed()
  feed.addBarsFromCSV("nflx", "WIKI-NFLX-2017-quandl.csv")

  # Evaluate the strategy with the feed's bars.
  myStrategy = VWMAStrategy(feed, "nflx", 10000, 70, 50)
  myStrategy.run()
  print("Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity())


if __name__ == "__main__":
  main()

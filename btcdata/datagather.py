import logging
import argparse
import sys
from datagatherer import Datagatherer


class DatagathererCLI:
    def __init__(self):
        pass

    def exec_command(self, args):
        if "watch" in args.command:
            self.datagatherer.loop()
        if "replay-history" in args.command:
            self.datagatherer.replay_history(args.replay_history)
        if "get-balance" in args.command:
            if not args.markets:
                logging.error("You must use --markets argument to specify markets")
                sys.exit(2)
            pmarkets = args.markets.split(",")
            pmarketsi = []
            for pmarket in pmarkets:
                exec('import private_markets.' + pmarket.lower())
                market = eval('private_markets.' + pmarket.lower()
                              + '.Private' + pmarket + '()')
                pmarketsi.append(market)
            for market in pmarketsi:
                print(market)

    def create_datagatherer(self, args):
        self.datagatherer = Datagatherer()
        if args.observers:
            self.datagatherer.init_observers(args.observers.split(","))
        if args.markets:
            self.datagatherer.init_markets(args.markets.split(","))

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="more verbose",
                            action="store_true")
        parser.add_argument("-o", "--observers", type=str,
                            help="observers, example: -oLogger,Emailer")
        parser.add_argument("-m", "--markets", type=str,
                            help="markets, example: -mMtGox,Bitstamp")
        parser.add_argument("command", nargs='*', default="watch",
                            help='verb: "watch|replay-history|get-balance"')
        args = parser.parse_args()
        level = logging.INFO
        if args.verbose:
            level = logging.DEBUG
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                            level=level)
        self.create_datagatherer(args)
        self.exec_command(args)

def main():
    cli = DatagathererCLI()
    cli.main()

if __name__ == "__main__":
    main()

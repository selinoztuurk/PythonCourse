import random


class Portfolio:
    cash = 0
    investments = {}
    log = []

    def addCash(self, amount):
        self.cash += amount
        new_log = f'Added cash: +${amount}, New cash amount: {self.cash}'
        self.log.append(new_log)

    def buy(self, num_shares, investment):
        self.cash -= investment.price * num_shares
        if investment in self.investments:
            self.investments[investment] += num_shares
        else:
            self.investments[investment] = num_shares
        new_log = f'Bought new {investment.__class__.__name__}: {num_shares} {investment.symbol}, ' \
                  f'paid ${investment.price * num_shares} cash'
        self.log.append(new_log)

    def buyStock(self, num_shares, stock):
        if not isinstance(num_shares, int):
            new_log = f'Tried to buy stock, error due to non-integer number of shares'
            self.log.append(new_log)
            return
        self.buy(num_shares, stock)

    def buyMutualFund(self, num_shares, mutual_fund):
        if not isinstance(num_shares, float):
            new_log = f'Tried to buy mutual fund, error due to integer number of shares'
            self.log.append(new_log)
            return
        self.buy(num_shares, mutual_fund)

    def sell(self, investment, num_shares, min_range, max_range):
        x = self.investments[investment]
        if x >= num_shares:
            self.investments[investment] -= num_shares
            sell_price = random.uniform(investment.price*min_range, investment.price*max_range)
            self.cash += sell_price * num_shares
            new_log = f'Sold {investment.__class__.__name__}: {num_shares} {investment.symbol}, ' \
                      f'at price {sell_price} for each share'
            self.log.append(new_log)
        else:
            new_log = f'Tried to sell {num_shares} shares of {investment.symbol}, ' \
                          f'error due to insufficient amount of shares.'
            self.log.append(new_log)

    def sellStock(self, stock_symbol, num_shares):
        if not isinstance(num_shares, int):
            new_log = f'Tried to sell stock, error due to non-integer number of shares'
            self.log.append(new_log)
            return
        for investment in self.investments:
            if investment.symbol == stock_symbol and isinstance(investment, Stock):
                self.sell(investment, num_shares, 0.5, 1.5)
                return
            else:
                continue
        new_log = f'Tried to sell {num_shares} shares of {stock_symbol}, ' \
                  f'error due to lack of {stock_symbol} in the portfolio.'
        self.log.append(new_log)

    def sellMutualFund(self, mutual_fund_symbol, num_shares):
        if not isinstance(num_shares, float):
            new_log = f'Tried to sell mutual fund, error due to integer number of shares'
            self.log.append(new_log)
            return
        for investment in self.investments:
            if investment.symbol == mutual_fund_symbol and isinstance(investment, MutualFund):
                self.sell(investment, num_shares, 0.9, 1.2)
                return
            else:
                continue
        new_log = f'Tried to sell {num_shares} shares of {mutual_fund_symbol}, ' \
                  f'error due to lack of {mutual_fund_symbol} in the portfolio.'
        self.log.append(new_log)

    def withdrawCash(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            new_log = f'Withdrew cash: -${amount}, New cash amount: {self.cash}'
            self.log.append(new_log)
        else:
            new_log = f'Tried to withdraw ${amount}, error due to lack of cash.'
            self.log.append(new_log)

    def __str__(self):

        nicely_formatted_lines = {}
        for investment in self.investments:
            if investment.__class__.__name__ not in nicely_formatted_lines:
                nicely_formatted_lines[investment.__class__.__name__] = []
            new_line = f'{self.investments[investment]} {investment.symbol}'
            nicely_formatted_lines[investment.__class__.__name__].append(new_line)

        string_to_be_returned = f'\nCurrent Portfolio: \nCash: ${self.cash} '
        for eachClass in nicely_formatted_lines.keys():
            string_to_be_returned += f'\n{eachClass}:'
            for line in nicely_formatted_lines[eachClass]:
                string_to_be_returned += f'\n{line}'

        return string_to_be_returned

    def history(self):
        print("\nTransaction History:")
        for log in self.log:
            print(log)


class Investment:

    def __init__(self, price, symbol):
        self.symbol = symbol
        self.price = price


class Stock(Investment):

    pass


class MutualFund(Investment):

    def __init__(self, symbol):
        super().__init__(1, symbol)


portfolio = Portfolio()
portfolio.addCash(300.50)
s = Stock(20, "HFH")
portfolio.buyStock(5, s)
mf1 = MutualFund("BRT")
mf2 = MutualFund("GHT")
portfolio.buyMutualFund(10.3, mf1)
portfolio.buyMutualFund(2, mf2)  # Error, whole number
portfolio.buyMutualFund(2.0, mf2)
print(portfolio)
portfolio.sellMutualFund("BRT", 3)  # Error, whole number
portfolio.sellMutualFund("BRT", 3.0)
portfolio.sellStock("HFH", 1)
portfolio.withdrawCash(50)
portfolio.history()

# additional test cases

portfolio.withdrawCash(200)  # Error, lack of cash
portfolio.addCash(500)

portfolio.buyStock(10.5, s)  # Error, fraction number
portfolio.sellStock("HFH", 10.5)  # Error, fraction number
portfolio.buyMutualFund(10, s)  # Error, whole number
portfolio.sellMutualFund("BRT", 10)  # Error, whole number

portfolio.sellStock("ERR", 10)  # Error, non-existing investment
portfolio.sellMutualFund("ERR", 1)  # Error, non-existing investment

print(portfolio)
portfolio.history()


# bonus

class Bond(Investment):

    pass


b = Bond(50, "BON")
portfolio.buy(5, b)
portfolio.sell(b, 2, 1, 2)
print(portfolio)
portfolio.history()
